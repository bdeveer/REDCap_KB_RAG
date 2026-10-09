#!/usr/bin/env python3
"""
REDCap Longitudinal Structure Generator

Reads a JSON spec describing arms, events, and instrument designations,
then writes the CSV files REDCap expects for import (KB RC-IMP-09).

Usage:
    python generate_longitudinal.py --spec spec.json --output-dir ./output/
    python generate_longitudinal.py --spec spec.json --preview

Spec format (top-level keys: "arms", "events", "mapping" -- nothing else):
{
  "arms": [
    {"arm_num": 1, "name": "Treatment"},       # "arm_name" is accepted as an alias
    {"arm_num": 2, "name": "Control"}
  ],
  "events": [
    {
      "event_name": "Baseline",
      "arm_num": 1,
      "day_offset": 0,
      "offset_min": 0,           # optional -- days BEFORE day_offset (window), default 0
      "offset_max": 0,           # optional -- days AFTER day_offset (window), default 0
      "custom_event_label": ""   # optional -- piped label, e.g. "[visit_date]"
    }
  ],
  "mapping": [
    {"event_name": "Baseline", "arm_num": 1, "form": "demographics"},
    {"unique_event_name": "baseline_arm_1", "form": "consent"}
  ]
}

Notes:
- The key is "mapping" (singular). Any other top-level key (e.g. "mappings")
  is an error, so a misnamed key can never silently drop the designations file.
- Mapping rows reference an event either by event_name + arm_num (preferred)
  or by its expected unique_event_name.
- Events.csv leaves unique_event_name BLANK so REDCap generates it on import.
  (Supplying a value means "modify the existing event with this name" --
  RC-API-20.) Only set unique_event_name on an event when you really mean that.
- The unique_event_names written to InstrumentDesignations.csv are PREDICTED
  from REDCap's documented algorithm (RC-LONG-01). Verify them against a real
  events export (export_events / Download events) after importing Events.csv.
- Arms.csv is written only for multi-arm projects; arm 1 is created
  automatically when longitudinal mode is enabled (RC-IMP-09).
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from io import StringIO
from pathlib import Path

# Windows consoles default to cp1252, which cannot print the report symbols.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


ALLOWED_TOP_KEYS = {"arms", "events", "mapping"}

EVENTS_HEADER = [
    "event_name", "arm_num", "day_offset", "offset_min", "offset_max",
    "unique_event_name", "custom_event_label",
]


# ---------------------------------------------------------------------------
# unique_event_name prediction
# ---------------------------------------------------------------------------

def derive_unique_event_name(event_name: str, arm_num: int) -> str:
    """
    PREDICT the unique_event_name REDCap will generate (RC-LONG-01).

    REDCap generates the real value on import; this is only an expectation used
    to build the designations file. Documented rules:
      1. Lowercase the event name.
      2. Remove hyphens entirely (they are joiners, not separators).
         e.g. "Follow-up" -> "followup"   (NOT "follow_up")
      3. Replace every remaining non-alphanumeric character with an underscore.
      4. Collapse consecutive underscores into one.
      5. Strip leading/trailing underscores.
      6. Append "_arm_N".

    Accented characters are transliterated to their unaccented equivalents
    (REDCap 17.3.0+ behavior for newly created projects; older projects may
    keep the accents). The KB documents no length/truncation rule, so none is
    applied -- verify long names against a real export.
    """
    slug = unicodedata.normalize("NFKD", event_name)
    slug = "".join(ch for ch in slug if not unicodedata.combining(ch))
    slug = slug.lower()
    slug = slug.replace("-", "")               # step 2: hyphens removed, not replaced
    slug = re.sub(r"[^a-z0-9]+", "_", slug)   # step 3: everything else -> underscore
    slug = re.sub(r"_+", "_", slug)            # step 4: collapse consecutive underscores
    slug = slug.strip("_")                     # step 5: strip edges
    return f"{slug}_arm_{arm_num}"


def event_key(evt: dict) -> str:
    """Expected unique_event_name for a spec event (explicit value wins)."""
    return evt.get("unique_event_name") or derive_unique_event_name(
        evt.get("event_name", ""), evt.get("arm_num", 1)
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_spec(spec: dict) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors stop generation."""
    errors, warnings = [], []

    if not isinstance(spec, dict):
        return ["Spec must be a JSON object with keys: arms, events, mapping."], []

    unknown = set(spec) - ALLOWED_TOP_KEYS
    for key in sorted(unknown):
        hint = " (did you mean 'mapping'?)" if key.lower().startswith(("mapping", "designation", "instrument")) else ""
        errors.append(f"Unknown top-level key '{key}'{hint}. Allowed keys: arms, events, mapping.")

    for key in ALLOWED_TOP_KEYS:
        if key in spec and not isinstance(spec[key], list):
            errors.append(f"'{key}' must be a list.")
    if errors:
        return errors, warnings

    arms = spec.get("arms", [])
    events = spec.get("events", [])
    mapping = spec.get("mapping", [])

    if not events:
        errors.append("No events in spec -- nothing to generate.")
        return errors, warnings

    for evt in events:
        if not str(evt.get("event_name", "")).strip():
            errors.append(f"Event with no event_name: {evt}")
        for col in ("day_offset", "offset_min", "offset_max"):
            val = evt.get(col)
            if val is None:
                continue
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                errors.append(f"Event '{evt.get('event_name')}': {col} must be a number, got {val!r}.")
            elif val < 0:
                errors.append(
                    f"Event '{evt.get('event_name')}': {col}={val} is negative. "
                    "offset_min/offset_max are window widths in days (positive numbers), "
                    "and day_offset must be >= 0."
                )
        if evt.get("unique_event_name"):
            warnings.append(
                f"Event '{evt.get('event_name')}' sets unique_event_name="
                f"'{evt['unique_event_name']}'. On import REDCap treats this as MODIFYING an "
                "existing event with that name, not creating a new one (RC-API-20). "
                "Remove it unless that is intended."
            )

    arm_nums = {a.get("arm_num") for a in arms if "arm_num" in a}
    event_arm_nums = {e.get("arm_num", 1) for e in events}

    missing_arms = event_arm_nums - arm_nums
    if arms and missing_arms:
        warnings.append(
            f"Events reference arm_num(s) not in the arms list: {sorted(missing_arms)}. "
            "They will be added to Arms.csv with auto-generated names ('Arm N')."
        )
    all_arms = arm_nums | event_arm_nums
    if all_arms and all_arms != {1} and len(all_arms) == 1:
        warnings.append(
            f"Single-arm project uses arm_num {sorted(all_arms)[0]}. Arm 1 is the arm REDCap "
            "creates automatically -- use arm_num 1 for single-arm projects."
        )

    # Duplicate events within an arm (same name or same predicted unique name)
    seen: dict[tuple, str] = {}
    for evt in events:
        k = (evt.get("arm_num", 1), event_key(evt))
        if k in seen:
            errors.append(
                f"Arm {k[0]}: events '{seen[k]}' and '{evt.get('event_name')}' both map to "
                f"unique_event_name '{k[1]}'. Rename one so each event in an arm is distinct."
            )
        else:
            seen[k] = evt.get("event_name", "")

    if any(not str(e.get("event_name", "")).isascii() for e in events):
        warnings.append(
            "Some event names contain non-ASCII characters. Predicted names assume REDCap "
            "17.3.0+ transliteration of accents; projects created earlier may differ. "
            "Verify against an events export."
        )

    if not mapping:
        warnings.append(
            "No 'mapping' rows in spec -- InstrumentDesignations.csv will NOT be generated."
        )

    # Check for ordering ambiguity: multiple events sharing the same day_offset within an arm.
    # REDCap sorts ties alphabetically by unique_event_name, which is usually not the
    # intended clinical order. Warn and show what the alphabetical order will be.
    arm_day_events: dict = defaultdict(list)
    for evt in events:
        key = (evt.get("arm_num", 1), evt.get("day_offset", 0))
        arm_day_events[key].append(evt)

    for (arm_num, day_offset), evts in sorted(arm_day_events.items()):
        if len(evts) > 1:
            names = [e.get("event_name", "") for e in evts]
            sorted_names = [e.get("event_name", "") for e in sorted(evts, key=event_key)]
            if names != sorted_names:
                warnings.append(
                    f"Arm {arm_num}: {len(names)} events share day_offset={day_offset}. "
                    f"REDCap will display them alphabetically by unique_event_name — "
                    f"which may not be your intended order. "
                    f"Alphabetical order will be: {' → '.join(sorted_names)}. "
                    f"To enforce a specific order, assign sequential day_offsets "
                    f"(e.g. 0, 1, 2, ...) even for same-day events."
                )

    return errors, warnings


# ---------------------------------------------------------------------------
# CSV generation
# ---------------------------------------------------------------------------

def resolve_arms(arms: list[dict], events: list[dict]) -> list[dict]:
    """Arms from the spec plus any arm referenced by events (auto-named 'Arm N')."""
    by_num = {}
    for arm in arms:
        if "arm_num" in arm:
            num = arm["arm_num"]
            by_num[num] = arm.get("name") or arm.get("arm_name") or f"Arm {num}"
    for evt in events:
        num = evt.get("arm_num", 1)
        by_num.setdefault(num, f"Arm {num}")
    return [{"arm_num": n, "name": by_num[n]} for n in sorted(by_num)]


def generate_arms_csv(arms: list[dict]) -> str:
    """Return Arms CSV content as a string (columns per RC-IMP-09: arm_num,name)."""
    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["arm_num", "name"])
    for arm in arms:
        writer.writerow([arm["arm_num"], arm["name"]])
    return buf.getvalue()


def generate_events_csv(events: list[dict]) -> tuple[str, list[dict]]:
    """
    Return Events CSV content and the enriched events list.

    The CSV leaves unique_event_name blank (REDCap generates it) unless the spec
    explicitly sets one. The enriched list carries the EXPECTED unique name,
    used only for the designations file and the summary.
    """
    enriched = []
    for evt in events:
        enriched.append({
            "event_name": evt.get("event_name", ""),
            "arm_num": evt.get("arm_num", 1),
            "day_offset": evt.get("day_offset", 0),
            "offset_min": evt.get("offset_min", 0),
            "offset_max": evt.get("offset_max", 0),
            "unique_event_name": evt.get("unique_event_name", ""),
            "custom_event_label": evt.get("custom_event_label", ""),
            "expected_unique_event_name": event_key(evt),
        })

    # Sort by arm, then day_offset
    enriched.sort(key=lambda e: (e["arm_num"], e["day_offset"]))

    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(EVENTS_HEADER)
    for evt in enriched:
        writer.writerow([evt[col] for col in EVENTS_HEADER])
    return buf.getvalue(), enriched


def generate_mapping_csv(mapping: list[dict], enriched_events: list[dict]) -> tuple[str, int, list[str]]:
    """
    Return (Instrument Designations CSV content, rows written, warnings).

    Each mapping row is resolved to an event by event_name + arm_num or by
    unique_event_name. Rows that match no event are skipped with a warning.
    """
    by_uen = {e["expected_unique_event_name"]: e for e in enriched_events}
    by_name = {(e["arm_num"], e["event_name"].strip().lower()): e for e in enriched_events}

    warnings = []
    written = set()
    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["arm_num", "unique_event_name", "form"])
    for row in mapping:
        form = str(row.get("form", "")).strip()
        if not form:
            warnings.append(f"Mapping row with empty form skipped: {row}")
            continue
        if row.get("unique_event_name"):
            evt = by_uen.get(row["unique_event_name"])
            ref = row["unique_event_name"]
        else:
            arm = row.get("arm_num", 1)
            evt = by_name.get((arm, str(row.get("event_name", "")).strip().lower()))
            ref = f"'{row.get('event_name', '')}' (arm {arm})"
        if evt is None:
            warnings.append(f"Mapping row skipped -- event {ref} not found in events (form '{form}').")
            continue
        if "arm_num" in row and row["arm_num"] != evt["arm_num"]:
            warnings.append(
                f"Mapping row skipped -- arm_num {row['arm_num']} does not match event "
                f"{evt['expected_unique_event_name']} (arm {evt['arm_num']}), form '{form}'."
            )
            continue
        key = (evt["arm_num"], evt["expected_unique_event_name"], form)
        if key in written:
            warnings.append(f"Duplicate mapping row ignored: {key[1]} / {form}")
            continue
        written.add(key)
        writer.writerow(list(key))
    return buf.getvalue(), len(written), warnings


# ---------------------------------------------------------------------------
# Preview renderer
# ---------------------------------------------------------------------------

def preview(arms_csv: str, events_csv: str, mapping_csv: str) -> None:
    for title, content in (
        ("Arms.csv", arms_csv),
        ("Events.csv", events_csv),
        ("InstrumentDesignations.csv", mapping_csv),
    ):
        print(f"\n{'='*60}")
        print(f"  PREVIEW: {title}")
        print(f"{'='*60}")
        print(content.strip() if content else "(not generated)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate REDCap longitudinal structure CSV files from a JSON spec."
    )
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file")
    parser.add_argument("--output-dir", help="Directory to write the CSV files")
    parser.add_argument("--preview", action="store_true",
                        help="Print CSV content to stdout instead of writing files")
    args = parser.parse_args()

    if not args.output_dir and not args.preview:
        print("Error: provide --output-dir or --preview", file=sys.stderr)
        sys.exit(1)

    # Load spec
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"Error: spec file not found: {args.spec}", file=sys.stderr)
        sys.exit(1)

    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)

    # Validate
    errors, warnings = validate_spec(spec)
    if errors:
        print("\n✗ Errors (nothing generated):", file=sys.stderr)
        for e in errors:
            print(f"  • {e}", file=sys.stderr)
        sys.exit(1)

    events = spec.get("events", [])
    mapping = spec.get("mapping", [])
    arms = resolve_arms(spec.get("arms", []), events)
    multi_arm = len(arms) > 1

    # Generate
    arms_csv = generate_arms_csv(arms) if multi_arm else ""
    events_csv, enriched_events = generate_events_csv(events)
    mapping_csv, mapping_rows, map_warnings = (
        generate_mapping_csv(mapping, enriched_events) if mapping else ("", 0, [])
    )
    warnings.extend(map_warnings)

    if warnings:
        print("\n⚠  Warnings:", file=sys.stderr)
        for w in warnings:
            print(f"  • {w}", file=sys.stderr)

    # Summary
    print(f"\nGenerated:")
    if multi_arm:
        print(f"  Arms                   : {len(arms)} row(s)")
    else:
        print(f"  Arms                   : skipped (single arm -- arm 1 is created automatically;"
              f" rename it in Define My Events if needed: '{arms[0]['name']}')")
    print(f"  Events                 : {len(enriched_events)} row(s) (unique_event_name left blank for REDCap)")
    print(f"  Instrument Designations: {mapping_rows} row(s)" if mapping_csv
          else "  Instrument Designations: NOT generated (no 'mapping' rows)")

    print(f"\n  EXPECTED unique_event_names (predicted -- REDCap generates the real values;")
    print(f"  verify against an events export after importing Events.csv):")
    for evt in enriched_events:
        print(f"    {evt['event_name']} (Arm {evt['arm_num']})  →  {evt['expected_unique_event_name']}")

    if args.preview:
        preview(arms_csv, events_csv, mapping_csv)
        return

    # Write files
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files_written = []
    for name, content in (
        ("Arms.csv", arms_csv),
        ("Events.csv", events_csv),
        ("InstrumentDesignations.csv", mapping_csv),
    ):
        if content:
            p = out_dir / name
            p.write_text(content, encoding="utf-8")
            files_written.append(str(p))

    print(f"\nFiles written to {out_dir}:")
    for f in files_written:
        print(f"  {f}")


if __name__ == "__main__":
    main()

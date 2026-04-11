#!/usr/bin/env python3
"""
REDCap Longitudinal Structure Generator

Reads a JSON spec describing arms, events, and instrument designations,
then writes the three CSV files REDCap expects for import.

Usage:
    python generate_longitudinal.py --spec spec.json --output-dir ./output/
    python generate_longitudinal.py --spec spec.json --preview

Spec format:
{
  "arms": [
    {"arm_num": 1, "arm_name": "Treatment"},
    {"arm_num": 2, "arm_name": "Control"}
  ],
  "events": [
    {
      "event_name": "Baseline",
      "arm_num": 1,
      "day_offset": 0,
      "offset_min": 0,       # optional — defaults to day_offset
      "offset_max": 0        # optional — defaults to day_offset
    }
  ],
  "mapping": [
    {"unique_event_name": "baseline_arm_1", "form": "demographics"}
  ]
}

Notes:
- unique_event_name in events is auto-derived if omitted.
- mapping rows reference unique_event_name; the script validates they match known events.
- offset_min/offset_max default to day_offset if omitted (no visit window).
"""

import argparse
import csv
import json
import re
import sys
from io import StringIO
from pathlib import Path


# ---------------------------------------------------------------------------
# unique_event_name derivation
# ---------------------------------------------------------------------------

def derive_unique_event_name(event_name: str, arm_num: int) -> str:
    """
    Replicate REDCap's auto-generation of unique_event_name.
    Rule: lowercase, strip non-alphanumeric (keep underscores), collapse
    runs of underscores/spaces into a single underscore, append _arm_N.
    """
    slug = event_name.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return f"{slug}_arm_{arm_num}"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_spec(spec: dict) -> list[str]:
    """Return a list of warning/error strings. Empty = valid."""
    warnings = []

    arms = spec.get("arms", [])
    events = spec.get("events", [])
    mapping = spec.get("mapping", [])

    arm_nums = {a.get("arm_num") for a in arms if "arm_num" in a}
    event_arm_nums = {e.get("arm_num") for e in events if "arm_num" in e}

    # Arms referenced in events but not defined in arms list
    if arms:
        missing_arms = event_arm_nums - arm_nums
        if missing_arms:
            warnings.append(
                f"Events reference arm_num(s) not in the arms list: {sorted(missing_arms)}. "
                "They will be included with auto-generated names."
            )

    # Build the full unique_event_name → arm_num lookup
    event_lookup: dict[str, int] = {}
    for evt in events:
        uen = evt.get("unique_event_name") or derive_unique_event_name(
            evt.get("event_name", ""), evt.get("arm_num", 1)
        )
        event_lookup[uen] = evt.get("arm_num", 1)

    # Mapping entries referencing unknown events
    unknown_events = set()
    for row in mapping:
        uen = row.get("unique_event_name", "")
        if uen and uen not in event_lookup:
            unknown_events.add(uen)
    if unknown_events:
        warnings.append(
            f"Mapping references unique_event_name(s) not found in events: "
            + ", ".join(sorted(unknown_events))
        )

    # Forms with empty name
    empty_forms = [r for r in mapping if not r.get("form", "").strip()]
    if empty_forms:
        warnings.append(f"{len(empty_forms)} mapping row(s) have an empty form name — skipped.")

    return warnings


# ---------------------------------------------------------------------------
# CSV generation
# ---------------------------------------------------------------------------

def generate_arms_csv(arms: list[dict]) -> str:
    """Return Arms CSV content as a string."""
    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["arm_num", "arm_name"])
    for arm in sorted(arms, key=lambda a: a.get("arm_num", 0)):
        writer.writerow([arm["arm_num"], arm.get("arm_name", f"Arm {arm['arm_num']}")])
    return buf.getvalue()


def generate_events_csv(events: list[dict]) -> tuple[str, list[dict]]:
    """
    Return Events CSV content and the enriched events list
    (with unique_event_name filled in).
    """
    enriched = []
    for evt in events:
        day = evt.get("day_offset", 0)
        uen = evt.get("unique_event_name") or derive_unique_event_name(
            evt.get("event_name", ""), evt.get("arm_num", 1)
        )
        enriched.append({
            "event_name": evt.get("event_name", ""),
            "arm_num": evt.get("arm_num", 1),
            "day_offset": day,
            "offset_min": evt.get("offset_min", day),
            "offset_max": evt.get("offset_max", day),
            "unique_event_name": uen,
        })

    # Sort by arm, then day_offset
    enriched.sort(key=lambda e: (e["arm_num"], e["day_offset"]))

    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["event_name", "arm_num", "day_offset", "offset_min", "offset_max", "unique_event_name"])
    for evt in enriched:
        writer.writerow([
            evt["event_name"],
            evt["arm_num"],
            evt["day_offset"],
            evt["offset_min"],
            evt["offset_max"],
            evt["unique_event_name"],
        ])
    return buf.getvalue(), enriched


def generate_mapping_csv(mapping: list[dict], enriched_events: list[dict]) -> str:
    """
    Return Instrument Designations CSV content.
    Resolves arm_num for each mapping row from the enriched_events lookup.
    """
    uen_to_arm = {e["unique_event_name"]: e["arm_num"] for e in enriched_events}

    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["arm_num", "unique_event_name", "form"])
    for row in mapping:
        form = row.get("form", "").strip()
        if not form:
            continue
        uen = row.get("unique_event_name", "")
        arm_num = uen_to_arm.get(uen, row.get("arm_num", ""))
        writer.writerow([arm_num, uen, form])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Preview renderer
# ---------------------------------------------------------------------------

def preview(arms_csv: str, events_csv: str, mapping_csv: str) -> None:
    sep = "-" * 60

    print(f"\n{'='*60}")
    print("  PREVIEW: Arms.csv")
    print(f"{'='*60}")
    print(arms_csv.strip())

    print(f"\n{'='*60}")
    print("  PREVIEW: Events.csv")
    print(f"{'='*60}")
    print(events_csv.strip())

    print(f"\n{'='*60}")
    print("  PREVIEW: InstrumentDesignations.csv")
    print(f"{'='*60}")
    print(mapping_csv.strip())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate REDCap longitudinal structure CSV files from a JSON spec."
    )
    parser.add_argument("--spec", required=True, help="Path to the JSON spec file")
    parser.add_argument("--output-dir", help="Directory to write the three CSV files")
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

    arms = spec.get("arms", [])
    events = spec.get("events", [])
    mapping = spec.get("mapping", [])

    # Validate
    warnings = validate_spec(spec)
    if warnings:
        print("\n⚠  Warnings:", file=sys.stderr)
        for w in warnings:
            print(f"  • {w}", file=sys.stderr)

    # Generate
    arms_csv = generate_arms_csv(arms) if arms else ""
    events_csv, enriched_events = generate_events_csv(events) if events else ("", [])
    mapping_csv = generate_mapping_csv(mapping, enriched_events) if mapping else ""

    # Summary
    print(f"\nGenerated:")
    print(f"  Arms                  : {len(arms)} row(s)")
    print(f"  Events                : {len(enriched_events)} row(s)")
    print(f"  Instrument Designations: {sum(1 for r in mapping if r.get('form','').strip())} row(s)")

    # Show unique_event_name mapping so the user can verify
    if enriched_events:
        print(f"\n  unique_event_name mapping (auto-derived where not specified):")
        for evt in enriched_events:
            note = "" if spec.get("events") and any(
                e.get("unique_event_name") == evt["unique_event_name"]
                for e in spec["events"]
            ) else "  ← auto-derived"
            print(f"    {evt['event_name']} (Arm {evt['arm_num']})  →  {evt['unique_event_name']}{note}")

    if args.preview:
        preview(arms_csv, events_csv, mapping_csv)
        return

    # Write files
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files_written = []

    if arms_csv:
        p = out_dir / "Arms.csv"
        p.write_text(arms_csv, encoding="utf-8")
        files_written.append(str(p))

    if events_csv:
        p = out_dir / "Events.csv"
        p.write_text(events_csv, encoding="utf-8")
        files_written.append(str(p))

    if mapping_csv:
        p = out_dir / "InstrumentDesignations.csv"
        p.write_text(mapping_csv, encoding="utf-8")
        files_written.append(str(p))

    print(f"\nFiles written to {out_dir}:")
    for f in files_written:
        print(f"  {f}")


if __name__ == "__main__":
    main()

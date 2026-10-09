#!/usr/bin/env python3
"""
REDCap Longitudinal Structure Parser

Parses the three CSVs that define a REDCap longitudinal project:
  - Arms CSV         (arm_num, arm_name/name)
  - Events CSV       (event_name, arm_num, day_offset, offset_min, offset_max,
                      unique_event_name, custom_event_label)
  - Mapping CSV      (arm_num, unique_event_name, form)  [instrument designations]

Each file may instead be the JSON array returned by the API / MCP exports
(export_arms, export_events, export_instrument_event_mappings) -- same keys.
offset_min/offset_max are window widths in days before/after day_offset.

Usage:
    python parse_longitudinal.py [--arms PATH] [--events PATH] [--mapping PATH] [--json]

Any of the three file flags can be omitted — the script works with whatever is available.
--json outputs machine-readable JSON; default is a human-readable text report.
"""

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

# Windows consoles default to cp1252, which cannot print the report symbols.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(value) -> str:
    """Normalize a cell to a stripped string (None -> '', numbers -> str)."""
    return "" if value is None else str(value).strip()


def open_csv(path: str) -> list[dict]:
    """
    Open a CSV (BOM/encoding resilient) or a JSON array as returned by the
    API exports (export_arms / export_events / export_instrument_event_mappings;
    keys match the CSV columns). Returns list of row dicts with string values.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    for encoding in ("utf-8-sig", "latin-1"):
        try:
            text = p.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if p.suffix.lower() == ".json" or text.lstrip().startswith("["):
        data = json.loads(text)
        if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
            raise ValueError(f"{path}: expected a JSON array of objects.")
        rows = data
    else:
        rows = list(csv.DictReader(text.splitlines()))

    # Strip whitespace from keys and values; short rows give None values,
    # extra cells land under a None key -- both are dropped/blanked here.
    return [{k.strip(): _clean(v) for k, v in row.items() if k} for row in rows]


def detect_file_type(rows: list[dict]) -> str:
    """
    Auto-detect which of the three CSV types this is based on column names.
    Returns 'arms', 'events', 'mapping', or 'unknown'.
    """
    if not rows:
        return "unknown"
    cols = set(k.lower() for k in rows[0].keys())

    # Mapping has 'form' and 'unique_event_name' but NOT 'day_offset'
    if "form" in cols and ("unique_event_name" in cols or "arm_num" in cols):
        if "day_offset" not in cols and "event_name" not in cols:
            return "mapping"

    # Events has 'event_name' and 'day_offset' or 'unique_event_name'
    if "event_name" in cols or "unique_event_name" in cols:
        if "day_offset" in cols or "unique_event_name" in cols:
            return "events"

    # Arms has arm_num + arm_name (or just 'name')
    if "arm_num" in cols and ("arm_name" in cols or "name" in cols):
        if "event_name" not in cols and "form" not in cols:
            return "arms"

    return "unknown"


# ---------------------------------------------------------------------------
# Parsers for each file type
# ---------------------------------------------------------------------------

def parse_arms(rows: list[dict]) -> list[dict]:
    """Parse Arms CSV rows into normalized dicts."""
    arms = []
    for row in rows:
        cols = {k.lower(): v for k, v in row.items()}
        arm_num = cols.get("arm_num", "").strip()
        name = cols.get("arm_name") or cols.get("name") or ""
        if arm_num:
            try:
                arms.append({"arm_num": int(arm_num), "arm_name": name.strip()})
            except ValueError:
                pass  # skip malformed rows
    arms.sort(key=lambda a: a["arm_num"])
    return arms


def parse_events(rows: list[dict]) -> list[dict]:
    """Parse Events CSV rows into normalized dicts."""
    events = []
    for row in rows:
        cols = {k.lower(): v for k, v in row.items()}
        event_name = (cols.get("event_name") or "").strip()
        arm_num_raw = (cols.get("arm_num") or "").strip()
        unique_event_name = (cols.get("unique_event_name") or "").strip()

        try:
            arm_num = int(arm_num_raw)
        except ValueError:
            continue

        predicted = not unique_event_name
        if predicted:
            # Upload-style files (e.g. from redcap-longitudinal-builder) leave
            # this blank; REDCap generates it on import. Predict it so the
            # mapping can still be cross-checked.
            unique_event_name = predict_unique_event_name(event_name, arm_num)

        event = {
            "event_name": event_name,
            "arm_num": arm_num,
            "day_offset": to_number_or_none(cols.get("day_offset")),
            # Window widths in days. The CSV uses positive numbers; the API
            # export returns offset_min as a negative number -- normalize.
            "offset_min": abs_or_none(to_number_or_none(cols.get("offset_min"))),
            "offset_max": abs_or_none(to_number_or_none(cols.get("offset_max"))),
            "unique_event_name": unique_event_name,
            "custom_event_label": (cols.get("custom_event_label") or "").strip(),
        }
        if predicted:
            event["unique_event_name_predicted"] = True
        if (cols.get("event_id") or "").strip():
            event["event_id"] = cols["event_id"].strip()
        events.append(event)

    # Sort by arm_num, then day_offset; same-day ties by unique_event_name
    # (REDCap's own tiebreak). Without day_offset, keep file order.
    events.sort(key=event_sort_key)
    return events


def predict_unique_event_name(event_name: str, arm_num: int) -> str:
    """REDCap's documented algorithm (RC-LONG-01); a prediction, not ground truth."""
    slug = unicodedata.normalize("NFKD", event_name)
    slug = "".join(ch for ch in slug if not unicodedata.combining(ch)).lower()
    slug = slug.replace("-", "")
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return f"{slug}_arm_{arm_num}"


def to_number_or_none(s):
    """'28' -> 28, '28.5' -> 28.5, '' / junk -> None."""
    try:
        n = float((s or "").strip())
    except ValueError:
        return None
    return int(n) if n.is_integer() else n


def abs_or_none(n):
    return None if n is None else abs(n)


def event_sort_key(e):
    has_day = e["day_offset"] is not None
    return (e["arm_num"], e["day_offset"] if has_day else 0,
            e["unique_event_name"] if has_day else "")


def parse_mapping(rows: list[dict]) -> list[dict]:
    """Parse Instrument Designation CSV rows into normalized dicts."""
    mapping = []
    for row in rows:
        cols = {k.lower(): v for k, v in row.items()}
        arm_num_raw = (cols.get("arm_num") or "").strip()
        unique_event_name = (cols.get("unique_event_name") or "").strip()
        form = (cols.get("form") or "").strip()

        if not form:
            continue
        try:
            arm_num = int(arm_num_raw)
        except ValueError:
            arm_num = None

        mapping.append({
            "arm_num": arm_num,
            "unique_event_name": unique_event_name,
            "form": form,
        })
    return mapping


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def build_analysis(arms, events, mapping):
    """Build a structured analysis dict from the parsed data."""

    # Index events by arm
    events_by_arm = defaultdict(list)
    for e in events:
        events_by_arm[e["arm_num"]].append(e)

    # Index mapping: unique_event_name -> list of forms
    forms_by_event = defaultdict(list)
    for m in mapping:
        forms_by_event[m["unique_event_name"]].append(m["form"])

    # Determine all known arm numbers (union of arms, events, mapping sources)
    arm_nums_from_arms = {a["arm_num"] for a in arms}
    arm_nums_from_events = {e["arm_num"] for e in events}
    arm_nums_from_mapping = {m["arm_num"] for m in mapping if m["arm_num"] is not None}
    all_arm_nums = sorted(arm_nums_from_arms | arm_nums_from_events | arm_nums_from_mapping)

    # Build arm name lookup — fall back to "Arm N" if name not in arms file
    arm_name_lookup = {a["arm_num"]: a["arm_name"] for a in arms}
    for num in all_arm_nums:
        if num not in arm_name_lookup:
            arm_name_lookup[num] = f"Arm {num}"

    # All unique forms (ordered by first appearance)
    seen_forms = []
    seen_set = set()
    for m in mapping:
        if m["form"] not in seen_set:
            seen_forms.append(m["form"])
            seen_set.add(m["form"])

    # Identify flags / issues
    issues = []

    # Forms in mapping but (potentially) not in any event
    all_event_names = {e["unique_event_name"] for e in events}
    mapping_event_names = {m["unique_event_name"] for m in mapping}

    if events and mapping:
        orphan_events_in_mapping = mapping_event_names - all_event_names
        if orphan_events_in_mapping:
            issues.append(
                f"Instrument designations reference event(s) not found in the Events file: "
                + ", ".join(sorted(orphan_events_in_mapping))
            )

        events_with_no_forms = all_event_names - mapping_event_names
        if events_with_no_forms:
            issues.append(
                f"Event(s) with no forms assigned: "
                + ", ".join(sorted(events_with_no_forms))
            )

    predicted = [e["unique_event_name"] for e in events if e.get("unique_event_name_predicted")]
    if predicted:
        issues.append(
            "Events file has blank unique_event_name (normal for an upload file). Names marked "
            "'~' were PREDICTED -- verify against a real events export after import: "
            + ", ".join(predicted)
        )

    # Check for forms never assigned anywhere
    if mapping and not seen_forms:
        issues.append("Mapping file contains no valid form assignments.")

    # Forms assigned to all events (universal)
    universal_forms = []
    if events and mapping:
        all_unique_events = [e["unique_event_name"] for e in events]
        for form in seen_forms:
            assigned_events = {
                m["unique_event_name"] for m in mapping if m["form"] == form
            }
            if all_unique_events and all(e in assigned_events for e in all_unique_events):
                universal_forms.append(form)

    # Forms assigned to only one event
    single_event_forms = []
    if events and mapping:
        for form in seen_forms:
            assigned = [m for m in mapping if m["form"] == form]
            if len(assigned) == 1:
                single_event_forms.append(form)

    return {
        "arm_count": len(all_arm_nums),
        "event_count": len(events),
        "total_assignments": len(mapping),
        "arms": [{"arm_num": n, "arm_name": arm_name_lookup[n],
                  "event_count": len(events_by_arm.get(n, []))}
                 for n in all_arm_nums],
        "events_by_arm": {
            str(arm_num): [
                {
                    "event_name": e["event_name"],
                    "unique_event_name": e["unique_event_name"],
                    "day_offset": e["day_offset"],
                    "offset_min": e["offset_min"],
                    "offset_max": e["offset_max"],
                    "custom_event_label": e["custom_event_label"],
                    **({"event_id": e["event_id"]} if "event_id" in e else {}),
                    "unique_event_name_predicted": e.get("unique_event_name_predicted", False),
                    "forms": forms_by_event.get(e["unique_event_name"], []),
                }
                for e in sorted(events_by_arm[arm_num], key=event_sort_key)
            ]
            for arm_num in all_arm_nums
        },
        "all_forms": seen_forms,
        "universal_forms": universal_forms,
        "single_event_forms": single_event_forms,
        "forms_by_event": dict(forms_by_event),
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Text report renderer
# ---------------------------------------------------------------------------

def render_text(arms_data, events_data, mapping_data, analysis) -> str:
    lines = []

    def section(title):
        lines.append("")
        lines.append(f"{'='*60}")
        lines.append(f"  {title}")
        lines.append(f"{'='*60}")

    def subsection(title):
        lines.append(f"\n--- {title} ---")

    # Header
    section("REDCap Longitudinal Structure Summary")

    a = analysis
    have_arms = bool(arms_data)
    have_events = bool(events_data)
    have_mapping = bool(mapping_data)

    lines.append(f"\nFiles parsed:")
    lines.append(f"  Arms file:    {'yes (%d arm(s))' % len(arms_data) if have_arms else 'not provided'}")
    lines.append(f"  Events file:  {'yes (%d event(s))' % len(events_data) if have_events else 'not provided'}")
    lines.append(f"  Mapping file: {'yes (%d assignment(s))' % len(mapping_data) if have_mapping else 'not provided'}")

    lines.append(f"\nOverview:")
    lines.append(f"  Arms   : {a['arm_count']}")
    lines.append(f"  Events : {a['event_count']}")
    lines.append(f"  Form-event assignments: {a['total_assignments']}")

    # Arms
    if a["arms"]:
        section("Arms")
        for arm in a["arms"]:
            lines.append(f"  Arm {arm['arm_num']}: {arm['arm_name']}  ({arm['event_count']} event(s))")

    # Events per arm
    if a["events_by_arm"]:
        section("Events")
        for arm in a["arms"]:
            arm_num = arm["arm_num"]
            arm_evts = a["events_by_arm"].get(str(arm_num), [])
            if not arm_evts:
                continue
            subsection(f"Arm {arm_num}: {arm['arm_name']}")
            for evt in arm_evts:
                day = evt["day_offset"]
                lo, hi = evt["offset_min"] or 0, evt["offset_max"] or 0
                window = ""
                if (lo or hi) and day is not None:
                    # offset_min/offset_max are days before/after day_offset
                    window = f"  [window: -{lo}/+{hi} days → Day {day - lo:g}–{day + hi:g}]"
                elif lo or hi:
                    window = f"  [window: -{lo}/+{hi} days]"
                label = f"  label: {evt['custom_event_label']}" if evt["custom_event_label"] else ""
                day_str = f"{day:g}" if day is not None else "—"
                uen = ("~" if evt["unique_event_name_predicted"] else "") + evt["unique_event_name"]
                lines.append(
                    f"  Day {day_str:>4}  {evt['event_name']:<30} ({uen}){window}{label}"
                )

    # Form-event matrix
    if have_mapping and have_events and a["all_forms"] and a["events_by_arm"]:
        section("Form-Event Matrix")
        lines.append("")

        multi_arm = len(a["arms"]) > 1
        col_width = 13
        form_col_width = max(len(f) for f in a["all_forms"]) + 2

        def abbrev(name, max_len=12):
            return name[:max_len] if len(name) > max_len else name

        if multi_arm:
            # Render one sub-matrix per arm so duplicate event names don't confuse
            for arm in a["arms"]:
                arm_evts = a["events_by_arm"].get(str(arm["arm_num"]), [])
                if not arm_evts:
                    continue

                lines.append(f"\n  Arm {arm['arm_num']}: {arm['arm_name']}")

                # Header row
                header = f"  {'Form':<{form_col_width}}"
                for evt in arm_evts:
                    header += f" {abbrev(evt['event_name']):^{col_width}}"
                lines.append(header)

                # Separator
                sep = "  " + "-" * form_col_width
                for _ in arm_evts:
                    sep += " " + "-" * col_width
                lines.append(sep)

                # Data rows — only forms assigned at least once in this arm
                for form in a["all_forms"]:
                    row_str = f"  {form:<{form_col_width}}"
                    form_in_arm = False
                    for evt in arm_evts:
                        assigned_forms = a["forms_by_event"].get(evt["unique_event_name"], [])
                        mark = "✓" if form in assigned_forms else ""
                        if mark:
                            form_in_arm = True
                        row_str += f" {mark:^{col_width}}"
                    # Only print rows where this form appears at least once in this arm
                    if form_in_arm:
                        lines.append(row_str)
        else:
            # Single arm — simple flat matrix
            all_events_ordered = a["events_by_arm"].get(
                str(a["arms"][0]["arm_num"]) if a["arms"] else "1", []
            )

            header = f"{'Form':<{form_col_width}}"
            for evt in all_events_ordered:
                header += f" {abbrev(evt['event_name']):^{col_width}}"
            lines.append(header)

            sep = "-" * form_col_width
            for _ in all_events_ordered:
                sep += " " + "-" * col_width
            lines.append(sep)

            for form in a["all_forms"]:
                row_str = f"{form:<{form_col_width}}"
                for evt in all_events_ordered:
                    assigned_forms = a["forms_by_event"].get(evt["unique_event_name"], [])
                    mark = "✓" if form in assigned_forms else ""
                    row_str += f" {mark:^{col_width}}"
                lines.append(row_str)

    # Notable patterns
    section("Notable Patterns")
    found_pattern = False

    if a["universal_forms"]:
        found_pattern = True
        lines.append(f"\n  Forms assigned to ALL events (universal collection):")
        for f in a["universal_forms"]:
            lines.append(f"    - {f}")

    if a["single_event_forms"]:
        found_pattern = True
        lines.append(f"\n  Forms assigned to only ONE event:")
        for f in a["single_event_forms"]:
            # Find which event
            for m in mapping_data:
                if m["form"] == f:
                    lines.append(f"    - {f}  →  {m['unique_event_name']}")
                    break

    if not found_pattern:
        lines.append("\n  No notable patterns detected.")

    # Issues
    if a["issues"]:
        section("⚠  Issues / Warnings")
        for issue in a["issues"]:
            lines.append(f"\n  • {issue}")
    else:
        lines.append("\n\n✓ No structural issues detected.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Parse REDCap longitudinal project CSVs.")
    parser.add_argument("--arms",    help="Path to Arms CSV")
    parser.add_argument("--events",  help="Path to Events CSV")
    parser.add_argument("--mapping", help="Path to Instrument Designations / formEventMapping CSV")
    parser.add_argument("--json",    action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()

    if not any([args.arms, args.events, args.mapping]):
        print("Error: provide at least one of --arms, --events, or --mapping", file=sys.stderr)
        sys.exit(1)

    arms_data, events_data, mapping_data = [], [], []
    errors = []

    def load(path, expected_type):
        try:
            rows = open_csv(path)
            detected = detect_file_type(rows)
            if detected != expected_type and detected != "unknown":
                print(
                    f"Warning: {path} was expected to be '{expected_type}' "
                    f"but looks like '{detected}'. Proceeding anyway.",
                    file=sys.stderr,
                )
            return rows
        except (OSError, ValueError, csv.Error) as e:
            errors.append(str(e))
            print(f"Error loading {path}: {e}", file=sys.stderr)
            return []

    if args.arms:
        raw = load(args.arms, "arms")
        arms_data = parse_arms(raw)

    if args.events:
        raw = load(args.events, "events")
        events_data = parse_events(raw)

    if args.mapping:
        raw = load(args.mapping, "mapping")
        mapping_data = parse_mapping(raw)

    analysis = build_analysis(arms_data, events_data, mapping_data)

    if args.json:
        output = {
            "arms": arms_data,
            "events": events_data,
            "mapping": mapping_data,
            "analysis": analysis,
            "parse_errors": errors,
        }
        print(json.dumps(output, indent=2))
    else:
        print(render_text(arms_data, events_data, mapping_data, analysis))


if __name__ == "__main__":
    main()

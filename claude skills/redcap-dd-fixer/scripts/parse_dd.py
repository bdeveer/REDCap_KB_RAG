#!/usr/bin/env python3
"""
REDCap Data Dictionary Parser
Parses a REDCap Data Dictionary CSV and outputs a structured JSON summary.

Usage:
    python parse_dd.py <path_to_data_dictionary.csv> [--json | --text]

Handles:
- UTF-8 with and without BOM
- Quoted fields, embedded commas, HTML in labels
- All 18 standard REDCap columns
"""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


COLUMNS = [
    "Variable / Field Name",
    "Form Name",
    "Section Header",
    "Field Type",
    "Field Label",
    "Choices, Calculations, OR Slider Labels",
    "Field Note",
    "Text Validation Type OR Show Slider Number",
    "Text Validation Min",
    "Text Validation Max",
    "Identifier?",
    "Branching Logic (Show field only if...)",
    "Required Field?",
    "Custom Alignment",
    "Question Number (surveys only)",
    "Matrix Group Name",
    "Matrix Ranking?",
    "Field Annotation",
]

VALID_FIELD_TYPES = {
    "text", "notes", "dropdown", "radio", "checkbox",
    "calc", "file", "descriptive", "slider", "yesno",
    "truefalse", "sql",
}

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}

VALIDATION_TYPES = {
    "date_ymd", "date_mdy", "date_dmy",
    "datetime_ymd", "datetime_mdy", "datetime_dmy",
    "datetime_seconds_ymd", "datetime_seconds_mdy", "datetime_seconds_dmy",
    "number", "number_1dp", "number_2dp", "number_3dp", "number_4dp",
    "integer", "email", "phone", "phone_australia",
    "zipcode", "mrn_10d", "mrn_generic", "url",
    "alpha_only", "postalcode_canada", "ssn", "time",
}


def read_dd(path: str) -> list[dict]:
    """Read a data dictionary CSV, handling BOM and encoding gracefully."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Try UTF-8 with BOM first, then UTF-8, then latin-1 as fallback
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, encoding=encoding, newline="") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
                # Verify we got the expected columns
                if rows and "Variable / Field Name" not in rows[0]:
                    # Try to find the column with slight name variation
                    continue
                return rows
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not decode {path} with any supported encoding.")


def strip_html(text: str) -> str:
    """Remove HTML tags for display purposes."""
    return re.sub(r"<[^>]+>", "", text).strip()


def parse_choices(choices_str: str) -> list[dict]:
    """Parse pipe-delimited choices string into list of {value, label} dicts."""
    choices = []
    if not choices_str.strip():
        return choices
    for item in choices_str.split("|"):
        item = item.strip()
        if "," in item:
            value, label = item.split(",", 1)
            choices.append({
                "value": value.strip(),
                "label": label.strip(),
            })
        else:
            choices.append({"value": item, "label": item})
    return choices


def extract_action_tags(annotation: str) -> list[str]:
    """Extract @TAG action tag names from annotation text."""
    # Match @TAGNAME or @TAGNAME='value' or @TAGNAME(...)
    return re.findall(r"@[A-Z][A-Z0-9_-]*", annotation)


def analyze_branching_logic(bl: str) -> dict:
    """Extract referenced variable names from a branching logic expression."""
    if not bl.strip():
        return {"empty": True, "referenced_variables": []}
    # Variables referenced as [var_name] or [event_name][var_name]
    refs = re.findall(r"\[([a-z0-9_]+)\]", bl)
    # Filter out known event name patterns (contain 'arm')
    var_refs = [r for r in refs if "arm" not in r]
    return {
        "empty": False,
        "raw": bl,
        "referenced_variables": list(set(var_refs)),
    }


def summarize(rows: list[dict]) -> dict:
    """Produce a structured summary of the data dictionary."""
    if not rows:
        return {"error": "No rows found in data dictionary."}

    # ── Basic counts ─────────────────────────────────────────────────────────
    total_fields = len(rows)
    field_type_counts = Counter(r.get("Field Type", "").strip() for r in rows)
    validation_counts = Counter(
        r.get("Text Validation Type OR Show Slider Number", "").strip()
        for r in rows
        if r.get("Text Validation Type OR Show Slider Number", "").strip()
    )

    # ── Forms (instruments) ──────────────────────────────────────────────────
    forms_order = []
    forms_map = defaultdict(list)
    for r in rows:
        fn = r.get("Form Name", "").strip()
        if fn and fn not in forms_order:
            forms_order.append(fn)
        if fn:
            forms_map[fn].append(r)

    forms = []
    for fn in forms_order:
        form_rows = forms_map[fn]
        ft_counts = Counter(r.get("Field Type", "").strip() for r in form_rows)
        has_survey_hints = any(
            r.get("Question Number (surveys only)", "").strip() for r in form_rows
        )
        forms.append({
            "name": fn,
            "field_count": len(form_rows),
            "field_types": dict(ft_counts),
            "likely_survey": has_survey_hints,
        })

    # ── Record ID ────────────────────────────────────────────────────────────
    record_id_var = rows[0].get("Variable / Field Name", "").strip() if rows else "record_id"

    # ── Identifiers and required fields ──────────────────────────────────────
    identifiers = [
        r.get("Variable / Field Name", "").strip()
        for r in rows
        if r.get("Identifier?", "").strip().lower() == "y"
    ]
    required_fields = [
        r.get("Variable / Field Name", "").strip()
        for r in rows
        if r.get("Required Field?", "").strip().lower() == "y"
    ]

    # ── Matrix groups ────────────────────────────────────────────────────────
    matrix_groups = defaultdict(list)
    for r in rows:
        mg = r.get("Matrix Group Name", "").strip()
        if mg:
            matrix_groups[mg].append(r.get("Variable / Field Name", "").strip())

    matrices = [
        {"group_name": mg, "variables": vars_, "count": len(vars_)}
        for mg, vars_ in matrix_groups.items()
    ]

    # ── Calculated fields ────────────────────────────────────────────────────
    calc_fields = [
        {
            "variable": r.get("Variable / Field Name", "").strip(),
            "form": r.get("Form Name", "").strip(),
            "formula": r.get("Choices, Calculations, OR Slider Labels", "").strip(),
        }
        for r in rows
        if r.get("Field Type", "").strip() == "calc"
    ]

    # ── Action tags ──────────────────────────────────────────────────────────
    all_action_tags: Counter = Counter()
    action_tagged_fields = []
    for r in rows:
        ann = r.get("Field Annotation", "").strip()
        if ann:
            tags = extract_action_tags(ann)
            if tags:
                all_action_tags.update(tags)
                action_tagged_fields.append({
                    "variable": r.get("Variable / Field Name", "").strip(),
                    "form": r.get("Form Name", "").strip(),
                    "tags": tags,
                    "full_annotation": ann,
                })

    # ── Branching logic ───────────────────────────────────────────────────────
    branching_fields = []
    for r in rows:
        bl = r.get("Branching Logic (Show field only if...)", "").strip()
        if bl:
            branching_fields.append({
                "variable": r.get("Variable / Field Name", "").strip(),
                "form": r.get("Form Name", "").strip(),
                "logic": bl,
            })

    # ── Section headers ───────────────────────────────────────────────────────
    section_headers = [
        {
            "header_text": strip_html(r.get("Section Header", "").strip()),
            "on_variable": r.get("Variable / Field Name", "").strip(),
            "form": r.get("Form Name", "").strip(),
        }
        for r in rows
        if r.get("Section Header", "").strip()
    ]

    # ── Descriptive fields (potential survey intro/instructions) ──────────────
    descriptive_fields = [
        {
            "variable": r.get("Variable / Field Name", "").strip(),
            "form": r.get("Form Name", "").strip(),
            "label_preview": strip_html(r.get("Field Label", "")).strip()[:100],
        }
        for r in rows
        if r.get("Field Type", "").strip() == "descriptive"
    ]

    # ── Potential issues ──────────────────────────────────────────────────────
    issues = []

    # Check: dropdown/radio/checkbox fields with no choices
    for r in rows:
        ft = r.get("Field Type", "").strip()
        choices = r.get("Choices, Calculations, OR Slider Labels", "").strip()
        var = r.get("Variable / Field Name", "").strip()
        if ft in CHOICE_TYPES and not choices:
            issues.append(f"MISSING CHOICES: '{var}' is type '{ft}' but has no choices defined.")

    # Check: calc fields with no formula
    for r in rows:
        ft = r.get("Field Type", "").strip()
        formula = r.get("Choices, Calculations, OR Slider Labels", "").strip()
        var = r.get("Variable / Field Name", "").strip()
        if ft == "calc" and not formula:
            issues.append(f"MISSING FORMULA: '{var}' is type 'calc' but has no formula.")

    # Check: validation min/max on non-text fields
    for r in rows:
        ft = r.get("Field Type", "").strip()
        val_min = r.get("Text Validation Min", "").strip()
        val_max = r.get("Text Validation Max", "").strip()
        var = r.get("Variable / Field Name", "").strip()
        if ft != "text" and (val_min or val_max):
            issues.append(
                f"VALIDATION ON NON-TEXT: '{var}' (type '{ft}') has validation min/max set, which is only valid for text fields."
            )

    # Check: duplicate variable names
    var_names = [r.get("Variable / Field Name", "").strip() for r in rows]
    dupes = [v for v, c in Counter(var_names).items() if c > 1 and v]
    if dupes:
        for d in dupes:
            issues.append(f"DUPLICATE VARIABLE NAME: '{d}' appears more than once.")

    # Check: invalid field types
    for r in rows:
        ft = r.get("Field Type", "").strip()
        var = r.get("Variable / Field Name", "").strip()
        if ft and ft not in VALID_FIELD_TYPES:
            issues.append(f"UNKNOWN FIELD TYPE: '{var}' has unsupported type '{ft}'.")

    # ── Project type hints ────────────────────────────────────────────────────
    hints = []
    if any(r.get("Question Number (surveys only)", "").strip() for r in rows):
        hints.append("Contains question numbers — likely includes survey instruments.")
    if len(forms) > 1:
        hints.append(f"Multi-instrument project with {len(forms)} instruments.")
    if calc_fields:
        hints.append(f"Contains {len(calc_fields)} calculated field(s).")
    if matrices:
        hints.append(f"Contains {len(matrices)} matrix group(s).")
    if identifiers:
        hints.append(f"Contains {len(identifiers)} identifier-flagged field(s).")
    # Check for longitudinal event references in branching logic
    event_refs = any(
        "arm" in r.get("Branching Logic (Show field only if...)", "").lower()
        for r in rows
    )
    if event_refs:
        hints.append("Branching logic references event names — likely a longitudinal project.")

    # ── Build final output ────────────────────────────────────────────────────
    return {
        "file_summary": {
            "total_fields": total_fields,
            "instrument_count": len(forms),
            "record_id_variable": record_id_var,
        },
        "field_type_distribution": dict(field_type_counts),
        "validation_types_used": dict(validation_counts),
        "instruments": forms,
        "identifiers": identifiers,
        "required_fields": required_fields,
        "matrices": matrices,
        "calc_fields": calc_fields,
        "action_tags": {
            "tag_frequency": dict(all_action_tags),
            "tagged_fields": action_tagged_fields,
        },
        "branching_logic": {
            "count": len(branching_fields),
            "fields": branching_fields,
        },
        "section_headers": section_headers,
        "descriptive_fields": descriptive_fields,
        "project_hints": hints,
        "potential_issues": issues,
    }


def print_text_report(summary: dict, filename: str) -> None:
    """Print a human-readable text summary."""
    fs = summary["file_summary"]
    print(f"\n{'='*60}")
    print(f"REDCap Data Dictionary: {filename}")
    print(f"{'='*60}")
    print(f"Total fields:      {fs['total_fields']}")
    print(f"Instruments:       {fs['instrument_count']}")
    print(f"Record ID field:   {fs['record_id_variable']}")

    print(f"\n── Field Types ──")
    for ft, count in sorted(summary["field_type_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {ft:<15} {count}")

    print(f"\n── Instruments ──")
    for form in summary["instruments"]:
        survey_tag = " [survey hints]" if form["likely_survey"] else ""
        print(f"  {form['name']}: {form['field_count']} fields{survey_tag}")
        for ft, cnt in sorted(form["field_types"].items(), key=lambda x: -x[1]):
            print(f"    {ft}: {cnt}")

    if summary["identifiers"]:
        print(f"\n── Identifier Fields ({len(summary['identifiers'])}) ──")
        print(f"  {', '.join(summary['identifiers'])}")

    if summary["required_fields"]:
        print(f"\n── Required Fields ({len(summary['required_fields'])}) ──")
        print(f"  {', '.join(summary['required_fields'][:20])}")
        if len(summary["required_fields"]) > 20:
            print(f"  ... and {len(summary['required_fields']) - 20} more")

    if summary["matrices"]:
        print(f"\n── Matrix Groups ({len(summary['matrices'])}) ──")
        for m in summary["matrices"]:
            print(f"  {m['group_name']}: {m['count']} variables")

    if summary["calc_fields"]:
        print(f"\n── Calculated Fields ({len(summary['calc_fields'])}) ──")
        for c in summary["calc_fields"]:
            formula_preview = c["formula"][:60] + ("..." if len(c["formula"]) > 60 else "")
            print(f"  {c['variable']} ({c['form']}): {formula_preview}")

    if summary["action_tags"]["tag_frequency"]:
        print(f"\n── Action Tags ──")
        for tag, count in sorted(summary["action_tags"]["tag_frequency"].items(), key=lambda x: -x[1]):
            print(f"  {tag}: {count}")

    bl_count = summary["branching_logic"]["count"]
    if bl_count:
        print(f"\n── Branching Logic ──")
        print(f"  {bl_count} field(s) have branching logic conditions.")

    if summary["project_hints"]:
        print(f"\n── Project Hints ──")
        for hint in summary["project_hints"]:
            print(f"  • {hint}")

    if summary["potential_issues"]:
        print(f"\n── Potential Issues ({len(summary['potential_issues'])}) ──")
        for issue in summary["potential_issues"]:
            print(f"  ⚠️  {issue}")
    else:
        print(f"\n✓ No structural issues detected.")

    print()


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_dd.py <data_dictionary.csv> [--json | --text]")
        sys.exit(1)

    path = sys.argv[1]
    output_format = "text"
    if "--json" in sys.argv:
        output_format = "json"

    try:
        rows = read_dd(path)
        summary = summarize(rows)

        if output_format == "json":
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print_text_report(summary, Path(path).name)

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

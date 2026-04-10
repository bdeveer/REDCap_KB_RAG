#!/usr/bin/env python3
"""
REDCap Data Dictionary Builder
Generates a REDCap-compatible Data Dictionary CSV from a JSON spec file.

Usage:
    # Build a new DD from scratch:
    python build_dd.py spec.json --output MyStudy_DataDictionary.csv

    # Append new instruments to an existing DD:
    python build_dd.py spec.json --append existing_dd.csv --output MyStudy_DD_updated.csv

JSON Spec Format:
    {
      "project": {
        "record_id_variable": "record_id",
        "record_id_label": "Record ID"
      },
      "instruments": [
        {
          "form_name": "demographics",
          "fields": [
            {
              "variable": "dob",
              "label": "Date of Birth",
              "field_type": "text",
              "validation": "date_ymd",
              "required": false,
              "identifier": true
            },
            {
              "variable": "sex",
              "label": "Biological Sex",
              "field_type": "radio",
              "choices": [
                {"value": "1", "label": "Male"},
                {"value": "2", "label": "Female"},
                {"value": "99", "label": "Unknown"}
              ]
            },
            {
              "variable": "bmi",
              "label": "BMI (calculated)",
              "field_type": "calc",
              "formula": "([weight_kg])/(([height_m])^(2))"
            }
          ]
        }
      ]
    }
"""

import csv
import json
import re
import sys
from pathlib import Path

# The 18 REDCap DD column headers, in the order REDCap expects them
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
    "calc", "file", "descriptive", "slider", "yesno", "truefalse",
}

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}


def slugify_variable(label: str, max_len: int = 26) -> str:
    """Convert a field label into a REDCap-safe variable name suggestion."""
    s = label.lower()
    # Remove HTML tags
    s = re.sub(r"<[^>]+>", "", s)
    # Remove anything that isn't a letter, digit, or space/underscore
    s = re.sub(r"[^a-z0-9_\s]", " ", s)
    # Collapse whitespace to underscores
    s = re.sub(r"[\s_]+", "_", s.strip())
    # Strip leading/trailing underscores
    s = s.strip("_")
    # Must start with a letter
    if s and s[0].isdigit():
        s = "v_" + s
    if not s:
        s = "field"
    return s[:max_len].rstrip("_")


def format_choices(choices) -> str:
    """
    Convert choices to REDCap pipe-delimited format.

    Accepts:
    - A list of {"value": ..., "label": ...} dicts
    - A plain string (passed through as-is — assumed already formatted)
    """
    if isinstance(choices, str):
        return choices.strip()
    if not choices:
        return ""
    parts = []
    for c in choices:
        if isinstance(c, dict):
            value = str(c.get("value", "")).strip()
            label = str(c.get("label", "")).strip()
            parts.append(f"{value}, {label}")
        else:
            parts.append(str(c).strip())
    return " | ".join(parts)


def validate_variable_name(name: str) -> list[str]:
    """Return a list of validation warnings for a variable name."""
    warnings = []
    if not name:
        warnings.append("Variable name is empty")
        return warnings
    if not re.match(r"^[a-z]", name):
        warnings.append(f"  '{name}': must start with a lowercase letter")
    if not re.match(r"^[a-z0-9_]+$", name):
        warnings.append(f"  '{name}': contains invalid characters — only a-z, 0-9, and _ allowed")
    if len(name) > 26:
        warnings.append(f"  '{name}': {len(name)} characters — REDCap limit is 26")
    return warnings


def build_rows(spec: dict, existing_variable_names: set | None = None) -> tuple[list[dict], list[str]]:
    """
    Convert a spec dict into a list of REDCap DD row dicts.

    Returns (rows, warnings) where warnings is a list of human-readable strings.
    """
    rows = []
    warnings = []
    seen_variables: set[str] = set(existing_variable_names or set())

    project = spec.get("project", {})
    record_id_var = project.get("record_id_variable", "record_id").strip()
    record_id_label = project.get("record_id_label", "Record ID").strip()
    instruments = spec.get("instruments", [])

    # Record ID row — only added on a fresh build (not when appending)
    if existing_variable_names is None:
        first_form = instruments[0].get("form_name", "instrument_1") if instruments else "instrument_1"
        rows.append(_empty_row(record_id_var, first_form, "text", record_id_label))
        seen_variables.add(record_id_var)

    for instrument in instruments:
        form_name = instrument.get("form_name", "").strip()
        if not form_name:
            warnings.append("WARNING: An instrument entry is missing a 'form_name' and was skipped.")
            continue

        # Flag non-conforming form names but continue — user can fix in REDCap
        if not re.match(r"^[a-z0-9_]+$", form_name):
            warnings.append(
                f"WARNING: Form name '{form_name}' contains uppercase or special characters. "
                "REDCap form names should be lowercase letters, digits, and underscores only."
            )

        for field in instrument.get("fields", []):
            variable = field.get("variable", "").strip()
            label = field.get("label", "").strip()
            field_type = field.get("field_type", "text").strip().lower()

            # Auto-generate variable name from label if not provided
            if not variable:
                variable = slugify_variable(label)
                warnings.append(
                    f"NOTE: No variable name given for '{label}' — "
                    f"auto-generated: '{variable}'. Please confirm this is correct."
                )

            # Variable name validation
            var_warnings = validate_variable_name(variable)
            if var_warnings:
                warnings.extend(var_warnings)

            # Duplicate detection
            if variable in seen_variables:
                warnings.append(
                    f"ERROR: Variable '{variable}' already exists. "
                    "Duplicate variable names will cause the upload to fail."
                )
            else:
                seen_variables.add(variable)

            # Field type validation
            if field_type not in VALID_FIELD_TYPES:
                warnings.append(
                    f"WARNING: '{variable}' has unknown field type '{field_type}'. "
                    f"Valid types: {', '.join(sorted(VALID_FIELD_TYPES))}"
                )

            # Build Column F (Choices / Calculation / Slider Labels)
            col_f = _build_column_f(field, field_type, variable, warnings)

            # Flag choice-type fields with no choices
            if field_type in CHOICE_TYPES and not col_f:
                warnings.append(
                    f"ERROR: '{variable}' is type '{field_type}' but has no choices defined. "
                    "REDCap will reject the upload until choices are added."
                )

            # Flag calc fields with no formula
            if field_type == "calc" and not col_f:
                warnings.append(
                    f"WARNING: '{variable}' is type 'calc' but has no formula. "
                    "It will always display blank in REDCap."
                )

            # Validation columns only apply to text fields
            validation = field.get("validation", "").strip() if field_type == "text" else ""
            val_min = field.get("validation_min", "").strip() if field_type == "text" else ""
            val_max = field.get("validation_max", "").strip() if field_type == "text" else ""

            row = {
                "Variable / Field Name": variable,
                "Form Name": form_name,
                "Section Header": field.get("section_header", ""),
                "Field Type": field_type,
                "Field Label": label,
                "Choices, Calculations, OR Slider Labels": col_f,
                "Field Note": field.get("field_note", ""),
                "Text Validation Type OR Show Slider Number": validation,
                "Text Validation Min": val_min,
                "Text Validation Max": val_max,
                "Identifier?": "y" if field.get("identifier") else "",
                "Branching Logic (Show field only if...)": field.get("branching_logic", ""),
                "Required Field?": "y" if field.get("required") else "",
                "Custom Alignment": field.get("custom_alignment", ""),
                "Question Number (surveys only)": field.get("question_number", ""),
                "Matrix Group Name": field.get("matrix_group", ""),
                "Matrix Ranking?": "y" if field.get("matrix_ranking") else "",
                "Field Annotation": field.get("field_annotation", ""),
            }
            rows.append(row)

    return rows, warnings


def _build_column_f(field: dict, field_type: str, variable: str, warnings: list) -> str:
    """Build the Choices/Calculation/Slider Labels column value for a field."""
    if field_type in CHOICE_TYPES:
        return format_choices(field.get("choices", []))

    elif field_type == "calc":
        # Accept formula in 'formula' key (preferred) or 'choices' key (fallback)
        formula = field.get("formula", field.get("choices", ""))
        if isinstance(formula, str):
            return formula.strip()
        return ""

    elif field_type == "slider":
        # Optional endpoint labels as a string
        labels = field.get("choices", "")
        if isinstance(labels, str):
            return labels.strip()
        return ""

    return ""  # text, notes, descriptive, file, yesno, truefalse, etc. have nothing here


def _empty_row(variable: str, form_name: str, field_type: str, label: str) -> dict:
    """Return a row dict with all columns, filled with defaults."""
    return {col: "" for col in COLUMNS} | {
        "Variable / Field Name": variable,
        "Form Name": form_name,
        "Field Type": field_type,
        "Field Label": label,
    }


def read_existing_dd(path: str) -> tuple[list[dict], set]:
    """
    Read an existing DD CSV.
    Returns (rows_as_dicts, set_of_variable_names).
    Tries UTF-8 BOM, then UTF-8, then latin-1 as fallback.
    """
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, encoding=encoding, newline="") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
                if not rows:
                    return [], set()
                variable_names = {r.get("Variable / Field Name", "").strip() for r in rows}
                variable_names.discard("")
                return rows, variable_names
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not decode '{path}' with UTF-8 or latin-1.")


def write_csv(path: str, rows: list[dict]) -> None:
    """Write a list of row dicts to a CSV file using the standard 18 REDCap columns."""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            # Ensure every column is present; fill missing with empty string
            full_row = {col: row.get(col, "") for col in COLUMNS}
            writer.writerow(full_row)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    spec_path = sys.argv[1]
    output_path: str | None = None
    append_path: str | None = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        elif arg == "--append" and i + 1 < len(sys.argv):
            append_path = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            i += 1

    # Default output path
    if not output_path:
        output_path = Path(spec_path).stem + "_DataDictionary.csv"

    # Load the JSON spec
    try:
        with open(spec_path, encoding="utf-8") as fh:
            spec = json.load(fh)
    except FileNotFoundError:
        print(f"Error: spec file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in spec file: {e}", file=sys.stderr)
        sys.exit(1)

    # Load existing DD if appending
    existing_rows: list[dict] = []
    existing_variable_names: set | None = None

    if append_path:
        try:
            existing_rows, existing_variable_names = read_existing_dd(append_path)
            print(f"Loaded existing DD: {len(existing_rows)} fields from '{append_path}'")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading existing DD: {e}", file=sys.stderr)
            sys.exit(1)

    # Build new rows from spec
    new_rows, warnings = build_rows(spec, existing_variable_names)

    # Print warnings
    if warnings:
        print(f"\n{'='*60}")
        print(f"Warnings / Issues ({len(warnings)})")
        print(f"{'='*60}")
        for w in warnings:
            print(w)
        print()

    # Combine and write output
    all_rows = existing_rows + new_rows
    write_csv(output_path, all_rows)

    # Summary
    print(f"{'='*60}")
    print(f"Output: {output_path}")
    if append_path:
        print(f"  Existing fields: {len(existing_rows)}")
        print(f"  New fields added: {len(new_rows)}")
        print(f"  Total fields: {len(all_rows)}")
    else:
        print(f"  Total fields written: {len(all_rows)}")
    print(f"{'='*60}")

    if any("ERROR:" in w for w in warnings):
        print("\n⚠️  One or more ERRORs were found. The file was written but may fail to upload")
        print("   until the errors above are resolved.\n")
    else:
        print("\n✓ No blocking errors. Validate with parse_dd.py before uploading:\n")
        print(f"  python parse_dd.py \"{output_path}\" --text\n")


if __name__ == "__main__":
    main()

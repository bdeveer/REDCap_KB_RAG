#!/usr/bin/env python3
"""
REDCap Data Dictionary Builder
Generates a REDCap-compatible Data Dictionary CSV from a JSON spec file.

Usage:
    # Build a new DD from scratch:
    python build_dd.py spec.json --output MyStudy_DataDictionary.csv

    # Append new instruments/fields to an existing DD:
    python build_dd.py spec.json --append existing_dd.csv --output MyStudy_DD_updated.csv

    When appending, fields for a form that already exists are inserted directly after
    that form's last existing row (REDCap requires each form's rows to be contiguous);
    new forms go at the end. The output uses the same header style as the input DD
    (display headers from the Data Dictionary page, or API-style headers such as
    field_name, form_name, ...).

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
              "custom_alignment": "LH",
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

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

# Windows consoles default to cp1252, which cannot print the report symbols.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# Shared Data Dictionary code lives in the redcap-data-dictionary skill. Skills are
# installed as directory junctions to the repo folders, so resolve the real path and
# use the sibling skill folder.
_SHARED_DIR = Path(__file__).resolve().parents[2] / "redcap-data-dictionary" / "scripts"
sys.path.insert(0, str(_SHARED_DIR))
try:
    from dd_common import (
        COLUMNS, CHOICE_TYPES, FILE_VALIDATION_TYPES, MATRIX_TYPES,
        SLIDER_VALIDATION_TYPES, VALID_ALIGNMENTS, VALID_FIELD_TYPES,
        parse_choices, read_dd, write_dd,
    )
except ImportError as _e:
    sys.exit(
        f"Error: build_dd.py requires the redcap-data-dictionary skill to be installed "
        f"alongside this one (shared module expected at {_SHARED_DIR / 'dd_common.py'}): {_e}"
    )

# 'sql' is valid in an existing DD but admin-only — never build new sql fields (RC-FD-08 §5.4)
BUILD_FIELD_TYPES = VALID_FIELD_TYPES - {"sql"}


def _s(value) -> str:
    """Coerce a JSON scalar to a stripped string (None -> "", 0 -> "0")."""
    if value is None:
        return ""
    return str(value).strip()


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
            value = _s(c.get("value"))
            label = _s(c.get("label"))
            parts.append(f"{value}, {label}")
        else:
            parts.append(_s(c))
    return " | ".join(parts)


def validate_variable_name(name: str) -> list[str]:
    """Return a list of validation warnings for a variable name."""
    warnings = []
    if not name:
        warnings.append("ERROR: Variable name is empty")
        return warnings
    if not re.match(r"^[a-z]", name):
        warnings.append(f"ERROR: '{name}': must start with a lowercase letter")
    if not re.match(r"^[a-z0-9_]+$", name):
        warnings.append(f"ERROR: '{name}': contains invalid characters — only a-z, 0-9, and _ allowed")
    if len(name) > 26:
        warnings.append(
            f"WARNING: '{name}': {len(name)} characters. RC-FD-08 §5.1: "
            "\"Maximum recommended length: 26 characters.\" Not an upload error, but consider shortening."
        )
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
    record_id_var = _s(project.get("record_id_variable")) or "record_id"
    record_id_label = _s(project.get("record_id_label")) or "Record ID"
    instruments = spec.get("instruments", [])

    # Record ID row — only added on a fresh build (not when appending)
    if existing_variable_names is None:
        first_form = (_s(instruments[0].get("form_name")) if instruments else "") or "instrument_1"
        rows.append(_empty_row(record_id_var, first_form, "text", record_id_label))
        seen_variables.add(record_id_var)

    for instrument in instruments:
        form_name = _s(instrument.get("form_name"))
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
            variable = _s(field.get("variable"))
            label = _s(field.get("label"))
            field_type = (_s(field.get("field_type")) or "text").lower()

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

            # Duplicate detection (against the existing DD and earlier spec fields)
            if variable in seen_variables:
                warnings.append(
                    f"ERROR: Variable '{variable}' already exists. "
                    "Duplicate variable names will cause the upload to fail."
                )
            else:
                seen_variables.add(variable)

            # Field type validation
            if field_type not in BUILD_FIELD_TYPES:
                warnings.append(
                    f"WARNING: '{variable}' has unknown field type '{field_type}'. "
                    f"Valid types: {', '.join(sorted(BUILD_FIELD_TYPES))}"
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

            # Columns H-J (validation / slider number / min / max)
            validation, val_min, val_max = _build_validation(field, field_type, variable, warnings)

            # Column N — accept 'custom_alignment' (preferred) or 'alignment'
            alignment = (_s(field.get("custom_alignment")) or _s(field.get("alignment"))).upper()
            if alignment and alignment not in VALID_ALIGNMENTS:
                warnings.append(
                    f"ERROR: '{variable}' has custom alignment '{alignment}'. "
                    f"Only {', '.join(sorted(VALID_ALIGNMENTS))} (or blank) are accepted by REDCap."
                )

            row = {
                "Variable / Field Name": variable,
                "Form Name": form_name,
                "Section Header": _s(field.get("section_header")),
                "Field Type": field_type,
                "Field Label": label,
                "Choices, Calculations, OR Slider Labels": col_f,
                "Field Note": _s(field.get("field_note")),
                "Text Validation Type OR Show Slider Number": validation,
                "Text Validation Min": val_min,
                "Text Validation Max": val_max,
                "Identifier?": "y" if field.get("identifier") else "",
                "Branching Logic (Show field only if...)": _s(field.get("branching_logic")),
                "Required Field?": "y" if field.get("required") else "",
                "Custom Alignment": alignment,
                "Question Number (surveys only)": _s(field.get("question_number")),
                "Matrix Group Name": _s(field.get("matrix_group")),
                "Matrix Ranking?": "y" if field.get("matrix_ranking") else "",
                "Field Annotation": _s(field.get("field_annotation")),
            }
            rows.append(row)

    return rows, warnings


def _build_validation(field: dict, field_type: str, variable: str, warnings: list) -> tuple[str, str, str]:
    """
    Build Columns H, I, J. Per RC-FD-08 §5.7, Column H applies to text fields (any
    validation), file fields (signature / enhanced_signature) and slider fields (number).
    Min/Max apply to text fields and to sliders, where they set the slider's lower and
    upper bound (confirmed on a real export, 2026-10-09; RC-FD-08 §5.8 says text only).
    """
    validation = _s(field.get("validation"))
    val_min = _s(field.get("validation_min"))
    val_max = _s(field.get("validation_max"))

    if field_type == "text":
        return validation, val_min, val_max

    allowed = {"file": FILE_VALIDATION_TYPES, "slider": SLIDER_VALIDATION_TYPES}.get(field_type, set())
    if validation and validation not in allowed:
        hint = f" (allowed: {', '.join(sorted(allowed))})" if allowed else ""
        warnings.append(
            f"WARNING: '{variable}' is type '{field_type}'; validation '{validation}' "
            f"is not valid for this type and was dropped{hint}."
        )
        validation = ""
    if field_type == "slider":
        return validation, val_min, val_max
    if val_min or val_max:
        warnings.append(
            f"WARNING: '{variable}' is type '{field_type}'; validation_min/max apply to "
            "text and slider fields only and were dropped."
        )
    return validation, "", ""


def _build_column_f(field: dict, field_type: str, variable: str, warnings: list) -> str:
    """Build the Choices/Calculation/Slider Labels column value for a field."""
    if field_type in CHOICE_TYPES:
        return format_choices(field.get("choices", []))

    elif field_type == "calc":
        # Accept formula in 'formula' key (preferred) or 'choices' key (fallback)
        formula = field.get("formula", field.get("choices", ""))
        if isinstance(formula, (list, dict)):
            return ""
        return _s(formula)

    elif field_type == "slider":
        # Optional endpoint labels: "Left | Right" string or a list of labels
        labels = field.get("choices", "")
        if isinstance(labels, list):
            return " | ".join(_s(x) for x in labels)
        if isinstance(labels, dict):
            return ""
        return _s(labels)

    return ""  # text, notes, descriptive, file, yesno, truefalse, etc. have nothing here


def _empty_row(variable: str, form_name: str, field_type: str, label: str) -> dict:
    """Return a row dict with all columns, filled with defaults."""
    return {col: "" for col in COLUMNS} | {
        "Variable / Field Name": variable,
        "Form Name": form_name,
        "Field Type": field_type,
        "Field Label": label,
    }


def read_existing_dd(path: str) -> tuple[list[dict], str]:
    """
    Read an existing DD (via dd_common.read_dd, strict headers).
    Returns (rows keyed by display headers with all 18 columns present, header_style)
    where header_style is "display" or "api". Fully blank lines are skipped.
    Raises FileNotFoundError / ValueError (unrecognised headers).
    """
    result = read_dd(path, strict=True)
    for note in result.warnings:
        print(f"Note: {note}", file=sys.stderr)
    rows = []
    for raw in result.rows:
        if not any((v or "").strip() for k, v in raw.items() if k is not None):
            continue  # skip fully blank lines
        rows.append({col: raw.get(col) or "" for col in COLUMNS})
    return rows, result.header_style


def merge_rows(existing_rows: list[dict], new_rows: list[dict]) -> list[dict]:
    """
    Combine existing and new rows so every form stays contiguous.
    New rows for a form already in the DD go right after that form's last existing row;
    new forms are appended at the end in the order they first appear in the spec.
    """
    new_by_form: dict[str, list[dict]] = {}
    for row in new_rows:
        new_by_form.setdefault(row["Form Name"], []).append(row)

    last_index = {row["Form Name"]: i for i, row in enumerate(existing_rows)}
    inserts: dict[int, list[dict]] = {}
    for form, rows in new_by_form.items():
        if form in last_index:
            inserts[last_index[form]] = rows

    merged = []
    for i, row in enumerate(existing_rows):
        merged.append(row)
        merged.extend(inserts.get(i, []))
    for form, rows in new_by_form.items():
        if form not in last_index:
            merged.extend(rows)
    return merged


def check_structure(rows: list[dict]) -> list[str]:
    """Check the combined DD for split forms and matrix group problems."""
    warnings = []

    # Form contiguity — REDCap rejects a DD whose form rows are split
    seen_forms: set[str] = set()
    prev = None
    for r in rows:
        form = r["Form Name"].strip()
        if form != prev:
            if form in seen_forms:
                warnings.append(
                    f"ERROR: Rows for form '{form}' are not contiguous in the output DD. "
                    "REDCap requires all of a form's fields to be together."
                )
            seen_forms.add(form)
            prev = form

    # Matrix groups (RC-FD-08 §5.14-5.15)
    groups: dict[str, list[int]] = {}
    for i, r in enumerate(rows):
        group = r["Matrix Group Name"].strip()
        if group:
            groups.setdefault(group, []).append(i)

    def _norm_choices(text: str) -> tuple:
        return tuple((c["value"], c["label"]) for c in parse_choices(text))

    for group, idx in groups.items():
        members = [rows[i] for i in idx]
        names = ", ".join(m["Variable / Field Name"] for m in members)
        if idx != list(range(idx[0], idx[0] + len(idx))):
            warnings.append(
                f"WARNING: Matrix group '{group}' rows are not contiguous ({names}). "
                "All matrix fields must be sequential in the Data Dictionary."
            )
        bad_types = [m["Variable / Field Name"] for m in members if m["Field Type"].strip() not in MATRIX_TYPES]
        if bad_types:
            warnings.append(
                f"WARNING: Matrix group '{group}' contains non-radio/checkbox fields: "
                f"{', '.join(bad_types)}. Matrix fields must be radio or checkbox."
            )
        if len({m["Field Type"].strip() for m in members}) > 1:
            warnings.append(f"WARNING: Matrix group '{group}' mixes field types ({names}).")
        if len({_norm_choices(m["Choices, Calculations, OR Slider Labels"]) for m in members}) > 1:
            warnings.append(
                f"WARNING: Matrix group '{group}' fields do not share identical choices ({names})."
            )
        if any(m["Matrix Ranking?"].strip().lower() == "y" for m in members) and any(
            m["Field Type"].strip() == "checkbox" for m in members
        ):
            warnings.append(
                f"WARNING: Matrix group '{group}' has Matrix Ranking on checkbox fields — "
                "ranking is only supported for radio matrices."
            )
    return warnings


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

    # Fail loudly on a malformed spec rather than silently adding nothing
    if not isinstance(spec, dict):
        print("Error: the spec must be a JSON object with an \"instruments\" list.", file=sys.stderr)
        sys.exit(1)
    unknown = sorted(set(spec) - {"project", "instruments"})
    if unknown:
        print(f"Error: unknown top-level key(s) in spec: {', '.join(unknown)}. "
              "Expected \"project\" and \"instruments\" (fields go inside each instrument).",
              file=sys.stderr)
        sys.exit(1)
    if not any(inst.get("fields") for inst in spec.get("instruments") or [] if isinstance(inst, dict)):
        print("Error: the spec has no fields — expected \"instruments\": "
              "[{\"form_name\": ..., \"fields\": [...]}].", file=sys.stderr)
        sys.exit(1)

    # Load existing DD if appending
    existing_rows: list[dict] = []
    existing_variable_names: set | None = None
    header_style = "display"

    if append_path:
        try:
            existing_rows, header_style = read_existing_dd(append_path)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading existing DD: {e} Nothing was written.", file=sys.stderr)
            sys.exit(1)
        existing_counts = Counter(r["Variable / Field Name"].strip() for r in existing_rows)
        existing_counts.pop("", None)
        existing_variable_names = set(existing_counts)
        print(f"Loaded existing DD: {len(existing_rows)} fields from '{append_path}' "
              f"({header_style} headers)")

    # Build new rows from spec (duplicates vs. existing + earlier spec fields are flagged here)
    new_rows, warnings = build_rows(spec, existing_variable_names)
    if append_path:
        warnings += [
            f"ERROR: Variable '{name}' appears {n} times in the existing DD."
            for name, n in existing_counts.items() if n > 1
        ]

    # Merge keeping forms contiguous, then check the combined result
    all_rows = merge_rows(existing_rows, new_rows)
    warnings += check_structure(all_rows)

    # Print warnings
    if warnings:
        print(f"\n{'='*60}")
        print(f"Warnings / Issues ({len(warnings)})")
        print(f"{'='*60}")
        for w in warnings:
            print(w)
        print()

    write_dd(output_path, all_rows, header_style)

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

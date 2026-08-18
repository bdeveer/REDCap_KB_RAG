#!/usr/bin/env python3
"""
REDCap Data Dictionary Fixer
Applies safe, automatic corrections to a REDCap Data Dictionary CSV and
produces a corrected file alongside a detailed change log.

Usage:
    python fix_dd.py <input_dd.csv> [--output <output_path.csv>] [--log-json]

Outputs:
    - Corrected CSV (default: <input>_fixed.csv)
    - Change log printed to stdout (or JSON with --log-json)

What it fixes automatically:
    - Whitespace: strips leading/trailing spaces from all cells
    - Variable names: lowercases, strips
    - Field types: lowercases, strips
    - Branching logic (Column L):
        - Double quotes → single quotes
        - == → = (equality operator)
        - != → <> (not-equal operator)
        - && → AND (boolean keyword)
        - || → OR (boolean keyword)
    - Identifier? (Column K): normalizes 'Y'/'yes' → 'y'; 'N'/'no' → ''
    - Required Field? (Column M): same normalization
    - Text Validation Min/Max (Columns I/J): clears these on non-text fields
      (REDCap rejects min/max on dropdown, radio, checkbox, calc, etc.)
    - Field Annotation (Column R): double quotes → single quotes inside
      @CALCTEXT(...) and @CALCDATE(...) expressions

What it flags but does NOT auto-fix:
    - Missing choices on dropdown/radio/checkbox fields
    - Missing formula on calc fields
    - Duplicate variable names
    - Invalid field types
    - Variable name characters that REDCap rejects (non-alphanumeric/underscore)
    - Complex branching logic or formula syntax errors (see syntax fixer skill)
"""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ── Column name constants ─────────────────────────────────────────────────────

COL_VARIABLE      = "Variable / Field Name"
COL_FORM          = "Form Name"
COL_SECTION       = "Section Header"
COL_FIELD_TYPE    = "Field Type"
COL_LABEL         = "Field Label"
COL_CHOICES       = "Choices, Calculations, OR Slider Labels"
COL_NOTE          = "Field Note"
COL_VALIDATION    = "Text Validation Type OR Show Slider Number"
COL_VAL_MIN       = "Text Validation Min"
COL_VAL_MAX       = "Text Validation Max"
COL_IDENTIFIER    = "Identifier?"
COL_BRANCHING     = "Branching Logic (Show field only if...)"
COL_REQUIRED      = "Required Field?"
COL_ALIGNMENT     = "Custom Alignment"
COL_QUESTION_NUM  = "Question Number (surveys only)"
COL_MATRIX_GROUP  = "Matrix Group Name"
COL_MATRIX_RANK   = "Matrix Ranking?"
COL_ANNOTATION    = "Field Annotation"

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}

VALID_FIELD_TYPES = {
    "text", "notes", "dropdown", "radio", "checkbox",
    "calc", "file", "descriptive", "slider", "yesno",
    "truefalse", "sql",
}

VALID_VARIABLE_RE = re.compile(r'^[a-z][a-z0-9_]*$')


# ── CSV I/O ───────────────────────────────────────────────────────────────────

def read_dd(path: str) -> tuple[list[dict], list[str]]:
    """Read a data dictionary CSV, returning (rows, fieldnames).
    Handles BOM and UTF-8/latin-1 encoding gracefully."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, encoding=encoding, newline="") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
                fieldnames = reader.fieldnames or []
                if rows and COL_VARIABLE in rows[0]:
                    return rows, fieldnames
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not decode {path} with any supported encoding.")


def write_dd(path: str, rows: list[dict], fieldnames: list[str]) -> None:
    """Write a data dictionary CSV with consistent encoding (UTF-8, no BOM)."""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ── Fix helpers ───────────────────────────────────────────────────────────────

def fix_branching_logic(value: str) -> tuple[str, list[str]]:
    """
    Apply safe operator substitutions to a branching logic expression.
    Returns (fixed_value, list_of_changes_made).
    """
    if not value.strip():
        return value, []

    original = value
    changes = []

    # Double quotes → single quotes (string delimiters in REDCap are single quotes;
    # double quotes are accepted but break when the DD is resaved through Excel)
    if '"' in value:
        value = value.replace('"', "'")
        changes.append('Double quotes → single quotes')

    # == → = (equality; careful not to catch <= or >=)
    new_value = re.sub(r'(?<![<>!])={2}', '=', value)
    if new_value != value:
        changes.append('== → = (equality operator)')
        value = new_value

    # != → <> (not-equal)
    new_value = value.replace('!=', '<>')
    if new_value != value:
        changes.append('!= → <> (not-equal operator)')
        value = new_value

    # && → AND (boolean)
    new_value = re.sub(r'\s*&&\s*', ' AND ', value)
    if new_value != value:
        changes.append('&& → AND (boolean keyword)')
        value = new_value

    # || → OR (boolean)
    new_value = re.sub(r'\s*\|\|\s*', ' OR ', value)
    if new_value != value:
        changes.append('|| → OR (boolean keyword)')
        value = new_value

    return value, changes


def fix_annotation(value: str) -> tuple[str, list[str]]:
    """
    Fix double quotes inside @CALCTEXT(...) and @CALCDATE(...) calls.
    Leaves other annotation content (designer notes, @HIDDEN, etc.) untouched.
    """
    if not value.strip():
        return value, []

    original = value
    changes = []

    def replace_quotes_in_calctag(match):
        tag_content = match.group(0)
        if '"' in tag_content:
            return tag_content.replace('"', "'")
        return tag_content

    # Fix @CALCTEXT(...) and @CALCDATE(...)
    pattern = re.compile(r'@CALCTEXT\([^)]*\)|@CALCDATE\([^)]*\)', re.IGNORECASE)
    new_value = pattern.sub(replace_quotes_in_calctag, value)

    if new_value != value:
        changes.append('Double quotes → single quotes inside @CALCTEXT/@CALCDATE')
        value = new_value

    return value, changes


def normalize_yesno_flag(value: str) -> tuple[str, list[str]]:
    """Normalize Identifier? and Required Field? to 'y' or empty string."""
    stripped = value.strip().lower()
    if stripped in ('y', 'yes', '1', 'true'):
        fixed = 'y'
    else:
        fixed = ''
    if fixed != value:
        return fixed, [f"Normalized '{value}' → '{fixed}'"]
    return value, []


# ── Main fixer ────────────────────────────────────────────────────────────────

def fix_dd(rows: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Apply all auto-fixes to the rows.

    Returns:
        (fixed_rows, change_log, flag_log)

    change_log: list of {row, variable, column, old, new, fix}
    flag_log:   list of {row, variable, issue, severity}
    """
    fixed_rows = []
    change_log = []
    flag_log = []

    # Track variable names for duplicate detection
    var_name_counts = Counter(
        r.get(COL_VARIABLE, "").strip().lower() for r in rows
    )

    for row_num, row in enumerate(rows, start=2):  # row 1 is header; data from row 2
        fixed_row = dict(row)
        var = row.get(COL_VARIABLE, "").strip()
        field_type = row.get(COL_FIELD_TYPE, "").strip().lower()

        def log_change(column, old, new, fix_description):
            change_log.append({
                "row": row_num,
                "variable": var,
                "column": column,
                "old": old,
                "new": new,
                "fix": fix_description,
            })

        def log_flag(issue, severity="WARNING"):
            flag_log.append({
                "row": row_num,
                "variable": var,
                "issue": issue,
                "severity": severity,
            })

        # ── Strip whitespace from ALL cells ──────────────────────────────────
        for col in fixed_row:
            original = fixed_row[col]
            if original is None:
                fixed_row[col] = ""
                continue
            stripped = original.strip()
            if stripped != original:
                fixed_row[col] = stripped
                log_change(col, repr(original), repr(stripped), "Stripped leading/trailing whitespace")

        # Re-read after strip
        var = fixed_row.get(COL_VARIABLE, "").strip()
        field_type = fixed_row.get(COL_FIELD_TYPE, "").strip()

        # ── Variable name: lowercase ──────────────────────────────────────────
        if var and var != var.lower():
            old_var = var
            var = var.lower()
            fixed_row[COL_VARIABLE] = var
            log_change(COL_VARIABLE, old_var, var, "Lowercased variable name")

        # ── Variable name: flag invalid characters ────────────────────────────
        if var and not VALID_VARIABLE_RE.match(var):
            log_flag(
                f"Variable name '{var}' contains invalid characters. "
                "REDCap allows only lowercase letters, digits, and underscores, "
                "starting with a letter.",
                severity="ERROR"
            )

        # ── Variable name: flag duplicates ────────────────────────────────────
        if var and var_name_counts[var.lower()] > 1:
            log_flag(
                f"Variable name '{var}' is duplicated — REDCap will reject the upload.",
                severity="ERROR"
            )

        # ── Field type: lowercase, flag if invalid ────────────────────────────
        if field_type and field_type != field_type.lower():
            old_ft = field_type
            field_type = field_type.lower()
            fixed_row[COL_FIELD_TYPE] = field_type
            log_change(COL_FIELD_TYPE, old_ft, field_type, "Lowercased field type")

        if field_type and field_type not in VALID_FIELD_TYPES:
            log_flag(
                f"Unknown field type '{field_type}'. REDCap will reject this field.",
                severity="ERROR"
            )

        # ── Missing choices on choice-type fields ────────────────────────────
        if field_type in CHOICE_TYPES:
            choices = fixed_row.get(COL_CHOICES, "").strip()
            if not choices:
                log_flag(
                    f"Field type '{field_type}' but no choices defined. "
                    "REDCap will reject the upload — choices must be added manually.",
                    severity="ERROR"
                )

        # ── Missing formula on calc fields ────────────────────────────────────
        if field_type == "calc":
            formula = fixed_row.get(COL_CHOICES, "").strip()
            if not formula:
                log_flag(
                    "Calc field has no formula — the field will always display blank.",
                    severity="ERROR"
                )

        # ── Validation min/max on non-text fields ─────────────────────────────
        if field_type != "text":
            val_min = fixed_row.get(COL_VAL_MIN, "").strip()
            val_max = fixed_row.get(COL_VAL_MAX, "").strip()
            if val_min:
                fixed_row[COL_VAL_MIN] = ""
                log_change(COL_VAL_MIN, val_min, "", f"Cleared validation min (only valid on text fields; field is '{field_type}')")
            if val_max:
                fixed_row[COL_VAL_MAX] = ""
                log_change(COL_VAL_MAX, val_max, "", f"Cleared validation max (only valid on text fields; field is '{field_type}')")

        # ── Branching logic ───────────────────────────────────────────────────
        bl_raw = fixed_row.get(COL_BRANCHING, "").strip()
        if bl_raw:
            bl_fixed, bl_changes = fix_branching_logic(bl_raw)
            if bl_fixed != bl_raw:
                fixed_row[COL_BRANCHING] = bl_fixed
                combined = "; ".join(bl_changes)
                log_change(COL_BRANCHING, bl_raw, bl_fixed, f"Branching logic: {combined}")

        # ── Identifier? normalization ─────────────────────────────────────────
        ident_raw = fixed_row.get(COL_IDENTIFIER, "")
        ident_fixed, ident_changes = normalize_yesno_flag(ident_raw)
        if ident_changes:
            fixed_row[COL_IDENTIFIER] = ident_fixed
            for change in ident_changes:
                log_change(COL_IDENTIFIER, ident_raw, ident_fixed, f"Identifier flag: {change}")

        # ── Required Field? normalization ─────────────────────────────────────
        req_raw = fixed_row.get(COL_REQUIRED, "")
        req_fixed, req_changes = normalize_yesno_flag(req_raw)
        if req_changes:
            fixed_row[COL_REQUIRED] = req_fixed
            for change in req_changes:
                log_change(COL_REQUIRED, req_raw, req_fixed, f"Required flag: {change}")

        # ── Field Annotation ──────────────────────────────────────────────────
        ann_raw = fixed_row.get(COL_ANNOTATION, "").strip()
        if ann_raw:
            ann_fixed, ann_changes = fix_annotation(ann_raw)
            if ann_fixed != ann_raw:
                fixed_row[COL_ANNOTATION] = ann_fixed
                for change in ann_changes:
                    log_change(COL_ANNOTATION, ann_raw, ann_fixed, f"Annotation: {change}")

        fixed_rows.append(fixed_row)

    return fixed_rows, change_log, flag_log


# ── Reporting ─────────────────────────────────────────────────────────────────

def print_text_report(change_log: list[dict], flag_log: list[dict], output_path: str) -> None:
    """Print a human-readable change and flag report."""
    print(f"\n{'='*60}")
    print(f"REDCap Data Dictionary Fixer — Report")
    print(f"Output file: {output_path}")
    print(f"{'='*60}")

    if change_log:
        print(f"\n── AUTO-FIXES APPLIED ({len(change_log)}) ──────────────────────")
        for c in change_log:
            print(f"  Row {c['row']} | {c['variable']} | {c['column']}")
            print(f"    Fix: {c['fix']}")
            if len(c['old']) < 80 and len(c['new']) < 80:
                print(f"    Before: {c['old']}")
                print(f"    After:  {c['new']}")
    else:
        print("\n✓ No auto-fixes needed.")

    if flag_log:
        errors = [f for f in flag_log if f['severity'] == 'ERROR']
        warnings = [f for f in flag_log if f['severity'] == 'WARNING']
        print(f"\n── ISSUES REQUIRING MANUAL ATTENTION ({len(flag_log)}) ──────────")
        if errors:
            print(f"\n  ERRORS (will prevent upload or cause data loss):")
            for f in errors:
                print(f"  ✗ Row {f['row']} | {f['variable']}: {f['issue']}")
        if warnings:
            print(f"\n  WARNINGS:")
            for f in warnings:
                print(f"  ⚠ Row {f['row']} | {f['variable']}: {f['issue']}")
    else:
        print("\n✓ No unresolvable issues detected.")

    print()


def print_json_report(change_log: list[dict], flag_log: list[dict], output_path: str) -> None:
    report = {
        "output_file": output_path,
        "auto_fixes_applied": len(change_log),
        "issues_flagged": len(flag_log),
        "changes": change_log,
        "flags": flag_log,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: fix_dd.py <data_dictionary.csv> [--output <output.csv>] [--log-json]")
        sys.exit(1)

    input_path = sys.argv[1]
    log_json = "--log-json" in sys.argv

    # Determine output path
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        output_path = sys.argv[idx + 1]
    else:
        p = Path(input_path)
        output_path = str(p.parent / (p.stem + "_fixed" + p.suffix))

    try:
        rows, fieldnames = read_dd(input_path)
        fixed_rows, change_log, flag_log = fix_dd(rows)
        write_dd(output_path, fixed_rows, fieldnames)

        if log_json:
            print_json_report(change_log, flag_log, output_path)
        else:
            print_text_report(change_log, flag_log, output_path)

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

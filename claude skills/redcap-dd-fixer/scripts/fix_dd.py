#!/usr/bin/env python3
"""
REDCap Data Dictionary Fixer
Applies safe, automatic corrections to a REDCap Data Dictionary CSV and
produces a corrected file alongside a detailed change log.

Usage:
    python fix_dd.py <input_dd.csv> [--output <output_path.csv>] [--log-json]

Outputs:
    - Corrected CSV (default: <input>_fixed.csv), same header style as the
      input (display headers or API-style headers such as field_name)
    - Change log file next to the output CSV (<output>_changes.txt, or
      <output>_changes.json with --log-json), written BEFORE the CSV
    - The same change log printed to stdout

What it fixes automatically:
    - Whitespace: strips leading/trailing spaces from all cells
    - Field types: lowercases
    - Branching logic (Column L), outside string literals only:
        - "double-quoted" literals → 'single-quoted' (only when the literal
          contains no apostrophe; otherwise left as double quotes and flagged)
        - == → = (equality operator)
        - != → <> (not-equal operator)
        - && → AND (boolean keyword)
        - || → OR (boolean keyword)
    - Identifier? (Column K) / Required Field? (Column M): 'Y'/'yes'/'1'/'true'
      → 'y'; 'N'/'no'/'0'/'false' → ''. Anything else is kept and flagged.
    - Text Validation Min/Max (Columns I/J): clears these on fields that are
      neither text nor slider (REDCap rejects min/max on dropdown, radio,
      checkbox, calc, etc.)
    - Field Annotation (Column R): "double-quoted" literals → 'single-quoted'
      inside @CALCTEXT(...) and @CALCDATE(...) (balanced-parenthesis scan;
      literals containing an apostrophe are left as double quotes)

What it flags but does NOT auto-fix:
    - Variable names with uppercase letters or invalid characters (never
      renamed: references in logic/calcs/piping and collected data would break)
    - Missing choices on dropdown/radio/checkbox fields
    - Missing formula on calc fields
    - Duplicate variable names
    - Invalid field types
    - Unrecognised Identifier?/Required Field? values
    - Unbalanced quotes or parentheses in branching logic / @CALC tags
    - Complex branching logic or formula syntax errors (see syntax fixer skill)
"""

import argparse
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
        COL_ANNOTATION, COL_BRANCHING, COL_CHOICES, COL_FIELD_TYPE, COL_IDENTIFIER,
        COL_LABEL, COL_NOTE, COL_REQUIRED, COL_SECTION, COL_VAL_MAX, COL_VAL_MIN,
        COL_VARIABLE, CHOICE_TYPES, VALID_FIELD_TYPES, VALID_VARIABLE_RE,
        read_dd, write_dd,
    )
except ImportError as _e:
    sys.exit(
        f"Error: fix_dd.py requires the redcap-data-dictionary skill to be installed "
        f"alongside this one (shared module expected at {_SHARED_DIR / 'dd_common.py'}): {_e}"
    )


# ── Fixer settings ────────────────────────────────────────────────────────────

# Field types on which Text Validation Min/Max are meaningful
MINMAX_TYPES = {"text", "slider"}

YES_VALUES = {"y", "yes", "1", "true"}
NO_VALUES = {"", "n", "no", "0", "false"}

# Columns where other fields' variable names can be referenced
REFERENCE_COLUMNS = (COL_BRANCHING, COL_CHOICES, COL_ANNOTATION, COL_LABEL,
                     COL_NOTE, COL_SECTION)


# ── Expression helpers ────────────────────────────────────────────────────────

def split_literals(expr: str) -> list[tuple[str, str]]:
    """
    Split an expression into segments of (kind, text):
      kind 'code'         — expression text outside string literals
      kind "'" or '"'     — a complete string literal, delimiters included
      kind 'unterminated' — an opening quote with no closing quote (rest of expr)
    Backslash escapes inside literals are honoured.
    """
    segments = []
    buf = []
    i, n = 0, len(expr)
    while i < n:
        ch = expr[i]
        if ch in ("'", '"'):
            if buf:
                segments.append(("code", "".join(buf)))
                buf = []
            j = i + 1
            while j < n and expr[j] != ch:
                j += 2 if expr[j] == "\\" else 1
            if j >= n:
                segments.append(("unterminated", expr[i:]))
                return segments
            segments.append((ch, expr[i:j + 1]))
            i = j + 1
        else:
            buf.append(ch)
            i += 1
    if buf:
        segments.append(("code", "".join(buf)))
    return segments


def convert_double_quoted(segments: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], int, list[str]]:
    """
    Convert "double-quoted" literals to 'single-quoted' ones when that is safe
    (content has no apostrophe or backslash). Returns (segments, converted, kept)
    where kept lists the double-quoted literals left unchanged.
    """
    converted = 0
    kept = []
    out = []
    for kind, text in segments:
        if kind == '"':
            content = text[1:-1]
            if "'" in content or "\\" in content:
                kept.append(text)
            else:
                text = "'" + content + "'"
                kind = "'"
                converted += 1
        out.append((kind, text))
    return out, converted, kept


def find_calc_tags(value: str) -> list[tuple[int, int, int]]:
    """
    Locate @CALCTEXT(...) / @CALCDATE(...) calls using a balanced-parenthesis
    scan that ignores parentheses inside string literals.
    Returns a list of (open_paren_index, close_paren_index, tag_start);
    close_paren_index is -1 if the call is never closed.
    """
    results = []
    for m in re.finditer(r'@CALC(?:TEXT|DATE)\s*\(', value, re.IGNORECASE):
        open_idx = m.end() - 1
        depth = 0
        i, n = open_idx, len(value)
        close_idx = -1
        while i < n:
            ch = value[i]
            if ch in ("'", '"'):
                j = i + 1
                while j < n and value[j] != ch:
                    j += 2 if value[j] == "\\" else 1
                i = j + 1
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    close_idx = i
                    break
            i += 1
        results.append((open_idx, close_idx, m.start()))
    return results


# ── Fix helpers ───────────────────────────────────────────────────────────────

def fix_branching_logic(value: str) -> tuple[str, list[str], list[str]]:
    """
    Apply safe substitutions to a branching logic expression. Operators are
    only rewritten outside string literals.
    Returns (fixed_value, list_of_changes_made, list_of_issues_to_flag).
    """
    if not value.strip():
        return value, [], []

    changes = []
    issues = []

    segments = split_literals(value)

    # "..." → '...' (single quotes are the safe choice for DD/Excel round-trips;
    # literals containing an apostrophe stay double-quoted — REDCap accepts both)
    segments, converted, kept = convert_double_quoted(segments)
    if converted:
        changes.append('Double-quoted string literals → single quotes')
    if kept:
        issues.append(
            "Double-quoted string(s) contain an apostrophe and were left unchanged: "
            + ", ".join(kept)
            + ". REDCap accepts double quotes, but Excel can mangle them — check "
            "the value survives the round-trip, or rephrase without the apostrophe."
        )
    if any(kind == "unterminated" for kind, _ in segments):
        issues.append("Unbalanced quote in branching logic — a string literal is never closed.")

    op_changes = []

    def fix_code(code: str) -> str:
        # == → = (equality; careful not to catch <= or >=)
        new = re.sub(r'(?<![<>!])={2}', '=', code)
        if new != code:
            op_changes.append('== → = (equality operator)')
            code = new
        # != → <> (not-equal)
        new = code.replace('!=', '<>')
        if new != code:
            op_changes.append('!= → <> (not-equal operator)')
            code = new
        # && → AND (boolean)
        new = re.sub(r'\s*&&\s*', ' AND ', code)
        if new != code:
            op_changes.append('&& → AND (boolean keyword)')
            code = new
        # || → OR (boolean)
        new = re.sub(r'\s*\|\|\s*', ' OR ', code)
        if new != code:
            op_changes.append('|| → OR (boolean keyword)')
            code = new
        return code

    value = "".join(fix_code(text) if kind == "code" else text for kind, text in segments)
    for change in op_changes:
        if change not in changes:
            changes.append(change)

    return value.strip(), changes, issues


def fix_annotation(value: str) -> tuple[str, list[str], list[str]]:
    """
    Convert safe double-quoted literals to single quotes inside @CALCTEXT(...)
    and @CALCDATE(...) calls (nested parentheses supported). Leaves other
    annotation content (designer notes, @HIDDEN, etc.) untouched.
    Returns (fixed_value, changes, issues).
    """
    if not value.strip():
        return value, [], []

    changes = []
    issues = []
    pieces = []
    pos = 0
    converted_total = 0

    for open_idx, close_idx, tag_start in find_calc_tags(value):
        if open_idx < pos:
            continue  # nested inside a tag already processed
        if close_idx == -1:
            issues.append(
                f"Unbalanced parentheses in '{value[tag_start:open_idx + 1]}...' — "
                "the call is never closed; left unchanged."
            )
            continue
        inner = value[open_idx + 1:close_idx]
        segments, converted, _kept = convert_double_quoted(split_literals(inner))
        converted_total += converted
        pieces.append(value[pos:open_idx + 1])
        pieces.append("".join(text for _, text in segments))
        pos = close_idx

    pieces.append(value[pos:])
    new_value = "".join(pieces)

    if converted_total:
        changes.append('Double-quoted string literals → single quotes inside @CALCTEXT/@CALCDATE')

    return new_value, changes, issues


def normalize_yesno_flag(value: str) -> tuple[str, list[str], bool]:
    """
    Normalize Identifier? and Required Field? to 'y' or empty string.
    Returns (value, changes, recognised). Unrecognised values are returned
    unchanged with recognised=False so the caller can flag them.
    """
    stripped = value.strip().lower()
    if stripped in YES_VALUES:
        fixed = 'y'
    elif stripped in NO_VALUES:
        fixed = ''
    else:
        return value, [], False
    if fixed != value:
        return fixed, [f"Normalized '{value}' → '{fixed}'"], True
    return value, [], True


def find_references(rows: list[dict], name: str) -> list[tuple[int, str]]:
    """Return (row_number, variable) pairs whose expression/piping columns
    reference [name] exactly (including [name(1)] checkbox and [name:...] forms)."""
    pattern = re.compile(r'\[' + re.escape(name) + r'(?=[\]():])')
    hits = []
    for row_num, row in enumerate(rows, start=2):
        for col in REFERENCE_COLUMNS:
            cell = row.get(col) or ""
            if isinstance(cell, str) and pattern.search(cell):
                hits.append((row_num, (row.get(COL_VARIABLE) or "").strip()))
                break
    return hits


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
        (r.get(COL_VARIABLE) or "").strip().lower() for r in rows
    )

    for row_num, row in enumerate(rows, start=2):  # row 1 is header; data from row 2
        fixed_row = dict(row)
        var = (row.get(COL_VARIABLE) or "").strip()

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

        # ── Extra cells beyond the header row ────────────────────────────────
        extra = fixed_row.pop(None, None)
        if extra:
            log_flag(
                f"Row has {len(extra)} more cell(s) than there are headers "
                f"(likely an unquoted comma); extra cells dropped from output: {extra}",
                severity="ERROR"
            )

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
        var = fixed_row.get(COL_VARIABLE, "")
        field_type = fixed_row.get(COL_FIELD_TYPE, "")

        # ── Variable name: flag (never rename) ───────────────────────────────
        if var and not VALID_VARIABLE_RE.match(var):
            refs = [r for r in find_references(rows, var) if r[0] != row_num]
            if refs:
                ref_text = (" Referenced as [" + var + "] by: "
                            + ", ".join(f"row {n} ({v})" for n, v in refs)
                            + " — any rename must update those references too.")
            else:
                ref_text = ""
            if VALID_VARIABLE_RE.match(var.lower()):
                issue = (f"Variable name '{var}' contains uppercase letters. REDCap "
                         f"variable names must be lowercase (e.g. '{var.lower()}'). "
                         "Not renamed automatically: renaming breaks references and "
                         "orphans any data already collected.")
            else:
                issue = (f"Variable name '{var}' contains invalid characters. REDCap "
                         "allows only lowercase letters, digits, and underscores, "
                         "starting with a letter. Not renamed automatically.")
            log_flag(issue + ref_text, severity="ERROR")

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

        # ── Validation min/max on fields that don't support them ──────────────
        if field_type not in MINMAX_TYPES:
            val_min = fixed_row.get(COL_VAL_MIN, "").strip()
            val_max = fixed_row.get(COL_VAL_MAX, "").strip()
            if val_min:
                fixed_row[COL_VAL_MIN] = ""
                log_change(COL_VAL_MIN, val_min, "", f"Cleared validation min (only valid on text/slider fields; field is '{field_type}')")
            if val_max:
                fixed_row[COL_VAL_MAX] = ""
                log_change(COL_VAL_MAX, val_max, "", f"Cleared validation max (only valid on text/slider fields; field is '{field_type}')")

        # ── Branching logic ───────────────────────────────────────────────────
        bl_raw = fixed_row.get(COL_BRANCHING, "").strip()
        if bl_raw:
            bl_fixed, bl_changes, bl_issues = fix_branching_logic(bl_raw)
            if bl_fixed != bl_raw:
                fixed_row[COL_BRANCHING] = bl_fixed
                combined = "; ".join(bl_changes)
                log_change(COL_BRANCHING, bl_raw, bl_fixed, f"Branching logic: {combined}")
            for issue in bl_issues:
                log_flag(f"Branching logic: {issue}")

        # ── Identifier? / Required Field? normalization ──────────────────────
        for col, label in ((COL_IDENTIFIER, "Identifier"), (COL_REQUIRED, "Required")):
            if col not in fixed_row:
                continue
            flag_raw = fixed_row.get(col, "")
            flag_fixed, flag_changes, recognised = normalize_yesno_flag(flag_raw)
            if not recognised:
                log_flag(
                    f"{col} has unrecognised value '{flag_raw}' (left unchanged). "
                    "REDCap accepts only 'y' or blank."
                )
            elif flag_changes:
                fixed_row[col] = flag_fixed
                for change in flag_changes:
                    log_change(col, flag_raw, flag_fixed, f"{label} flag: {change}")

        # ── Field Annotation ──────────────────────────────────────────────────
        ann_raw = fixed_row.get(COL_ANNOTATION, "").strip()
        if ann_raw:
            ann_fixed, ann_changes, ann_issues = fix_annotation(ann_raw)
            if ann_fixed != ann_raw:
                fixed_row[COL_ANNOTATION] = ann_fixed
                for change in ann_changes:
                    log_change(COL_ANNOTATION, ann_raw, ann_fixed, f"Annotation: {change}")
            for issue in ann_issues:
                log_flag(f"Annotation: {issue}")

        fixed_rows.append(fixed_row)

    return fixed_rows, change_log, flag_log


# ── Reporting ─────────────────────────────────────────────────────────────────

def build_text_report(change_log: list[dict], flag_log: list[dict], output_path: str) -> str:
    """Build a human-readable change and flag report."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"REDCap Data Dictionary Fixer — Report")
    lines.append(f"Output file: {output_path}")
    lines.append(f"{'='*60}")

    if change_log:
        lines.append(f"\n── AUTO-FIXES APPLIED ({len(change_log)}) ──────────────────────")
        for c in change_log:
            lines.append(f"  Row {c['row']} | {c['variable']} | {c['column']}")
            lines.append(f"    Fix: {c['fix']}")
            if len(c['old']) < 80 and len(c['new']) < 80:
                lines.append(f"    Before: {c['old']}")
                lines.append(f"    After:  {c['new']}")
    else:
        lines.append("\n✓ No auto-fixes needed.")

    if flag_log:
        errors = [f for f in flag_log if f['severity'] == 'ERROR']
        warnings = [f for f in flag_log if f['severity'] == 'WARNING']
        lines.append(f"\n── ISSUES REQUIRING MANUAL ATTENTION ({len(flag_log)}) ──────────")
        if errors:
            lines.append(f"\n  ERRORS (will prevent upload or cause data loss):")
            for f in errors:
                lines.append(f"  ✗ Row {f['row']} | {f['variable']}: {f['issue']}")
        if warnings:
            lines.append(f"\n  WARNINGS:")
            for f in warnings:
                lines.append(f"  ⚠ Row {f['row']} | {f['variable']}: {f['issue']}")
    else:
        lines.append("\n✓ No unresolvable issues detected.")

    lines.append("")
    return "\n".join(lines) + "\n"


def build_json_report(change_log: list[dict], flag_log: list[dict], output_path: str) -> str:
    report = {
        "output_file": output_path,
        "auto_fixes_applied": len(change_log),
        "issues_flagged": len(flag_log),
        "changes": change_log,
        "flags": flag_log,
    }
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Apply safe automatic fixes to a REDCap Data Dictionary CSV."
    )
    parser.add_argument("input", help="Path to the data dictionary CSV")
    parser.add_argument("--output", help="Path for the corrected CSV (default: <input>_fixed.csv)")
    parser.add_argument("--log-json", action="store_true", help="Emit the change log as JSON")
    args = parser.parse_args()

    input_path = args.input
    if args.output:
        output_path = args.output
    else:
        p = Path(input_path)
        output_path = str(p.parent / (p.stem + "_fixed" + p.suffix))

    out = Path(output_path)
    log_path = str(out.parent / (out.stem + "_changes" + (".json" if args.log_json else ".txt")))

    try:
        dd = read_dd(input_path)
        for note in dd.warnings:
            print(f"Note: {note}", file=sys.stderr)
        rows = dd.rows
        fixed_rows, change_log, flag_log = fix_dd(rows)

        # Build and save the change log before writing the CSV, so a corrected
        # file never exists without its log.
        if args.log_json:
            report = build_json_report(change_log, flag_log, output_path)
        else:
            report = build_text_report(change_log, flag_log, output_path)
        with open(log_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(report)

        # Same header style and column order as the input
        write_dd(output_path, fixed_rows, dd.header_style, dd.columns)

        sys.stdout.write(report)
        if not args.log_json:
            print(f"Change log saved to: {log_path}")

    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

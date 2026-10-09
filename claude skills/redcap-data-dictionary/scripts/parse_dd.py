#!/usr/bin/env python3
"""
REDCap Data Dictionary Parser
Parses a REDCap Data Dictionary and outputs a structured summary.

Usage:
    python parse_dd.py <data_dictionary.csv | metadata.json> [--text | --json] [--fields]

    --text    Human-readable project summary (default)
    --json    Structured JSON summary
    --fields  Every field in full (label, type, choices, validation, branching
              logic, annotation, ...), grouped by instrument, no truncation —
              suitable as LLM context. Add --json for the same as a JSON list.

Handles (via dd_common.py):
- UTF-8 with and without BOM, cp1252/latin-1 fallback
- Display headers ("Variable / Field Name", ...) or API headers (field_name, ...)
- JSON metadata from the API / a REDCap connector's export_metadata
- Large HTML fields in descriptive variables
- All 18 standard REDCap columns
- Cross-instrument branching logic dependencies
- Repeating instrument detection
- Instrument complexity ranking
- Choice value gap detection
- Action tag inventory and explanations
"""

import argparse
import html
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Windows consoles default to cp1252, which cannot print the report symbols.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# Shared Data Dictionary reading / constants (same folder as this script)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dd_common import (  # noqa: E402
    CHOICE_TYPES, VALID_FIELD_TYPES, COLUMNS, parse_choices, read_dd,
)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

# Action tag brief descriptions — checked against the KB action tag index (RC-AT-01)
# and the per-category articles RC-AT-03..11. Not exhaustive: for any tag not listed,
# look it up in RC-AT-01.
ACTION_TAG_DESCRIPTIONS = {
    "@NOMISSING":           "Disables missing data codes for this field (hides the M button); does not make the field required (RC-PROJ-04 §7.6)",
    "@HIDDEN":              "Hides field in both survey and data entry modes",
    "@HIDDEN-SURVEY":       "Hides field in survey mode only; still visible in data entry",
    "@HIDDEN-FORM":         "Hides field in data entry mode only; still visible in surveys",
    "@HIDDEN-PDF":          "Excludes field from PDF/print view of the instrument",
    "@READONLY":            "Makes field read-only in both survey and data entry",
    "@READONLY-SURVEY":     "Makes field read-only in survey mode only",
    "@IF":                  "Conditionally applies another action tag based on a logic expression: @IF([cond],'@TAG','')",
    "@CALCTEXT":            "Calculates a text value from an expression; Text Box fields only; the value is stored (RC-AT-09)",
    "@CALCDATE":            "Calculates a date from a source date + offset; Text Box fields with date validation only; the value is stored (RC-AT-09)",
    "@DEFAULT":             "Pre-fills the field with a specified value when the form first loads",
    "@SETVALUE":            "Like @DEFAULT, but re-applies the value on every form load, overwriting what is there (RC-AT-06)",
    "@NOW":                 "Pre-fills with the current date and time when the form loads",
    "@TODAY":               "Pre-fills with today's date when the form loads",
    "@PASSWORDMASK":        "Masks input as asterisks; value is still stored in plain text",
    "@NONEOFTHEABOVE":      "Adds a 'None of the above' option to a checkbox that unchecks all other selections when chosen",
    "@HIDEBUTTON":          "Hides the Today/Now button next to a date or datetime field (RC-AT-07)",
    "@HIDEDATEPICKER":      "Hides the calendar/time picker icon on a date, time or datetime field; not the Today/Now button; 17.5.0+ (RC-AT-07)",
    "@HIDESUBMIT-SURVEY":   "Hides the survey submit button — provided by an external module, not core REDCap (RC-AT-EM-01)",
    "@FORCE-MINMAX":        "Forces validation min/max enforcement even when the user tries to override the out-of-range warning",
    "@HIDECHOICE":          "Hides specific choice option(s) without removing them from the data",
    "@SHOWCHOICE":          "Shows specific choice option(s) that are otherwise hidden",
    "@CHARLIMIT":           "Limits the number of characters a user can enter in a text or notes field",
    "@PLACEHOLDER":         "Shows greyed-out placeholder text inside an empty text field",
    "@BARCODE-APP":         "Enables barcode scanning via the REDCap mobile app camera",
    "@LATITUDE":            "Captures GPS latitude coordinate via device location services",
    "@LONGITUDE":           "Captures GPS longitude coordinate via device location services",
    "@MAXCHECKED":          "Limits the maximum number of checkboxes that can be selected simultaneously",
    "@MAXCHOICE":           "Caps how many records can select each option, e.g. @MAXCHOICE(1=25,2=30); checked on page load only (RC-AT-03)",
    "@LANGUAGE-CURRENT-SURVEY": "Returns the language code of the current survey session (used in multi-language projects)",
}

# Heuristic keywords for project type classification
_CLINICAL_KEYWORDS = [
    "consent", "eligibility", "randomiz", "adverse_event", "ae_",
    "discharge", "screening", "enroll", "baseline", "follow_up",
    "medical_history", "blood", "vital", "medication", "inpatient",
    "outpatient", "intervention", "finalize", "completion",
]
_SURVEY_KEYWORDS = ["survey", "questionnaire", "participant_survey", "patient_reported"]
_ADMIN_KEYWORDS  = ["tracker", "notification", "announcement", "migration", "module", "admin"]


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def load_rows(path: str) -> list[dict]:
    """Read a DD (CSV or metadata JSON) via dd_common; drop fully blank rows
    (Excel often leaves trailing ',,,,' lines). Read notes go to stderr."""
    result = read_dd(path)
    for note in result.warnings:
        print(f"Note: {note}", file=sys.stderr)
    return [
        r for r in result.rows
        if any((v or "").strip() for k, v in r.items() if k is not None)
    ]


def strip_html(text: str) -> str:
    """Remove HTML tags for display purposes."""
    return re.sub(r"<[^>]+>", "", text).strip()


def check_choice_gaps(choices_str: str) -> list[tuple]:
    """
    Return a list of (lo, hi) gap pairs where numeric choice codes are non-consecutive.
    Returns None if codes are non-numeric (gaps are not meaningful).
    Returns [] if no gaps found.
    """
    choices = parse_choices(choices_str)
    numeric_values = []
    for c in choices:
        try:
            numeric_values.append(int(c["value"]))
        except ValueError:
            return None  # Non-numeric codes — gap check not applicable
    if len(numeric_values) < 2:
        return []
    numeric_values.sort()
    gaps = []
    for i in range(len(numeric_values) - 1):
        diff = numeric_values[i + 1] - numeric_values[i]
        if diff > 1:
            gaps.append((numeric_values[i], numeric_values[i + 1]))
    return gaps


def extract_action_tags(annotation: str) -> list[str]:
    """Extract @TAG action tag names from annotation text."""
    return re.findall(r"@[A-Z][A-Z0-9_-]*", annotation)


def classify_project_type(form_names: list[str], rows: list[dict]) -> str:
    """
    Heuristic classification of the project type based on instrument names and
    branching logic patterns. Returns a short descriptive label.
    """
    names_blob = " ".join(form_names).lower()
    has_longitudinal_bl = any(
        "arm" in r.get("Branching Logic (Show field only if...)", "").lower() or
        "arm" in r.get("Choices, Calculations, OR Slider Labels", "").lower()
        for r in rows
    )

    clinical_score = sum(1 for kw in _CLINICAL_KEYWORDS if kw in names_blob)
    survey_score   = sum(1 for kw in _SURVEY_KEYWORDS   if kw in names_blob)
    admin_score    = sum(1 for kw in _ADMIN_KEYWORDS     if kw in names_blob)

    if clinical_score >= 3 and has_longitudinal_bl:
        return "Clinical trial — longitudinal, multi-event"
    elif clinical_score >= 2:
        return "Clinical research study"
    elif admin_score >= 2:
        return "Administrative / operational tool"
    elif survey_score >= 1:
        return "Survey / questionnaire project"
    elif len(form_names) == 1:
        return "Single-instrument data collection"
    else:
        return "Research data collection project"


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def summarize(rows: list[dict]) -> dict:
    """Produce a structured summary of the data dictionary."""
    if not rows:
        return {"error": "No rows found in data dictionary."}

    total_fields = len(rows)

    # ── Field type counts ────────────────────────────────────────────────────
    field_type_counts = Counter(r.get("Field Type", "").strip() for r in rows)

    # ── Validation types used ────────────────────────────────────────────────
    validation_counts = Counter(
        r.get("Text Validation Type OR Show Slider Number", "").strip()
        for r in rows
        if r.get("Text Validation Type OR Show Slider Number", "").strip()
    )

    # ── Forms (instruments) ──────────────────────────────────────────────────
    forms_order: list[str] = []
    forms_map: dict[str, list] = defaultdict(list)
    for r in rows:
        fn = r.get("Form Name", "").strip()
        if fn and fn not in forms_order:
            forms_order.append(fn)
        if fn:
            forms_map[fn].append(r)

    # Build var→form lookup for cross-instrument dependency checks
    var_to_form: dict[str, str] = {
        r.get("Variable / Field Name", "").strip(): r.get("Form Name", "").strip()
        for r in rows
        if r.get("Variable / Field Name", "").strip()
    }

    # ── Per-instrument analysis ───────────────────────────────────────────────
    forms = []
    for fn in forms_order:
        form_rows = forms_map[fn]
        ft_counts = Counter(r.get("Field Type", "").strip() for r in form_rows)
        bl_count  = sum(1 for r in form_rows if r.get("Branching Logic (Show field only if...)", "").strip())
        calc_count = sum(1 for r in form_rows if r.get("Field Type", "").strip() == "calc")
        tag_count  = sum(1 for r in form_rows if r.get("Field Annotation", "").strip())
        has_survey_q_nums = any(r.get("Question Number (surveys only)", "").strip() for r in form_rows)
        has_current_instance = any(
            "[current-instance]" in (
                r.get("Choices, Calculations, OR Slider Labels", "") +
                r.get("Branching Logic (Show field only if...)", "") +
                r.get("Field Annotation", "")
            )
            for r in form_rows
        )
        # Complexity score: field count + weighted BL + calc + action tags
        complexity = len(form_rows) + (bl_count * 2) + (calc_count * 3) + tag_count

        forms.append({
            "name":                  fn,
            "field_count":           len(form_rows),
            "field_types":           dict(ft_counts),
            "bl_count":              bl_count,
            "calc_count":            calc_count,
            "action_tag_count":      tag_count,
            "complexity_score":      complexity,
            "likely_survey":         has_survey_q_nums,
            "likely_repeating":      has_current_instance,
        })

    # ── Record ID ────────────────────────────────────────────────────────────
    record_id_var = rows[0].get("Variable / Field Name", "").strip() if rows else "record_id"
    record_id_is_custom = record_id_var != "record_id"

    # ── Identifiers and required fields ──────────────────────────────────────
    identifiers = [
        r.get("Variable / Field Name", "").strip()
        for r in rows if r.get("Identifier?", "").strip().lower() == "y"
    ]
    required_fields = [
        r.get("Variable / Field Name", "").strip()
        for r in rows if r.get("Required Field?", "").strip().lower() == "y"
    ]

    # ── Matrix groups ─────────────────────────────────────────────────────────
    matrix_groups: dict[str, list] = defaultdict(list)
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
            "form":     r.get("Form Name", "").strip(),
            "formula":  r.get("Choices, Calculations, OR Slider Labels", "").strip(),
        }
        for r in rows if r.get("Field Type", "").strip() == "calc"
    ]

    # ── SQL fields ────────────────────────────────────────────────────────────
    sql_fields = [
        {
            "variable": r.get("Variable / Field Name", "").strip(),
            "form":     r.get("Form Name", "").strip(),
        }
        for r in rows if r.get("Field Type", "").strip() == "sql"
    ]

    # ── Action tags ───────────────────────────────────────────────────────────
    all_action_tags: Counter = Counter()
    action_tagged_fields = []
    for r in rows:
        ann = r.get("Field Annotation", "").strip()
        if ann:
            tags = extract_action_tags(ann)
            if tags:
                all_action_tags.update(tags)
                action_tagged_fields.append({
                    "variable":        r.get("Variable / Field Name", "").strip(),
                    "form":            r.get("Form Name", "").strip(),
                    "tags":            tags,
                    "full_annotation": ann,
                })

    # ── Branching logic + cross-instrument dependencies ───────────────────────
    branching_fields = []
    cross_instrument_deps = []

    for r in rows:
        bl = r.get("Branching Logic (Show field only if...)", "").strip()
        if not bl:
            continue
        var  = r.get("Variable / Field Name", "").strip()
        form = r.get("Form Name", "").strip()
        branching_fields.append({"variable": var, "form": form, "logic": bl})

        # Identify variable references (excluding event identifiers that contain 'arm')
        refs = re.findall(r"\[([a-z0-9_]+)\]", bl)
        for ref in refs:
            if "arm" in ref:
                continue  # event name, not a variable
            if ref not in var_to_form:
                continue  # might be a smart variable or system field
            ref_form = var_to_form[ref]
            if ref_form and ref_form != form:
                cross_instrument_deps.append({
                    "variable":           var,
                    "on_form":            form,
                    "references":         ref,
                    "from_form":          ref_form,
                })

    # Deduplicate cross-instrument deps (same pair may appear multiple times)
    seen_pairs: set = set()
    unique_cross_deps = []
    for dep in cross_instrument_deps:
        key = (dep["on_form"], dep["from_form"])
        if key not in seen_pairs:
            seen_pairs.add(key)
            unique_cross_deps.append({
                "dependent_form":    dep["on_form"],
                "depends_on_form":   dep["from_form"],
                "example_variable":  dep["variable"],
                "example_reference": dep["references"],
            })

    # ── Section headers ───────────────────────────────────────────────────────
    section_headers = [
        {
            "header_text": strip_html(r.get("Section Header", "").strip()),
            "on_variable": r.get("Variable / Field Name", "").strip(),
            "form":        r.get("Form Name", "").strip(),
        }
        for r in rows if r.get("Section Header", "").strip()
    ]

    # ── Descriptive fields ────────────────────────────────────────────────────
    descriptive_fields = [
        {
            "variable":      r.get("Variable / Field Name", "").strip(),
            "form":          r.get("Form Name", "").strip(),
            "label_preview": strip_html(r.get("Field Label", "")).strip()[:100],
        }
        for r in rows if r.get("Field Type", "").strip() == "descriptive"
    ]

    # ── Project type ──────────────────────────────────────────────────────────
    project_type = classify_project_type(forms_order, rows)

    # ── Instrument complexity ranking (top 5) ─────────────────────────────────
    top_complex = sorted(forms, key=lambda f: f["complexity_score"], reverse=True)[:5]

    # ── Potential issues ──────────────────────────────────────────────────────
    issues = []

    # SQL fields — must flag prominently
    if sql_fields:
        forms_with_sql = list(set(f["form"] for f in sql_fields))
        issues.append(
            f"SQL FIELDS ({len(sql_fields)} fields in {forms_with_sql}): "
            f"The 'sql' field type is administrator-only and driven by database queries "
            f"configured in REDCap's admin panel. These rows must NOT be edited or removed "
            f"from the Data Dictionary CSV — doing so will break the field's functionality."
        )

    # Required checkboxes
    for r in rows:
        ft  = r.get("Field Type", "").strip()
        req = r.get("Required Field?", "").strip().lower()
        var = r.get("Variable / Field Name", "").strip()
        if ft == "checkbox" and req == "y":
            issues.append(
                f"REQUIRED CHECKBOX: '{var}' is a checkbox marked as required — "
                f"REDCap cannot enforce 'at least one selected' on checkboxes. "
                f"The required flag will be silently ignored (RC-FD-08). Consider branching logic "
                f"or a validation check (e.g. a Data Quality rule) instead."
            )

    # Missing choices on choice-type fields
    for r in rows:
        ft      = r.get("Field Type", "").strip()
        choices = r.get("Choices, Calculations, OR Slider Labels", "").strip()
        var     = r.get("Variable / Field Name", "").strip()
        if ft in CHOICE_TYPES and not choices:
            issues.append(
                f"MISSING CHOICES: '{var}' is type '{ft}' but has no choices defined. "
                f"REDCap will reject this field on upload."
            )

    # Missing formula on calc fields
    for r in rows:
        ft      = r.get("Field Type", "").strip()
        formula = r.get("Choices, Calculations, OR Slider Labels", "").strip()
        var     = r.get("Variable / Field Name", "").strip()
        if ft == "calc" and not formula:
            issues.append(
                f"MISSING FORMULA: '{var}' is type 'calc' but has no formula. "
                f"The field will display as blank."
            )

    # Validation min/max on non-text fields (sliders use min/max as the slider's
    # lower/upper bound — confirmed on a real export, 2026-10-09)
    for r in rows:
        ft      = r.get("Field Type", "").strip()
        val_min = r.get("Text Validation Min", "").strip()
        val_max = r.get("Text Validation Max", "").strip()
        var     = r.get("Variable / Field Name", "").strip()
        if ft not in ("text", "slider") and (val_min or val_max):
            issues.append(
                f"VALIDATION ON NON-TEXT: '{var}' (type '{ft}') has validation min/max set, "
                f"which is only valid for text and slider fields. Upload will fail."
            )

    # Duplicate variable names
    var_names = [r.get("Variable / Field Name", "").strip() for r in rows]
    for v, count in Counter(var_names).items():
        if count > 1 and v:
            issues.append(f"DUPLICATE VARIABLE NAME: '{v}' appears {count} times. Upload will fail.")

    # Invalid field types
    for r in rows:
        ft  = r.get("Field Type", "").strip()
        var = r.get("Variable / Field Name", "").strip()
        if ft and ft not in VALID_FIELD_TYPES:
            issues.append(
                f"UNKNOWN FIELD TYPE: '{var}' has unsupported field type '{ft}'. "
                f"Upload will fail."
            )

    # Choice value gaps (flag but don't treat as errors — may be intentional coding)
    choice_gap_warnings = []
    for r in rows:
        ft      = r.get("Field Type", "").strip()
        choices = r.get("Choices, Calculations, OR Slider Labels", "").strip()
        var     = r.get("Variable / Field Name", "").strip()
        if ft in CHOICE_TYPES and choices:
            gaps = check_choice_gaps(choices)
            if gaps:
                gap_desc = ", ".join(f"{lo}→{hi}" for lo, hi in gaps)
                choice_gap_warnings.append({
                    "variable": var,
                    "form":     r.get("Form Name", "").strip(),
                    "gaps":     gap_desc,
                })

    # ── Project hints ──────────────────────────────────────────────────────────
    hints = [f"Project type: {project_type}"]
    if record_id_is_custom:
        hints.append(f"Custom record ID variable: '{record_id_var}' (not the default 'record_id') — typical in multi-site studies.")
    if len(forms) > 1:
        hints.append(f"Multi-instrument project: {len(forms)} instruments.")
    if calc_fields:
        hints.append(f"Contains {len(calc_fields)} calculated field(s).")
    if matrices:
        hints.append(f"Contains {len(matrices)} matrix group(s).")
    if identifiers:
        hints.append(f"Contains {len(identifiers)} identifier-flagged field(s).")
    repeating = [f["name"] for f in forms if f["likely_repeating"]]
    if repeating:
        hints.append(f"Likely repeating instrument(s) (uses [current-instance]): {repeating}.")
    has_longitudinal_bl = any(
        "arm" in r.get("Branching Logic (Show field only if...)", "").lower() or
        "arm" in r.get("Choices, Calculations, OR Slider Labels", "").lower()
        for r in rows
    )
    if has_longitudinal_bl:
        hints.append("Branching logic references event names — confirmed longitudinal project.")
    if unique_cross_deps:
        hints.append(
            f"{len(unique_cross_deps)} cross-instrument branching logic dependency pair(s) detected — "
            f"some instruments depend on values entered in other instruments."
        )

    # ── Assemble output ───────────────────────────────────────────────────────
    return {
        "file_summary": {
            "total_fields":        total_fields,
            "instrument_count":    len(forms),
            "record_id_variable":  record_id_var,
            "record_id_is_custom": record_id_is_custom,
            "project_type":        project_type,
        },
        "field_type_distribution": dict(field_type_counts),
        "validation_types_used":   dict(validation_counts),
        "instruments":             forms,
        "top_complex_instruments": [
            {"name": f["name"], "complexity_score": f["complexity_score"],
             "field_count": f["field_count"], "bl_count": f["bl_count"],
             "calc_count": f["calc_count"]}
            for f in top_complex
        ],
        "identifiers":    identifiers,
        "required_fields": required_fields,
        "matrices":       matrices,
        "sql_fields":     sql_fields,
        "calc_fields":    calc_fields,
        "action_tags": {
            "tag_frequency":   dict(all_action_tags),
            "tag_descriptions": {
                tag: ACTION_TAG_DESCRIPTIONS.get(tag, "(no description available)")
                for tag in all_action_tags
            },
            "tagged_fields":   action_tagged_fields,
        },
        "branching_logic": {
            "count":                len(branching_fields),
            "fields":               branching_fields,
            "cross_instrument_deps": unique_cross_deps,
        },
        "choice_gap_warnings": choice_gap_warnings,
        "section_headers":     section_headers,
        "descriptive_fields":  descriptive_fields,
        "project_hints":       hints,
        "potential_issues":    issues,
    }


# ---------------------------------------------------------------------------
# Text report
# ---------------------------------------------------------------------------

def print_text_report(summary: dict, filename: str) -> None:
    """Print a human-readable text summary."""
    fs = summary["file_summary"]

    print(f"\n{'='*65}")
    print(f"REDCap Data Dictionary: {filename}")
    print(f"{'='*65}")
    print(f"Project type:      {fs['project_type']}")
    print(f"Total fields:      {fs['total_fields']}")
    print(f"Instruments:       {fs['instrument_count']}")
    print(f"Record ID field:   {fs['record_id_variable']}"
          + (" (custom)" if fs["record_id_is_custom"] else ""))

    # ── Field types ───────────────────────────────────────────────────────────
    print(f"\n── Field Types ──")
    for ft, count in sorted(summary["field_type_distribution"].items(), key=lambda x: -x[1]):
        note = " ⚠️  (admin-only — do not edit in CSV)" if ft == "sql" else ""
        print(f"  {ft:<15} {count}{note}")

    # ── Instruments ────────────────────────────────────────────────────────────
    print(f"\n── Instruments ──")
    for form in summary["instruments"]:
        tags = []
        if form["likely_survey"]:    tags.append("survey")
        if form["likely_repeating"]: tags.append("repeating")
        tag_str = f"  [{', '.join(tags)}]" if tags else ""
        print(f"  {form['name']}: {form['field_count']} fields  "
              f"(complexity: {form['complexity_score']}, "
              f"BL: {form['bl_count']}, calc: {form['calc_count']}){tag_str}")
        for ft, cnt in sorted(form["field_types"].items(), key=lambda x: -x[1]):
            print(f"    {ft}: {cnt}")

    # ── Complexity ranking ─────────────────────────────────────────────────────
    if len(summary["instruments"]) > 1:
        print(f"\n── Most Complex Instruments (top 5) ──")
        for f in summary["top_complex_instruments"]:
            print(f"  {f['name']}: score={f['complexity_score']} "
                  f"({f['field_count']} fields, {f['bl_count']} BL, {f['calc_count']} calc)")

    # ── Cross-instrument dependencies ─────────────────────────────────────────
    cross = summary["branching_logic"]["cross_instrument_deps"]
    if cross:
        print(f"\n── Cross-Instrument Branching Logic Dependencies ({len(cross)}) ──")
        for dep in cross:
            print(f"  {dep['dependent_form']}  ←depends on→  {dep['depends_on_form']}")
            print(f"    (e.g. [{dep['example_reference']}] referenced by {dep['example_variable']})")

    # ── Identifiers ────────────────────────────────────────────────────────────
    if summary["identifiers"]:
        print(f"\n── Identifier Fields ({len(summary['identifiers'])}) ──")
        print(f"  {', '.join(summary['identifiers'])}")

    # ── Required fields (count only for large projects) ────────────────────────
    req = summary["required_fields"]
    if req:
        preview = req[:10]
        more    = len(req) - 10
        print(f"\n── Required Fields ({len(req)}) ──")
        print(f"  {', '.join(preview)}" + (f", ... and {more} more" if more > 0 else ""))

    # ── Matrix groups ──────────────────────────────────────────────────────────
    if summary["matrices"]:
        print(f"\n── Matrix Groups ({len(summary['matrices'])}) ──")
        for m in summary["matrices"]:
            print(f"  {m['group_name']}: {m['count']} variables")

    # ── Calculated fields ──────────────────────────────────────────────────────
    if summary["calc_fields"]:
        print(f"\n── Calculated Fields ({len(summary['calc_fields'])}) ──")
        for c in summary["calc_fields"]:
            preview = c["formula"][:70] + ("..." if len(c["formula"]) > 70 else "")
            print(f"  {c['variable']} ({c['form']}): {preview}")

    # ── Action tags ────────────────────────────────────────────────────────────
    tag_freq = summary["action_tags"]["tag_frequency"]
    tag_desc = summary["action_tags"]["tag_descriptions"]
    if tag_freq:
        print(f"\n── Action Tags ──")
        for tag, count in sorted(tag_freq.items(), key=lambda x: -x[1]):
            desc = tag_desc.get(tag, "")
            print(f"  {tag} ×{count}")
            if desc:
                print(f"    → {desc}")

    # ── Branching logic ────────────────────────────────────────────────────────
    bl_count = summary["branching_logic"]["count"]
    if bl_count:
        print(f"\n── Branching Logic ──")
        print(f"  {bl_count} field(s) have branching logic conditions.")

    # ── Choice value gap warnings ──────────────────────────────────────────────
    gap_warns = summary["choice_gap_warnings"]
    if gap_warns:
        print(f"\n── Choice Value Gaps (may be intentional — review) ({len(gap_warns)}) ──")
        for w in gap_warns[:15]:
            print(f"  {w['variable']} ({w['form']}): gap(s) at {w['gaps']}")
        if len(gap_warns) > 15:
            print(f"  ... and {len(gap_warns) - 15} more")

    # ── Project hints ──────────────────────────────────────────────────────────
    if summary["project_hints"]:
        print(f"\n── Project Hints ──")
        for hint in summary["project_hints"]:
            print(f"  • {hint}")

    # ── Issues ─────────────────────────────────────────────────────────────────
    if summary["potential_issues"]:
        print(f"\n── ⚠️  Potential Issues ({len(summary['potential_issues'])}) ──")
        for issue in summary["potential_issues"]:
            print(f"  ⚠️  {issue}")
            print()
    else:
        print(f"\n✓ No structural issues detected.")

    print()


# ---------------------------------------------------------------------------
# Full per-field listing (--fields)
# ---------------------------------------------------------------------------

_IMPLIED_CHOICES = {
    "yesno":     [{"value": "1", "label": "Yes"}, {"value": "0", "label": "No"}],
    "truefalse": [{"value": "1", "label": "True"}, {"value": "0", "label": "False"}],
}


def html_to_text(text: str) -> str:
    """HTML → plain text without truncation: <br>/<p>/<li> become line breaks,
    tags are removed, entities decoded, blank lines and runs of spaces collapsed."""
    text = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr)>", "\n", text or "")
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def field_records(rows: list[dict]) -> list[dict]:
    """One complete record per field, in DD order."""
    records = []
    for r in rows:
        get = lambda col: (r.get(col) or "").strip()  # noqa: E731
        ft = get("Field Type")
        col_f = get("Choices, Calculations, OR Slider Labels")
        rec = {
            "variable":        get("Variable / Field Name"),
            "form":            get("Form Name"),
            "section_header":  html_to_text(get("Section Header")),
            "field_type":      ft,
            "label":           html_to_text(get("Field Label")),
            "choices":         parse_choices(col_f) if ft in CHOICE_TYPES else _IMPLIED_CHOICES.get(ft, []),
            "calculation":     col_f if ft == "calc" else "",
            "slider_labels":   col_f if ft == "slider" else "",
            "other_column_f":  col_f if ft not in CHOICE_TYPES | {"calc", "slider"} else "",
            "field_note":      html_to_text(get("Field Note")),
            "validation":      get("Text Validation Type OR Show Slider Number"),
            "validation_min":  get("Text Validation Min"),
            "validation_max":  get("Text Validation Max"),
            "identifier":      get("Identifier?").lower() == "y",
            "required":        get("Required Field?").lower() == "y",
            "branching_logic": get("Branching Logic (Show field only if...)"),
            "custom_alignment": get("Custom Alignment"),
            "question_number": get("Question Number (surveys only)"),
            "matrix_group":    get("Matrix Group Name"),
            "matrix_ranking":  get("Matrix Ranking?").lower() == "y",
            "annotation":      get("Field Annotation"),
        }
        # Keep any non-standard columns rather than silently dropping them
        for k, v in r.items():
            if k is not None and k not in COLUMNS and (v or "").strip():
                rec.setdefault("extra_columns", {})[k] = v.strip()
        records.append(rec)
    return records


def print_fields_report(records: list[dict], filename: str) -> None:
    """Print every field in full, grouped by instrument."""
    forms: dict[str, list] = defaultdict(list)
    for rec in records:
        forms[rec["form"]].append(rec)

    def block(label: str, value: str, indent: str = "    ") -> None:
        if not value:
            return
        lines = value.splitlines()
        print(f"{indent}{label}: {lines[0]}")
        for ln in lines[1:]:
            print(f"{indent}{' ' * (len(label) + 2)}{ln}")

    print(f"REDCap Data Dictionary — all fields: {filename}")
    print(f"{len(records)} fields in {len(forms)} instrument(s). "
          "Labels are shown as plain text (HTML removed); nothing is truncated.")
    for form, recs in forms.items():
        print(f"\n{'=' * 65}\nInstrument: {form or '(no form name)'}  ({len(recs)} fields)\n{'=' * 65}")
        for rec in recs:
            if rec["section_header"]:
                print(f"\n  --- Section: {rec['section_header'].replace(chr(10), ' / ')} ---")
            print(f"\n  [{rec['variable']}] ({rec['field_type']})")
            block("label", rec["label"])
            if rec["choices"]:
                implied = " (built-in)" if rec["field_type"] in _IMPLIED_CHOICES else ""
                block(f"choices{implied}",
                      "\n".join(f"{c['value']} = {c['label']}" for c in rec["choices"]))
            block("calculation", rec["calculation"])
            block("slider labels", rec["slider_labels"])
            block("column F", rec["other_column_f"])
            val = rec["validation"]
            if rec["validation_min"] or rec["validation_max"]:
                val += f" (min {rec['validation_min'] or '-'}, max {rec['validation_max'] or '-'})"
            block("validation", val.strip())
            block("note", rec["field_note"])
            flags = [name for name, on in (("identifier", rec["identifier"]),
                                           ("required", rec["required"]),
                                           ("matrix ranking", rec["matrix_ranking"])) if on]
            block("flags", ", ".join(flags))
            block("show only if", rec["branching_logic"])
            block("matrix group", rec["matrix_group"])
            block("alignment", rec["custom_alignment"])
            block("question number", rec["question_number"])
            block("annotation", rec["annotation"])
            for k, v in rec.get("extra_columns", {}).items():
                block(k, v)
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Summarize a REDCap Data Dictionary (CSV with display or API "
                    "headers, or export_metadata JSON).")
    ap.add_argument("path", help="Data Dictionary CSV or metadata JSON")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--text", action="store_true", help="text output (default)")
    ap.add_argument("--fields", action="store_true",
                    help="list every field in full instead of the summary")
    args = ap.parse_args()

    path = args.path
    try:
        rows = load_rows(path)
        if args.fields:
            records = field_records(rows)
            if args.json:
                print(json.dumps(records, indent=2, ensure_ascii=False))
            else:
                print_fields_report(records, Path(path).name)
            return
        summary = summarize(rows)
        if "error" in summary:
            raise ValueError(summary["error"])
        if args.json:
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print_text_report(summary, Path(path).name)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

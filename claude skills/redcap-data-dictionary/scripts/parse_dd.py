#!/usr/bin/env python3
"""
REDCap Data Dictionary Parser
Parses a REDCap Data Dictionary CSV and outputs a structured JSON summary.

Usage:
    python parse_dd.py <path_to_data_dictionary.csv> [--json | --text]

Handles:
- UTF-8 with and without BOM
- Large HTML fields in descriptive variables
- All 18 standard REDCap columns
- Cross-instrument branching logic dependencies
- Repeating instrument detection
- Instrument complexity ranking
- Choice value gap detection
- Action tag inventory and explanations
"""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# REDCap descriptive fields can contain large HTML blobs; raise the limit
csv.field_size_limit(10 * 1024 * 1024)  # 10 MB

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

VALID_FIELD_TYPES = {
    "text", "notes", "dropdown", "radio", "checkbox",
    "calc", "file", "descriptive", "slider", "yesno",
    "truefalse", "sql",
}

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}

# Action tag brief descriptions — drawn from RC-FD-08 and REDCap documentation.
# NOTE: A full KB article (RC-AT-01) has not yet been written. These descriptions
# cover the tags observed across the example projects; the list is not exhaustive.
ACTION_TAG_DESCRIPTIONS = {
    "@NOMISSING":           "Prevents saving with a missing value even when field is not in the Required list; commonly used in clinical trials to enforce data completeness",
    "@HIDDEN":              "Hides field in both survey and data entry modes",
    "@HIDDEN-SURVEY":       "Hides field in survey mode only; still visible in data entry",
    "@HIDDEN-FORM":         "Hides field in data entry mode only; still visible in surveys",
    "@HIDDEN-PDF":          "Excludes field from PDF/print view of the instrument",
    "@READONLY":            "Makes field read-only in both survey and data entry",
    "@READONLY-SURVEY":     "Makes field read-only in survey mode only",
    "@IF":                  "Conditionally applies another action tag based on a logic expression: @IF([cond],'@TAG','')",
    "@CALCTEXT":            "Displays a calculated text string in a descriptive field; value is not stored",
    "@CALCDATE":            "Displays a calculated date in a descriptive field; value is not stored",
    "@DEFAULT":             "Pre-fills the field with a specified value when the form first loads",
    "@SETVALUE":            "Programmatically sets a field value, typically used with smart variables or piping",
    "@NOW":                 "Pre-fills with the current date and time when the form loads",
    "@TODAY":               "Pre-fills with today's date when the form loads",
    "@PASSWORDMASK":        "Masks input as asterisks; value is still stored in plain text",
    "@NONEOFTHEABOVE":      "Adds a 'None of the above' option to a checkbox that unchecks all other selections when chosen",
    "@HIDEBUTTON":          "Hides the save/submit button on a form or survey page",
    "@HIDESUBMIT-SURVEY":   "Hides the submit button on a survey page",
    "@FORCE-MINMAX":        "Forces validation min/max enforcement even when the user tries to override the out-of-range warning",
    "@HIDECHOICE":          "Hides specific choice option(s) without removing them from the data",
    "@SHOWCHOICE":          "Shows specific choice option(s) that are otherwise hidden",
    "@CHARLIMIT":           "Limits the number of characters a user can enter in a text or notes field",
    "@PLACEHOLDER":         "Shows greyed-out placeholder text inside an empty text field",
    "@BARCODE-APP":         "Enables barcode scanning via the REDCap mobile app camera",
    "@BARCODE":             "Enables barcode scanning (generic; use @BARCODE-APP for mobile app context)",
    "@LATITUDE":            "Captures GPS latitude coordinate via device location services",
    "@LONGITUDE":           "Captures GPS longitude coordinate via device location services",
    "@MAXCHECKED":          "Limits the maximum number of checkboxes that can be selected simultaneously",
    "@MAXCHOICE":           "Limits the maximum number of choices selectable",
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

def read_dd(path: str) -> list[dict]:
    """Read a data dictionary CSV, handling BOM and encoding gracefully."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(path, encoding=encoding, newline="") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
                if rows and "Variable / Field Name" not in rows[0]:
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
            choices.append({"value": value.strip(), "label": label.strip()})
        else:
            choices.append({"value": item, "label": item})
    return choices


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
                f"The required flag will be silently ignored. Consider using branching logic "
                f"or @NOMISSING on individual checkbox sub-options instead."
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

    # Validation min/max on non-text fields
    for r in rows:
        ft      = r.get("Field Type", "").strip()
        val_min = r.get("Text Validation Min", "").strip()
        val_max = r.get("Text Validation Max", "").strip()
        var     = r.get("Variable / Field Name", "").strip()
        if ft != "text" and (val_min or val_max):
            issues.append(
                f"VALIDATION ON NON-TEXT: '{var}' (type '{ft}') has validation min/max set, "
                f"which is only valid for text fields. Upload will fail."
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
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: parse_dd.py <data_dictionary.csv> [--json | --text]")
        sys.exit(1)

    path          = sys.argv[1]
    output_format = "json" if "--json" in sys.argv else "text"

    try:
        rows    = read_dd(path)
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

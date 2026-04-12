#!/usr/bin/env python3
"""
REDCap Codebook Reader
Reads a REDCap Codebook PDF or Data Dictionary CSV and produces either
a narrative summary or a compact LLM-context dump of the full project.

Usage:
    python codebook_report.py <path> [--summary | --llm-context]

Input formats:
  .pdf  — "Download PDF of All Instruments" export from REDCap (preferred for
          longitudinal projects: includes events table and repeating structure)
  .csv  — Data Dictionary CSV export (field content only; no event table)

Output modes:
  --summary      (default) Narrative prose for human reading
  --llm-context  Compact structured dump for LLM consumption (token-efficient)

Dependencies:
  PDF mode requires pdfplumber:
      pip install pdfplumber --break-system-packages
"""

import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10 * 1024 * 1024)  # Handle large HTML descriptive fields

# ── Reference data ────────────────────────────────────────────────────────────

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}

VALID_FIELD_TYPES = {
    "text", "notes", "dropdown", "radio", "checkbox",
    "calc", "file", "descriptive", "slider", "yesno",
    "truefalse", "sql",
}

_CLINICAL_KW = [
    "consent", "eligib", "randomiz", "adverse_event", "ae_", "discharge",
    "screen", "enroll", "baseline", "follow_up", "medical_history", "vital",
    "medication", "inpatient", "outpatient", "intervention",
]
_SURVEY_KW  = ["survey", "questionnaire", "patient_reported"]
_ADMIN_KW   = ["tracker", "notification", "announcement", "admin", "migration"]


# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text).strip()


def parse_choices(choices_str: str) -> list:
    choices = []
    for item in choices_str.split("|"):
        item = item.strip()
        if "," in item:
            value, label = item.split(",", 1)
            choices.append({"value": value.strip(), "label": label.strip()})
        else:
            choices.append({"value": item, "label": item})
    return choices


def extract_action_tags(annotation: str) -> list:
    return re.findall(r"@[A-Z][A-Z0-9_-]*", annotation)


def classify_project_type(form_names: list, field_labels: list = None) -> str:
    names_blob = " ".join(form_names).lower()
    labels_blob = " ".join(field_labels or []).lower()
    combined = names_blob + " " + labels_blob

    clinical = sum(1 for kw in _CLINICAL_KW if kw in combined)
    survey   = sum(1 for kw in _SURVEY_KW   if kw in combined)
    admin    = sum(1 for kw in _ADMIN_KW     if kw in combined)

    if clinical >= 3:
        return "Clinical research study"
    elif admin >= 2:
        return "Administrative / operational tool"
    elif survey >= 1:
        return "Survey / questionnaire project"
    elif len(form_names) == 1:
        return "Single-instrument data collection"
    else:
        return "Research data collection project"


def fmt_choices(choices: list, max_choices: int = 12) -> str:
    """Compact choice string: v=Label | v=Label"""
    if not choices:
        return ""
    parts = [f"{c['value']}={c['label']}" for c in choices[:max_choices]]
    suffix = f" | …+{len(choices)-max_choices} more" if len(choices) > max_choices else ""
    return " | ".join(parts) + suffix


def abbreviate_bl(bl: str, max_len: int = 120) -> str:
    """Shorten a branching logic expression for display."""
    bl = bl.strip()
    if len(bl) <= max_len:
        return bl
    return bl[:max_len] + "…"


# ── Data model ────────────────────────────────────────────────────────────────

def new_project() -> dict:
    return {
        "project_title": "",
        "project_pid": None,
        "snapshot_date": None,
        "project_type": "Research data collection project",
        "source_format": "",
        "is_longitudinal": False,
        "instruments": [],      # list of instrument dicts
        "events": [],           # list of event dicts (longitudinal only)
    }


def new_instrument(display_name: str, form_name: str) -> dict:
    return {
        "display_name": display_name,
        "form_name": form_name,
        "is_survey": False,
        "is_repeating": False,
        "events": [],           # event unique names assigned to this instrument
        "fields": [],           # list of field dicts
    }


def new_field() -> dict:
    return {
        "number": None,
        "variable": "",
        "label": "",
        "type": "",
        "choices": [],
        "formula": None,
        "validation": None,
        "validation_min": None,
        "validation_max": None,
        "branching_logic": None,
        "required": False,
        "identifier": False,
        "action_tags": [],
        "field_note": None,
        "section_header": None,
    }


# ── CSV parser ────────────────────────────────────────────────────────────────

def parse_csv(path: str) -> dict:
    """
    Parse a REDCap Data Dictionary CSV into the project data model.
    Produces complete field-level content (labels, choices, branching logic).
    Does NOT include event table or repeating structure (not in the CSV format).
    """
    p = Path(path)
    rows = None
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(p, encoding=encoding, newline="") as fh:
                reader = csv.DictReader(fh)
                rows = list(reader)
                if rows and "Variable / Field Name" in rows[0]:
                    break
                rows = None
        except UnicodeDecodeError:
            continue

    if not rows:
        raise ValueError(f"Could not parse as a REDCap Data Dictionary CSV: {path}")

    project = new_project()
    project["source_format"] = "csv"
    # Strip common REDCap filename suffixes to get a clean title
    stem = p.stem
    stem = re.sub(r"_DataDictionary.*$", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"_data_dictionary.*$", "", stem, flags=re.IGNORECASE)
    project["project_title"] = stem

    # Build instrument→field groups preserving order
    forms_order: list = []
    forms_map: dict = defaultdict(list)
    for r in rows:
        fn = r.get("Form Name", "").strip()
        if fn and fn not in forms_order:
            forms_order.append(fn)
        if fn:
            forms_map[fn].append(r)

    all_labels: list = []
    field_number = 1

    for fn in forms_order:
        form_rows = forms_map[fn]
        # Derive display name: title-case of the snake_case form name
        display = fn.replace("_", " ").title()
        instr = new_instrument(display, fn)

        has_survey_q = any(r.get("Question Number (surveys only)", "").strip() for r in form_rows)
        instr["is_survey"] = has_survey_q

        has_current_instance = any(
            "[current-instance]" in (
                r.get("Choices, Calculations, OR Slider Labels", "") +
                r.get("Branching Logic (Show field only if...)", "") +
                r.get("Field Annotation", "")
            )
            for r in form_rows
        )
        instr["is_repeating"] = has_current_instance

        for r in form_rows:
            f = new_field()
            f["number"] = field_number
            field_number += 1

            f["variable"] = r.get("Variable / Field Name", "").strip()
            raw_label = r.get("Field Label", "").strip()
            f["label"] = strip_html(raw_label)
            all_labels.append(f["label"])

            f["type"] = r.get("Field Type", "").strip()

            sec_hdr = r.get("Section Header", "").strip()
            f["section_header"] = strip_html(sec_hdr) or None

            f["field_note"] = r.get("Field Note", "").strip() or None
            f["required"] = r.get("Required Field?", "").strip().lower() == "y"
            f["identifier"] = r.get("Identifier?", "").strip().lower() == "y"

            choices_raw = r.get("Choices, Calculations, OR Slider Labels", "").strip()
            if f["type"] in CHOICE_TYPES and choices_raw:
                f["choices"] = parse_choices(choices_raw)
            elif f["type"] == "calc" and choices_raw:
                f["formula"] = choices_raw

            f["validation"]     = r.get("Text Validation Type OR Show Slider Number", "").strip() or None
            f["validation_min"] = r.get("Text Validation Min", "").strip() or None
            f["validation_max"] = r.get("Text Validation Max", "").strip() or None

            bl = r.get("Branching Logic (Show field only if...)", "").strip()
            f["branching_logic"] = bl or None

            ann = r.get("Field Annotation", "").strip()
            if ann:
                f["action_tags"] = extract_action_tags(ann)

            instr["fields"].append(f)

        project["instruments"].append(instr)

    # Classify project type
    project["project_type"] = classify_project_type(forms_order, all_labels)

    # Detect longitudinal hints in branching logic / calc formulas
    longitudinal_pattern = re.compile(r"\[[a-z0-9_]+_arm_\d+\]")
    project["is_longitudinal"] = any(
        longitudinal_pattern.search(
            r.get("Branching Logic (Show field only if...)", "") +
            r.get("Choices, Calculations, OR Slider Labels", "")
        )
        for r in rows
    )

    return project


# ── PDF parser ────────────────────────────────────────────────────────────────

def parse_pdf(path: str) -> dict:
    """
    Parse a REDCap Codebook PDF (the "Download PDF of All Instruments" export).
    Extracts project header, instruments summary table, events table (longitudinal),
    and the per-field table.

    Requires pdfplumber:
        pip install pdfplumber --break-system-packages
    """
    try:
        import pdfplumber
    except ImportError:
        print(
            "ERROR: pdfplumber is required for PDF parsing.\n"
            "Install it with: pip install pdfplumber --break-system-packages",
            file=sys.stderr,
        )
        sys.exit(1)

    project = new_project()
    project["source_format"] = "pdf"

    with pdfplumber.open(path) as pdf:
        # ── Collect all page text ─────────────────────────────────────────────
        all_text_pages: list = []
        for page in pdf.pages:
            t = page.extract_text(x_tolerance=3, y_tolerance=3) or ""
            all_text_pages.append(t)

        full_text = "\n".join(all_text_pages)

        # ── Parse header from first page ──────────────────────────────────────
        first_text = all_text_pages[0] if all_text_pages else ""
        project["project_title"] = _pdf_title(first_text)
        project["project_pid"]   = _pdf_pid(first_text)
        project["snapshot_date"] = _pdf_date(first_text)

        # ── Collect tables from all pages ─────────────────────────────────────
        all_tables: list = []
        for page in pdf.pages:
            tables = page.extract_tables() or []
            all_tables.extend(tables)

        # ── Parse summary table (instruments) and events table ────────────────
        _pdf_parse_summary_tables(project, all_tables)

        # ── Parse the main field table ─────────────────────────────────────────
        _pdf_parse_fields(project, all_tables, full_text)

    # Classify project
    form_names = [i["form_name"] for i in project["instruments"]]
    all_labels = [f["label"] for i in project["instruments"] for f in i["fields"]]
    project["project_type"] = classify_project_type(form_names, all_labels)

    return project


def _pdf_title(text: str) -> str:
    """Extract project title from codebook PDF first-page text."""
    # Header pattern: "Data Dictionary Codebook\nProject Name (PID: 1234)"
    m = re.search(r"Data Dictionary Codebook\s*\n(.+?)(?:\s*\(PID:|$)", text)
    if m:
        return m.group(1).strip()
    # Fallback: first non-empty line after "Codebook"
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        if "Codebook" in line and i + 1 < len(lines):
            candidate = lines[i + 1]
            if "Data Dictionary" not in candidate:
                return candidate
    return "Unknown Project"


def _pdf_pid(text: str) -> str | None:
    m = re.search(r"PID:\s*(\d+)", text)
    return m.group(1) if m else None


def _pdf_date(text: str) -> str | None:
    # REDCap date format in codebook header: "MM-DD-YYYY H:MMam/pm"
    m = re.search(r"(\d{2}-\d{2}-\d{4}\s+\d+:\d+(?:am|pm))", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def _pdf_parse_summary_tables(project: dict, all_tables: list) -> None:
    """
    Identify and parse the Instruments and Events summary tables from all tables.
    Instruments table header: Instrument | Form Name | [Events]
    Events table header: Event Name | Unique event name | Event ID
    """
    for table in all_tables:
        if not table or len(table) < 2:
            continue
        header = [str(c or "").strip().lower() for c in table[0]]

        # Events table
        if any("unique event" in h for h in header) or any("event id" in h for h in header):
            project["is_longitudinal"] = True
            for row in table[1:]:
                if not row or all(c is None or str(c).strip() == "" for c in row):
                    continue
                cells = [str(c or "").strip() for c in row]
                ev = {
                    "display_name":       cells[0] if len(cells) > 0 else "",
                    "unique_event_name":  cells[1] if len(cells) > 1 else "",
                    "event_id":           cells[2] if len(cells) > 2 else None,
                    "is_repeating":       any("repeat" in str(c).lower() for c in cells),
                }
                if ev["unique_event_name"]:
                    project["events"].append(ev)

        # Instruments summary table
        elif ("instrument" in header or "form name" in header) and len(header) >= 2:
            # Only process if we don't already have instruments from field parsing
            for row in table[1:]:
                if not row or all(c is None or str(c).strip() == "" for c in row):
                    continue
                cells = [str(c or "").strip() for c in row]
                display  = cells[0] if len(cells) > 0 else ""
                form_nm  = cells[1] if len(cells) > 1 else ""
                events_s = cells[2] if len(cells) > 2 else ""
                if display or form_nm:
                    # Store event assignment info; reconcile later with field table
                    pass  # Event assignments are captured per-instrument during field parsing


def _pdf_parse_fields(project: dict, all_tables: list, full_text: str) -> None:
    """
    Parse the main field-by-field table from the codebook PDF.
    Expected columns: # | Variable/Field Name [+BL] | Field Label | Field Attributes

    Falls back to text-based parsing if table extraction fails.
    """
    # Try to find the main field table(s)
    # Field tables have a numeric first column and 4 columns total
    field_tables = []
    for table in all_tables:
        if not table or len(table) < 2:
            continue
        # Identify field tables: first data cell is a number, and 4 columns
        first_data_row = next((r for r in table[1:] if r and any(str(c or "").strip() for c in r)), None)
        if first_data_row is None:
            continue
        first_cell = str(first_data_row[0] or "").strip()
        if len(table[0]) >= 3 and re.match(r"^\d+$", first_cell):
            field_tables.append(table)

    if field_tables:
        _parse_field_tables(project, field_tables)
    else:
        # Fallback: text-based parsing
        _parse_fields_from_text(project, full_text)


def _parse_field_tables(project: dict, field_tables: list) -> None:
    """Parse instruments and fields from structured field tables."""
    current_instr: dict | None = None

    for table in field_tables:
        for row in table:
            if not row:
                continue
            cells = [str(c or "").strip() for c in row]

            # Skip pure header rows
            if cells and cells[0].lower() in ("#", "variable / field name", ""):
                # Check if this might be an instrument banner (full-width row)
                non_empty = [c for c in cells if c]
                if len(non_empty) == 1 and current_instr is not None:
                    # Single text in row = likely instrument banner in some PDF layouts
                    pass
                continue

            # Instrument banner: row where field # is empty and text describes instrument
            if not cells[0] and cells[1] if len(cells) > 1 else False:
                banner_text = " ".join(c for c in cells if c)
                # Try to detect "Display Name\nform_name" pattern
                m = re.search(r"([^\n]+)\n([a-z][a-z0-9_]*)", banner_text)
                if m:
                    display_nm = m.group(1).strip()
                    form_nm    = m.group(2).strip()
                else:
                    display_nm = banner_text.strip()
                    form_nm    = banner_text.strip().lower().replace(" ", "_")

                is_surv = "survey" in banner_text.lower() or "enabled as survey" in banner_text.lower()
                current_instr = new_instrument(display_nm, form_nm)
                current_instr["is_survey"] = is_surv
                project["instruments"].append(current_instr)
                continue

            # Field row: first cell is a field number
            if re.match(r"^\d+$", cells[0]):
                if current_instr is None:
                    current_instr = new_instrument("Unknown", "unknown")
                    project["instruments"].append(current_instr)

                f = new_field()
                f["number"] = int(cells[0])

                # Column 2: variable name + optional branching logic
                var_cell = cells[1] if len(cells) > 1 else ""
                bl_match = re.split(r"\nShow the field ONLY if:|Show the field ONLY if:", var_cell, maxsplit=1)
                f["variable"] = bl_match[0].strip()
                if len(bl_match) > 1:
                    f["branching_logic"] = bl_match[1].strip() or None

                # Column 3: field label (+ section header above + field note below)
                label_cell = cells[2] if len(cells) > 2 else ""
                label_lines = label_cell.splitlines()
                # Heuristic: if first line looks like a section header (short, title-like)
                # and there are multiple lines, the first is the section header
                f["label"] = label_cell.strip()

                # Column 4: field attributes
                attr_cell = cells[3] if len(cells) > 3 else ""
                _parse_field_attributes(f, attr_cell)

                current_instr["fields"].append(f)


def _parse_field_attributes(f: dict, attr_text: str) -> None:
    """Parse the Field Attributes column content into a field dict."""
    text = attr_text.strip()
    if not text:
        return

    # Required / Identifier flags
    f["required"]   = "Required" in text
    f["identifier"] = "Identifier" in text

    # Field type — first token before comma or newline
    type_match = re.match(r"^([a-z]+(?:\s*\(Matrix\))?)", text.lower())
    if type_match:
        raw_type = type_match.group(1).strip()
        if "matrix" in raw_type:
            f["type"] = "radio"  # matrix groups use radio
        else:
            f["type"] = raw_type.split("(")[0].strip()

    # Validation: "text (date_mdy)" or "text (email)"
    val_match = re.search(r"text\s*\(([^)]+)\)", text, re.IGNORECASE)
    if val_match:
        f["validation"] = val_match.group(1).strip()

    # Choices: look for "Choices:" block or coded value lines like "0, Label"
    choices_block = re.search(r"Choices?:\s*(.+?)(?=Calculation:|Annotation:|Required|Identifier|$)", text, re.DOTALL | re.IGNORECASE)
    if choices_block:
        choices_text = choices_block.group(1).strip()
        # Parse lines like "0, Label\n1, Another"
        choices = []
        for line in choices_text.splitlines():
            line = line.strip()
            m = re.match(r"^(\S+),\s*(.+)$", line)
            if m:
                choices.append({"value": m.group(1).strip(), "label": m.group(2).strip()})
        if choices:
            f["choices"] = choices

    # Calculation formula
    calc_match = re.search(r"Calculation:\s*(.+?)(?=Annotation:|Required|Identifier|$)", text, re.DOTALL | re.IGNORECASE)
    if calc_match:
        f["formula"] = calc_match.group(1).strip()

    # Action tags from annotation line
    ann_match = re.search(r"Annotation:\s*(.+?)(?=Required|Identifier|$)", text, re.DOTALL | re.IGNORECASE)
    if ann_match:
        f["action_tags"] = extract_action_tags(ann_match.group(1))
    else:
        # Also check raw text for @tags
        f["action_tags"] = extract_action_tags(text)


def _parse_fields_from_text(project: dict, full_text: str) -> None:
    """
    Fallback text-based field parser when table extraction fails.
    Uses line patterns to detect instrument banners and field entries.
    """
    current_instr: dict | None = None
    field_number = 0

    for line in full_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Instrument banner: lines that look like form headers
        # Pattern: all-caps or title-case line not starting with a number
        if re.match(r"^[A-Z][A-Za-z\s&-]+$", line) and len(line) > 5 and not re.match(r"^\d", line):
            # Could be an instrument name
            if not any(kw in line for kw in ["Field", "Variable", "Label", "Attributes", "Data Dictionary"]):
                form_nm = line.lower().replace(" ", "_")
                current_instr = new_instrument(line, form_nm)
                project["instruments"].append(current_instr)
                continue

        # Field entry: line starting with a number
        m = re.match(r"^(\d+)\s+([a-z][a-z0-9_]*)\s+(.*)", line)
        if m and current_instr is not None:
            field_number = int(m.group(1))
            f = new_field()
            f["number"] = field_number
            f["variable"] = m.group(2).strip()
            f["label"] = m.group(3).strip()
            current_instr["fields"].append(f)


# ── Summary stats ─────────────────────────────────────────────────────────────

def compute_stats(project: dict) -> dict:
    """Compute aggregate statistics across all instruments."""
    all_fields = [f for i in project["instruments"] for f in i["fields"]]
    ft_dist = Counter(f["type"] for f in all_fields)
    return {
        "total_fields":            len(all_fields),
        "instrument_count":        len(project["instruments"]),
        "field_type_distribution": dict(ft_dist),
        "branching_logic_count":   sum(1 for f in all_fields if f["branching_logic"]),
        "calc_count":              ft_dist.get("calc", 0),
        "identifier_count":        sum(1 for f in all_fields if f["identifier"]),
        "required_count":          sum(1 for f in all_fields if f["required"]),
        "action_tagged_count":     sum(1 for f in all_fields if f["action_tags"]),
        "survey_count":            sum(1 for i in project["instruments"] if i["is_survey"]),
        "repeating_count":         sum(1 for i in project["instruments"] if i["is_repeating"]),
    }


# ── Output: --summary ─────────────────────────────────────────────────────────

def print_summary(project: dict) -> None:
    """
    Human-readable narrative summary of the project.
    Focuses on what the project is, what it collects, and notable design features.
    """
    stats = compute_stats(project)
    instruments = project["instruments"]

    print(f"\n{'='*70}")
    title = project["project_title"]
    if project["project_pid"]:
        title += f" (PID: {project['project_pid']})"
    print(f"REDCap Project: {title}")
    if project["snapshot_date"]:
        print(f"Snapshot: {project['snapshot_date']}")
    print(f"Source: {project['source_format'].upper()}")
    print(f"{'='*70}")

    # Project overview
    print(f"\nProject type: {project['project_type']}")
    print(f"Total fields: {stats['total_fields']} across {stats['instrument_count']} instrument(s)")

    if project["is_longitudinal"]:
        print("Longitudinal: Yes")
        if project["events"]:
            print(f"Events: {len(project['events'])}")

    if stats["survey_count"]:
        print(f"Surveys: {stats['survey_count']} instrument(s) enabled as survey")
    if stats["repeating_count"]:
        print(f"Repeating: {stats['repeating_count']} instrument(s) use [current-instance]")

    # Field type overview
    print(f"\n── Field Types ──")
    for ft, cnt in sorted(stats["field_type_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {ft:<15} {cnt}")

    # Events (longitudinal only)
    if project["events"]:
        print(f"\n── Events ({len(project['events'])}) ──")
        for ev in project["events"]:
            rep = "  [repeating event]" if ev.get("is_repeating") else ""
            print(f"  {ev['display_name']} → {ev['unique_event_name']}{rep}")
        print("  (Use unique_event_name in expressions like [event_name][field_name])")

    # Per-instrument summaries
    print(f"\n── Instruments ──")
    for instr in instruments:
        tags = []
        if instr["is_survey"]:    tags.append("survey")
        if instr["is_repeating"]: tags.append("repeating")
        if instr["events"]:       tags.append(f"events: {', '.join(instr['events'])}")
        tag_str = f"  [{', '.join(tags)}]" if tags else ""
        fields = instr["fields"]
        ft_local = Counter(f["type"] for f in fields)
        bl_local  = sum(1 for f in fields if f["branching_logic"])
        calc_local = ft_local.get("calc", 0)

        print(f"\n  {instr['display_name']} ({instr['form_name']})"
              f"  —  {len(fields)} fields{tag_str}")
        print(f"    Field types: " +
              ", ".join(f"{ft}:{cnt}" for ft, cnt in sorted(ft_local.items(), key=lambda x: -x[1])))
        if bl_local:
            print(f"    Branching logic on {bl_local} field(s)")
        if calc_local:
            print(f"    Calculated fields: {calc_local}")

        # Highlight key fields (identifiers, required, notable types)
        ids       = [f for f in fields if f["identifier"]]
        required  = [f for f in fields if f["required"]]
        calcs     = [f for f in fields if f["type"] == "calc"]
        tagged    = [f for f in fields if f["action_tags"]]

        if ids:
            print(f"    Identifiers: {', '.join(f['variable'] for f in ids)}")
        if required:
            preview = [f["variable"] for f in required[:8]]
            more    = len(required) - 8
            print(f"    Required ({len(required)}): {', '.join(preview)}"
                  + (f" … +{more} more" if more > 0 else ""))
        if calcs:
            print(f"    Calc fields: {', '.join(f['variable'] for f in calcs)}")
        if tagged:
            tag_types = Counter(t for f in tagged for t in f["action_tags"])
            top_tags = [f"{t}×{c}" for t, c in tag_types.most_common(5)]
            print(f"    Action tags: {', '.join(top_tags)}")

        # Sample a few field labels to give a sense of content
        data_fields = [f for f in fields if f["type"] not in ("descriptive",) and f["label"]]
        sample = data_fields[:5]
        if sample:
            print(f"    Sample questions:")
            for f in sample:
                print(f"      • [{f['variable']}] {f['label'][:80]}")

    # Warnings
    warnings = _collect_warnings(project)
    if warnings:
        print(f"\n── ⚠  Warnings ({len(warnings)}) ──")
        for w in warnings:
            print(f"  ⚠  {w}")

    if project["source_format"] == "csv":
        print(
            f"\n  Note: This analysis is based on the Data Dictionary CSV. "
            f"Longitudinal event names, repeating instrument configuration, and "
            f"event-instrument assignments are not available in this format — "
            f"use the Codebook PDF for those."
        )

    print()


# ── Output: --llm-context ─────────────────────────────────────────────────────

def print_llm_context(project: dict) -> None:
    """
    Compact, token-efficient dump of the entire project for LLM consumption.
    Encodes all instruments, fields, labels, choices, and branching logic
    in a dense but readable structured format.
    """
    stats = compute_stats(project)

    # ── Header block ──────────────────────────────────────────────────────────
    print(f"=== REDCap Project Context ===")
    title = project["project_title"]
    if project["project_pid"]:
        title += f" | PID: {project['project_pid']}"
    if project["snapshot_date"]:
        title += f" | Snapshot: {project['snapshot_date']}"
    print(title)
    print(f"Type: {project['project_type']}")
    print(f"Fields: {stats['total_fields']} | Instruments: {stats['instrument_count']} | "
          f"Longitudinal: {'YES' if project['is_longitudinal'] else 'no'}")

    ft_line = " | ".join(f"{ft}:{cnt}" for ft, cnt in
                         sorted(stats["field_type_distribution"].items(), key=lambda x: -x[1]))
    print(f"FieldTypes: {ft_line}")

    flags = []
    if stats["branching_logic_count"]: flags.append(f"BL:{stats['branching_logic_count']}")
    if stats["calc_count"]:            flags.append(f"Calc:{stats['calc_count']}")
    if stats["identifier_count"]:      flags.append(f"Identifiers:{stats['identifier_count']}")
    if stats["required_count"]:        flags.append(f"Required:{stats['required_count']}")
    if stats["survey_count"]:          flags.append(f"Surveys:{stats['survey_count']}")
    if stats["repeating_count"]:       flags.append(f"Repeating:{stats['repeating_count']}")
    if flags:
        print(f"Flags: {' | '.join(flags)}")

    if project["source_format"] == "csv":
        print("Note: CSV source — event table and repeating config not included. Use Codebook PDF for full context.")

    # ── Events block (longitudinal only) ──────────────────────────────────────
    if project["events"]:
        print(f"\n--- EVENTS ({len(project['events'])}) ---")
        for ev in project["events"]:
            rep = " [REPEATING]" if ev.get("is_repeating") else ""
            print(f"  {ev['display_name']} → {ev['unique_event_name']}{rep}")

    # ── Instruments index ─────────────────────────────────────────────────────
    print(f"\n--- INSTRUMENTS ---")
    for i, instr in enumerate(project["instruments"], 1):
        tags = []
        if instr["is_survey"]:    tags.append("survey")
        if instr["is_repeating"]: tags.append("repeating")
        if instr["events"]:       tags.append("events:" + ",".join(instr["events"]))
        tag_str = f" [{', '.join(tags)}]" if tags else ""
        print(f"  {i}. {instr['display_name']} ({instr['form_name']}) — {len(instr['fields'])} fields{tag_str}")

    # ── Per-instrument field listings ─────────────────────────────────────────
    print(f"\n--- FIELDS ---")
    for instr in project["instruments"]:
        tags = []
        if instr["is_survey"]:    tags.append("SURVEY")
        if instr["is_repeating"]: tags.append("REPEATING")
        tag_str = f" [{', '.join(tags)}]" if tags else ""
        print(f"\n=== {instr['display_name']} ({instr['form_name']}){tag_str} ===")

        if instr["events"]:
            print(f"  [Events: {', '.join(instr['events'])}]")

        for f in instr["fields"]:
            _print_llm_field(f)

    # ── Warnings ──────────────────────────────────────────────────────────────
    warnings = _collect_warnings(project)
    if warnings:
        print(f"\n--- WARNINGS ({len(warnings)}) ---")
        for w in warnings:
            print(f"  ! {w}")

    print()


def _print_llm_field(f: dict) -> None:
    """Print one field entry in the compact LLM-context format."""
    # Optional section header
    if f.get("section_header"):
        print(f"  [SECTION: {f['section_header']}]")

    # Build field header line
    num = f"#{f['number']} " if f["number"] else ""
    var = f["variable"]
    ftype = f["type"]

    # Type + validation
    if f["validation"]:
        type_str = f"{ftype}/{f['validation']}"
        if f["validation_min"] or f["validation_max"]:
            rng = f"{f['validation_min'] or '?'}-{f['validation_max'] or '?'}"
            type_str += f" [{rng}]"
    else:
        type_str = ftype

    # Flags
    flag_parts = []
    if f["required"]:   flag_parts.append("required")
    if f["identifier"]: flag_parts.append("identifier")
    flag_str = ", ".join(flag_parts)

    # Label (truncated if very long)
    label = f["label"][:100] + ("…" if len(f["label"]) > 100 else "")

    # Conditional prefix
    bl_prefix = "[if] " if f["branching_logic"] else ""

    line = f"  {bl_prefix}{num}{var} | {type_str} | {label!r}"
    if flag_str:
        line += f" | {flag_str}"
    print(line)

    # Choices
    if f["choices"]:
        print(f"    → {fmt_choices(f['choices'])}")

    # Calculation formula
    if f["formula"]:
        formula_preview = f["formula"][:150] + ("…" if len(f["formula"]) > 150 else "")
        print(f"    calc: {formula_preview}")

    # Branching logic
    if f["branching_logic"]:
        print(f"    BL: {abbreviate_bl(f['branching_logic'])}")

    # Action tags
    if f["action_tags"]:
        print(f"    @: {' '.join(f['action_tags'])}")

    # Field note (short)
    if f.get("field_note"):
        note_preview = f["field_note"][:80] + ("…" if len(f["field_note"]) > 80 else "")
        print(f"    note: {note_preview}")


# ── Warnings ──────────────────────────────────────────────────────────────────

def _collect_warnings(project: dict) -> list:
    """Collect design warnings across all instruments."""
    warnings = []
    for instr in project["instruments"]:
        for f in instr["fields"]:
            if f["type"] == "checkbox" and f["required"]:
                warnings.append(
                    f"[{f['variable']}] is a checkbox marked required — "
                    f"REDCap cannot enforce 'at least one selected'. The required flag is silently ignored."
                )
            if f["type"] in CHOICE_TYPES and not f["choices"] and project["source_format"] == "csv":
                warnings.append(
                    f"[{f['variable']}] is type '{f['type']}' but has no choices defined."
                )
            if f["type"] == "calc" and not f["formula"] and project["source_format"] == "csv":
                warnings.append(
                    f"[{f['variable']}] is type 'calc' but has no formula."
                )
    return warnings


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    path = sys.argv[1]
    mode = "llm-context" if "--llm-context" in sys.argv else "summary"

    ext = Path(path).suffix.lower()

    try:
        if ext == ".pdf":
            project = parse_pdf(path)
        elif ext == ".csv":
            project = parse_csv(path)
        else:
            # Try CSV first, then PDF
            try:
                project = parse_csv(path)
            except Exception:
                project = parse_pdf(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if mode == "llm-context":
        print_llm_context(project)
    else:
        print_summary(project)


if __name__ == "__main__":
    main()

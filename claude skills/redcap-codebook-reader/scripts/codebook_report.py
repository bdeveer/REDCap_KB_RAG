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
            # Normalize: strip HTML tags, then collapse whitespace runs (incl. \n → space)
            f["label"] = re.sub(r"\s+", " ", strip_html(raw_label)).strip()
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

def _normalize_fi_ligature(text: str) -> str:
    """
    Fix ligature encoding issues common in REDCap codebook PDFs:
      - fi ligature → '!'  (e.g., "!eld" = "field", "Con!rm" = "Confirm")
      - ff ligature → '#'  (e.g., "O#ce" = "Office")
      - ffi ligature → '"' (e.g., "su"cient" = "sufficient")

    Strategy: replace '!' with 'fi' whenever it is adjacent to a letter
    (either preceded or followed by one). This is safe in codebook context
    because legitimate '!' characters don't appear next to word characters.
    Same logic for '#' → 'ff' and '"' → 'ffi' adjacent to letters.
    """
    # fi ligature: ! adjacent to a letter → fi
    text = re.sub(r"(?<=[A-Za-z])!|!(?=[A-Za-z])", "fi", text)
    # ff ligature: # after a letter → ff  (handles word-final "off" = "o#" and mid-word)
    # Left-only lookbehind: won't match "# items" (space before #) or "#3" (digit before #)
    text = re.sub(r"(?<=[A-Za-z])#", "ff", text)
    # ffi ligature: " between letters → ffi
    text = re.sub(r'(?<=[A-Za-z])"(?=[A-Za-z])', "ffi", text)
    return text


def parse_pdf(path: str) -> dict:
    """
    Parse a REDCap Codebook PDF (the "Download PDF of All Instruments" export).
    Extracts project header, instruments summary table, events table (longitudinal),
    and the per-field table.

    Requires pdfplumber:
        pip install pdfplumber --break-system-packages

    PDF table column layout (confirmed from REDCap codebook PDFs):
      Col 0: empty/blank
      Col 1: instrument banner text OR empty
      Col 2: field number OR empty
      Col 3: [variable_name] (+ optional BL after newline) OR empty
      Col 4: field label (+ optional section header prefix)
      Col 5: field attributes (type, choices, action tags, etc.)
      Col 6+: empty/overflow columns
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
        # ── First page text for header ────────────────────────────────────────
        first_text = pdf.pages[0].extract_text(x_tolerance=3, y_tolerance=3) or "" if pdf.pages else ""
        project["project_title"] = _pdf_title(first_text)
        project["project_pid"]   = _pdf_pid(first_text)
        project["snapshot_date"] = _pdf_date(first_text)

        # ── Collect all tables from all pages ─────────────────────────────────
        all_tables: list = []
        for page in pdf.pages:
            tables = page.extract_tables() or []
            all_tables.extend(tables)

        # ── Parse the instruments/events summary and events tables ─────────────
        _pdf_parse_summary_tables(project, all_tables)

        # ── Parse the main field-by-field table ────────────────────────────────
        _pdf_parse_field_tables(project, all_tables)

    # Classify project
    form_names  = [i["form_name"] for i in project["instruments"]]
    all_labels  = [f["label"] for i in project["instruments"] for f in i["fields"]]
    project["project_type"] = classify_project_type(form_names, all_labels)

    return project


def _pdf_title(text: str) -> str:
    m = re.search(r"Data Dictionary Codebook\s*\n(.+?)(?:\s*\(PID:|$)", text)
    if m:
        return m.group(1).strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for i, line in enumerate(lines):
        if "Codebook" in line and i + 1 < len(lines):
            cand = lines[i + 1]
            if "Data Dictionary" not in cand:
                return cand
    return "Unknown Project"


def _pdf_pid(text: str) -> str | None:
    m = re.search(r"PID:\s*(\d+)", text)
    return m.group(1) if m else None


def _pdf_date(text: str) -> str | None:
    m = re.search(r"(\d{2}-\d{2}-\d{4}\s+\d+:\d+(?:am|pm))", text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def _pdf_parse_summary_tables(project: dict, all_tables: list) -> None:
    """
    Parse the Instruments summary table and the Events table (longitudinal projects).

    Instruments table: 2-column, header row "Instrument | Form Name"
    Events table: 3+ column, header row contains "Unique event name" or "Event ID"
    """
    for table in all_tables:
        if not table or len(table) < 2:
            continue

        # Look at second row (first is often a merged mega-cell or title row)
        header_row = next(
            (r for r in table[:3] if r and any(str(c or "").strip() for c in r)),
            None
        )
        if not header_row:
            continue
        header = [str(c or "").strip().lower() for c in header_row]

        # Events table: contains "unique event" in a column header
        if any("unique event" in h for h in header):
            project["is_longitudinal"] = True
            for row in table:
                cells = [str(c or "").strip() for c in row]
                if not any(cells):
                    continue
                if "unique event" in " ".join(cells).lower():
                    continue  # skip header row
                ev = {
                    "display_name":      cells[0] if len(cells) > 0 else "",
                    "unique_event_name": cells[1] if len(cells) > 1 else "",
                    "event_id":          cells[2] if len(cells) > 2 else None,
                    "is_repeating":      any("repeat" in str(c).lower() for c in cells),
                }
                if ev["unique_event_name"] and ev["unique_event_name"] != "Unique event name":
                    project["events"].append(ev)

        # Instruments summary table: 2-column with "Instrument" header
        elif len(header) == 2 and ("instrument" in header[0] or "form name" in header[1]):
            # We don't need to pre-populate instruments here — field parsing handles it.
            # But we capture event assignments if col 2 exists.
            pass


def _pdf_parse_field_tables(project: dict, all_tables: list) -> None:
    """
    Parse the main field-by-field table from codebook PDF tables.

    Confirmed column layout:
      [0]: empty  [1]: instrument banner or ''  [2]: field #  [3]: [variable]+BL
      [4]: label  [5]: attributes  [6+]: empty

    Skips: mega-cell first rows, column header rows, continuation rows.

    Handles cross-table continuations: when a page break splits a field row
    across two tables (e.g., "ONLY" split as "ONL" in table T and "Y if:\n..."
    in the next table), the pending field is completed when the continuation
    row is detected.
    """
    current_instr: dict | None = None
    pending_field: dict | None = None   # field with BL truncated at "ONL" — waiting for "Y if:..." continuation
    last_field: dict | None = None      # most recently completed field (for full-BL standalone rows)

    for table in all_tables:
        if not table:
            continue

        for row_idx, row in enumerate(table):
            if not row:
                continue

            # Normalize ALL cells: apply fi/ff/ffi-ligature fix and pad to 6 cells
            cells = [_normalize_fi_ligature(str(c or "").strip()) for c in row]
            while len(cells) < 6:
                cells.append("")

            # ── Skip mega-cell first row (contains all page text as one blob) ─
            if row_idx == 0 and len(cells[0]) > 100:
                continue

            # ── Skip column header row ─────────────────────────────────────────
            if cells[2].strip() == "#" or "variable / field" in cells[3].lower():
                continue

            # ── Instrument banner ──────────────────────────────────────────────
            # Must be checked BEFORE the continuation-row skip below.
            # Pattern: col 1 has "Instrument: Name (form_name) ..."
            #          col 2 is empty (not a field number)
            if "Instrument:" in cells[1] and not re.match(r"^\d+$", cells[2].strip()):
                banner = cells[1]
                m = re.search(
                    r"Instrument:\s+(.+?)\s*\(([a-z][a-z0-9_]*)\)",
                    banner
                )
                if m:
                    display_nm = m.group(1).strip()
                    form_nm    = m.group(2).strip()
                else:
                    # Fallback: strip "Instrument:" prefix and rendering artifacts
                    display_nm = re.sub(r"Instrument:\s*", "", banner)
                    display_nm = re.sub(r"\(cid:\d+\).*", "", display_nm).strip()
                    form_nm    = display_nm.lower().replace(" ", "_")

                is_surv = "Enabled as survey" in banner or "(cid:0)" in banner
                current_instr = new_instrument(display_nm, form_nm)
                current_instr["is_survey"] = is_surv
                project["instruments"].append(current_instr)
                pending_field = None  # clear pending on instrument change
                continue

            # ── Cross-table BL continuation — two forms ────────────────────────
            # Page breaks can split a field row's BL across tables. Two forms:
            #
            # Form 1 ("Y if:…"): field row ends at "ONL", next row starts "Y if:\n[expr]"
            #   → pending_field holds the incomplete field
            #
            # Form 2 ("Show the field ONLY if:…"): entire BL appears as a standalone
            #   row (no field number) after choice-overflow tables separated the two
            #   → last_field receives the BL
            #
            # Both forms have empty col[2]. Check BEFORE the generic continuation skip.
            if not cells[2]:
                c3_norm = re.sub(r"([A-Za-z])\n([A-Za-z])", r"\1\2", cells[3])

                # Form 1: tail starting with "Y if:"
                if pending_field is not None and re.match(r"^Y if:\s*", c3_norm, re.IGNORECASE):
                    bl_tail = re.sub(r"^Y if:\s*\n?", "", c3_norm, flags=re.IGNORECASE).strip()
                    pending_field["branching_logic"] = bl_tail or None
                    if cells[4]:
                        tail = cells[4].replace("\n", " ").strip()
                        pending_field["label"] = (pending_field["label"] + " " + tail).strip()
                    pending_field = None
                    continue

                # Form 2: full BL text in a standalone row (e.g., after choice tables)
                bl_full_m = re.search(
                    r"Show the (?:field) ONLY if:\n(.+)",
                    c3_norm,
                    re.DOTALL | re.IGNORECASE,
                )
                if bl_full_m and last_field is not None and last_field["branching_logic"] is None:
                    last_field["branching_logic"] = bl_full_m.group(1).strip() or None
                    continue

            # Reset pending_field only when we hit a new proper field row (digit in col 2).
            # Do NOT reset on choice/summary tables whose col[2] contains non-digit text.
            if pending_field is not None and re.match(r"^\d+$", cells[2].strip()):
                pending_field = None

            # ── Skip continuation rows (empty col 2 AND no bracket in col 3) ──
            # These are choice overflow rows like ['', '', '', '', '', '0', 'Incomplete', ...]
            # Choices are already embedded in col 5 of their own field row — skip duplicates.
            if not cells[2] and not re.match(r"^\[", cells[3]):
                continue

            # ── Field row ──────────────────────────────────────────────────────
            # Col 2 is a digit, col 3 starts with [variable_name].
            # PDF line-wrapping can embed \n inside variable names (e.g., [email_pre\nview_complete]).
            # Normalize mid-word breaks in col 3 FIRST, then match the variable name.
            num_match  = re.match(r"^\d+$", cells[2].strip())
            var_cell_raw  = cells[3]
            var_cell_norm = re.sub(r"([A-Za-z])\n([A-Za-z])", r"\1\2", var_cell_raw)
            var_m = re.match(r"^\[([a-z][a-z0-9_]*)\]", var_cell_norm.strip())

            if num_match and var_m:
                if current_instr is None:
                    current_instr = new_instrument("Unknown Instrument", "unknown")
                    project["instruments"].append(current_instr)

                f = new_field()
                f["number"] = int(cells[2].strip())
                f["variable"] = var_m.group(1)

                # Skip auto-generated instrument completion status fields
                # (_complete fields are uniform across all projects, not user-designed)
                if f["variable"].endswith("_complete"):
                    continue

                # Extract branching logic from col 3 if present after the variable name.
                bl_split = re.split(
                    r"\nShow the (?:field|!eld) ONLY if:\n",
                    var_cell_norm,
                    maxsplit=1,
                    flags=re.IGNORECASE,
                )
                if len(bl_split) > 1:
                    f["branching_logic"] = bl_split[1].strip() or None
                elif re.search(r"Show the (?:field|!eld) ONL$", var_cell_norm, re.IGNORECASE):
                    # BL was truncated at the table/page boundary — mark as pending
                    pending_field = f

                # ── Parse label from col 4 ─────────────────────────────────────
                label_cell = cells[4]
                if label_cell.startswith("Section Header:"):
                    parts = label_cell.split("\n", 1)
                    f["section_header"] = parts[0].replace("Section Header:", "").strip()
                    raw_label = parts[1].strip() if len(parts) > 1 else ""
                else:
                    raw_label = label_cell
                # Normalize PDF line-wrapping artifacts in labels
                f["label"] = raw_label.replace("\n", " ").strip()

                # ── Parse attributes from col 5 ────────────────────────────────
                _parse_pdf_attributes(f, cells[5])

                current_instr["fields"].append(f)
                last_field = f


def _parse_pdf_attributes(f: dict, attr_text: str) -> None:
    """
    Parse the Field Attributes column from the codebook PDF.

    Format of attr_text (col 5):
      Line 0: type info — "text", "text (email), Required", "dropdown, Required", etc.
      Line 1+: choices ("1 Label\n2 Label"), annotation, custom alignment, slider labels, etc.

    Choices embedded as "N Label" lines after a dropdown/radio/checkbox type line.
    Annotation line: "Field Annotation: @TAG..." (may be multiline for long expressions).
    """
    if not attr_text:
        return

    lines = attr_text.splitlines()
    if not lines:
        return

    # ── Line 0: type, optional validation, Required/Identifier flags ───────────
    type_line = lines[0].strip()

    # Field type — match known types at the start of the line
    type_m = re.match(
        r"^(text|notes|dropdown|radio|checkbox|calc|file|descriptive|slider|yesno|truefalse|sql)",
        type_line.lower()
    )
    if type_m:
        f["type"] = type_m.group(1)

    # Validation: "text (date_mdy)", "text (email)", etc. (not for slider parenthetical)
    if f["type"] == "text":
        val_m = re.search(r"\(([a-z_]+(?:_[a-z]+)*)\)", type_line)
        if val_m:
            f["validation"] = val_m.group(1).strip()

    # Required / Identifier from type line
    f["required"]   = "Required" in type_line
    f["identifier"] = "Identifier" in type_line

    # ── Remaining lines: choices, annotation, alignment, BL ───────────────────
    in_annotation = False
    annotation_parts: list = []
    last_choice_idx = -1  # index of the last appended choice (for multiline labels)

    for line in lines[1:]:
        line_s = line.strip()
        if not line_s:
            in_annotation = False
            continue

        # Required / Identifier as standalone lines
        if line_s in ("Required", "Identifier"):
            if line_s == "Required":   f["required"]   = True
            if line_s == "Identifier": f["identifier"] = True
            in_annotation = False
            last_choice_idx = -1
            continue

        # Field Annotation trigger line
        if line_s.startswith("Field Annotation:"):
            in_annotation = True
            last_choice_idx = -1
            ann_text = line_s.replace("Field Annotation:", "").strip()
            annotation_parts.append(ann_text)
            continue

        # Annotation continuation lines: @ tag start, quoted strings, or anything
        # that isn't a new choice/custom alignment/slider (covers split tags like
        # "@HIDESUBMIT-\nSURVEY" where "SURVEY" appears alone on the next line).
        if in_annotation and (
            line_s.startswith("@")
            or line_s.startswith('"')
            or line_s.startswith("'")
            or (
                not re.match(r"^\d+\s", line_s)
                and not line_s.startswith("Custom")
                and not line_s.startswith("Slider")
                and line_s not in ("Required", "Identifier")
            )
        ):
            annotation_parts.append(line_s)
            continue

        in_annotation = False

        # Custom alignment — skip
        if line_s.startswith("Custom alignment:"):
            last_choice_idx = -1
            continue

        # Slider labels — skip
        if line_s.startswith("Slider labels:"):
            last_choice_idx = -1
            continue

        # Branching logic within attributes (rare — usually in col 3, but occasionally here)
        if "Show the field ONLY if:" in line_s or "Show the !eld ONLY if:" in line_s:
            last_choice_idx = -1
            continue  # BL from col 3 takes precedence; skip if somehow duplicated here

        # Choice line: "N Label text" where N is a digit
        choice_m = re.match(r"^(\d+)\s+(.+)$", line_s)
        if choice_m and f["type"] in CHOICE_TYPES:
            val = choice_m.group(1)
            lbl = choice_m.group(2).strip()
            # Skip _complete field choices (Incomplete/Unverified/Complete)
            if not (val in ("0", "1", "2") and lbl in ("Incomplete", "Unverified", "Complete")):
                # REDCap codebook PDF shows checkbox choices prefixed with
                # the subvariable name: "fieldname___code Actual Label".
                # Strip that prefix so only the human-readable label is kept.
                if f["type"] == "checkbox":
                    subvar_prefix = re.match(
                        r"^[a-z][a-z0-9_]*___\d+\s+(.+)$",
                        lbl,
                        re.IGNORECASE
                    )
                    if subvar_prefix:
                        lbl = subvar_prefix.group(1).strip()
                f["choices"].append({"value": val, "label": lbl})
                last_choice_idx = len(f["choices"]) - 1
            continue

        # Multiline choice label continuation: PDF sometimes wraps long choice labels
        # across lines (e.g., "Keyboard/Mouse\nWireless Combo" for one choice).
        # If we're in a choice field and this line doesn't match anything else,
        # append it to the most recent choice's label.
        if last_choice_idx >= 0 and f["type"] in CHOICE_TYPES:
            f["choices"][last_choice_idx]["label"] += " " + line_s
            continue

        last_choice_idx = -1

        # Calculation formula line (calc fields sometimes have the formula here)
        if f["type"] == "calc" and not f["formula"]:
            f["formula"] = line_s

    # Commit collected action tags.
    # Repair hyphenated tags split across lines (e.g., "@HIDESUBMIT- SURVEY" → "@HIDESUBMIT-SURVEY")
    if annotation_parts:
        full_ann = " ".join(annotation_parts)
        full_ann = re.sub(r"(@[A-Z][A-Z0-9_-]*-)\s+([A-Z])", r"\1\2", full_ann)
        f["action_tags"] = extract_action_tags(full_ann)


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

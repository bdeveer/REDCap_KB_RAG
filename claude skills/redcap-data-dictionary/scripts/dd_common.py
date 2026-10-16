#!/usr/bin/env python3
"""
Shared REDCap Data Dictionary helpers.

Single implementation used by:
    redcap-data-dictionary/scripts/parse_dd.py
    redcap-dd-builder/scripts/build_dd.py
    redcap-dd-fixer/scripts/fix_dd.py

Provides:
    - The 18 Data Dictionary columns, display and API names, in RC-FD-08 §4.2 order
    - Header detection / mapping: rows are always keyed by DISPLAY names; the
      input's header style ("display" or "api") is remembered so writers can
      write back the same style
    - read_dd(path): CSV (UTF-8 with/without BOM, then cp1252, then latin-1) or
      JSON metadata as returned by the API / a REDCap connector's export_metadata
    - write_dd(path, rows, header_style)
    - parse_choices, VALID_FIELD_TYPES, validation type sets
"""

from __future__ import annotations


import csv
import io
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

# REDCap descriptive fields can hold large HTML blobs that exceed the csv
# module's 128 KB default field limit. sys.maxsize overflows on some builds.
_limit = sys.maxsize
while True:
    try:
        csv.field_size_limit(_limit)
        break
    except OverflowError:
        _limit //= 10


# ── Columns (RC-FD-08 §4.2, columns A–R) ──────────────────────────────────────

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

# Display headers, as in a Data Dictionary downloaded from the REDCap UI
COLUMNS = [
    COL_VARIABLE, COL_FORM, COL_SECTION, COL_FIELD_TYPE, COL_LABEL,
    COL_CHOICES, COL_NOTE, COL_VALIDATION, COL_VAL_MIN, COL_VAL_MAX,
    COL_IDENTIFIER, COL_BRANCHING, COL_REQUIRED, COL_ALIGNMENT,
    COL_QUESTION_NUM, COL_MATRIX_GROUP, COL_MATRIX_RANK, COL_ANNOTATION,
]

# The same 18 columns as named by the API metadata export (RC-API-07), same order
API_COLUMNS = [
    "field_name", "form_name", "section_header", "field_type", "field_label",
    "select_choices_or_calculations", "field_note",
    "text_validation_type_or_show_slider_number",
    "text_validation_min", "text_validation_max",
    "identifier", "branching_logic", "required_field", "custom_alignment",
    "question_number", "matrix_group_name", "matrix_ranking", "field_annotation",
]

API_TO_DISPLAY = dict(zip(API_COLUMNS, COLUMNS))
DISPLAY_TO_API = dict(zip(COLUMNS, API_COLUMNS))

HEADER_DISPLAY = "display"
HEADER_API = "api"

# Case-insensitive lookup: any known header (either style) → display name
_HEADER_LOOKUP = {name.lower(): name for name in COLUMNS}
_HEADER_LOOKUP.update({api: disp for api, disp in API_TO_DISPLAY.items()})


# ── Reference data ────────────────────────────────────────────────────────────

# RC-FD-08 §5.4. 'sql' is admin-only (RC-FD-12) but valid in an existing DD.
VALID_FIELD_TYPES = {
    "text", "notes", "dropdown", "radio", "checkbox",
    "calc", "file", "descriptive", "slider", "yesno",
    "truefalse", "sql",
}

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}
MATRIX_TYPES = {"radio", "checkbox"}

# Column H codes (RC-FD-08 §5.7). Not exhaustive: sites can enable extra types.
TEXT_VALIDATION_TYPES = {
    "date_ymd", "date_mdy", "date_dmy",
    "datetime_ymd", "datetime_mdy", "datetime_dmy",
    "datetime_seconds_ymd", "datetime_seconds_mdy", "datetime_seconds_dmy",
    "number", "number_1dp", "number_2dp", "number_3dp", "number_4dp",
    "integer", "email", "phone", "phone_australia",
    "zipcode", "mrn_10d", "mrn_generic", "url",
    "alpha_only", "postalcode_canada", "ssn", "time",
}
# Used on "file" fields: signature = classic drawn signature,
# enhanced_signature = typed-or-drawn variant (17.1.0+)
FILE_VALIDATION_TYPES = {"signature", "enhanced_signature"}
# On sliders, 'number' shows the value next to the handle
SLIDER_VALIDATION_TYPES = {"number"}
VALIDATION_TYPES = TEXT_VALIDATION_TYPES | FILE_VALIDATION_TYPES | SLIDER_VALIDATION_TYPES

# Column N codes (RC-FD-08 §5.12) — any other value fails the upload
VALID_ALIGNMENTS = {"LH", "LV", "RH", "RV"}

VALID_VARIABLE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
MAX_VARIABLE_LENGTH = 26   # recommended maximum (RC-FD-08 §5.1)


# ── Headers ───────────────────────────────────────────────────────────────────

def canonical_header(name: str) -> str:
    """Map a raw header (display or API style, any case, stray BOM/space) to its
    display name. Unknown headers are returned stripped but otherwise unchanged."""
    stripped = (name or "").replace("﻿", "").strip()
    return _HEADER_LOOKUP.get(stripped.lower(), stripped)


def detect_header_style(headers) -> str | None:
    """Return "display", "api", or None if no Variable / Field Name column."""
    cleaned = [(h or "").replace("﻿", "").strip().lower() for h in headers]
    if COL_VARIABLE.lower() in cleaned:
        return HEADER_DISPLAY
    if "field_name" in cleaned:
        return HEADER_API
    return None


# ── Reading ───────────────────────────────────────────────────────────────────

class DDRead(NamedTuple):
    rows: list            # dicts keyed by display names; extra cells under key None
    header_style: str     # "display" or "api"
    warnings: list        # human-readable notes about how the file was read
    columns: list         # display names in the file's column order (incl. unknown)


_ENCODINGS = ("utf-8-sig", "cp1252", "latin-1")   # utf-8-sig also reads BOM-less UTF-8


def read_dd(path, strict: bool = False) -> DDRead:
    """
    Read a Data Dictionary: a CSV with display or API headers, or JSON metadata
    (a list of field objects with API keys, as returned by the API / a REDCap
    connector's export_metadata).

    strict=True rejects files with unrecognised columns (used before writing a
    merged DD). Raises FileNotFoundError or ValueError.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    raw = path.read_bytes()
    text = None
    warnings = []
    for encoding in _ENCODINGS:
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None:   # unreachable: latin-1 decodes anything
        raise ValueError(f"Could not decode {path}.")
    if encoding != "utf-8-sig":
        warnings.append(
            f"{path.name} is not UTF-8; read it as {encoding}. Check accented/special "
            "characters, and re-save the file as 'CSV UTF-8' if they look wrong."
        )

    if path.suffix.lower() == ".json" or text.lstrip()[:1] in ("[", "{"):
        rows, style, columns = _rows_from_json(text, path)
    else:
        rows, style, columns = _rows_from_csv(text, path)

    unknown = [c for c in columns if c not in COLUMNS]
    if unknown:
        msg = f"Unrecognised column(s) in {path.name}: {', '.join(repr(c) for c in unknown)}"
        if strict:
            raise ValueError(
                msg + ". Expected the 18 REDCap display headers (\"Variable / Field Name\", "
                "\"Form Name\", ...) or the API-style headers (field_name, form_name, ...)."
            )
        warnings.append(msg + " — kept as-is.")
    if strict and COL_FORM not in columns:
        raise ValueError(f"{path.name} has no 'Form Name' (or 'form_name') column.")

    return DDRead(rows, style, warnings, columns)


def _rows_from_csv(text: str, path: Path):
    reader = csv.DictReader(io.StringIO(text, newline=""))
    fieldnames = reader.fieldnames or []
    style = detect_header_style(fieldnames)
    if style is None:
        raise ValueError(
            f"{path} has no '{COL_VARIABLE}' (or 'field_name') column — "
            "is this a REDCap Data Dictionary?"
        )
    to_display = {f: canonical_header(f) for f in fieldnames}
    rows = []
    for raw_row in reader:
        row = {}
        for key, value in raw_row.items():
            if key is None:          # extra cells beyond the header row
                row[None] = value
            else:
                row[to_display[key]] = "" if value is None else value
        rows.append(row)
    return rows, style, [to_display[f] for f in fieldnames]


def _rows_from_json(text: str, path: Path):
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"{path} is not valid JSON: {e}") from None
    if isinstance(data, dict):
        # Accept a wrapper object such as {"metadata": [...]} or {"data": [...]}
        lists = [v for v in data.values() if isinstance(v, list)]
        data = lists[0] if len(lists) == 1 else data.get("metadata", data.get("data"))
    if not isinstance(data, list) or not all(isinstance(r, dict) for r in data):
        raise ValueError(
            f"{path} is not REDCap metadata JSON (expected a list of field objects "
            "with keys such as field_name, form_name, field_type)."
        )
    keys = []
    for r in data:
        for k in r:
            if k not in keys:
                keys.append(k)
    style = detect_header_style(keys)
    if data and style is None:
        raise ValueError(f"{path}: metadata objects have no 'field_name' key.")
    rows = [
        {canonical_header(k): "" if v is None else str(v) for k, v in r.items()}
        for r in data
    ]
    # JSON comes from the API, but any CSV written from it is meant for the
    # Data Dictionary upload page, so write it back with display headers.
    return rows, HEADER_DISPLAY, [canonical_header(k) for k in keys]


# ── Writing ───────────────────────────────────────────────────────────────────

def write_dd(path, rows: list, header_style: str = HEADER_DISPLAY, columns=None) -> None:
    """
    Write rows (keyed by display names) as a UTF-8 CSV without BOM.
    header_style "api" writes API headers (field_name, ...), otherwise display
    headers. columns = display names to write, in order (default: the 18 columns).
    Missing cells are written blank; keys not in columns (and None) are ignored.
    """
    columns = list(columns) if columns else COLUMNS
    if header_style == HEADER_API:
        headers = [DISPLAY_TO_API.get(c, c) for c in columns]
    else:
        headers = columns
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(["" if row.get(c) is None else row.get(c) for c in columns])


# ── Column F helpers ──────────────────────────────────────────────────────────

def parse_choices(choices_str: str) -> list[dict]:
    """Parse 'raw, Label | raw, Label' into [{value, label}, ...].
    Items without a comma use the item as both value and label; empty items are skipped."""
    choices = []
    for item in (choices_str or "").split("|"):
        item = item.strip()
        if not item:
            continue
        if "," in item:
            value, label = item.split(",", 1)
            choices.append({"value": value.strip(), "label": label.strip()})
        else:
            choices.append({"value": item, "label": item})
    return choices

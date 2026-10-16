#!/usr/bin/env python3
"""
REDCap Codebook Reader (PDF only)
Reads a REDCap Codebook PDF and produces either a narrative summary or a
complete LLM-context dump of the project structure.

Usage:
    python codebook_report.py <codebook.pdf> [--summary | --llm-context]

Input:
  .pdf  -- a saved copy of the REDCap Codebook page. Open it from Project Setup
           ("Codebook" in the Design your data collection instruments section)
           or from the left-hand project menu -> Codebook, then print / save
           it as PDF. NOT "Download PDF of All Instruments" -- that is the set
           of blank data-entry forms, not the Codebook.

  Data Dictionary CSVs are not handled here. Use:
      python ~/.claude/skills/redcap-data-dictionary/scripts/parse_dd.py <csv> --text

Output modes:
  --summary      (default) Narrative prose for human reading
  --llm-context  Full structured dump for LLM consumption (no truncation)

Dependencies:
  pdfplumber:
      py -m pip install pdfplumber
"""

from __future__ import annotations

import logging
import re
import sys
from collections import Counter
from pathlib import Path

# Windows consoles default to cp1252, which cannot print the report symbols.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# pdfminer logs harmless warnings such as "Could not get FontBBox from font
# descriptor" for fonts embedded by browsers; keep stderr clean.
logging.getLogger("pdfminer").setLevel(logging.ERROR)

DD_SKILL_CMD = "python ~/.claude/skills/redcap-data-dictionary/scripts/parse_dd.py <csv> --text"
CONNECTOR_HINT = (
    "If you have API access, the REDCap connector exports (export_metadata, "
    "export_events, export_instrument_event_mappings, "
    "export_repeating_instruments_events) are more reliable than parsing a PDF."
)

# -- Reference data -----------------------------------------------------------

CHOICE_TYPES = {"dropdown", "radio", "checkbox"}

_CLINICAL_KW = [
    "consent", "eligib", "randomiz", "adverse_event", "ae_", "discharge",
    "screen", "enroll", "baseline", "follow_up", "medical_history", "vital",
    "medication", "inpatient", "outpatient", "intervention",
]
_SURVEY_KW  = ["survey", "questionnaire", "patient_reported"]
_ADMIN_KW   = ["tracker", "notification", "announcement", "admin", "migration"]

# Typographic ligature code points (U+FB00-U+FB06) -> plain letters.
_LIGATURES = {
    "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi",
    "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st",
}
_LIGATURE_RE = re.compile("[ﬀ-ﬆ]")

# Some REDCap codebook PDFs map the "fi" ligature glyph to '!' in the text
# layer. We only repair the fixed REDCap boilerplate where this is known to
# occur; user-entered text is never touched (a real '!' or '#' must survive).
_BOILERPLATE_FIXES = [
    (re.compile(r"Show the !eld ONLY if", re.IGNORECASE), "Show the field ONLY if"),
]

_FIELD_TYPES_RE = re.compile(
    r"^(text|notes|dropdown|radio|checkbox|calc|file|descriptive|slider|yesno|truefalse|sql)\b",
    re.IGNORECASE,
)


# -- Helpers ------------------------------------------------------------------

def extract_action_tags(annotation: str) -> list:
    return re.findall(r"@[A-Z][A-Z0-9_-]*", annotation)


def normalize_pdf_text(text: str) -> str:
    """Replace ligature code points and known boilerplate glyph artifacts only."""
    text = _LIGATURE_RE.sub(lambda m: _LIGATURES[m.group(0)], text)
    for pat, repl in _BOILERPLATE_FIXES:
        text = pat.sub(repl, text)
    return text


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


# Branching logic and calc formulas only accept straight quotes, so curly
# quotes there are text-layer font artifacts and are straightened.
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})
CLIP_MARK = " [...clipped...] "


def fmt_choices(choices: list) -> str:
    """Full choice string: v=Label | v=Label"""
    return " | ".join(f"{c['value']}={c['label']}" for c in choices)


# -- Data model ---------------------------------------------------------------

def new_project() -> dict:
    return {
        "project_title": "",
        "project_pid": None,
        "snapshot_date": None,
        "project_type": "Research data collection project",
        "is_longitudinal": False,
        "instruments": [],      # list of instrument dicts
        "events": [],           # list of event dicts (longitudinal only)
    }


def new_instrument(display_name: str, form_name: str) -> dict:
    return {
        "display_name": display_name,
        "form_name": form_name,
        "is_survey": False,
        # Events exactly as printed in the Codebook's Instruments table
        # (unique event names in current REDCap versions, display names in
        # some older ones).
        "events": [],
        # Repeat icon (Font Awesome glyph) next to the instrument name, and
        # the events whose entry carries the icon, if the text layer has it.
        "repeating_icon": False,
        "repeating_events": [],
        "fields": [],
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
        "annotation": None,     # full Field Annotation text, verbatim
        "action_tags": [],
        "field_note": None,
        "section_header": None,
        "custom_alignment": None,
        "question_number": None,
        "is_matrix": False,     # "(Matrix)" is printed; the group name is not
        "slider_labels": [],
        "ontology": None,       # e.g. BIOPORTAL:CTCAE
        "other_attributes": [], # attribute lines not recognised (kept, not dropped)
        "truncated": False,     # text ran past the printed page edge (clipped)
    }


# -- PDF parser ---------------------------------------------------------------
#
# The Codebook is an HTML page; users print it from the browser. The PDF text
# layer is therefore read as positioned words, not as pdfplumber "tables"
# (browser-printed pages have no ruling lines and the table detector merges or
# splits rows unpredictably). Layout of the field table (x positions come from
# its column-header row, so page size / zoom do not matter):
#
#   [#] [Variable / Field Name]  [Field Label]        [Field Attributes]
#   12  [calcsum]                Section Header: ...  calc
#       Show the field ONLY if:  Label text           Calculation: ...
#       [v1] = '1'               Field note (italic)    1 Choice label  (indented)
#
# * Instrument banners ("Instrument: Name (form_name)  Enabled as survey") sit
#   left of the variable column; an "Active languages" line follows them.
# * A field row runs from its number to the next number/banner, including
#   across page breaks.
# * Browser print header/footer lines (date, page title, page URL, "1/17") are
#   dropped. Private Use Area glyphs (REDCap's Font Awesome icons) are removed
#   from text; the repeat icon in the Instruments table is recorded.

_PUA_RE = re.compile("[-]")
_REPEAT_ICON = ""     # Font Awesome "repeat" glyph

# Browser print header/footer lines (only dropped inside the page margins,
# except the Codebook URL, which is dropped anywhere).
_BROWSER_CHROME_RES = [
    re.compile(r"https?://\S+"),
    re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4},\s"),                    # "10/9/26, 10:16 AM ..."
    re.compile(r"^(?:Page\s+)?\d+\s*(?:/|of)\s*\d+$", re.IGNORECASE),  # "1/17", "Page 1 of 17"
    re.compile(r"\|\s*REDCap\s*$"),                                 # page title
]
_MARGIN_PT = 30.0

_SHOW_IF_KEY = "showthefieldonlyif:"
_HEADER_WORDS = {"#", "Variable", "/", "Field", "Name", "Label", "Note", "Attributes", "(Field",
                 "Type,", "Validation,", "Choices,", "Calculations,", "etc.)"}

_ATTR_MARKERS = ("Field Annotation:", "Calculation:", "Custom alignment:", "Question number:",
                 "Slider labels:")

CHOICE_LIKE = CHOICE_TYPES | {"yesno", "truefalse"}


def _is_bold(font: str) -> bool:
    return "Bold" in font or "Semibold" in font or "Black" in font


def _is_italic(font: str) -> bool:
    return "Italic" in font or "Oblique" in font


def _group_lines(words: list, tol: float = 2.5) -> list:
    """Group words (sorted or not) into visual lines by vertical position."""
    lines: list = []
    for w in sorted(words, key=lambda w: (w["gy"], w["x0"])):
        if lines and w["gy"] - lines[-1][0]["gy"] <= tol:
            lines[-1].append(w)
        else:
            lines.append([w])
    return [sorted(ln, key=lambda w: w["x0"]) for ln in lines]


def _line(ws: list) -> dict:
    """A text line built from words: text, extent, and first-word char width."""
    ws = [w for w in ws if w["text"]]
    first = ws[0]
    # Words are also split where the font changes (e.g. an emoji glyph);
    # only a visible gap means there was a space.
    text = first["text"]
    for p, w in zip(ws, ws[1:]):
        text += ("" if w["x0"] - p["x1"] < 0.6 else " ") + w["text"]
    return {
        "text": text,
        "x0": first["x0"],
        "x1": max(w["x1"] for w in ws),
        "gy": first["gy"],
        "words": ws,
        "cw": (first["x1"] - first["x0"]) / max(1, len(first["text"])),
        "clipped": any(w.get("clipped") for w in ws),
    }


def _lines(words: list) -> list:
    return [_line(ln) for ln in _group_lines([w for w in words if w["text"]]) if any(w["text"] for w in ln)]


def _page_words(page, pi: int) -> tuple:
    """Words of one page with font info; browser header/footer removed.
    Returns (words, right_clip_x)."""
    raw = page.extract_words(x_tolerance=1.5, y_tolerance=2, extra_attrs=["fontname", "size"])
    words = []
    for w in raw:
        txt = w["text"]
        font = w.get("fontname", "") or ""
        icons = "".join(_PUA_RE.findall(txt)) if "Awesome" in font or _PUA_RE.fullmatch(txt) else ""
        words.append({
            "page": pi, "top": float(w["top"]), "gy": pi * 100000.0 + float(w["top"]),
            "x0": float(w["x0"]), "x1": float(w["x1"]),
            "text": normalize_pdf_text(_PUA_RE.sub("", txt)).strip(),
            "icons": icons, "font": font, "size": round(float(w.get("size") or 0), 1),
        })
    height, width = float(page.height), float(page.width)
    keep, clip = [], None
    for ln in _group_lines(words):
        text = " ".join(w["text"] for w in ln if w["text"])
        in_margin = ln[0]["top"] < _MARGIN_PT or ln[0]["top"] > height - _MARGIN_PT
        if "data_dictionary_codebook.php" in text or (
                in_margin and any(p.search(text) for p in _BROWSER_CHROME_RES)):
            clip = max(clip or 0.0, max(w["x1"] for w in ln))
            continue
        keep.extend(ln)
    if clip is None or clip < width * 0.6:
        clip = width - 24.0      # typical browser print margin
    return keep, clip


def parse_pdf(path: str) -> dict:
    """
    Parse a REDCap Codebook PDF (saved/printed copy of the Codebook page):
    project header, Instruments and Events summary tables, and the field table.
    """
    try:
        import pdfplumber
    except ImportError:
        print(
            "ERROR: pdfplumber is not installed, so the Codebook PDF cannot be read.\n"
            "Install it with:  py -m pip install pdfplumber\n"
            + CONNECTOR_HINT,
            file=sys.stderr,
        )
        sys.exit(1)

    words: list = []
    clips: dict = {}
    try:
        with pdfplumber.open(path) as pdf:
            for pi, page in enumerate(pdf.pages):
                ws, clips[pi] = _page_words(page, pi)
                words.extend(ws)
    except Exception as e:  # pdfminer raises a variety of exception types
        raise ValueError(f"Could not read PDF ({type(e).__name__}: {e})") from e

    project = new_project()
    parse_words(project, words, clips)
    return project


def parse_words(project: dict, words: list, clips: dict | None = None) -> None:
    """Fill the project model from positioned words (see _page_words)."""
    words = sorted(words, key=lambda w: (w["gy"], w["x0"]))
    headers = _find_field_headers(words)
    start_gy = headers[0]["gy"] if headers else float("inf")
    pre = [w for w in words if w["gy"] < start_gy - 8]

    _parse_header_info(project, pre)
    instr_info = _parse_summary_tables(project, pre)
    if headers:
        _parse_field_rows(project, words, headers, clips or {})

    for instr in project["instruments"]:
        info = instr_info.get(instr["form_name"])
        if info:
            instr["events"] = info["events"]
            instr["repeating_icon"] = info["repeating_icon"]
            instr["repeating_events"] = info["repeating_events"]

    form_names = [i["form_name"] for i in project["instruments"]]
    all_labels = [f["label"] for i in project["instruments"] for f in i["fields"]]
    project["project_type"] = classify_project_type(form_names, all_labels)


def _parse_header_info(project: dict, pre: list) -> None:
    first_page = min((w["page"] for w in pre), default=0)
    lines = [ln["text"] for ln in _lines([w for w in pre if w["page"] == first_page])]
    text = "\n".join(lines)
    project["project_title"] = "Unknown Project"
    for ln in lines:
        m = re.search(r"^(.*?)\s*\(PID:\s*(\d+)\)", ln)
        if m:
            project["project_title"] = m.group(1).strip() or "Unknown Project"
            project["project_pid"] = m.group(2)
            break
    m = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{4}\s+\d{1,2}:\d{2}\s*(?:am|pm)?)", text, re.IGNORECASE)
    project["snapshot_date"] = m.group(1).strip() if m else None


def _next_to(words: list, w: dict, text: str, gap: float = 6.0) -> dict | None:
    """The word `text` immediately right of w on the same line."""
    for v in words:
        if v["text"] == text and v["page"] == w["page"] and abs(v["top"] - w["top"]) < 2 \
                and 0 <= v["x0"] - w["x1"] <= gap:
            return v
    return None


def _prev_to(words: list, w: dict, text: str, gap: float = 6.0) -> dict | None:
    for v in words:
        if v["text"] == text and v["page"] == w["page"] and abs(v["top"] - w["top"]) < 2 \
                and 0 <= w["x0"] - v["x1"] <= gap:
            return v
    return None


def _find_field_headers(words: list) -> list:
    """Column-header rows of the field table ('#  Variable / Field Name  Field Label
    Field Attributes'); browsers may repeat them on every page."""
    out = []
    for w in words:
        if w["text"] != "Variable":
            continue
        near = [v for v in words if v["page"] == w["page"] and abs(v["top"] - w["top"]) < 14]
        num = next((v for v in near if v["text"] == "#" and v["x1"] <= w["x0"]), None)
        lab = next((v for v in near if v["text"] == "Label" and v["x0"] > w["x1"]), None)
        att = next((v for v in near if v["text"].startswith("Attributes") and v["x0"] > w["x1"]), None)
        if not (num and lab and att):
            continue
        lab_f = _prev_to(near, lab, "Field") or lab
        att_f = _prev_to(near, att, "Field") or att
        out.append({"page": w["page"], "top": w["top"], "gy": w["gy"],
                    "x_num": num["x0"], "x_var": w["x0"],
                    "x_label": lab_f["x0"], "x_attr": att_f["x0"]})
    return out


# -- Summary tables (Instruments / Events) ------------------------------------

def _parse_summary_tables(project: dict, pre: list) -> dict:
    """
    Parse the Instruments table (Instrument | Form Name | Events) and, for
    longitudinal projects, the Events table (Event Name | Unique event name |
    Event ID) printed beside it. Returns
    {form_name: {"events": [...], "repeating_icon": bool, "repeating_events": [...]}}.
    """
    info: dict = {}
    hdr_words = [w for w in pre if w["text"]]

    # Events table
    ev_x = None
    uniq = next((w for w in hdr_words if w["text"] == "Unique"
                 and _next_to(hdr_words, w, "event")), None)
    if uniq:
        same = [w for w in hdr_words if w["page"] == uniq["page"] and abs(w["top"] - uniq["top"]) < 2]
        name_w = max((w for w in same if w["text"] == "Event" and w["x1"] < uniq["x0"]
                      and _next_to(same, w, "Name")), key=lambda w: w["x0"], default=None)
        id_w = next((w for w in same if w["text"] == "Event" and w["x0"] > uniq["x1"]
                     and _next_to(same, w, "ID")), None)
        arm_w = next((w for w in same if w["text"].lower().startswith("arm") and w["x0"] > uniq["x1"]), None)
        ev_x = name_w["x0"] if name_w else uniq["x0"]
        project["is_longitudinal"] = True
        _parse_events_table(project, pre, uniq, ev_x, id_w, arm_w)

    # Instruments table
    form_w = next((w for w in hdr_words if w["text"] == "Form" and _next_to(hdr_words, w, "Name")
                   and _prev_to(hdr_words, w, "Instrument", gap=200)), None)
    if not form_w:
        return info
    same = [w for w in hdr_words if w["page"] == form_w["page"] and abs(w["top"] - form_w["top"]) < 2]
    inst_w = _prev_to(same, form_w, "Instrument", gap=200)
    evc_w = next((w for w in same if w["text"] == "Events" and w["x0"] > form_w["x1"]
                  and (ev_x is None or w["x0"] < ev_x - 2)), None)
    right = ev_x - 2 if (ev_x is not None and ev_x > form_w["x0"]) else float("inf")
    x_inst, x_form = inst_w["x0"], form_w["x0"]
    x_ev = evc_w["x0"] if evc_w else None

    body = [w for w in pre if w["gy"] > form_w["gy"] + 3 and w["x0"] < right and w["x0"] >= x_inst - 3]
    stop = min((w["gy"] for w in body if w["text"] and (_is_bold(w["font"]) or w["text"] == "Languages")),
               default=float("inf"))
    body = [w for w in body if w["gy"] < stop]
    anchors = [w for w in body if abs(w["x0"] - x_form) < 3 and re.fullmatch(r"[a-z][a-z0-9_]*", w["text"])]
    known_uniq = {e["unique_event_name"] for e in project["events"]}
    for k, a in enumerate(anchors):
        lo = a["gy"] - 3
        hi = anchors[k + 1]["gy"] - 3 if k + 1 < len(anchors) else float("inf")
        row = [w for w in body if lo <= w["gy"] < hi]
        name_ws = [w for w in row if w["x0"] < x_form - 2]
        rep_icon = any(_REPEAT_ICON in w["icons"] for w in name_ws)
        events, rep_events = [], []
        if x_ev is not None:
            ev_lines = _group_lines([w for w in row if w["x0"] >= x_ev - 2])
            tokens = []
            for ln in ev_lines:
                for w in ln:
                    if w["text"]:
                        tokens.append([w["text"], False])
                    elif _REPEAT_ICON in w["icons"] and tokens:
                        tokens[-1][1] = True
            if tokens and all(t in known_uniq or re.fullmatch(r"[a-z0-9][a-z0-9_]*", t) for t, _ in tokens):
                events = [t for t, _ in tokens]
                rep_events = [t for t, r in tokens if r]
            else:
                events = _split_event_cell(" ".join(t for t, _ in tokens), project["events"])
        info[a["text"]] = {"events": events, "repeating_icon": rep_icon, "repeating_events": rep_events}
    return info


def _parse_events_table(project: dict, pre: list, uniq: dict, ev_x: float,
                        id_w: dict | None, arm_w: dict | None) -> None:
    body = [w for w in pre if w["gy"] > uniq["gy"] + 3 and w["x0"] >= ev_x - 2]
    # The table ends at the next bold heading in this column (e.g. "Languages").
    stop = min((w["gy"] for w in body if w["text"] and (_is_bold(w["font"]) or w["text"] == "Languages")),
               default=float("inf"))
    body = [w for w in body if w["gy"] < stop and w["text"]]
    x_u = uniq["x0"]
    x_id = id_w["x0"] if id_w else None
    x_arm = arm_w["x0"] if arm_w else None
    anchors = [w for w in body if abs(w["x0"] - x_u) < 3 and re.fullmatch(r"[a-z0-9][a-z0-9_]*", w["text"])]
    for k, a in enumerate(anchors):
        lo = a["gy"] - 3
        hi = anchors[k + 1]["gy"] - 3 if k + 1 < len(anchors) else a["gy"] + 12
        row = [w for w in body if lo <= w["gy"] < hi]
        name = " ".join(w["text"] for ln in _group_lines([w for w in row if w["x0"] < x_u - 2]) for w in ln)
        right_cols = sorted(x for x in (x_id, x_arm) if x is not None)

        def cell(x):
            if x is None:
                return ""
            nxt = next((c for c in right_cols if c > x + 1), float("inf"))
            return " ".join(w["text"] for w in row if x - 2 <= w["x0"] < nxt - 2 and abs(w["gy"] - a["gy"]) < 3)

        ev_id = cell(x_id)
        arm = cell(x_arm)
        if not arm:
            m = re.search(r"_arm_(\d+)$", a["text"])
            arm = m.group(1) if m else None
        project["events"].append({
            "display_name": name.strip(),
            "unique_event_name": a["text"],
            "event_id": ev_id if re.fullmatch(r"\d+", ev_id or "") else None,
            "arm": arm or None,
        })


def _split_event_cell(cell: str, known_events: list) -> list:
    """
    Split an Events cell from the Instruments table into event names when it
    shows display names. Match the Events table's display names (longest first,
    so "Visit 10" is not read as "Visit 1"); otherwise fall back to commas.
    """
    flat = re.sub(r"\s+", " ", cell).strip()
    if not flat:
        return []
    names = sorted({e["display_name"] for e in known_events if e["display_name"]}, key=len, reverse=True)
    if names:
        found = []
        taken = [False] * len(flat)
        for nm in names:
            for m in re.finditer(rf"(?<![\w]){re.escape(nm)}(?![\w])", flat):
                if not any(taken[m.start():m.end()]):
                    found.append((m.start(), nm))
                    for k in range(m.start(), m.end()):
                        taken[k] = True
        if found:
            seen, out = set(), []
            for _, nm in sorted(found):
                if nm not in seen:
                    seen.add(nm)
                    out.append(nm)
            return out
    return [p.strip() for p in flat.split(",") if p.strip()]


# -- Field table --------------------------------------------------------------

def _parse_field_rows(project: dict, words: list, headers: list, clips: dict) -> None:
    h0 = headers[0]
    x_var, x_label, x_attr = h0["x_var"], h0["x_label"], h0["x_attr"]

    def col(w):
        if w["x0"] < x_var - 2:
            return "num"
        if w["x0"] < x_label - 2:
            return "var"
        if w["x0"] < x_attr - 2:
            return "label"
        return "attr"

    def in_header(w):
        return any(w["page"] == h["page"] and abs(w["top"] - h["top"]) < 14
                   and w["x0"] >= h["x_num"] - 3
                   and (_is_bold(w["font"]) or w["text"] in _HEADER_WORDS) for h in headers)

    body = [w for w in words if w["gy"] > h0["gy"] + 8 and w["text"] and not in_header(w)]
    for w in body:
        w["col"] = col(w)

    # Body text size of the label column (section headers and field notes are smaller).
    sizes = Counter(w["size"] for w in body if w["col"] == "label" and not _is_italic(w["font"]))
    body_size = sizes.most_common(1)[0][0] if sizes else 0.0

    banners = [w for w in body if w["text"] == "Instrument:" and w["col"] == "num"]
    var_starts: dict = {}
    for w in body:
        if w["col"] == "var" and w["text"].startswith("["):
            var_starts.setdefault(w["page"], []).append(w)
    anchors = [w for w in body if w["col"] == "num" and re.fullmatch(r"\d+", w["text"])
               and any(abs(v["top"] - w["top"]) < 3 for v in var_starts.get(w["page"], []))]

    marks = sorted([(b["gy"], "banner", b) for b in banners] + [(a["gy"], "field", a) for a in anchors],
                   key=lambda m: m[0])
    # Expression-wrap limit of the variable column (its right padding is ~6-7pt).
    var_limit = x_label - 6.6
    current: dict | None = None

    for k, (gy, kind, w) in enumerate(marks):
        lo = gy - 4
        hi = marks[k + 1][0] - 4 if k + 1 < len(marks) else float("inf")
        if kind == "banner":
            line = [v for v in body if abs(v["gy"] - gy) < 4]
            text = " ".join(v["text"] for v in sorted(line, key=lambda v: v["x0"]))
            m = re.search(r"Instrument:\s+(.+?)\s*\(([a-z][a-z0-9_]*)\)", text)
            if m:
                display_nm, form_nm = m.group(1).strip(), m.group(2)
            else:
                display_nm = re.sub(r"^.*?Instrument:\s*", "", text).strip()
                form_nm = re.sub(r"\W+", "_", display_nm.lower()).strip("_")
            current = new_instrument(display_nm, form_nm)
            current["is_survey"] = "Enabled as survey" in text
            project["instruments"].append(current)
            continue

        region = [v for v in body if lo <= v["gy"] < hi]
        for v in region:
            v["clipped"] = v["x1"] > clips.get(v["page"], 1e9) - 6
        by_col = {c: [v for v in region if v["col"] == c] for c in ("var", "label", "attr")}
        f = new_field()
        f["number"] = int(w["text"])
        if not _parse_var_column(f, _lines(by_col["var"]), var_limit):
            continue
        if current is None:
            current = new_instrument("Unknown Instrument", "unknown")
            project["instruments"].append(current)
        if f["variable"] == f"{current['form_name']}_complete":
            continue
        _parse_label_column(f, _lines(by_col["label"]), body_size)
        _parse_attr_column(f, _lines(by_col["attr"]), x_attr)
        f["truncated"] = any(v["clipped"] for v in region)
        current["fields"].append(f)


def _join_expr(lines: list, mode: str = "normal", limit: float | None = None,
               straighten: bool = True) -> str:
    """
    Re-join wrapped lines of an expression (branching logic, calc, annotation).
    The PDF has no trailing spaces, so whether a space was lost at a wrap is
    inferred:
      * inside an unclosed [...] or between "][": no space (split name);
      * mode "break_all" (variable column, which breaks mid-word): no space only
        when the previous line is full and the wrap is between two word
        characters (e.g. "o" + "r [x] = '1'");
      * mode "normal" (attributes column, wraps at spaces or after a closing
        bracket): no space after ")" / "]" before a comparison operator,
        or after a word hyphen.
    Curly quotes are text-layer artifacts in expressions and are straightened
    unless straighten=False (annotations are kept verbatim). Where a line was
    clipped at the page edge, CLIP_MARK marks the lost text.
    """
    out, prev = "", None
    for ln in lines:
        t = ln["text"].strip()
        if straighten:
            t = t.translate(_QUOTES)
        if not t:
            continue
        if not out:
            out, prev = t, ln
            continue
        a, b = out[-1].translate(_QUOTES), t[0].translate(_QUOTES)
        word = lambda c: c.isalnum() or c == "_"
        if prev.get("clipped"):
            sep = CLIP_MARK       # text past the printed page edge is lost
        elif out.count("[") > out.count("]") or (a == "]" and b == "["):
            sep = ""
        elif mode == "break_all":
            full = limit is not None and prev["x1"] + ln["cw"] > limit + 0.5
            sep = "" if full and word(a) and word(b) else " "
        elif a in ")]" and b in "<>=!":
            sep = ""
        elif a == "-" and len(out) > 1 and out[-2].isalnum() and b.isalnum():
            sep = ""
        else:
            sep = " "
        out += sep + t
        prev = ln
    return out


def _join_text(parts: list) -> str:
    """Join wrapped label/choice text: one space, none after a word hyphen
    or between "][" (a wrapped piping reference)."""
    out = ""
    for p in (x.strip() for x in parts):
        if not p:
            continue
        if out and ((out[-1] == "-" and len(out) > 1 and out[-2].isalpha() and p[0].isalpha())
                    or (out[-1] == "]" and p[0] == "[")):     # hyphen / piping "[event][field]"
            out += p
        else:
            out = f"{out} {p}" if out else p
    return out


def _parse_var_column(f: dict, lines: list, limit: float) -> bool:
    """[variable_name] (wrapped mid-name if long), then optional
    'Show the field ONLY if:' and the branching logic. False if no variable."""
    texts = [ln["text"] for ln in lines]
    k_bl, span = len(lines), 0
    for k in range(1, len(lines)):
        for s in (1, 2, 3):
            key = re.sub(r"\s+", "", "".join(texts[k:k + s])).lower().replace("!eld", "field")
            if key == _SHOW_IF_KEY:
                k_bl, span = k, s
                break
        if span:
            break
    name = re.sub(r"\s+", "", "".join(texts[:k_bl]))
    m = re.match(r"^\[([a-z][a-z0-9_]*)\]", name)
    if not m:
        return False
    f["variable"] = m.group(1)
    if span:
        f["branching_logic"] = _join_expr(lines[k_bl + span:], "break_all", limit) or None
    return True


def _small_italic(line: dict, body_size: float) -> bool:
    return all(_is_italic(w["font"]) and (not body_size or w["size"] < body_size - 0.4)
               for w in line["words"])


def _parse_label_column(f: dict, lines: list, body_size: float) -> None:
    """Optional 'Section Header: ...' (small italic), the label (rendered text
    for HTML labels), then the field note (small italic, after the label)."""
    i = 0
    if lines and lines[0]["text"].startswith("Section Header:"):
        parts = [lines[0]["text"][len("Section Header:"):]]
        i = 1
        while i < len(lines) - 1 and _small_italic(lines[i], body_size):
            parts.append(lines[i]["text"])
            i += 1
        f["section_header"] = _join_text(parts) or None
    rest = lines[i:]
    j = len(rest)
    while j > 1 and _small_italic(rest[j - 1], body_size):
        j -= 1
    f["label"] = _join_text([ln["text"] for ln in rest[:j]])
    f["field_note"] = _join_text([ln["text"] for ln in rest[j:]]) or None


def _parse_type_line(f: dict, type_line: str) -> None:
    """
    First line(s) of the attributes cell, e.g.:
      "text (email), Required, Identifier"
      "text (integer, Min: 0, Max: 120)"
      "slider (number, Min: 0, Max: 100)"   (number = show slider value)
      "radio (Matrix), Required"
    """
    type_m = _FIELD_TYPES_RE.match(type_line)
    if type_m:
        f["type"] = type_m.group(1).lower()

    paren = re.search(r"\(([^)]*)\)", type_line)
    if paren:
        inner = paren.group(1)
        if re.search(r"\bMatrix\b", inner):
            f["is_matrix"] = True
        mn = re.search(r"Min:\s*([^,)]*)", inner, re.IGNORECASE)
        mx = re.search(r"Max:\s*([^,)]*)", inner, re.IGNORECASE)
        if mn and mn.group(1).strip():
            f["validation_min"] = mn.group(1).strip()
        if mx and mx.group(1).strip():
            f["validation_max"] = mx.group(1).strip()
        first = inner.split(",", 1)[0].strip()
        if first and not re.match(r"^(Min|Max):|^Matrix$", first, re.IGNORECASE) \
                and f["type"] in ("text", "slider", "dropdown"):
            f["validation"] = first

    rest = type_line[paren.end():] if paren else type_line
    f["required"] = bool(re.search(r"\bRequired\b", rest))
    f["identifier"] = bool(re.search(r"\bIdentifier\b", rest))


def _parse_attr_column(f: dict, lines: list, x_attr: float) -> None:
    """
    Field Attributes column. Lines at the column's left edge: type line,
    "Calculation:", "Field Annotation:", "Slider labels:", "Custom alignment:",
    "Question number:". Indented lines: choices ("code  label", checkbox
    "code  field___code  label"), wrapped choice labels further right, or an
    ontology (BIOPORTAL:...) for text fields.
    """
    if not lines:
        return
    i, type_parts = 0, []
    while i < len(lines) and (i == 0 or "".join(type_parts).count("(") > "".join(type_parts).count(")")):
        type_parts.append(lines[i]["text"])
        i += 1
        if i >= 3:
            break
    _parse_type_line(f, " ".join(type_parts))

    mode = None              # None | "annotation" | "calc"
    ann_lines: list = []
    calc_lines: list = []
    code_x = None
    last_choice = None

    for ln in lines[i:]:
        t = ln["text"].strip()
        indented = ln["x0"] > x_attr + 1.5

        if indented:
            mode = None
            if f["type"] in CHOICE_LIKE:
                if code_x is None:
                    code_x = ln["x0"]
                if ln["x0"] < code_x + 1.5:
                    toks = t.split()
                    code, rest = toks[0], toks[1:]
                    if f["type"] == "checkbox" and rest and re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*___\S+", rest[0]):
                        rest = rest[1:]
                    last_choice = {"value": code, "label": " ".join(rest)}
                    f["choices"].append(last_choice)
                elif last_choice is not None:
                    last_choice["label"] = _join_text([last_choice["label"], t])
                else:
                    f["other_attributes"].append(t)
            elif re.match(r"^[A-Z][A-Z0-9_-]*:\S+", t) and f["type"] == "text" and not f["ontology"]:
                f["ontology"] = t.split()[0]
            else:
                f["other_attributes"].append(t)
            continue

        last_choice = None
        if t in ("Required", "Identifier"):
            f["required"] = f["required"] or t == "Required"
            f["identifier"] = f["identifier"] or t == "Identifier"
            mode = None
            continue
        marker = next((mk for mk in _ATTR_MARKERS if t.startswith(mk)), None)
        if marker:
            val = t[len(marker):].strip()
            mode = None
            if marker == "Field Annotation:":
                mode = "annotation"
                if val:
                    ann_lines.append(dict(ln, text=val))
            elif marker == "Calculation:":
                mode = "calc"
                if val:
                    calc_lines.append(dict(ln, text=val))
            elif marker == "Custom alignment:":
                f["custom_alignment"] = val or None
            elif marker == "Question number:":
                f["question_number"] = val or None
            elif marker == "Slider labels:":
                f["slider_labels"] = [x.strip() for x in re.split(r",\s?", val)]
            continue
        if mode == "annotation":
            ann_lines.append(ln)
        elif mode == "calc":
            calc_lines.append(ln)
        elif f["type"] == "calc" and not calc_lines:
            calc_lines.append(ln)          # older layouts: formula without a prefix
        else:
            f["other_attributes"].append(t)

    if calc_lines:
        f["formula"] = _join_expr(calc_lines, "normal") or None
    if ann_lines:
        full_ann = _join_expr(ann_lines, "normal", straighten=False)   # verbatim
        # Repair hyphenated tags split across lines ("@HIDESUBMIT- SURVEY")
        full_ann = re.sub(r"(@[A-Z][A-Z0-9_]*-)\s+([A-Z])", r"\1\2", full_ann)
        f["annotation"] = full_ann or None
        f["action_tags"] = extract_action_tags(full_ann)


# -- Summary stats ------------------------------------------------------------

def compute_stats(project: dict) -> dict:
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
    }


REPEATING_NOTE = (
    "Repeating setup is read only from the repeat icon (a Font Awesome glyph) "
    "next to an instrument/its events in the Instruments table, when the PDF "
    "text layer carries it; repeating whole events are not detected. Confirm "
    "with export_repeating_instruments_events via a REDCap connector."
)
NOT_IN_PDF_NOTE = (
    "Not available from a Codebook PDF: matrix group names (only '(Matrix)' is "
    "printed), matrix ranking, raw HTML/markup of labels (only the rendered text), "
    "and the exact spacing at line wraps inside expressions (re-joined heuristically). "
    "Text that ran past the page edge when printed is clipped and lost."
)


# -- Output: --summary --------------------------------------------------------

def print_summary(project: dict) -> None:
    stats = compute_stats(project)
    instruments = project["instruments"]

    print(f"\n{'='*70}")
    title = project["project_title"]
    if project["project_pid"]:
        title += f" (PID: {project['project_pid']})"
    print(f"REDCap Project: {title}")
    if project["snapshot_date"]:
        print(f"Snapshot: {project['snapshot_date']}")
    print("Source: Codebook PDF")
    print(f"{'='*70}")

    print(f"\nProject type: {project['project_type']} (heuristic, from form names/labels)")
    print(f"Total fields: {stats['total_fields']} across {stats['instrument_count']} instrument(s)"
          f" (auto-generated _complete fields excluded)")

    if project["is_longitudinal"]:
        print("Longitudinal: Yes")
        if project["events"]:
            print(f"Events: {len(project['events'])}")

    if stats["survey_count"]:
        print(f"Surveys: {stats['survey_count']} instrument(s) enabled as survey")

    print(f"\n── Field Types ──")
    for ft, cnt in sorted(stats["field_type_distribution"].items(), key=lambda x: -x[1]):
        print(f"  {ft or '(unknown)':<15} {cnt}")

    if project["events"]:
        print(f"\n── Events ({len(project['events'])}) ──")
        for ev in project["events"]:
            extra = f"  [arm: {ev['arm']}]" if ev.get("arm") else ""
            print(f"  {ev['display_name']} → {ev['unique_event_name']}{extra}")
        print("  (Use unique_event_name in expressions like [event_name][field_name])")

    print(f"\n── Instruments ──")
    for instr in instruments:
        tags = []
        if instr["is_survey"]: tags.append("survey")
        if instr.get("repeating_icon") or instr.get("repeating_events"):
            tags.append("repeat icon")
        if instr["events"]:    tags.append(f"events: {', '.join(instr['events'])}")
        tag_str = f"  [{', '.join(tags)}]" if tags else ""
        fields = instr["fields"]
        ft_local = Counter(f["type"] for f in fields)
        bl_local = sum(1 for f in fields if f["branching_logic"])
        calc_local = ft_local.get("calc", 0)

        print(f"\n  {instr['display_name']} ({instr['form_name']})"
              f"  —  {len(fields)} fields{tag_str}")
        print(f"    Field types: " +
              ", ".join(f"{ft}:{cnt}" for ft, cnt in sorted(ft_local.items(), key=lambda x: -x[1])))
        if bl_local:
            print(f"    Branching logic on {bl_local} field(s)")
        if calc_local:
            print(f"    Calculated fields: {calc_local}")

        ids      = [f for f in fields if f["identifier"]]
        required = [f for f in fields if f["required"]]
        calcs    = [f for f in fields if f["type"] == "calc"]
        tagged   = [f for f in fields if f["action_tags"]]

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

        data_fields = [f for f in fields if f["type"] != "descriptive" and f["label"]]
        if data_fields:
            print(f"    Sample questions:")
            for f in data_fields[:5]:
                print(f"      • [{f['variable']}] {f['label'][:80]}")

    warnings = _collect_warnings(project)
    if warnings:
        print(f"\n── ⚠  Warnings ({len(warnings)}) ──")
        for w in warnings:
            print(f"  ⚠  {w}")

    print(f"\n  Note: {REPEATING_NOTE}")
    print(f"  Note: {NOT_IN_PDF_NOTE}")
    if project["is_longitudinal"] and not any(i["events"] for i in instruments):
        print("  Note: Instrument-event assignments could not be read from this PDF; "
              "use export_instrument_event_mappings via a REDCap connector.")
    print()


# -- Output: --llm-context ----------------------------------------------------

def print_llm_context(project: dict) -> None:
    """Complete structured dump of the project for LLM consumption (no truncation)."""
    stats = compute_stats(project)

    print(f"=== REDCap Project Context ===")
    title = project["project_title"]
    if project["project_pid"]:
        title += f" | PID: {project['project_pid']}"
    if project["snapshot_date"]:
        title += f" | Snapshot: {project['snapshot_date']}"
    print(title)
    print("Source: Codebook PDF (auto-generated {form_name}_complete fields omitted)")
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
    if flags:
        print(f"Flags: {' | '.join(flags)}")
    print(f"Note: {REPEATING_NOTE}")
    print(f"Note: {NOT_IN_PDF_NOTE}")

    if project["events"]:
        print(f"\n--- EVENTS ({len(project['events'])}) ---")
        for ev in project["events"]:
            extra = []
            if ev.get("arm"):      extra.append(f"arm={ev['arm']}")
            if ev.get("event_id"): extra.append(f"id={ev['event_id']}")
            ex = f" [{', '.join(extra)}]" if extra else ""
            print(f"  {ev['display_name']} → {ev['unique_event_name']}{ex}")

    print(f"\n--- INSTRUMENTS ---")
    for i, instr in enumerate(project["instruments"], 1):
        tags = []
        if instr["is_survey"]: tags.append("survey")
        rep_ev = instr.get("repeating_events") or []
        if rep_ev and rep_ev == instr["events"]:
            tags.append("repeat icon (instrument, on all its events)")
        elif instr.get("repeating_icon") or rep_ev:
            tags.append("repeat icon" + (" on events:" + ",".join(rep_ev) if rep_ev else ""))
        if instr["events"]:    tags.append("events(as printed):" + ",".join(instr["events"]))
        tag_str = f" [{'; '.join(tags)}]" if tags else ""
        print(f"  {i}. {instr['display_name']} ({instr['form_name']}) — {len(instr['fields'])} fields{tag_str}")

    print(f"\n--- FIELDS ---")
    for instr in project["instruments"]:
        tag_str = " [SURVEY]" if instr["is_survey"] else ""
        print(f"\n=== {instr['display_name']} ({instr['form_name']}){tag_str} ===")
        if instr["events"]:
            print(f"  [Events (as printed): {', '.join(instr['events'])}]")
        for f in instr["fields"]:
            _print_llm_field(f)

    warnings = _collect_warnings(project)
    if warnings:
        print(f"\n--- WARNINGS ({len(warnings)}) ---")
        for w in warnings:
            print(f"  ! {w}")
    print()


def _print_llm_field(f: dict) -> None:
    """Print one field entry. Nothing is truncated."""
    if f.get("section_header"):
        print(f"  [SECTION: {f['section_header']}]")

    num = f"#{f['number']} " if f["number"] else ""
    type_str = f["type"] or "?"
    if f["validation"]:
        type_str += f"/{f['validation']}"
    if f["validation_min"] or f["validation_max"]:
        type_str += f" [{f['validation_min'] or '?'}..{f['validation_max'] or '?'}]"

    flag_parts = []
    if f["required"]:   flag_parts.append("required")
    if f["identifier"]: flag_parts.append("identifier")
    if f.get("is_matrix"): flag_parts.append("matrix (group name not in PDF)")

    bl_prefix = "[if] " if f["branching_logic"] else ""
    line = f"  {bl_prefix}{num}{f['variable']} | {type_str} | {f['label']!r}"
    if flag_parts:
        line += f" | {', '.join(flag_parts)}"
    print(line)

    if f["choices"]:
        print(f"    → {fmt_choices(f['choices'])}")
    if f.get("slider_labels"):
        print(f"    slider labels: {' | '.join(f['slider_labels'])}")
    if f.get("ontology"):
        print(f"    ontology: {f['ontology']}")
    if f["formula"]:
        print(f"    calc: {f['formula']}")
    if f["branching_logic"]:
        print(f"    BL: {f['branching_logic'].strip()}")
    if f["annotation"]:
        print(f"    annotation: {f['annotation']}")
    if f.get("field_note"):
        print(f"    note: {f['field_note']}")
    extras = []
    if f.get("custom_alignment"): extras.append(f"alignment={f['custom_alignment']}")
    if f.get("question_number"):  extras.append(f"question_number={f['question_number']}")
    if extras:
        print(f"    {' | '.join(extras)}")
    for line in f.get("other_attributes") or []:
        print(f"    attr: {line}")
    if f.get("truncated"):
        print("    ! text clipped at the printed page edge; label/annotation may be incomplete")


# -- Warnings -----------------------------------------------------------------

def _collect_warnings(project: dict) -> list:
    warnings = []
    for instr in project["instruments"]:
        for f in instr["fields"]:
            if f["type"] == "checkbox" and f["required"]:
                warnings.append(
                    f"[{f['variable']}] is a checkbox marked required — "
                    f"REDCap cannot enforce 'at least one selected'. The required flag is silently ignored."
                )
            if f.get("truncated"):
                warnings.append(
                    f"[{f['variable']}] has text that ran past the printed page edge and was clipped "
                    f"in the PDF; its label/annotation may be incomplete (check the Codebook page or "
                    f"export_metadata)."
                )
    return warnings


# -- Entry point --------------------------------------------------------------

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    path = sys.argv[1]
    mode = "llm-context" if "--llm-context" in sys.argv else "summary"
    ext = Path(path).suffix.lower()

    if ext == ".csv":
        print(
            "This skill reads REDCap Codebook PDFs only. For a Data Dictionary CSV use the\n"
            "redcap-data-dictionary skill:\n"
            f"    {DD_SKILL_CMD.replace('<csv>', chr(34) + path + chr(34))}",
            file=sys.stderr,
        )
        sys.exit(2)
    if ext != ".pdf":
        print(f"Error: expected a Codebook .pdf, got '{ext or 'no extension'}'.", file=sys.stderr)
        sys.exit(2)
    if not Path(path).is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        project = parse_pdf(path)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not project["instruments"] or not any(i["fields"] for i in project["instruments"]):
        print(
            "Error: no Codebook field table found in this PDF. Make sure it is a saved copy of "
            "the Codebook page (Project Setup or left-hand menu -> Codebook), not "
            "'Download PDF of All Instruments' (blank data-entry forms).\n" + CONNECTOR_HINT,
            file=sys.stderr,
        )
        sys.exit(1)

    if mode == "llm-context":
        print_llm_context(project)
    else:
        print_summary(project)


if __name__ == "__main__":
    main()

---
name: redcap-codebook-reader
description: |
  Read and interpret a REDCap Codebook PDF (a saved/printed copy of the
  project's Codebook page) to produce a structured project overview. PDF
  codebooks only. Use when a user uploads a Codebook PDF and wants to
  understand what a REDCap project collects, get a summary they can share
  with stakeholders, or provide a complete project description for
  LLM-assisted analysis. Trigger on: "summarize this codebook", "what does
  this project collect" (with a Codebook PDF), "read this codebook", "what's
  in this codebook", "explain this project to me" (with a Codebook PDF), or
  any time a user uploads a PDF whose name contains Codebook and asks for a
  description or summary. Also use when another skill needs the full picture
  of a project and only a Codebook PDF is available. Use --llm-context when
  another skill or pipeline needs the output; --summary for human-facing
  output. Do NOT use for Data Dictionary CSVs (redcap-data-dictionary) or
  for live projects (redcap-project-analyzer).
---

# REDCap Codebook Reader Skill

> **REDCap connectors:** before calling any REDCap MCP tool from this skill, read `references/CONNECTOR-RULES.md` (bundled with this skill; the source copy is `claude skills/CONNECTOR-RULES.md` in the REDCap_KB_RAG repo) and follow it — confirm the connector and PID, flag production, stay read-only unless the user explicitly confirms a write on a non-production connector, and never expose the API token.

This skill reads a REDCap **Codebook PDF** and produces either a
human-readable narrative summary or a complete LLM-context dump of the
project structure.

**Not for:**
- **Data Dictionary CSVs** → use the redcap-data-dictionary skill:
  `python ~/.claude/skills/redcap-data-dictionary/scripts/parse_dd.py <csv> --text`
  (the script exits with this pointer if given a `.csv`).
- **Live projects with API access** → use redcap-project-analyzer.

---

## Offer the API Route First (when available)

A PDF is a lossy source: text extraction can mangle wrapped expressions,
and some information is shown only as icons. If the user has API access to
the project and a REDCap connector is available, pulling metadata directly
is more reliable than parsing a PDF. Offer it:

> "If you have API access to this project, I can read its structure
> directly through the REDCap connector instead of parsing the PDF — that is
> more reliable, especially for events and repeating setup. Want me to do
> that?"

The read-only exports that cover what the Codebook shows:

| Export | Gives you |
|--------|-----------|
| `export_metadata` | Every field: name, form, type, label, choices, calc, validation, branching logic, annotation, required/identifier |
| `export_events` | Events with unique event names (longitudinal) |
| `export_instrument_event_mappings` | Which instruments are assigned to which events |
| `export_repeating_instruments_events` | Which instruments/events are repeating |

Only these read-only exports are needed — never call import/delete tools
for this task. If the user prefers the PDF (or has no API access), continue
below.

---

## Step 1 — Get the Codebook PDF

Use the path the user gives or attaches. If they only name the file, look
in the folder they are working in or use Glob; ask if more than one file
matches.

**If they don't have it yet**, tell them how to get it (RC-FD-05 §3):

> "Open the Codebook in your project — either from **Project Setup** (click
> **Codebook** in the *Design your data collection instruments* section) or
> from the **left-hand project menu → Codebook**. Then print the page and
> choose **Save as PDF** (or use a PDF/download option if your REDCap
> version shows one on the Codebook page). Send me that PDF."

**Not the same thing:** *"Download PDF of All Instruments"* produces the
blank data-entry forms, not the Codebook. It lacks the field-attribute
table, the Instruments/Events summary tables, and the codebook layout this
script parses. If that's what the user has, ask for the Codebook instead
(or offer the connector route above). If the script reports *"no Codebook
field table found"*, this mix-up is the most likely cause.

---

## Step 2 — Choose the Output Mode

| Situation | Use mode |
|-----------|----------|
| User wants a plain-language summary | `--summary` |
| User wants to share with stakeholders or document the project | `--summary` |
| Another skill needs project context before its work | `--llm-context` |
| User says "for an LLM", "machine-readable", or "structured" | `--llm-context` |
| User wants to paste context into another Claude session | `--llm-context` |

When unclear, default to `--summary` and offer `--llm-context` if they need
it for further processing.

---

## Step 3 — Run the Script

**Finding `<skill_path>`:** The skill's base directory, shown when the skill loads (normally `~/.claude/skills/<skill-name>`).

```bash
python <skill_path>/scripts/codebook_report.py <path_to_codebook.pdf> --summary
python <skill_path>/scripts/codebook_report.py <path_to_codebook.pdf> --llm-context
```

The script needs **pdfplumber**. If it is missing, the script exits with
an install hint; install it and re-run:
```bash
py -m pip install pdfplumber
```

Exit codes: `0` ok; `1` unreadable PDF / missing file / pdfplumber
missing / no Codebook field table found; `2` wrong input type (e.g. a CSV).

Read the full output before presenting it to the user.

---

## Step 4 — Present or Use the Output

### For `--summary` output (human-facing):

Present the output as-is or lightly reformat it. Call out:

- **Project type and scale** — the project-type label is a keyword
  heuristic; treat it as a guess.
- **Events** (if longitudinal) — list the unique event names, since these
  are what REDCap uses in expressions like `[event_name][field_name]`.
- **Instrument-event assignments** — shown exactly as printed in the
  Codebook's Instruments table (unique event names such as
  `baseline_arm_1` in current REDCap versions).
- **Repeating setup** — only a "repeat icon" flag read from the icon glyph in
  the Instruments table (see below). Present it as likely, not confirmed;
  confirm with `export_repeating_instruments_events` or a visual check.
- **Clipped text** — a warning means some text ran past the printed page
  edge and is missing from the PDF (marked `[...clipped...]`).
- **Notable design features** — action tags, calculated scoring, cross-
  instrument dependencies, matrix groups.
- **Warnings** — e.g. required checkboxes.

### For `--llm-context` output (machine-facing):

Pass the output verbatim. Nothing is truncated: full labels, every choice,
full branching logic, full calc formulas, and the complete Field Annotation
text (including `@CALCTEXT(...)`/`@DEFAULT=...` expressions). When handing
off to another skill, prepend:

> "Use the following REDCap project context to complete the task. All field
> names, choice codes, and event names in this context are the exact strings
> used in REDCap expressions."

---

## What the Script Extracts (and What It Doesn't)

The script reads the browser-printed Codebook page by word position (column
layout taken from the field table's header row). It drops the browser's
print header/footer (date, page title, page URL, `1/17` page counter) and
removes icon-font glyphs (Unicode Private Use Area). Per RC-FD-05, the
Codebook shows the items below. The script extracts:

- Project title, PID, and snapshot timestamp (header)
- Variable names, field types, labels, section headers, and field notes
  (the small italic line under the label)
- Choices with raw codes and labels, any code format (`1`, `-77`, `AL`,
  `Other`), read from the choice table's code column; wrapped choice labels
  are re-joined. Checkbox options skip the `fieldname___code` subvariable.
  Yes/No and True/False fields show their fixed `1`/`0` choices.
- Validation type and min/max (`text (integer, Min: 0, Max: 120)`); slider
  min/max, "show number" (`slider (number, ...)`), and slider labels
- Calculation formulas
- Branching logic ("Show the field ONLY if:")
- Field annotations, verbatim, plus the list of action tags
- Required and Identifier flags; custom alignment; survey question number;
  the "(Matrix)" flag; BioPortal ontology on text fields
- "Enabled as survey" per instrument
- Events table (longitudinal): event name, unique event name, event ID; arm
  from the `_arm_N` suffix
- Instrument-event assignments from the Instruments table's Events column,
  as printed (unique event names in current versions, so arm-qualified)
- A "repeat icon" flag when the Instruments table shows the repeat icon
  glyph (Font Awesome U+F363) next to an instrument or its events

On the test project (103 fields, 10 instruments) every field, form, type,
label, choice, validation, calc, branching logic, flag, note and section
header matched the Data Dictionary. The only mismatch was one annotation
that was clipped at the page edge in the PDF.

**Not extracted from the PDF — say so rather than guess:**

- **Matrix group names and matrix ranking.** Only "(Matrix)" is printed.
- **Raw HTML/markup** in labels and section headers. The PDF holds only the
  rendered text (descriptive fields with HTML come out as plain text).
- **Confirmed repeating setup.** The repeat icon flag depends on the glyph
  surviving in the text layer, and whole-event repeating is not detected.
  Use `export_repeating_instruments_events`.
- **Text clipped at the page edge.** A long unbroken string (e.g. a
  `@CALCTEXT(...)` with no spaces) can run past the printed page and is
  lost. The script marks the gap `[...clipped...]` and warns; get the
  exact text from the Codebook page or `export_metadata`.
- **Exact whitespace at line wraps** in expressions. Wrapped lines are
  re-joined by rule (no space inside `[...]` or between `][`; mid-word
  breaks in branching logic are detected from line width), which matched
  the test project, but odd spacing in the original cannot be recovered.
- **Slider labels that contain commas** are split at the comma (the PDF
  prints them comma-separated).

The Codebook itself does NOT include (configure separately in REDCap):
survey settings, user rights and DAGs, randomization, alerts, data quality
rules, reports.

**Text-extraction caveats:** Ligature code points (U+FB00–FB06) are
normalized; the known REDCap boilerplate artifact `Show the !eld ONLY if`
is repaired. Ordinary characters such as `!` and `#` in user text are never
rewritten, so if a font maps a ligature to `!`/`#` you may see e.g. `O#ce`
in a label — read it in context, and prefer the connector route for exact
text. Curly quotes in branching logic and calc formulas are straightened
(REDCap expressions only accept straight quotes); annotations are left
verbatim.

---

## Auto-Generated `_complete` Fields

Every instrument has a system-generated completion status field named
`{form_name}_complete` (e.g. `application_complete`), a dropdown with
`0` Incomplete, `1` Unverified, `2` Complete. It appears as the last field
of each instrument in the Codebook and in data exports, but not in the Data
Dictionary CSV (RC-FD-05 §5) — so the Codebook has exactly one more field
per instrument than the CSV.

**The script skips only `{form_name}_complete` for the instrument being
parsed**, so field counts align with the Data Dictionary. User fields that
merely end in `_complete` (e.g. `consent_complete` on a non-`consent` form)
are kept. Reference completion status in downstream work by its variable
name:

```
# Show a field only if a prior form is marked Complete
[intake_complete] = '2'

# Calc that counts how many forms are complete
if([form_a_complete]='2', 1, 0) + if([form_b_complete]='2', 1, 0)
```

---

## Important REDCap Syntax Notes

- **Checkbox expression syntax:** The Codebook shows `fieldname___code` as the
  subvariable name (used in exports), but REDCap expressions must use
  `[fieldname(code)]` — e.g., `[race(3)] = '1'`. Never use the triple-underscore
  form in branching logic or calc fields.

- **Choice codes vs. labels:** In branching logic, always use the raw code,
  not the label. E.g., `[sex] = '1'` not `[sex] = 'Female'`.

- **Event names in expressions:** Cross-event references use the unique
  event name: `[baseline_arm_1][weight]`, not the display name ("Baseline").

- **Piped labels:** The Codebook shows raw piping syntax like
  `[event][field]` in labels; it does not resolve piped values.

---

## Common Scenarios

**User uploads a Data Dictionary CSV:**
→ Don't use this skill. Use redcap-data-dictionary
(`parse_dd.py <csv> --text`).

**User uploads a Codebook PDF for a longitudinal project:**
→ If they have API access, offer the connector route. Otherwise run
`--summary` (and `--llm-context` if a follow-up task needs it). Flag that
repeating setup must be checked separately.

**User uploads "Download PDF of All Instruments" output:**
→ Explain it's the blank forms, not the Codebook; give the Step 1
instructions or offer the connector route.

**Another skill (e.g., redcap-syntax) needs project context:**
→ Run `--llm-context` and pass the output verbatim.

**User says "I need to describe this project for an IRB submission":**
→ Run `--summary`, then offer a Word document via the docx skill.

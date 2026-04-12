---
name: redcap-codebook-reader
description: |
  Read and interpret a REDCap Codebook PDF or Data Dictionary CSV to produce
  a structured project overview. Use this skill whenever a user uploads a
  Codebook PDF or Data Dictionary CSV and wants to understand what a REDCap
  project collects, get a summary they can share with stakeholders, or
  provide a complete project description for LLM-assisted analysis. Trigger
  on: "summarize this project", "what does this project collect", "give me
  an overview of this REDCap project", "I uploaded a codebook", "read this
  codebook", "what's in this codebook", "explain this project to me",
  "help an LLM understand this project", "create a project summary for
  documentation", or any time a user uploads a file whose name ends in
  DataDictionary, Codebook, or PDF and asks for a description or summary.
  Also trigger when another skill needs a full picture of the project
  before doing its work (e.g. building branching logic, writing KB articles
  about a specific project). Use --llm-context mode when another skill or
  pipeline needs the output, or when the user asks for a machine-readable
  or structured version. Use --summary mode for human-facing output.
---

# REDCap Codebook Reader Skill

This skill reads a REDCap Codebook (PDF or Data Dictionary CSV) and produces
either a human-readable narrative summary or a compact LLM-context dump
of the full project structure.

---

## What This Skill Does

The REDCap Codebook is the authoritative human-readable view of a project's
instruments and variables (RC-FD-05). It shows every field's variable name,
label, type, choices, branching logic, action tags, and required/identifier
flags — all in one place. For longitudinal projects, it also includes the
Events table with unique event names and the repeating instrument/event
configuration.

This skill parses that information and produces one of two outputs:

- **`--summary`** (default) — A narrative overview for human consumption.
  Use for: project documentation, stakeholder briefs, onboarding to an
  unfamiliar project, or preparing context before consulting with an SME.

- **`--llm-context`** — A compact, token-efficient structured dump for
  LLM consumption. Use for: giving another Claude session a complete
  picture of the project before asking it to write branching logic,
  build a data dictionary, answer questions about specific fields, etc.
  The format encodes every field (variable name, type, label, choices,
  branching logic conditions, action tags) as a dense but readable
  per-line entry, grouped by instrument.

---

## Supported Input Formats

| Format | How to get it from REDCap | What it includes |
|--------|--------------------------|-----------------|
| **PDF** (preferred) | Project Setup → "Download PDF of All Instruments" | Full Codebook: instruments, fields, event table, repeating config |
| **CSV** | Project Setup → "Download the current Data Dictionary" | Field content only — no event table, no repeating setup |

**Recommend PDF for longitudinal projects.** The Data Dictionary CSV does not
include the Events table or the instrument-event assignment information.
The Codebook PDF is the only single-document source for the full project
picture, including which events each instrument appears at and which
instruments are configured as repeating. For classic (non-longitudinal)
projects, the CSV is sufficient.

---

## Step 1 — Identify the Input File

The user will have uploaded one of:
- A PDF file (often named something like `MyStudy_Codebook.pdf` or downloaded
  via "Download PDF of All Instruments")
- A CSV file (named with `_DataDictionary_` in the filename)

Uploaded files are at `/sessions/.../mnt/uploads/<filename>`.
If the user has a mounted workspace folder, check there too.

**If neither format is uploaded**, ask the user:
> "To give you a full project overview, I'll need either the Codebook PDF
> (from Project Setup → 'Download PDF of All Instruments') or the Data
> Dictionary CSV (from Project Setup → 'Download the current Data
> Dictionary'). The PDF is preferred for longitudinal projects as it
> includes the events table. Which do you have?"

---

## Step 2 — Choose the Output Mode

| Situation | Use mode |
|-----------|----------|
| User wants a plain-language summary | `--summary` |
| User wants to share with stakeholders or document the project | `--summary` |
| Another skill needs project context before its work | `--llm-context` |
| User says "for an LLM", "machine-readable", or "structured" | `--llm-context` |
| User wants to paste context into another Claude session | `--llm-context` |

When unclear, default to `--summary` and offer to also produce
`--llm-context` if they need it for further processing.

---

## Step 3 — Run the Script

**Finding `<skill_path>`:** The skill lives in the directory containing
this SKILL.md file. Use that as `<skill_path>`.

```bash
# For PDF input:
python <skill_path>/scripts/codebook_report.py <path_to_codebook.pdf> --summary
python <skill_path>/scripts/codebook_report.py <path_to_codebook.pdf> --llm-context

# For CSV input:
python <skill_path>/scripts/codebook_report.py <path_to_dd.csv> --summary
python <skill_path>/scripts/codebook_report.py <path_to_dd.csv> --llm-context
```

If PDF mode fails with an import error, install pdfplumber first:
```bash
pip install pdfplumber --break-system-packages
```

Read the full output before presenting to the user.

---

## Step 4 — Present or Use the Output

### For `--summary` output (human-facing):

Present the output as-is or lightly reformat it. Call out:

- **Project type and scale** — what kind of project it is, how many
  instruments and fields.
- **Events** (if longitudinal) — list all unique event names, since these
  are needed in branching logic and piping expressions. Remind the user
  these exact strings are what REDCap uses in expressions like
  `[event_name][field_name]`.
- **Repeating setup** — note which instruments use `[current-instance]`
  (indicating a repeating instrument), since the Data Dictionary alone
  cannot show this configuration.
- **Notable design features** — action tags, calculated scoring, cross-
  instrument dependencies, matrix groups.
- **Warnings** — required checkboxes, missing choices, etc.
- **Source limitation** — if the source was CSV, remind the user that
  the event table and repeating configuration are not available and
  recommend the Codebook PDF for a complete picture.

### For `--llm-context` output (machine-facing):

Pass the output verbatim to the receiving LLM session or downstream skill.
You do not need to reformat or summarize it — the format is designed to be
consumed directly. When handing off to another skill, prepend the block with:

> "Use the following REDCap project context to complete the task. All field
> names, choice codes, and event names in this context are the exact strings
> used in REDCap expressions."

---

## What the Codebook Shows (vs. What It Doesn't)

Per RC-FD-05, the Codebook includes:

- Variable names, labels, field types
- Choices with coded values and labels (use codes in branching logic expressions)
- Validation type and min/max range
- Calculation formulas for calc fields
- Branching logic conditions
- Action tag annotations (verbatim)
- Required and Identifier flags
- Section headers and field notes
- **[PDF only]** Unique event names for each event in longitudinal projects
- **[PDF only]** Which instruments are assigned to which events
- **[PDF only]** Which instruments/events are configured as repeating
- **Auto-generated `_complete` fields** (see below)

The Codebook does NOT include (configure separately in REDCap):
- Survey settings (queue, auto-continue, theme)
- User rights and Data Access Groups
- Randomization setup
- Alerts and notifications
- Data Quality rules
- Reports

---

## Auto-Generated `_complete` Fields

Every REDCap instrument automatically has a system-generated completion
status field. Its variable name follows the pattern `{form_name}_complete`
(e.g., `application_complete`, `review_1_complete`). This field is a
dropdown with three fixed choices:

| Code | Label |
|------|-------|
| `0` | Incomplete |
| `1` | Unverified |
| `2` | Complete |

**Where it appears:**

| Location | Present? |
|----------|----------|
| Codebook PDF | ✓ Yes — appears as the final field in each instrument section |
| Data exports (CSV, R, SPSS, etc.) | ✓ Yes |
| Codebook web view | ✓ Yes |
| Data Dictionary CSV | ✗ No — auto-generated fields are excluded |
| Data Dictionary upload | ✗ No — cannot be added, modified, or removed |

**Implication for field counts:** The Codebook PDF will always have
exactly one more field per instrument than the Data Dictionary CSV.
For a project with N instruments, the Codebook PDF has N extra fields.
This is expected — not a discrepancy.

**The script skips `_complete` fields** by default when parsing a
Codebook PDF, so that PDF and CSV field counts align and the output
focuses on user-designed fields. If you need completion status
information in downstream work, reference the field by its variable
name `{form_name}_complete` — it is always present in data exports
and can be used in branching logic and calculated fields.

**Using `_complete` in expressions:**

```
# Show a field only if a prior form is marked Complete
[intake_complete] = '2'

# Calc that counts how many forms are complete
if([form_a_complete]='2', 1, 0) + if([form_b_complete]='2', 1, 0)
```

---

## Important REDCap Syntax Notes

These frequently come up when using codebook output for downstream work:

- **Checkbox expression syntax:** The Codebook shows `fieldname___code` as the
  subvariable name (used in exports), but REDCap expressions must use
  `[fieldname(code)]` — e.g., `[race(3)] = '1'`. Never use the triple-underscore
  form in branching logic or calc fields.

- **Choice codes vs. labels:** The Codebook shows both. In branching logic,
  always use the numeric code, not the label. E.g., `[sex] = '1'` not
  `[sex] = 'Female'`.

- **Event names in expressions:** Longitudinal cross-event references use the
  unique event name from the Events table: `[baseline_arm_1][weight]`. The
  display name ("Baseline") is not used in expressions.

- **Piped labels:** In longitudinal projects, some field labels use piping
  syntax like `[event][field]`. The Codebook shows the raw syntax — it
  does not resolve piped values. This is expected behavior.

---

## Common Scenarios

**User uploads a DD CSV and asks "what does this project collect?"**
→ Run `--summary` on the CSV. Note at the end that event info is not
available and recommend the Codebook PDF if the project is longitudinal.

**User uploads a Codebook PDF for a longitudinal project:**
→ Run both `--summary` and `--llm-context`. Present the summary to the user
and keep the LLM context ready if a follow-up task needs it (e.g., building
branching logic for a specific instrument).

**Another skill (e.g., redcap-syntax-builder) needs project context:**
→ Run `--llm-context` and pass the output verbatim as context to that skill.

**User says "I need to describe this project for an IRB submission":**
→ Run `--summary`, then offer to produce a more detailed Word document
using the docx skill with the summary as source content.

**User says "I need to share this project structure with a developer":**
→ Run `--llm-context`. The structured format is easy for developers and
LLMs to parse. Offer to wrap it in a Word doc if they need a formal deliverable.

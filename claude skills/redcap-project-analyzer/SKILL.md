---
name: redcap-project-analyzer
description: >
  Read-only design audit of a live REDCap project, pulled through the REDCap MCP connectors
  (one connector per REDCap server). Flags design issues, broken
  branching logic, calc-field chains, structural antipatterns and style-convention gaps, and writes
  a structured markdown report. Use whenever the user wants to audit, review, health-check, or
  assess the structure and configuration of an existing project on a REDCap server. Trigger on:
  "analyze my REDCap project", "audit PID 12345", "review the project design", "check for issues
  in my REDCap project", "is my project structured correctly", "project health check", "look at
  my REDCap project", "can you review how this project is set up", "something seems wrong with my
  project structure". Only calls metadata export tools — never imports, deletes, or exports
  records, reports, logging, or survey participants. Do NOT use for data dictionary CSV files or
  longitudinal CSV files on disk (use the redcap-dd-* / redcap-data-dictionary and
  redcap-longitudinal-* skills), for building or fixing a project, or for anything that changes
  a project.
---

# REDCap Project Analyzer

> **REDCap connectors:** before calling any REDCap MCP tool from this skill, read `references/CONNECTOR-RULES.md` (bundled with this skill; the source copy is `claude skills/CONNECTOR-RULES.md` in the REDCap_KB_RAG repo) and follow it — confirm the connector and PID, flag production, stay read-only unless the user explicitly confirms a write on a non-production connector, and never expose the API token.

This skill reads a REDCap project's design through the REDCap MCP connector tools and produces a
structured analysis report flagging design issues, logic errors, and structural antipatterns.
Work through the steps below in order. The confirmation in Steps 1–2 is important — don't skip
ahead to pulling data.

---

## Read-only rule (applies to every step)

This is a design audit. It never changes a project and never needs participant data. The **only**
tools you may call are these, on the confirmed connector (`mcp__<connector>__<tool>`):

- `check_connection`
- `export_redcap_version`
- `export_project_info`
- `export_metadata`
- `export_instruments`
- `export_field_names`
- `export_arms`
- `export_events`
- `export_instrument_event_mappings`
- `export_repeating_instruments_events`

This list is exhaustive. Never call any `import_*`, `delete_*`, `rename_record`,
`randomize_record`, `switch_dag`, `create_file_repository_folder`, or `generate_next_record_name`
tool. Also never call `export_records`, `export_report`, `export_logging`, `export_pdf`,
`export_project_xml`, `export_file_*`, `export_survey_*`, or user/DAG exports — they return
participant or user data that a design audit does not need. If a check would require one of
these, skip it and note the limitation in the report.

Do not fall back to raw HTTP (Python `requests`, `curl`) to reach the API. The MCP connector
tools are the only method.

---

## Step 1: Identify the connector and the project

Each REDCap server has its own connector. Which connectors exist, which are production, and where
their API URLs are recorded is institution-specific and lives in the local connector map, `~/.claude/redcap-connectors.md`
(see `CONNECTOR-RULES.md`). Read it before asking, and use the URL from there rather than from memory.

Always ask the user which server and which project (PID or title) they mean — even if it seems
obvious from context. Then state back, before any tool call:

> "I'll use the **`<connector>`** connector → `https://<your-redcap-server>/api/`
> for **PID 12345**. ⚠️ This is a **production** server with live data — I'll only read the
> project design (metadata), never records or participant data. OK to proceed?"

Include the ⚠️ production line whenever the connector map marks the connector as production.
Wait for the user to confirm.

### API token

Each connector may have a default token configured. Try the connector's default first (call the
tools with no `token` argument). If there is no default, or the default belongs to a different
project, ask the user for the project's API token and explain where to find it:

> "To get your API token:
> 1. Open your REDCap project
> 2. In the left sidebar, look for **API** under the Applications section
> 3. If you see a token already listed there, copy it
> 4. If not, click **Generate Token** — if that option isn't visible, you may need to ask your
>    REDCap administrator to grant you API access for this project
>
> The token is a 32-character string tied to your account and this one project."

Token handling rules:

- Pass the token **only** as the tool's `token` argument.
- Never echo it back, quote it, or include it in a summary.
- Never write it to a file, script, report, or memory.

---

## Step 2: Confirm the connection and the right project

Call `check_connection` first. If it fails, stop and help the user fix it (wrong connector,
missing/invalid token, or no API rights on the project) before continuing.

Then call `export_redcap_version` and `export_project_info`. From project info, note
`project_id`, `project_title`, `is_longitudinal`, `surveys_enabled`,
`record_autonumbering_enabled`, `has_repeating_instruments_or_events`, `in_production`, and
`purpose`.

Show the user the **project title and PID** and ask: *"Is this the right project?"* Do not pull
further data until they confirm. If the PID doesn't match what they asked for, the token belongs
to a different project — stop and get the right token.

---

## Step 3: Pull the project design

Once confirmed, call these on the same connector (in parallel where possible):

- `export_metadata` (full data dictionary — no `fields`/`forms` filter)
- `export_instruments`
- If `is_longitudinal = 1`: `export_arms`, `export_events`, `export_instrument_event_mappings`
- If `has_repeating_instruments_or_events = 1`: `export_repeating_instruments_events`

Keep the results in context for the analysis; do not write them to disk. Always keep the exact
`export_redcap_version` string for the report.

Confirm counts to the user ("I pulled N fields across N forms") so they can sanity-check before
the analysis.

---

## Step 4: Analyze the project

Run each check below. Collect all findings before writing the report. Flag severity clearly:

- 🔴 **Critical** — Will cause broken behavior or data problems (fix these first)
- 🟡 **Warning** — Suboptimal design that may cause confusion or maintenance issues
- 🔵 **Suggestion** — A better REDCap feature exists for this pattern

### Parsing field references (used by 4b and 4c)

To extract field references from branching logic or calc formulas:

1. Find every bracketed token `[...]`.
2. Strip any `(code)` suffix inside the brackets, so a checkbox reference `[symptoms(3)]` counts
   as field `symptoms`. (Also strip instance/smart-variable suffixes such as `[field][1]` or
   `:value`-style modifiers where present.)
3. A bracketed token is an **event prefix**, not a field, when it is immediately followed by
   another `[...]` (e.g. `[baseline_arm_1][weight]`) **and** it matches a unique event name from
   `export_events`. Treat the second token as the field.
4. Skip Smart Variables (`[event-name]`, `[record-id]`, `[current-instance]`, etc. — tokens
   containing a hyphen) and anything that isn't a valid variable name.

Cross-reference the remaining names against the field list from `export_metadata`.

### 4a. Structural pattern checks

**Numbered/versioned forms instead of longitudinal design**
Look at instrument variable names and labels. Patterns like `visit_1_form`, `visit_2_form` or
`baseline_form`, `month_3_form`, `month_6_form` in a non-longitudinal project strongly suggest the
project should use longitudinal events instead. Two or more such forms = 🟡 Warning.

**Language-specific forms instead of Multi-Language Management (MLM)**
Instrument names containing language codes or suffixes — `consent_en`, `consent_fr`, `form_spanish`,
`questionnaire_dutch` — suggest the team duplicated forms for translation. REDCap's MLM feature
handles this in a single form. Two or more such pairs = 🟡 Warning.

**Numbered field series instead of a repeating instrument**
Within a single form, a run of fields like `medication_1_name`, `medication_2_name`,
`medication_3_name` (or `adverse_event_1`, `adverse_event_2`...) is better modeled as a repeating
instrument. Three or more fields in such a series = 🟡 Warning.

**Classic project that looks longitudinal**
If the project is NOT longitudinal but has 4+ instruments whose names clearly represent time points
(e.g., screening, baseline, week4, week8, month6, followup) — flag as 🔵 Suggestion to enable
longitudinal mode and collapse these into events.

**Duplicate instruments (copies of the same form)**
Instruments with nearly identical names (e.g., `demographics` and `demographics_copy`,
`baseline_survey` and `baseline_survey_v2`) suggest version management by duplication rather than
using Data Dictionary versioning or project XML export. Flag as 🟡 Warning.

### 4b. Field-level checks

**Calculated fields referencing other calculated fields**
Build a dependency graph: for each `calc` field, parse its formula using the reference rules
above. If any referenced field is itself a `calc` type, that's a chain. Chains of depth 3+
= 🟡 Warning (REDCap recalculates in field order, so deep chains can produce stale values).

**Text fields with date/time semantics but no validation**
Fields whose variable name or label contains "date", "dob", "time", "datetime" that have
`field_type = text` and `text_validation_type_or_show_slider_number` is blank = 🟡 Warning.

**Very large forms**
Any single instrument with more than 100 fields = 🔵 Suggestion to split into sub-forms.

**Fields with empty or very short labels**
`field_label` that is empty, blank, or under 4 characters (excluding `record_id` and descriptive
fields used as spacers) = 🔵 Suggestion.

**Missing field notes where they'd help**
Text and number fields in a project with `surveys_enabled = 1` that have no `field_note` and no
validation — users filling out surveys may not know the expected format. Flag forms with 5+ such
fields as 🔵 Suggestion. (The API does not say which instruments are surveys, so word this as
"if this form is used as a survey".)

### 4c. Branching logic checks

This is the highest-value analysis. Parse branching logic carefully.

**References to non-existent fields**
Extract field references from every branching logic expression using the parsing rules above
(checkbox `(code)` suffixes stripped, event prefixes set aside). Any reference to a field that
doesn't exist in the project = 🔴 Critical. Report the offending field and the bad reference.

**References to non-existent events (longitudinal only)**
In longitudinal projects, branching logic can reference events as `[event_name][field_name]`.
For any bracketed token that is immediately followed by another `[...]` but does **not** match an
event name from `export_events` (and isn't a field or Smart Variable) = 🔴 Critical.

**Logic checking for impossible choice values**
For radio, dropdown, and checkbox fields, extract the `select_choices_or_calculations` values.
Then scan branching logic for patterns like `[field_name] = 'value'` or `[field_name](value)`.
If a comparison value doesn't appear in that field's choice list, it can never be true = 🟡 Warning.
Include the field name and the impossible value in the report.

**Circular branching logic**
If Field A's logic references Field B, and Field B's logic references Field A (or any cycle) =
🔴 Critical.

### 4d. Project configuration checks

**Record autonumbering off in a longitudinal project**
`is_longitudinal = 1` and `record_autonumbering_enabled = 0` = 🔵 Suggestion (manual record IDs
are error-prone in multi-site longitudinal studies).

**Surveys enabled**
`surveys_enabled` comes from `export_project_info`, but none of the allowed tools reports which
instruments are enabled as surveys, so don't flag "surveys enabled but no survey instrument".
Just report Surveys: Yes/No in the header.

**Project purpose**
Report `purpose` with its label (and `purpose_other` if present) in the project-structure table.
Codes (as stored in the `redcap_projects` table):

| `purpose` | Label | | `status` | Label |
|---|---|---|---|---|
| 0 | Practice / Just for fun | | 0 | Development |
| 1 | Other | | 1 | Production |
| 2 | Research | | 2 | Inactive |
| 3 | Quality Improvement | | 3 | Archived |
| 4 | Operational Support | | | |

Purpose 0 (Practice) is not an error on its own. Flag it as **Low** only if the project is in
Production (`status = 1`) — a practice project collecting real data usually has the wrong purpose
set, which matters for reporting. If `purpose = 2` (Research), note whether PI and IRB fields are filled in
when `export_project_info` returns them.

**No data validation on any text field in a large project**
If the project has 20+ text fields and none have `text_validation_type_or_show_slider_number` set
= 🔵 Suggestion to add validation for data quality.

### 4e. Style convention checks

Read `kb/RC-DSGN-01_REDCap-Project-Design-Best-Practices.md` in the REDCap_KB_RAG repo before running these checks — it is the authoritative
source for each rule. These are detectable from the data dictionary export.

**Notes fields with wrong alignment (RC-DSGN-01 §2.1)**
For every `notes` field, check `custom_alignment`. If it is blank (defaults to `RV`) or set to
`RH` or `RV`, the text area will render at half-width — cramped and hard to type in. The correct
values are `LH` or `LV`. Flag each offending field as 🔵 Suggestion with the field variable name,
its instrument, and a note that the fix is a one-field change in the Online Designer.

**"Other (specify)" fields without branching logic (RC-DSGN-01 §5.4)**
Scan for free-text (`text` or `notes`) fields whose variable name contains `_other`, `_specify`,
`_oth`, or `_other_specify`. For each match, check whether `branching_logic` is populated. If
the field has no branching logic, it is unconditionally visible — a blank value there is
ambiguous (not applicable vs. overlooked). Flag as 🟡 Warning. Report the field name and suggest
adding branching logic that shows it only when the parent radio/dropdown's "Other" choice is
selected.

**Required fields that are conditionally relevant (RC-DSGN-01 §5.5)**
For every field where `required_field = 'y'` AND `branching_logic` is populated: check whether
the branching condition is simple (one field, one value) or complex (multiple conditions). Simple
cases may be intentional; flag complex cases where the required field only applies under a narrow
condition, and any required field whose logic references another required field that itself has
branching logic — these are the ones most likely to block form submission unexpectedly. Report as
🟡 Warning with the field name and its branching expression.

**Repeating instruments without a custom form label (RC-DSGN-01 §6.1)**
If the project uses repeating instruments (check `export_repeating_instruments_events`), verify
whether a custom form label is configured. A blank label means each instance shows only as
"Instance 1", "Instance 2", etc. in the record status dashboard — making it hard to navigate
when a record has many instances. Flag missing labels as 🔵 Suggestion, and note that the label
is configured in Project Setup → Repeating Instruments (not in the Online Designer).

---

## Step 5: Generate the report

Produce a structured markdown report. Use the template below exactly. Save it as a `.md` file
in a folder the user names (default: the current working folder) and tell them the full file path.

```
# REDCap Project Analysis Report

**Project:** [title] (PID [project_id])
**REDCap Version:** [exact version string from export_redcap_version — never guess or approximate]
**Server:** [connector name] — [API URL from the connector map, no token] [⚠️ Production, if applicable]
**Analyzed:** [today's date]
**Project type:** [Classic / Longitudinal] | Surveys: [Yes/No] | Repeating instruments: [Yes/No] | Status: [Development / Production]

---

## Summary

[2–4 sentence plain-English overview: what the project appears to collect, its scale, and the
most important findings. E.g.: "This is a longitudinal oncology study with 4 arms and 18 events,
collecting data across 312 fields in 14 instruments. The analysis found 2 critical issues (broken
branching logic references) and 5 warnings, the most important of which is a pattern of language-
duplicated forms that would benefit from MLM migration."]

---

## Project Structure

| Item | Count / Value |
|------|--------------|
| Instruments (forms) | N |
| Total fields | N |
| — Calculated fields | N |
| — Text fields | N |
| — Radio/dropdown/checkbox | N |
| — Descriptive fields | N |
| Arms | N (longitudinal only) |
| Events | N (longitudinal only) |
| Repeating instruments | [names] or None |
| Purpose | [code — label] |

---

## Issues Found

### 🔴 Critical Issues (N)

> These should be fixed before the project goes into production or before new data collection begins.

**[Issue title]** — [Form or field name]
[Plain explanation of the problem and why it matters. Be specific: include the field name, the
bad value, or the exact logic that's broken.]

*(repeat for each critical issue)*

---

### 🟡 Warnings (N)

> These won't break the project but represent design decisions that may cause problems or extra
> work over time.

**[Issue title]** — [Form or field name]
[Explanation. Reference the specific fields or forms involved. Mention the better REDCap feature
where applicable.]

*(repeat for each warning)*

---

### 🔵 Suggestions (N)

> Lower priority. These are patterns where a different REDCap approach would make the project
> easier to maintain.

**[Issue title]** — [Form or field name]
[Brief explanation. Keep these concise.]

*(repeat for each suggestion)*

---

## Top Recommendations

[Numbered list of the 3–5 most impactful things to address, in priority order. Write for the
project team, not just the REDCap admin — explain the user impact, not just the technical fix.]

1. [Most critical thing]
2. [Second priority]
...

---

## Limitations

[Checks skipped or only partly possible through the read-only API — e.g. which instruments are
surveys, complex expressions needing runtime evaluation.]
```

---

## Important reminders

- **Read-only.** Only the tools in the read-only rule above. No exceptions, even if the user asks
  for a quick fix mid-audit — point them to the Online Designer or the redcap-dd-fixer skill.
- **Never include the API token in the report, in chat, or in any saved file.** The report only
  names the connector and API URL.
- Branching logic analysis is best-effort: complex expressions with `datediff()`, `sum()`,
  `if()`, or event-scoped references require runtime evaluation to fully validate. Flag what you
  can and note limitations.
- If the project has very few fields or is clearly brand-new, say so in the summary and note that
  there's less to analyze — don't pad the report with non-issues.
- Use judgment about what matters: a project with 10 fields and 1 form doesn't need the same
  scrutiny as a 300-field longitudinal study.
- For MLM suggestions: search for RC-MLM-01 in the KB for context on how MLM works and its limitations before recommending it.

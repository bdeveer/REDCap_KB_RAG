---
name: redcap-project-analyzer
description: >
  Analyze a REDCap project for design issues, logic errors, and structural problems by connecting
  to the REDCap API. Use this skill whenever the user wants to audit, review, health-check, or
  assess a REDCap project's structure and configuration. Trigger on: "analyze my REDCap project",
  "audit this project", "review the project design", "check for issues in my REDCap project",
  "is my project structured correctly", "project health check", "look at my REDCap project",
  "can you review how this project is set up", "something seems wrong with my project structure",
  or any time the user wants an automated review of a REDCap project through the API. Walks the
  user step by step through obtaining an API token if they don't have one, confirms the correct
  REDCap instance before pulling data, and produces a structured report of findings.
---

# REDCap Project Analyzer

This skill connects to a REDCap project via API and produces a structured analysis report flagging
design issues, logic errors, and structural antipatterns. Work through the steps below in order.
The interactive setup in Steps 1–2 is important — don't skip ahead to pulling data.

---

## Step 1: Explain what you need and why

Before asking for any credentials, explain what the analysis involves in plain terms. Something like:

> "To analyze your project I need to connect to it using the **REDCap API** — a way for programs
> to read project data directly. For this I need two things:
>
> **1. Your REDCap URL** — the base web address of your REDCap server, for example:
> `https://redcap.yourorganization.edu`
> (Just the hostname — not the full URL of a specific page)
>
> **2. An API token** — a 32-character string that acts as your personal key to this specific
> project. It's tied to both your user account and the project, so a token from one project won't
> work on another, and someone else's token won't give you access to your project."

Then explain how to get the token:

> "To get your API token:
> 1. Open your REDCap project
> 2. In the left sidebar, look for **API** under the Applications section
> 3. If you see a token already listed there, copy it
> 4. If not, click **Generate Token** — if that option isn't visible, you may need to ask your
>    REDCap administrator to grant you API access for this project
>
> The token looks like: `A1B2C3D4E5F6A1B2C3D4E5F6A1B2C3D4`
>
> You can share it here — I'll use it only for this session and won't store it anywhere."

Ask the user to provide both the URL and the token. Wait for their reply before doing anything else.

---

## Step 2: Confirm the connection and the right project

Once the user provides the URL and token, verify the connection immediately using Python. The goal
is to confirm (a) the credentials work and (b) this is the project the user intended.

> **Cowork/sandbox note:** The bash sandbox cannot make outbound HTTPS requests to external
> servers — attempts will fail with a proxy 403 error. In Cowork sessions, **always use the
> MCP tools** (`mcp__redcap-prod__*`, `mcp__redcap-test__*`, `mcp__redcap-dev__*`) instead of
> Python `requests`. Every MCP tool accepts a `token` parameter that overrides its default,
> so you can pass the user's token directly. The Python scripts in Steps 2–3 are reference
> implementations for non-Cowork environments (Claude Code, API) where direct HTTP works.

```python
import requests, json, sys

url = "https://YOUR_REDCAP_URL/api/"   # replace with user's URL, ensure /api/ suffix
token = "USER_TOKEN"

# Step 1: Get REDCap version
r = requests.post(url, data={"token": token, "content": "version"})
if r.status_code != 200 or not r.text.strip():
    print(f"ERROR {r.status_code}: Could not connect. Response: {r.text[:200]}")
    sys.exit(1)
version = r.text.strip()
print(f"Connected to REDCap v{version}")

# Step 2: Get project info
r2 = requests.post(url, data={
    "token": token, "content": "project",
    "format": "json", "returnFormat": "json"
})
proj = json.loads(r2.text)
print(json.dumps({
    "project_id": proj.get("project_id"),
    "project_title": proj.get("project_title"),
    "is_longitudinal": proj.get("is_longitudinal"),
    "surveys_enabled": proj.get("surveys_enabled"),
    "record_autonumbering_enabled": proj.get("record_autonumbering_enabled"),
    "has_repeating_instruments_or_events": proj.get("has_repeating_instruments_or_events"),
    "in_production": proj.get("in_production"),
    "purpose": proj.get("purpose"),
}, indent=2))
```

Show the user the **project title and PID** and ask: *"Is this the right project?"* Do not pull
further data until they confirm. If the URL is missing `/api/`, the token is wrong (403 error), or
the project doesn't match, stop and help them correct it before continuing.

**If the user's project is one of the already-connected MCP instances** (redcap-dev, redcap-prod,
or redcap-test), you can use those MCP tools directly instead of raw HTTP — they're already
authenticated. Ask which instance they mean if it's ambiguous.

---

## Step 3: Pull all project data

Once confirmed, gather everything needed for analysis. In Cowork, call the MCP tools in parallel
(export_redcap_version, export_project_info, export_metadata, export_instruments, and conditionally
export_arms, export_events, export_instrument_event_mappings,
export_repeating_instruments_events) — each accepts the user's `token` parameter directly.
Always call `export_redcap_version` so the exact version string goes into the report. In other
environments, use the Python script below which writes results to temp JSON files for the
analysis step.

```python
import requests, json, os

url = "https://YOUR_REDCAP_URL/api/"
token = "USER_TOKEN"
OUT = "/tmp/rc_analysis/"
os.makedirs(OUT, exist_ok=True)

def call(content, extra=None):
    params = {"token": token, "content": content, "format": "json", "returnFormat": "json"}
    if extra:
        params.update(extra)
    r = requests.post(url, data=params)
    try:
        return json.loads(r.text)
    except:
        return r.text

proj = call("project")
metadata = call("metadata")
instruments = call("instrument")
arms = call("arm") if proj.get("is_longitudinal") == 1 else []
events = call("event") if proj.get("is_longitudinal") == 1 else []
mappings = call("formEventMapping") if proj.get("is_longitudinal") == 1 else []
repeating = call("repeatingInstrumentsAndEvents") if proj.get("has_repeating_instruments_or_events") == 1 else []

for name, data in [
    ("project", proj), ("metadata", metadata), ("instruments", instruments),
    ("arms", arms), ("events", events), ("mappings", mappings), ("repeating", repeating)
]:
    with open(f"{OUT}{name}.json", "w") as f:
        json.dump(data, f, indent=2)

print(f"Pulled {len(metadata)} fields across {len(instruments)} instruments")
```

Confirm counts to the user ("I pulled N fields across N forms") so they can sanity-check before
the analysis.

---

## Step 4: Analyze the project

Run each check below. Collect all findings before writing the report. Flag severity clearly:

- 🔴 **Critical** — Will cause broken behavior or data problems (fix these first)
- 🟡 **Warning** — Suboptimal design that may cause confusion or maintenance issues
- 🔵 **Suggestion** — A better REDCap feature exists for this pattern

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
Build a dependency graph: for each `calc` field, parse its formula and extract `[field_name]`
references. If any referenced field is itself a `calc` type, that's a chain. Chains of depth 3+
= 🟡 Warning (REDCap recalculates in field order, so deep chains can produce stale values).

**Text fields with date/time semantics but no validation**
Fields whose variable name or label contains "date", "dob", "time", "datetime" that have
`field_type = text` and `text_validation_type_or_show_slider_number` is blank = 🟡 Warning.

**Required fields that are hidden by branching logic**
A field that is `required_field = 'y'` AND has branching logic. This isn't always wrong, but flag
any required field whose branching logic references *another required field that itself has branching
logic* — nested required+branching chains are a common source of "can't submit the form" bugs.
Flag as 🟡 Warning with the specific field names.

**Very large forms**
Any single instrument with more than 100 fields = 🔵 Suggestion to split into sub-forms.

**Fields with empty or very short labels**
`field_label` that is empty, blank, or under 4 characters (excluding `record_id` and descriptive
fields used as spacers) = 🔵 Suggestion.

**Missing field notes where they'd help**
Text and number fields in a survey-enabled project with no `field_note` and no validation — users
filling out surveys may not know the expected format. Flag forms with 5+ such fields as 🔵 Suggestion.

### 4c. Branching logic checks

This is the highest-value analysis. Parse branching logic carefully.

**References to non-existent fields**
Extract all `[field_name]` patterns from every branching logic expression (use regex
`\[([a-z_][a-z0-9_]*)\]`, excluding event-qualified references for now). Cross-reference against
the complete field list from the data dictionary. Any reference to a field that doesn't exist in
the project = 🔴 Critical. Report the offending field and the bad reference.

**References to non-existent events (longitudinal only)**
In longitudinal projects, branching logic can reference events as `[event_name][field_name]`.
Extract event names from these references and check against the actual event list. Missing event
= 🔴 Critical.

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

**Surveys enabled but no instrument configured as a survey**
`surveys_enabled = 1` in project info but no survey participants visible or no survey-designated
instrument in the instrument list = 🟡 Warning.

**Project in production with no description/purpose set**
`in_production = 1` and `purpose = 0` (not set) = 🔵 Suggestion (good practice for IRB and audit).

**No data validation on any text field in a large project**
If the project has 20+ text fields and none have `text_validation_type_or_show_slider_number` set
= 🔵 Suggestion to add validation for data quality.

---

## Step 5: Generate the report

Produce a structured markdown report. Use the template below exactly. Save it as a `.md` file
in the user's workspace folder and provide a download link.

```
# REDCap Project Analysis Report

**Project:** [title] (PID [project_id])
**REDCap Version:** [exact version string from export_redcap_version API call — never guess or approximate]
**REDCap URL:** [base URL, no token]
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
```

---

## Important reminders

- **Never include the API token in the report or in any saved file.** The report should only
  reference the REDCap URL (without the token).
- Branching logic analysis is best-effort: complex expressions with `datediff()`, `sum()`,
  `if()`, or event-scoped references require runtime evaluation to fully validate. Flag what you
  can and note limitations.
- If the project has very few fields or is clearly brand-new, say so in the summary and note that
  there's less to analyze — don't pad the report with non-issues.
- Use judgment about what matters: a project with 10 fields and 1 form doesn't need the same
  scrutiny as a 300-field longitudinal study.
- For MLM suggestions: check the KB article RC-UNCLASSIFIED-01 or search for MLM in the KB for
  context on how MLM works and its limitations before recommending it.

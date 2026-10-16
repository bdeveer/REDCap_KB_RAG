---
name: redcap-longitudinal-builder
description: |
  Build the three REDCap longitudinal project CSV files — Arms, Events, and Instrument
  Designations — from user input or uploaded documentation. Use this skill whenever a
  user wants to set up or draft a longitudinal project structure, is starting a new
  longitudinal REDCap project, wants to generate importable CSV files, or describes a
  study schedule and needs it turned into importable CSVs. Trigger on: "create my events",
  "set up the longitudinal structure", "generate the arms and events", "build the event
  mapping", "import longitudinal setup", "I have a protocol and need the event CSVs",
  "help me design the longitudinal structure", or any time the user describes study
  timepoints, visit schedules, arms, or form assignments and wants files to import.
  Also trigger when a user shares a protocol document, schedule table, or spreadsheet
  and asks to turn it into a REDCap longitudinal setup. Do NOT use for reading,
  summarizing, or explaining an existing project's arms/events/mappings (use
  redcap-longitudinal-structure for that) — use this one only when building new structure.
---

# REDCap Longitudinal Builder Skill

> **REDCap connectors:** before calling any REDCap MCP tool from this skill, read `references/CONNECTOR-RULES.md` (bundled with this skill; the source copy is `claude skills/CONNECTOR-RULES.md` in the REDCap_KB_RAG repo) and follow it — confirm the connector and PID, flag production, stay read-only unless the user explicitly confirms a write on a non-production connector, and never expose the API token.

This skill guides you through collecting the information needed to generate the three
REDCap longitudinal project CSV files, then produces them ready for import.

---

## What You're Building

Three CSV files define a REDCap longitudinal project's structure:

| File | Purpose | UI upload location |
|------|---------|-------------------|
| **Arms** | Study arms (parallel groups or sequential phases) | Project Setup → Define My Events → Upload or download arms/events |
| **Events** | Timepoints within each arm | Project Setup → Define My Events → Upload or download arms/events |
| **Instrument Designations** | Which forms are collected at which events | Project Setup → Designate Instruments for My Events → Upload or download instrument mappings |

All three files can be uploaded directly through the REDCap UI — no API access required.
The REDCap API (`action=import`) is an alternative for programmatic or scripted workflows.
Generating these files ahead of time saves significant manual data entry, especially for
complex multi-arm studies.

> **Upload order matters:** Always upload in this sequence: **Arms → Events → Instrument
> Designations**. Events reference arm numbers, and designations reference unique event
> names — so each layer must exist before the next can be imported.

> **Additive vs. replace:** Arms and events uploads are additive (existing rows are
> untouched). The instrument-event designations upload replaces the full mapping — any
> combination not in the file will be unchecked. Always start from a downloaded copy of
> the existing mapping rather than building from scratch if the project already has data.

---

## Step 1: Identify the Input Source

The user may provide design information in two ways:

### A) Documentation (protocol, schedule table, Word doc, spreadsheet)

If the user has uploaded a document, read it carefully and extract:
- Study arm names and count
- Event/visit names and their scheduled days
- Visit windows (acceptable day ranges per event)
- Which forms/instruments are used and at which visits

Look for tables like "Schedule of Events", "Study Visits", or "Assessments by Visit".
Clinical trials often have a Standard of Assessment (SoA) table — this is exactly what
you need.

After extracting, **always confirm your interpretation with the user** before generating
files. Misreading a protocol table is easy and the user knows their study best.

### B) Conversation

If the user hasn't uploaded anything, ask them for the following information
**in a single conversational turn** — don't fire off one question at a time.
Present a structured prompt like:

> To build your longitudinal project files, I need:
> 1. **Arms**: How many study arms? What are they called? (e.g. Treatment / Control,
>    or just a single arm like "Cohort A")
> 2. **Events**: For each arm, list the visits/timepoints in order:
>    - Visit name (e.g. Screening, Baseline, Week 4, Month 6, End of Study)
>    - Scheduled day from arm start (Day 0 = first visit)
>    - Acceptable visit window in days (e.g. ±7 days, or leave blank if none)
> 3. **Forms**: List your instrument/form names and which visits they're collected at.
>    (If you haven't finalized form names yet, use placeholders — you can update the
>    mapping later.)

If the user gives you partial information, ask only the missing pieces.

---

## Step 2: Clarify Ambiguities Before Building

Before generating, resolve these common ambiguities:

**Classic mode vs. longitudinal mode — confirm longitudinal is the right choice**
Per the REDCap Project Design Best Practices (`kb/RC-DSGN-01_REDCap-Project-Design-Best-Practices.md` in the REDCap_KB_RAG repo, Section 3.1), longitudinal mode
should only be used when at least one of the following is true:
- The same instrument is completed by the same participant at more than one time point, OR
- The project needs multiple arms, event-based branching logic, or scheduling windows

If the user describes a project where each form is completed exactly once per participant —
even if there are many forms — that is a classic project, not a longitudinal one. Classic mode
achieves the same result with less configuration overhead. Flag this before building:

> "Just to confirm: does each participant complete any of these forms more than once, or are
> all forms completed exactly once? If every form is only ever completed once per participant,
> a classic (non-longitudinal) REDCap project would be simpler to configure and avoids
> unnecessary event setup and a more confusing record status dashboard."

If the user confirms forms repeat across timepoints, or they have multiple arms, or they have a
specific architectural reason to use longitudinal mode — proceed with the build. If they confirm
everything is single-instance, redirect them to the `redcap-dd-builder` skill instead.

**Single arm vs. multi-arm**: A longitudinal project can have just one arm. If the user
describes a single cohort with multiple visits, that's one arm. If they describe parallel
groups, treatment vs. control, or different study phases with different event schedules,
that's multiple arms.

**Shared vs. arm-specific events**: In multi-arm projects, "Baseline" in Arm 1 and
"Baseline" in Arm 2 are *separate events* with different `unique_event_name` values
(`baseline_arm_1`, `baseline_arm_2`). Clarify whether the same event schedule applies
to all arms or differs by arm.

**Visit windows**: Not all projects use visit windows. `offset_min` and `offset_max` are
window **widths in days** before/after `day_offset` (positive numbers, RC-LONG-01), not
absolute days. No window = leave them out (default `0`). "±7 days" = `offset_min: 7,
offset_max: 7`; "-3/+14 days" = `offset_min: 3, offset_max: 14`.

**Form names**: These must match the variable names in the data dictionary exactly
(lowercase, underscores). If the user gives you human-readable names like "Demographics
Form", convert them to likely variable names (`demographics`) and confirm.

**Day 0**: Clarify which visit is Day 0 if the user uses relative days. Usually
Screening or Baseline is Day 0.

**Same-day events and display order**: If multiple events fall on the same day
(common in studies where events are sequential steps rather than time-separated
visits — e.g. Screening → Consent → Baseline → Randomization all on Day 0), ask
the user what order they want to see them displayed in REDCap. Then assign
sequential `day_offset` values starting from 0 (0, 1, 2, 3…) to enforce that order.
Do not leave all events at `day_offset=0` unless alphabetical ordering by event name
happens to be correct — it usually isn't.

---

## Step 3: Build the Specification

Once you have all the information, construct the project spec as a Python dict or JSON
structure to pass to the generator script. The format:

```json
{
  "arms": [
    {"arm_num": 1, "name": "Treatment"},
    {"arm_num": 2, "name": "Control"}
  ],
  "events": [
    {
      "event_name": "Baseline",
      "arm_num": 1,
      "day_offset": 0,
      "offset_min": 0,
      "offset_max": 0
    },
    {
      "event_name": "Month 3",
      "arm_num": 1,
      "day_offset": 90,
      "offset_min": 7,
      "offset_max": 7,
      "custom_event_label": ""
    }
  ],
  "mapping": [
    {"event_name": "Baseline", "arm_num": 1, "form": "demographics"},
    {"event_name": "Month 3",  "arm_num": 1, "form": "labs"}
  ]
}
```

**Spec keys are strict:** the only top-level keys are `arms`, `events`, and `mapping`
(singular). Any other key — e.g. `"mappings"` — is an error and nothing is generated, so
a misnamed key can never silently drop `InstrumentDesignations.csv`. If `mapping` is
missing or empty the script warns loudly and writes only Arms/Events. Arms accept `name`
(the Arms CSV column) or `arm_name`. Mapping rows reference an event by `event_name` +
`arm_num` (preferred) or by its expected `unique_event_name`; rows matching no event are
skipped with a warning. `custom_event_label` is optional (piped label, e.g. `[visit_date]`).

**Note on `unique_event_name`**: Do not set it on events. `Events.csv` leaves the
`unique_event_name` column **blank** so REDCap generates it on import (RC-IMP-09) —
supplying a value tells REDCap to *modify an existing event* with that name (RC-API-20),
and the generator warns if you do. The generator still computes the **expected** name
for each event and uses it in `InstrumentDesignations.csv` and the summary.

These expected names are **predictions**. REDCap's documented algorithm (RC-LONG-01),
which the generator follows:
1. Lowercase
2. **Remove hyphens entirely** — they vanish, not become underscores
   (`"Follow-up"` → `"followup"`, **not** `"follow_up"`)
3. Replace all other non-alphanumeric characters with underscores
4. Collapse consecutive underscores; strip leading/trailing
5. Append `_arm_N`

Examples: `"Follow-up 30 min"` → `followup_30_min_arm_1`,
`"Ad Hoc Follow-up"` → `ad_hoc_followup_arm_1`, `"Month 3"` → `month_3_arm_1`.

Accented characters are transliterated (REDCap 17.3.0+ in newly created projects;
older projects may keep accents). The KB documents no length limit or truncation rule,
so the generator applies none. Two events in the same arm that would produce the same
name (e.g. "Follow-up" and "Followup") are rejected as an error.

**Always verify after importing `Events.csv`:** download the events (Define My Events →
download events, or API/MCP `export_events`, RC-API-19) and confirm each real
`unique_event_name` matches the expected name in `InstrumentDesignations.csv` before
uploading the designations. A mismatched name makes that mapping row fail silently
(RC-IMP-09). If any differ, fix the designations file with the real names.

**Scheduling columns:** `Events.csv` always includes `day_offset`, `offset_min`,
`offset_max` (needed for display order). RC-LONG-01 notes these columns appear in
REDCap's own export only when the Scheduling module is active; if an upload is rejected
in a project without scheduling, remove those three columns.

**Event display order — critical for same-day events**: REDCap displays events in
ascending `day_offset` order. When multiple events share the same `day_offset`,
REDCap breaks the tie by sorting alphabetically by `unique_event_name`. This is
almost never the intended clinical order. For example, a project with Screening,
Consent, Baseline, Randomization all at Day 0 will display as:
`Baseline → Consent → Randomization → Screening` (alphabetical), not the logical flow.

**To enforce a specific order**: assign sequential `day_offset` values even for
same-day events (e.g. 0, 1, 2, 3…). REDCap will display events in day_offset order,
and `day_offset=0` vs `day_offset=1` makes no practical difference to visit scheduling
while guaranteeing the display order you want. The generator warns you if it detects
same-day events that would sort alphabetically into an unintended order.

---

## Step 4: Run the Generator

Save the spec as `longitudinal_spec.json` in `<output_folder>` (the folder the user is working in, or one they name; never a temp folder) and run:

```bash
python <skill_path>/scripts/generate_longitudinal.py \
  --spec <output_folder>/longitudinal_spec.json \
  --output-dir <output_folder>
```

The script writes up to three CSV files:
- `Arms.csv` — `arm_num,name`; **only written for multi-arm projects** (see below).
  Arms referenced by events but missing from `arms` are added as "Arm N".
- `Events.csv` — `event_name,arm_num,day_offset,offset_min,offset_max,unique_event_name,custom_event_label`
  with `unique_event_name` blank
- `InstrumentDesignations.csv` — `arm_num,unique_event_name,form` using expected names;
  only written when the spec has `mapping` rows

It also prints a summary (including the expected unique event names) and any warnings.
Errors (unknown spec keys, duplicate event names in an arm, negative offsets, no events)
stop the run with exit code 1 and no files are written.

> **Single-arm projects: no Arms.csv.** Arm 1 is created automatically when longitudinal
> mode is enabled (RC-IMP-09), so the script does not write `Arms.csv` when only arm 1 is
> used. If the user wants arm 1 renamed, tell them to rename it in Define My Events.

For a quick preview without writing files:
```bash
python <skill_path>/scripts/generate_longitudinal.py \
  --spec <output_folder>/longitudinal_spec.json \
  --preview
```

---

## Step 5: Review and Present

After generation, do three things:

1. **Run the reader script** from the companion `redcap-longitudinal-structure` skill to
   parse the generated files and show the user a formatted summary. This double-checks
   the output and gives the user a clear confirmation of what was built:

   ```bash
   python ~/.claude/skills/redcap-longitudinal-structure/scripts/parse_longitudinal.py \
     --arms <output_folder>/Arms.csv \
     --events <output_folder>/Events.csv \
     --mapping <output_folder>/InstrumentDesignations.csv
   ```

   Omit `--arms` for single-arm projects (no `Arms.csv`). Because `Events.csv` has a blank
   `unique_event_name`, the reader predicts the names and marks them with `~` — tell the
   user these are expected names to verify after import, not confirmed ones.

2. **Give the user the full path of each file** as a link.
   For single-arm projects, present only `Events.csv` and `InstrumentDesignations.csv`.

3. **Include repeatable instrument/event instructions.** This is mandatory — do not wait
   for the user to ask. Based on the project design, identify any instruments or events
   that need to be configured as repeatable in REDCap and include the following as part
   of your response:

   - **Which instrument(s) or event(s)** should be repeatable, and why (e.g. "the Ad Hoc
     Follow-up form can occur multiple times per participant")
   - **Repeat mode**: "Repeat Instruments" (only specific forms repeat within a fixed
     event) vs. "Repeat Entire Event" (the whole event, with all its forms, repeats).
     Use "Repeat Instruments" when only one or a few forms repeat; use "Repeat Entire
     Event" when all forms at that event are collected multiple times.
   - **Step-by-step UI instructions:**
     1. Go to **Project Setup**
     2. Under "Optional modules and customizations," click **Enable** (or **Modify**)
        next to "Repeatable instruments and events"
     3. Find the instrument or event row, set the dropdown to the appropriate repeat mode
     4. Save
   - **Suggested repeat instrument label** if applicable — this is the label shown on
     the "+" button in the data entry interface (e.g. "Add follow-up visit"). Suggest
     something short and descriptive that will make sense to a data entry user.

Tell the user how to import the files:

> **Uploading through the REDCap UI (no API access needed):**
> 1. In Project Setup, click **Define My Events**.
> 2. *(Multi-arm projects only)* Open the **"Upload or download arms/events"** dropdown
>    and upload `Arms.csv` first.
> 3. Upload `Events.csv` using the same dropdown.
> 4. Navigate to **Designate Instruments for My Events**, open the **"Upload or download
>    instrument mappings"** dropdown, and upload `InstrumentDesignations.csv`.
>
> **Important:** The instrument designations upload replaces the entire mapping — any
> combination not in the file will be unchecked. If the project already has designations,
> download the current mapping first and merge your new rows into it before uploading.
>
> **Alternative — REDCap API:** POST each file with the appropriate `content` parameter
> (`arm`, `event`, `formEventMapping`) and `action=import`. Use `override=0` for arms and
> events (`override=1` deletes all existing arms/events first, RC-API-17/20). Arms and
> events imports are additive; instrument-event mapping import replaces the full
> configuration (same behavior as the UI upload).

### Uploading via the REDCap MCP connectors

The instrument-event mapping import **replaces the whole mapping** — any designation not
in the file is unchecked. If the user wants you to import through the REDCap MCP
connectors instead of uploading themselves:

1. **First export the current state** from the target project: `export_arms`,
   `export_events`, `export_instrument_event_mappings`. Merge new rows into the existing
   mapping rather than importing the generated file alone, and show the user the diff.
2. **Only import on connectors the connector map (`~/.claude/redcap-connectors.md`) marks as non-production** —
   and only after the user
   explicitly confirms the target project and the import.
3. **Never import on production connectors.** For those, hand the user the files to upload themselves.
4. Import in order arms → events → mappings; after events, run `export_events` and use the
   real `unique_event_name` values in the mapping before importing it.

---

## Step 6: Offer to Iterate

After presenting, ask:
- Does the event schedule look right?
- Are all the form assignments correct?
- Do you need to add, remove, or rename anything?

Rebuild and regenerate as needed. The spec JSON is fast to modify and regenerate.

---

## Common Scenarios

### Protocol with a Schedule of Events table
Extract the rows (visits) and columns (instruments). Each column with a checkmark or
"X" at a given visit = one row in the mapping. Confirm arm structure, then generate.

### Single-arm longitudinal project
Set `"arms": [{"arm_num": 1, "name": "Arm 1"}]` (or omit `arms`). All events go under
`arm_num: 1`. The script does not write `Arms.csv`.

### Same event schedule across all arms
Build events for Arm 1, then duplicate them for other arms with incremented `arm_num`.
The generator handles this if you include all arm/event combos in the spec.

### User knows event names but not form names yet
Generate the Arms and Events CSVs now; skip or stub the mapping. Note that the
Instrument Designations import requires forms to already exist in the project.

### Updating an existing project (adding events or arms)
Generate only the new rows — both the UI upload and the API import for events and arms
are additive (add if missing, ignore if already present). Existing events not in the
file are unaffected. Make clear to the user that uploading a partial events file will
not delete anything that is already configured. For instrument designations, the upload
always replaces the full mapping, so the user should download the current mapping first,
add the new rows, and re-upload the merged file.

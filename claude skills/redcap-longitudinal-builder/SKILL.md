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
  and asks to turn it into a REDCap longitudinal setup. This is the companion to the
  redcap-longitudinal-structure skill (which reads existing files) — use this one when
  building from scratch.
---

# REDCap Longitudinal Builder Skill

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
Per the team style guide (`STYLE-GUIDE.md` at the repo root, Section 2.1), longitudinal mode
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

**Visit windows**: Not all projects use visit windows. If the user doesn't mention them,
set `offset_min = offset_max = day_offset` (meaning no window). If they say "±7 days",
set `offset_min = day_offset - 7` and `offset_max = day_offset + 7`.

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
    {"arm_num": 1, "arm_name": "Treatment"},
    {"arm_num": 2, "arm_name": "Control"}
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
      "offset_min": 83,
      "offset_max": 97
    }
  ],
  "mapping": [
    {"unique_event_name": "baseline_arm_1", "form": "demographics"},
    {"unique_event_name": "month_3_arm_1",  "form": "labs"}
  ]
}
```

**Note on `unique_event_name`**: You don't need to set this for events — the generator
derives it automatically. Leave `unique_event_name` out of the events array and the
generator will compute the correct value. The same function is used when building
the mapping, so the two files will always stay in sync.

REDCap's actual slugification algorithm (which the generator replicates exactly):
1. Lowercase
2. **Remove hyphens entirely** — they vanish, not become underscores
   (`"Follow-up"` → `"followup"`, **not** `"follow_up"`)
3. Replace all other non-alphanumeric characters with underscores
4. Collapse consecutive underscores; strip leading/trailing
5. Append `_arm_N`

Examples: `"Follow-up 30 min"` → `followup_30_min_arm_1`,
`"Ad Hoc Follow-up"` → `ad_hoc_followup_arm_1`, `"Month 3"` → `month_3_arm_1`.

**Do not manually type `unique_event_name` values into the spec** unless copying
them from an existing REDCap export — hand-typed names frequently diverge from
what REDCap generates, which breaks the mapping import.

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

Save the spec to a temp JSON file and run:

```bash
python <skill_path>/scripts/generate_longitudinal.py \
  --spec /tmp/longitudinal_spec.json \
  --output-dir /tmp/longitudinal_output/
```

The script writes up to three CSV files:
- `Arms.csv` — **only generated and presented for multi-arm projects** (see below)
- `Events.csv`
- `InstrumentDesignations.csv`

It also prints a summary of what was generated and any warnings.

> **Single-arm projects: skip Arms.csv entirely.** REDCap creates a default arm
> automatically, so there is nothing to import. Do not generate or present `Arms.csv`
> when the project has only one arm — it adds confusion without benefit.

For a quick preview without writing files:
```bash
python <skill_path>/scripts/generate_longitudinal.py \
  --spec /tmp/longitudinal_spec.json \
  --preview
```

---

## Step 5: Review and Present

After generation, do three things:

1. **Run the reader script** from the companion `redcap-longitudinal-structure` skill to
   parse the generated files and show the user a formatted summary. This double-checks
   the output and gives the user a clear confirmation of what was built:

   ```bash
   python <reader_skill_path>/scripts/parse_longitudinal.py \
     --arms /tmp/longitudinal_output/Arms.csv \
     --events /tmp/longitudinal_output/Events.csv \
     --mapping /tmp/longitudinal_output/InstrumentDesignations.csv
   ```

2. **Copy files to the workspace folder** and present them so the user can download them.
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
> (`arm`, `event`, `formEventMapping`) and `action=import`. Arms and events imports are
> additive; instrument-event mapping import replaces the full configuration (same
> behavior as the UI upload).

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
Set `"arms": [{"arm_num": 1, "arm_name": "Arm 1"}]` (or the user's preferred name).
All events go under `arm_num: 1`. Do not generate or present `Arms.csv`.

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

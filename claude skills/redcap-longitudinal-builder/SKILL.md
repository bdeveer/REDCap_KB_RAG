---
name: redcap-longitudinal-builder
description: |
  Build the three REDCap longitudinal project CSV files — Arms, Events, and Instrument
  Designations — from user input or uploaded documentation. Use this skill whenever a
  user wants to set up or draft a longitudinal project structure, is starting a new
  longitudinal REDCap project, wants to generate files for API import, or describes a
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

| File | Purpose | REDCap API import type |
|------|---------|------------------------|
| **Arms** | Study arms (parallel groups or sequential phases) | `content=arm` |
| **Events** | Timepoints within each arm | `content=event` |
| **Instrument Designations** | Which forms are collected at which events | `content=formEventMapping` |

These can be imported into REDCap via API (`action=import`) or manually through
Project Setup. Generating them ahead of time saves significant manual data entry,
especially for complex multi-arm studies.

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
derives it automatically from the event name and arm number using REDCap's convention:
lowercase, spaces → underscores, `_arm_N` suffix. E.g. "Month 3" in Arm 1 →
`month_3_arm_1`. If the user references a specific `unique_event_name` (e.g. from an
existing project), use that exact value in the mapping instead.

---

## Step 4: Run the Generator

Save the spec to a temp JSON file and run:

```bash
python <skill_path>/scripts/generate_longitudinal.py \
  --spec /tmp/longitudinal_spec.json \
  --output-dir /tmp/longitudinal_output/
```

The script writes three CSV files:
- `Arms.csv`
- `Events.csv`
- `InstrumentDesignations.csv`

It also prints a summary of what was generated and any warnings.

For a quick preview without writing files:
```bash
python <skill_path>/scripts/generate_longitudinal.py \
  --spec /tmp/longitudinal_spec.json \
  --preview
```

---

## Step 5: Review and Present

After generation, do two things:

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

Tell the user how to import the files:
> These files are ready for REDCap API import. For each file, use a POST request with
> `content=arm`/`event`/`formEventMapping` and `action=import`. Or share them with your
> REDCap admin for import. Note that `unique_event_name` values in the Events file are
> auto-generated by REDCap — if you import via API and REDCap generates different values,
> update the Instrument Designations file to match before importing it.

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
All events go under `arm_num: 1`.

### Same event schedule across all arms
Build events for Arm 1, then duplicate them for other arms with incremented `arm_num`.
The generator handles this if you include all arm/event combos in the spec.

### User knows event names but not form names yet
Generate the Arms and Events CSVs now; skip or stub the mapping. Note that the
Instrument Designations import requires forms to already exist in the project.

### Updating an existing project (adding events or arms)
Generate only the new rows — REDCap API import with `action=import` for events and
arms does an *upsert* (add if missing, ignore if already present). Make clear to the
user that existing events won't be deleted by an import; REDCap only adds new ones.

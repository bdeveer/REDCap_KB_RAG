---
id: RC-LONG-01
title: Longitudinal Project Setup
domain: Longitudinal & Repeated Setup
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-FD-01 — Form Design Overview
- RC-NAV-UI-01 — Project Navigation UI
version: '1.3'
last_updated: 2026-08
related:
- id: RC-CC-04
  title: 'Control Center: User Settings & Defaults'
- id: RC-LONG-02
  title: Repeated Instruments & Events Setup
- id: RC-NAV-REC-02
  title: Longitudinal Mode & Arms
- id: RC-NAV-REC-03
  title: Repeated Instruments & Repeated Events
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
tags:
- longitudinal & repeated setup
- longitudinal
synonyms:
- how do i set up a longitudinal project
- collect data across multiple time points and events
- enable longitudinal mode in redcap
- define arms and events
- assign instruments to events
- multiple visits or timepoints per participant
- set up study arms for control and intervention groups
- designate which forms are collected at which event
---

# 1. Overview

This article covers how to configure a REDCap project for longitudinal data collection. Longitudinal mode allows you to collect data across multiple time points (events) and, optionally, across distinct participant cohorts (arms). The setup involves enabling longitudinal mode, defining your arms and events, and designating which instruments are collected at which events. This article also describes how a longitudinal setup affects other REDCap features such as branching logic and data exports.

Repeated instruments and repeated events are a separate feature that can be layered on top of a longitudinal project — see [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) for that configuration.

---

# 2. Key Concepts & Definitions

**Longitudinal Mode**

A project setting that enables time-point-based data collection. When active, REDCap organizes data by record, arm, and event rather than simply by record and instrument. All longitudinal features are hidden until this mode is enabled.

**Arm**

A named grouping of events within a longitudinal project. Arms are used to separate distinct participant cohorts that follow different data collection schedules (e.g., a control arm and an intervention arm). Projects with a single participant flow require only one arm.

**Event**

A defined time point within an arm (e.g., Baseline, Week 4 Follow-up, Month 12). Each event can have one or more instruments designated to it. Events control when and in what order data is collected for each record.

**Event Label**

The human-readable name you assign to an event (e.g., "Baseline," "3 Month Follow-Up"). Changing an event label after the project has collected data will also change its unique event name, which can break branching logic referencing that event.

**Unique Event Name**

A system-generated identifier for each event, derived from the event label and arm number (e.g., `baseline_arm_1`). It is used to reference events in branching logic, piping, and calculated fields. Cannot be manually overridden through the UI; may be specified in a CSV upload, but leaving it blank and letting REDCap generate it is strongly preferred.

REDCap generates the unique event name using this algorithm: lowercase the event label, remove hyphens entirely (they do not become underscores), replace all remaining non-alphanumeric characters with underscores, collapse consecutive underscores, and append `_arm_N`. Examples: `"Baseline"` → `baseline_arm_1`; `"Follow-up 30 min"` → `followup_30_min_arm_1` (not `follow_up_30_min_arm_1`); `"Ad Hoc Follow-up"` → `ad_hoc_followup_arm_1`. When building instrument-event mapping CSVs externally, derive unique event names using this exact algorithm — hand-typed approximations frequently diverge from what REDCap generates and will cause mapping imports to fail.

**Custom Event Label**

An optional field that allows you to pipe a variable's value into the event's display label. Uses standard REDCap piping syntax (e.g., `[visit_date]`). The piped variable must exist within that event.

**Event ID**

A permanent numeric identifier assigned by REDCap to each event. Unlike the unique event name, the event ID does not change when the event label is renamed. Used in advanced features and internal database references.

**Instrument Designation**

The assignment of one or more instruments to a specific event within an arm. Only designated instruments appear when entering data for a given event. An instrument can be designated to multiple events across one or more arms.

---

# 3. Enabling Longitudinal Mode

Before any longitudinal features are accessible, you must enable longitudinal mode from the Project Setup page.

1. Navigate to your project and open **Project Setup**.
2. Locate the option labeled **"Use longitudinal data collection with defined events?"** at the top of the page.
3. Click the corresponding **Enable** button.

Once enabled, the longitudinal configuration tools — Define My Events and Designate Instruments for My Events — become visible in Project Setup.

> **Critical:** Disabling longitudinal mode after data collection has begun will delete all data that was not collected in the very first event of the project. Do not disable longitudinal mode unless you are certain no data outside the first event needs to be retained.

> **Institution-specific:** In Production mode, disabling longitudinal mode or un-designating events may require administrator approval. Many installations enable this safeguard by default. Move your project to Production before collecting real data to benefit from this protection.

---

# 4. Defining Arms & Events

After enabling longitudinal mode, click the **Define My Events** button in Project Setup to reach the arm and event configuration page. By default, REDCap creates one arm ("Arm 1") with one event pre-populated.

## 4.1 Managing Arms

Arms appear as tabs across the top of the Define My Events page.

**Renaming an arm:** Click the **Rename Arm** link next to the arm tab and enter a new name.

**Adding a new arm:** Click the **+Add New Arm** tab, enter a name, and confirm. New arms are created without any events — you must add events to them manually.

**Deleting an arm:** The delete option appears next to the rename link when more than one arm exists.

> **Critical:** Deleting an arm permanently deletes all records and data associated with that arm. This action cannot be undone.

## 4.2 Event Table Columns

Within each arm, events are displayed in a table with the following columns:

| **Column** | **Description** |
|---|---|
| Move | Drag handle to reorder events. Hover over the column to reveal the up/down arrow icon. |
| Edit / Delete | Pencil icon edits the event label or custom event label. Red X deletes the event. |
| Event # | System-assigned display order number for the event. |
| Event Label | The human-readable name of the event. Must be unique within the arm. |
| Custom Event Label | Optional piping field. Enter a variable name in brackets (e.g., `[visit_date]`) to display that value in the event label during data entry. |
| Unique Event Name | Auto-generated from the arm number and event label. Used in logic references. Read-only; changes when the event label is renamed. |
| Event ID | Permanent numeric identifier. Does not change when the event label is renamed. |

> **Important:** If you rename an event label, the unique event name changes with it. Any branching logic, piping, or calculated fields that reference the old unique event name will break. Review all logic after renaming events.

## 4.3 Adding & Deleting Events

**Adding an event:** Enter an event name in the **Event label** text box at the bottom of the arm's table, optionally fill in a custom event label, and click **Add new event**.

**Deleting an event:** Click the red X icon next to the event. Deleting an event permanently deletes any data recorded in that event for all records in the project.

---

> **Navigation notes.** A direct link to **Define My Events** appears in the "Project Home and Design" section of the left-hand menu from **15.3.3** (repositioned slightly in 15.4.0 for consistency with earlier layouts). From **17.4.1**, **Designate Instruments for My Events** is likewise reachable directly from the left-hand menu and gained a **Print Page** button. From **15.4.5**, icons distinguish repeating instruments from repeating events on Define My Events, Designate Forms and the Online Designer.

> **Critical — accented characters in event and DAG names (17.3.0+).** In **newly created** projects, accented characters in Data Access Group or longitudinal event names are transliterated to their unaccented equivalents when REDCap generates the **unique** name. Since unique event names are what branching logic, piping and API calls reference, a project created before 17.3.0 may hold unique names containing accents while a project created after does not — so logic copied between the two can silently fail to match. Check the unique names, not the display labels, when moving expressions between projects.

---

# 5. Designating Instruments to Events

After defining arms and events, navigate to the **Designate Instruments for My Events** tab (accessible from the Define My Events page or via the button in Project Setup).

This page displays a matrix with instruments as rows and events as columns. A separate tab appears for each arm.

**To designate instruments:**

1. Click **Begin Editing** to unlock the checkboxes.
2. Check the box for each instrument-event combination you want to enable. Use **Select All** or **Deselect All** at the top of the table to apply changes in bulk.
3. Click **Save** to confirm your selections.

> **Critical:** Unchecking an instrument-event combination that already contains saved data will make that data inaccessible — it will no longer appear in the UI. The data is not deleted from the database and can be recovered by re-checking the combination, but treat this as a high-risk action: always verify the combination is empty, or export the data first, before removing a designation. If new data is collected in the same instrument-event combination after it was unchecked and then re-checked, there may be record-level collisions that require backend database intervention to resolve. If you are unsure, contact your local REDCap administrator before proceeding.

> **Important:** Always designate the first instrument in your project (the one containing the record ID field) to the very first event in each arm. REDCap stores the record ID in this instrument-event combination. Omitting it will cause unpredictable behavior and risk data not being saved correctly.

---

# 6. Bulk Setup via CSV Upload & Download

Both the Define My Events page and the Designate Instruments page support CSV-based bulk operations, useful for projects with large numbers of events or complex instrument-event mappings.

## 6.1 Arms & Events (Define My Events page)

Access bulk options from the **Upload or download arms/events** dropdown.

> **Upload order:** When setting up a project via CSV, always upload in this sequence: **arms → events → instrument mappings**. Events reference arm numbers, so the arm must exist before events are uploaded. Instrument mappings reference unique event names, so events must exist before mappings are uploaded. Uploading out of order will cause references to fail.

> **Single-arm projects:** If your project has only one arm, you do not need to upload the arms CSV. REDCap creates "Arm 1" automatically when longitudinal mode is enabled. Start with the events upload, then upload instrument mappings.

| **Option** | **Behavior** |
|---|---|
| Upload arms (CSV) | **Additive.** Adds new arms. Existing arms not in the file are unaffected. |
| Download arms (CSV) | Exports current arm configuration. Useful for backup or bulk editing. |
| Upload events (CSV) | **Additive.** Adds new events. Existing events not in the file are unaffected. |
| Download events (CSV) | Exports current event configuration. |

> **Note:** Arms and event uploads are additive — you can safely upload a file containing only new rows without affecting existing configuration. This is the opposite of instrument-event mapping uploads, which replace the entire mapping (see §6.2). Keep this distinction in mind when planning bulk updates.

### Arms CSV format

**Columns:** `arm_num`, `name`

| **Column** | **Type** | **Notes** |
|---|---|---|
| `arm_num` | Positive integer | Sequential, starting at 1. No leading zeros. |
| `name` | Free text | Descriptive label shown in the UI (e.g., "Control", "Intervention"). |

Example:

```
arm_num,name
1,Control
2,Intervention
```

### Events CSV format

**Core columns (always present):** `event_name`, `arm_num`, `unique_event_name`, `custom_event_label`

**Additional columns when the Scheduling module is active:** `day_offset`, `offset_min`, `offset_max` appear between `arm_num` and `unique_event_name`.

Full column order (scheduling active): `event_name`, `arm_num`, `day_offset`, `offset_min`, `offset_max`, `unique_event_name`, `custom_event_label`

| **Column** | **Type** | **Notes** |
|---|---|---|
| `event_name` | Free text | Display label for the event. **Values containing spaces or special characters are wrapped in double quotes** in the CSV (e.g., `"3 Month"`, `"End of Study"`). |
| `arm_num` | Positive integer | Must match an existing arm. In multi-arm projects, every event must appear as a separate row for each arm — there is no single row that spans multiple arms. A 2-arm, 6-event project produces 12 rows in the events CSV. |
| `day_offset` | Integer ≥ 0 | Days from the reference date (e.g., enrollment). REDCap sorts events by `day_offset` ascending. |
| `offset_min` | Integer ≥ 0 | Early scheduling window (days before the target date). Expressed as a positive number in the CSV — e.g., `3` means the window opens 3 days before the target date. Note: the API Export Events endpoint returns this value as a negative integer (e.g., `-3`); if building a CSV from API output, convert to its absolute value. |
| `offset_max` | Integer ≥ 0 | Late scheduling window (days after the target date). Expressed as a positive number. Symmetric windows (e.g., ±14 days) appear as the same value in both columns. |
| `unique_event_name` | Snake_case string | May be left blank on upload — REDCap auto-generates from the event name and arm number. **Recommended: leave blank and let REDCap generate.** See derivation rule below. |
| `custom_event_label` | Free text or blank | Piped event label. Leave blank if not used. The column is always present in exports — even when all values are empty. |

**`unique_event_name` derivation rule:** REDCap lowercases the event name, removes hyphens entirely (they do not become underscores), replaces all remaining non-alphanumeric characters with underscores, collapses consecutive underscores into one, and appends `_arm_{N}`. Examples: "Screening" → `screening_arm_1`; "3 Month" → `3_month_arm_1`; "End of Study" → `end_of_study_arm_1`; "Follow-up" → `followup_arm_1` (hyphen removed, not converted); "Ad Hoc (Visit)" → `ad_hoc_visit_arm_1` (parentheses become underscores, consecutive underscores collapsed). Hand-typing unique event names that don't match this rule exactly will cause the mapping upload to silently fail.

- `day_offset`, `offset_min`, and `offset_max` appear in the downloaded events CSV only when the scheduling module is active for the project. Include them in an upload only when scheduling is in use.
- When multiple events share the same `day_offset`, REDCap breaks the display-order tie by sorting alphabetically by unique event name — which is rarely the intended clinical order. To enforce a specific display order among same-day events, assign sequential `day_offset` values (e.g., 0, 1, 2, 3…) even if the events all occur on the same calendar day.

Example (scheduling module active, 2-arm project — rows for both arms shown):

```
event_name,arm_num,day_offset,offset_min,offset_max,unique_event_name,custom_event_label
Screening,1,0,0,0,screening_arm_1,
Baseline,1,7,7,7,baseline_arm_1,
"3 Month",1,90,14,14,3_month_arm_1,
"6 Month",1,180,14,14,6_month_arm_1,
"9 Month",1,270,14,14,9_month_arm_1,
"End of Study",1,365,14,14,end_of_study_arm_1,
Screening,2,0,0,0,screening_arm_2,
Baseline,2,7,7,7,baseline_arm_2,
"3 Month",2,90,14,14,3_month_arm_2,
"6 Month",2,180,14,14,6_month_arm_2,
"9 Month",2,270,14,14,9_month_arm_2,
"End of Study",2,365,14,14,end_of_study_arm_2,
```

## 6.2 Instrument-Event Mappings (Designate Instruments page)

Access bulk options from the **Upload or download instrument mappings** dropdown:

| **Option** | **Behavior** |
|---|---|
| Upload instrument-event mappings (CSV) | Replaces the full mapping configuration. Any instrument-event combination omitted from the file will be unchecked. |
| Download instrument-event mappings (CSV) | Exports current mappings. Useful for backup or bulk editing. |

### Instrument-Event Mappings CSV format

**Columns:** `arm_num`, `unique_event_name`, `form`

| **Column** | **Type** | **Notes** |
|---|---|---|
| `arm_num` | Positive integer | Arm the event belongs to. |
| `unique_event_name` | Snake_case string | Must match a `unique_event_name` that already exists in the project. Copy directly from a downloaded events CSV or the Define My Events page — do not type by hand. |
| `form` | Snake_case string | The instrument's **internal variable name**, not its display label. Found in the Data Dictionary (`form_name` column) or the Online Designer. Example: `phq9`, `medication_list`, `adverse_event_log`. |

Each row represents one instrument designated to one event. An event with five instruments assigned to it produces five rows in this file. In multi-arm projects the entire mapping is replicated per arm — arm 1 rows first, then arm 2, etc. File size scales as total (events × instruments per event) across all arms.

> **Important:** Unlike arm and event uploads, the instrument-event mapping upload is not additive — it replaces the complete mapping configuration. Omitting a mapping will uncheck it, potentially deleting data if the combination contained records. Always start from a downloaded export and edit it rather than building from scratch.

Example (2-arm project, abbreviated):

```
arm_num,unique_event_name,form
1,screening_arm_1,screening
1,baseline_arm_1,demographics
1,baseline_arm_1,social_history
1,baseline_arm_1,phq9
1,3_month_arm_1,phq9
1,3_month_arm_1,medication_list
...
2,screening_arm_2,screening
2,baseline_arm_2,demographics
2,baseline_arm_2,social_history
2,baseline_arm_2,phq9
2,3_month_arm_2,phq9
2,3_month_arm_2,medication_list
...
```

> **Repeatable mapping not covered here:** The bulk CSV workflow described in this section covers arms, events, and instrument-event designations only. The configuration of which instruments or events are repeatable (set up via the repeating instruments and events popup in Project Setup) cannot be exported or imported through the UI. Use the REDCap API for programmatic management of repeatable mappings. See [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) for details.

For the full column-by-column reference, upload order rules, and common mistakes for all three CSV formats, see **[RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) — Longitudinal Structure CSV**.

---

# 7. Modifying an Existing Longitudinal Setup

Changing arms, events, or instrument designations in a project that has already collected data carries significant risk. The following actions can cause data loss or break project logic:

- Renaming event labels (changes unique event names, breaks logic references)
- Deleting events or arms (permanently deletes associated data)
- Removing instrument-event designations (deletes data in that combination)
- Reordering events (may affect downstream workflow features)

**Best practice:** Before making any changes to an active project, clone the entire project and test the modifications in the copy first. If you are unsure about the impact of a change, consult your local REDCap administrator before proceeding.

> **Institution-specific:** Production-mode changes to the longitudinal setup may require administrator approval. Contact your REDCap support team before modifying the setup of an active production project.

---

# 8. Effects on Other REDCap Features

A longitudinal setup changes behavior in several other areas of REDCap. Understanding these effects before finalizing your setup will prevent surprises during data collection.

## 8.1 Branching Logic

In a standard (non-longitudinal) project, branching logic references fields by variable name alone (e.g., `[dob]`). In a longitudinal project, any reference to a variable in a *different* event must include the event's unique event name:

```
[baseline_arm_1][dob]
```

References to variables *within the same instrument or event* ("local" references) do not require the event prefix. Cross-event references without the event prefix will not evaluate correctly.

See [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) — Branching Logic Overview & Scope for full syntax details.

## 8.2 Piping

Piping follows the same rules as branching logic. Piping a variable from a different event requires the unique event name prefix. Local piping (within the same event) does not.

## 8.3 Reports & Data Exports

In a non-longitudinal project, each record produces one row in a report or export. In a longitudinal project, the output produces **one row per event per record**. A project with 10 events and 100 records will produce up to 1,000 rows.

To identify which row belongs to which event and record, REDCap adds coordinate variables to exports (e.g., `redcap_event_name`). Exports from longitudinal projects will contain many empty cells because most instruments are only designated to specific events.

**Best practice:** Use the report builder's event filters to export only the data you need for any given analysis. Exporting all data from a large longitudinal project produces unwieldy output with sparse rows.

## 8.4 Workflow Features

Automated Survey Invitations, the Survey Queue, the scheduling module, and Form Display Logic all incorporate the longitudinal event structure into their configuration. Each can be scoped to specific events. For large projects with many events, using the bulk upload options for these features is recommended.

---

# 9. Common Questions

**Q: Do I need more than one arm?**

**A:** Only if different participant cohorts follow a different event or instrument schedule. A control group and intervention group that collect the same instruments at the same time points can use a single arm. If the intervention group needs an additional instrument at every event, a second arm allows you to designate that instrument separately without affecting the control arm.

**Q: Can I add events after the project has already collected data?**

**A:** Yes. Adding new events to an existing project does not affect existing data. You will need to designate instruments to the new event and configure any relevant workflow features after adding it.

**Q: What happens if I forget to designate the first instrument to the first event?**

**A:** REDCap stores the record ID in the first instrument-event combination. If that combination is not designated, new records may fail to save data correctly and the project can exhibit unpredictable behavior. Always designate your first instrument to your first event before collecting data.

**Q: Can the same instrument appear in multiple events?**

**A:** Yes. An instrument can be designated to as many events as needed across any arm. This is standard practice for instruments that are administered at every time point (e.g., a vitals form collected at every visit).

**Q: Can I change an event label after data collection has started?**

**A:** Technically yes, but it is strongly discouraged. Renaming an event label changes its unique event name, which will break any branching logic, piping, or calculated fields that reference the old name. Always test in a cloned project first and audit all logic before renaming.

**Q: What is the difference between a unique event name and an event ID?**

**A:** The unique event name is a readable identifier (e.g., `baseline_arm_1`) that changes if the event label is renamed. The event ID is a permanent numeric identifier that never changes. For branching logic and piping, you use the unique event name. The event ID is used in certain advanced integrations and is generated and managed by REDCap.

**Q: How does REDCap determine the display order of events?**

**A:** REDCap displays events in ascending `day_offset` order. When two or more events share the same `day_offset`, REDCap sorts them alphabetically by unique event name — not by the order they were created or entered. This catches many users off guard when all events are at Day 0 (common in projects where events represent sequential steps rather than time-separated visits). To enforce a specific display order, assign sequential `day_offset` values (0, 1, 2, 3…) to events that would otherwise share the same offset. The difference between Day 0 and Day 1 has no practical scheduling impact but guarantees the correct display sequence.

**Q: If I upload an events CSV with only new events in it, will my existing events be deleted?**

**A:** No. The events upload is additive — REDCap adds any events in the file that do not already exist and leaves existing events untouched. This is different from the instrument-event mapping upload, which replaces the full mapping configuration. You can safely upload a partial events file without affecting events that are already configured.

**Q: Do I need to upload an arms CSV for a single-arm project?**

**A:** No. When longitudinal mode is enabled, REDCap automatically creates one arm ("Arm 1"). For single-arm projects, skip the arms upload entirely and begin with the events CSV upload, followed by the instrument-event mappings upload.

**Q: What columns does the events CSV need, and what is optional?**

**A:** The minimum required columns are `event_name`, `arm_num`, `unique_event_name`, and `custom_event_label`. The `unique_event_name` column can be left blank — REDCap will auto-generate it. The `custom_event_label` column can also be blank. If the scheduling module is active, the CSV will also contain `day_offset`, `offset_min`, and `offset_max` columns; include those only when scheduling is in use. Download the existing events CSV from REDCap and use it as a template to ensure the column order and names are correct.

---

# 10. Common Mistakes & Gotchas

**Disabling longitudinal mode with existing data.** Turning off longitudinal mode deletes all data outside the first event, without a confirmation prompt specific to each record. There is no undo. Never disable longitudinal mode in a project with collected data unless you have verified that all data resides in the first event.

**Renaming events without auditing logic.** Every reference to a renamed event's unique event name in branching logic, piping, or calculated fields will silently stop working. REDCap will not flag broken logic at the time of renaming. Always run a full logic audit after any event rename.

**Omitting the first instrument from the first event.** Failing to designate the record-ID instrument to the first event causes records to save incorrectly or not at all. This is one of the most common and consequential configuration errors in new longitudinal projects.

**Uploading instrument-event mappings expecting additive behavior.** The instrument-event mapping CSV upload replaces the entire mapping, not just the rows in the file. Uploading a partial mapping will uncheck all omitted combinations. Always download and edit the existing mapping rather than creating a file from scratch.

**Uploading events before arms in a multi-arm project.** Events reference arm numbers in the CSV. If you upload an events CSV before the corresponding arms exist, REDCap cannot assign events correctly. For multi-arm projects, always upload in order: arms first, then events, then instrument-event mappings. Single-arm projects can skip the arms upload since Arm 1 is created automatically.

**Assuming exports will be one row per record.** Longitudinal exports produce one row per event per record. Many users attempt to read a longitudinal export expecting a flat structure and are surprised by the volume of rows and empty cells. Plan your analysis workflow before collecting data.

**Expecting same-day events to appear in entry order.** When multiple events share the same `day_offset`, REDCap sorts them alphabetically by unique event name rather than by the order they were entered. For example, events named Screening, Consent, Baseline, and Randomization all at `day_offset=0` will display as Baseline → Consent → Randomization → Screening. To control display order, assign sequential `day_offset` values (0, 1, 2, 3…) to same-day events.

**Manually typing unique event names in CSV mapping files.** The unique event name REDCap generates does not always match a naive word-for-word conversion. Specifically, REDCap removes hyphens rather than replacing them with underscores: `"Follow-up"` becomes `followup`, not `follow_up`. Hand-typed unique event names in instrument-event mapping CSVs frequently diverge from what REDCap actually generated, causing mapping imports to silently fail (the referenced event simply doesn't exist under that name). Always derive unique event names using REDCap's exact algorithm, or download the events CSV from REDCap and copy the names from there.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md)** — retrieve the list of arms defined in the project
- **[RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md)** — create or update arm definitions programmatically
- **[RC-API-18 — Delete Arms API](RC-API-18_Delete-Arms.md)** — remove one or more arms from a project programmatically
- **[RC-API-19 — Export Events API](RC-API-19_Export-Events.md)** — retrieve the list of events across all arms
- **[RC-API-20 — Import Events API](RC-API-20_Import-Events.md)** — create or update event definitions programmatically
- **[RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md)** — remove events from a project programmatically
- **[RC-API-10 — Export Instrument-Event Mappings API](RC-API-10_Export-Instrument-Event-Mappings.md)** — retrieve which instruments are assigned to which events
- **[RC-API-11 — Import Instrument-Event Mappings API](RC-API-11_Import-Instrument-Event-Mappings.md)** — update instrument-to-event assignments programmatically

---


# 11. Administrator Configuration

Whether project-level users can add or modify events and arms on a Production project is controlled by an administrator setting in the Control Center under System Configuration → User Settings & Defaults (see **[RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md)**, "Allow Normal Users to Add or Modify Events and Arms in Production").

When this setting is disabled — which is the default in most instances — only REDCap administrators can add or modify events and arms on a project in Production status. Users who need this change must submit a request to the REDCap support team.

When the setting is enabled, project-level users with Project Design and Setup rights can add events and modify certain event properties directly on a Production project. Even then, only administrators can delete events in production. Users can designate instruments to events that have not yet been designated, but cannot un-designate instruments that are already designated.

> **Note:** This setting applies to the REDCap UI only. The Import Arms and Import Events API endpoints remain restricted to Development status even when this setting is enabled. To modify arms or events via the API on a Production project, the project must first be returned to Development status.

> **See also:** [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md)

---

# 12. Related Articles

- [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md) (controls whether users can modify events/arms in Production)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (layering repeated instruments or events onto a longitudinal project)
- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) (navigating longitudinal records as a data entry user)
- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) (navigating repeated instances as a data entry user)
- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (setting up instruments before longitudinal configuration)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (building and managing instruments)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)(how branching logic is affected by longitudinal setup)
- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md) (data entry in a longitudinal context)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (accessing Project Setup)

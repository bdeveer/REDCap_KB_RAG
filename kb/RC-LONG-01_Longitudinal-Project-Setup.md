

**Longitudinal Project Setup**

| **Article ID** | [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) |
|---|---|
| **Domain** | Longitudinal & Repeated Setup |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — longitudinal setup behaviour checked against source code; Export Events offset values live-tested on 17.5.6 (Standard), 2026-10; pages not re-captured |
| **Prerequisite** | [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md); [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) |
| **Version** | 1.7 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md); [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md); [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md); [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md); [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)|
| **Synonyms** | how do i set up a longitudinal project; collect data across multiple time points and events; enable longitudinal mode in redcap; define arms and events; assign instruments to events; multiple visits or timepoints per participant; set up study arms for control and intervention groups; designate which forms are collected at which event |

---

## 1. Overview

This article covers how to configure a REDCap project for longitudinal data collection. Longitudinal mode allows you to collect data across multiple time points (events) and, optionally, across distinct participant cohorts (arms). The setup involves enabling longitudinal mode, defining your arms and events, and designating which instruments are collected at which events. This article also describes how a longitudinal setup affects other REDCap features such as branching logic and data exports.

Repeated instruments and repeated events are a separate feature that can be layered on top of a longitudinal project — see [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) for that configuration.

---

## 2. Key Concepts & Definitions

**Longitudinal Mode**

A project setting that enables time-point-based data collection. When active, REDCap organizes data by record, arm, and event rather than simply by record and instrument. All longitudinal features are hidden until this mode is enabled. REDCap only treats the project as longitudinal once it has more than one event; with a single event it behaves like a classic project.

**Arm**

A named grouping of events within a longitudinal project. Arms are used to separate distinct participant cohorts that follow different data collection schedules (e.g., a control arm and an intervention arm). Projects with a single participant flow require only one arm.

**Event**

A defined time point within an arm (e.g., Baseline, Week 4 Follow-up, Month 12). Each event can have one or more instruments designated to it. Events control when and in what order data is collected for each record.

**Event Label**

The human-readable name you assign to an event (e.g., "Baseline," "3 Month Follow-Up"). Changing an event label after the project has collected data will also change its unique event name, which can break branching logic referencing that event.

**Unique Event Name**

A system-generated identifier for each event, derived from the event label and arm number (e.g., `baseline_arm_1`). It is used to reference events in branching logic, piping, and calculated fields. It cannot be set by hand — not in the UI and not in a CSV upload (for a new event, a value supplied in the upload is ignored and REDCap generates the name itself).

REDCap generates the unique event name from the event label using this algorithm: remove punctuation and all other special characters (hyphens, parentheses, slashes and so on are deleted, not turned into underscores), replace each space with an underscore, lowercase the result, cut it to 18 characters, trim any leading or trailing underscores, and append `_arm_N`. Consecutive underscores are not collapsed. If two events in the project end up with the same name, the second gets a `b` appended, the third a `c`, and so on (e.g. `visit_arm_1`, `visit_arm_1b`). Examples: `"Baseline"` → `baseline_arm_1`; `"Follow-up 30 min"` → `followup_30_min_arm_1` (not `follow_up_30_min_arm_1`); `"Visit - Week 2"` → `visit__week_2_arm_1` (double underscore, because the hyphen is removed and both spaces remain); `"Month 12 Follow-up Visit"` → `month_12_followup_arm_1` (cut to 18 characters, trailing underscore trimmed). If nothing is left after removing characters (for example, a label written entirely in a non-Latin script), REDCap substitutes a 10-character code derived from the label. When building instrument-event mapping CSVs externally, derive unique event names using this exact algorithm — or better, copy them from a downloaded events CSV — because hand-typed approximations frequently diverge from what REDCap generates and the mapping import will be rejected.

**Custom Event Label**

An optional field that allows you to pipe a variable's value into the event's display label. Uses standard REDCap piping syntax (e.g., `[visit_date]`). The piped variable must exist within that event.

**Event ID**

A permanent numeric identifier assigned by REDCap to each event. Unlike the unique event name, the event ID does not change when the event label is renamed. Used in advanced features and internal database references.

**Instrument Designation**

The assignment of one or more instruments to a specific event within an arm. Only designated instruments appear when entering data for a given event. An instrument can be designated to multiple events across one or more arms.

---

## 3. Enabling Longitudinal Mode

Before any longitudinal features are accessible, you must enable longitudinal mode from the Project Setup page.

1. Navigate to your project and open **Project Setup**.
2. Locate the option labeled **"Use longitudinal data collection with defined events?"** at the top of the page.
3. Click the corresponding **Enable** button.

Once enabled, the longitudinal configuration tools — Define My Events and Designate Instruments for My Events — become visible in Project Setup.

> **Critical:** Disabling longitudinal mode after data collection has begun makes all data outside the very first event (of Arm 1) inaccessible — REDCap asks for confirmation, then hides the other arms and events and only the first event's data remains available. Strictly, that data is hidden rather than erased, and re-enabling longitudinal mode with the exact same setup may bring it back, but restoring can have side effects. Treat it as lost: do not disable longitudinal mode unless you are certain no data outside the first event needs to be retained, and export the full dataset first.

> **Institution-specific:** In Production status, only REDCap administrators can enable or disable longitudinal mode, and normal users cannot remove instrument designations; how such requests are submitted and approved varies by institution. Move your project to Production before collecting real data to benefit from this protection.

---

## 4. Defining Arms & Events

After enabling longitudinal mode, click the **Define My Events** button in Project Setup to reach the arm and event configuration page. Every project already has one arm ("Arm 1") with one event, so these are pre-populated.

### 4.1 Managing Arms

Arms appear as tabs across the top of the Define My Events page.

**Renaming an arm:** Click the **Rename Arm** link next to the arm tab and enter a new name.

**Adding a new arm:** Click the **+Add New Arm** tab, enter a name, and confirm. New arms are created without any events — you must add events to them manually.

**Deleting an arm:** The delete option appears next to the rename link when more than one arm exists. In Production it is shown only to REDCap administrators.

> **Critical:** Deleting an arm makes all records and data associated with that arm inaccessible. The data is hidden rather than erased and may reappear if the exact same arm and events are recreated, but restoring can have side effects — treat the deletion as irreversible and export the arm's data first.

### 4.2 Event Table Columns

Within each arm, events are displayed in a table with the following columns:

| **Column** | **Description** |
|---|---|
| Move | Drag handle to reorder events. Hover over the column to reveal the up/down arrow icon. Without the Scheduling module or MyCap, this drag order is the display order. |
| Edit / Delete | Pencil icon edits the event label or custom event label. Red X deletes the event. |
| Event # | System-assigned display order number for the event. |
| Day offset and offset range | Shown only when the Scheduling module or MyCap is enabled. Events are then ordered by day offset rather than by drag order. |
| Event Label | The human-readable name of the event, up to 30 characters. Keep it unique within the arm — REDCap checks this when you add an event on this page, but not on CSV upload. |
| Custom Event Label | Optional piping field. Enter a variable name in brackets (e.g., `[visit_date]`) to display that value in the event label during data entry. |
| Unique Event Name | Auto-generated from the arm number and event label. Used in logic references. Read-only; changes when the event label is renamed. |
| Event ID | Permanent numeric identifier. Does not change when the event label is renamed. |

> **Important:** If you rename an event label, the unique event name changes with it. Any branching logic, piping, or calculated fields that reference the old unique event name will break. Review all logic after renaming events.

### 4.3 Adding & Deleting Events

**Adding an event:** Enter an event name in the **Event label** text box at the bottom of the arm's table, optionally fill in a custom event label, and click **Add new event**.

**Deleting an event:** Click the red X icon next to the event. The last remaining event cannot be deleted. Deleting an event makes any data recorded in that event inaccessible for all records in the project. The data is hidden rather than erased and may reappear if the exact same event is restored, but restoring can have side effects — treat the deletion as irreversible and export the event's data first.

---

> **Navigation notes.** A direct link to **Define My Events** appears in the "Project Home and Design" section of the left-hand menu from **15.3.3** (repositioned slightly in 15.4.0 for consistency with earlier layouts). From **15.4.5**, icons distinguish repeating instruments from repeating events on Define My Events, Designate Forms and the Online Designer.

> **Version caveat (17.6 Standard; not in LTS 17.3 or 16):** The direct left-hand-menu link to **Designate Instruments for My Events** and the **Print Page** button on that page are Standard-release features (from 17.4.1 per the changelog). On LTS 17.3 or 16, open the page from Project Setup or the Define My Events page instead.

> **Version caveat (accented characters in event and DAG names, 17.3.0+):** In projects **created** on 17.3.0 or later, accented letters in Data Access Group or event labels are flattened to their unaccented equivalents when REDCap generates the **unique** name (`"Visité"` → `visite_arm_1`). Projects created earlier keep the old behaviour even after an upgrade: accented letters are simply dropped (`"Visité"` → `visit_arm_1`). A project created from an XML file carries the behaviour of the project it was exported from. Because branching logic, piping and API calls reference unique names, logic copied between an older and a newer project can silently fail to match — check the unique names, not the display labels, when moving expressions between projects.

---

## 5. Designating Instruments to Events

After defining arms and events, navigate to the **Designate Instruments for My Events** tab (accessible from the Define My Events page or via the button in Project Setup).

This page displays a matrix with instruments as rows and events as columns. A separate tab appears for each arm.

**To designate instruments:**

1. Click **Begin Editing** to unlock the checkboxes.
2. Check the box for each instrument-event combination you want to enable. Use **Select All** or **Deselect All** at the top of the table to apply changes in bulk.
3. Click **Save** to confirm your selections.

> **Critical:** Unchecking an instrument-event combination that already contains saved data will make that data inaccessible — it will no longer appear in the UI. The data is not deleted from the database and can be recovered by re-checking the combination, but treat this as a high-risk action: always verify the combination is empty, or export the data first, before removing a designation. If new data is collected in the same instrument-event combination after it was unchecked and then re-checked, there may be record-level collisions that require backend database intervention to resolve. Removing a designation also sets any active Automated Survey Invitation for that instrument and event to inactive, so review your ASIs if you later re-check the combination. If you are unsure, contact your local REDCap administrator before proceeding.

> **Important:** Always designate the first instrument in your project (the one containing the record ID field) to the very first event in each arm. REDCap stores the record ID in this instrument-event combination. Omitting it leads to problems that vary by project setup rather than to one predictable failure — reported symptoms include orphaned records and branching logic or calculations not firing as expected. Because the symptom is unpredictable and usually surfaces long after data collection starts, treat this as a setup step to verify rather than a risk to weigh.

---

## 6. Bulk Setup via CSV Upload & Download

Both the Define My Events page and the Designate Instruments page support CSV-based bulk operations, useful for projects with large numbers of events or complex instrument-event mappings.

### 6.1 Arms & Events (Define My Events page)

Access bulk options from the **Upload or download arms/events** dropdown.

> **Upload order:** When setting up a project via CSV, always upload in this sequence: **arms → events → instrument mappings**. Events reference arm numbers, so the arm must exist before events are uploaded. Instrument mappings reference unique event names, so events must exist before mappings are uploaded. Uploading out of order will cause references to fail.

> **Single-arm projects:** If your project has only one arm, you do not need to upload the arms CSV. Every project already has "Arm 1". Start with the events upload, then upload instrument mappings.

| **Option** | **Behavior** |
|---|---|
| Upload arms (CSV) | **Additive.** A row whose `arm_num` matches an existing arm updates that arm's name; any other row creates a new arm. Existing arms not in the file are unaffected. |
| Download arms (CSV) | Exports current arm configuration. Useful for backup or bulk editing. |
| Upload events (CSV) | **Additive.** A row whose `unique_event_name` matches an existing event updates that event; any other row creates a new event. Existing events not in the file are unaffected. REDCap shows a preview of the changes before you commit them. |
| Download events (CSV) | Exports current event configuration. |

> **Version caveat (LTS 16; 17.x below 17.4.3 Standard / 17.3.9 LTS):** **Download arms** only works once the project has at least two events. On these versions, add a second event first, or use the Export Arms API.

> **Note:** Arms and event uploads are additive — you can safely upload a file containing only new rows without affecting existing configuration. This is the opposite of instrument-event mapping uploads, which replace the entire mapping (see §6.2). Keep this distinction in mind when planning bulk updates. If any row references an arm that does not exist (or, for mappings, an event that does not exist), REDCap reports an error and saves nothing from the file.

#### Arms CSV format

**Columns:** `arm_num`, `name`

| **Column** | **Type** | **Notes** |
|---|---|---|
| `arm_num` | Integer 1–99 | No leading zeros. Numbers need not be consecutive, but numbering 1, 2, 3… keeps unique event names (`_arm_N`) easy to read. |
| `name` | Free text, up to 50 characters | Descriptive label shown in the UI (e.g., "Control", "Intervention"). If left blank, REDCap names the arm "Arm N". |

Example:

```
arm_num,name
1,Control
2,Intervention
```

#### Events CSV format

**Core columns (always present):** `event_name`, `arm_num`, `unique_event_name`, `custom_event_label`

**Additional columns when the Scheduling module (or MyCap) is active:** `day_offset`, `offset_min`, `offset_max` appear between `arm_num` and `unique_event_name`.

Full column order (scheduling active): `event_name`, `arm_num`, `day_offset`, `offset_min`, `offset_max`, `unique_event_name`, `custom_event_label`

| **Column** | **Type** | **Notes** |
|---|---|---|
| `event_name` | Free text, up to 30 characters | Display label for the event. **Values containing spaces or special characters are wrapped in double quotes** in the CSV (e.g., `"3 Month"`, `"End of Study"`). |
| `arm_num` | Positive integer | Must match an existing arm. In multi-arm projects, every event must appear as a separate row for each arm — there is no single row that spans multiple arms. A 2-arm, 6-event project produces 12 rows in the events CSV. |
| `day_offset` | Integer, −9999 to 9999 | Days from the reference date (e.g., enrollment); negative values are allowed for events before it. With Scheduling or MyCap active, REDCap sorts events by `day_offset` ascending. If the column is absent, each event's row number in the file is used instead, so row order sets the display order. |
| `offset_min` | Integer ≥ 0 | Early scheduling window (days before the target date). Expressed as a positive number in the CSV — e.g., `3` means the window opens 3 days before the target date. The API Export Events endpoint returns it the same way (positive), and only when the Scheduling module is enabled. |
| `offset_max` | Integer ≥ 0 | Late scheduling window (days after the target date). Expressed as a positive number. Symmetric windows (e.g., ±14 days) appear as the same value in both columns. |
| `unique_event_name` | Snake_case string | Leave blank for new events — REDCap always generates the name from the event name and arm number and ignores any value you supply. Fill it in only to update an existing event: a value matching an existing unique event name updates that event instead of creating a new one. See derivation rule below. |
| `custom_event_label` | Free text or blank | Piped event label. Leave blank if not used. The column is always present in exports — even when all values are empty. |

**`unique_event_name` derivation rule:** REDCap removes punctuation and all other special characters from the event name (they are deleted, not turned into underscores), replaces each space with an underscore, lowercases the result, cuts it to 18 characters, trims leading and trailing underscores, and appends `_arm_{N}`. Consecutive underscores are not collapsed. A second event with the same result gets `b` appended, a third `c`, and so on. Examples: "Screening" → `screening_arm_1`; "3 Month" → `3_month_arm_1`; "End of Study" → `end_of_study_arm_1`; "Follow-up" → `followup_arm_1` (hyphen removed, not converted); "Ad Hoc (Visit)" → `ad_hoc_visit_arm_1` (parentheses removed); "Visit - Week 2" → `visit__week_2_arm_1` (double underscore kept); "Month 12 Follow-up Visit" → `month_12_followup_arm_1` (cut to 18 characters). A mapping upload that references a unique event name not in the project is rejected with an error and nothing in the file is saved.

- `day_offset`, `offset_min`, and `offset_max` appear in the downloaded events CSV only when the Scheduling module or MyCap is active for the project. Include them in an upload only when scheduling is in use.
- With Scheduling or MyCap active, events are ordered by `day_offset`, and events sharing the same `day_offset` are sorted alphabetically by event label — which is rarely the intended clinical order. To enforce a specific display order among same-day events, assign sequential `day_offset` values (e.g., 0, 1, 2, 3…) even if the events all occur on the same calendar day. Without Scheduling or MyCap, the order is simply the drag order on the Define My Events page.

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

### 6.2 Instrument-Event Mappings (Designate Instruments page)

Access bulk options from the **Upload or download instrument mappings** dropdown:

| **Option** | **Behavior** |
|---|---|
| Upload instrument-event mappings (CSV) | Replaces the full mapping configuration. Any instrument-event combination omitted from the file will be unchecked. The upload is refused if it would remove events that MyCap task schedules depend on. |
| Download instrument-event mappings (CSV) | Exports current mappings. Useful for backup or bulk editing. |

#### Instrument-Event Mappings CSV format

**Columns:** `arm_num`, `unique_event_name`, `form`

| **Column** | **Type** | **Notes** |
|---|---|---|
| `arm_num` | Positive integer | Arm the event belongs to. |
| `unique_event_name` | Snake_case string | Must match a `unique_event_name` that already exists in the project. Copy directly from a downloaded events CSV or the Define My Events page — do not type by hand. |
| `form` | Snake_case string | The instrument's **internal variable name**, not its display label. Found in the Data Dictionary (`form_name` column) or the Online Designer. Example: `phq9`, `medication_list`, `adverse_event_log`. |

Each row represents one instrument designated to one event. An event with five instruments assigned to it produces five rows in this file. In multi-arm projects the entire mapping is replicated per arm — arm 1 rows first, then arm 2, etc. File size scales as total (events × instruments per event) across all arms.

> **Important:** Unlike arm and event uploads, the instrument-event mapping upload is not additive — it replaces the complete mapping configuration. Omitting a mapping will uncheck it, making any data in that combination inaccessible until the combination is re-checked (see §5). Always start from a downloaded export and edit it rather than building from scratch.

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

## 7. Modifying an Existing Longitudinal Setup

Changing arms, events, or instrument designations in a project that has already collected data carries significant risk. The following actions can cause data loss or break project logic:

- Renaming event labels (changes unique event names, breaks logic references)
- Deleting events or arms (the associated data becomes inaccessible — hidden rather than erased, but treat it as lost; restoring the exact setup may bring it back with side effects)
- Removing instrument-event designations (data in that combination is hidden until the combination is re-checked; active ASIs for it are deactivated)
- Reordering events (may affect downstream workflow features; if a different event becomes the first event, REDCap warns you because the public survey is tied to the first event)

**Best practice:** Before making any changes to an active project, export the full dataset, then clone the entire project and test the modifications in the copy first. If you are unsure about the impact of a change, consult your local REDCap administrator before proceeding.

> **Institution-specific:** Production-mode changes to the longitudinal setup may require administrator approval (see §11 for what normal users can do themselves). Contact your REDCap support team before modifying the setup of an active production project. Administrators editing events in Production see a red warning on the page as a reminder.

---

## 8. Effects on Other REDCap Features

A longitudinal setup changes behavior in several other areas of REDCap. Understanding these effects before finalizing your setup will prevent surprises during data collection.

### 8.1 Branching Logic

In a standard (non-longitudinal) project, branching logic references fields by variable name alone (e.g., `[dob]`). In a longitudinal project, any reference to a variable in a *different* event must include the event's unique event name:

```
[baseline_arm_1][dob]
```

References to variables *within the same instrument or event* ("local" references) do not require the event prefix. Cross-event references without the event prefix will not evaluate correctly.

See [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) — Branching Logic Overview & Scope for full syntax details.

### 8.2 Piping

Piping follows the same rules as branching logic. Piping a variable from a different event requires the unique event name prefix. Local piping (within the same event) does not.

### 8.3 Reports & Data Exports

In a non-longitudinal project, each record produces one row in a report or export. In a longitudinal project, the output produces **one row per event per record**. A project with 10 events and 100 records will produce up to 1,000 rows.

To identify which row belongs to which event and record, REDCap adds coordinate variables to exports (e.g., `redcap_event_name`). Exports from longitudinal projects will contain many empty cells because most instruments are only designated to specific events.

**Best practice:** Use the report builder's event filters to export only the data you need for any given analysis. Exporting all data from a large longitudinal project produces unwieldy output with sparse rows.

### 8.4 Workflow Features

Automated Survey Invitations, the Survey Queue, the scheduling module, and Form Display Logic all incorporate the longitudinal event structure into their configuration. Each can be scoped to specific events. For large projects with many events, using the bulk upload options for these features is recommended.

---

## 9. Common Questions

**Q: Do I need more than one arm?**

**A:** Only if different participant cohorts follow a different event or instrument schedule. A control group and intervention group that collect the same instruments at the same time points can use a single arm. If the intervention group needs an additional instrument at every event, a second arm allows you to designate that instrument separately without affecting the control arm.

**Q: Can I add events after the project has already collected data?**

**A:** Yes. Adding new events to an existing project does not affect existing data. You will need to designate instruments to the new event and configure any relevant workflow features after adding it.

**Q: What happens if I forget to designate the first instrument to the first event?**

**A:** REDCap stores the record ID in the first instrument-event combination. Leaving it undesignated does not produce one specific documented error; in practice it produces different problems in different projects, including orphaned records and logic that fails to fire. Always designate your first instrument to your first event before collecting data.

**Q: Can the same instrument appear in multiple events?**

**A:** Yes. An instrument can be designated to as many events as needed across any arm. This is standard practice for instruments that are administered at every time point (e.g., a vitals form collected at every visit).

**Q: Can I change an event label after data collection has started?**

**A:** Technically yes, but it is strongly discouraged. Renaming an event label changes its unique event name, which will break any branching logic, piping, or calculated fields that reference the old name. Always test in a cloned project first and audit all logic before renaming.

**Q: What is the difference between a unique event name and an event ID?**

**A:** The unique event name is a readable identifier (e.g., `baseline_arm_1`) that changes if the event label is renamed. The event ID is a permanent numeric identifier that never changes. For branching logic and piping, you use the unique event name. The event ID is used in certain advanced integrations and is generated and managed by REDCap.

**Q: How does REDCap determine the display order of events?**

**A:** It depends on whether the Scheduling module or MyCap is enabled. Without either, events appear in the order you arrange them by dragging on the Define My Events page (and, for an events CSV upload, new events follow their row order in the file). With Scheduling or MyCap, events are displayed in ascending `day_offset` order, and you can only reorder them by changing offsets. When two or more events then share the same `day_offset`, REDCap sorts them alphabetically by event label — not by the order they were created or entered. This catches many users off guard when all events are at Day 0 (common in projects where events represent sequential steps rather than time-separated visits). To enforce a specific display order, assign sequential `day_offset` values (0, 1, 2, 3…) to events that would otherwise share the same offset. The difference between Day 0 and Day 1 has no practical scheduling impact but guarantees the correct display sequence.

**Q: If I upload an events CSV with only new events in it, will my existing events be deleted?**

**A:** No. The events upload is additive — REDCap adds any events in the file that do not already exist, updates any whose unique event name matches a row, and leaves events not in the file untouched. This is different from the instrument-event mapping upload, which replaces the full mapping configuration. You can safely upload a partial events file without affecting events that are already configured.

**Q: Do I need to upload an arms CSV for a single-arm project?**

**A:** No. Every project already has one arm ("Arm 1"). For single-arm projects, skip the arms upload entirely and begin with the events CSV upload, followed by the instrument-event mappings upload.

**Q: What columns does the events CSV need, and what is optional?**

**A:** The minimum required columns are `event_name`, `arm_num`, `unique_event_name`, and `custom_event_label`. Leave the `unique_event_name` column blank for new events — REDCap always generates it. The `custom_event_label` column can also be blank. If the Scheduling module or MyCap is active, the CSV will also contain `day_offset`, `offset_min`, and `offset_max` columns; include those only when scheduling is in use. Download the existing events CSV from REDCap and use it as a template to ensure the column order and names are correct.

---

## 10. Common Mistakes & Gotchas

**Disabling longitudinal mode with existing data.** Turning off longitudinal mode makes all data outside the first event inaccessible after a single confirmation prompt — nothing warns you record by record. The data is hidden rather than erased and re-enabling longitudinal mode with the exact same setup may bring it back, but restoring can have side effects, so treat it as having no undo. Never disable longitudinal mode in a project with collected data unless you have verified that all data resides in the first event, and export everything first.

**Renaming events without auditing logic.** Every reference to a renamed event's unique event name in branching logic, piping, or calculated fields will silently stop working. REDCap will not flag broken logic at the time of renaming. Always run a full logic audit after any event rename.

**Omitting the first instrument from the first event.** Failing to designate the record-ID instrument to the first event causes downstream problems whose shape depends on the project — orphaned records and mis-firing logic are the ones most often reported. This is one of the most common and consequential configuration errors in new longitudinal projects, and one of the hardest to diagnose after the fact, precisely because the symptom rarely points back at the mapping.

**Uploading instrument-event mappings expecting additive behavior.** The instrument-event mapping CSV upload replaces the entire mapping, not just the rows in the file. Uploading a partial mapping will uncheck all omitted combinations. Always download and edit the existing mapping rather than creating a file from scratch.

**Uploading events before arms in a multi-arm project.** Events reference arm numbers in the CSV. If you upload an events CSV before the corresponding arms exist, REDCap rejects the upload with an error and saves none of the events. For multi-arm projects, always upload in order: arms first, then events, then instrument-event mappings. Single-arm projects can skip the arms upload since Arm 1 is created automatically.

**Assuming exports will be one row per record.** Longitudinal exports produce one row per event per record. Many users attempt to read a longitudinal export expecting a flat structure and are surprised by the volume of rows and empty cells. Plan your analysis workflow before collecting data.

**Expecting same-day events to appear in entry order.** With the Scheduling module or MyCap active, events that share the same `day_offset` are sorted alphabetically by event label rather than by the order they were entered. For example, events named Screening, Consent, Baseline, and Randomization all at `day_offset=0` will display as Baseline → Consent → Randomization → Screening. To control display order, assign sequential `day_offset` values (0, 1, 2, 3…) to same-day events.

**Manually typing unique event names in CSV mapping files.** The unique event name REDCap generates does not always match a naive word-for-word conversion. Specifically, REDCap removes hyphens and other punctuation rather than replacing them with underscores (`"Follow-up"` becomes `followup`, not `follow_up`), keeps double underscores where a removed character sat between two spaces, cuts the name to 18 characters before adding `_arm_N`, and adds `b`, `c`… to duplicates. Hand-typed unique event names in instrument-event mapping CSVs frequently diverge from what REDCap actually generated, and the mapping upload is then rejected with an error (the referenced event doesn't exist under that name) and nothing in the file is saved. Always derive unique event names using REDCap's exact algorithm, or download the events CSV from REDCap and copy the names from there.

---

### API Access

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


## 11. Administrator Configuration

Whether project-level users can add or modify events and arms on a Production project is controlled by an administrator setting in the Control Center under System Configuration → User Settings & Defaults (see **[RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md)**, "Allow Normal Users to Add or Modify Events and Arms in Production").

The setting is enabled on a new REDCap installation, but many institutions turn it off — ask your REDCap administrators which applies to you. When it is disabled, only REDCap administrators can add or modify events and arms on a project in Production status. Users who need this change must submit a request to the REDCap support team.

When the setting is enabled, project-level users with Project Design and Setup rights can, on a Production project, add new events and arms, reorder events (only when neither the Scheduling module nor MyCap is enabled, since otherwise order follows the day offsets), and designate instruments to events that have not yet been designated. They cannot edit existing events on the Define My Events page, and an events or arms CSV upload that changes an existing event's label, offsets or custom event label, or an existing arm's name, is rejected. Only administrators can delete events or arms, enable or disable longitudinal mode, or un-designate instruments that are already designated in production.

> **Note:** Over the API, Import Arms and Import Events follow the same rule on a Production project: they are allowed when this setting is enabled, and blocked otherwise. Delete Arms, Delete Events and Import Instrument-Event Mappings are blocked for Production projects regardless of the setting; for those changes, ask an administrator or make them in the UI where permitted.

> **See also:** [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md)

---

## 12. Related Articles

- [RC-CC-04 — Control Center: User Settings & Defaults](RC-CC-04_Control-Center-User-Settings.md) (controls whether users can modify events/arms in Production)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (layering repeated instruments or events onto a longitudinal project)
- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) (navigating longitudinal records as a data entry user)
- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) (navigating repeated instances as a data entry user)
- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (setting up instruments before longitudinal configuration)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (building and managing instruments)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (how branching logic is affected by longitudinal setup)
- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md) (data entry in a longitudinal context)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (accessing Project Setup)

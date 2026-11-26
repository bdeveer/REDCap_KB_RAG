---
id: RC-IMP-09
title: Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings
domain: Data Import
applies_to:
- Longitudinal REDCap projects
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — arms,
  events and mapping CSV upload behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap'
- RC-LONG-01 — Longitudinal Project Setup
version: '1.1'
last_updated: 2026-11
related:
- id: RC-IMP-03
  title: 'CSV Upload Reference: All Bulk Upload Options in REDCap'
- id: RC-LONG-01
  title: Longitudinal Project Setup
- id: RC-API-16
  title: Export Arms API through RC-API-21 — Delete Events API
tags:
- data import
- data
synonyms:
- how do i import arms and events via csv
- upload instrument-event mappings csv
- bulk build longitudinal structure from a spreadsheet
- correct order to upload arms events and mappings
- copy a longitudinal project's event structure
- single-arm project skip the arms upload
- why does my event mapping upload fail
- import the schedule of events for a longitudinal project
---

# 1. Overview

Three CSV uploads govern the fundamental structure of a longitudinal REDCap project: arms, events, and the mapping of instruments to events. These three uploads are always used together and must be applied in a specific order. This article covers the format and gotchas for all three.

**Upload order when building from scratch:** arms → events → instrument-event mappings. Events reference arm numbers, and mappings reference unique event names — uploading out of order makes those rows fail. REDCap reports an error for a row that references an arm or event that does not exist, and saves nothing from the file.

> **Single-arm projects:** Arm 1 is created automatically when longitudinal mode is enabled. Skip the arms upload entirely — start directly with the events upload.

For a general overview of longitudinal project setup in the REDCap UI, see [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md).

---

# 2. Arms CSV

**Location:** Project Setup → Define My Events → "Upload or download arms/events" dropdown → download/upload arms.

**What it does:** Creates arms (participant cohorts or study phases) in a longitudinal project. Each row defines one arm.

**Upload behavior — Additive/update:** `arm_num` is the match key. A row whose `arm_num` matches an existing arm renames that arm to the `name` in the file; any other row creates a new arm. Existing arms not in the file are left unchanged. To delete an arm, use the Define My Events UI directly.

**Rights required:** Project Design and Setup.

## Column Reference

| Column | Required | Notes |
|---|---|---|
| `arm_num` | Yes | Integer 1–99, no leading zeros. The arm number referenced by the events upload and used in unique event names (`_arm_N`). Arm 1 is the default arm. |
| `name` | No | Display name for the arm shown in the REDCap UI (e.g., `Control`, `Intervention`). Free text, up to 50 characters. If left blank, REDCap names the arm "Arm N". |

## Example

```csv
arm_num,name
1,Control
2,Intervention
```

> **Version caveat (LTS 16; 17.x below 17.4.3 Standard / 17.3.9 LTS):** **Download arms** only works once the project has at least two events. On these versions, add a second event first, or use the Export Arms API.

---

# 3. Events CSV

**Location:** Project Setup → Define My Events → "Upload or download arms/events" dropdown → download/upload events.

**What it does:** Creates events (time points or visits) within arms. Each row defines one event.

**Upload behavior — Additive/update:** `unique_event_name` is the match key. A row whose `unique_event_name` matches an existing event updates that event (label, offsets, custom event label); a row with a blank `unique_event_name` creates a new event. Existing events not in the file are left unchanged. REDCap shows a preview of the changes before you commit them.

> **Production projects:** what non-administrators can change through this upload in production depends on an administrator setting. See [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (§11) before uploading to a production project.

**Rights required:** Project Design and Setup.

## Column Reference

The downloaded file uses this column order: `event_name`, `arm_num`, then `day_offset`, `offset_min`, `offset_max` (only when the Scheduling module or MyCap is active), then `unique_event_name`, `custom_event_label`.

### Core columns (always present)

| Column | Required | Notes |
|---|---|---|
| `event_name` | Yes | Display name for the event shown in the REDCap UI (e.g., `Baseline`, `3 Month Follow-up`). Free text, up to 30 characters. |
| `arm_num` | Yes | The arm this event belongs to. Must match an `arm_num` value in the project. |
| `unique_event_name` | Blank for new events; keep for existing events | The system identifier used in branching logic, piping, and API calls (e.g., `baseline_arm_1`). It is the match key: **leave it blank for new events** — REDCap generates the value from the event name and arm number — and **keep the downloaded value for existing events** so the row updates that event. Never hand-type it (see Common Mistakes below). |
| `custom_event_label` | No | Optional piped label displayed in place of the event name on the Record Home Page. Supports piping syntax (e.g., `[visit_date]`). Leave blank if not in use. On a row that updates an existing event, a blank value clears that event's custom label. |

### Additional columns (Scheduling module only)

| Column | Required | Notes |
|---|---|---|
| `day_offset` | No | The target day number for this event relative to a reference date (day 0). Used by the scheduling module. |
| `offset_min` | No | Minimum acceptable day offset (window start). |
| `offset_max` | No | Maximum acceptable day offset (window end). |

If the offset columns are left out of the file, each event's `day_offset` is set to its row number in the file. If the columns are present, every row needs a value: a blank offset is reported as an error.

## Example

```csv
event_name,arm_num,unique_event_name,custom_event_label
Screening,1,,
Baseline,1,,
3 Month Follow-up,1,,
6 Month Follow-up,1,,
Screening,2,,
Baseline,2,,
3 Month Follow-up,2,,
```

Note that `unique_event_name` is left blank in every row because these are all new events — REDCap will generate appropriate values on import. When editing a downloaded file, keep the existing values so the rows update those events instead of creating new ones.

---

# 4. Instrument-Event Mappings CSV

**Location:** Project Setup → Define My Events → Designate Instruments for My Events → "Upload or download instrument mappings" dropdown.

**What it does:** Defines which instruments are designated (assigned) to which events. Each row represents one instrument–event combination. Only designated combinations appear on the Record Home Page and are accessible for data entry at that event.

**Upload behavior — Replace:** Unlike the arms and events uploads, this upload **replaces the entire mapping**. Any instrument–event combination not present in the uploaded file will be unchecked. If records exist for a removed combination, that data becomes inaccessible (though it is not deleted from the database). Always download the current mapping first and edit it rather than building a new file from scratch. The upload is refused if it would remove instrument-event designations that MyCap task schedules depend on.

**Rights required:** Project Design and Setup.

## Column Reference

| Column | Required | Notes |
|---|---|---|
| `arm_num` | Yes | The arm number this mapping applies to. REDCap checks only that the arm exists; the `unique_event_name` decides which event is designated, so keep the two consistent. |
| `unique_event_name` | Yes | The system-generated unique event name (e.g., `baseline_arm_1`). Must match exactly — copy from a downloaded events CSV or from the Define My Events page, never type by hand. |
| `form` | Yes | The instrument's variable name (lowercase, underscored). Must match the `form_name` column in the project's Data Dictionary exactly. |

## Example

```csv
arm_num,unique_event_name,form
1,screening_arm_1,screening
1,screening_arm_1,demographics
1,baseline_arm_1,demographics
1,baseline_arm_1,phq9
1,3_month_followup_arm_1,phq9
2,screening_arm_2,screening
2,baseline_arm_2,phq9
```

---

# 5. Common Mistakes

**Typing unique event names by hand.** REDCap's unique event name algorithm removes hyphens rather than converting them to underscores. An event labeled "3 Month Follow-up" becomes `3_month_followup_arm_1`, not `3_month_follow_up_arm_1`. A mismatch here makes REDCap reject the mapping upload with an error, and nothing in the file is saved. Always copy unique event names from a downloaded events export or from the Define My Events page.

**Uploading the instrument-event mapping before arms and events exist.** The mapping references unique event names that must already be present in the project. If you upload the mapping file before uploading events (or before creating events in the UI), REDCap reports an error for the unknown event names and saves nothing from the file.

**Building the instrument-event mapping file from scratch instead of downloading first.** Because this upload replaces the entire mapping, any combination you omit is removed. If the project already has designations, omitting them from the file will uncheck them. Always start from a downloaded export of the current mapping.

**Uploading events to the wrong arm.** In multi-arm projects, the `arm_num` column in the events file must match the arms that already exist. If an event references a non-existent arm number, it will be rejected.

**Clearing unique_event_name when re-uploading a downloaded events file.** `unique_event_name` is how REDCap matches a row to an existing event. If you clear the column, every row is treated as a new event and the whole schedule is duplicated. Keep the downloaded values for existing events and leave the column blank only on rows for new events. Do not type a value for a new event — REDCap generates the name itself.

---

# 6. API Equivalents

All three CSV uploads have corresponding API methods.

| **Feature** | **Export** | **Import** | **Delete** |
|---|---|---|---|
| Arms | [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md) | [RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md) | [RC-API-18 — Delete Arms API](RC-API-18_Delete-Arms.md) |
| Events | [RC-API-19 — Export Events API](RC-API-19_Export-Events.md) | [RC-API-20 — Import Events API](RC-API-20_Import-Events.md) | [RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md) |
| Instrument–Event Mappings | [RC-API-10 — Export Instrument-Event Mappings API](RC-API-10_Export-Instrument-Event-Mappings.md) | [RC-API-11 — Import Instrument-Event Mappings API](RC-API-11_Import-Instrument-Event-Mappings.md) | — |

See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

---

# 7. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) (index of all CSV upload types in REDCap)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (full UI walkthrough for longitudinal configuration)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (repeating instrument and event configuration)
- [RC-API-10 — Export Instrument-Event Mappings API](RC-API-10_Export-Instrument-Event-Mappings.md)
- [RC-API-11 — Import Instrument-Event Mappings API](RC-API-11_Import-Instrument-Event-Mappings.md)
- [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md)
- [RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md)
- [RC-API-19 — Export Events API](RC-API-19_Export-Events.md)
- [RC-API-20 — Import Events API](RC-API-20_Import-Events.md)

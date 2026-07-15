

**Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings**

| **Article ID** | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | Longitudinal REDCap projects |
| **Prerequisite** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) |
| **Skill Level** | Intermediate |
| **Version** | 1.0 |
| **Last Updated** | 2026-05-07 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md) through [RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md)|
| **Synonyms** | how do i import arms and events via csv; upload instrument-event mappings csv; bulk build longitudinal structure from a spreadsheet; correct order to upload arms events and mappings; copy a longitudinal project's event structure; single-arm project skip the arms upload; why do my event references fail silently; import the schedule of events for a longitudinal project |

---

## 1. Overview

Three CSV uploads govern the fundamental structure of a longitudinal REDCap project: arms, events, and the mapping of instruments to events. These three uploads are always used together and must be applied in a specific order. This article covers the format and gotchas for all three.

**Upload order when building from scratch:** arms → events → instrument-event mappings. Events reference arm numbers, and mappings reference unique event names — uploading out of order will cause references to fail silently.

> **Single-arm projects:** Arm 1 is created automatically when longitudinal mode is enabled. Skip the arms upload entirely — start directly with the events upload.

For a general overview of longitudinal project setup in the REDCap UI, see [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md).

---

## 2. Arms CSV

**Location:** Project Setup → Define My Events → "Upload or download arms/events" dropdown → download/upload arms.

**What it does:** Creates arms (participant cohorts or study phases) in a longitudinal project. Each row defines one arm.

**Upload behavior — Additive:** REDCap adds any arms in the file that do not already exist. Existing arms not in the file are left unchanged. To rename or delete an arm, use the Define My Events UI directly.

**Rights required:** Project Design and Setup.

### Column Reference

| Column | Required | Notes |
|---|---|---|
| `arm_num` | Yes | Integer. The arm number used internally and referenced by the events upload. Arm 1 is the default arm. |
| `name` | Yes | Display name for the arm shown in the REDCap UI (e.g., `Arm 1`, `Control`, `Intervention`). Free text; no character restrictions. |

### Example

```csv
arm_num,name
1,Control
2,Intervention
```

---

## 3. Events CSV

**Location:** Project Setup → Define My Events → "Upload or download arms/events" dropdown → download/upload events.

**What it does:** Creates events (time points or visits) within arms. Each row defines one event.

**Upload behavior — Additive:** REDCap adds any events in the file that do not already exist. Existing events not in the file are left unchanged.

**Rights required:** Project Design and Setup.

### Column Reference

#### Core columns (always present)

| Column | Required | Notes |
|---|---|---|
| `event_name` | Yes | Display name for the event shown in the REDCap UI (e.g., `Baseline`, `3 Month Follow-up`). Free text. |
| `arm_num` | Yes | The arm this event belongs to. Must match an `arm_num` value in the project. |
| `unique_event_name` | Recommended blank | The system identifier used in branching logic, piping, and API calls (e.g., `baseline_arm_1`). **Leave this column blank** — REDCap auto-generates the value from the event name and arm number. Hand-typed values frequently diverge from what REDCap generates (see Common Mistakes below). |
| `custom_event_label` | No | Optional piped label displayed in place of the event name on the Record Home Page. Supports piping syntax (e.g., `[visit_date]`). Leave blank if not in use. |

#### Additional columns (Scheduling module only)

| Column | Required | Notes |
|---|---|---|
| `day_offset` | No | The target day number for this event relative to a reference date (day 0). Used by the scheduling module. |
| `offset_min` | No | Minimum acceptable day offset (window start). |
| `offset_max` | No | Maximum acceptable day offset (window end). |

### Example

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

Note that `unique_event_name` is left blank in every row — REDCap will generate appropriate values on import.

---

## 4. Instrument-Event Mappings CSV

**Location:** Project Setup → Define My Events → Designate Instruments for My Events → "Upload or download instrument mappings" dropdown.

**What it does:** Defines which instruments are designated (assigned) to which events. Each row represents one instrument–event combination. Only designated combinations appear on the Record Home Page and are accessible for data entry at that event.

**Upload behavior — Replace:** Unlike the arms and events uploads, this upload **replaces the entire mapping**. Any instrument–event combination not present in the uploaded file will be unchecked. If records exist for a removed combination, that data becomes inaccessible (though it is not deleted from the database). Always download the current mapping first and edit it rather than building a new file from scratch.

**Rights required:** Project Design and Setup.

### Column Reference

| Column | Required | Notes |
|---|---|---|
| `arm_num` | Yes | The arm number this mapping applies to. |
| `unique_event_name` | Yes | The system-generated unique event name (e.g., `baseline_arm_1`). Must match exactly — copy from a downloaded events CSV or from the Define My Events page, never type by hand. |
| `form` | Yes | The instrument's variable name (lowercase, underscored). Must match the `form_name` column in the project's Data Dictionary exactly. |

### Example

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

## 5. Common Mistakes

**Typing unique event names by hand.** REDCap's unique event name algorithm removes hyphens rather than converting them to underscores. An event labeled "3 Month Follow-up" becomes `3_month_followup_arm_1`, not `3_month_follow_up_arm_1`. A mismatch here causes the mapping row to be silently ignored — the instrument simply won't be assigned. Always copy unique event names from a downloaded events export or from the Define My Events page.

**Uploading the instrument-event mapping before arms and events exist.** The mapping references unique event names that must already be present in the project. If you upload the mapping file before uploading events (or before creating events in the UI), the rows will fail silently.

**Building the instrument-event mapping file from scratch instead of downloading first.** Because this upload replaces the entire mapping, any combination you omit is removed. If the project already has designations, omitting them from the file will uncheck them. Always start from a downloaded export of the current mapping.

**Uploading events to the wrong arm.** In multi-arm projects, the `arm_num` column in the events file must match the arms that already exist. If an event references a non-existent arm number, it will be rejected.

**Leaving unique_event_name populated in the events upload.** If you copy a downloaded events file and leave the `unique_event_name` column populated, REDCap will attempt to use those values — which may conflict with existing events or differ subtly from what REDCap would have generated. Clear the column before re-uploading a modified events file to let REDCap regenerate clean values.

---

## 6. API Equivalents

All three CSV uploads have corresponding API methods.

| **Feature** | **Export** | **Import** | **Delete** |
|---|---|---|---|
| Arms | [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md) | [RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md) | [RC-API-18 — Delete Arms API](RC-API-18_Delete-Arms.md) |
| Events | [RC-API-19 — Export Events API](RC-API-19_Export-Events.md) | [RC-API-20 — Import Events API](RC-API-20_Import-Events.md) | [RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md) |
| Instrument–Event Mappings | [RC-API-10 — Export Instrument-Event Mappings API](RC-API-10_Export-Instrument-Event-Mappings.md) | [RC-API-11 — Import Instrument-Event Mappings API](RC-API-11_Import-Instrument-Event-Mappings.md) | — |

See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

---

## 7. Related Articles

- [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md)(index of all CSV upload types in REDCap)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (full UI walkthrough for longitudinal configuration)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md)(repeating instrument and event configuration)
- [RC-API-10 — Export Instrument-Event Mappings API](RC-API-10_Export-Instrument-Event-Mappings.md)
- [RC-API-11 — Import Instrument-Event Mappings API](RC-API-11_Import-Instrument-Event-Mappings.md)
- [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md)
- [RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md)
- [RC-API-19 — Export Events API](RC-API-19_Export-Events.md)
- [RC-API-20 — Import Events API](RC-API-20_Import-Events.md)

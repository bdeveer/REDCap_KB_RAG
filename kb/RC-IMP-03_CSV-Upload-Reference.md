RC-IMP-03

**CSV Upload Reference: All Bulk Upload Options in REDCap**

| **Article ID** | RC-IMP-03 |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types; required rights vary per feature |
| **Prerequisite** | RC-IMP-01 — Data Import Overview |
| **Skill Level** | Intermediate |
| **Version** | 1.0 |
| **Last Updated** | 2026-04-16 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-IMP-01 — Data Import Overview; RC-FD-03 — Data Dictionary; RC-LONG-01 — Longitudinal Project Setup; RC-USER-02 — User Rights: Adding Users & Managing Roles; RC-DAG-01 — Data Access Groups |

---

# 1. Overview

REDCap offers CSV-based upload and download for many areas of a project — not just participant data. Knowing which settings can be managed via file upload lets you work more efficiently on large projects and move configurations between projects without rebuilding them by hand.

This article is a comprehensive reference of every REDCap setting that supports CSV upload. For each, it describes: where to find the upload option in the UI, what the upload does (additive vs. replace), and which article covers the full details.

> **CSV vs. other file types:** This article focuses on CSV uploads. REDCap also supports XML (for full project backups and record imports via CDISC ODM format) and ZIP files (for importing individual instruments). See RC-IMP-01 — Data Import Overview for coverage of those formats.

---

# 2. Quick Reference Table

| **What you're uploading** | **Location in REDCap** | **Upload behavior** | **Rights required** | **Detailed article** |
|---|---|---|---|---|
| Data Dictionary | Project Setup or Online Designer | **Replaces** all instruments and fields | Project Design and Setup | RC-FD-03 |
| Arms | Define My Events | **Additive** — adds new arms, existing unchanged | Project Design and Setup | RC-LONG-01 |
| Events | Define My Events | **Additive** — adds new events, existing unchanged | Project Design and Setup | RC-LONG-01 |
| Instrument–Event Mappings | Designate Instruments for My Events | **Replaces** entire mapping | Project Design and Setup | RC-LONG-01 |
| Record Data | Applications → Data Import Tool | Additive by default; can overwrite with setting | Data Entry rights | RC-IMP-01 |
| Users | User Rights | Additive/update | User Rights | RC-USER-02 |
| User Roles | User Rights | Additive/update | User Rights | RC-USER-02 |
| User–Role Assignments | User Rights | Additive/update | User Rights | RC-USER-02 |
| Data Access Groups (DAGs) | DAGs / User Rights | Additive/update | Data Access Groups | RC-DAG-01 |
| User–DAG Assignments | DAGs / User Rights | Additive/update | Data Access Groups | RC-DAG-01 |
| Alerts & Notifications | Alerts & Notifications | Additive — imports alert definitions | Project Design and Setup | RC-ALERT-01 |
| Automated Survey Invitations (ASI) | Online Designer → Automated Survey Invitations button | Additive/update | Project Design and Setup | RC-SURV-06 |
| Survey Queue | Online Designer → Survey Queue button | Additive/update | Project Design and Setup | RC-SURV-07 |
| Survey Settings | Online Designer → Survey Settings button | Additive/update | Project Design and Setup | RC-SURV-02 |
| Form Display Logic | Online Designer → Form Display Logic | Additive/update | Project Design and Setup | RC-FDL-01 |
| Data Quality Rules | Data Quality module | Additive/update | Project Design and Setup | RC-DQ-01 |
| Language Setups (MLM) | Multi-Language Management | Additive/update | Project Design and Setup | RC-MLM-01 |
| Randomization Allocation Table | Randomization module | Replaces active allocation table | Randomization Setup rights | RC-RAND-02 |

> **Download-only:** The Logging module supports CSV *download* but not upload.

---

# 3. Project Structure

## 3.1 Data Dictionary

**Location:** Project Setup → "Data Collection Instruments" section → Data Dictionary button; or the Online Designer header.

**What it does:** Defines all variables and instruments in the project. A single CSV file represents the complete instrument configuration — every field, label, choice, validation rule, branching logic expression, and instrument assignment lives here.

**Upload behavior — Replace:** Uploading a Data Dictionary **replaces the entire current configuration**. Variables present in the project but absent from the uploaded file are deleted, along with any data they contain.

**Key safety practice:** Always download and save a snapshot of the current Data Dictionary before uploading a modified version. This is your only recovery path if a bad upload needs to be rolled back.

**Full details:** RC-FD-03 — Data Dictionary

---

## 3.2 Instrument–Event Mappings

**Location:** Define My Events → Designate Instruments for My Events → "Upload or download instrument mappings" dropdown.

**What it does:** Defines which instruments are assigned (designated) to which events in a longitudinal project. Each row in the CSV represents one instrument–event combination.

**Upload behavior — Replace:** Unlike the arms and events uploads, the instrument–event mapping upload **replaces the entire mapping**. Any instrument–event combination omitted from the file will be unchecked — potentially deleting data if that combination had records saved in it. Always download the current mapping first and edit it rather than building a new file from scratch.

**CSV columns:** `arm_num`, `unique_event_name`, `form`

**Full details:** RC-LONG-01 — Longitudinal Project Setup, Section 6.2

---

# 4. Longitudinal Setup

## 4.1 Arms

**Location:** Define My Events → "Upload or download arms/events" dropdown.

**What it does:** Creates arms (participant cohorts) in a longitudinal project. Each row defines one arm.

**Upload behavior — Additive:** REDCap adds any arms in the file that do not already exist. Existing arms not in the file are left unchanged.

**CSV columns:** `arm_num`, `name`

> **Single-arm projects:** Arm 1 is created automatically when longitudinal mode is enabled. Skip the arms upload entirely for single-arm projects — start directly with the events upload.

**Upload order:** When setting up a longitudinal project from scratch via CSV, always upload in sequence: **arms → events → instrument-event mappings**. Events reference arm numbers, and mappings reference unique event names — uploading out of order will cause references to fail.

**Full details:** RC-LONG-01 — Longitudinal Project Setup, Section 6.1

---

## 4.2 Events

**Location:** Define My Events → "Upload or download arms/events" dropdown.

**What it does:** Creates events (time points) within arms of a longitudinal project.

**Upload behavior — Additive:** REDCap adds any events in the file that do not already exist. Existing events not in the file are left unchanged.

**CSV columns (core):** `event_name`, `arm_num`, `unique_event_name`, `custom_event_label`

- `unique_event_name` may be left blank — REDCap auto-generates it from the event name and arm number. **Recommended:** leave this column blank and let REDCap generate the value. Hand-typed unique event names frequently diverge from what REDCap generates (particularly for event names containing hyphens, which REDCap removes rather than converting to underscores).
- `custom_event_label` may be left blank if piped event labels are not in use.

**CSV columns (with Scheduling module active):** adds `day_offset`, `offset_min`, `offset_max`

**Full details:** RC-LONG-01 — Longitudinal Project Setup, Section 6.1

---

# 5. User Access & DAGs

## 5.1 Users, User Roles, and User–Role Assignments

**Location:** User Rights → "Upload or download users, roles, and assignments" button (top right of the User Rights page).

**What it does:** The bulk user management feature lets you download the current configuration of all users, roles, and role assignments as structured files, then upload modified versions to apply changes in bulk. This is useful for large projects or migrating a user configuration from another project.

**Upload behavior:** Additive/update — new users are added, existing user configurations are updated to match the file.

**Rights required:** User Rights privilege.

**Full details:** RC-USER-02 — User Rights: Adding Users & Managing Roles, Section 7

---

## 5.2 Data Access Groups (DAGs) and User–DAG Assignments

**Location:** Applications → DAGs (or User Rights → Data Access Group tab) → "Upload or download DAGs/User-DAG assignments" button.

**What it does:** Two related uploads are available here:

- **DAGs upload** — creates DAG definitions (group names). Useful for initial setup of a multi-site project.
- **User–DAG assignments upload** — assigns users to DAGs in bulk.

**Upload behavior:** Additive/update — new DAGs or assignments are added; existing ones may be updated.

**Rights required:** Data Access Groups privilege.

**Full details:** RC-DAG-01 — Data Access Groups, Section 7

---

# 6. Records (Participant Data)

## 6.1 Record Data Import

**Location:** Applications → Data Import Tool.

**What it does:** Imports participant record data in bulk from a CSV file. Any REDCap data export in CSV format can be re-imported into the same project as-is. Partial imports (specific fields or records only) are also supported.

**Upload behavior:** Additive by default — blank cells in the import file are ignored and existing values are preserved. An optional setting ("Overwrite data with blank values") can be enabled to erase existing values with blank cells.

**Required columns:**

- Record ID (always)
- `redcap_event_name` (required for longitudinal projects)
- `redcap_repeat_instrument` and `redcap_repeat_instance` (required for repeated instruments or events)
- `redcap_data_access_group` (required if the uploading user is assigned to a DAG)

**Getting the right header row:** Download the Data Import Template from within the Data Import Tool, or export existing data — both produce the correct column structure for your project.

**Important:** Clicking "Upload File" only stages a preview. The data is not saved until you scroll down and click "Import Data" on the results screen.

**Full details:** RC-IMP-01 — Data Import Overview, Sections 8 and 9

---

# 7. Other Project Configuration

## 7.1 Alerts & Notifications

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**What it does:** Exports all alert definitions from a project as a CSV file and allows importing alert configurations — useful for copying a set of alerts from one project to another or for making bulk edits outside of REDCap.

**Upload behavior:** Additive — imported alerts are added to the existing list.

**Rights required:** Project Design and Setup.

**Full details:** RC-ALERT-01 — Alerts & Notifications: Setup

---

## 7.2 Automated Survey Invitations (ASI)

**Location:** Online Designer → "Automated Survey Invitations" button (project-level, not per-instrument).

**What it does:** Exports all ASI configurations for the project as a CSV and allows re-importing them — useful for copying a complex invitation schedule from one project to another or for batch-editing invitation logic outside of REDCap.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Full details:** RC-SURV-06 — Automated Survey Invitations (ASI)

---

## 7.3 Survey Queue

**Location:** Online Designer → Survey Queue → "Upload or download survey queue" option.

**What it does:** Exports the survey queue configuration as a CSV and allows re-importing it. The survey queue defines the order and conditional logic governing which surveys are presented to a participant after completing a prior survey.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup.

**Full details:** RC-SURV-07 — Survey Queue

---

## 7.4 Survey Settings

**Location:** Online Designer → "Survey Settings" button (project-level, not per-instrument).

**What it does:** Exports the survey settings for all survey-enabled instruments in the project as a CSV and allows re-importing them. This is useful for replicating settings (e.g., auto-continue, response limits, custom completion text) across projects without reconfiguring each instrument manually.

**Upload behavior:** Additive/update — imported settings overwrite the current settings for the instruments specified in the file.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Full details:** RC-SURV-02 — Survey Settings: Basic Options & Design

---

## 7.5 Form Display Logic

**Location:** Online Designer → Form Display Logic → "Upload or download form display logic" option.

**What it does:** Exports the Form Display Logic (FDL) configuration for a project as a CSV and allows re-importing it. FDL controls which entire instruments are shown or hidden to users based on field values or user roles — distinct from branching logic, which operates at the field level.

**Upload behavior:** Additive/update — imported rules replace or update the existing FDL configuration.

**Rights required:** Project Design and Setup.

**Full details:** RC-FDL-01 — Form Display Logic

---

## 7.7 Data Quality Rules

**Location:** Applications → Data Quality → "Upload or download rules" option.

**What it does:** Allows bulk management of custom Data Quality rule definitions. Rules can be exported from one project and imported into another, or edited outside REDCap and re-uploaded.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup.

**Full details:** RC-DQ-01 — Data Quality Module

---

## 7.8 Multi-Language Management (Language Setups)

**Location:** Applications → Multi-Language Management → upload/download controls per language.

**What it does:** Exports translated field labels, choices, and other text strings for a given language as a CSV file. The translated file can be edited externally and re-imported, making it practical to send translations to an external translator without giving them REDCap access.

**Upload behavior:** Updates the translation strings for the specified language.

**Rights required:** Project Design and Setup.

**Full details:** RC-MLM-01 — Multi-Language Management

---


## 7.10 Randomization Allocation Table

**Location:** Applications → Randomization → (select model) → Upload Allocation Table.

**What it does:** Uploads the randomization allocation table — the pre-generated schedule that defines which treatment arm each randomized subject receives. The allocation table is produced externally by a statistician and uploaded to REDCap before randomization begins.

**Upload behavior — Replace:** The uploaded file replaces the current allocation table for that model. Once randomization has begun, the table is locked and cannot be replaced without resetting randomization (which requires administrator involvement).

**Rights required:** Randomization Setup rights.

**Full details:** RC-RAND-02 — Randomization Setup Guide

---

# 8. What Cannot Be Uploaded via CSV

The following are download-only or not file-based:

- **Survey Participant List** — The participant list (Survey Distribution Tool) can be exported to CSV and supports copy-pasting a list of participants to add them, but there is no CSV file upload path for participants.
- **Logging** — Logging records can be downloaded as CSV for audit purposes, but there is no upload path.
- **Repeating Instruments/Events configuration** — Which instruments or events are set as repeatable is configured through the UI popup in Project Setup, not via CSV. This configuration can be managed via API (RC-API-51, RC-API-53) but not through a file upload in the UI.
- **Report definitions** — Custom reports are created and managed in the UI only. There is no CSV export/import for report configurations.

---

# 9. Common Questions

**Q: Which CSV uploads replace the existing configuration, and which just add to it?**

**A:** The table in Section 2 lists the behavior for every upload. The critical ones to remember are the two that **replace**: the Data Dictionary (replaces all instruments and fields) and the Instrument–Event Mapping (replaces the entire designation matrix). Every other CSV upload is additive or update-only. For the two replace-type uploads, always download the current version first so you can recover from an unintended change.

**Q: Can I use these CSV uploads to copy a project setup from one project to another?**

**A:** For most configuration areas, yes — download the CSV from the source project, then upload it into the target project. This works well for Arms, Events, Instrument–Event Mappings, Alerts, Data Quality Rules, User Roles, and DAG definitions. For the Data Dictionary, you can also download from one project and upload to another, but be aware that branching logic referencing specific event names or variable names will need to be validated after the upload. For a full project copy including all data, use the XML backup feature (Project Setup → Other Functionality → Copy or back up the project).

**Q: Is there a way to undo a CSV upload?**

**A:** There is no undo button. For replace-type uploads (Data Dictionary, Instrument–Event Mappings), the recovery path is to re-upload the version you downloaded before making changes — which is why downloading a backup first is essential. For additive uploads (Arms, Events, Users, DAGs), reverting means manually removing the items that were added.

**Q: Do CSV uploads go through the change review queue in Production mode?**

**A:** It depends on the feature. Data Dictionary uploads in Production mode go through the same change queue review process as Online Designer changes — they are not live until a project administrator approves them. Most other CSV uploads (Users, DAGs, Alerts, Data Quality Rules, etc.) take effect immediately regardless of project mode, because they do not modify instrument or field definitions.

**Q: What columns do I need in my CSV file for a record data import?**

**A:** The minimum required column is the Record ID. If your project is longitudinal, you must also include `redcap_event_name`. If you have repeating instruments or events, add `redcap_repeat_instrument` and `redcap_repeat_instance`. If you are assigned to a Data Access Group, add `redcap_data_access_group`. The Data Import Tool provides a download template with the correct column structure for your specific project — use that template as a starting point rather than building a CSV from scratch.

**Q: Can I import a file exported from REDCap directly back into the same project without any changes?**

**A:** Yes. Any CSV file exported from REDCap's data export feature can be re-imported directly into the same project without modification. The column structure will be correct, including all required fields and event names. This is useful for recovering from accidental deletions, sharing participant data with external analysts (who can make edits and return the file), or migrating records between projects with the same structure.

---

# 10. Common Mistakes & Gotchas

**Uploading instrument–event mappings without downloading first.** This upload replaces the entire mapping. Building a file from scratch and uploading it will uncheck every mapping not in the file — potentially deleting data for instrument–event combinations that had records. Always start from a downloaded export of the current mapping.

**Manually typing unique event names in instrument–event mapping files.** REDCap's unique event name generation algorithm removes hyphens rather than converting them to underscores. An event labeled "Follow-up" becomes `followup_arm_1`, not `follow_up_arm_1`. Hand-typed names that don't match exactly will cause the mapping to silently fail (the event simply won't be found). Always copy unique event names from a downloaded Events CSV or from the Define My Events page.

**Uploading events before arms in a multi-arm project.** Events reference arm numbers — if the arm doesn't exist yet, REDCap cannot assign the event correctly. For multi-arm projects, always upload in order: arms → events → instrument–event mappings.

**Uploading a Data Dictionary without a backup.** The Data Dictionary upload replaces your entire instrument configuration. If you accidentally omit rows (e.g., by filtering your spreadsheet), those variables and their data are deleted on upload. Always save a dated snapshot before editing.

**Assuming "Upload File" in the Data Import Tool saves the data.** The upload step only stages a preview. The data is committed only after you scroll down and click "Import Data" at the bottom of the results screen. If you navigate away after clicking "Upload File," nothing is saved.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic alternatives to the CSV uploads described in this article. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

Most CSV upload features in REDCap have a corresponding API method that achieves the same result without a file upload. The API is especially useful for automation, scripted project setup, and system-to-system integration.

| **Feature** | **Export** | **Import** | **Delete** |
|---|---|---|---|
| Data Dictionary | RC-API-07 | RC-API-08 | — |
| Arms | RC-API-16 | RC-API-17 | RC-API-18 |
| Events | RC-API-19 | RC-API-20 | RC-API-21 |
| Instrument–Event Mappings | RC-API-10 | RC-API-11 | — |
| Repeating Instruments/Events *(API only — no UI upload)* | RC-API-51 | RC-API-53 | — |
| Record Data | RC-API-02 | RC-API-03 | RC-API-04 |
| Users | RC-API-22 | RC-API-23 | RC-API-24 |
| User Roles | RC-API-25 | RC-API-26 | RC-API-27 |
| User–Role Assignments | RC-API-55 | RC-API-56 | — |
| DAGs | RC-API-28 | RC-API-29 | RC-API-30 |
| User–DAG Assignments | RC-API-31 | RC-API-32 | — |
| Survey Participants *(export only in UI)* | RC-API-43 | — | — |

> **No API equivalent:** Alerts & Notifications, Automated Survey Invitations, Survey Queue, Survey Settings, Form Display Logic, Data Quality Rules, Multi-Language Management, and Randomization Allocation Tables do not have dedicated API methods. These must be managed through the REDCap UI or CSV upload/download.

---

# 11. Related Articles

- RC-IMP-01 — Data Import Overview (overview of all import mechanisms including XML and zip files)
- RC-FD-03 — Data Dictionary (complete Data Dictionary reference)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (column-by-column DD format reference)
- RC-LONG-01 — Longitudinal Project Setup (arms, events, and instrument–event mapping uploads)
- RC-USER-02 — User Rights: Adding Users & Managing Roles (bulk user management)
- RC-DAG-01 — Data Access Groups (bulk DAG and user–DAG assignment management)
- RC-ALERT-01 — Alerts & Notifications: Setup (alert configuration and bulk upload)
- RC-DQ-01 — Data Quality Module (data quality rule upload/download)
- RC-MLM-01 — Multi-Language Management (language CSV upload workflow)
- RC-RAND-02 — Randomization Setup Guide (allocation table upload)

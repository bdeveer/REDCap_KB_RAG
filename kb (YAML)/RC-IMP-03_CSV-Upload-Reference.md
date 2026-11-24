---
id: RC-IMP-03
title: 'CSV Upload Reference: All Bulk Upload Options in REDCap'
domain: Data Import
applies_to:
- All REDCap project types
- required rights vary per feature
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured. CSV upload behaviour checked against source code of v17.6.5 (Standard)
  / v17.3.31 and v16.0.61 (LTS)
prerequisites:
- RC-IMP-01 — Data Import Overview
version: '2.1'
last_updated: 2026-11
related:
- id: RC-IMP-01
  title: Data Import Overview
- id: RC-FD-03
  title: Data Dictionary
- id: RC-LONG-01
  title: Longitudinal Project Setup
- id: RC-USER-02
  title: 'User Rights: Adding Users & Managing Roles'
- id: RC-DAG-01
  title: Data Access Groups
tags:
- data import
- data
synonyms:
- what can i upload via csv in redcap
- list of all csv upload options
- bulk upload settings with a csv file
- import users dags or events from csv
- which redcap features support csv upload
- move configuration between projects via csv
- csv upload behavior additive vs replace
- comprehensive csv upload reference
- which csv uploads replace or overwrite
- empty csv deleted all survey settings
---

# 1. Overview

REDCap offers CSV-based upload and download for many areas of a project — not just participant data. Knowing which settings can be managed via file upload lets you work more efficiently on large projects and move configurations between projects without rebuilding them by hand.

This article is a comprehensive index of every REDCap setting that supports CSV upload. For each, it describes: where to find the upload option in the UI, what the upload does (additive vs. replace), which rights are required, and which article covers the full details including the column-by-column format reference.

> **CSV vs. other file types:** This article focuses on CSV uploads. REDCap also supports XML (for full project backups and record imports via CDISC ODM format) and ZIP files (for importing individual instruments). See [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) for coverage of those formats.

---

# 2. Quick Reference Table

| **What you're uploading** | **Location in REDCap** | **Upload behavior** | **Rights required** | **Format reference** |
|---|---|---|---|---|
| Data Dictionary | Project Setup or Online Designer | **Replaces** all instruments and fields | Project Design and Setup | [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) |
| Arms | Define My Events | **Adds and updates** — new arms are added; an arm whose number matches an existing arm is renamed. Never deletes | Project Design and Setup | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
| Events | Define My Events | **Adds and updates** — new events are added; an event whose unique event name matches has its name, day offset, offset range and custom event label updated. Never deletes | Project Design and Setup | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
| Instrument–Event Mappings | Designate Instruments for My Events | **Replaces** entire mapping | Project Design and Setup | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
| Record Data | Applications → Data Import Tool | **Adds and updates** — by default, non-blank file values overwrite existing values and blank cells are skipped; with the overwrite option, blank cells also erase existing values | Data Import Tool | [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md) |
| Users | User Rights | Adds and updates; never deletes | User Rights | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) |
| User Roles | User Rights | Adds and updates; never deletes | User Rights | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) |
| User–Role Assignments | User Rights | Adds and updates; never deletes | User Rights | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) |
| Data Access Groups (DAGs) | DAGs / User Rights | Adds and updates — blank unique group name creates a DAG; an existing unique group name renames that DAG | Data Access Groups | [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) |
| User–DAG Assignments | DAGs / User Rights | Adds and updates; a blank DAG cell removes the user from their DAG | Data Access Groups (users assigned to a DAG cannot run it) | [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) |
| Alerts & Notifications | Alerts & Notifications | **Adds and updates** — blank alert ID creates a new alert; an existing alert ID updates that alert | Alerts & Notifications | [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) |
| Automated Survey Invitations (ASI) | Online Designer → Automated Survey Invitations button | Adds and updates, matched on survey + event | Project Design and Setup | [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md) |
| Survey Queue | Online Designer → Survey Queue button | Adds and updates, replacing the settings for each survey/event in the file. **An empty file can delete the whole queue** | Project Design and Setup | [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md) |
| Survey Settings | Online Designer → Survey Settings button | Adds and updates (can enable surveys). **An empty file can delete all survey settings** | Project Design and Setup | [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md) |
| Form Display Logic | Online Designer → Form Display Logic | **Replaces** all form display logic conditions. **An empty file can delete them all** | Project Design and Setup | [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md) |
| Data Quality Rules | Data Quality module | Additive — new rules are appended | Data Quality — create/edit rules (download: either Data Quality right) | [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) |
| Language Setups (MLM) | Multi-Language Management | Additive by default; optional overwrite | Project Design and Setup | [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) |
| Randomization Allocation Table | Randomization module | **Replaces** the allocation table (an administrator upload in Production appends) | Randomization Setup rights | [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md) |

> **Download-only:** The Logging module supports CSV *download* but not upload.

> **Empty-file uploads delete everything (Survey Settings, Survey Queue, Form Display Logic).** Uploading an empty file makes REDCap ask whether to delete ALL existing settings of that type — for Survey Settings the prompt reads "Delete ALL existing Survey settings?". Confirming does exactly that. For Survey Settings the deletion cascades: participant lists, response tracking, Automated Survey Invitations, the survey queue, e-Consent settings and PDF archive entries for those surveys are removed too (the response data itself is kept). This needs only Project Design and Setup rights and works in Production without review. Always download the current file first, and click Cancel if you see this prompt unexpectedly.

---

# 3. Project Structure

## 3.1 Data Dictionary

**Location:** Project Setup → "Data Collection Instruments" section → Data Dictionary button; or the Online Designer header.

**What it does:** Defines all variables and instruments in the project. A single CSV file represents the complete instrument configuration — every field, label, choice, validation rule, branching logic expression, and instrument assignment lives here.

**Upload behavior — Replace:** Uploading a Data Dictionary **replaces the entire current configuration**. Variables present in the project but absent from the uploaded file are deleted. Their data is no longer accessible in forms, reports or exports; REDCap does not purge it, and it can reappear if a field with the same variable name is created again — so deleting a field is not a way to remove sensitive data, and avoid reusing old variable names. If the upload removes a whole instrument, that instrument's event designations and form-level user rights are permanently lost.

**Key safety practice:** Always download and save a copy of the current Data Dictionary before uploading a modified version. REDCap also takes an automatic Data Dictionary snapshot before every upload (and every API metadata import); these are listed on the Project Revision History page and can be downloaded to roll back a bad upload.

**Full details:** [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)

---

# 4. Longitudinal Setup (Arms, Events, Instrument-Event Mappings)

Arms, events, and instrument-event mappings are always used together and must be uploaded in sequence. The column reference, upload order, and common mistakes for all three are covered in a single dedicated article.

- **Arms and events uploads add and update, never delete.** Arms are matched on arm number (a match is renamed); events are matched on unique event name (a match has its name, day offset, offset range and custom event label updated).
- **The mapping upload replaces the whole designation grid.** The file needs `arm_num`, `unique_event_name` and `form` columns. It fails if it would remove a mapping that a MyCap task schedule uses.
- **Production:** users who are not administrators can upload arms, events or mappings only if a Control Center setting allows it, and even then cannot remove (un-designate) an existing mapping. Otherwise they get an error and must ask an administrator.

**Full format reference:** [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md)

---

# 5. User Access & DAGs

## 5.1 Users, User Roles, and User–Role Assignments

**Location:** User Rights → "Upload or download users, roles, and assignments" button (top right of the User Rights page).

**What it does:** The bulk user management feature lets you download the current configuration of all users, roles, and role assignments as structured files, then upload modified versions to apply changes in bulk. This is useful for large projects or migrating a user configuration from another project.

**Upload behavior:** Additive/update — new users are added, existing user configurations are updated to match the file. Users, roles or assignments missing from the file are left alone; the upload never deletes them.

**Rights required:** User Rights privilege.

**Full details:** [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md), Section 7

---

## 5.2 Data Access Groups (DAGs) and User–DAG Assignments

**Location:** Applications → DAGs (or User Rights → Data Access Group tab) → "Upload or download DAGs/User-DAG assignments" button.

**What it does:** Two related uploads are available here:

- **DAGs upload** — creates DAG definitions (group names). Useful for initial setup of a multi-site project.
- **User–DAG assignments upload** — assigns users to DAGs in bulk.

**Upload behavior:** Additive/update — new DAGs or assignments are added; existing ones may be updated. Nothing is deleted.

**Rights required:** Data Access Groups privilege. Users who are themselves assigned to a DAG cannot run the User–DAG assignments upload (administrators excepted).

**DAGs CSV columns:** `data_access_group_name`, `unique_group_name` (both columns must be present)

- `data_access_group_name` — Human-readable display name (e.g., `Boston Site`). Quote values that contain spaces or commas.
- `unique_group_name` — System identifier used in all API and data entry operations. Leave blank to create a new DAG; REDCap auto-generates the unique name (lowercase, spaces → underscores) and you cannot choose it. A non-blank value must match an existing DAG in the project — that DAG is renamed to the display name in the file; a value that doesn't exist gives an error. Exports include a third column, `data_access_group_id`, which is read-only and ignored on import.
- **Copying DAGs to another project:** clear the `unique_group_name` column before uploading to the target project, otherwise every row errors because those names don't exist there yet.

**User–DAG assignments CSV columns:** `username`, `redcap_data_access_group`

- `username` — REDCap login name; must match an existing project user.
- `redcap_data_access_group` — The `unique_group_name` of the target DAG (not the display name). Leave blank to remove the user from all DAGs (grants all-DAG access). Duplicate username rows are an error.

**Full details:** [RC-API-29 — Import DAGs API](RC-API-29_Import-DAGs.md); [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md), Section 7

---

# 6. Records (Participant Data)

**Location:** Applications → Data Import Tool.

**Upload behavior:** Not purely additive. New records are created, and for existing records any non-blank value in the file **overwrites** the stored value; blank cells are skipped by default. If you choose the option to overwrite existing values with blanks, blank cells also **erase** stored values. Review the comparison screen before committing.

**Rights required:** the Data Import Tool user right.

The record data CSV has a detailed column-by-column format reference, including handling of longitudinal projects, repeating instruments, checkbox fields, and system columns. See the dedicated article:

**Full format reference:** [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md)

---

# 7. Other Project Configuration

## 7.1 Alerts & Notifications

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**What it does:** Exports all alert definitions from a project as a CSV file and allows importing alert configurations — useful for copying a set of alerts from one project to another or for making bulk edits outside of REDCap.

**Upload behavior:** Adds and updates — rows with a blank alert unique ID (the `A-nnn` value) create new alerts; rows with an existing alert ID update that alert. An ID that does not exist in the project gives the error "Unique Alert ID does not exists." — so when copying alerts to another project, clear the alert ID column first.

**Rights required:** the Alerts & Notifications user right (for both upload and download).

**Full format reference:** [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md)

---

## 7.2 Automated Survey Invitations (ASI)

**Location:** Online Designer → "Automated Survey Invitations" button (project-level, not per-instrument).

**What it does:** Exports all ASI configurations for the project as a CSV and allows re-importing them — useful for copying a complex invitation schedule from one project to another or for batch-editing invitation logic outside of REDCap.

**Upload behavior:** Additive/update — ASIs matching the `form_name`/`event_name` key are updated; others are left unchanged. An invalid or missing `event_name` does not cause an error: the row is silently applied to the project's first event, so check event names carefully. A repeating ASI copied to a project where that survey/event is not repeating has its recurrence reset.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

> **Version caveat (17.x vs 16.0 LTS):** The 17.x ASI file adds a `condition_reevaluate_send_time` column that 16.0 LTS files do not have. When moving ASI files between instances on different release lines, start from a file downloaded from the target instance.

**Full format reference:** [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md)

---

## 7.3 Survey Queue

**Location:** Online Designer → Survey Queue → "Upload or download survey queue" option.

**What it does:** Exports the survey queue configuration as a CSV and allows re-importing it. The survey queue defines the order and conditional logic governing which surveys are presented to a participant after completing a prior survey.

**Upload behavior:** Additive/update — each survey/event in the file has its queue settings replaced; surveys not in the file are unchanged. Duplicate survey/event rows and invalid events are errors. **An empty file prompts to delete the entire survey queue** (see the warning in Section 2).

**Rights required:** Project Design and Setup.

**Full format reference:** [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md)

---

## 7.4 Survey Settings

**Location:** Online Designer → download icon next to "Survey Settings" (project-level download of all survey-enabled instruments).

**What it does:** Exports the survey settings for all survey-enabled instruments in the project as a CSV and allows re-importing them. Useful for replicating settings across projects without reconfiguring each instrument manually.

**Upload behavior:** Additive/update — imported rows overwrite the current settings for the instruments named in the file, and a row for an instrument that is not yet a survey enables it as a survey. Every row must include every column; rows with the wrong number of columns are rejected.

> **Warning — empty file:** Uploading an empty Survey Settings file prompts "Delete ALL existing Survey settings?". Confirming removes the survey settings for every instrument along with their participant lists, response tracking, ASIs, survey queue, e-Consent settings and PDF archive entries (response data is kept). This works in Production with only Project Design and Setup rights. Click Cancel unless you really intend this.

**Rights required:** Project Design and Setup (at least one instrument must be survey-enabled in the project).

> **Version caveat (17.x vs 16.0 LTS):** The 17.x Survey Settings file adds a column (`end_survey_redirect_redcap_share_before_next_survey`). Because rows with the wrong column count are rejected, a file exported from 16.0 LTS will probably fail on 17.x (and vice versa). Download a fresh template from the target instance and copy your values into it.

**Full format reference:** [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md)

---

## 7.5 Form Display Logic

**Location:** Online Designer → Form Display Logic → "Upload or download form display logic" option.

**What it does:** Exports the Form Display Logic (FDL) configuration for a project as a CSV and allows re-importing it. FDL controls which entire instruments are enabled or disabled to users based on field values or user attributes — distinct from branching logic, which operates at the field level.

**Upload behavior — Replace:** The uploaded file **replaces all** existing Form Display Logic conditions; any condition not in the file is removed. Download the current file first. An empty file prompts to delete all conditions (see the warning in Section 2).

**Rights required:** Project Design and Setup.

**Full format reference:** [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md)

---

## 7.6 Data Quality Rules

**Location:** Applications → Data Quality → "Upload or download rules" option.

**What it does:** Exports all custom Data Quality rule definitions from a project as a CSV and allows re-importing them. Useful for copying a rule set from one project to another or for bulk-authoring rules outside REDCap. Default rules (A–I) are not exported.

**Upload behavior:** Additive — imported rules are appended to the existing custom rule list; existing rules are not replaced.

**Rights required:** Uploading needs the Data Quality right to create/edit rules; downloading needs either Data Quality right (create/edit or execute).

**Column reference:**

| Column | Description | Accepted Values |
|---|---|---|
| `rule_name` | Display name shown in the Data Quality module | Any text string |
| `rule_logic` | Boolean logic expression; records where this evaluates to true are flagged | Valid REDCap branching logic syntax; use `[event][field]` notation in longitudinal projects |
| `real_time_execution` | Whether the rule runs in real time as data is entered | `y` to enable; `n` or empty to disable |

> **CSV escaping:** Any `rule_logic` cell containing `""` (empty-string comparison) must double every `"`. The pattern `[field] <> ""` in REDCap logic becomes `"[field] <> """""` in the CSV (four escaped-quote characters plus one closing delimiter = five trailing `"`). Most spreadsheet apps apply this automatically; apply it manually if building the file in a text editor or code.

**Full format reference:** [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) §6 — Importing and Exporting Custom Rules

---

## 7.7 Multi-Language Management (Language Setups)

**Location:** Applications → Multi-Language Management → Export/Import buttons per language row (Languages tab), or per-instrument export icons (Forms/Surveys tab).

**File format:** JSON or CSV. REDCap calls these "Language Setups" in the UI. Translation files can be exported and imported as JSON or as CSV (CSV columns: `section`, `type`, `name`, `index`, `kind`, `text`; you choose the delimiter on export). The settings file and the snapshot contents are JSON. Two distinct file types exist: **translation files** (one per language) and a **settings file** (project-wide). Both are included in a **snapshot ZIP**. The JSON structure is described below.

**Rights required:** Project Design and Setup (Draft Mode required for Production projects).

---

### Translation File

**Filename pattern:** `REDCapTranslation_{langID}_pid{pid}_{timestamp}.json` (or `.csv`)

**What it does:** Carries all translated strings for one language. Export to send to an external translator or back up a language's current state; import to load translated strings back into the project. Imports are **additive by default** — existing translations are preserved unless "Overwrite existing translations" is selected. This means partial imports (e.g., a single instrument's export) are safe.

**Top-level envelope fields:**

| Field | Type | Description |
|---|---|---|
| `creator` | string | Always `"REDCap MLM"` — identifies the file origin |
| `version` | string | MLM module version that generated the file (e.g., `"v16.0.25"`) |
| `timestamp` | string | Export datetime in `"YYYY-MM-DD HH:MM:SS"` format |
| `instructions` | string | Human-readable import instructions (empty when exported without prompts) |
| `key` | string | Language ID (e.g., `"de"`, `"en-US"`) — must match an existing language in the target project |
| `display` | string | Language display name (e.g., `"German"`) |
| `notes` | string | Optional freetext notes about the language |
| `rtl` | boolean | Whether right-to-left rendering is enabled for this language |
| `sort` | string | Sort override value; empty string = default sort order |

**Translation array fields** (each is an array of objects; empty arrays are valid and common for base-language exports or untranslated sections):

| Field | Object shape | Content |
|---|---|---|
| `uiTranslations` | `{id, translation, hash}` | UI strings shown on data entry and survey pages (~570–580 strings for a fully translated language). `hash` is a server-side change-detection token — do not modify manually. |
| `uiOptions` | `{id, value}` | UI rendering flags. Currently two: `paging_symbols` (bool) and `submit_symbol` (bool). |
| `formTranslations` | `{id, translation}` | Instrument/form name translations. `id` is the instrument name. |
| `eventTranslations` | `{id, translation}` | Event name translations (longitudinal projects only). |
| `fieldTranslations` | *(nested)* | Field label, choice label, section header, and descriptive text translations. The largest section for content-heavy projects. |
| `matrixTranslations` | *(nested)* | Matrix group header translations. |
| `surveyTranslations` | `{id, active}` | Survey-level activation per instrument. `id` = instrument name; `active` = bool indicating whether this language is enabled for the survey. |
| `sqTranslations` | *(nested)* | Survey Queue custom message translations. |
| `asiTranslations` | *(nested)* | Automated Survey Invitation subject/body translations. |
| `alertTranslations` | *(nested)* | Alert subject/body/sender translations. |
| `mdcTranslations` | *(nested)* | Missing Data Code label translations. |
| `pdfTranslations` | *(nested)* | PDF customization text translations. |
| `protemailTranslations` | *(nested)* | Protected Email Mode customization translations. |
| `myCapTranslations` | *(nested)* | MyCap app settings translations. |

> **Base language export:** A base-language export contains metadata (`key`, `display`, etc.) and `surveyTranslations` activation flags, but `uiTranslations` and all content arrays are empty. The base language is the source text — it has no translations of its own.

> **Manual editing:** The file's instructions field explicitly states it can be edited manually. Keep the JSON structure intact. Do not alter `hash` values; REDCap uses them to detect whether source text changed after a translation was saved (triggering the "Review Changed Items" notification).

---

### Settings File

**Filename pattern:** `REDCapTranslation_Settings_pid{pid}_{timestamp}.json`

**What it does:** Captures the full project-level MLM configuration — which languages are active, which instruments are enabled per language, field/alert exclusions, language sources, and admin-controlled flags. Useful for replicating a project's MLM setup to a new project or for backup/restore of configuration (not translation content). Import via the **Import General Settings** button on the Languages tab.

> **Prerequisite:** At least one language must already exist in the target project before importing settings.

**Key fields:**

| Field | Type | Description |
|---|---|---|
| `refLang` | string | Language ID of the base (reference) language |
| `fallbackLang` | string | Language ID of the fallback language |
| `langActive` | `{langID: bool}` | Active/inactive state per language |
| `myCapActive` | `{langID: bool}` | MyCap-active state per language |
| `designatedField` | string | Field name of the Language Preference Field; empty string if not set |
| `status` | string | Project status at export time (`"dev"` = development) |
| `disabled` | boolean | Whether MLM is disabled for the project |
| `highlightMissingDataentry` | boolean | Highlight untranslated text on data entry forms |
| `highlightMissingSurvey` | boolean | Highlight untranslated text on survey pages |
| `autoDetectBrowserLang` | boolean | Enable browser language auto-detection for first-time survey respondents |
| `dataEntryEnabled` | `{instrument: {langID: bool}}` | Per-instrument, per-language data entry toggle |
| `surveyEnabled` | `{instrument: {langID: bool}}` | Per-instrument, per-language survey toggle |
| `excludedSettings` | `{instrument: {settingName: bool}}` | Survey settings excluded from translation per instrument |
| `excludedFields` | `{fieldName: bool}` | Fields excluded from translation (`false` = included, `true` = excluded) |
| `excludedAlerts` | `{alertID: bool}` | Alerts excluded from translation |
| `alertSources` | `{alertID: "field"\|"user"}` | Language source per alert: `"field"` = Language Preference Field; `"user"` = active session language |
| `asiSources` | `{instrument: "field"\|"user"}` | Language source per ASI |
| `admin-enabled` / `admin-disabled` | boolean | Admin-level enable/disable flags (read-only in the project context) |
| `allow-from-file` / `allow-from-scratch` | boolean | Admin settings controlling which initialization methods are available |
| `optional-subscription` | boolean | Admin setting for optional system language subscription |
| `allow-ui-overrides` | boolean | Admin setting allowing project-level UI string overrides |

> **Best-effort import:** The instructions field notes that import is "best-effort" — any setting not applicable at import time (e.g., a language ID that doesn't exist in the target project) is silently ignored rather than causing an error.

---

### Snapshot ZIP

**Filename pattern:** `REDCap_MLM_Snapshot_pid{pid}_{timestamp}.zip`

**Contents:** One translation JSON per language in the project plus one settings JSON. Snapshots are created automatically when a project first moves to Production and each time drafted MLM changes are approved. They can also be created manually via the **Create Snapshot** button on the Languages tab. Individual files can be extracted and re-imported to restore a previous state.

**Full details:** [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) (§7 covers export/import workflow; §3.5 covers snapshots)

---

## 7.8 Randomization Allocation Table

**Location:** Applications → Randomization → (select model) → Upload Allocation Table.

**What it does:** Uploads the randomization allocation table — the pre-generated schedule that defines which treatment arm each randomized subject receives. The allocation table is produced externally by a statistician and uploaded to REDCap before randomization begins.

**Upload behavior — Replace:** The uploaded file replaces the current allocation table for that model. Once randomization has begun in Production, the table is locked and cannot be replaced without resetting randomization (which requires administrator involvement). In Production, an administrator can upload additional allocation rows; these are **appended** to the existing table rather than replacing it.

**Rights required:** Randomization Setup rights.

> **Always use the downloaded template as the starting point.** REDCap dynamically generates the template based on the model's configuration — the column headers, stratification variables, and DAG column are specific to each project and model, and which columns are required depends on the model. Do not build this file from scratch.

**Column reference:**

| Column | Required | Description | Accepted Values |
|---|---|---|---|
| `redcap_randomization_number` | Optional | Sequential slot identifier | Leave blank (REDCap auto-assigns) or sequential integers starting at 1 |
| `redcap_randomization_group` | **Required** | Coded value of the randomization variable for this slot | Raw coded integer (e.g., `1` for Intervention, `2` for Control). Do **not** use labels. |
| `redcap_data_access_group` | Conditional | Numeric DAG ID for multi-site stratification. Only present when the model uses DAG-based site stratification. | Numeric DAG ID — **not** the `unique_group_name` text string used in DAG CSV uploads. Obtain from the template legend or via the API (`export_dags` → `data_access_group_id` field). |
| *(stratification variable columns)* | Conditional | One column per stratification variable, named after the REDCap field name. Only present when the model uses stratification. | Raw coded integer values from the field's choices. Do **not** use labels. |

> **DAG IDs vs. DAG names:** The `redcap_data_access_group` column uses numeric IDs (e.g., `4151`), not the text `unique_group_name` values used elsewhere in REDCap's DAG CSVs. These IDs appear in the legend section embedded in the downloaded template file.

> **Notes columns:** The downloaded template includes embedded notes and a coded-value legend in extra columns to the right of the data. REDCap ignores all extra columns on upload — you do not need to remove them before uploading. This makes the template safe to share with a statistician as-is.

**Allocation structure:**

Each row represents one allocation slot, consumed in order as subjects are randomized. When using stratification, the table must contain rows for every combination of stratification variable levels. The statistician generates a balanced allocation within each stratum cell; rows should be grouped by stratum combination (e.g., all slots for gender=Male/industry=Private, then gender=Male/industry=Academia, and so on across all stratum cells). Two upload slots exist — **Development** (for testing) and **Production** (for live data collection). Upload to the Development slot first and test thoroughly. The Production slot must be populated before the project can move to Production status.

**Full details:** [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md)

---

# 8. What Cannot Be Uploaded via CSV

The following are download-only or not file-based:

- **Survey Participant List** — The participant list (Survey Distribution Tool) can be exported to CSV and supports copy-pasting a list of participants to add them, but there is no CSV file upload path for participants.
- **Logging** — Logging records can be downloaded as CSV for audit purposes, but there is no upload path.
- **Repeating Instruments/Events configuration** — Which instruments or events are set as repeatable is configured through the UI popup in Project Setup, not via CSV. This configuration can be managed via API ([RC-API-51 — Export Repeating Instruments and Events API](RC-API-51_Export-Repeating-Instruments-and-Events.md), [RC-API-53 — Import Repeating Instruments and Events API](RC-API-53_Import-Repeating-Instruments-and-Events.md)) but not through a file upload in the UI.
- **Report definitions** — Custom reports are created and managed in the UI only. There is no CSV export/import for report configurations.

---

# 9. Common Questions

**Q: Which CSV uploads replace the existing configuration, and which just add to it?**

**A:** The table in Section 2 lists the behavior for every upload. Four uploads **replace**: the Data Dictionary (replaces all instruments and fields), the Instrument–Event Mapping (replaces the entire designation matrix), Form Display Logic (replaces all conditions) and the Randomization Allocation Table (except an administrator upload in Production, which appends). The other uploads add and update, but "update" matters: Arms, Events, Alerts, ASIs, Survey Settings, Survey Queue and DAG uploads change existing items that match, and a record data import overwrites existing values. In addition, an **empty** Survey Settings, Survey Queue or Form Display Logic file offers to delete everything of that type. Always download the current version first so you can recover from an unintended change.

**Q: Can I use these CSV uploads to copy a project setup from one project to another?**

**A:** For most configuration areas, yes — download the CSV from the source project, then upload it into the target project. This works well for Arms, Events, Instrument–Event Mappings, Data Quality Rules and User Roles. Two need a tweak first: for **Alerts**, clear the alert unique ID column (otherwise the upload fails with "Unique Alert ID does not exists."); for **DAGs**, clear the `unique_group_name` column so REDCap creates new DAGs instead of erroring. For ASIs, check that every `event_name` exists in the target — an unknown event silently falls back to the first event. For the Data Dictionary, you can also download from one project and upload to another, but be aware that branching logic referencing specific event names or variable names will need to be validated after the upload. For a full project copy including all data, use the XML backup feature (Project Setup → Other Functionality → Copy or back up the project).

**Q: Is there a way to undo a CSV upload?**

**A:** There is no undo button. For replace-type uploads (Data Dictionary, Instrument–Event Mappings, Form Display Logic), the recovery path is to re-upload the version you downloaded before making changes — which is why downloading a backup first is essential. For the Data Dictionary, REDCap also keeps an automatic snapshot taken before every upload, downloadable from Project Revision History. For add-and-update uploads (Arms, Events, Users, DAGs, Alerts), reverting means manually removing the items that were added and re-uploading your earlier file to restore items that were changed.

**Q: Do CSV uploads go through the change review queue in Production mode?**

**A:** It depends on the feature. Data Dictionary uploads in Production mode go through the same change queue review process as Online Designer changes — they are not live until a project administrator approves them. Most other CSV uploads (Users, DAGs, Alerts, Data Quality Rules, Survey Settings, Survey Queue, Form Display Logic, etc.) take effect immediately regardless of project mode, because they do not modify instrument or field definitions — including the empty-file "delete all" option for Survey Settings, Survey Queue and Form Display Logic. Arms, events and instrument–event mappings are different: in Production, non-administrators can upload them only if a Control Center setting allows it.

---

# 10. Common Mistakes & Gotchas

**Uploading a Data Dictionary without a backup.** The Data Dictionary upload replaces your entire instrument configuration. If you accidentally omit rows (e.g., by filtering your spreadsheet), those variables are deleted on upload and their data is no longer accessible in forms, reports or exports. REDCap does not purge that data, and it can reappear if a field with the same variable name is created again — so deleting a field is not a way to remove sensitive data, and avoid reusing old variable names. Always save a dated copy before editing; the automatic snapshot on Project Revision History is a second safety net.

**Uploading an empty Survey Settings, Survey Queue or Form Display Logic file.** REDCap treats an empty file as a request to delete everything of that type and asks you to confirm. For Survey Settings, confirming also wipes participant lists, ASIs, the survey queue and e-Consent settings. Click Cancel if you didn't mean it.

**Treating "additive" as "safe".** Arms, events, alerts, ASIs, DAGs and record data uploads update matching existing items. A record import overwrites stored values with any non-blank values in the file.

**Longitudinal structure upload mistakes (arms, events, instrument-event mappings).** The most common mistakes — wrong upload order, hand-typed unique event names, building the mapping file from scratch — are covered in [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md)

---

## API Access

> **Note:** The following REDCap API methods provide programmatic alternatives to the CSV uploads described in this article. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

Most CSV upload features in REDCap have a corresponding API method that achieves the same result without a file upload. The API is especially useful for automation, scripted project setup, and system-to-system integration.

| **Feature** | **Export** | **Import** | **Delete** |
|---|---|---|---|
| Data Dictionary | [RC-API-07 — Export Metadata (Data Dictionary) API](RC-API-07_Export-Metadata.md) | [RC-API-08 — Import Metadata (Data Dictionary) API](RC-API-08_Import-Metadata.md) | — |
| Arms | [RC-API-16 — Export Arms API](RC-API-16_Export-Arms.md) | [RC-API-17 — Import Arms API](RC-API-17_Import-Arms.md) | [RC-API-18 — Delete Arms API](RC-API-18_Delete-Arms.md) |
| Events | [RC-API-19 — Export Events API](RC-API-19_Export-Events.md) | [RC-API-20 — Import Events API](RC-API-20_Import-Events.md) | [RC-API-21 — Delete Events API](RC-API-21_Delete-Events.md) |
| Instrument–Event Mappings | [RC-API-10 — Export Instrument-Event Mappings API](RC-API-10_Export-Instrument-Event-Mappings.md) | [RC-API-11 — Import Instrument-Event Mappings API](RC-API-11_Import-Instrument-Event-Mappings.md) | — |
| Repeating Instruments/Events *(API only — no UI upload)* | [RC-API-51 — Export Repeating Instruments and Events API](RC-API-51_Export-Repeating-Instruments-and-Events.md) | [RC-API-53 — Import Repeating Instruments and Events API](RC-API-53_Import-Repeating-Instruments-and-Events.md) | — |
| Record Data | [RC-API-02 — Export Records API](RC-API-02_Export-Records.md) | [RC-API-03 — Import Records API](RC-API-03_Import-Records.md) | [RC-API-04 — Delete Records API](RC-API-04_Delete-Records.md) |
| Users | [RC-API-22 — Export Users API](RC-API-22_Export-Users.md) | [RC-API-23 — Import Users API](RC-API-23_Import-Users.md) | [RC-API-24 — Delete Users API](RC-API-24_Delete-Users.md) |
| User Roles | [RC-API-25 — Export User Roles API](RC-API-25_Export-User-Roles.md) | [RC-API-26 — Import User Roles API](RC-API-26_Import-User-Roles.md) | [RC-API-27 — Delete User Roles API](RC-API-27_Delete-User-Roles.md) |
| User–Role Assignments | [RC-API-55 — Export User-Role Assignments API](RC-API-55_Export-User-Role-Assignments.md) | [RC-API-56 — Import User-Role Assignments API](RC-API-56_Import-User-Role-Assignments.md) | — |
| DAGs | [RC-API-28 — Export DAGs API](RC-API-28_Export-DAGs.md) | [RC-API-29 — Import DAGs API](RC-API-29_Import-DAGs.md) | [RC-API-30 — Delete DAGs API](RC-API-30_Delete-DAGs.md) |
| User–DAG Assignments | [RC-API-31 — Export User-DAG Assignments API](RC-API-31_Export-User-DAG-Assignments.md) | [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md) | — |
| Survey Participants *(export only in UI)* | [RC-API-43 — Export Survey Participants API](RC-API-43_Export-Survey-Participants.md) | — | — |

> **API arms/events override:** Unlike the UI upload, the Import Arms and Import Events API methods accept an override option that **deletes all existing arms (or events) first** and then imports the file. It is blocked in Production, but in Development it removes anything not in the file. Leave override off unless you mean to rebuild the structure.

> **No API equivalent:** Alerts & Notifications, Automated Survey Invitations, Survey Queue, Survey Settings, Form Display Logic, Data Quality Rules, Multi-Language Management, and Randomization Allocation Tables do not have dedicated API methods. These must be managed through the REDCap UI or CSV upload/download.

---

# 11. Related Articles

- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (overview of all import mechanisms including XML and zip files)
- [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md) (column reference for participant data imports)
- [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) (column reference for alert bulk upload)
- [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md) (column reference for ASI bulk upload)
- [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md) (column reference for survey settings bulk upload)
- [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md) (column reference for FDL bulk upload)
- [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) (arms, events, and instrument-event mapping format reference)
- [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md) (column reference for survey queue bulk upload)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (complete Data Dictionary reference)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (column-by-column DD format reference)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (arms, events, and instrument–event mapping uploads)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (bulk user management)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (bulk DAG and user–DAG assignment management)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (alert configuration and bulk upload)
- [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) (data quality rule upload/download)
- [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) (language CSV upload workflow)
- [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md) (allocation table upload)

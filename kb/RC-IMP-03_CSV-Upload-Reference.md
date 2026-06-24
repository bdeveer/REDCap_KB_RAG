

**CSV Upload Reference: All Bulk Upload Options in REDCap**

| **Article ID** | [RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap](RC-IMP-03_CSV-Upload-Reference.md) |
|---|---|
| **Domain** | Data Import |
| **Applies To** | All REDCap project types; required rights vary per feature |
| **Prerequisite** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) |
| **Skill Level** | Intermediate |
| **Version** | 2.0 |
| **Last Updated** | 2026-05-07 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md); [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) |
| **Synonyms** | what can i upload via csv in redcap; list of all csv upload options; bulk upload settings with a csv file; import users dags or events from csv; which redcap features support csv upload; move configuration between projects via csv; csv upload behavior additive vs replace; comprehensive csv upload reference |

---

## 1. Overview

REDCap offers CSV-based upload and download for many areas of a project — not just participant data. Knowing which settings can be managed via file upload lets you work more efficiently on large projects and move configurations between projects without rebuilding them by hand.

This article is a comprehensive index of every REDCap setting that supports CSV upload. For each, it describes: where to find the upload option in the UI, what the upload does (additive vs. replace), which rights are required, and which article covers the full details including the column-by-column format reference.

> **CSV vs. other file types:** This article focuses on CSV uploads. REDCap also supports XML (for full project backups and record imports via CDISC ODM format) and ZIP files (for importing individual instruments). See [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) for coverage of those formats.

---

## 2. Quick Reference Table

| **What you're uploading** | **Location in REDCap** | **Upload behavior** | **Rights required** | **Format reference** |
|---|---|---|---|---|
| Data Dictionary | Project Setup or Online Designer | **Replaces** all instruments and fields | Project Design and Setup | [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) |
| Arms | Define My Events | **Additive** — adds new arms, existing unchanged | Project Design and Setup | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
| Events | Define My Events | **Additive** — adds new events, existing unchanged | Project Design and Setup | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
| Instrument–Event Mappings | Designate Instruments for My Events | **Replaces** entire mapping | Project Design and Setup | [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md) |
| Record Data | Applications → Data Import Tool | Additive by default; can overwrite with setting | Data Entry rights | [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md) |
| Users | User Rights | Additive/update | User Rights | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) |
| User Roles | User Rights | Additive/update | User Rights | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) |
| User–Role Assignments | User Rights | Additive/update | User Rights | [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) |
| Data Access Groups (DAGs) | DAGs / User Rights | Additive/update | Data Access Groups | [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) |
| User–DAG Assignments | DAGs / User Rights | Additive/update | Data Access Groups | [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) |
| Alerts & Notifications | Alerts & Notifications | Additive — imports alert definitions | Project Design and Setup | [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md) |
| Automated Survey Invitations (ASI) | Online Designer → Automated Survey Invitations button | Additive/update | Project Design and Setup | [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md) |
| Survey Queue | Online Designer → Survey Queue button | Additive/update | Project Design and Setup | [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md) |
| Survey Settings | Online Designer → Survey Settings button | Additive/update | Project Design and Setup | [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md) |
| Form Display Logic | Online Designer → Form Display Logic | Additive/update | Project Design and Setup | [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md) |
| Data Quality Rules | Data Quality module | Additive/update | Project Design and Setup | [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) |
| Language Setups (MLM) | Multi-Language Management | Additive/update | Project Design and Setup | [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) |
| Randomization Allocation Table | Randomization module | Replaces active allocation table | Randomization Setup rights | [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md) |

> **Download-only:** The Logging module supports CSV *download* but not upload.

---

## 3. Project Structure

### 3.1 Data Dictionary

**Location:** Project Setup → "Data Collection Instruments" section → Data Dictionary button; or the Online Designer header.

**What it does:** Defines all variables and instruments in the project. A single CSV file represents the complete instrument configuration — every field, label, choice, validation rule, branching logic expression, and instrument assignment lives here.

**Upload behavior — Replace:** Uploading a Data Dictionary **replaces the entire current configuration**. Variables present in the project but absent from the uploaded file are deleted, along with any data they contain.

**Key safety practice:** Always download and save a snapshot of the current Data Dictionary before uploading a modified version. This is your only recovery path if a bad upload needs to be rolled back.

**Full details:** [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md)

---

## 4. Longitudinal Setup (Arms, Events, Instrument-Event Mappings)

Arms, events, and instrument-event mappings are always used together and must be uploaded in sequence. The column reference, upload order, and common mistakes for all three are covered in a single dedicated article.

**Full format reference:** [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md)

---

## 5. User Access & DAGs

### 5.1 Users, User Roles, and User–Role Assignments

**Location:** User Rights → "Upload or download users, roles, and assignments" button (top right of the User Rights page).

**What it does:** The bulk user management feature lets you download the current configuration of all users, roles, and role assignments as structured files, then upload modified versions to apply changes in bulk. This is useful for large projects or migrating a user configuration from another project.

**Upload behavior:** Additive/update — new users are added, existing user configurations are updated to match the file.

**Rights required:** User Rights privilege.

**Full details:** [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md), Section 7

---

### 5.2 Data Access Groups (DAGs) and User–DAG Assignments

**Location:** Applications → DAGs (or User Rights → Data Access Group tab) → "Upload or download DAGs/User-DAG assignments" button.

**What it does:** Two related uploads are available here:

- **DAGs upload** — creates DAG definitions (group names). Useful for initial setup of a multi-site project.
- **User–DAG assignments upload** — assigns users to DAGs in bulk.

**Upload behavior:** Additive/update — new DAGs or assignments are added; existing ones may be updated.

**Rights required:** Data Access Groups privilege.

**DAGs CSV columns:** `data_access_group_name`, `unique_group_name`

- `data_access_group_name` — Human-readable display name (e.g., `Boston Site`). Quote values that contain spaces or commas.
- `unique_group_name` — System identifier used in all API and data entry operations. Leave blank to let REDCap auto-generate it (lowercase, spaces → underscores). Exports include a third column, `data_access_group_id`, which is read-only and ignored on import.

**User–DAG assignments CSV columns:** `username`, `redcap_data_access_group`

- `username` — REDCap login name; must match an existing project user.
- `redcap_data_access_group` — The `unique_group_name` of the target DAG (not the display name). Leave blank to remove the user from all DAGs (grants all-DAG access).

**Full details:** [RC-API-29 — Import DAGs API](RC-API-29_Import-DAGs.md); [RC-API-32 — Import User-DAG Assignments API](RC-API-32_Import-User-DAG-Assignments.md); [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md), Section 7

---

## 6. Records (Participant Data)

**Location:** Applications → Data Import Tool.

The record data CSV has a detailed column-by-column format reference, including handling of longitudinal projects, repeating instruments, checkbox fields, and system columns. See the dedicated article:

**Full format reference:** [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md)

---

## 7. Other Project Configuration

### 7.1 Alerts & Notifications

**Location:** Applications → Alerts & Notifications → "Upload or download alerts" button.

**What it does:** Exports all alert definitions from a project as a CSV file and allows importing alert configurations — useful for copying a set of alerts from one project to another or for making bulk edits outside of REDCap.

**Upload behavior:** Additive — imported alerts are added to the existing list.

**Rights required:** Project Design and Setup.

**Full format reference:** [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md)

---

### 7.2 Automated Survey Invitations (ASI)

**Location:** Online Designer → "Automated Survey Invitations" button (project-level, not per-instrument).

**What it does:** Exports all ASI configurations for the project as a CSV and allows re-importing them — useful for copying a complex invitation schedule from one project to another or for batch-editing invitation logic outside of REDCap.

**Upload behavior:** Additive/update — ASIs matching the `form_name`/`event_name` key are updated; others are left unchanged.

**Rights required:** Project Design and Setup (at least one survey must be enabled in the project).

**Full format reference:** [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md)

---

### 7.3 Survey Queue

**Location:** Online Designer → Survey Queue → "Upload or download survey queue" option.

**What it does:** Exports the survey queue configuration as a CSV and allows re-importing it. The survey queue defines the order and conditional logic governing which surveys are presented to a participant after completing a prior survey.

**Upload behavior:** Additive/update.

**Rights required:** Project Design and Setup.

**Full format reference:** [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md)

---

### 7.4 Survey Settings

**Location:** Online Designer → download icon next to "Survey Settings" (project-level download of all survey-enabled instruments).

**What it does:** Exports the survey settings for all survey-enabled instruments in the project as a CSV and allows re-importing them. Useful for replicating settings across projects without reconfiguring each instrument manually.

**Upload behavior:** Additive/update — imported rows overwrite the current settings for the instruments named in the file.

**Rights required:** Project Design and Setup (at least one instrument must be survey-enabled in the project).

**Full format reference:** [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md)

---

### 7.5 Form Display Logic

**Location:** Online Designer → Form Display Logic → "Upload or download form display logic" option.

**What it does:** Exports the Form Display Logic (FDL) configuration for a project as a CSV and allows re-importing it. FDL controls which entire instruments are enabled or disabled to users based on field values or user attributes — distinct from branching logic, which operates at the field level.

**Upload behavior:** Additive/update — imported rules replace or update the existing FDL configuration.

**Rights required:** Project Design and Setup.

**Full format reference:** [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md)

---

### 7.6 Data Quality Rules

**Location:** Applications → Data Quality → "Upload or download rules" option.

**What it does:** Exports all custom Data Quality rule definitions from a project as a CSV and allows re-importing them. Useful for copying a rule set from one project to another or for bulk-authoring rules outside REDCap. Default rules (A–H) are not exported.

**Upload behavior:** Additive — imported rules are appended to the existing custom rule list; existing rules are not replaced.

**Rights required:** Project Design and Setup.

**Column reference:**

| Column | Description | Accepted Values |
|---|---|---|
| `rule_name` | Display name shown in the Data Quality module | Any text string |
| `rule_logic` | Boolean logic expression; records where this evaluates to true are flagged | Valid REDCap branching logic syntax; use `[event][field]` notation in longitudinal projects |
| `real_time_execution` | Whether the rule runs in real time as data is entered | `y` to enable; `n` or empty to disable |

> **CSV escaping:** Any `rule_logic` cell containing `""` (empty-string comparison) must double every `"`. The pattern `[field] <> ""` in REDCap logic becomes `"[field] <> """""` in the CSV (four escaped-quote characters plus one closing delimiter = five trailing `"`). Most spreadsheet apps apply this automatically; apply it manually if building the file in a text editor or code.

**Full format reference:** [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) §6 — Importing and Exporting Custom Rules

---

### 7.7 Multi-Language Management (Language Setups)

**Location:** Applications → Multi-Language Management → Export/Import buttons per language row (Languages tab), or per-instrument export icons (Forms/Surveys tab).

**File format:** JSON (not CSV). REDCap calls these "Language Setups" in the UI but all MLM files are JSON. Two distinct file types exist: **translation files** (one per language) and a **settings file** (project-wide). Both are included in a **snapshot ZIP**.

**Rights required:** Project Design and Setup (Draft Mode required for Production projects).

---

#### Translation File

**Filename pattern:** `REDCapTranslation_{langID}_{pid}_{timestamp}.json`

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

#### Settings File

**Filename pattern:** `REDCapTranslation_Settings_{pid}_{timestamp}.json`

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

#### Snapshot ZIP

**Filename pattern:** `REDCap_MLM_Snapshot_{pid}_{timestamp}.zip`

**Contents:** One translation JSON per language in the project plus one settings JSON. Snapshots are created automatically when a project first moves to Production and each time drafted MLM changes are approved. They can also be created manually via the **Create Snapshot** button on the Languages tab. Individual files can be extracted and re-imported to restore a previous state.

**Full details:** [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) (§7 covers export/import workflow; §3.5 covers snapshots)

---

### 7.8 Randomization Allocation Table

**Location:** Applications → Randomization → (select model) → Upload Allocation Table.

**What it does:** Uploads the randomization allocation table — the pre-generated schedule that defines which treatment arm each randomized subject receives. The allocation table is produced externally by a statistician and uploaded to REDCap before randomization begins.

**Upload behavior — Replace:** The uploaded file replaces the current allocation table for that model. Once randomization has begun in Production, the table is locked and cannot be replaced without resetting randomization (which requires administrator involvement).

**Rights required:** Randomization Setup rights.

> **Always use the downloaded template as the starting point.** REDCap dynamically generates the template based on the model's configuration — the column headers, stratification variables, and DAG column are specific to each project and model. Do not build this file from scratch.

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

## 8. What Cannot Be Uploaded via CSV

The following are download-only or not file-based:

- **Survey Participant List** — The participant list (Survey Distribution Tool) can be exported to CSV and supports copy-pasting a list of participants to add them, but there is no CSV file upload path for participants.
- **Logging** — Logging records can be downloaded as CSV for audit purposes, but there is no upload path.
- **Repeating Instruments/Events configuration** — Which instruments or events are set as repeatable is configured through the UI popup in Project Setup, not via CSV. This configuration can be managed via API ([RC-API-51 — Export Repeating Instruments and Events API](RC-API-51_Export-Repeating-Instruments-and-Events.md), [RC-API-53 — Import Repeating Instruments and Events API](RC-API-53_Import-Repeating-Instruments-and-Events.md)) but not through a file upload in the UI.
- **Report definitions** — Custom reports are created and managed in the UI only. There is no CSV export/import for report configurations.

---

## 9. Common Questions

**Q: Which CSV uploads replace the existing configuration, and which just add to it?**

**A:** The table in Section 2 lists the behavior for every upload. The critical ones to remember are the two that **replace**: the Data Dictionary (replaces all instruments and fields) and the Instrument–Event Mapping (replaces the entire designation matrix). Every other CSV upload is additive or update-only. For the two replace-type uploads, always download the current version first so you can recover from an unintended change.

**Q: Can I use these CSV uploads to copy a project setup from one project to another?**

**A:** For most configuration areas, yes — download the CSV from the source project, then upload it into the target project. This works well for Arms, Events, Instrument–Event Mappings, Alerts, Data Quality Rules, User Roles, and DAG definitions. For the Data Dictionary, you can also download from one project and upload to another, but be aware that branching logic referencing specific event names or variable names will need to be validated after the upload. For a full project copy including all data, use the XML backup feature (Project Setup → Other Functionality → Copy or back up the project).

**Q: Is there a way to undo a CSV upload?**

**A:** There is no undo button. For replace-type uploads (Data Dictionary, Instrument–Event Mappings), the recovery path is to re-upload the version you downloaded before making changes — which is why downloading a backup first is essential. For additive uploads (Arms, Events, Users, DAGs), reverting means manually removing the items that were added.

**Q: Do CSV uploads go through the change review queue in Production mode?**

**A:** It depends on the feature. Data Dictionary uploads in Production mode go through the same change queue review process as Online Designer changes — they are not live until a project administrator approves them. Most other CSV uploads (Users, DAGs, Alerts, Data Quality Rules, etc.) take effect immediately regardless of project mode, because they do not modify instrument or field definitions.

---

## 10. Common Mistakes & Gotchas

**Uploading a Data Dictionary without a backup.** The Data Dictionary upload replaces your entire instrument configuration. If you accidentally omit rows (e.g., by filtering your spreadsheet), those variables and their data are deleted on upload. Always save a dated snapshot before editing.

**Longitudinal structure upload mistakes (arms, events, instrument-event mappings).** The most common mistakes — wrong upload order, hand-typed unique event names, building the mapping file from scratch — are covered in [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md)

---

### API Access

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

> **No API equivalent:** Alerts & Notifications, Automated Survey Invitations, Survey Queue, Survey Settings, Form Display Logic, Data Quality Rules, Multi-Language Management, and Randomization Allocation Tables do not have dedicated API methods. These must be managed through the REDCap UI or CSV upload/download.

---

## 11. Related Articles

- [RC-IMP-01 — Data Import Overview](RC-IMP-01_Data-Import-Overview.md) (overview of all import mechanisms including XML and zip files)
- [RC-IMP-04 — Record Data CSV Import — Column Reference and Format Guide](RC-IMP-04_Record-Data-CSV-Import.md)(column reference for participant data imports)
- [RC-IMP-05 — Alerts & Notifications CSV — Column Reference and Format Guide](RC-IMP-05_Alerts-Notifications-CSV.md)(column reference for alert bulk upload)
- [RC-IMP-06 — Automated Survey Invitations CSV — Column Reference and Format Guide](RC-IMP-06_Automated-Survey-Invitations-CSV.md)(column reference for ASI bulk upload)
- [RC-IMP-07 — Survey Settings CSV — Column Reference and Format Guide](RC-IMP-07_Survey-Settings-CSV.md)(column reference for survey settings bulk upload)
- [RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md)(column reference for FDL bulk upload)
- [RC-IMP-09 — Longitudinal Structure CSV — Arms, Events, and Instrument-Event Mappings](RC-IMP-09_Longitudinal-Structure-CSV.md)(arms, events, and instrument-event mapping format reference)
- [RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md)(column reference for survey queue bulk upload)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (complete Data Dictionary reference)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (column-by-column DD format reference)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (arms, events, and instrument–event mapping uploads)
- [RC-USER-02 — User Rights: Adding Users & Managing Roles](RC-USER-02_User-Rights-Adding-Users-and-Managing-Roles.md) (bulk user management)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md) (bulk DAG and user–DAG assignment management)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (alert configuration and bulk upload)
- [RC-DQ-01 — Data Quality Module](RC-DQ-01_Data-Quality-Module.md) (data quality rule upload/download)
- [RC-MLM-01 — Multi-Language Management](RC-MLM-01_Multi-Language-Management.md) (language CSV upload workflow)
- [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md) (allocation table upload)

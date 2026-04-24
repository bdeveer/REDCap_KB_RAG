RC-CC-24

**Control Center: Edit Project Settings**

| **Article ID** | RC-CC-24 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators only |
| **Prerequisite** | RC-CC-21 — Control Center: Overview & Navigation |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-08 — Home Page, Templates & Project Defaults; RC-CC-05 — File Storage Settings; RC-CC-06 — Modules & Services Configuration; RC-PROJ-04 — Project Setup: Additional Customizations; RC-AI-01 — AI Tools Overview; RC-CDIS-01 — Clinical Data Interoperability Services |

---

# 1. Overview

The **Edit Project Settings** page (`ControlCenter/edit_project.php`) is an administrator-only tool that allows REDCap admins to view and override the governing settings for any specific project on the instance. It is accessed from the **Projects** section of the Control Center left menu.

This page is distinct from two similar-sounding areas:

- **Default Project Settings** (RC-CC-08) — sets system-wide defaults applied when *new* projects are created
- **Additional Customizations** in Project Setup (RC-PROJ-04) — project-level settings accessible to *project administrators* (users with Design & Setup rights)

Edit Project Settings exposes a superset of those settings, including ones only REDCap admins can touch (online/offline status, Twilio toggle, GDPR erasure features, per-project AI endpoint override, and system-value overrides like contact name, logo URL, and file size limits).

---

# 2. Key Concepts

**Online Status** — A project can be set to ONLINE (normal access) or OFFLINE (normal users are denied access; admins retain access). Distinct from production/development status.

**System value vs. project override** — Many settings in the lower portion of this page default to a system-wide value configured elsewhere in the Control Center. Entering a value here overrides that system default for this specific project only. Leaving the field blank means the system value applies.

**GDPR / Right to Erasure** — Two settings on this page help projects comply with data privacy regulations (such as GDPR) that require the ability to permanently delete a participant's data and audit trail.

**Double Data Entry (DDE)** — A data quality feature where two users independently enter the same data, then a Reviewer reconciles discrepancies using the Data Comparison Tool.

**Date Shifting** — A de-identification export option that shifts all date values for a record by a random number of days within a defined range. The range is configured on this page.

**Rapid Retrieval** — An internal REDCap caching mechanism that stores certain pages in temporary cache to accelerate load time when no data or metadata has changed recently. This is automated and not directly configurable.

---

# 3. Accessing the Page and Project Info Panel

Navigate to **Control Center → Projects → Edit Project Settings**. On first load, a search box appears to select a project by PID or name. Once a project is selected, the full settings form loads.

At the top of the form, REDCap displays diagnostic information about the selected project:

- **Data table** — The `redcap_dataX` table in the database where the project's records are stored (e.g., `redcap_data8`)
- **Logging table** — The `redcap_log_eventX` table used for the project's audit trail (e.g., `redcap_log_event10`)
- **Move Project Data** — A link to a tool that can migrate the project's data to a different `redcap_dataX` table. This may improve performance for projects with a very large number of records whose pages load slowly.

> **Note:** A quick-access navigation widget in the top nav bar (the PID input box) supports a shortcut: type a PID followed by `eps` (e.g., `1234 eps`) to jump directly to Edit Project Settings for that project.

---

# 4. Core Project Settings

These settings control fundamental project behavior.

| Setting | Options | Notes |
|---|---|---|
| Online Status | ONLINE / OFFLINE | OFFLINE denies access to all non-admin users |
| Language | Language file selection | Affects button labels and system text within the project |
| Character Encoding | Default (ANSI/UTF-8), Japanese (Shift JIS), Simplified Chinese, Traditional Chinese | Applied to PDF and CSV exports |
| Enable Auto-Calculations | Enabled (default) / Disabled | See below |
| Shared Library | Enabled / Disabled | Controls whether the project can import forms from the REDCap Shared Library via the Online Designer |
| Twilio SMS/Voice | Enabled / Disabled | If disabled, the Twilio option is hidden from all users in this project |

**Auto-calculations detail:** When enabled (default), server-side calculations run for calculated fields whenever data is imported via the Data Import Tool or API, and when saving a form or survey containing cross-form or cross-event calculations. When disabled, calculations only execute via JavaScript (client-side) on the data entry page itself — they do not run on API or import operations.

> **Important:** Disable auto-calculations only if they are causing significant performance issues when saving records. If disabled, some calculations may not update and must be corrected using Data Quality Rule H.

---

# 5. GDPR / Data Privacy Settings

This section contains three settings intended to support compliance with data privacy regulations (such as GDPR) that may require "right to erasure."

## 5.1 Delete Record's Logging When Deleting the Record

When enabled, users deleting a record are prompted to also delete all logged data values and actions for that record from the Project Logging page. The user must type `DELETE` to confirm. The choice is made per-record at deletion time.

- **Scope in multi-arm longitudinal projects:** Logging is deleted only for the record within the *current arm* — not across all arms.
- **Does not apply to:** Bulk "Erase all data" operations or deleting all records when moving to production. Those operations always delete all data-related log events.

## 5.2 Auto-Delete Data Export Files in the File Repository

Accepts a number of days (1–999). When set to a value greater than 0, a cron job runs every 12 hours and deletes Data Export Files in the File Repository that are older than the specified number of days.

- **Scope:** Only files under the **Data Export Files** tab of the File Repository. No other file types are affected.
- **To disable:** Set the value to 0 or leave blank.
- **Warning:** Once enabled, the cron may begin deleting files within a few hours. Enable with care.

## 5.3 Custom Survey Footer Text (Project-Level Override)

A text block displayed at the bottom of all survey pages in this specific project, overriding or supplementing the system-level default.

- **Link text (optional):** If provided, this text appears as a clickable link at the bottom of every survey page. Clicking it opens the custom text in a modal dialog. If left blank, the custom text is displayed inline instead.
- **Custom survey footer text:** The actual content. HTML is supported (styled text, links, images).

> **Note:** The system-level default custom survey footer is configured in Default Project Settings (RC-CC-08). This project-level override takes precedence for this project only.

---

# 6. AI Services — Project-Level Override

If AI Services are enabled globally (configured in **Modules & Services Configuration**, RC-CC-06), this section allows an admin to supply a *project-specific* AI endpoint that replaces the system-level configuration for this project only.

Three types of AI service are supported:

**1. Azure OpenAI (cloud-hosted) — PREFERRED**
REDCap's recommended configuration. Requires setting up a Microsoft Azure OpenAI deployment.
- Endpoint URL format: `https://{your-resource-name}.openai.azure.com/openai/deployments/[AI_DEPLOYMENT_NAME]`
- Model Version: Uses the `api-version` from the Endpoint Target URI (e.g., `2024-08-01-preview`), which may differ from the displayed model version.

**2. Additional cloud-hosted OpenAI-compatible services**
Services such as Mistral AI, Nebius AI Studio, GroqCloud, and Together AI expose an OpenAI-compatible API. Each has its own endpoint URL, API key, and model name/identifier.

> **Disclaimer:** REDCap/Vanderbilt has no affiliation with these services and cannot vouch for their security standards. Review their documentation before use.

**3. Locally-hosted OpenAI-compatible services**
Software packages such as LM Studio, LocalAI, GPT4All, and Ollama allow institutions to run open-source language models locally using the OpenAI API standard. The local installation provides its own endpoint URL. API keys may or may not apply depending on the service.

**Fields configured here:**

| Field | Notes |
|---|---|
| API Endpoint URL | The full endpoint URL for the AI service |
| API Key | Password field; may be left blank for local deployments |
| API Model Version/Name | For Azure: date string (e.g., `2024-02-01`); for others: model identifier (e.g., `mistral-tiny`, `hermes-3-llama-3.2-3b`) |

Project-level values **overwrite** any system-level AI configuration for this project.

---

# 7. Miscellaneous Project Settings

## 7.1 Names of Contact Persons

A free-text field for recording the names of people responsible for or associated with the project. This text is **not displayed anywhere within the project** — it is purely for administrative bookkeeping in the Control Center.

## 7.2 Double Data Entry Module

When enabled, two project users can be designated as **Data Entry Person #1** and **Data Entry Person #2** (assigned via the User Rights page). Each person creates records using the same record name and enters data without being able to see the other's entries. All other users are Reviewers.

Reviewers use the **Data Comparison Tool** to view differences between Person #1 and Person #2's entries and adjudicate discrepancies, producing a merged third record.

Only one person can be designated as Person #1 or #2 at a time.

## 7.3 Date Shifting De-Identification: Date Shift Range

Sets the maximum number of days used when date shifting is applied during data export. The actual shift per record is a random number between 0 and this value.

Date shifting is applied when a user selects the date-shifting de-identification option on the Data Export, Reports & Stats page.

## 7.4 DTS (Data Transfer Services)

Cannot be enabled here unless the global DTS setting has first been turned on in **Modules & Services Configuration** (RC-CC-06). If the global setting is off, this control is disabled.

## 7.5 CDIS: Allow Patient Email Address from EHR

Applies only to the **Clinical Data Mart** and **Clinical Data Pull** services within CDIS (RC-CDIS-01). Controls whether the patient's email address can be imported from the EHR for this project.

This project-level setting is only active when the global CDIS setting is configured as "Allow individual projects to decide." If the global setting is "Yes" or "No," this field is overridden and becomes read-only.

## 7.6 CDIS: Connected FHIR System

Allows selecting a specific FHIR (Fast Healthcare Interoperability Resources) system for the project, if multiple FHIR system configurations have been created on the CDIS Settings page. If set to **Default**, the first FHIR system in the list is used.

## 7.7 e-Consent: Allow Responses to Be Edited

When enabled (default), users setting up e-Consent for a survey in this project can choose whether participants' completed e-Consent responses may be modified after submission. When disabled by an admin here, modifications are prevented for all e-Consent responses in the project, regardless of how the survey is configured.

## 7.8 e-Consent: Store Non-Governed PDF Snapshots on External Storage

Applies only when the External Storage server ("The Vault") is enabled for the e-Consent Framework in **Modules & Services Configuration**.

When enabled (default): any PDF Snapshot being saved to the File Repository that contains at least one completed e-Consent response is *also* stored on the External Storage server — even if the snapshot is not itself e-Consent governed.

When disabled: only e-Consent governed PDF Snapshots are sent to the Vault for this project.

---

# 8. Custom Branding and Text

## 8.1 Display Custom Logo and Institution Name

Controls whether the institution's logo and name (configured globally in General Configuration) appear at the top of every page in this project. Default: Yes.

## 8.2 Custom Text for Project Home Page

Rich text (HTML) displayed at the top of the Project Home page for this project. Uses the TinyMCE editor. Leave blank for no custom text.

## 8.3 Custom Text for All Data Entry Pages

Rich text (HTML) displayed at the top of every data entry page in this project. Uses the TinyMCE editor. Leave blank for no custom text.

---

# 9. Custom Project Overrides (Overwrite System Values)

The fields in this section override system-wide values for this specific project. If left blank, the global/system-level value applies. The current global value is displayed beneath each field in red for reference.

| Field | Description | Typical global default |
|---|---|---|
| Name of REDCap Administrator | Support contact name shown in project interface | Configured in General Configuration |
| Email of REDCap Administrator | Support contact email | Configured in General Configuration |
| Name of Institution | Institution name shown in project pages | Configured in General Configuration |
| Name of Organization at Institution | Sub-unit or department name | Configured in General Configuration |
| Name of Grant to Cite | Displayed when users export data; leave blank if no grant | Configured in General Configuration |
| URL for Custom Logo | URL of a project-specific header logo (max 650px wide) | System logo URL |
| Min. data points for Smart Charts/Tables on public surfaces | Minimum record count before Smart Charts, Smart Tables, or Smart Functions display on public dashboards, public report instructions, survey queue text, or survey pages | 8 |
| Upload max file size — file fields | Maximum file size (MB) for File Upload fields on forms/surveys | 128 MB |
| Upload max file size — general attachments | Maximum file size (MB) for Descriptive field attachments and Data Resolution Workflow attachments | 128 MB |
| File Repository upload max file size | Maximum file size (MB) for files uploaded to the File Repository | 128 MB |
| File Repository total storage limit | Total MB cap for all files in the project's File Repository; set to 0 or blank to disable the cap | Blank (no limit) |
| Record Limit (development projects) | Maximum number of records allowed while project is in Development status; users see a warning once the limit is reached; 0 = use global default | 0 |

> **Note:** Changes to any of these fields take effect immediately for this project only. They do not affect other projects or the system-wide default.

---

# 10. Common Questions

**Q: What is the difference between Edit Project Settings and Default Project Settings?**
Default Project Settings (Control Center → System Configuration) set the system-wide defaults applied when *any new project* is created. Edit Project Settings modifies the configuration of *one specific, already-existing* project. Changes here do not affect other projects, and changes to Default Project Settings do not retroactively update existing projects.

**Q: How do I take a project offline without deleting it?**
Set Online Status to OFFLINE on this page. Normal users are denied access immediately. The project and all its data remain intact. Admins can still access the project. Change back to ONLINE when ready to restore access.

**Q: Can a project admin (non-administrator) access Edit Project Settings?**
No. This page is accessible only to REDCap system administrators. Project administrators (users with Design & Setup rights in a project) can access the Additional Customizations section of their project's Project Setup page, but they cannot reach Edit Project Settings in the Control Center.

**Q: If I disable auto-calculations for a project, what happens to existing calculated field values?**
Existing values remain as-is. Going forward, calculations will only update when a user manually saves the data entry form containing the field. Cross-form or cross-event calculations will not update via API imports or the Data Import Tool. Data Quality Rule H can be used to find and fix stale calculated values.

**Q: What does setting Online Status to OFFLINE actually do?**
Any user who is not a REDCap administrator will be unable to access the project — they will see an access-denied message. Administrators retain full access. This is useful for maintenance, archiving, or preventing accidental data entry without permanently removing user access rights.

**Q: If I set a project-level AI endpoint, does it affect the AI tools for all users in that project?**
Yes. The project-level AI configuration applies to all AI-powered features within the project (writing tools, summarization, translations) for all users. It replaces the system-level AI configuration specifically for that project.

**Q: Can I enable GDPR log deletion without also enabling the auto-delete of Data Export Files?**
Yes. The two GDPR settings are independent of each other. You can enable deletion of logging upon record deletion, enable auto-deletion of export files, or enable both — they operate separately.

**Q: How does the Date Shift Range interact with the Data Export Tool?**
When a user exports data from the Data Exports, Reports & Stats page and selects the date-shifting de-identification option, REDCap randomly shifts each record's date values by 0 to N days, where N is the Date Shift Range configured here (default: 364 days). Each record gets a different random shift, which is applied consistently to all date fields in that record during that export.

---

# 11. Common Mistakes & Gotchas

**Setting a project offline and forgetting it.** The OFFLINE status is not prominently flagged anywhere users encounter it — they simply get an access-denied message. Administrators sometimes set a project offline during maintenance and then forget to restore it. Set a reminder or add a note to the project's administrative bookkeeping (the Contact Persons field on this page).

**Enabling GDPR log deletion on an active project without communicating to the team.** Once this setting is on, any user who deletes a record will be prompted to also delete the logging history. If team members don't understand what this means — that it permanently erases audit trail data — they may inadvertently confirm the deletion. Enable this setting only after informing all users who have record-deletion rights.

**Setting an auto-delete interval too short for export files.** The cron runs every 12 hours. Setting the interval to 1 day means export files created before yesterday could disappear within hours of being created. Users expecting to return to a file the next day may find it gone. Choose an interval that accommodates your team's actual data review workflow.

**Leaving project-level AI credentials blank when system AI is configured.** If you enter an API Endpoint URL but leave the API Key blank (and the service requires one), AI tools will silently fail for users in this project. The page does not validate connectivity at save time — test the configuration after saving.

**Assuming record limit applies to production projects.** The Record Limit setting on this page applies only while the project is in **Development** status. It has no effect once the project is moved to Production. It is intended to prevent test databases from growing excessively large during development.

**Confusing project-level custom logo URL with the file-based logo upload.** The Custom Logo field here is a *URL* pointing to an image (hosted on the REDCap server or elsewhere). It does not accept a file upload. If you need to host the image on REDCap, upload it via another mechanism (e.g., the File Repository of a designated reference project) and use the resulting URL here.

---

# 12. Related Articles

- RC-CC-08 — Control Center: Home Page, Templates & Project Defaults (system-wide defaults this page can override)
- RC-CC-05 — Control Center: File Storage Settings (global file size settings)
- RC-CC-06 — Control Center: Modules & Services Configuration (global AI and Twilio settings)
- RC-CC-21 — Control Center: Overview & Navigation (CC structure and navigation)
- RC-PROJ-04 — Project Setup: Additional Customizations (project-level settings accessible to project admins)
- RC-PROJ-01 — Project Lifecycle: Status and Settings (production/development status; Draft Mode)
- RC-AI-01 — REDCap AI Tools: Overview and Security (AI features enabled by the AI settings configured here)
- RC-CDIS-01 — Clinical Data Interoperability Services: Overview & Control Center Setup (FHIR/EHR integration configured here)
- RC-TXT-02 — Texting: Administrator Setup (Twilio global configuration)

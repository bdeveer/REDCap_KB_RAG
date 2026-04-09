RC-UNCLASSIFIED-01

**Unclassified: REDCap FAQ v16.1.3 Orphaned Topics**

| **Article ID** | RC-UNCLASSIFIED-01 |
|---|---|
| **Domain** | Multiple (see sections below) |
| **Applies To** | All REDCap projects |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support (sourced from FAQ v16.1.3) |
| **Related Topics** | See per-section references below |

> **Note to KB maintainers:** This article is a holding area for content from the REDCap 16.1.3 FAQ that maps to topics not yet covered by a dedicated KB article. Each section below is a candidate for its own article. See the "Suggested New Articles" section at the end.

---

# 1. Project Lifecycle: Statuses and Transitions

## 1.1 Project Statuses

Every REDCap project exists in one of four lifecycle statuses:

**Development** — The starting state for all new projects. All design decisions are implemented in real time. All data entry and survey features can be tested. No production safeguards are in place.

**Production** — The active data collection state. Design changes require Draft Mode and a review/approval process to prevent unintentional impact on existing data. To enter Production, click the "Move project to Production" button at the bottom of the Project Setup page. At that point, REDCap prompts you to either delete all test data or retain it — best practice is to delete all test data before going live.

**Analysis/Cleanup** — Indicates that formal data collection is complete. Most features used during data collection (surveys, ASIs, Alerts & Notifications) are disabled. No new records can be created. Existing data remains intact and accessible. From Analysis/Cleanup the project can return to Production, or be moved to Completed. While in this status, an administrator can set the data to either Editable (existing records only) or Read-only/Locked.

**Completed** — Indicates the project is fully done. The project is taken offline and hidden from all users' project lists. Only a REDCap administrator can access or change status from Completed. To view completed projects, use the "Show Completed Projects" link at the bottom of the My Projects page.

> **Note on legacy statuses:** Prior to REDCap version 9.8.0 (standard) / 10.0.5 (LTS), projects used "Inactive" and "Archived" statuses. These were automatically migrated: Inactive → Analysis/Cleanup; Archived → Analysis/Cleanup within the renamed "My Hidden Projects" folder.

**Why move to Production?** Moving to Production preserves data accuracy and integrity. The post-production change control process provides a safety check to prevent accidental deletion, recoding, or overwriting of data that has already been collected.

## 1.2 Moving Back to Development

Only a REDCap administrator can move a production project back to Development status.

## 1.3 Copying a Project

Users with the right to create projects can navigate to Project Setup → Other Functionality and request a copy. When copying, REDCap presents a checklist of items that can be brought over: records, user rights, roles, alerts, reports, and so on. REDCap only shows options that are active in the source project. Project logging is **never** copied — this includes record creation timestamps, survey timestamps, and project management history.

## 1.4 Deleting a Project

Development projects can be deleted by project users via Other Functionality → Delete the project. Production projects require a deletion request, which is sent to the REDCap administrator. After an administrator deletes a project, it persists in the database for 30 days (recoverable by admin) before being permanently removed. Associated files take an additional 30 days to delete (60 days total from the user-initiated deletion).

---

# 2. Making Production Changes

## 2.1 Process Overview

To make any instrument design changes in Production, click "Enter Draft Mode" on the Online Designer or Data Dictionary page. Make changes in Draft Mode. Review a detailed summary of all drafted changes by clicking the hyperlink at the top of the page. Then click "Submit Changes for Review."

Depending on your institution's configuration, some changes are processed automatically while others require REDCap administrator approval. Review and approval times vary by institution.

## 2.2 Change Risk Flags

REDCap flags potentially harmful changes during draft review:

- **\*Possible label mismatch** — a coded value's label was changed, which may alter the meaning of existing data
- **\*Possible data loss** — a change may cause stored data to become ambiguous
- **\*Data WILL be lost** — the change will delete stored data (e.g., deleting a checkbox option)

## 2.3 Rules for Safe Production Changes

To protect your data when modifying a production database:

- **Do not rename existing variable names** — data stored for those variables will be lost. To recover, revert to the original variable name.
- **Do not rename existing form names via a data dictionary upload** — form completeness data will be lost. Form names can be changed within the Online Designer without data loss.
- **Do not modify codes for existing dropdown, radio, or checkbox choices** — existing data will be lost or misinterpreted. To reorder/add choices, keep existing codes unchanged and use the next available code number.

**Example:** If choices are `1, red | 2, yellow | 3, blue` and you want to add "green" and reorder alphabetically, do **not** recode existing choices. Instead, extend: `3, blue | 4, green | 1, red | 2, yellow`. The display order can be changed; the codes must stay the same.

**Adding choices** — Adding new options to a dropdown, radio, or checkbox field has no data impact. However, analytically it changes the question for records that already completed the instrument before the new option existed.

**Deleting choices** — Deleting a radio/dropdown option does not change stored data but removes the option from future data entry. Deleting a checkbox option **permanently deletes the stored 0/1 values for that option**. REDCap flags this as **Data WILL be lost**.

## 2.4 Project Does Not Go Offline During Review

The project does not go offline while changes are pending approval. All functionality, including survey collection and data entry, continues normally.

## 2.5 Events in Longitudinal Projects

Deleting events requires administrator action. If events are deleted, data tied to those events is not erased — it becomes "orphaned" in the system. Data for remaining events is not affected unless branching logic or calculations referenced the deleted events.

---

# 3. Data Quality Module

## 3.1 What It Does

The Data Quality module allows project users to find discrepancies in data. It provides a set of built-in default rules (including Rule H for calculated field corrections) and allows users to write custom rules. Rules use the same logic syntax as branching logic.

## 3.2 Custom Rules

Custom rules must evaluate to TRUE or FALSE — not to a value. They can include mathematical operations and any of the Special Functions listed in RC-CALC-01. Custom rules use the same syntax as branching logic.

## 3.3 Real-Time Execution

Each custom rule has a "Real Time Execution" checkbox. When enabled, the rule runs automatically every time a user saves a data entry form. If a discrepancy is found, a popup notifies the user. Real-time execution works only on data entry forms — it is **not** available for surveys.

## 3.4 Running Rules Manually

Running a rule manually evaluates all records in the project and shows the number of records matching the rule's criteria. Clicking "view" shows the specific records and instance numbers (for repeating instruments).

## 3.5 Rule H — Correcting Calculated Fields

Rule H finds calculated fields whose stored values differ from their computed values (which can occur after design changes or data imports). Running Rule H displays a button to auto-correct all such values across the entire project. This is the recommended way to fix calculated fields after modifying their equations or after a data import that affected dependent fields.

## 3.6 Data Quality vs. Branching Logic

A Data Quality custom rule must always evaluate to TRUE or FALSE. A calculated field must always result in a number. Branching logic can use similar syntax to both, but each context has distinct constraints.

---

# 4. API and Data Entry Trigger

## 4.1 The REDCap API

The REDCap API (Application Programming Interface) allows external systems to connect to REDCap programmatically for data import and export. An API token is required — requested per project via Project Setup → Other Functionality. Each user needs a separate token per project. Tokens are scoped to the user's existing rights: an API export token only provides the same data access the user has manually.

To get started: verify API user rights are granted in User Rights, request an API token, wait for approval, then use the API Playground to explore available methods and generate sample code in PHP, Python, R, Ruby, Java, cURL, or Perl.

## 4.2 The Data Entry Trigger (DET)

The Data Entry Trigger is an advanced feature that sends an HTTP POST request to a specified URL whenever any record or survey response is created or modified in the project via normal data entry (not data imports). Its primary use is notifying external systems in real time so they can take action — such as calling the API to pull updated data.

The POST payload includes: `project_id`, `username`, `instrument`, `record`, `redcap_event_name`, `redcap_data_access_group`, and `instrument_complete` status.

---

# 5. Multi-Language Management (MLM)

## 5.1 What MLM Does

Multi-Language Management (MLM) allows a project to present its interface — field labels, surveys, alerts, PDFs, and user interface text — in multiple languages simultaneously. REDCap does **not** translate content automatically; all translations must be provided by the project team. MLM is a standard feature but must be enabled per project by a REDCap administrator (or by users with Project Design rights if already enabled system-wide).

## 5.2 Languages and Fallback

The **base language** matches the project's primary language (the language used in the Online Designer). The **fallback language** is used when a translation is missing in the selected display language. If neither the selected nor the fallback translation exists for a given item, the base language displays.

## 5.3 Adding and Importing Translations

Languages can be added in three ways: from available system languages (configured by an administrator), by importing a JSON, CSV, or INI translation file, or by creating a language from scratch and adding translations manually. Translations must be saved explicitly using the yellow "Save Changes" button — MLM does not auto-save.

## 5.4 Enabling Languages for Surveys and Forms

After adding a language, it must be activated (set to "Active") on the Languages tab and then designated for specific forms/surveys on the Forms/Surveys tab. Each language must be configured independently.

## 5.5 Tracking Language Used During Data Entry

Two action tags capture which language was active during data collection:
- `@LANGUAGE-CURRENT-FORM` — records the language used in data entry mode
- `@LANGUAGE-CURRENT-SURVEY` — records the language used in survey mode

These can be added to hidden fields and later used in reports to track language distribution across records.

## 5.6 MLM Limitations

- MLM does **not** work with the REDCap Mobile App.
- MLM does **not** work with MyCap.
- Downloading instrument PDFs in a specific language is done from the MLM page, not the standard PDF download.
- Browser cookies store the respondent's last selected language preference for surveys; clearing cookies resets this preference.

---

# 6. MyCap Overview

## 6.1 What MyCap Is

MyCap is a participant-facing mobile application for continuous data collection. It allows participants to complete surveys and active tasks (activities using device sensors) on their personal iOS or Android devices, with or without internet connectivity. Data syncs to the REDCap project when connectivity is available.

MyCap is a standard built-in feature since REDCap v13.0. It may still need to be enabled at the institutional level — contact your REDCap administrator if you do not see the MyCap option.

## 6.2 MyCap vs. REDCap Mobile App

| Feature | MyCap | REDCap Mobile App |
|---|---|---|
| Installed on | Participant's personal device | Study team device |
| Requires REDCap login | No | Yes |
| Use case | Remote participant data collection over time | Offline data entry at point of care |
| Internet required | No (syncs when available) | No (syncs when available) |

## 6.3 MyCap (new, purple logo) vs. MyCap Classic (black logo)

The new MyCap app was released in September 2023 as a full rewrite (minimum REDCap v13.10.0). It adds longitudinal project support, participant dashboards, image/video capture, multi-user device support, and parity between iOS and Android for active tasks. MyCap Classic was retired in August 2024 and no longer receives updates. All new projects should direct participants to the new MyCap app.

## 6.4 Onboarding Participants

Each participant must have a record ID in REDCap before joining via the app. Access is granted through a unique QR Code (scanned using the MyCap app, not the device camera) or a Dynamic Link (a URL participants can click to join, even without the app installed — it redirects to the appropriate app store first).

Use Dynamic Links for fully remote trials. Use QR Codes for in-person setups where the study team's device displays the code. The Dynamic Link or QR Code HTML can be automatically delivered via Survey Completion Text or Alerts & Notifications.

## 6.5 Limitations

- MyCap does not support REDCap piping, smart variables, or most action tags (the `@HIDDEN` action tag is honored; MyCap has its own set of mobile-specific action tags).
- Branching logic within a single instrument is supported; cross-instrument branching is not.
- Push notifications are sent for new messages but cannot be scheduled for a future time.
- Task notifications are sent at 8 AM local device time and this time cannot currently be changed.
- MLM and piping are not supported in MyCap.

---

# 7. Suggested New KB Articles

Based on the content above and other FAQ topics not yet covered by dedicated articles, the following new articles are recommended:

| Suggested Article ID | Proposed Title | Source Content |
|---|---|---|
| RC-PROJ-01 | Project Lifecycle: Setup, Status, and Settings | Sections 1–2 above; FAQ "General Project Setup" and "Making Production Changes" sections |
| RC-DQ-01 | Data Quality Module | Section 3 above; FAQ "Data Quality Module" and "Functions for Logic in Reports" sections |
| RC-API-01 | API and Data Entry Trigger | Section 4 above; FAQ "API / Data Entry Trigger" section |
| RC-MLM-01 | Multi-Language Management (MLM) | Section 5 above (resolves ⚠️ gap already noted in KB-REFERENCE-MAP); FAQ "Multi-Language Management" section |
| RC-MYCAP-01 | MyCap: Setup and Management | Section 6 above; FAQ "MyCap" section |
| RC-DDE-01 | Double Data Entry | FAQ "Double Data Entry" section (merging records, reviewer role, exporting merged records) |
| RC-PROJ-02 | Project Dashboards | FAQ "What is a project dashboard?" section (smart charts, tables, public dashboards, wizard) |

---

# 8. Related Articles

- RC-SURV-06 — Automated Survey Invitations (ASI details)
- RC-SURV-08 — e-Consent Framework: Setup & Management
- RC-CALC-01 — Special Functions Reference (functions used in Data Quality rules)
- RC-USER-03 — User Rights: Configuring User Privileges
- RC-DAG-01 — Data Access Groups
- RC-LONG-01 — Longitudinal Project Setup
- RC-IMP-01 — Data Import Overview

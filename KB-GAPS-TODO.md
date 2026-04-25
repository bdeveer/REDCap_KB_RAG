# KB Gaps — Articles Still Needed

These articles are referenced by existing KB articles or skills but do not yet exist in the KB.

---

## Open Gaps

### ⚠️ RC-CAL-01 — Calendar

**Why needed:** REDCap includes a built-in Calendar module accessible from the project menu, but no KB article covers it. Users occasionally ask how to use it or what its limitations are.

**Domain slug:** CAL (new domain)
**What to cover:** Accessing the Calendar from the project menu, how calendar entries are created (manually vs. from scheduling fields), viewing by day/week/month, filtering by user or instrument, difference between the project calendar and the scheduling module, known limitations (not integrated with external calendars)

---

### ✅ RC-PROJ-04 — Additional Project Settings (Secondary ID, Record Label, etc.)

Resolved. Article written: `RC-PROJ-04_Project-Setup-Additional-Customizations.md`

---

### ⚠️ RC-FD-11 — Advanced Online Designer Options

**Why needed:** RC-FD-02 and RC-FD-06 cover the core Online Designer and instrument/field management. Advanced or lesser-known designer capabilities have no dedicated coverage.

**Domain slug:** FD (established)
**What to cover:** Matrix field groups (matrix of radio buttons / checkboxes); field annotation (notes visible only in designer); stop actions on required fields; section header customization; field alignment options; copy/move fields between instruments from within the designer; drag-and-drop reordering; using the designer in production (move to production implications); differences between the designer and the Data Dictionary for complex edits

---

### ⚠️ RC-LOCK-01 — Record Locking & E-Signatures

**Why needed:** Record locking is a significant REDCap feature for clinical data integrity and regulatory workflows. It is mentioned in passing in RC-DE-13 (Record Administration) but has no dedicated article. E-signature support makes this a distinct topic from simple record-level admin actions.

**Domain slug:** LOCK (new domain)
**What to cover:** What record locking does (prevents further edits to a form/record), difference between locking a single instrument vs. entire record; how to enable record locking (project-level setting, user rights required); locking and unlocking workflow; e-signature configuration and user flow; locked form indicators in the UI; interaction with Data Resolution Workflow; locking in longitudinal projects (per-event behavior); audit trail entries for lock/unlock/e-sign events; admin override capabilities

---

### ⚠️ RC-CC-22 — Admin: Imitate User (Access As)

**Why needed:** REDCap Control Center includes an "Access As" (imitate user) function that allows administrators to log in and navigate REDCap as another user. This is a powerful diagnostic and support tool with no KB coverage.

**Domain slug:** CC (established)
**What to cover:** Where to find the imitate-user function (Control Center → Users & Access Management or similar); how to initiate a session as another user; what the admin can and cannot do while imitating (project access governed by the imitated user's rights); session behavior and how to exit imitation; audit trail and logging — whether admin actions during imitation are attributed to the admin or the imitated user; appropriate use cases (troubleshooting, support); privacy and policy considerations

---

### ✅ RC-MSG-01 — REDCap Messenger

Resolved. Article written: `RC-MSG-01_REDCap-Messenger.md`

---

### ✅ RC-PROF-01 — My Profile (User Profile Settings)

Resolved 2026-04-23. Article written: `RC-PROF-01_My-Profile-User-Profile-Settings.md`

---

### ⚠️ RC-PROJ-05 — Copy Project

**Why needed:** REDCap includes a "Copy Project" function that allows users to duplicate an existing project. This is a common workflow for creating templates or starting new studies, but it has no dedicated KB coverage.

**Domain slug:** PROJ (established)
**What to cover:** Accessing Copy Project (from project header or Project Setup); options during copy (copy data records, copy user list, copy DAGs, copy reports, etc.); what is always copied vs. optional; resulting project status (Draft); limitations (survey participant lists, randomization setup, external module configurations may not carry over); use cases (templates, pilot-to-production, cloning a study arm)

---

### ⚠️ RC-PROJ-06 — Project Migrations

**Why needed:** Projects sometimes need to be moved between REDCap instances (e.g., from a test server to production, or between institutions). The process involves XML export/import and has important caveats that are not documented in the KB.

**Domain slug:** PROJ (established)
**What to cover:** When and why a migration is needed; exporting a project as XML (full vs. no-data); importing XML to create a new project on the target instance; what survives migration (structure, branching logic, surveys, user rights structure) and what does not (user accounts, data, file uploads, API tokens, external module configs, DAG assignments); post-migration checklist; migrating longitudinal projects; common pitfalls and troubleshooting

---

### ⚠️ RC-PLUS-01 — REDCap+

**Why needed:** REDCap+ (or REDCap Plus) is an extended offering beyond standard REDCap — no KB article explains what it is, how it differs from standard REDCap, or how to access its features.

**Domain slug:** PLUS (new domain)
**What to cover:** What REDCap+ is and how it relates to standard REDCap; additional features or modules included; licensing/access model; how to enable or request REDCap+ features; any relevant setup steps in Control Center; differences in user experience compared to standard REDCap

*Note: Content for this article will need to be sourced from institutional documentation or REDCap consortium materials, as REDCap+ specifics may vary by deployment.*

---

### ⚠️ RC-FREP-01 — File Repository

**Why needed:** REDCap's File Repository is a project-level file storage area for documents that are not tied to a specific record/field. It is distinct from file upload fields in instruments and has no KB coverage.

**Domain slug:** FREP (new domain)
**What to cover:** Accessing the File Repository (project menu); uploading and organizing files (folders); who can access the File Repository (user rights); downloading files; deleting files and audit trail; difference between File Repository and file upload instrument fields; using the File Repository for sharing documents with study staff; storage limits; API access to File Repository (export/import file repository file endpoints)

---

### ⚠️ RC-NOTIF-01 — REDCap System Notifications (Notification Center)

**Why needed:** REDCap has an in-app notification system (bell icon / notification center) that surfaces system messages, project activity, and admin broadcasts. This is distinct from the Alerts & Notifications module (RC-ALERT series) and has no KB coverage.

**Domain slug:** NOTIF (new domain)
**What to cover:** Where notifications appear in the UI (bell icon, notification panel); types of notifications generated (project status changes, user invitations, system messages, admin broadcasts); marking notifications as read/dismissed; admin-side: sending broadcasts or system-wide notifications via Control Center; notification preferences (if user-configurable); difference between this notification center and email-based Alerts & Notifications

---

### ⚠️ RC-SURV-10 — Survey Login (Respondent Authentication)

**Why needed:** RC-SURV-03 touches on survey access methods briefly, and RC-SURV-04 covers link types, but the Survey Login feature — which requires respondents to authenticate before accessing a survey — has no dedicated article.

**Domain slug:** SURV (established)
**What to cover:** What Survey Login is and when to use it; enabling survey login for an instrument; authentication methods (e.g., requiring a field value match such as date of birth or MRN); how respondents experience the login prompt; combining survey login with the survey queue; interaction with public vs. private survey links; troubleshooting failed logins; difference between survey login and e-consent or survey access codes

---

### ⚠️ RC-DE-13 — Record Administration (Choose Action for Record)

**Why needed:** RC-DE-01 calls out the 'Choose action for record' button as out of scope for routine data entry but provides no pointer to a covering article. No existing article covers record-level admin operations.

**Domain slug:** DE (established)
**What to cover:** Accessing 'Choose action for record' from the Record Home Page, available actions (move record to different DAG, rename/renumber record, delete record, lock/unlock record), who can perform each action (user rights required), consequences and irreversibility of deletion, audit trail behavior after admin actions

---

## Already Exists — No Action Needed

These were previously marked ⚠️ or are new additions since the last review. Listed roughly in order of when they were resolved.

### Control Center (RC-CC)

The full RC-CC series is written and on disk:

- RC-CC-01 — Notifications & Reporting ✅
- RC-CC-02 — General System Configuration ✅ *(was ⚠️)*
- RC-CC-03 — Security & Authentication Configuration ✅
- RC-CC-04 — User Settings & Defaults ✅ *(was ⚠️)*
- RC-CC-05 — File Storage & Upload Settings ✅ *(was ⚠️)*
- RC-CC-06 — Modules & Services Configuration ✅ *(was ⚠️)*
- RC-CC-07 — Users & Access Management ✅ *(was ⚠️)*
- RC-CC-08 — Home Page, Templates & Project Defaults ✅ *(was ⚠️)*
- RC-CC-09 — To-Do List ✅
- RC-CC-10 — URL Shortener ✅
- RC-CC-11 — System Statistics ✅
- RC-CC-12 — User Activity Log ✅
- RC-CC-13 — User Activity Graphs ✅
- RC-CC-14 — Map of Users ✅
- RC-CC-15 — Top Usage Report ✅
- RC-CC-16 — Database Activity Monitor ✅
- RC-CC-17 — Database Query Tool ✅
- RC-CC-18 — Custom Application Links ✅
- RC-CC-19 — Publication Matching ✅
- RC-CC-20 — Multi-Language Management ✅
- RC-CC-21 — Control Center: Overview & Navigation ✅

### Clinical Data Interoperability Services (RC-CDIS) — new domain

- RC-CDIS-01 — Clinical Data Interoperability Services: Overview & Control Center Setup ✅
- RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage ✅
- RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage ✅ *(resolves RC-IMP-02 gap)*
- RC-CDIS-04 — CDP vs CDM: Feature Comparison ✅

> **Note:** RC-IMP-02 (Clinical Data Mart Integration) was previously listed as a Priority 5 gap. It is now fully covered by the RC-CDIS domain, particularly RC-CDIS-03.

### AI Tools (RC-AI) — new domain

- RC-AI-01 — REDCap AI Tools: Overview & Security ✅
- RC-AI-02 — AI Writing Tools ✅
- RC-AI-03 — AI Translations ✅
- RC-AI-04 — AI Summarization ✅

### API (RC-API) — major expansion

RC-API-01 was previously the only API article. The full API reference series (RC-API-02 through RC-API-56) now covers every API endpoint individually. ✅

### Data Entry (RC-DE) — major expansion

RC-DE-01 was previously the only DE article. The domain now covers:

- RC-DE-02 — Basic Data Entry ✅
- RC-DE-03 — Longitudinal Projects & DAGs ✅
- RC-DE-04 — Editing Data & Audit Trail ✅
- RC-DE-05 — Field Validations ✅
- RC-DE-06 — Bio-Medical Ontologies ✅
- RC-DE-07 — Computer Adaptive Tests (CAT) ✅
- RC-DE-08 — Field Comment Log ✅
- RC-DE-09 — Data Entry with Data Access Groups ✅
- RC-DE-10 — Longitudinal & Repeated Data Entry ✅
- RC-DE-11 — Instrument Save Options ✅
- RC-DE-12 — Data Resolution Workflow ✅

### Dynamic Data Pull (RC-DDP) — new domain

- RC-DDP-01 — Dynamic Data Pull: Overview & User Guide ✅
- RC-DDP-02 — Dynamic Data Pull: Admin Setup & Technical Specs ✅

### External Modules (RC-EM) — new domain

- RC-EM-01 — External Modules: Overview & Manager ✅
- RC-EM-02 — External Modules: Installed Catalog ✅

### Data Export & Reports (RC-EXPRT) — new domain

- RC-EXPRT-01 — Data Export: Overview & Workflow ✅
- RC-EXPRT-02 — Data Export: Export Formats ✅
- RC-EXPRT-03 — Data Export: User Rights & Export Access ✅
- RC-EXPRT-04 — Data Export: De-identification & Formatting Options ✅
- RC-EXPRT-05 — Data Export: Report Types & Other Export Options ✅
- RC-EXPRT-06 — Custom Reports: Setup & Field Selection ✅
- RC-EXPRT-07 — Custom Reports: Filtering & Ordering ✅
- RC-EXPRT-08 — Custom Reports: Management & Organization ✅

### Form Design (RC-FD) — major expansion

- RC-FD-01 — Form Design Overview ✅
- RC-FD-02 — Online Designer ✅
- RC-FD-03 — Data Dictionary ✅
- RC-FD-04 — Instrument Library & Zip Files ✅
- RC-FD-05 — Codebook ✅
- RC-FD-06 — Online Designer – Instrument and Field Management ✅
- RC-FD-07 — Field Embedding ✅
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques ✅ *(was Priority 3)*
- RC-FD-09 — Field Embedding: Advanced Layout Patterns & Workflow Design ✅
- RC-FD-10 — Advanced Workflow Patterns: Multi-Stage Review and Operational Processing ✅

### Institution-Specific (RC-INST) — new domain

- RC-INST-01 — Institution-Specific Settings & Policies ✅

### Data Import (RC-IMP) — expansion

- RC-IMP-03 — CSV Upload Reference: All Bulk Upload Options in REDCap ✅

### Integration (RC-INTG) — new domain

- RC-INTG-01 — Data Entry Trigger ✅

### Navigation (RC-NAV-REC, RC-NAV-UI) — new domains

- RC-NAV-REC-01 — Record Navigation Overview ✅
- RC-NAV-REC-02 — Longitudinal Mode & Arms ✅
- RC-NAV-REC-03 — Repeated Instruments & Repeated Events ✅
- RC-NAV-REC-04 — Record Status Dashboard & Other Record Links ✅
- RC-NAV-UI-01 — Project Navigation UI ✅
- RC-NAV-UI-02 — Project Menu Reference ✅

### Piping & Smart Variables (RC-PIPE) — major expansion

- RC-PIPE-01 — Piping: Basics, Syntax & Field Types ✅
- RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers ✅
- RC-PIPE-03 — Smart Variables Overview ✅
- RC-PIPE-04 — Piping: Emails, Notifications & Logic Features ✅
- RC-PIPE-05 through RC-PIPE-17 — Smart Variables (User, Record, Form, Survey, Event & Arm, Repeating, Aggregate Functions, Optional Parameters, Randomization, Project Dashboards, Public Reports, MyCap, Miscellaneous) ✅

### Project (RC-PROJ)

- RC-PROJ-02 — Project Setup Checklist ✅
- RC-PROJ-03 — Project Dashboards ✅ *(was Priority 4)*

### Texting (RC-TXT) — new domain

- RC-TXT-01 — Texting in REDCap: Setup and Usage ✅
- RC-TXT-02 — Texting: Administrator Setup ✅

### Messaging (RC-MSG) — new domain

- RC-MSG-01 — REDCap Messenger ✅

### Project (RC-PROJ) — continued

- RC-PROJ-04 — Project Setup: Additional Customizations ✅

### Profile (RC-PROF) — new domain

- RC-PROF-01 — My Profile: User Profile Settings ✅

### Previously tracked (earlier resolved)

- RC-BL-05 — Branching Logic in Longitudinal Projects ✅
- RC-CALC-02 — Calculated Fields ✅
- RC-AT-01 through RC-AT-11, RC-AT-EM-01 — Full Action Tags series ✅
- RC-SURV-01 through RC-SURV-09 — Full Surveys series ✅
- RC-LONG-01 — Longitudinal Project Setup ✅
- RC-LONG-02 — Repeated Instruments & Events Setup ✅
- RC-FDL-01 — Form Display Logic ✅
- RC-BL-01 through RC-BL-04 — Branching Logic series ✅
- RC-RAND-01 through RC-RAND-03 — Randomization series ✅
- RC-ALERT-01, RC-ALERT-02 — Alerts & Notifications ✅
- RC-USER-01 through RC-USER-04 — User Rights series ✅
- RC-DAG-01 — Data Access Groups ✅
- RC-MLM-01 — Multi-Language Management ✅
- RC-API-01 — REDCap API ✅
- RC-PROJ-01 — Project Lifecycle: Status and Settings ✅
- RC-MYCAP-01 through RC-MYCAP-08 — Full MyCap series ✅
- RC-DQ-01 — Data Quality Module ✅
- RC-MOB-01 — REDCap Mobile App ✅
- RC-DDE-01 — Double Data Entry ✅

---

## Notes

- RC-PROJ-02 (ID) is used for "Project Setup Checklist."
- RC-ALERT-03 was resolved as an alternative alert delivery topic — covered by RC-TXT-01 and RC-TXT-02.

*Last updated: 2026-04-24 — Resolved RC-CC-23 (Backup Options). Open gaps (11): RC-DE-13, RC-CAL-01, RC-FD-11, RC-LOCK-01, RC-CC-22, RC-PROJ-05, RC-PROJ-06, RC-PLUS-01, RC-FREP-01, RC-NOTIF-01, RC-SURV-10.*

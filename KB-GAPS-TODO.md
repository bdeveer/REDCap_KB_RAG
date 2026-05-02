# KB Gaps — Articles Still Needed

These articles are referenced by existing KB articles or skills but do not yet exist in the KB.

---

## Open Gaps

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


---

### ⚠️ RC-DE-13 — Record Administration (Choose Action for Record)

**Why needed:** RC-DE-01 calls out the 'Choose action for record' button as out of scope for routine data entry but provides no pointer to a covering article. No existing article covers record-level admin operations.

**Domain slug:** DE (established)
**What to cover:** Accessing 'Choose action for record' from the Record Home Page, available actions (move record to different DAG, rename/renumber record, delete record, lock/unlock record), who can perform each action (user rights required), consequences and irreversibility of deletion, audit trail behavior after admin actions

---

### ⚠️ RC-NAV-UI-03 — Project Bookmarks

**Why needed:** No existing article covers the project bookmarking feature, which allows users to mark frequently-used projects as bookmarks for quick access from the My Projects page. This is a commonly used navigation convenience feature with no KB coverage.

**Domain slug:** NAV-UI (established)
**What to cover:** What project bookmarks are and how they differ from the full My Projects list; how to add and remove a bookmark (star/bookmark icon on the My Projects page); where bookmarks appear in the UI (top of My Projects list or dedicated section); behavior when a project is moved to a different status or deleted; whether bookmarks are user-specific or shared; interaction with project search and filtering on the My Projects page; any admin-level considerations

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
- RC-CC-22 — Administrator Project Tools ✅
- RC-CC-23 — Backup Options ✅
- RC-CC-24 — Control Center: Edit Project Settings ✅

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
- RC-EM-02 — External Modules: Installed Catalog (Production) ✅
- RC-EM-03 — External Modules: Installed Catalog (Test) ✅
- RC-EM-04 — External Modules: Installed Catalog (Development) ✅

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
- RC-FD-12 — Dynamic SQL Field Type ✅ *(was ⚠️ RC-FD-12 SQL Field Type gap)*

### Institution-Specific (RC-INST) — new domain

- RC-INST-01 — Institution-Specific Settings & Policies (Production) ✅
- RC-INST-02 — Institution-Specific Settings & Policies (Test) ✅
- RC-INST-03 — Institution-Specific Settings & Policies (Development) ✅

### Longitudinal (RC-LONG) — expansion

- RC-LONG-03 — Longitudinal Clinical Research Design Patterns ✅

### MCP Server (RC-MCP) — new domain

- RC-MCP-01 — MCP Server Setup and Management ✅

### Operational Use Cases (RC-OPS) — new domain

- RC-OPS-01 — REDCap as an Operational Request Management System ✅

### Send It (RC-SENDIT) — new domain

- RC-SENDIT-01 — Send It: Secure File Transfer ✅

### REDCap Plus (RC-PLUS) — new domain

- RC-PLUS-01 — REDCap+: Overview & Subscription ✅ *(was ⚠️)*

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
- RC-PROJ-05 (Copy Project gap) — Copy Project content integrated into RC-PROJ-01 ✅
- RC-PROJ-05 (on disk) — Project Migration ✅ *(resolves RC-PROJ-06 gap)*

### Profile (RC-PROF) — new domain

- RC-PROF-01 — My Profile: User Profile Settings ✅

### File Repository (RC-FILE) — new domain

- RC-FILE-01 — File Repository ✅ *(was RC-FREP-01 gap; domain slug changed from FREP to FILE)*

### Calendar (RC-CAL) — new domain

- RC-CAL-01 — Calendar ✅

---

### Logging (RC-LOG) — new domain

- RC-LOG-01 — Logging — Project Audit Trail ✅

---

### Previously tracked (earlier resolved)

- RC-BL-05 — Branching Logic in Longitudinal Projects ✅
- RC-CALC-02 — Calculated Fields ✅
- RC-AT-01 through RC-AT-11, RC-AT-EM-01 — Full Action Tags series ✅
- RC-SURV-01 through RC-SURV-09 — Full Surveys series ✅
- RC-SURV-10 — Survey Login ✅
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

*Last updated: 2026-05-01 — Full repo audit. RC-PLUS-01 resolved (article exists on disk). New articles logged: RC-CC-22/23/24, RC-EM-03/04, RC-INST-02/03, RC-LONG-03, RC-MCP-01, RC-OPS-01, RC-SENDIT-01. Open gaps (3): RC-DE-13, RC-FD-11, RC-LOCK-01.*

# KB Gaps — Articles Still Needed

These articles are referenced by existing KB articles or skills but do not yet exist in the KB.

---

## Priority 3 — Out-of-scope references without a covering article

### ⚠️ RC-DE-13 — Record Administration (Choose Action for Record)

**Why needed:** RC-DE-01 calls out the 'Choose action for record' button as out of scope for routine data entry but provides no pointer to a covering article. No existing article covers record-level admin operations.

**Domain slug:** DE (established)
**What to cover:** Accessing 'Choose action for record' from the Record Home Page, available actions (move record to different DAG, rename/renumber record, delete record, lock/unlock record), who can perform each action (user rights required), consequences and irreversibility of deletion, audit trail behavior after admin actions

---

### ⚠️ RC-FDL-01 — Form Display Logic

**Why needed:** RC-SURV-07 explicitly marks Form Display Logic as out of scope and notes it is a separate Online Designer feature adjacent to the survey queue. No existing article covers it.

**Domain slug:** FDL (new)
**What to cover:** What Form Display Logic is (staff/user access to forms based on conditional logic, distinct from branching logic and survey queue), where to find it in the Online Designer, how to configure logic rules, interaction with the auto-continue feature in the survey queue, differences from branching logic and user rights

---

## Priority 4 — Surfaced by RC-UNCLASSIFIED-01 (good interim coverage exists)

### ⚠️ RC-PROJ-01 — Project Lifecycle: Statuses and Transitions

**Why needed:** RC-UNCLASSIFIED-01 §1–2 covers project statuses (Development, Production, Analysis/Cleanup, Completed), moving to Production, copying/deleting projects, Draft Mode, and production change risk flags. No dedicated article exists.

**Domain slug:** PROJ (new)
**What to cover:** All four lifecycle statuses and transitions, the move-to-Production workflow, copying a project (what is/isn't copied), deleting a project (recovery window), Draft Mode and production change review, change risk flags (\*Possible label mismatch, \*Possible data loss, \*Data WILL be lost), rules for safe production changes
**Interim coverage:** RC-UNCLASSIFIED-01 §1–2

---

### ⚠️ RC-DQ-01 — Data Quality Module

**Why needed:** RC-UNCLASSIFIED-01 §3 covers the Data Quality module including default rules, custom rules, real-time execution, Rule H (correcting calculated fields after design changes or imports). Referenced by RC-CALC-01 (Special Functions). No dedicated article exists.

**Domain slug:** DQ (new)
**What to cover:** Default rules, custom rule syntax (same as branching logic), real-time execution (forms only, not surveys), running rules manually, Rule H and when to use it, Data Quality vs. branching logic constraints
**Interim coverage:** RC-UNCLASSIFIED-01 §3

---

### ⚠️ RC-PROJ-02 — Project Dashboards

**Why needed:** RC-UNCLASSIFIED-01 suggests this article. Smart Variables for dashboards are covered in RC-PIPE-14 but the dashboard feature itself (setup, chart/table wizard, public dashboards) has no home.

**Domain slug:** PROJ (established if RC-PROJ-01 is created)
**What to cover:** What a project dashboard is, the dashboard wizard (smart charts, tables), public dashboards, embedding dashboards in survey confirmation pages or alerts
**Interim coverage:** RC-UNCLASSIFIED-01 (implicit), RC-PIPE-14

---

### ⚠️ RC-DDE-01 — Double Data Entry

**Why needed:** RC-UNCLASSIFIED-01 identifies Double Data Entry as an unclassified FAQ topic. No existing article covers it.

**Domain slug:** DDE (new)
**What to cover:** What Double Data Entry is (two independent data entry passes per record), enabling DDE, the reviewer role, merging records, resolving discrepancies, exporting merged records
**Interim coverage:** RC-UNCLASSIFIED-01 (implicit only — content not yet in unclassified)

---

## Priority 5 — Useful context for integrations and field data collection

### ⚠️ RC-API-01 — REDCap API

**Why needed:** Clinical trial projects like REHAB HFpEF often integrate with external systems via the API. The skill currently cannot explain API-related design decisions (e.g., why certain fields are hidden or read-only may be because they're populated via API). Referenced by RC-EXPRT-02 and RC-NAV-UI-02.

**Domain slug:** API (established)
**What to cover:** API basics, API token management, common endpoints (import/export records, import/export data dictionary, file upload/download), API Playground, rate limits and best practices, use cases for automation

---

### ⚠️ RC-IMP-02 — Clinical Data Mart Integration

**Why needed:** RC-IMP-01 lists Clinical Data Mart as an advanced import method and marks it out of scope. No existing article covers it.

**Domain slug:** IMP (established)
**What to cover:** What Clinical Data Mart is, how the integration works in REDCap (automated data pulls from an EHR/CDW), configuration requirements, typical use cases (clinical trial pre-population), limitations and data governance considerations
**Note:** Highly institution-specific — only relevant if the local REDCap instance has CDM integration configured.

---

### ⚠️ RC-MOB-01 — REDCap Mobile App vs. MyCap

**Why needed:** The skill notes mobile considerations (matrix size, instrument size, `@BARCODE-APP`) but has no KB article to back this up. Useful for projects with field-based data collection. Referenced by RC-NAV-UI-01 and RC-NAV-UI-02.

**Domain slug:** MOB (established)
**What to cover:** REDCap Mobile App (offline data collection, setup, supported field types, action tag limitations), MyCap (participant-facing app, difference from surveys, MyCap tasks and schedules), when to use Mobile App vs. MyCap vs. surveys

---

## Already Exists — No Action Needed

These were previously marked ⚠️ but have since been resolved:

- RC-BL-05 — Branching Logic in Longitudinal Projects ✅ *(was Priority 3)*
- RC-CALC-02 — Calculated Fields ✅ *(was Priority 3)*
- RC-AT-01 through RC-AT-11, RC-AT-EM-01 — Full Action Tags series ✅ *(was Priority 1)*
- RC-SURV-01 through RC-SURV-09 — Full Surveys series ✅ *(was Priority 2)*
- RC-LONG-01 — Longitudinal Project Setup ✅
- RC-LONG-02 — Repeated Instruments & Events Setup ✅
- RC-FD-08 — Data Dictionary Column Reference ✅
- RC-BL-01 through RC-BL-04 — Branching Logic series ✅
- RC-RAND-01 through RC-RAND-03 — Randomization series ✅
- RC-ALERT-01, RC-ALERT-02 — Alerts & Notifications ✅
- RC-USER-01 through RC-USER-04 — User Rights series ✅
- RC-DAG-01 — Data Access Groups ✅
- RC-MLM-01 — Multi-Language Management ✅ *(was Priority 2)*
- RC-ALERT-03 — Alternative Alert Delivery Types ✅ *(covered by RC-TXT-01 and RC-TXT-02)*

---

## Notes

- When writing RC-API-01, the REHAB HFpEF project is a good real-world example of API-populated fields (hidden/read-only fields set via external systems).
- RC-UNCLASSIFIED-01 provides interim coverage for RC-PROJ-01 (§1–2), RC-DQ-01 (§3), RC-API-01 (§4), and RC-MOB-01/MyCap (§6). Those sections can serve as drafting source material.

*Last updated: 2026-04-10 (RC-MLM-01 resolved; RC-ALERT-03 covered by RC-TXT-01/RC-TXT-02; RC-PROJ-01, RC-DQ-01, RC-PROJ-02, RC-DDE-01 added from RC-UNCLASSIFIED-01 review; stale ⚠️ references in KB articles cleaned up)*

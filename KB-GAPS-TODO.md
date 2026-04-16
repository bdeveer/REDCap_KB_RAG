# KB Gaps — Articles Still Needed

These articles are referenced by existing KB articles or skills but do not yet exist in the KB.

---

## Priority 3 — Out-of-scope references without a covering article

### ⚠️ RC-DE-13 — Record Administration (Choose Action for Record)

**Why needed:** RC-DE-01 calls out the 'Choose action for record' button as out of scope for routine data entry but provides no pointer to a covering article. No existing article covers record-level admin operations.

**Domain slug:** DE (established)
**What to cover:** Accessing 'Choose action for record' from the Record Home Page, available actions (move record to different DAG, rename/renumber record, delete record, lock/unlock record), who can perform each action (user rights required), consequences and irreversibility of deletion, audit trail behavior after admin actions

---

## Priority 4 — Surfaced by RC-UNCLASSIFIED-01 (good interim coverage exists)


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
- RC-FDL-01 — Form Display Logic ✅ *(was Priority 3)*
- RC-FD-08 — Data Dictionary Column Reference ✅
- RC-BL-01 through RC-BL-04 — Branching Logic series ✅
- RC-RAND-01 through RC-RAND-03 — Randomization series ✅
- RC-ALERT-01, RC-ALERT-02 — Alerts & Notifications ✅
- RC-USER-01 through RC-USER-04 — User Rights series ✅
- RC-DAG-01 — Data Access Groups ✅
- RC-MLM-01 — Multi-Language Management ✅ *(was Priority 2)*
- RC-ALERT-03 — Alternative Alert Delivery Types ✅ *(covered by RC-TXT-01 and RC-TXT-02)*
- RC-API-01 — REDCap API ✅ *(was Priority 5; based on official REDCap API documentation; supersedes RC-UNCLASSIFIED-01 §4 interim coverage)*
- RC-PROJ-01 — Project Lifecycle: Status and Settings ✅ *(was Priority 4; supersedes RC-UNCLASSIFIED-01 §1–2)*
- RC-MYCAP-01 through RC-MYCAP-08 — Full MyCap series ✅ *(supersedes RC-UNCLASSIFIED-01 §6)*
- RC-DQ-01 — Data Quality Module ✅ *(was Priority 4; supersedes RC-UNCLASSIFIED-01 §3)*

---

## Notes

- RC-UNCLASSIFIED-01 §3 has been superseded by RC-DQ-01. RC-UNCLASSIFIED-01 now contains only the suggested articles table and related articles section. It can be archived or removed once RC-DDE-01 and RC-PROJ-02 are created.

*Last updated: 2026-04-15 (RC-DQ-01 resolved — supersedes RC-UNCLASSIFIED-01 §3; RC-UNCLASSIFIED-01 now empty of active interim content)*

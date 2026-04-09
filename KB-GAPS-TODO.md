# KB Gaps — Articles Still Needed

These articles are referenced by existing KB articles or skills but do not yet exist in the KB.

---

## Priority 2 — Surfaced by instrument patterns / multilingual projects

### ⚠️ RC-MLM-01 — Multi-Language Management Overview

**Why needed:** The parser encounters non-English field labels and multilingual projects (e.g., Dutch Oranjeschool registration, bilingual eConsent). The skill can note non-ASCII content but cannot explain REDCap's Multi-Language Management (MLM) module. Also referenced by RC-AT-10 (Action Tags: Language).

**Domain slug:** MLM (established)
**What to cover:** How MLM works, translating field labels vs. choices vs. survey text, the `@LANGUAGE-CURRENT-SURVEY` action tag, the language selector in survey mode, enabling MLM on a project, importing/exporting translations

---

## Priority 3 — Out-of-scope references without a covering article

### ⚠️ RC-CALC-02 — Calculated Fields (Field Type)

**Why needed:** RC-BL-01 explicitly lists "calculated fields and calculation syntax" as out of scope and defers to a dedicated training course. RC-CALC-01 covers Special Functions (used inside formulas), and RC-AT-09 covers @CALCTEXT/@CALCDATE, but no article explains the **Calculated Field field type** itself. Multiple articles reference it without explaining it.

**Domain slug:** CALC (established, RC-CALC-01 already exists)
**What to cover:** What a calculated field is and how it differs from a text field, creating a calculated field in the Online Designer and Data Dictionary, formula syntax basics, numeric-only output limitation, when to use @CALCTEXT/@CALCDATE instead, how values are updated (real-time, data import, Data Quality rule H), display behavior and read-only enforcement

---

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

## Priority 4 — Useful context for integrations and field data collection

### ⚠️ RC-API-01 — REDCap API

**Why needed:** Clinical trial projects like REHAB HFpEF often integrate with external systems via the API. The skill currently cannot explain API-related design decisions (e.g., why certain fields are hidden or read-only may be because they're populated via API). Referenced by RC-EXPRT-02 and RC-NAV-UI-02.

**Domain slug:** API (established)
**What to cover:** API basics, API token management, common endpoints (import/export records, import/export data dictionary, file upload/download), API Playground, rate limits and best practices, use cases for automation

---

### ⚠️ RC-ALERT-03 — Alternative Alert Delivery Types (SMS, Voice, SendGrid)

**Why needed:** RC-ALERT-01 explicitly states it covers email only and marks SMS, Voice Call, and SendGrid as out of scope. No other article covers these delivery methods.

**Domain slug:** ALERT (established)
**What to cover:** Enabling SMS and voice delivery (institution-level configuration requirement), composing SMS vs. email alerts (character limits, no HTML), SendGrid integration and when it applies, comparing delivery reliability and use cases across types
**Note:** Relevance depends on whether the institution has SMS/voice enabled. Confirm with REDCap admin before prioritizing.

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

---

## Notes

- The **KB-REFERENCE-MAP.md** still shows ⚠️ for RC-ALERT-01, RC-LONG-01, RC-SURV-01, and RC-USER-03 in some outbound-link sections — these are stale and should be cleaned up in a future reference map update.
- When writing RC-MLM-01, RC-AT-10 (Action Tags: Language) is a useful companion article that already covers `@LANGUAGE-CURRENT-SURVEY` in depth.
- When writing RC-API-01, the REHAB HFpEF project is a good real-world example of API-populated fields (hidden/read-only fields set via external systems).

*Last updated: 2026-04-08*

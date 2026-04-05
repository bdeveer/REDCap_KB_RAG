# KB Gaps — Articles Still Needed

These articles are referenced by existing KB articles or skills but do not yet exist in the KB.

---

## Priority 2 — Surfaced by instrument patterns / multilingual projects

### ⚠️ RC-MLM-01 — Multi-Language Management Overview

**Why needed:** The parser encounters non-English field labels and multilingual projects (e.g., Dutch Oranjeschool registration, bilingual eConsent). The skill can note non-ASCII content but cannot explain REDCap's Multi-Language Management (MLM) module. Also referenced by RC-AT-10 (Action Tags: Language).

**Domain slug:** MLM (established)
**What to cover:** How MLM works, translating field labels vs. choices vs. survey text, the `@LANGUAGE-CURRENT-SURVEY` action tag, the language selector in survey mode, enabling MLM on a project, importing/exporting translations

---

## Priority 4 — Useful context for integrations and field data collection

### ⚠️ RC-API-01 — REDCap API

**Why needed:** Clinical trial projects like REHAB HFpEF often integrate with external systems via the API. The skill currently cannot explain API-related design decisions (e.g., why certain fields are hidden or read-only may be because they're populated via API). Referenced by RC-EXPRT-02 and RC-NAV-UI-02.

**Domain slug:** API (established)
**What to cover:** API basics, API token management, common endpoints (import/export records, import/export data dictionary, file upload/download), API Playground, rate limits and best practices, use cases for automation

---

### ⚠️ RC-MOB-01 — REDCap Mobile App vs. MyCap

**Why needed:** The skill notes mobile considerations (matrix size, instrument size, `@BARCODE-APP`) but has no KB article to back this up. Useful for projects with field-based data collection. Referenced by RC-NAV-UI-01 and RC-NAV-UI-02.

**Domain slug:** MOB (established)
**What to cover:** REDCap Mobile App (offline data collection, setup, supported field types, action tag limitations), MyCap (participant-facing app, difference from surveys, MyCap tasks and schedules), when to use Mobile App vs. MyCap vs. surveys

---

## Already Exists — No Action Needed

These were previously marked ⚠️ but have since been resolved:

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

*Last updated: 2026-04-04*

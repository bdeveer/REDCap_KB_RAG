# KB Gaps — Articles Needed for redcap-data-dictionary Skill

These articles are referenced by the skill or surfaced by the parser but do not yet exist in the KB.
Each one would improve the skill's ability to explain REDCap concepts accurately and in full.

---

## Priority 1 — Directly referenced by the skill

### ⚠️ RC-AT-01 — Action Tags

**Why needed:** The skill's parser inventories all action tags found in a data dictionary and provides brief inline descriptions. However, the skill notes explicitly that no full KB article exists yet. A complete RC-AT-01 would let the skill cross-reference a proper article rather than relying solely on parser descriptions.

**What to cover:**
- What action tags are and how they differ from branching logic and required-field flags
- Syntax: `@TAG`, `@TAG='value'`, `@TAG(expression)`, multiple tags space-separated
- Excel Column R formatting requirement (must set cell format to Text before typing `@`)
- Complete reference table of all supported tags with syntax, effect, and common use cases
- Tags that interact: `@IF` with other tags, `@HIDDEN` vs. `@HIDDEN-SURVEY` vs. `@HIDDEN-FORM`
- Tags that have data implications vs. purely cosmetic tags (e.g., `@CALCTEXT` stores nothing; `@PASSWORDMASK` stores in plain text)
- Action tags not supported in the REDCap Mobile App
- Common mistakes: `@NOMISSING` vs. Required Field; `@READONLY` in production vs. development mode; `@DEFAULT` only fires on first load

**Tags to document at minimum (all observed across example projects):**
`@NOMISSING`, `@HIDDEN`, `@HIDDEN-SURVEY`, `@HIDDEN-FORM`, `@HIDDEN-PDF`, `@READONLY`, `@READONLY-SURVEY`, `@IF`, `@CALCTEXT`, `@CALCDATE`, `@DEFAULT`, `@SETVALUE`, `@NOW`, `@TODAY`, `@PASSWORDMASK`, `@NONEOFTHEABOVE`, `@HIDEBUTTON`, `@HIDESUBMIT-SURVEY`, `@FORCE-MINMAX`, `@HIDECHOICE`, `@SHOWCHOICE`, `@CHARLIMIT`, `@PLACEHOLDER`, `@BARCODE-APP`, `@LATITUDE`, `@LONGITUDE`, `@MAXCHECKED`, `@MAXCHOICE`, `@LANGUAGE-CURRENT-SURVEY`

**Domain slug:** AT (established)
**Prerequisite:** RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques
**Related:** RC-BL-01 (branching logic), RC-FD-02 (Online Designer), RC-LONG-01 (longitudinal)

---

## Priority 2 — Referenced by instrument patterns detected by the parser

### ⚠️ RC-SURV-01 — Surveys: Basics

**Why needed:** The parser detects survey instruments (via question numbers in Column O) and notes them. Without a survey article, the skill can identify survey instruments but cannot explain survey-specific concepts like survey queue, completion actions, or survey vs. data entry mode differences.

**Domain slug:** SURV (established)
**What to cover:** Survey mode vs. data entry mode, enabling surveys on an instrument, survey settings page, completion actions, survey queue basics, @HIDDEN-SURVEY vs. @HIDDEN-FORM behavior

---

### ⚠️ RC-MLM-01 — Multi-Language Management Overview

**Why needed:** The parser encounters non-English field labels and multilingual projects (e.g., Dutch Oranjeschool registration, bilingual eConsent). The skill can note non-ASCII content but cannot explain REDCap's Multi-Language Management (MLM) module.

**Domain slug:** MLM (established)
**What to cover:** How MLM works, translating field labels vs. choices vs. survey text, the `@LANGUAGE-CURRENT-SURVEY` action tag, the language selector in survey mode

---

## Priority 3 — Referenced in cross-instrument BL dependencies

### ⚠️ RC-AT-01 (same as Priority 1) covers `@IF` which is the main tool for conditional action tags cross-instrument

No additional articles needed at this tier beyond RC-AT-01.

---

## Priority 4 — Useful context for large clinical trial projects

### ⚠️ RC-API-01 — REDCap API

**Why needed:** Clinical trial projects like REHAB HFpEF often integrate with external systems via the API. The skill currently cannot explain API-related design decisions (e.g., why certain fields are hidden or read-only may be because they're populated via API).

**Domain slug:** API (established)

---

### ⚠️ RC-MOB-01 — REDCap Mobile App vs. MyCap

**Why needed:** The skill notes mobile considerations (matrix size, instrument size, @BARCODE-APP) but has no KB article to back this up. Useful for projects with field-based data collection.

**Domain slug:** MOB (established)

---

## Already Exists — No Action Needed

These were previously marked ⚠️ but have since been resolved:
- RC-LONG-01 — Longitudinal Project Setup ✅
- RC-LONG-02 — Repeated Instruments & Events Setup ✅
- RC-FD-08 — Data Dictionary Column Reference ✅ (key reference for the skill)
- RC-BL-01 through RC-BL-04 — Branching Logic series ✅
- RC-RAND-01 through RC-RAND-03 — Randomization series ✅
- RC-ALERT-01, RC-ALERT-02 — Alerts & Notifications ✅

---

## Notes for Article Writers

When writing RC-AT-01, the REHAB HFpEF data dictionary (`REHABHFpEF_DataDictionary_2026-04-04.csv`) is an excellent real-world source of action tag examples — it uses 14 distinct tags across 1,306 fields. The parser output (run with `--json`) shows each tag's frequency and annotated fields, which could inform the "common use cases" section.

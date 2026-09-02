# Project To-Do

Running list of development tasks for the REDCap KB / RAG project — separate from KB article gaps (see KB-GAPS-TODO.md).

---

## KB Content

- [x] **Remove all Yale references** — Audit every article in `kb/` for Yale-specific placeholders and callout boxes. Replace with generic institution-agnostic language or a standardized `> **Institution-specific:**` placeholder pattern. Known affected files: RC-DQ-01, RC-DE-05, RC-SURV-08, RC-AI-01, RC-PIPE-04, RC-USER-03, RC-LONG-01, RC-LONG-02, RC-MOB-01, RC-MYCAP-01, RC-TXT-01, RC-EXPRT-06, RC-SURV-02, RC-USER-01 (14 files total).

- [ ] **Flesh out RC-INST-01** — The article structure and `[FILL IN]` template exist but all placeholders need to be populated with real values for this installation: support channel, support hours, server time zone, draft mode policy, account creation workflow, global suspension rules, and enabled/disabled external modules.

---

## Tooling & Skills

- [x] **Teach Claude how to build the alerts upload CSV** — Document the CSV format REDCap uses for importing Alerts & Notifications. Add to a skill (or to the relevant KB article) with enough spec detail that Claude can generate a valid import file from scratch.

- [x] **Feed Claude examples of all uploadable file formats** — For each upload type in RC-IMP-03, provide a real or representative example file. Use these to expand the relevant KB articles with annotated column-by-column breakdowns, accepted values, escaping rules, and common mistakes. Goal: Claude can generate any valid upload file from scratch given a plain-language description.
  - [x] Data Dictionary
  - [x] Arms
  - [x] Events
  - [x] Instrument–Event Mappings
  - [x] Record Data
  - [x] Users
  - [x] User Roles
  - [x] User–Role Assignments
  - [x] Data Access Groups (DAGs)
  - [x] User–DAG Assignments
  - [x] Alerts & Notifications
  - [x] Automated Survey Invitations (ASI)
  - [x] Survey Queue
  - [x] Survey Settings
  - [x] Form Display Logic
  - [x] Data Quality Rules
  - [x] Language Setups (MLM)
  - [x] Randomization Allocation Table

---

## Documentation

- [ ] **Flesh out the style guide** — Expand `STYLE-GUIDE.md` to cover REDCap project design conventions beyond field alignment: naming standards for fields/instruments/events, branching logic patterns, calculated field practices, survey design guidelines, etc. Also add a **"How to contribute to this guide"** section explaining the process for proposing and documenting new conventions (what triggers an addition, how to phrase a principle, where to add it).
  - **v1.4 (2026-05-16):** Added §5.7 (prefer `[user-role-name]` over `[user-role-label]` in branching logic; DAG name stability); §9 Variable and Instrument Naming (9.1 variable name rules and permanence, 9.2 unique instrument display names); §10 ASI Safety Patterns (10.1 kill switch field, 10.2 "Ensure logic is still true"). Cross-references added to RC-PIPE-05, RC-SURV-06, RC-FD-06, RC-BL-01.
  - Still to add: calculated field conventions (RC-CALC-02), record ID / identifier patterns, choice coding conventions (raw value standards), locking/signing workflow guidance (RC-LOCK-01), "How to contribute" meta-section.

- [ ] **Redo README** — The current README needs a full rewrite. Scope TBD — review what's there first and decide what it should cover (project purpose, repo structure, how to use the KB, how to contribute, etc.).

---

## Housekeeping

- [x] **Add "Related Articles" section to articles that were missing it as their last section** — All 224 articles now pass the format checker with 0 errors and 0 warnings. Fixed: numbered existing unnumbered sections (RC-DQ-01, RC-MLM-01, RC-SURV-08, RC-SURV-09, RC-AI-01–04, RC-CALC-01); added new sections to RC-EM-01–04, RC-FD-06, RC-INST-01–03, RC-RAND-01–03, RC-SURV-01. Also fixed RC-CAL-01 (wrong file format) and RC-FD-09 (duplicate section number 7).

- [x] **Fix section 1 naming in 3 articles** — RC-CC-07 (body content wrapped under `# 1. Overview`; existing sections renumbered), RC-CC-20 (intro promoted to `# 1. Overview`; Page Tabs renumbered to `# 2.`), RC-CC-21 (renamed from "What Is the Control Center?" to "Overview").

- [x] **Institution-neutrality check** — `tools/check_institution_neutral.py` scans `kb/` and `kb (YAML)/` for real institution names and for host names that aren't recognised placeholders (`yourinstitution.edu`, `institution.edu`, etc.). RC-INST-01 is exempt, since local values belong there. Run `python3 tools/check_institution_neutral.py`; exits 1 on any hit so it can gate CI. Cleared the last stray Yale reference at the same time (RC-IMP-05, an example `email-from` address → `example.edu`).
  - Not yet wired into `.github/workflows/deploy-docs.yml` — decide whether a hit should block the Pages deploy or just warn.

---

## Completed

- [x] **Create an inventory of all uploadable CSV formats** — RC-IMP-03_CSV-Upload-Reference.md
- [x] **Create API skills and project-build checklist** — RC-PROJ-02 (article) + supporting skill
- [x] **Create institutional setup template structure** — RC-INST-01_Institution-Specific-Settings-and-Policies.md (template built; content population is the open task above)
- [x] **Remove all Yale references** — Confirmed clean via audit; literal "Yale" text was already removed in a prior commit. All 14 flagged articles use the correct `> **Institution-specific:**` callout pattern.
- [x] **Clean up Author field across all articles** — All 204 KB articles now have `| **Author** | See KB-SOURCE-ATTESTATION.md |`. The previous "REDCap Support" placeholder has been removed. CDIS articles (which had no metadata table) received a minimal header; RAND and NAV-UI articles had the Author row inserted after `Last Reviewed`.
- [x] **Add TCC repo to attestation file** — TCC (Training Collaboration Committee) section added to `KB-SOURCE-ATTESTATION.md`, covering RC-MOB-01, RC-MYCAP-01 through RC-MYCAP-08, and RC-MLM-01. Includes specific source document credits and repository URL.

---

*Last updated: 2026-05-16 (RC-DSGN-01 v1.4 — style guide expanded with §5.7 role/DAG smart variable naming, §9 variable and instrument naming conventions, §10 ASI safety patterns. Cross-refs updated.)*

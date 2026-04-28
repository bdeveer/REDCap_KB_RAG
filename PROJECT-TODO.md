# Project To-Do

Running list of development tasks for the REDCap KB / RAG project — separate from KB article gaps (see KB-GAPS-TODO.md).

---

## KB Content

- [x] **Remove all Yale references** — Audit every article in `kb/` for Yale-specific placeholders and callout boxes. Replace with generic institution-agnostic language or a standardized `> **Institution-specific:**` placeholder pattern. Known affected files: RC-DQ-01, RC-DE-05, RC-SURV-08, RC-AI-01, RC-PIPE-04, RC-USER-03, RC-LONG-01, RC-LONG-02, RC-MOB-01, RC-MYCAP-01, RC-TXT-01, RC-EXPRT-06, RC-SURV-02, RC-USER-01 (14 files total).

- [ ] **Flesh out RC-INST-01** — The article structure and `[FILL IN]` template exist but all placeholders need to be populated with real values for this installation: support channel, support hours, server time zone, draft mode policy, account creation workflow, global suspension rules, and enabled/disabled external modules.

---

## Tooling & Skills

- [ ] **Teach Claude how to build the alerts upload CSV** — Document the CSV format REDCap uses for importing Alerts & Notifications. Add to a skill (or to the relevant KB article) with enough spec detail that Claude can generate a valid import file from scratch.

- [ ] **Feed Claude examples of all uploadable file formats** — For each upload type in RC-IMP-03, provide a real or representative example file. Use these to expand the relevant KB articles with annotated column-by-column breakdowns, accepted values, escaping rules, and common mistakes. Goal: Claude can generate any valid upload file from scratch given a plain-language description.

---

## Documentation

- [ ] **Flesh out the style guide** — Expand `STYLE-GUIDE.md` to cover REDCap project design conventions beyond field alignment: naming standards for fields/instruments/events, branching logic patterns, calculated field practices, survey design guidelines, etc. Also add a **"How to contribute to this guide"** section explaining the process for proposing and documenting new conventions (what triggers an addition, how to phrase a principle, where to add it).

- [ ] **Redo README** — The current README needs a full rewrite. Scope TBD — review what's there first and decide what it should cover (project purpose, repo structure, how to use the KB, how to contribute, etc.).

---

## Housekeeping

- [ ] **Add "Related Articles" section to 21 articles that are missing it as their last section** — The KB format checker flags these because the final section is not "Related Articles". Each either needs the section added or (if it exists mid-article) moved to the end. Grouped by what currently ends the article:
  - *Ends with "Common Mistakes & Gotchas"*: RC-AI-01, RC-AI-02, RC-AI-03, RC-AI-04, RC-CALC-01, RC-DQ-01, RC-MLM-01, RC-SURV-08, RC-SURV-09
  - *Ends with "Common Questions"*: RC-EM-01, RC-EM-02, RC-EM-03, RC-EM-04, RC-INST-01, RC-INST-02, RC-INST-03
  - *Ends with "Version & Change Notes"*: RC-FD-06, RC-RAND-01, RC-RAND-02, RC-RAND-03, RC-SURV-01

- [ ] **Fix section 1 naming in 3 articles** — The checker expects section 1 to be called "Overview"; these articles use a different name for their opening section:
  - RC-CC-07 — section 1 is "Common Questions" (article is missing intro sections entirely)
  - RC-CC-20 — section 1 is "Page Tabs"
  - RC-CC-21 — section 1 is "What Is the Control Center?" (intro content is there, just not titled "Overview")

---

## Completed

- [x] **Create an inventory of all uploadable CSV formats** — RC-IMP-03_CSV-Upload-Reference.md
- [x] **Create API skills and project-build checklist** — RC-PROJ-02 (article) + supporting skill
- [x] **Create institutional setup template structure** — RC-INST-01_Institution-Specific-Settings-and-Policies.md (template built; content population is the open task above)
- [x] **Remove all Yale references** — Confirmed clean via audit; literal "Yale" text was already removed in a prior commit. All 14 flagged articles use the correct `> **Institution-specific:**` callout pattern.
- [x] **Clean up Author field across all articles** — All 204 KB articles now have `| **Author** | See KB-SOURCE-ATTESTATION.md |`. The previous "REDCap Support" placeholder has been removed. CDIS articles (which had no metadata table) received a minimal header; RAND and NAV-UI articles had the Author row inserted after `Last Reviewed`.
- [x] **Add TCC repo to attestation file** — TCC (Training Collaboration Committee) section added to `KB-SOURCE-ATTESTATION.md`, covering RC-MOB-01, RC-MYCAP-01 through RC-MYCAP-08, and RC-MLM-01. Includes specific source document credits and repository URL.

---

*Last updated: 2026-04-27 (KB format checker + fixer scripts added; 38 errors resolved across 73 articles; 24 remaining warnings logged above)*

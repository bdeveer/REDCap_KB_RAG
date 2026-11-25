# KB Source Review Plan

Plan for checking the whole KB against REDCap source code, using the method in
`redcap_src\METHODOLOGY.md` (fact-check agents → spot-check → notes → go-ahead →
edit → review → rebuild). Drafted 2026-11-24, after the first run (randomization:
RC-RAND-01/02/03, RC-PIPE-13, plus randomization rights in RC-USER-03).

Versions compared: **17.6.5 Standard / 17.3.31 LTS / 16.0.61 LTS**.

> This file lives in the public repo. Keep source paths, file names and code out of
> it. The article-to-module map and all findings go in `redcap_src\notes\`.

---

## 1. Where the KB stands

| Verification level (from each article's `Verified Against` row) | Articles |
|---|---|
| Source code checked | 5 (RAND-01/02/03, PIPE-13, part of USER-03) |
| Live-checked on a test instance (17.5.6 Standard only) | 63 |
| Changelog review only | 172 |
| Other / none (templates, infra, MCP) | 10 |

A changelog review only checks what changed between releases. It never checked the
original claims, which came from v15–16 help pages, the FAQ and training documents.
The first source review found more than ten claims that were wrong in every
version across four articles. Some of them came straight from REDCap's own Help
text. Expect a similar error rate in the 172 changelog-only articles.

Live checks covered 17.5.6 Standard only. For those 63 articles, the main risk is
behaviour that differs on LTS 16.

## 2. How articles are ranked

Impact = **reach × harm if wrong × gap in verification**. Articles that source code
can't verify drop out.

- **Reach.** Inbound links in `meta/KB-CROSS-REFS.md`, a proxy for how often RAG
  retrieves the article and how many other articles repeat its claims. RC-API-01
  has 100, RC-USER-03 41, RC-DAG-01 40, RC-CC-06 38, RC-FD-02 37 and RC-USER-01 36.
  The median is about 5.
- **Harm if wrong**, from highest to lowest:
  1. Data exposure: rights, DAGs, de-identification, survey access, API tokens.
  2. Data loss or integrity: changes in production, import overwrite, deletes,
     audit trail.
  3. Compliance: e-Consent, e-signatures, locking, PDF snapshots.
  4. Silently wrong values: logic, calculations, piping.
  5. Workflow and UI.
- **Gap in verification.** Changelog-only articles rank above live-checked ones,
  and live-checked ones rank above articles already checked against source.
- **Verifiable from source.** Behaviour, defaults, limits, rights and parameters
  are verifiable. Design advice, institution templates and self-hosting guides are
  not.

## 3. Wave 0: set-up and quick wins (do first)

1. **Module map.** Write `redcap_src\notes\module-map.md` (private), mapping each
   article ID to its source areas. It does the scoping in METHODOLOGY step 1 once
   for all articles, so each wave reuses it.
2. **Hash-compare script.** Script METHODOLOGY step 1.3 in `redcap_src\`: give it
   a module, and it lists the files that differ across the three versions. It
   becomes a change detector later (see §6).
3. **Open TODOs that source can settle.** These are cheap, single-question
   look-ups that have been blocked for months. Settle them first:
   - `datediff` signature and where the date-format parameter goes (RC-CALC-01
     §5.1, RC-ALERT-01 §3.3).
   - A Completed project for a non-admin member: is it listed, linked or
     openable? (RC-PROJ-01 §2.4, RC-NAV-UI-04 §5)
   - Does a 2FA reset issue a new authenticator secret? (RC-CC-03 §3.1)
   - REDCap+ login protection: does it cover the Public Survey, and does the
     8-data-point threshold apply? (RC-SURV-10 §5, RC-EXPRT-06 §4.2, RC-PROJ-03
     §5.5, RC-PLUS-01 §4)
   - Pages gated behind a REDCap+ subscription that were written from release
     notes (RC-PLUS-02 §3–4, RC-PLUS-04 layout, RC-CDIS-05). The code is in the
     download even without a subscription.

   Mark each one in `PROJECT-TODO.md` as "source-checked; live check pending"
   (README rule 6).

## 4. Review waves, by impact

Each wave is one or two sessions, grouped by source area so the scoping and hash
compare are shared. Articles in bold are the main targets. The companion sweep
looks for the same claims repeated in other articles (METHODOLOGY step 5).

### Wave 1: access control and data exposure

| Article | Inbound | Level now | Why |
|---|---|---|---|
| **RC-USER-03** Configuring User Privileges | 41 | CL (+rand. SRC) | Hub for every rights claim |
| **RC-USER-01** Overview & Three-Tier Access | 36 | CL | |
| **RC-DAG-01** Data Access Groups | 40 | CL | DAG isolation is a data-exposure boundary |
| **RC-USER-02** Adding Users & Roles | 18 | CL | |
| **RC-USER-04** User Management | 9 | CL | Expiration, suspension |
| **RC-EXPRT-03** Export User Rights | 9 | CL | De-identified / no-PHI export levels |
| **RC-EXPRT-04** De-identification Options | 4 | CL | Which fields each option removes |
| **RC-API-01** REDCap API (hub) | 100 | CL | Token rights. Most-linked article in the KB |

Companion sweep: RC-DE-09, RC-DE-03, RC-API-22/23/25/26/28–33/55/56 (user, role
and DAG endpoints share this code), and RC-CC-07.

### Wave 2: changes in production and data integrity

| Article | Inbound | Level now |
|---|---|---|
| **RC-PROJ-01** Project Lifecycle (status, draft mode) | 19 | CL |
| **RC-FD-02** Online Designer | 37 | CL |
| **RC-FD-06** Instrument & Field Management | 8 | CL |
| **RC-FD-03** Data Dictionary | 25 | CL |
| **RC-FD-08** DD Column Reference | 13 | CL |
| **RC-IMP-01 / 03 / 04** Import overview, CSV reference, record import (overwrite, blank handling) | 9 / 9 / 4 | CL |
| **RC-API-03** Import Records, **RC-API-08** Import Metadata | 14 / 9 | LIVE (Std only) |
| **RC-LOG-01** Logging / audit trail | 4 | CL |
| **RC-DE-04** Editing Data & Audit Trail | 9 | CL |
| **RC-DE-13** Record Administration (delete, rename) | 3 | CL |
| **RC-PROJ-05** Project Migration | 2 | CL |

### Wave 3: compliance features

**RC-SURV-08** e-Consent, **RC-SURV-09** PDF Snapshots, **RC-LOCK-01** Locking &
E-Signatures, **RC-SURV-10** Survey Login, **RC-SURV-03** Survey access &
termination, **RC-CC-03** Security & Authentication. All but CC-03 are
changelog-only. Their regulatory claims (Part 11, what a signature or snapshot
records) are the ones institutions rely on.

### Wave 4: the logic engine (highest claim density)

**RC-BL-01–05**, **RC-CALC-01/02**, **RC-PIPE-01–04**, **RC-PIPE-05–17**,
**RC-AT-01–11**, **RC-FDL-01**, **RC-DE-05** (validations). BL-01 and PIPE-03 have
30 inbound links each. Every function signature, operator rule and smart-variable
return value can be checked against the parser. Mistakes here give silently wrong
data in live projects. These articles also feed the `redcap-syntax` skill, so
fixes carry over to generated expressions.

Run it as four sub-waves, each with its own report, go-ahead and commit:

| Sub-wave | Articles | Notes |
|---|---|---|
| 4a Logic engine | RC-BL-01–05, RC-CALC-01/02, RC-FDL-01 (8) | First: shared parser, most inbound links |
| 4b Piping | RC-PIPE-01–04, RC-DE-05 (5) | |
| 4c Smart variables | RC-PIPE-05–17 except PIPE-13 (12) | Two or three articles per agent |
| 4d Action tags | RC-AT-01–11 (11) | Two or three articles per agent |

### Wave 5: longitudinal, surveys and automation

**RC-LONG-01/02**, **RC-NAV-REC-02/03**, **RC-DE-10**, **RC-SURV-01/02/04/05/06/07**,
**RC-ALERT-01/02**, **RC-MLM-01**, and the matching upload formats **RC-IMP-05/06/07/08/09/10**.
LONG-01 has 35 inbound links, ALERT-01 33, LONG-02 30 and SURV-01 28. ASI timing
and alert trigger rules are the usual sources of support tickets.

### Wave 6: exports, reports and everyday data entry

RC-EXPRT-01/02/05/06/07/08, RC-DE-01/02/11/12, RC-DQ-01, RC-NAV-REC-01/04,
RC-NAV-UI-01–04, RC-FD-01/04/05/07/11/12, RC-FILE-01, RC-PROJ-02/03/04,
RC-DDE-01, RC-CAL-01, RC-PROF-01.

### Wave 7: API method articles (RC-API-02–56)

These are uniform and dense with parameters, and each method maps to one area of
the source. Batch four to six endpoints per agent, grouped by resource (records,
metadata, arms/events, surveys, file repository, project). The user, role and DAG
endpoints were already covered in Wave 1. For the 24 that were live-tested,
check only the parameter tables and the LTS 16 differences.

### Wave 8: Control Center and admin

RC-CC-01–26, RC-PLUS-01–05, RC-EM-01, RC-AI-01–04, RC-CC-26, RC-TXT-02, RC-DDP-02,
RC-CDIS-01–05. Most CC articles were live-checked on 17.5.6, so the work here is
mainly the LTS 16 differences. Some articles are already partly done in Wave 0
(PLUS, CDIS-05) or Wave 3 (CC-03).

### Wave 9: specialty modules

RC-MYCAP-01–08 and RC-MOB-01 (server side only: the app is a separate codebase),
RC-TXT-01, RC-MSG-01, RC-SENDIT-01, RC-INTG-01, RC-DDP-01, RC-DE-06/07/08.

### Out of scope, or factual spot-check only

- Not verifiable from source: RC-INST-01/02/03 and RC-EM-02/03/04 (institution
  templates), RC-INFRA-01/02 (self-hosting), RC-MCP-01 (this repo's own server),
  RC-AT-EM-01 (an external module, not core).
- Design or pattern articles, where only the stated REDCap behaviour gets checked
  and the advice is left alone: RC-DSGN-01, RC-LONG-03, RC-FD-09, RC-FD-10,
  RC-OPS-01.
- RC-INFRA-03 (release lines): keep it on the changelog, but check any behaviour
  claims.

## 5. Changes to the method for running it at scale

- **Sessions by area, agents by article.** Keep one fact-check agent per article,
  but run each wave in one session so the module map and hash compare are shared.
  Large related groups (PIPE-05–17, API batches) can share an agent.
- **Brief by verification level.** Changelog-only articles get a full claim list.
  For live-checked articles, tell the agent which sections were live-tested, and
  have it check those sections only for differences on LTS 17 and 16.
- **Track yield.** Record the A/B/C counts for each wave in the notes file. If a
  wave turns up few real errors (likely for the live-tested API articles), make
  later similar waves spot-checks.
- **Help text is not ground truth.** The first run found REDCap's own Help/FAQ text
  wrong. Several KB articles came from that text, so contradictions with it are
  expected. Flag them for a live check rather than discarding them.
- **Commit once per wave** (or once per sub-cluster in large waves), with messages
  like `<IDs>: <topic> review against source`.

### Chunk size (set 2026-11-25)

Wave 3 and Wave 4a each used about 40% of one session allowance (Wave 3: 6
changelog-only articles, about 2,100 lines; Wave 4a: 8 articles, about 3,600
lines, five of them partly live-tested). No chunk may use more than 40%, so each
chunk in the table above targets about 25–30%:

- **At most about 6 fact-check agents and 1,400 lines** of changelog-only articles,
  or about 2,300 lines when most articles were live-tested (those agents check
  only LTS differences and untested claims).
- **Batch small related articles**, 2–5 per agent (smart variables, action tags,
  upload formats, API methods, live-tested Control Center pages). One agent
  reading the shared source once is cheaper than several agents reading it.
- **Keep reports short:** ask agents for about 1,200 words, no CONFIRMED list
  beyond one line per claim, and skip facts already in earlier wave notes.
- **One report, go-ahead and commit per chunk.** Two chunks can share a session
  only if the first finished well under 40%.

## 6. Keeping it current afterwards

When a new version is added with `add-version.ps1`, hash-compare each module in the
module map against the previous version of the same release line. Only articles
whose modules changed need a new source check. This replaces matching changelog
entries to articles by keyword. It also clears the `PROJECT-TODO` item to pin a
version on every article, because each source-reviewed article gets a pinned
`Verified Against` row.

## 7. Progress

`Verified Against` is the tracker: an article counts as done when that row says
"checked against source code". To get the remaining count, grep `kb/` for
`Verified Against` rows that lack that phrase.

| Wave | Articles (main targets) | Status |
|---|---|---|
| Pilot: randomization | 4 + rights in USER-03 | Done 2026-11-24 (8080071) |
| 0 Set-up and TODOs | 5 open TODOs → 13 articles edited | Done 2026-11-24 |
| 1 Access & exposure | 8 + 4 from the sweep | Done 2026-11-24 |
| 2 Production & integrity | 14 + 2 from the sweep | Done 2026-11-24 |
| 3 Compliance | 6 + 2 from the sweep | Done 2026-11-25 |
| 4a Logic engine | 8 + 3 from the sweep | Done 2026-11-25 |
| 4b Piping | 5 + 3 from the sweep | Done 2026-11-25 |
| 4c-1 Smart variables | 6 (sweep found nothing) | Done 2026-11-25 |
| 4c-2 Smart variables | 6 + 3 from the sweep | Done 2026-11-25 |
| 4d-1 Action tags | AT-01–06 (6; 2–3 per agent) | Done 2026-11-25 (6 + 1 from the sweep) |
| 4d-2 Action tags | AT-07–11 (5; 2–3 per agent; also fix AT-09 rule H wording) | Done 2026-11-25 (5 + 2 from the sweep) |
| 5a Longitudinal | LONG-01/02, DE-10, NAV-REC-02/03 (5) | — |
| 5b Surveys core | SURV-01/02/04/05 (4) | Done 2026-11-25 (4; sweep found nothing) |
| 5c Automation | SURV-06/07, ALERT-01/02 (4) | — |
| 5d MLM and upload formats | MLM-01, IMP-05–10 (7; IMP 3 per agent) | — |
| 6a Exports | EXPRT-01/02/05/06/07/08 (6) | — |
| 6b Data entry | DE-01/02/11/12, DDE-01 (5) | — |
| 6c Data quality and navigation | DQ-01, NAV-REC-01/04, NAV-UI-01/02 (5) | — |
| 6d Designer I | FD-01/04/05 (3) | — |
| 6e Designer II | FD-07/11/12, NAV-UI-03/04 (5) | — |
| 6f Project and misc | PROJ-02/03/04, FILE-01, CAL-01, PROF-01 (6) | — |
| 7a API | API-02–13 except 03, 08 (10; 5 per agent) | — |
| 7b API | API-14–24 except 18 (10; 5 per agent) | — |
| 7c API | API-25–36 except 31, 32 (10; 5 per agent) | — |
| 7d API | API-37–46 (10; 5 per agent) | — |
| 7e API | API-47–56 (10; 5 per agent) | — |
| 8a Control Center I | CC-01, 02, 04–09 (8; LTS differences, 2 per agent) | — |
| 8b Control Center II | CC-10–18 (9; LTS differences, 2–3 per agent) | — |
| 8c Control Center III | CC-19–26 (8; LTS differences, 2 per agent) | — |
| 8d REDCap+ and modules | PLUS-01–05, EM-01, TXT-02 (7) | — |
| 8e AI and DDP | AI-01–04, DDP-02 (5) | — |
| 8f CDIS | CDIS-01–05 (5) | — |
| 9a MyCap I | MYCAP-01–04 (4) | — |
| 9b MyCap II | MYCAP-05–08 (4) | — |
| 9c Mobile, texting, messenger | MOB-01, TXT-01, MSG-01 (3) | — |
| 9d Specialty | SENDIT-01, INTG-01, DDP-01, DE-06/07/08 (6; 2 per agent) | — |

# KB Update To-Do — REDCap 15.0.0 → 17.4.1

**Generated:** 2026-08-18
**Source:** `ChangeLog_Standard_2026-08-18.csv` (9,135 rows) + `ChangeLog_LTS_2026-08-18.csv` (6,392 rows)
**Current releases:** Standard **17.4.1** (2026-08-13) · LTS **17.3.7** (2026-08-13)
**KB high-water mark before this review:** 17.1.3

---

## Scope & method

- **Version floor:** 15.0.0. **Change types:** `New Feature`, `Improvement`, `Change`. Plain bug fixes and security fixes were excluded per scoping decision.
- Standard and LTS logs were merged and de-duplicated on normalised description text; each item is attributed to the **earliest** version it shipped in. That yields **343 unique entries** — 28 New Feature, 200 Improvement, 115 Change.
- Entries were matched against the 243 KB articles in `KB-INDEX.md` using title, synonym, heading and keyword-map overlap, then reviewed by hand. Every "not covered" claim below was confirmed by a literal string search against `kb/`.

**Severity key**

| Tag | Meaning |
|---|---|
| **NEW** | No KB coverage exists — a new article is needed |
| **WRONG** | Existing KB text is now factually incorrect |
| **GAP** | Existing article is correct but silent on the change |
| **MINOR** | Cosmetic / UI-polish; update only when the article is next touched |

---

## Summary

| Priority | Items | Effort |
|---|---|---|
| P0 — New articles | 6 | Large |
| P1 — Wrong or materially incomplete | 24 | Medium |
| P2 — Gaps worth filling | 41 | Small–medium |
| P3 — Minor / cosmetic | ~90 | Trivial |
| No doc impact | ~180 | — |

---

## P0 — New articles needed

These are whole features with **zero** coverage in the KB. Four of the six are REDCap+ features, which `RC-PLUS-01` currently only names in passing.

- [ ] **RC-PLUS-02 — Project Migration Tool** *(17.0.0, REDCap+)*
  `RC-PLUS-01` already cites `RC-PLUS-02` as *(planned)* in three places (lines 13, 94, 206) — those are dangling references today. Migrates structure, metadata, data, files and logs between REDCap instances; both source and destination must participate. **Also reconcile with `RC-PROJ-05` (Project Migration)**, which describes the pre-17.0 manual/XML approach and now needs a pointer plus a scope note saying it covers the non-REDCap+ path.

- [ ] **RC-PLUS-03 — Reward Services** *(17.0.0, REDCap+)*
  Participant compensation/payment management. Only string match in the KB is the one-line feature list in `RC-PLUS-01`. Note the 17.1.3 admin option letting Rewards-permission managers enter an audit reason without the extra sensitive-action confirmation step, and the 17.3.3 System Statistics counters.

- [ ] **RC-PLUS-04 — Project Administrator Groups (PAGs)** *(17.1.0, REDCap+)*
  Project-level administration delegated to designated group admins instead of system admins. **Zero** matches in `kb/`. Needs a clear disambiguation section against **Access Control Groups** (`RC-CC-25`) and **Data Access Groups** (`RC-DAG-01`) — three similarly-named grouping constructs is a support-ticket generator.

- [ ] **RC-PLUS-05 — Email Verification & Unsubscribe** *(17.3.0, REDCap+)*
  New smart variables `[email-verify-link]`, `[email-unsubscribe-link]`, `[email-verified]` and others. **Zero** matches. Requires companion entries in `RC-PIPE-03` (Smart Variables Overview) and `RC-PIPE-08` or `RC-PIPE-17`. 17.3.3 added System Statistics counters for this feature.

- [ ] **RC-SHARE-01 — REDCap SHARE** *(17.3.0, REDCap+)*
  Participants connect to supported EHR patient portals and authorise transfer of clinical data into a project. Distinct from CDIS: not institution-specific, works across supported healthcare orgs. **Not covered** — the apparent grep hits are all "REDCap Shared Library" false positives. Subsequent 17.3.1 refinements: public searchable directory of published healthcare organisations in the Control Center, patient-identifier selection by FHIR system/type (exact or regex), authorised-EHR fetching prioritised ahead of retained-payload processing with Job Diagnostics staging, provider-specific CarePlan searches for Epic and SMART Health IT, and SHARE totals split from project participants on System Statistics. Needs cross-refs to and from `RC-CDIS-01`/`RC-CDIS-04`.

- [ ] **RC-ACCESS-01 — Accessibility in REDCap Surveys & Forms** *(16.0.6 → 17.3.0)*
  Roughly a dozen accessibility improvements landed with no home article: screen-reader page-change announcements on surveys, language-selector expand/collapse state, keyboard focus highlighting on survey fields and buttons, slider focus highlighting, keyboard access to date/time pickers, `BR`-tag handling in field labels, accessible Descriptive Popups, auto-scroll-and-focus to the first incomplete required field, login-error association and announcement, and survey navigation button hover/focus glow. Worth one article that consolidates the accessibility posture rather than scattering a sentence across ten articles.

---

## P1 — Wrong or materially incomplete

### Infrastructure & upgrade blockers

- [ ] **`RC-INFRA-01`, `RC-INFRA-02`, `RC-CC-02` — PHP minimum is stale. WRONG**
  15.0.8 dropped PHP 7 (min 8.0.2); **16.0.5 dropped PHP 8.0 — minimum is now PHP 8.1.0**, and PHP 8.5 is officially supported. `RC-INFRA-01` and `RC-CC-02` mention PHP 8.1 but there is **no mention of PHP 8.5 anywhere in the KB**. Anyone provisioning from the current articles may pick an unsupported runtime.

- [ ] **`RC-INFRA-01`, `RC-INFRA-02` — legacy UTF8/UTF8-MB3 charset support dropped. WRONG/NEW**
  16.0.0's "Important Change": REDCap dropped database support for legacy UTF8/UTF8-MB3 charset and collation (MySQL/MariaDB deprecation). **Admins cannot upgrade until the database is converted.** `utf8mb4` appears **nowhere** in the KB. This is the single most likely cause of a blocked upgrade and deserves prominent treatment in both infra articles.

- [ ] **`RC-INFRA-01`, `RC-CC-03` — Content Security Policy header. GAP**
  15.5.1 added a CSP header. Also 15.4.5 added `includeSubDomains` to the HSTS header. Neither string appears in the KB; both matter for reverse-proxy and External Module troubleshooting.

- [ ] **`RC-INFRA-01`, `RC-CC-03` — session cookie renamed. GAP**
  15.7.0 changed the authenticated-session cookie from `PHPSESSID` to an installation-specific name derived from the directory path. Relevant to load balancers, SSO and anything inspecting cookies.

- [ ] **`RC-INFRA-01`, `RC-CC-23` — old version directories are now a stated security risk. GAP**
  15.5.36 flags that leaving old REDCap version directories on the server keeps known vulnerabilities reachable. Pairs with the **Automatic Version Redirect** feature below.

- [ ] **`RC-INFRA-01`, `RC-CC-02` — temp directory must not be web-accessible. GAP**
  15.3.2 security improvement (REDCap now attempts to auto-protect under IIS/Apache), warning text clarified in 15.4.0, and 17.0.2 extended the Configuration Check to verify the user-uploaded file directory is not under webroot when using Local file storage.

### Control Center

- [ ] **`RC-CC-02` + possible new `RC-CC-26` — AI Configuration Settings page. WRONG**
  17.2.0 moved **all** system-level AI configuration out of General Configuration onto a dedicated "AI Configuration Settings" page in the Control Center, with more flexible controls. Any current instruction that routes admins to General Configuration for AI setup is now wrong. Affects `RC-AI-01` too. Also 15.2.0 added Google Gemini and other cloud-hosted AI engine options; 17.1.4 extended Azure OpenAI to support Azure API Management (APIM) gateway deployments.

- [ ] **`RC-CC-02` / `RC-CC-23` — Automatic Version Redirect. GAP**
  17.2.2 added automatic redirection of bookmarks and old survey invitation links pointing at removed version folders. 17.3.0 changed delivery: `redcap_redirect.php` is now embedded directly in the Configuration Check steps rather than downloaded via the non-versioned files workflow. **Not covered.**

- [ ] **`RC-CC-24` / `RC-DE-05` — admins can now add and edit custom field validation types. GAP**
  17.4.0 made the Field Validation Types page editable in the Control Center (absorbing the "Add Validation Types" External Module). `RC-DE-05` should note that the validation list is now site-extensible. Related: 16.0.7 allows custom validations with `email` datatype to be used for the Designated Email Field and survey invitations.

- [ ] **`RC-CC-07` / `RC-SURV-04` — "Survey Link Lookup" renamed to "Link Lookup". WRONG**
  15.9.0 rebranded and expanded the page beyond survey links. Three articles still reference the old name.

- [ ] **`RC-CC-07` — Email Users page overhaul. GAP**
  15.3.0 added saveable named user filters with descriptions and criteria; 15.8.4 added a Username filter.

- [ ] **`RC-CC-11` — System Statistics additions. GAP**
  15.7.5 CSV download button; 16.0.1 unique-users-logged-in stats (past month / past 6 months); 17.3.3 PAG and Email Verification/Unsubscribe stats when a REDCap+ subscription is active; 17.3.1 SHARE totals separated from project participants.

- [ ] **`RC-CC-02` — Configuration Check has changed substantially. GAP**
  Cumulative: temp-subfolder creation test (15.1.1), main-directory-writable check (16.0.15), `.bcmap` MIME type (16.1.5), `.woff2` MIME type (16.1.6), warning when Restricted Upload File Types is unset (16.1.8), webroot check for local file storage (17.0.2), and — **behaviour change** — 17.0.7 restricted service checks to only those services actually enabled, where previous versions checked all regardless.

- [ ] **`RC-CC-02`, `RC-CC-23` — Easy Upgrade. GAP**
  15.0.6 always-visible "Check again" link; 15.9.2 Easy Upgrade start/finish/failure now logged to the User Activity Log; 16.0.15 added a production-server warning; 17.0.0 the version list displays even when Easy Upgrade is disabled; 17.4.0 Easy Upgrade is now usable on AWS CloudFormation / Elastic Beanstalk deployments without added security risk.

### User rights & access

- [ ] **`RC-USER-03` — Form-level Delete rights. GAP**
  15.7.0 introduced per-instrument delete privileges (the Delete Data button on a form) grantable **without** whole-record or event delete rights. `RC-USER-03` matches on "form-level delete" but the granularity change should be verified against the actual privilege table. Related 15.7.5 change: checking "Delete Records" on the User Rights page now behaves differently on save.

- [ ] **`RC-CC-25`, `RC-USER-02` — Access Control Groups have grown since the article was written. GAP**
  16.1.8 added ACG assignment at table-based user creation and on the Edit User page; 17.1.0 added the ACG Project Creation Option (ACGs can gate project creation / creation requests); 17.1.3 removed the User Rights requirement on recipients of ACG alert messages sent via `[user-acg-noncompliant-rights]` — **verify that smart variable is documented in `RC-PIPE-05`**.

- [ ] **`RC-EXPRT-03`, `RC-CC-23` — printing forms without Full Data Set export rights. WRONG**
  17.0.2 made the print version of a data entry form show an error for users lacking Full Data Set export privileges on that instrument; 17.0.4 then added a system-level setting letting admins allow such printing. Two-step behaviour change worth stating precisely.

### Fields, forms & design

- [ ] **`RC-FD-06`, `RC-DE-05`, `RC-FD-08` — Enhanced Signature field type. NEW/GAP**
  17.1.0 added a new, more accessible signature field supporting both scribbled and hand-typed signatures. **Zero** matches in `kb/`. Follow-ups: MLM support for the "Sign Here" and "Please type your signature before saving." strings (17.3.0), and Copy/Paste Fields support (17.3.0). Also check `RC-LOCK-01` for interaction with e-signatures.

- [ ] **`RC-FD-06` — Copy/Paste Fields. GAP**
  17.2.0: Ctrl/Cmd-click the Copy icon in the Online Designer copies field attributes to the clipboard as JSON, pasteable elsewhere. 17.2.1 corrected the on-screen key hint to "Cmd" on Mac. **Not covered.**

- [ ] **`RC-AT-01`, `RC-AT-06` — `@SAVE-PROMPT-EXEMPT` and `@SAVE-PROMPT-EXEMPT-WHEN-AUTOSET`. GAP**
  Both added in 15.2.0; **zero** matches in `kb/`. The `-WHEN-AUTOSET` variant specifically suppresses the "Save your changes?" prompt for values set by `@DEFAULT`, `@SETVALUE`, `@TODAY` or `@NOW` — squarely an autofill-article concern.

- [ ] **`RC-AT-11`, `RC-MYCAP-02`, `RC-MYCAP-08` — `MC-FIELD-SLIDER-BASIC` / `MC-FIELD-SLIDER-CONTINUOUS` removed. WRONG**
  15.7.2 removed both as valid action tags (they only ever worked in an older MyCap app). Two articles still document them. **Highest-confidence factual error found in this pass.**

- [ ] **`RC-CALC-01` — `random()` function missing. GAP**
  17.0.3 added `random(min, max)`. `dayoftheweek()`, `age_at_date()` and `isblanknotmissingcode()` are already present — `random()` is the only one absent.

- [ ] **`RC-FDL-01` — Form Display Logic gained two capability tiers. GAP**
  15.3.2 FDL usable within a specific repeating event; 15.5.1 "Enable support for MyCap App" checkbox applying FDL conditions in MyCap; 15.7.3 **condition-level FDL settings** — granular control per condition across data entry forms, Survey Auto-Continue and MyCap, replacing the previous all-or-nothing model. 17.4.0 converted the form multi-selects to Select2. The 15.7.3 change likely makes existing prose incorrect, not merely incomplete. Also check `RC-IMP-08` (Form Display Logic CSV).

- [ ] **`RC-DE-02` — Section Navigation box. GAP**
  16.1.5 added an always-visible right-hand navigation box on data entry forms for jumping between sections. **Not covered**, and it is a visible change every data-entry user will notice.

### Surveys & alerts

- [ ] **`RC-ALERT-01`, `RC-SURV-06` — "Re-evaluate Send Time" for Alerts & ASIs. GAP**
  17.2.0 added the ability to re-evaluate scheduled send times for alerts and ASIs sent relative to a stored date/time. Note for readers: 17.3.7 LTS / 17.4.1 Standard fixed two significant bugs in it (the checkbox not persisting, and incorrect rescheduling on unrelated data changes) — **document the feature as requiring ≥17.4.1 / ≥17.3.7 to behave correctly.**

- [ ] **`RC-ALERT-01` — Pause Recurring Alerts. GAP**
  15.4.0 added "Allow pausing of recurrences?" for conditional alerts using "Ensure logic is still true…". **Not covered.**

- [ ] **`RC-CC-02`, `RC-ALERT-01` — Universal DO-NOT-REPLY address. GAP**
  15.4.0 added a system-level do-not-reply From/Reply-To address for automated system email. `RC-CC-02` mentions it; `RC-ALERT-01` should note the interaction with alert From addresses.

- [ ] **`RC-SURV-03` — survey "Save & Return Later" security correction. WRONG (behaviour)**
  17.4.1 / 17.3.7 fixed a flaw where a Return Code worked against another participant's survey link. If any KB text describes Return Code scope loosely, tighten it: a Return Code is valid **only** for its own participant-specific link.

---

## P2 — Gaps worth filling

### CDIS — the largest cluster (~45 entries)

`RC-CDIS-01` through `RC-CDIS-04` are the most out-of-date articles in the KB relative to the changelog. Notably, **"Break the Glass" / "Break-the-Glass" appears nowhere in `kb/`**, and neither does **"Mapping Helper"** or **"gender identity"**, despite BTG being a recurring theme across 15.0.0–17.2.x.

- [ ] `RC-CDIS-01` — **Break the Glass (BTG)**, Epic-only, has no coverage at all. Improvements: logging detail for success and failure paths (15.0.0); improved workflow when not using the Patient/demographics mapping (15.4.0); deferred token requests (15.8.1); clearer FHIR token feedback (15.8.4); resource/endpoint-level protection beyond patient-level (16.0.4); cached protected-patient-list TTL raised 5→10 days (16.0.6); cache files moved to the REDCap temp folder (16.0.8); state moved to temp-data tables for deployment safety (16.1.1); confirmation step now accepts email code, SMS code, Duo push and OTP in addition to password (16.1.2).
- [ ] `RC-CDIS-01` — CDIS Access Token Priority Rules Manager (15.1.0), letting project owners prioritise FHIR access tokens. **Not covered.**
- [ ] `RC-CDIS-01`/`RC-CDIS-03` — EHR demographic expansion: FHIR ID as patient identifier, pronouns and other personal preferences (15.3.3); multi-race mapping via a "Race (all coded values)" field without breaking single-value setups (15.9.0); **gender identity mapped separately from legal sex, sex assigned at birth, and sex for clinical use** (17.1.3).
- [ ] `RC-CDIS-02` — CDP adjudication was rebuilt across many releases: cleaner layout (15.6.0); validation display improvements (15.7.4); empty-EHR-response guidance (15.7.4, 15.9.0); transformer-adjusted item counts and always-available Save (15.7.5); pre-fetch validation of record identifier and temporal reference field (17.2.1); display options to show matching REDCap values first and narrow to instrument/event/instance (17.2.1).
- [ ] `RC-CDIS-02` — Mapping Helper additions: review pasted/uploaded FHIR payloads without a live fetch, and search for patient identifiers by entering demographics (both 17.1.3). CDP Mapping Setup now reachable directly from the project's Clinical Data Interoperability Services menu (17.2.0). Mapping page refactored to a form-based workflow with event-aware copy tools (16.0.8), sticky header and select-all when copying to multiple events (16.0.9), validation messages under the related column (16.0.9).
- [ ] `RC-CDIS-01` — infrastructure: weekly cron to prune expired FHIR tokens (16.0.0); dedicated CDIS temp-file folder (16.0.8); fetch reconciler for stuck "fetching" records (16.0.8); Twig replaces Blade in the EHR authorisation workflow (15.5.0); per-MRN/per-resource subprocesses for Data Mart fetches (15.9.0); Data Mart processing now follows record sort order rather than MRN order (16.1.2); grouped diagnostics and sanitized token-endpoint detail on the FHIR launcher error page (17.2.0); SMART on FHIR EHR launch context retention through Shibboleth and external login handoffs (17.1.2).

### MyCap (~40 entries)

`RC-MYCAP-01` … `RC-MYCAP-08`. Beyond the removed slider action tags already listed as WRONG in P1:

- [ ] `RC-MYCAP-05` — **MyCap Email Notifications** (15.7.0): a Messages tab for composing email notifications sent when a participant message arrives, with DAG awareness. Participant List columns added: Last accessed (16.0.6), App Version (17.0.1), Device Info (17.2.2). "Delete/Undelete" renamed **"Disable/Enable"** with participant notification (15.3.3) — a rename worth checking for stale text. Message search (15.8.4), announcement search (16.0.6), scheduled announcements (16.0.9), message CSV download (16.1.4). Purple is now the default theme (15.8.4).
- [ ] `RC-MYCAP-02` — Signature-type fields now receive data from the app (15.4.1); `@latitude`/`@longitude` supported inside tasks (15.4.5) — verify `RC-AT-11` reflects the MyCap context; `[survey-link]` usable in MyCap task field labels (15.8.4); rich text editor for task instructions and completion steps (16.0.8) and Intro/Capture page instructions (16.1.5); retroactive-completion day limit (17.3.1); warning when a chart field is not Required (15.7.5).
- [ ] `RC-MYCAP-07` — MLM language-switch lockout option (15.6.0); three new app languages Zulu `zu-ZA`, Afrikaans `af-ZA`, Czech `cs-CZ` (17.0.4); DAG-specific Contacts/Links/About pages (15.4.2).
- [ ] `RC-MYCAP-01`/`RC-MYCAP-08` — server max-upload limit now in the config JSON (16.1.2); baseline-date field guardrails (15.5.6); notice after 30 days with MyCap enabled but no tasks (15.7.5); Participant List performance (15.5.5).

### Multi-Language Management

- [ ] `RC-MLM-01` — cookie policy text translatable, under the User Interface tab (15.8.1); `__lang` URL parameter to preset Survey Queue language (15.0.1); true/false and yes/no choice labels are fixed and cannot be translated per-field (15.0.1); embedded-field preservation notice (15.2.4); Snapshot facility moved from the Settings tab to the **Languages tab** (15.4.5 — stale-navigation risk); "Language preference field" wording changed (15.5.1); AI translation prompt now includes the target language ID (15.5.1); on-the-fly swapping of calc/CALCTEXT piping sources (17.0.0); `:field-label` piping support (17.0.4); **"Discourage browser-based translation of survey pages"** setting (17.1.0); `lang` attribute now re-evaluated on language switch, not only page load (16.0.6, 17.1.0); JSON export now carries **LLM-friendly instructions** for export → translate → re-import workflows (17.1.3).

### Reports, exports & dashboards

- [ ] `RC-EXPRT-06` — "Quick Set" on Edit Report Step 2: paste or type field names to add/replace report fields (15.5.0), plus a link to copy all current report field names (15.5.1).
- [ ] `RC-EXPRT-08`, `RC-PROJ-03` — **access code protection for public reports and public project dashboards** (16.0.5). `[report-access-code]` is already in `RC-PIPE-15` ✓; confirm the dashboard equivalent is in `RC-PIPE-14`.
- [ ] `RC-EXPRT-05` — the export dialog now cites the Randomization publication when randomization is set up (15.5.0) and the External Module Framework publication when EMs are enabled (15.5.0).
- [ ] `RC-NAV-REC-04` — aggregate and project-level smart variables now work in Custom Record Status Dashboard descriptions (15.7.2); row hover/keyboard-focus highlighting (16.1.1).

### Records, data entry & navigation

- [ ] `RC-DE-13` — "Choose action for record" gained links to Logging, Notification Log and Survey Invitation Log (15.0.3), Survey Queue always shown even when empty (15.0.6), and Email Logging when the user has access (15.7.2).
- [ ] `RC-NAV-REC-03`, `RC-DE-10` — repeating-instrument tables/popups rewritten (15.3.2, refined 15.3.3, custom label link reverted 15.4.1); custom paging size (15.4.3); status filters persist per table (15.5.5); sort order persists per user per project (15.7.2); **Previous/Next links between repeating event instances** (17.0.7).
- [ ] `RC-DE-01` — searchable record and field drop-downs on Add/Edit Records (17.0.7); user preferences to remember the last search target and force searches to the Record Home Page (16.1.4); "Save & Go To Next Record" behaviour at the end of the record list with auto-numbering (15.7.0).
- [ ] `RC-PROJ-01`/`RC-DE-13` — Bulk Record Delete: background deletion option (15.6.0), instructional text corrected (15.8.4), **delete "all records from a report"** (17.4.0), and the 17.2.0 UI rule that unselecting an instrument unselects its event.
- [ ] `RC-DQ-01` — DQ rules A–I runnable against selected fields (16.0.0); multi-record and multi-DAG filters (16.0.7); bulk delete of DQ rules (15.9.0); rule E behaviour when no numeric fields exist or are accessible (15.8.2).
- [ ] `RC-DE-12` — new project-level setting "Prevent calc/CALCTEXT fields with closed/verified data queries from being fixed by DQ rule H" (15.9.0); DAG-aware assignment of queries (15.0.1).
- [ ] `RC-FD-05` — Codebook: internal links from the Instruments table to the fields table (15.0.3), event IDs in the Events table (15.4.1), per-instrument download icons (16.1.4).
- [ ] `RC-LOG-01` — "SYSTEM" always present in the username filter (15.9.3); last-activity timestamp at top right (16.1.8); Email Logging searchable record drop-down (15.7.2) and a Type column in results (17.2.0); PDF downloads now log instrument/event/instance context and compact-format flag (17.0.0).

### API

- [ ] `RC-API-01` — the project API page now masks the token by default with a click-to-reveal control, and API/API Playground behaviour was improved (17.0.7).
- [ ] `RC-API-13` — Import File and `REDCap::addFileToField` accept the literal `new` to target a not-yet-created repeating instance (17.4.0).
- [ ] `RC-API-22` — Export Users returns `data_access_group_label` (16.0.0).
- [ ] `RC-API-46` — File Repository listing returns `role` and `dag` (16.0.8).
- [ ] `RC-API-34`/`RC-API-35` — P.I. email address handled correctly on Import/Export Project Info (15.8.2).
- [ ] `RC-API-01` — developer method `REDCap::getSurveyAccessCode()` (15.1.0), companion to the already-documented `RC-API-54`. Note the changelog's own typo, `getSurveyAccesCode`.

### External Modules

- [ ] `RC-EM-01` — Framework advanced to **Version 17** with strict Twig variables (17.0.1); new EM API endpoints (15.5.2); Twig 3 bundled in REDCap core beyond the EM Framework (15.5.0); edoc-id hashing on EM file uploads and in-module documentation linking (17.3.1); better failed-download error messaging (16.1.6); autocomplete drop-downs in EM config (16.1.8); **two new hooks — `redcap_module_dashboard_before_render` and `redcap_module_dashboard_after_render`** (17.4.0). Also 15.6.0: EM links now display in the left-hand menu while a project is in Analysis/Cleanup status, where previously they did not.
- [ ] `RC-CC-25` — note that Access Control Groups is the productised form of Andrew Poppe's "Security Access Groups" EM, that upgrading does **not** disable the EM, and that settings are **not** migrated (16.0.0). Same pattern for `RC-CC-24`/`RC-DE-05` and Adam Nunez's "Add Validation Types" EM (17.4.0).

### Miscellaneous

- [ ] `RC-FILE-01` — **admin-restricted folders** in the File Repository, visible only to admins with all-project access (15.5.0). Project-level override for max upload size on Edit Project Settings (16.1.0). Neither covered.
- [ ] `RC-CC-03` — OIDC scopes manually specifiable (15.4.2); more specific OIDC error output (15.7.0); custom button text for the "Local REDCap Login" button under OIDC & Table-based / Entra ID & Table-based (16.1.2); Duo library updated (15.9.2); Caps Lock warning on table-based login (15.7.2); **6-digit PIN required only once per session for e-signing under 2FA** (15.4.0) and the Duo-push equivalent (16.1.2); e-signature dialog text under "X & Table-based" 2FA (15.2.6).
- [ ] `RC-TXT-01`/`RC-TXT-02` — Twilio Alphanumeric Sender ID is in `RC-TXT-01` ✓ but confirm the outgoing-SMS-only limitation is stated; admin approval workflow for enabling Mosio/Twilio per project (15.6.0).
- [ ] `RC-FD-06` — new Online Designer methods for editing instrument label and unique instrument name (15.1.0); survey status icons for e-Consent and Stop Actions (15.1.0); field-count shown when bulk-updating branching logic (15.2.2); warning for instruments not designated to any event in longitudinal projects (15.2.6); rich text editor for Matrix Header Text (17.0.6); opt-out of the 26-character variable-name warning, per user per project (17.1.0); extra Draft Mode warning when temporary metadata changes already exist (17.3.0); "Go to field" via Ctrl-G/Cmd-G from the instrument overview (17.4.1); Standardized Field (CDE) search — **formerly "Field Bank"** — gained categories (16.0.7), so check `RC-FD-06` and `RC-CC-02` for the old name.
- [ ] `RC-LONG-01` — direct link to "Define My Events" in the left-hand menu (15.3.3, repositioned 15.4.0); repeating instrument/event icons across Define My Events, Designate Forms and Online Designer (15.4.5); **"Designate Instruments for My Events" now directly accessible from the left-hand menu** with a Print Page button (17.4.1); accented characters in DAG and event names are transliterated in the unique names for **new** projects (17.3.0).
- [ ] `RC-PROJ-01` — record limit for development projects is in `RC-CC-02`/`RC-PROJ-01` ✓; add the 15.5.5 admin bypass when copying a project. Project deletion purge-delay setting (15.2.6). Project Home stats now show instrument counts, event/arm counts (16.0.7) and created/production/analysis timestamps (16.0.9).
- [ ] `RC-PROJ-04` — Secondary Unique Field best-practice warning (15.8.0); clarified text on deleting a record's logging activity (15.7.2); extra confirmation on "Erase all data" in production (15.7.2). **Security-relevant:** 17.0.2 blocked administrators from injecting JavaScript into branching logic or calc/CALCTEXT equations — if any KB article suggests JS in logic as a technique, it must be corrected.
- [ ] `RC-FD-03`/`RC-FD-08` — Data Dictionary page UI simplified (15.0.1); multiple-choice fields with no choices now warn rather than error on upload (15.9.2); syntactically invalid branching logic, calculations and CALCTEXT are **automatically commented out** when creating a project from Project XML (17.0.3).
- [ ] `RC-FD-07`/`RC-FD-09` — pre-embedded text in a multiple-choice **choice label** is no longer displayed (15.7.3). Behaviour change affecting existing designs.
- [ ] `RC-DE-02`/`RC-CALC-02` — branching-logic and calculation errors are now combined into a single dialog listing all affected fields (15.7.0). Supported HTML tags in user input expanded: `blockquote` (15.0.1), `wbr` (15.4.5), `ruby` (15.5.6) — `RC-FD-08` likely carries the allowed-tag list.
- [ ] `RC-LOCK-01` — locking/e-signature settings from the Record Locking Customization page are now exportable and importable via Project XML (16.0.7).
- [ ] `RC-MSG-01` — "Mark all conversations as read" (15.7.4).
- [ ] `RC-CAL-01` — calendar table widened (16.0.7).
- [ ] `RC-MOB-01` — Mobile App dashboard now shows username, install time and latest-activity timestamps (16.1.8).
- [ ] `RC-CC-17` — Database Query Tool CSV exports include the custom query title in the filename (15.2.1).
- [ ] `RC-CC-05` — Azure Blob Storage supports Azure Government Cloud, US only (15.2.1); Restricted Upload File Types enforcement strengthened (15.8.0); the setting moved from Security & Authentication to File Upload Settings (16.0.1) — **check `RC-CC-03` for a stale pointer**.
- [ ] `RC-CC-08` — custom text at the top of the Create New Project page (15.0.0); "Custom footer text for survey pages" settable on Default Project Settings (15.9.0).
- [ ] `RC-CC-04` — new settings governing how users are added to projects, at the bottom of the User Settings page (16.1.5).
- [ ] `RC-PROJ-01` — non-admin users with Project Design rights can now clear the Record List Cache and Rapid Retrieval cache from Other Functionality (16.1.8).
- [ ] `RC-SURV-05` — Rapid Retrieval caching on the Participant List, its CSV export and the API export method (15.0.0); hardcoded links no longer persisting from previously sent invitations in Compose Survey Invitations (15.2.5).
- [ ] `RC-SURV-01`/`RC-SURV-02` — Descriptive Popup inline text limit raised to 255 characters with a maxlength safeguard (17.4.0); descriptive-field inline images no longer add leading space when the label is empty (15.6.0).
- [ ] `RC-DE-06` — BioPortal auto-selected when it is the only ontology service available (15.6.1).
- [ ] `RC-DDE-01` — form status icons on the Record Status Dashboard and Record Home Page now route correctly for DDE person 1/2 (15.8.2).
- [ ] `RC-USER-04` — "Manage All Project Tokens" indicates suspended users (15.8.2); API Tokens page has searchable drop-downs (17.1.0); duplicate-username detection when adding table-based users (17.0.6); User Allowlist "Delete all" uses a modern dialog (16.1.1); Sponsor Dashboard approval shows only affected users (16.1.1); "Password was last reset on X" reworded to "…by an admin on X" (16.1.1).
- [ ] `RC-FD-04` — PROMIS battery event designation when the first instrument is already designated (15.3.1).

---

## P3 — Minor / cosmetic

Roughly 90 entries are pure styling, wording, performance or internal-plumbing changes with no instructional consequence: button styling on the randomization setup page (15.0.1), Font Awesome 6.7.2 → 7.0.0 (15.5.5), My Projects page widened (15.9.2), `redcap_new_record_cache` table pruning (15.7.0), session-storage column widening (15.5.0), new data and log_event tables (16.0.0), cron-job management improvements (16.1.2), assorted logic-evaluation and CDP dashboard optimisations, and ESC-key dialog handling (15.4.1). Fold these in opportunistically; none justifies a dedicated edit.

Two are worth a line **if** the relevant article is already open:
- Fatal-error reports now include a privacy-safe snapshot of in-flight work (17.3.1) → `RC-INFRA-01`.
- MLM admin and end-user PDF manuals ship with REDCap (15.5.1) → `RC-MLM-01`.

---

## Already current — no action

Spot-checked and confirmed present in the KB, despite post-dating the nominal article versions:

| Change | Version | Covered in |
|---|---|---|
| `dayoftheweek()` | 15.8.0 | `RC-CALC-01` |
| `isblanknotmissingcode()` and companions | 15.7.0 | `RC-CALC-01` |
| `age_at_date()` | 16.1.1 | `RC-CALC-01`, `RC-CALC-02` |
| `[project-irb-number]`, `[project-purpose]`, `[project-status]`, `[project-title]` | 15.9.0 | `RC-PIPE-17` |
| `[report-access-code]` | 16.0.5 | `RC-PIPE-15` |
| `combineCheckboxOptions` on Export Records | 15.6.0 | `RC-API-02` |
| Export Survey Access Code API | 15.1.0 | `RC-API-54` |
| Survey Settings CSV import/export | 15.8.0 | `RC-IMP-07`, `RC-IMP-03` |
| Custom CSS for forms and surveys | 15.5.0 | `RC-FD-11` |
| Twilio Alphanumeric Sender ID | 15.2.0 | `RC-TXT-01` |
| Record limit for development projects | 15.5.0 | `RC-CC-02`, `RC-PROJ-01`, `RC-CC-04` |
| Universal DO-NOT-REPLY address | 15.4.0 | `RC-CC-02` |
| Access Control Groups (core feature) | 16.0.0 | `RC-CC-25` |

---

## Suggested order of work

1. **`RC-AT-11` / `RC-MYCAP-02` / `RC-MYCAP-08`** — remove the deleted slider action tags. Smallest edit, clearest factual error.
2. **`RC-INFRA-01` / `RC-INFRA-02`** — PHP 8.1 minimum, PHP 8.5 support, UTF8MB3 upgrade blocker. Highest operational risk.
3. **`RC-CC-02` / `RC-AI-01`** — AI Configuration Settings page relocation. Actively misroutes admins today.
4. **P0 REDCap+ articles** — `RC-PLUS-02` first, since `RC-PLUS-01` already has three dangling references to it.
5. **`RC-CDIS-*`** — largest single backlog; consider a dedicated pass rather than folding into general work.
6. Everything else by domain.

---

## Caveats

- Bug fixes and security fixes were excluded by scoping choice. The Save & Return Later Return Code fix (17.4.1 / 17.3.7) is included above only because it changes documented behaviour; there may be other behaviour-altering fixes in the ~6,000 excluded rows. Re-run with `Major bug fix` enabled if you want that swept too.
- Article-to-change matching was automated then hand-reviewed, but article *sections* were not read in full. Confirm the target section before editing — several items are flagged GAP where the article may already say something adjacent.
- Only 42 of 243 articles carry an explicit REDCap version in their metadata. Adding a pinned version to the rest would make the next changelog diff far cheaper.

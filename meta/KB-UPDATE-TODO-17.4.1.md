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

- [x] **REDCap SHARE — filed as `RC-CDIS-05`, not a new SHARE domain** *(17.3.0, REDCap+)* — *done 2026-08-18*
  Written from a live Control Center capture (LTS 17.3.6, no subscription) plus release notes. **Filed in the CDIS series**: every language key on the page is prefixed `cdis_pm_`, the feature is implemented in the CDIS codebase, and readers comparing SHARE against CDP/CDM will look there. No new slug needed.
  Covered: participant-mediated retrieval and how it differs from CDP/CDM, the fact that REDCap never receives portal credentials, the setup-survey and allow-list onboarding chain, the REDCap SHARE user right, the public organization directory and participant info page, and the 17.3.1 refinements. `RC-CDIS-04` gained a pointer noting a third option now exists.
  **Still pending:** the Projects tab and all in-project setup, dashboards and mapping UI — flagged in-article as unverified, needs a capture from a subscribed instance.
  *Original entry below, retained for context.*
  Participants connect to supported EHR patient portals and authorise transfer of clinical data into a project. Distinct from CDIS: not institution-specific, works across supported healthcare orgs. **Not covered** — the apparent grep hits are all "REDCap Shared Library" false positives. Subsequent 17.3.1 refinements: public searchable directory of published healthcare organisations in the Control Center, patient-identifier selection by FHIR system/type (exact or regex), authorised-EHR fetching prioritised ahead of retained-payload processing with Job Diagnostics staging, provider-specific CarePlan searches for Epic and SMART Health IT, and SHARE totals split from project participants on System Statistics. Needs cross-refs to and from `RC-CDIS-01`/`RC-CDIS-04`.

- [ ] **RC-ACCESS-01 — Accessibility in REDCap Surveys & Forms** *(16.0.6 → 17.3.0)*
  Roughly a dozen accessibility improvements landed with no home article: screen-reader page-change announcements on surveys, language-selector expand/collapse state, keyboard focus highlighting on survey fields and buttons, slider focus highlighting, keyboard access to date/time pickers, `BR`-tag handling in field labels, accessible Descriptive Popups, auto-scroll-and-focus to the first incomplete required field, login-error association and announcement, and survey navigation button hover/focus glow. Worth one article that consolidates the accessibility posture rather than scattering a sentence across ten articles.

---

## P1 — Wrong or materially incomplete

### Infrastructure & upgrade blockers

- [x] **`RC-INFRA-01`, `RC-INFRA-02` — PHP version coverage incomplete. GAP** — *done 2026-08-18*
  **Correction to this report:** originally tagged WRONG on the grounds that the PHP minimum was stale. It was not — `RC-INFRA-01` already said PHP 8.1, which is correct for 16.0.5+. The real gaps were the **PHP 8.5 support** added in 16.0.5 and the **upgrade-page fatal under PHP 8.4/8.5** on versions at or below 16.0.9 Standard / 16.0.10 LTS, which can strand an instance because it blocks the upgrade *out of* the affected version.
  Applied: version table in `RC-INFRA-01` §3.1 covering both the 15.0.8 and 16.0.5 thresholds, with a version caveat for the upgrade-page fatal and the drop-to-8.3 workaround. `RC-CC-02` still to check separately.

- [x] **`RC-INFRA-01`, `RC-INFRA-02` — legacy UTF8/UTF8-MB3 charset support dropped. WRONG** — *done 2026-08-18*
  **Correction to this report:** the drop happened in **15.6.0**, not 16.0.0 as originally stated. The changelog is explicit: administrators cannot upgrade to **15.6.0 or higher** until the Unicode Transformation has been performed. Getting this wrong by four minor versions would have sent readers looking in the wrong place.
  Applied: `RC-INFRA-01` §3.2 as a Critical callout with the remediation paths (13.2.0+ via Configuration Check; below 13.2.0 upgrade to 15.5.0 first; 15.5.40 as the safe staging version when a transformation is merely suspected). Database row in §3 now specifies `utf8mb4`. Two new gotchas. `RC-INFRA-02` §9 gained a pre-upgrade prerequisites list and §9.1 a known-bad versions table.

- [x] **`RC-INFRA-01`, `RC-CC-03` — Content Security Policy header. GAP** — *done 2026-08-18*
  CSP added 15.5.1, HSTS `includeSubDomains` 15.4.5. **The detail that matters was missing from this report:** REDCap deliberately **does not override a CSP header already set by the web server**, so a proxy-level CSP replaces rather than supplements REDCap's — and a stricter policy breaks External Modules in ways that look like module faults. Applied to `RC-INFRA-01` §4a.1 and `RC-CC-03` §12.3.

- [x] **`RC-INFRA-01`, `RC-CC-03` — session cookie renamed. GAP** — *done 2026-08-18*
  15.7.0. **Report understated the reason:** this is not cosmetic. Before 15.7.0, two REDCap installations on one server and domain shared the `PHPSESSID` name, so logging into the second destroyed the session in the first — running production and test on one host was actively broken. Applied to `RC-INFRA-01` §4a.2 and `RC-CC-03` §12.4, with a caveat for anything pinning the cookie by name.

- [x] **`RC-INFRA-01`, `RC-CC-02` — old version directories are a stated security risk. GAP** — *done 2026-08-18*
  **Two corrections.** The Standard version is **16.1.4**, not 15.5.36 (that was the LTS number). And the report omitted REDCap's own qualifier: it is *not* necessary to remove all old version directories at every future upgrade — the Configuration Check names the specific versions of concern.
  **Retargeted:** originally assigned to `RC-CC-23` (Backup Options), which is the wrong home — version-directory lifecycle is not a backup topic. Went to `RC-CC-02` (Configuration Check) and `RC-INFRA-01` §4a.4 instead.
  Folded in as one story: 16.1.5 blocks version-directory URLs for survey and API endpoints (`/api/index.php`, not `/redcap_vXX/API/index.php` — breaks hardcoded integrations), 17.2.2 adds Automatic Version Redirect, 17.3.0 and 17.4.0 fix it, and 16.1.7 warns that Rapid Retrieval caches can 404 once a version directory is removed.

- [x] **`RC-INFRA-01`, `RC-CC-02` — temp directory must not be web-accessible. GAP** — *done 2026-08-18*
  15.3.2, wording clarified 15.4.0, webroot check for uploaded files 17.0.2, subfolder-creation check 15.1.1. **Key detail the report missed:** REDCap auto-writes `web.config` and `.htaccess`, which protects IIS and Apache and does **nothing on NGINX** — those admins must block access themselves. Applied to `RC-INFRA-01` §4a.3 and `RC-CC-02` Directory Security Checks.

### Control Center

- [x] **New `RC-CC-26` — AI Configuration Settings page. WRONG** — *done 2026-08-18*
  **Correction to this report:** the affected article was `RC-CC-06` (Modules & Services Configuration), not `RC-CC-02` (General Configuration). `RC-CC-02` contains no AI content at all and never did. The AI settings moved *out of Modules/Services*, and `RC-AI-01` was pointing readers there.
  Verified against live captures from LTS 16.0.39 and LTS 17.3.6: on 17.3.6 the AI Services section is **absent from Modules/Services entirely** — no heading, no link, no residual fields. Page location confirmed as System Configuration → AI Configuration Settings, directly below Modules/Services Configuration.
  Applied: new `RC-CC-26` documenting the page, the three enablement scopes (including the easily-missed "all non-project pages"), the configuration table, the project-level selector, and an old→new settings mapping. `RC-CC-06` §AI Services retained for LTS 16.0.x readers behind a version caveat. `RC-AI-01` Administrator Configuration now routes by version.
  Still open: 15.2.0 Gemini and other engine options (already in `RC-CC-06`); **17.1.4 Azure OpenAI via Azure API Management (APIM) gateways — not yet documented anywhere.**

- [x] **`RC-CC-02` — Automatic Version Redirect. GAP** — *done 2026-08-18*
  Covered as part of the old-version-directory story above rather than separately, since 16.1.4, 16.1.5, 17.2.2, 17.3.0 and 17.4.0 are one continuous thread. Added: instructions cover Apache, NGINX and IIS only and require web server changes; a version caveat that 17.2.2–17.2.3 instructions named the **wrong directory** (version folder instead of REDCap root, fixed 17.3.0), and that 17.4.0 moved the redirect's own config check to client-side JavaScript after server-side URL testing proved unreliable.

- [x] **`RC-CC-08` / `RC-DE-05` — admins can now add and edit custom field validation types. GAP** — *done 2026-08-18*
  **Retargeted:** the Field Validation Types page is documented in `RC-CC-08` §6, not `RC-CC-24`. Applied there with the 17.4.0 in-UI add/edit capability, the absorbed "Add Validation Types" EM, and two version-independent consequences worth stating: copying an instrument or importing a Project XML fails if the target server lacks a custom validation type, and `email`-datatype custom validations can be used for the Designated Email Field (16.0.7).
  *Original entry:*
  17.4.0 made the Field Validation Types page editable in the Control Center (absorbing the "Add Validation Types" External Module). `RC-DE-05` should note that the validation list is now site-extensible. Related: 16.0.7 allows custom validations with `email` datatype to be used for the Designated Email Field and survey invitations.

- [x] **`RC-CC-21` — "Survey Link Lookup" renamed to "Link Lookup". NOT WRONG** — *done 2026-08-18*
  **Correction to this report: there was no error to fix.** The claim that "three articles still reference the old name" was an artefact of my grep matching the *new* name. A literal search for "Survey Link Lookup" returns **zero** hits KB-wide — the rename had already been applied. `RC-CC-21` was the only article describing the page, and it was already correct.
  Applied anyway: expanded its one-line entry to record the 15.9.0 rebrand and that the page now also searches survey queue links, public report links and public project dashboard links, which it did not previously say.
  *Original entry:*
  15.9.0 rebranded and expanded the page beyond survey links. Three articles still reference the old name.

- [x] **`RC-CC-07` — Email Users page overhaul. GAP** — *done 2026-08-18*
  The article already documented the rule-based filter builder. Added the part that was missing: **saved named filters** (15.3.0) with name, description and criteria, reusable across mailings — which is the actual point of the 15.3.0 rework — plus the 15.8.4 Username filter and a note that several filter *semantics* were wrong on older versions (active-status inflation 15.3.3; "does not contain"/"does not end with"/"is null" missing User Email matches 15.7.2).
  *Original entry:*
  15.3.0 added saveable named user filters with descriptions and criteria; 15.8.4 added a Username filter.

- [x] **`RC-CC-11` — System Statistics additions. GAP** — *done 2026-08-18*
  CSV download (15.7.5) was already covered. Added: unique-users-logged-in counts for the past month and 6 months (16.0.1), and a REDCap+/SHARE table covering the 17.3.1 split of project participants from EHR-specific records and the 17.3.3 PAG and Email Verification/Unsubscribe counts.
  *Original entry:*
  15.7.5 CSV download button; 16.0.1 unique-users-logged-in stats (past month / past 6 months); 17.3.3 PAG and Email Verification/Unsubscribe stats when a REDCap+ subscription is active; 17.3.1 SHARE totals separated from project participants.

- [x] **`RC-CC-02` — Configuration Check has changed substantially. GAP** — *done 2026-08-18*
  Remaining items after the previous commit: main-REDCap-directory-writable check (16.1.4, wording clarified 16.1.5), restricted-upload-types warning (16.1.8), `.bcmap` (16.1.5) and `.woff2` (16.1.6) MIME checks, and the 17.0.7 behaviour change limiting service checks to enabled features only. Also recorded two checks **withdrawn as unreliable** so nobody chases them: the MySQL 8.4 `restrict_fk_on_non_standard_key` recommendation (added 15.6.1, removed 15.8.4) and a Windows-only cron check (removed 17.3.0).
  *Original entry:*
  Cumulative: temp-subfolder creation test (15.1.1), main-directory-writable check (16.0.15), `.bcmap` MIME type (16.1.5), `.woff2` MIME type (16.1.6), warning when Restricted Upload File Types is unset (16.1.8), webroot check for local file storage (17.0.2), and — **behaviour change** — 17.0.7 restricted service checks to only those services actually enabled, where previous versions checked all regardless.

- [x] **`RC-CC-02` — Easy Upgrade. GAP** — *done 2026-08-18*
  **The important finding was a direct conflict the report missed.** 16.1.4 added *both* a Configuration Check recommending the main `redcap` directory be made non-writable by the application, *and* a warning that Easy Upgrade is no longer recommended on production — because Easy Upgrade requires exactly that write access. The two recommendations cannot both be satisfied; it is a documented trade-off, and 17.4.0's AWS Elastic Beanstalk exception exists because those deployments replace the directory wholesale. Also added: 15.0.6 "Check again" link, 15.9.2 logging to the User Activity Log, 17.0.0 version list shown even without Easy Upgrade, and a caveat for the 15.8.2 "must be taken offline" message that was wrong (fixed 15.8.3). Dropped `RC-CC-23` as a target — Easy Upgrade is not a backup topic.
  *Original entry:*
  15.0.6 always-visible "Check again" link; 15.9.2 Easy Upgrade start/finish/failure now logged to the User Activity Log; 16.0.15 added a production-server warning; 17.0.0 the version list displays even when Easy Upgrade is disabled; 17.4.0 Easy Upgrade is now usable on AWS CloudFormation / Elastic Beanstalk deployments without added security risk.

### User rights & access

- [x] **`RC-USER-03` — Form-level Delete rights. GAP** — *done 2026-08-18*
  **Mostly a false alarm.** The article already documented the feature accurately, including the View & Edit and Edit Survey Responses prerequisites and the Delete Records inheritance. Only real fix: replaced the vague "may not appear at all institutions depending on local configuration or REDCap version" with the actual threshold — **requires 15.7.0** — and named the Delete Data button it enables.
  *Original entry:*
  15.7.0 introduced per-instrument delete privileges (the Delete Data button on a form) grantable **without** whole-record or event delete rights. `RC-USER-03` matches on "form-level delete" but the granularity change should be verified against the actual privilege table. Related 15.7.5 change: checking "Delete Records" on the User Rights page now behaves differently on save.

- [x] **`RC-CC-25` — Access Control Groups have grown since the article was written. GAP** — *done 2026-08-18*
  Added ACG assignment at account creation and on the Edit User page (16.1.8); new §7a **Project Creation privilege** (17.1.0), noting it departs from ACG's usual "ceiling on grantable rights" model by granting or denying an instance-level capability outright; and the 17.3.3 closure of the obvious loophole — denying project creation did not stop project *copying* until copying began requiring both create permission and Full Access rights. Expanded §8 with the two ACG smart variables and the 17.1.3 removal of the User Rights requirement on `[user-acg-noncompliant-rights]`, which had been preventing exactly the users who needed the message from receiving it. `RC-USER-02` needed no change.
  *Original entry:*
  16.1.8 added ACG assignment at table-based user creation and on the Edit User page; 17.1.0 added the ACG Project Creation Option (ACGs can gate project creation / creation requests); 17.1.3 removed the User Rights requirement on recipients of ACG alert messages sent via `[user-acg-noncompliant-rights]` — **verify that smart variable is documented in `RC-PIPE-05`**.

- [x] **`RC-EXPRT-03` — printing forms without Full Data Set export rights. WRONG** — *done 2026-08-18*
  **Correction to this report:** the sequence was not "17.0.2 restricted, 17.0.4 added a setting to allow it". 17.0.4 explicitly **reverted** the 17.0.2 restriction and made the whole behaviour an administrative setting on the Control Center **User Settings** page. New `RC-EXPRT-03` §4a gives the three-state version table and tells admins to **verify the setting after upgrading**, since an instance that crossed both versions may not be in the state anyone expects. Also carried REDCap's own admission that the restriction is client-side and "inherently bypassable" — a deterrent against accidental print-to-PDF export, not an access control. Dropped `RC-CC-23`; not a backup topic.
  *Original entry:*
  17.0.2 made the print version of a data entry form show an error for users lacking Full Data Set export privileges on that instrument; 17.0.4 then added a system-level setting letting admins allow such printing. Two-step behaviour change worth stating precisely.

### Fields, forms & design

- [x] **`RC-FD-06` — Enhanced Signature field type. NEW/GAP** — *done 2026-08-18*
  Documented as `RC-FD-06` §8.8.1 beside the classic Signature field. Data Dictionary definition is field type `file` + validation `enhanced_signature`; existing Signature fields convert with no data loss. **Two consent-relevant caveats the report did not have:** on 17.1.0 the signature image was **missing from downloaded PDFs and PDF Snapshots** (fixed 17.1.1) — captured but absent from the archived document — and up to 17.2.x a **blank** signature could be submitted (fixed 17.3.0), so an image's presence is not evidence anything was signed. Retargeted: `RC-DE-05` and `RC-FD-08` were not the right homes; the field type belongs with the other field types in `RC-FD-06`.
  *Original entry:*
  17.1.0 added a new, more accessible signature field supporting both scribbled and hand-typed signatures. **Zero** matches in `kb/`. Follow-ups: MLM support for the "Sign Here" and "Please type your signature before saving." strings (17.3.0), and Copy/Paste Fields support (17.3.0). Also check `RC-LOCK-01` for interaction with e-signatures.

- [x] **`RC-FD-06` — Copy/Paste Fields. GAP** — *done 2026-08-18*
  `RC-FD-06` §6.3.1, with the Field-Level Actions table noting the Ctrl/Cmd-click variant. Key point: a field can be pasted into **another REDCap instance**, provided it is also 17.2.0+. Four fidelity caveats added — section-headers-only pasting (fixed 17.3.0), min/max validation on integer and number fields (17.3.1) and **choice order on multiple-choice fields (17.4.0)** were not carried across, so on earlier 17.x versions verify a pasted field rather than assuming a faithful copy.
  *Original entry:*
  17.2.0: Ctrl/Cmd-click the Copy icon in the Online Designer copies field attributes to the clipboard as JSON, pasteable elsewhere. 17.2.1 corrected the on-screen key hint to "Cmd" on Mac. **Not covered.**

- [x] **`RC-AT-01`, `RC-AT-06` — `@SAVE-PROMPT-EXEMPT` and `@SAVE-PROMPT-EXEMPT-WHEN-AUTOSET`. GAP** — *done 2026-08-18*
  New `RC-AT-06` §5a placing both tags in the context that motivates them — autofill tags writing on page load make REDCap warn about changes the user never made — plus both entries in the `RC-AT-01` master table. Documented that neither suppresses the prompt for the *page*, only for the tagged field, and carried REDCap's own data-loss warning.
  *Original entry:*
  Both added in 15.2.0; **zero** matches in `kb/`. The `-WHEN-AUTOSET` variant specifically suppresses the "Save your changes?" prompt for values set by `@DEFAULT`, `@SETVALUE`, `@TODAY` or `@NOW` — squarely an autofill-article concern.

- [x] **`RC-MYCAP-02`, `RC-MYCAP-08` — `MC-FIELD-SLIDER-BASIC` / `MC-FIELD-SLIDER-CONTINUOUS` removed. WRONG** — *done 2026-08-18*
  15.7.2 Standard removed both as valid action tags; they worked only in the now-retired MyCap Classic app, never in the current one.
  **Correction to this report:** `RC-AT-11` was listed here in error. It covers the *REDCap Mobile App* (`@BARCODE-APP`, `@APPUSERNAME-APP`, `@SYNC-APP`), not MyCap, and never mentioned the slider tags. Only two articles were affected.
  Applied: removed both rows from the §4.1 annotation table and the tag recommendation from the field-type table in `RC-MYCAP-02`; swapped the stale example in the `RC-MYCAP-08` testing checklist; added a version caveat noting the tags are inert rather than merely undocumented. Because this shipped as a *Change* rather than a fix, LTS instances on the 15.5.x line still list the tags as valid — the caveat says so.

- [x] **`RC-CALC-01` — `random()` function missing. GAP** — *done 2026-08-18*
  Added to §6.2 Mathematical Operations. Included a warning the changelog does not make: `random()` re-evaluates whenever a calculated field's inputs change or the form is re-saved, so it is **unsuitable for treatment allocation** — pointed at the Randomization module instead.
  *Original entry:*
  17.0.3 added `random(min, max)`. `dayoftheweek()`, `age_at_date()` and `isblanknotmissingcode()` are already present — `random()` is the only one absent.

- [x] **`RC-FDL-01` — Form Display Logic gained two capability tiers. WRONG** — *done 2026-08-18*
  **Upgraded from GAP to WRONG on inspection.** The article stated flatly that FDL conditions "are evaluated at the record level — not within the context of a specific event or repeating instance". Since **15.3.2** that is no longer universally true: conditions can be scoped to a repeating-event instance using `[previous-instance]` and `[current-instance]`. Corrected in place with the general rule retained.
  Added §5.1 covering the 15.7.3 move from project-wide Survey Auto-Continue/MyCap toggles to per-condition control, including the upgrade behaviour that applies the old setting to **every** condition. Three version caveats: MyCap FDL breaking with multi-condition instruments (16.1.8), MyCap publish failures (17.1.1), and Survey Auto-Continue skipping surveys where the first fix made it worse before 16.0.4 resolved it.
  *Original entry:*
  15.3.2 FDL usable within a specific repeating event; 15.5.1 "Enable support for MyCap App" checkbox applying FDL conditions in MyCap; 15.7.3 **condition-level FDL settings** — granular control per condition across data entry forms, Survey Auto-Continue and MyCap, replacing the previous all-or-nothing model. 17.4.0 converted the form multi-selects to Select2. The 15.7.3 change likely makes existing prose incorrect, not merely incomplete. Also check `RC-IMP-08` (Form Display Logic CSV).

- [x] **`RC-DE-02` — Section Navigation box. GAP** — *done 2026-08-18*
  New §6a. Two caveats: opening REDCap Messenger could leave the box **overlapping the form** and obscuring fields (fixed 17.0.0), and some headers were unreachable on forms with many sections (17.2.1).
  *Original entry:*
  16.1.5 added an always-visible right-hand navigation box on data entry forms for jumping between sections. **Not covered**, and it is a visible change every data-entry user will notice.

### Surveys & alerts

- [x] **`RC-ALERT-01`, `RC-SURV-06` — "Re-evaluate Send Time" for Alerts & ASIs. GAP** — *done 2026-08-18*
  Documented in both articles, with `RC-SURV-06` distinguishing it from the similar-sounding "Ensure logic is still true" checkbox — one decides *whether* an invitation sends, the other *when*. Scope limits recorded: unsent items only, send time only (not sender/subject/content), and **reminders are not rescheduled once the initial invitation has gone out**. Also the default asymmetry — on for new Alerts/ASIs, legacy behaviour retained for pre-upgrade ones, with nothing on screen distinguishing them. Caveat states the feature was unreliable for its **entire life before 17.4.1 / 17.3.7** and should be treated as requiring those versions.
  *Original entry:*
  17.2.0 added the ability to re-evaluate scheduled send times for alerts and ASIs sent relative to a stored date/time. Note for readers: 17.3.7 LTS / 17.4.1 Standard fixed two significant bugs in it (the checkbox not persisting, and incorrect rescheduling on unrelated data changes) — **document the feature as requiring ≥17.4.1 / ≥17.3.7 to behave correctly.**

- [x] **`RC-ALERT-01` — Pause Recurring Alerts. GAP** — *done 2026-08-18*
  Added under Alert Schedule with a pause-versus-delete comparison and the `datediff()` use case REDCap cites. **Caveat worth the whole entry:** on ≤17.2.x Standard / ≤16.0.38 LTS, unpausing could fire **all the alerts that would have been sent during the pause, at one-minute intervals** — a burst of near-identical emails to a participant, precisely the outcome pausing exists to prevent. Fixed 17.3.0 / 16.0.39.
  *Original entry:*
  15.4.0 added "Allow pausing of recurrences?" for conditional alerts using "Ensure logic is still true…". **Not covered.**

- [x] **`RC-ALERT-01` — Universal DO-NOT-REPLY address. GAP** — *done 2026-08-18*
  Already present in `RC-CC-02`; added to `RC-ALERT-01`'s Administrator Configuration section, where someone investigating alert From addresses will look. Noted it sets **both From and Reply-To**, and the ≤15.7.4 caveat that it was **not** applied to the Save & Return Later participant email — replies to which went to an unmonitored mailbox. Fixed 15.7.5.
  *Original entry:*
  15.4.0 added a system-level do-not-reply From/Reply-To address for automated system email. `RC-CC-02` mentions it; `RC-ALERT-01` should note the interaction with alert From addresses.

- [x] **`RC-SURV-03` — survey "Save & Return Later" security correction. WRONG (behaviour)** — *done 2026-08-18*
  Added an explicit statement of return-code scope — valid only for the participant-specific link it was issued against — followed by a **Critical** caveat that this did not hold on any version below 17.4.1 / 17.3.7: a participant holding another's individual survey link could open their saved responses using their *own* code. Framed as an upgrade priority for anyone running partially-completed surveys with sensitive data. Two smaller caveats added: the ≤17.0.2 public-link return code error, and the 15.4.5 transparency change telling participants their email address is retained in the system email logs — worth matching against consent materials.
  *Original entry:*
  17.4.1 / 17.3.7 fixed a flaw where a Return Code worked against another participant's survey link. If any KB text describes Return Code scope loosely, tighten it: a Return Code is valid **only** for its own participant-specific link.

---

## P2 — Gaps worth filling

### CDIS — the largest cluster (~45 entries)

`RC-CDIS-01` through `RC-CDIS-04` are the most out-of-date articles in the KB relative to the changelog. Notably, **"Break the Glass" / "Break-the-Glass" appears nowhere in `kb/`**, and neither does **"Mapping Helper"** or **"gender identity"**, despite BTG being a recurring theme across 15.0.0–17.2.x.

- [x] `RC-CDIS-01` — **Break the Glass (BTG)** — *done 2026-08-18.* New §6a: the workflow end to end, the 15.8.1 change to request tokens on user action rather than detection (earlier tokens expired before use), resource/endpoint-level detection (16.0.4), TTL 5→10 days (16.0.6), temp-data tables (16.1.1), and confirmation by email/SMS/Duo/OTP rather than password only (16.1.2) — which matters for SSO users with no REDCap password. Caveat: a BTG-protected patient could crash background CDP for the whole instance below 17.4.1 Standard. *Original entry:*, Epic-only, has no coverage at all. Improvements: logging detail for success and failure paths (15.0.0); improved workflow when not using the Patient/demographics mapping (15.4.0); deferred token requests (15.8.1); clearer FHIR token feedback (15.8.4); resource/endpoint-level protection beyond patient-level (16.0.4); cached protected-patient-list TTL raised 5→10 days (16.0.6); cache files moved to the REDCap temp folder (16.0.8); state moved to temp-data tables for deployment safety (16.1.1); confirmation step now accepts email code, SMS code, Duo push and OTP in addition to password (16.1.2).
- [x] `RC-CDIS-01` — CDIS Access Token Priority Rules Manager — *done 2026-08-18.* New §6.1, explaining why it exists: where several project users hold FHIR tokens, tokens differ in reach, so the same fetch returns different results depending on whose token was chosen. *Original entry:* (15.1.0), letting project owners prioritise FHIR access tokens. **Not covered.**
- [x] `RC-CDIS-02` — EHR demographic expansion — *done 2026-08-18.* Filed in `RC-CDIS-02` beside the existing Demography Field Coding section rather than `RC-CDIS-01`/`RC-CDIS-03`. Added FHIR ID and pronouns (15.3.3), multi-race (15.9.0) and gender identity separate from legal sex, sex assigned at birth and sex for clinical use (17.1.3) — with a note that projects predating these versions may hold **less complete historical data** than the current mapping implies. *Original entry:*: FHIR ID as patient identifier, pronouns and other personal preferences (15.3.3); multi-race mapping via a "Race (all coded values)" field without breaking single-value setups (15.9.0); **gender identity mapped separately from legal sex, sex assigned at birth, and sex for clinical use** (17.1.3).
- [x] `RC-CDIS-02` — CDP adjudication was rebuilt — *done 2026-08-18.* New §6.1 display options and §6.2 change history. Two caveats about **silently misplaced data**: adjudicated values saved to the wrong event instance below 16.1.8 Standard / 16.0.19 LTS, and to the wrong event entirely below 15.7.1 Standard. *Original entry:* across many releases: cleaner layout (15.6.0); validation display improvements (15.7.4); empty-EHR-response guidance (15.7.4, 15.9.0); transformer-adjusted item counts and always-available Save (15.7.5); pre-fetch validation of record identifier and temporal reference field (17.2.1); display options to show matching REDCap values first and narrow to instrument/event/instance (17.2.1).
- [x] `RC-CDIS-02` — Mapping Helper additions — *done 2026-08-18.* New §6.3. The 17.1.3 additions let you validate a mapping from a pasted FHIR payload instead of pulling real patient data. *Original entry:*: review pasted/uploaded FHIR payloads without a live fetch, and search for patient identifiers by entering demographics (both 17.1.3). CDP Mapping Setup now reachable directly from the project's Clinical Data Interoperability Services menu (17.2.0). Mapping page refactored to a form-based workflow with event-aware copy tools (16.0.8), sticky header and select-all when copying to multiple events (16.0.9), validation messages under the related column (16.0.9).
- [x] `RC-CDIS-01` — infrastructure — *done 2026-08-18.* New §6.2 table. Highlighted the 16.0.8 dedicated CDIS temp folder as worth setting on multi-server deployments, since per-server temp directories mean a background job on one app server may not find state written by another. Caveats for the two background-fetch defects that left work **silently incomplete**. *Original entry:* weekly cron to prune expired FHIR tokens (16.0.0); dedicated CDIS temp-file folder (16.0.8); fetch reconciler for stuck "fetching" records (16.0.8); Twig replaces Blade in the EHR authorisation workflow (15.5.0); per-MRN/per-resource subprocesses for Data Mart fetches (15.9.0); Data Mart processing now follows record sort order rather than MRN order (16.1.2); grouped diagnostics and sanitized token-endpoint detail on the FHIR launcher error page (17.2.0); SMART on FHIR EHR launch context retention through Shibboleth and external login handoffs (17.1.2).

### MyCap (~40 entries)

`RC-MYCAP-01` … `RC-MYCAP-08`. Beyond the removed slider action tags already listed as WRONG in P1:

- [x] `RC-MYCAP-05` — **MyCap Email Notifications** and participant management — *done 2026-08-18.* Email notifications on incoming participant messages (15.7.0), DAG-aware. Three new Participant List columns — Last accessed (16.0.6), App Version (17.0.1), Device Info (17.2.2) — framed as the diagnostic set for "it isn't working on my phone" reports. The **Delete/Undelete → Disable/Enable** rename (15.3.3) recorded with why it matters: nothing is deleted, and from the same release a config-JSON flag stops a disabled participant rejoining with an old QR code. Messaging additions: rich text (15.0.3), thread search (15.8.4), announcement search (16.0.6), scheduling (16.0.9), CSV download of all messages incl. auto-generated ones (16.1.4) — the practical audit trail. Also DAG-specific Contacts/Links/About (15.4.2), About rich text (16.0.8), Purple default (15.8.4). *Original entry:* (15.7.0): a Messages tab for composing email notifications sent when a participant message arrives, with DAG awareness. Participant List columns added: Last accessed (16.0.6), App Version (17.0.1), Device Info (17.2.2). "Delete/Undelete" renamed **"Disable/Enable"** with participant notification (15.3.3) — a rename worth checking for stale text. Message search (15.8.4), announcement search (16.0.6), scheduled announcements (16.0.9), message CSV download (16.1.4). Purple is now the default theme (15.8.4).
- [x] `RC-MYCAP-02` — instrument design changes — *done 2026-08-18.* **Corrected a wrong row:** the field-type table said Signature was **not** supported; it has been since 15.4.1. Added §4.5 for the remaining design behaviours (validation drop-down locked on MyCap fields 15.4.5, `[survey-link]` in task labels 15.8.4, rich text for Intro/Capture instructions 16.1.5, chart-field Required warning and the 30-day no-tasks notice 15.7.5), the 15.4.5 requirement on `@latitude`/`@longitude`, the 15.5.6 baseline-date guardrail, and the 17.3.1 day limit on retroactive completion — previously open-ended. *Original entry:* now receive data from the app (15.4.1); `@latitude`/`@longitude` supported inside tasks (15.4.5) — verify `RC-AT-11` reflects the MyCap context; `[survey-link]` usable in MyCap task field labels (15.8.4); rich text editor for task instructions and completion steps (16.0.8) and Intro/Capture page instructions (16.1.5); retroactive-completion day limit (17.3.1); warning when a chart field is not Required (15.7.5).
- [x] `RC-MYCAP-07` — MLM and language support — *done 2026-08-18.* Three languages added in 17.0.4 (Zulu `zu-ZA`, Afrikaans `af-ZA`, Czech `cs-CZ`), and the 15.6.0 setting preventing participants switching language in-app — documented with the reason: mixed-language MTB measures may not be directly comparable. *Original entry:* option (15.6.0); three new app languages Zulu `zu-ZA`, Afrikaans `af-ZA`, Czech `cs-CZ` (17.0.4); DAG-specific Contacts/Links/About pages (15.4.2).
- [x] `RC-MYCAP-01` — security posture and configuration JSON — *done 2026-08-18.* New §5.1 collecting the app-to-server security fixes, which matters because the article's security architecture claims are used for IRB language: **participant impersonation via a shared signing key was fixed twice**, 16.1.8 and again 17.2.0, so instances between those releases were still exposed. Plus QR-code study-code enumeration and SQL injection (17.2.3) and MyCap XSS (17.0.1, 17.0.3). New §5.2 on the config JSON — the disabled-participant flag (15.3.3) and the server max upload limit (16.1.2) that blocks oversized uploads on the device rather than failing at the server. Caveat for 17.2.0 breaking app communication for already-joined participants (fixed 17.2.1). *Original entry:* now in the config JSON (16.1.2); baseline-date field guardrails (15.5.6); notice after 30 days with MyCap enabled but no tasks (15.7.5); Participant List performance (15.5.5).

### Multi-Language Management

- [x] `RC-MLM-01`, `RC-CC-20` — MLM changes — *done 2026-08-18.*
  **Stale navigation corrected:** the Snapshot facility moved from the **Settings** tab to the **Languages** tab in 15.4.5; the article did not say which tab it was on, so the relocation is now stated explicitly.
  New content: §5.1a on what cannot be translated per field (true/false and yes/no choice labels are fixed; embedded fields must survive translation — both now hinted in the UI, 15.0.1 and 15.2.4); §5.10 piping interaction (calc/CALCTEXT source swapping 17.0.0, `:field-label` 17.0.4, Enhanced Signature strings 17.3.0); §5.11 on the `lang` HTML attribute, which from 17.1.0 is re-evaluated **on language switch** rather than only at page load — before that a screen reader kept the previous language's pronunciation rules for the rest of the session; §7.1a on the LLM round-trip workflow (17.1.3), which is the better route than the in-page AI button for anything large since the model sees surrounding context; the "Discourage browser-based translation" setting (17.1.0) with REDCap's own caveat that tools **may or may not honour** the markers; `__lang` extended to the Survey Queue (15.0.1); cookie policy translatable (15.8.1); MLM manuals shipping with REDCap (15.5.1).
  **Caveats added for silent failures:** UI overrides for subscribed system languages simply did not save below 16.1.6; base-language UI overrides stopped displaying between 15.6.0 and 15.7.1; AI auto-translate failed **with no error message at all** below 17.4.0, and could fail outright on any text containing a comma below 17.3.1; piped fields present only in MLM translations could render blank between 15.8.4 and 17.3.2.
  *Original entry:*, under the User Interface tab (15.8.1); `__lang` URL parameter to preset Survey Queue language (15.0.1); true/false and yes/no choice labels are fixed and cannot be translated per-field (15.0.1); embedded-field preservation notice (15.2.4); Snapshot facility moved from the Settings tab to the **Languages tab** (15.4.5 — stale-navigation risk); "Language preference field" wording changed (15.5.1); AI translation prompt now includes the target language ID (15.5.1); on-the-fly swapping of calc/CALCTEXT piping sources (17.0.0); `:field-label` piping support (17.0.4); **"Discourage browser-based translation of survey pages"** setting (17.1.0); `lang` attribute now re-evaluated on language switch, not only page load (16.0.6, 17.1.0); JSON export now carries **LLM-friendly instructions** for export → translate → re-import workflows (17.1.3).

### Reports, exports & dashboards

- [x] `RC-EXPRT-06` — Quick Set field entry — *done 2026-08-18.* Documented Quick Set (15.5.0), the copy-field-names links (15.5.0 and 15.5.1), and the practical use: replicating a report in another project becomes copy-and-paste rather than a manual rebuild. **Caveat:** below 15.5.5 Quick Set **silently dropped checkbox field names** in `checkbox_field___code` notation and gave no feedback during long operations, so it looked like a hang and lost data. *Original entry:*: paste or type field names to add/replace report fields (15.5.0), plus a link to copy all current report field names (15.5.1).
- [x] `RC-EXPRT-06`, `RC-EXPRT-08` — access code protection for public reports — *done 2026-08-18.* **`RC-PROJ-03` and `RC-PIPE-14` already covered the dashboard side** including `[dashboard-access-code]`; only the report side was missing. Added to `RC-EXPRT-06` §4.2 with a pointer from `RC-EXPRT-08`, where the unique report name lives. Stated plainly that an access code **gates a URL but is not access control** — no authentication, no record of who viewed, no per-recipient revocation. Also the 16.1.7 asymmetry: `[report-access-code]` is always shown in the smart variable docs because admins can still make reports public when the system setting is off, whereas `[dashboard-access-code]` is correctly hidden. *Original entry:* (16.0.5). `[report-access-code]` is already in `RC-PIPE-15` ✓; confirm the dashboard equivalent is in `RC-PIPE-14`.
- [x] `RC-EXPRT-05` — citation prompts in the export dialog — *done 2026-08-18.* New §5.1. Both citations appear at the point of export rather than in project setup, on the reasoning that whoever pulls the data for analysis is the one who needs them. *Original entry:* when randomization is set up (15.5.0) and the External Module Framework publication when EMs are enabled (15.5.0).
- [x] `RC-NAV-REC-04` — Custom Record Status Dashboard — *done 2026-08-18.* Smart variables in the description (15.7.2), letting a dashboard open with a live summary rather than static prose, plus row hover and keyboard focus highlighting (16.1.1). **Caveat worth the entry:** below 15.6.1, filter logic testing a form status field against blank — `[form1_complete] = ""` — could return an incorrect record set on both dashboards and reports. Silent failure: a plausible-looking but wrong list. *Original entry:* now work in Custom Record Status Dashboard descriptions (15.7.2); row hover/keyboard-focus highlighting (16.1.1).

### Records, data entry & navigation

- [x] `RC-DE-13` — "Choose action for record" — *done 2026-08-18.* **Corrected a wrong claim in the article:** the Logging, Notification Log, Email Logging and Survey Invitation Log entries were labelled *admin only*. They are **privilege-gated**, appearing for any user holding the corresponding page privilege (15.0.3, with Email Logging extended to non-admins in 15.7.2). Only the Database Query Tool is genuinely admin-restricted. Also added the Survey Queue row: shown whenever surveys are enabled even if the queue is empty (15.0.6), with a copy-link sub-option, and no longer shown at all where surveys are disabled. *Original entry:* to Logging, Notification Log and Survey Invitation Log (15.0.3), Survey Queue always shown even when empty (15.0.6), and Email Logging when the user has access (15.7.2).
- [x] `RC-NAV-REC-03` — repeating-instrument tables — *done 2026-08-18.* New §3a covering the 15.3.2 rewrite and everything since: custom paging (15.4.3), persistent status filters (15.5.5) and sort order (15.7.2), Previous/Next between repeating event instances (17.0.7). Noted the 15.4.1 reversal of clickable custom labels. **Caveat worth the entry:** below 17.3.4 an instance could be **omitted from the table entirely** if it had been Unverified and then partially completed — a missing row does not mean missing data. *Original entry:* (15.3.2, refined 15.3.3, custom label link reverted 15.4.1); custom paging size (15.4.3); status filters persist per table (15.5.5); sort order persists per user per project (15.7.2); **Previous/Next links between repeating event instances** (17.0.7).
- [x] `RC-DE-01` — Add/Edit Records behaviour — *done 2026-08-18.* New §2a: searchable record and field drop-downs (17.0.7), user preferences for search target and Record Home Page navigation (16.1.4), the arm-selection preference appearing only on multi-arm projects, and the pipe-character Data Search failure below 17.4.1. *Original entry:* (17.0.7); user preferences to remember the last search target and force searches to the Record Home Page (16.1.4); "Save & Go To Next Record" behaviour at the end of the record list with auto-numbering (15.7.0).
- [x] `RC-PROJ-01`/`RC-DE-13` — Bulk Record Delete: background deletion option (15.6.0), instructional text corrected (15.8.4), **delete "all records from a report"** (17.4.0), and the 17.2.0 UI rule that unselecting an instrument unselects its event. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-DQ-01` — Data Quality rule scoping — *done 2026-08-18.* New §3.1: field selection for rules A–I (16.0.0), multi-record and multi-DAG filters (16.0.7), bulk rule deletion (15.9.0). Three caveats: DQ CSV export ignored Full Access export rights below 17.4.0; rule E misbehaved with no numeric fields below 15.8.2; and **`age_at_date()` in rule H returned blank for any date falling on 29 February** below 16.1.8 — so a clean rule H pass on an affected version is not trustworthy for age calculations. *Original entry:* (16.0.0); multi-record and multi-DAG filters (16.0.7); bulk delete of DQ rules (15.9.0); rule E behaviour when no numeric fields exist or are accessible (15.8.2).
- [x] `RC-DE-12` — Data Resolution Workflow settings — *done 2026-08-18.* Documented the 15.9.0 setting preventing rule H from overwriting calc fields whose queries are closed or verified, explaining why it matters: an automated correction silently undoes a deliberate human decision. Added the below-17.0.2 caveat where closed/verified queries were excluded from DQ results even with the hide setting unchecked. *Original entry:* fields with closed/verified data queries from being fixed by DQ rule H" (15.9.0); DAG-aware assignment of queries (15.0.1).
- [x] `RC-FD-05` — Codebook — *done 2026-08-18.* Internal links from the Instruments table (15.0.3), per-instrument download icons (16.1.4), and event IDs in the Events table (15.4.1) — the last being useful when you need the numeric ID for an API call rather than the display name. *Original entry:* from the Instruments table to the fields table (15.0.3), event IDs in the Events table (15.4.1), per-instrument download icons (16.1.4).
- [x] `RC-LOG-01` — Logging page — *done 2026-08-18.* New §3.1: last-activity timestamp (16.1.8), Email Logging Type column (17.2.0) and searchable record drop-down (15.7.2), plus `SYSTEM` always offered in the user filter (15.9.3). Highlighted the 17.0.0 change adding **instrument, event and instance context to logged PDF downloads** — previously the log recorded that an export happened but not what it contained, which matters when the log is used as evidence. Caveat for Page Views filtering returning entries out of chronological order below 17.0.2. *Original entry:* (15.9.3); last-activity timestamp at top right (16.1.8); Email Logging searchable record drop-down (15.7.2) and a Type column in results (17.2.0); PDF downloads now log instrument/event/instance context and compact-format flag (17.0.0).

### API

- [x] `RC-API-01` — token masking, versioned URLs and rights enforcement — *done 2026-08-18.* Token masking (17.0.7) added to §3.3. New **§3.3a** on calling the API at `/api/index.php` and never at a versioned path: from 16.1.5 REDCap **rejects** versioned URLs, so an integration still using one breaks on upgrade and the failure looks like an API fault rather than a URL problem. New **§9a** collecting the rights-enforcement fixes, grouped because each one silently returned data the caller should not have received — File Export ignoring No Access rights, three survey code/link methods ignoring DAG membership, ACG compliance bypassable via API user-rights import, and admin-restricted folders appearing in File Repository listings. `REDCap::getSurveyAccessCode()` documented beside the Export Survey Access Code method, with the changelog's `getSurveyAccesCode` typo flagged so nobody copies it into code.
  *Original entry: the project API page now masks the token by default with a click-to-reveal control, and API/API Playground behaviour was improved (17.0.7).*
- [x] `RC-API-13` — Import File accepts `repeat_instance=new` — *done 2026-08-18.* Noted that it removes a race condition as much as a convenience: previously you had to query the highest instance number and add one, which two concurrent processes could collide on. *Original entry:* to target a not-yet-created repeating instance (17.4.0).
- [x] `RC-API-22` — Export Users returns `data_access_group_label` — *already covered, no change needed.* The field and its explanatory note were already present in the article. *Original entry:*
- [x] `RC-API-46` — File Repository listing — *done 2026-08-18.* `role` and `dag` were **already documented**. Added the part that was missing: **admin-restricted folders are excluded** from the response (wrongly included up to 16.0.7), so the listing must not be treated as a complete inventory of the File Repository. *Original entry:*
- [x] `RC-API-34`/`RC-API-35` — P.I. email address — *already covered, no change needed.* `project_pi_email` was already documented in the response field table. *Original entry:*
- [x] `RC-API-01` — developer method `REDCap::getSurveyAccessCode()` — *done 2026-08-18.* Documented beside the Export Survey Access Code method, with the changelog typo flagged so nobody copies it into code. *Original entry retained above.*

### External Modules

- [x] `RC-EM-01` — External Module Framework — *done 2026-08-18.* Added a **Framework Version** definition (v17 from 17.0.1; modules declaring none fall back to v1) and new §2a covering Twig 3 bundling, the new API endpoints, EM links in Analysis/Cleanup, edoc hashing, autocomplete config drop-downs, and the two new dashboard hooks. **Two compatibility boundaries called out for module authors:** Twig below 3.9.0 may break across 15.5.0, and strict variables in 17.0.1 turn previously-tolerated undefined variables into errors. **Caveat worth the entry:** `REDCap::getUserRights()` returned an **empty array** between 16.0.0 and 16.0.3 where the caller lacked User Rights privileges — any module or hook using it for an access decision saw no rights rather than the real ones. *Original entry:* with strict Twig variables (17.0.1); new EM API endpoints (15.5.2); Twig 3 bundled in REDCap core beyond the EM Framework (15.5.0); edoc-id hashing on EM file uploads and in-module documentation linking (17.3.1); better failed-download error messaging (16.1.6); autocomplete drop-downs in EM config (16.1.8); **two new hooks — `redcap_module_dashboard_before_render` and `redcap_module_dashboard_after_render`** (17.4.0). Also 15.6.0: EM links now display in the left-hand menu while a project is in Analysis/Cleanup status, where previously they did not.
- [x] `RC-EM-01`, `RC-CC-25` — features absorbed from community modules — *done 2026-08-18.* Generalised beyond ACGs into `RC-EM-01` §7a, since the same pattern applies four times: Access Control Groups from Andrew Poppe's *Security Access Groups* (16.0.0), editable field validation types from Adam Nunez's *Add Validation Types* (17.4.0), Automatic Version Redirect from Andy Martin's *REDCap Redirect* (17.2.2), and the record logging links from Luke Stevens' *Record Logging Links* (15.0.3). **The hazard is stated as Critical:** upgrading absorbs the feature but does **not** disable the module or migrate its settings, so an instance ends up running both side by side with independent configuration. For ACGs that means two systems enforcing overlapping ceilings on user rights, neither aware of the other — flagged in `RC-CC-25` as a pre-upgrade check. *Original entry:* of Andrew Poppe's "Security Access Groups" EM, that upgrading does **not** disable the EM, and that settings are **not** migrated (16.0.0). Same pattern for `RC-CC-24`/`RC-DE-05` and Adam Nunez's "Add Validation Types" EM (17.4.0).

### Miscellaneous

- [x] `RC-FILE-01` — **admin-restricted folders** in the File Repository, visible only to admins with all-project access (15.5.0). Project-level override for max upload size on Edit Project Settings (16.1.0). Neither covered. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-CC-03` — OIDC scopes manually specifiable (15.4.2); more specific OIDC error output (15.7.0); custom button text for the "Local REDCap Login" button under OIDC & Table-based / Entra ID & Table-based (16.1.2); Duo library updated (15.9.2); Caps Lock warning on table-based login (15.7.2); **6-digit PIN required only once per session for e-signing under 2FA** (15.4.0) and the Duo-push equivalent (16.1.2); e-signature dialog text under "X & Table-based" 2FA (15.2.6). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-TXT-01`/`RC-TXT-02` — Twilio Alphanumeric Sender ID is in `RC-TXT-01` ✓ but confirm the outgoing-SMS-only limitation is stated; admin approval workflow for enabling Mosio/Twilio per project (15.6.0). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-FD-06` — new Online Designer methods for editing instrument label and unique instrument name (15.1.0); survey status icons for e-Consent and Stop Actions (15.1.0); field-count shown when bulk-updating branching logic (15.2.2); warning for instruments not designated to any event in longitudinal projects (15.2.6); rich text editor for Matrix Header Text (17.0.6); opt-out of the 26-character variable-name warning, per user per project (17.1.0); extra Draft Mode warning when temporary metadata changes already exist (17.3.0); "Go to field" via Ctrl-G/Cmd-G from the instrument overview (17.4.1); Standardized Field (CDE) search — **formerly "Field Bank"** — gained categories (16.0.7), so check `RC-FD-06` and `RC-CC-02` for the old name. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-LONG-01` — direct link to "Define My Events" in the left-hand menu (15.3.3, repositioned 15.4.0); repeating instrument/event icons across Define My Events, Designate Forms and Online Designer (15.4.5); **"Designate Instruments for My Events" now directly accessible from the left-hand menu** with a Print Page button (17.4.1); accented characters in DAG and event names are transliterated in the unique names for **new** projects (17.3.0). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-PROJ-01` — record limit for development projects is in `RC-CC-02`/`RC-PROJ-01` ✓; add the 15.5.5 admin bypass when copying a project. Project deletion purge-delay setting (15.2.6). Project Home stats now show instrument counts, event/arm counts (16.0.7) and created/production/analysis timestamps (16.0.9). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-PROJ-04` — Secondary Unique Field best-practice warning (15.8.0); clarified text on deleting a record's logging activity (15.7.2); extra confirmation on "Erase all data" in production (15.7.2). **Security-relevant:** 17.0.2 blocked administrators from injecting JavaScript into branching logic or calc/CALCTEXT equations — if any KB article suggests JS in logic as a technique, it must be corrected. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-FD-03`/`RC-FD-08` — Data Dictionary page UI simplified (15.0.1); multiple-choice fields with no choices now warn rather than error on upload (15.9.2); syntactically invalid branching logic, calculations and CALCTEXT are **automatically commented out** when creating a project from Project XML (17.0.3). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-FD-07`/`RC-FD-09` — pre-embedded text in a multiple-choice **choice label** is no longer displayed (15.7.3). Behaviour change affecting existing designs. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-DE-02`/`RC-CALC-02` — branching-logic and calculation errors are now combined into a single dialog listing all affected fields (15.7.0). Supported HTML tags in user input expanded: `blockquote` (15.0.1), `wbr` (15.4.5), `ruby` (15.5.6) — `RC-FD-08` likely carries the allowed-tag list. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-LOCK-01` — locking/e-signature settings from the Record Locking Customization page are now exportable and importable via Project XML (16.0.7). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-MSG-01` — "Mark all conversations as read" (15.7.4). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-CAL-01` — calendar table widened (16.0.7). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-MOB-01` — Mobile App dashboard now shows username, install time and latest-activity timestamps (16.1.8). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-CC-17` — Database Query Tool CSV exports include the custom query title in the filename (15.2.1). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-CC-05` — Azure Blob Storage supports Azure Government Cloud, US only (15.2.1); Restricted Upload File Types enforcement strengthened (15.8.0); the setting moved from Security & Authentication to File Upload Settings (16.0.1) — **check `RC-CC-03` for a stale pointer**. — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-CC-08` — custom text at the top of the Create New Project page (15.0.0); "Custom footer text for survey pages" settable on Default Project Settings (15.9.0). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-CC-04` — new settings governing how users are added to projects, at the bottom of the User Settings page (16.1.5). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-PROJ-01` — non-admin users with Project Design rights can now clear the Record List Cache and Rapid Retrieval cache from Other Functionality (16.1.8). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-SURV-05` — Rapid Retrieval caching on the Participant List, its CSV export and the API export method (15.0.0); hardcoded links no longer persisting from previously sent invitations in Compose Survey Invitations (15.2.5). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-SURV-01`/`RC-SURV-02` — Descriptive Popup inline text limit raised to 255 characters with a maxlength safeguard (17.4.0); descriptive-field inline images no longer add leading space when the label is empty (15.6.0). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-DE-06` — BioPortal auto-selected when it is the only ontology service available (15.6.1). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-DDE-01` — form status icons on the Record Status Dashboard and Record Home Page now route correctly for DDE person 1/2 (15.8.2). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-USER-04` — "Manage All Project Tokens" indicates suspended users (15.8.2); API Tokens page has searchable drop-downs (17.1.0); duplicate-username detection when adding table-based users (17.0.6); User Allowlist "Delete all" uses a modern dialog (16.1.1); Sponsor Dashboard approval shows only affected users (16.1.1); "Password was last reset on X" reworded to "…by an admin on X" (16.1.1). — *done 2026-08-18 (miscellaneous sweep).*
- [x] `RC-FD-04` — PROMIS battery event designation when the first instrument is already designated (15.3.1). — *done 2026-08-18 (miscellaneous sweep).*

---


> **Sweep note (2026-08-18).** The final 26 P2 items were applied in a single pass across 26 articles, since each was a one- or two-line addition. **Two report corrections found during verification:** the User Allowlist dialog and Sponsor Dashboard approval changes are **15.6.1**, not 16.1.1 as recorded here. Several items also gained caveats the report did not anticipate — notably that partial Bulk Record Delete **ignored record-level locks** below 17.1.4, and that the project-level File Repository upload limit was **not enforced via the API** between 16.1.0 and 16.1.3.

---

## P3 — Minor / cosmetic — *re-triaged 2026-08-18*

The original P3 classification was made in a fast first pass. It was re-checked against the changelog after the P1 and P2 work, on the reasoning that a quick triage of ~90 entries is exactly where errors hide.

**Method.** An automated coverage check (does any distinctive term from the entry now appear in `kb/`?) proved unreliable — it reported 78 entries as uncovered, but a 20-item spot check found **19 were false positives**, flagged only because the article wording differs from the changelog wording. The check was discarded and the candidate set was re-read by hand instead.

**Result: three entries were misclassified and have now been applied.**

- [x] **`RC-FD-11` — Custom CSS: the article documented only half the feature. WRONG** — *done 2026-08-18*
  15.5.0 introduced **two separate** Custom CSS controls: form-level on the Online Designer page, and **survey-level on the Survey Settings page**. The article described only the form-level control and stated CSS is "instrument-scoped", which reads as though one setting covers both contexts. It does not — an instrument used as both a form and a survey needs both. Two behavioural differences added: **form-level CSS is subject to Draft Mode in production while survey-level is not** (so in a production project one goes through review and the other is live immediately), and survey CSS can be copied via "Copy design to other surveys". Also carried REDCap's own warning verbatim: internal selectors "may break without notice… will not be announced in advance" — which given roughly weekly releases makes custom CSS something to re-check after upgrades, since it fails visually rather than with an error.

- [x] **`RC-CC-17` — the Database Table Reference named singular tables that do not exist. WRONG** — *done 2026-08-18*
  The reference listed `redcap_data` and `redcap_log_event`. REDCap distributes projects across **numbered** tables — `redcap_data8`, `redcap_log_event10` — as `RC-CC-24` already documents. A query written against the singular name returns nothing or the wrong project's rows. Corrected, with a pointer to Edit Project Settings where a given project's tables are named, and a note that **16.0.0 added two further data tables and three further log_event tables**, so an enumerated list will silently go stale.

- [x] **`RC-INFRA-01` — fatal-error reports include a work snapshot (17.3.1)** — *done 2026-08-18*
  Flagged in the original triage as "worth a line if the article is open". Applied, with a note that a privacy-safe snapshot is still diagnostic output from a system holding participant data.

Already applied during the P2 work: **MLM admin and end-user PDF manuals ship with REDCap** (15.5.1) → `RC-MLM-01`.

**The remaining ~85 entries stay undocumented, deliberately.** They are styling, wording, performance and internal-plumbing changes: button styling on the randomization setup page (15.0.1), Font Awesome 6.7.2 → 7.0.0 (15.5.5), My Projects page widened (15.9.2), `redcap_new_record_cache` pruning (15.7.0), session-storage column widening (15.5.0), cron-job management (16.1.2), MyCap QR code sizing (15.4.2), ESC-key dialog handling (15.4.1), and assorted logic-evaluation and CDP dashboard optimisations.

Documenting them would add length without making any reader more capable, and would dilute retrieval — the same reasoning that keeps images out of the KB. The bar applied is the one recorded in the kb-creation skill: an entry earns a place only if it **changes what a reader should believe**, **defines a version window where documented behaviour did not hold**, or **silently affected data, rights or delivery**. These do none of those things.

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

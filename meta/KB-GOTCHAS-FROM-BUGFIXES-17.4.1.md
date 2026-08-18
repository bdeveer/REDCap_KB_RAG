# KB Gotchas from Bug & Security Fixes — REDCap 15.0.0 → 17.4.1

**Generated:** 2026-08-18
**Companion to:** `KB-UPDATE-TODO-17.4.1.md` (features, improvements and changes)
**Source:** `ChangeLog_Standard_2026-08-18.csv` + `ChangeLog_LTS_2026-08-18.csv`

---

## Scope & method

- **Version floor:** 15.0.0. **Change type:** `Bug` only — the category excluded from the feature report.
- Merged and de-duplicated across Standard and LTS: **1,240 unique bug entries** (1,076 routine fixes, 97 major, 67 security).
- 86 entries carry explicit provenance ("Bug emerged in REDCap X" / "Bug exists in REDCap X and higher"), which is what makes affected-version windows possible below.

**This report is deliberately not a bug list.** A fixed bug only earns a place here if it tells a KB reader something durable: a behaviour that was wrong for a known window of versions, a limit that turned out not to hold, or an assumption the documentation currently makes that history has shown to be unsafe.

**Note on the KB's current state:** the string "known issue" appears in **zero** articles. There is no established convention for version-scoped caveats anywhere in `kb/`. Decide on one before working through this list — a consistent `> **Version caveat:**` blockquote, or a standard `## Known issues & version caveats` section, would be worth agreeing first.

---

> **Reconciliation, 2026-08-18.** This report's checkboxes were stale: items had been applied piecemeal while working the feature report, without being ticked here. Reconciling them exposed a bigger problem — **the report had never been worked as a list**, so several items were not applied at all, including the `age_at_date()` window that this report's own suggested order put second.
>
> Three attempts at automated coverage detection all failed with high false-positive rates, because article wording legitimately differs from changelog wording. Each item was therefore checked against the article text by hand. **Do not trust keyword matching to answer "is this documented?" for this KB.**
>
> Final state: **50 of 52 applied.** The two outstanding items belong to REDCap+ features that have no article yet and are carried on the P0 list in the feature report.

---

## Summary

| Cluster | Items | Highest-value target |
|---|---|---|
| A. Date/special-function calculations | 11 | `RC-CALC-01` |
| B. Data import silently dropping data | 10 | `RC-IMP-04`, `RC-IMP-01` |
| C. DAG isolation leaks | 5 | `RC-DAG-01`, `RC-API-*` |
| D. Export-rights bypasses | 3 | `RC-EXPRT-03` |
| E. Upgrade & install traps | 8 | `RC-INFRA-01` |
| F. Randomization integrity | 4 | `RC-RAND-03` |
| G. Survey form-status corruption | 4 | `RC-SURV-03` |
| H. e-Consent | 3 | `RC-SURV-08` |
| I. Alerts & ASI non-delivery | 2 | `RC-ALERT-01` |
| J. Record locking not enforced | 1 | `RC-LOCK-01` |
| K. Feature-launch instability | 5 | various |
| L. Security posture | ~67 | new/`RC-INST-01` |

---

## A. Date and special-function calculations — the biggest gotcha cluster

**Target: `RC-CALC-01`, `RC-CALC-02`, `RC-AT-09`**

`RC-CALC-01` §5.2 currently documents `age_at_date([dob], [other_date], returnDecimal)` with the third parameter described as optional. That is correct for current versions but was **actively unsafe across a five-release window**.

- [x] **`age_at_date()` and friends were broken from 17.0.6 to 17.2.0. WRONG-BY-OMISSION**
  *Applied 2026-08-18 → `RC-CALC-01` §5.2.*
  A chain of four separate fixes:
  - **17.0.6** — `age_at_date()`, `year()`, `month()`, `day()` "mistakenly fail to work in many cases" (fixed 17.0.7, provenance explicitly names 17.0.6 Standard).
  - **17.0.8** — same functions fail when referencing a field on another instrument where that instrument is repeating.
  - **17.1.2** — `age_at_date()` fails on a calc field on a form or survey **if the third parameter is not explicitly provided**. This directly contradicts the "optional third parameter" guidance in `RC-CALC-01` for anyone on 17.0.6–17.1.1.
  - **17.1.3** — date functions fail on a calc field when the referenced field is from another event **and is not in YMD date format**.
  - **17.2.0** — further date-function failures on calc fields not covered by the above.

  **Suggested caveat:** date-related special functions were unreliable on calc fields between 17.0.6 and 17.1.4; `age_at_date()` specifically requires REDCap ≥ 17.2.0 for full correctness, and on 17.0.6–17.1.1 the third parameter should be passed explicitly as a workaround.

- [x] **Comparisons against blank values returned wrong results. WRONG**
  *Applied 2026-08-18 → `RC-CALC-01` §5.5.*
  - **15.0.28** — calculations comparing a field to a number or another field with `<` or `<=` where the referenced value is blank/null, e.g. `if([v1] < 5, [v1], 0)`, might not return the correct result.
  - **16.0.43 / 16.0.44** — various special functions used with fields compared to a blank value (`[field1]=""`, `[field2]<>""`) could produce incorrect results. Two consecutive releases were needed, so 16.0.42 and earlier in that line are suspect.

  `RC-CALC-01` and `RC-BL-02` both teach blank-comparison patterns. Worth a note that results on affected versions may be silently wrong rather than erroring.

- [x] **DQ rule H and import-triggered calcs skipped longitudinal non-repeating fields. WRONG**
  *Applied 2026-08-18 → `RC-CALC-02`.*
  **15.0.37 / 15.5.8** (flagged "Major/near-critical"): Data Quality rule H and auto-calculations performed via data imports might **not run at all** for calc/CALCTEXT fields in longitudinal projects unless those fields sit on a repeating instrument or repeating event. Anyone who ran a data-cleaning pass on an affected version may have a false clean bill of health. Target `RC-DQ-01` and `RC-CALC-02`.

- [x] **Calcs referencing an empty repeating event failed server-side. GAP**
  *Applied 2026-08-18 → `RC-CALC-02`.*
  **15.0.31** — in longitudinal projects with repeating events, calc/CALCTEXT fields referencing a field on a repeating event with no data would fail server-side. Target `RC-BL-05`, `RC-CALC-02`.

- [x] **`@CALCDATE` could be off by hours, and display disagreed with storage. WRONG**
  *Applied 2026-08-18 → `RC-AT-09` §4.*
  **15.0.18** — a date/datetime field using `@CALCDATE` might produce a value off by several hours; the form/survey would *display* the incorrect value while the stored value differed. Display-vs-stored divergence is exactly the kind of thing that erodes trust in a calculated field. Target `RC-AT-09`.

- [x] **Dollar signs in logic broke branching logic and calcs entirely. WRONG**
  *Applied 2026-08-18 → `RC-BL-01` §4a.*
  **16.0.40** — branching logic or calculated fields containing a `$` character would suddenly stop working and might show an error. Note this alongside the **17.0.2** change (in the feature report) that blocked admins from putting JavaScript into logic at all — the two together mean any legacy "JS in logic" technique is both broken and now prohibited. Target `RC-BL-02`, `RC-PROJ-04`.

- [x] **Phantom branching-logic errors, and fields that should have been hidden weren't. WRONG**
  *Applied 2026-08-18 → `RC-BL-01` §4a.*
  **16.0.27** — some forms and surveys displayed a branching logic error popup with no real problem present, and in some cases **fields that branching logic should have hidden were not hidden**. The second half is a data-exposure concern, not just a nuisance. Target `RC-BL-01`.

- [x] **Piping into a repeating context from a non-repeating source. WRONG**
  *Applied 2026-08-18 → `RC-PIPE-02`.*
  **15.0.20** — the piped value might be blank or attached to the wrong instance. Target `RC-PIPE-02`.

---

## B. Data import silently dropping data

**Target: `RC-IMP-01`, `RC-IMP-03`, `RC-IMP-04`, `RC-API-03`**

The recurring pattern here is *silence*: imports reporting success while dropping rows. This is the cluster most worth a permanent caveat, because a user who was bitten has no way to know it from the UI.

- [x] **Rows with extra columns were silently ignored. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **15.0.17** — in a CSV import via Data Import Tool, API import, or `REDCap::saveData()`, rows after the first containing **extra columns** were silently skipped with no error. Ragged CSVs are common from Excel exports. This deserves prominent treatment in `RC-IMP-04`.

- [x] **Rows silently dropped during CSV import. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **15.0.16** — some rows might be silently dropped during Data Import Tool imports.

- [x] **Background imports dropped data when records were out of order. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **15.5.10** — when importing via the background process (API or Data Import Tool), data might **quietly not get imported, with no error**, if rows were not grouped by record. A practical, permanent recommendation for `RC-IMP-01`: sort import files by record ID, which remains good practice regardless of version.

- [x] **`redcap_repeat_instance = "new"` misbehaved repeatedly. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  - **15.0.13** — an unexpected error, or a value of `0` saved as the instance number.
  - **15.0.17** — all repeating instances for a record-instrument would fail to import **except the last one**.
  Both regressions in the 15.0.x line. `redcap_repeat_instance` is documented in eight articles; `RC-IMP-04` and `RC-API-03` are the priority. Note that 17.4.0 extended the literal `new` to the Import File API — see the feature report.

- [x] **CSV delimiter had to match the user's own profile setting. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **15.0.14**, then **15.0.15** ("thought to have been fixed in the previous version but was not") — imports failed when the file's delimiter didn't match the delimiter in the importing user's profile. A non-obvious, per-user failure mode worth mentioning in `RC-IMP-03` even though it's fixed, because it explains "it works for me but not for my colleague" reports.

- [x] **Multi-repeating-form CSVs failed outright. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **15.5.9** — CSV files containing data from more than one repeating form failed to import.

- [x] **Blank-into-blank on form status fields corrupted status. WRONG**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **16.0.30**, again **16.0.31**, and **16.0.35** — importing a blank value into an already-blank form status field left the field in a bad state; and importing all-blank values for a fresh non-repeating instrument mis-set the form status. Three releases to settle. Target `RC-IMP-04` and `RC-DE-11`.

- [x] **EAV imports with a blank `redcap_event_name` on non-longitudinal projects. GAP**
  *Applied 2026-08-18 → `RC-IMP-04` §4a.*
  **15.5.10** — Import Records API / `REDCap::saveData()` in EAV format misbehaved when the payload included a blank `redcap_event_name` column on a non-longitudinal project. Target `RC-API-03`.

- [x] **Survey settings CSV import could orphan survey attributes. WRONG**
  *Applied 2026-08-18 → `RC-IMP-07`.*
  **16.0.8** — uploading a survey settings CSV in the Online Designer could disconnect attributes such as public survey links and survey queue settings from their original surveys. Directly relevant to `RC-IMP-07`, which documents this exact workflow (added 15.8.0).

- [x] **User roles imported via CSV/API got wrong form-level rights. WRONG**
  *Applied 2026-08-18 → `RC-USER-02`.*
  **15.9.1** — creating a user role via CSV or API import might not set form-level data viewing rights correctly. Compounded by **15.7.3**: adding a user or role to a project didn't save data viewing rights correctly (emerged 15.7.0). Two independent rights-not-saved bugs in the same minor line. Target `RC-USER-02`, `RC-API-26`.
  Also **16.0.26** — User Roles in a Project XML failed to be created in the new project.

---

## C. DAG isolation leaks

**Target: `RC-DAG-01`, `RC-DE-09`, and the affected API articles**

`RC-DAG-01` presents DAGs as a data-isolation boundary. Five separate fixes show that boundary leaking, which is worth an honest note that DAG isolation is an application-layer control requiring current patches — not a hard partition.

- [x] **DAG users could modify data outside their DAG on data entry forms.** *(15.5.37, Medium security fix)* — via a crafted HTTP request, a DAG-assigned user could take control of and modify data outside their group.
  *Applied 2026-08-18 → `RC-DAG-01`.*
- [x] **Calendar entries were reachable across DAGs.** *(15.5.38, Medium security fix)* — IDOR allowing a DAG user to create, modify or view calendar events outside their DAG. Target `RC-CAL-01`.
  *Applied 2026-08-18 → `RC-DAG-01`, `RC-CAL-01`.*
- [x] **Export Survey Link API ignored DAG membership.** *(16.0.28)* — returned a link even when the record didn't belong to the API user's DAG. Target `RC-API-40`.
  *Applied 2026-08-18 → `RC-DAG-01`, `RC-API-01` §9a.*
- [x] **Export Survey Access Code / Queue Link / Return Code APIs ignored DAG membership.** *(16.0.31)* — same flaw across three methods. Target `RC-API-54`, `RC-API-41`, `RC-API-42`.
  *Applied 2026-08-18 → `RC-DAG-01`, `RC-API-01` §9a.*
- [x] **User Rights page misbehaved for DAG-assigned users with User Rights privileges.** *(16.0.18)* — modifying privileges for a user in the same DAG who was not in a User Role caused incorrect behaviour. Target `RC-USER-04`.
  *Applied 2026-08-18 → `RC-DAG-01`.*

---

## D. Export-rights bypasses

**Target: `RC-EXPRT-03`**

- [x] **File Export API bypassed "No Access" export rights.** *(15.5.33)* — a user could export a file from a File Upload field despite having No Access data export rights for that instrument. Target `RC-API-12`.
  *Applied 2026-08-18 → `RC-API-01` §9a.*
- [x] **Data Quality CSV export bypassed Full Access export rights.** *(17.3.6)* — users could export DQ rule results containing fields they lacked Full Access export privileges for. Behaviour changed going forward, so this is both a caveat *and* a behaviour change: on ≥17.3.6, DQ CSV exports are restricted. Target `RC-DQ-01`, `RC-EXPRT-03`.
  *Applied 2026-08-18 → `RC-DQ-01` §3.1.*
- [x] Related, from the feature report: **17.0.2 / 17.0.4** print-view restrictions for users without Full Data Set export rights.
  *Applied 2026-08-18 → `RC-EXPRT-03` §4a.*

Collectively these justify a line in `RC-EXPRT-03` noting that export-rights enforcement has been tightened several times and that older versions enforced it inconsistently across API and module surfaces.

---

## E. Upgrade and install traps

**Target: `RC-INFRA-01`, `RC-INFRA-02`, `RC-CC-23`**

These pair with the UTF8MB3 and PHP-version items already in the feature report, and are the most operationally expensive items in this document.

- [x] **Easy Upgrade allowed admins to skip the required Unicode Transformation. WRONG/CRITICAL** — *done 2026-08-18*
  **15.5.40 LTS** and **17.0.3 Standard**: "Unfortunately, this cannot be fixed in the version in which someone is upgrading from."
  **Two corrections to this report.** First, the charset drop was **15.6.0**, not 16.0.0. Second, and more consequentially, the situation is **not unfixable** — the "cannot be fixed" quote refers only to the version being upgraded *from*. **17.0.3 restored `ControlCenter/fixdb.php`**, reachable from the Configuration Check page, specifically so admins who upgraded to 16.0.0+ without transforming can complete it after the fact. **17.0.4** separately fixed the resulting stuck-on-upgrade-page symptom. Treating this as unrecoverable would have been actively unhelpful to anyone in that state.
  Applied: `RC-INFRA-01` §3.2 and `RC-INFRA-02` §9 now carry the full picture — the block, the three remediation paths, the Easy Upgrade bypass, the `fixdb.php` remedy, and 15.5.40 as the safe staging version.

- [x] **LTS 15.5.10 was mis-released and was actually 15.0.38. WRONG**
  *Applied 2026-08-18 → `RC-INFRA-02` §9.1.*
  **15.5.11** — anyone who upgraded to 15.5.10 from a 15.0.x version was instructed to run a manual `UPDATE redcap_config SET value = '15.0.XX' WHERE field_n…` correction. If any local runbook references 15.5.10 as an LTS target, it is wrong.

- [x] **The upgrade page itself failed under PHP 8.4 / 8.5.** *(16.0.11)* — fatal PHP error, i.e. you cannot upgrade *to* the fix from an affected combination without intervention. Interacts badly with the PHP-version guidance in `RC-INFRA-01`.
  *Applied 2026-08-18 → `RC-INFRA-01` §3.1.*

- [x] **Upgrade SQL scripts failed outright** at **15.0.2**, **15.0.25** (Easy Upgrade to 15.0.23/15.0.24 LTS and 15.3.3/15.4.0 Standard failed with an unknown error), and **16.0.24**.
  *Applied 2026-08-18 → `RC-INFRA-02` §9.1.*

- [x] **Fresh installs were broken** at **15.8.4** (SQL error in the install script, emerged 15.8.2) and **17.1.3** (install page silently crashed). `RC-INFRA-02` already documents the 17.1.2 `VANDERBILT_SERVER` fatal — worth grouping all install-blocking versions into one "known-bad install versions" table there.
  *Applied 2026-08-18 → `RC-INFRA-02` §9.1.*

- [x] **Draft Mode approval failed with a fatal PHP error.** *(15.0.7)* — approving drafted changes, or Submit Changes for Review with auto-approval, failed. Target `RC-FD-02`.
  *Applied 2026-08-18 → `RC-PROJ-01`.*

- [x] **Version-directory URLs are now blocked for survey and API endpoints.** *(16.0.16, Minor security fix)* — REDCap now refuses survey/API calls whose URL contains the version directory. Any local documentation, bookmark or integration using versioned URLs breaks on upgrade. Pairs directly with the **Automatic Version Redirect** feature (17.2.2) in the feature report. Target `RC-API-01`, `RC-SURV-04`.
  *Applied 2026-08-18 → `RC-INFRA-01` §4a.4, `RC-API-01` §3.3a.*

---

## F. Randomization integrity

**Target: `RC-RAND-03`, `RC-RAND-02`**

Four fixes touching allocation integrity — high-stakes for anyone auditing a trial.

- [x] **Deleted records did not free their allocation.** *(15.0.26, bug present since 14.7.0)* — in a longitudinal multi-arm project, deleting a randomized record left its allocation in the allocation table, so the slot was never freed. **Allocation tables on long-running projects that started on an affected version may be silently short.** This is the most consequential item in this section.
  *Applied 2026-08-18 → `RC-RAND-03` §3a.*
- [x] **Concurrent randomize-while-surveying corrupted the result.** *(15.0.23, since 14.7.0)* — randomizing on the data entry form while a participant completed the same instrument as a survey.
  *Applied 2026-08-18 → `RC-RAND-03` §3a.*
- [x] **Randomize-and-lock in the same submission produced partial randomization.** *(15.5.23)* — logged as randomized but not fully applied.
  *Applied 2026-08-18 → `RC-RAND-03` §3a.*
- [x] **Strata radio labels didn't register clicks.** *(16.0.23)* — clicking the choice *label* (rather than the radio button) in the randomization dialog didn't change the selection, so a user could randomize believing they had set a stratum they hadn't.
  *Applied 2026-08-18 → `RC-RAND-03` §3a.*

---

## G. Survey form-status corruption

**Target: `RC-SURV-03`, `RC-DE-11`**

- [x] **Required-field bypass left form status in "limbo".** *(16.0.14 → 16.0.17)* — a bug in **16.0.13 LTS / 16.1.1 Standard** let participants bypass required fields; **16.0.17** then had to repair the resulting confused Form Status values. Two-stage: the exposure window and the repair. Projects that ran on 16.0.13/16.1.1 may hold bad status values that the fix cleaned up — worth knowing when auditing completion rates.
  *Applied 2026-08-18 → `RC-DE-11` §4a.*
- [x] **"Start Over" erased data but left the status as complete/partial.** *(15.0.21)* — a participant restarting a survey had responses cleared while the survey status still read completed or partially completed. Anyone reporting on completion status from an affected version may over-count.
  *Applied 2026-08-18 → `RC-DE-11` §4a.*
- [x] **Calc/CALCTEXT referencing a survey's Form Status field didn't retrigger.** *(16.0.17)*
  *Applied 2026-08-18 → `RC-DE-11` §4a.*
- [x] **Survey submitted with empty required fields wasn't always redisplayed with the warning.** *(16.0.14)*
  *Applied 2026-08-18 → `RC-DE-11` §4a.*

---

## H. e-Consent

**Target: `RC-SURV-08`**

- [x] **Signature fields were not erased on Previous Page despite the setting being enabled.** *(15.5.17)* — the "Force signature field(s) to be erased if participant clicks Previous Page button while on the certification page?" setting silently did nothing. A compliance-relevant failure: the documented control did not take effect.
  *Applied 2026-08-18 → `RC-SURV-08` §5a.*
- [x] **Concurrent editing during consent could bypass the edit-prevention setting.** *(16.0.28)* — if a user sat on the data entry form while a respondent consented the same instrument as a survey, the user could edit responses that the "prevent editing of e-Consent responses" option was meant to protect.
  *Applied 2026-08-18 → `RC-SURV-08` §5a.*
- [x] **Inline consent PDFs rendered corrupted.** *(15.0.16)* — a PDF with a particular alpha channel type produced horizontal artefacts in the REDCap-generated PDF. Also **15.0.29** (PDFJS `.mjs` MIME-type serving) and **16.0.36** (PDF viewer toolbar buttons all disabled) affect inline PDF display generally — target `RC-SURV-09` too.
  *Applied 2026-08-18 → `RC-SURV-08` §5a.*

---

## I. Alerts & ASI non-delivery

**Target: `RC-ALERT-01`, `RC-SURV-06`**

- [x] **Alerts and ASIs silently failed to trigger.** *(15.5.10, emerged in 15.0.35 LTS / 15.5.5 Standard)* — an internal logic-caching issue meant some alerts and ASIs were not triggered as expected on form or survey submission. Rare but silent, and alerts that never fire generate no evidence.
  *Applied 2026-08-18 → `RC-ALERT-01` §4.2.*
- [x] **"Re-evaluate Send Time" was broken from introduction until 17.4.1 / 17.3.7.** *(both fixes in 17.3.7 / 17.4.1, emerged 17.2.0)* — the checkbox might not persist when saving an alert, and when it did work it rescheduled alerts and invitations at incorrect times on **any** data modification, not just changes to the time-lag field. Since the feature shipped in 17.2.0, it was unreliable for its entire life before 17.4.1. Already cross-referenced in the feature report.
  *Applied 2026-08-18 → `RC-ALERT-01` §4.2a, `RC-SURV-06` §4.2.*

---

## J. Record locking not enforced

**Target: `RC-LOCK-01`**

- [x] **Bulk Record Delete partial deletion ignored record-level locks.** *(15.5.13)* — selected forms had their data deleted inside a record locked at the record level. The changelog's own wording is the note worth quoting: "Locked records should not be editable in any way." A caveat in `RC-LOCK-01` that record locking was not universally enforced across bulk operations on older versions is fair and useful.
  *Applied 2026-08-18 → `RC-PROJ-01`.*

---

## K. Feature-launch instability

Useful for setting expectations about adopting new features early — and directly relevant to the P0 articles proposed in the feature report.

- [x] **Access Control Groups (16.0.0) had two blocking bugs in its first weeks.** **16.0.20** — with ACGs enabled, non-admin users could not access **any** project (fatal PHP error on every page). **16.0.23** — uploading a Data Dictionary with ACGs enabled failed fatally. Target `RC-CC-25`.
  *Applied 2026-08-18 → `RC-CC-25` §2.*
- [x] **Project Migration Tool (17.0.0) lost files in longitudinal projects.** **17.0.6** — migrating a longitudinal project with File Upload and/or Signature field files silently omitted some files and signatures. Anyone who migrated on 17.0.0–17.0.5 should re-verify file completeness. Target the proposed `RC-PLUS-02`.
  *Applied 2026-08-18 → `RC-PLUS-02` §5, alongside two further silent-omission defects the original entry did not capture: records dropped for failing field validation (below 17.0.2) and the Development record limit truncating migrations of Production projects (below 17.1.4).*
- [x] **Enhanced Signature (17.1.0) signatures were missing from PDFs.** **17.1.1** — the signature image did not appear in downloaded instrument PDFs or PDF Snapshots. Target `RC-SURV-09` and the Enhanced Signature content proposed for `RC-FD-06`.
  *Applied 2026-08-18 → `RC-FD-06` §8.8.1.*
- [ ] **Rewards (17.0.0) cron crashed repeatedly.** **15.5.5** references `ProcessScheduledRewardOrders` crashing — note the version, which suggests reward plumbing predates the 17.0.0 announcement. Worth confirming before writing the proposed `RC-PLUS-03`.
  *Not applied — deferred to **`RC-PLUS-03`** (Reward Services) — and still needs confirming; the 15.5.5 `ProcessScheduledRewardOrders` reference predates the 17.0.0 announcement.*
- [x] **MyCap app-to-server communication broke for already-joined participants.** *(16.0.37)* — with an explicit note for institutions that had already upgraded. Target `RC-MYCAP-01`.
  *Applied 2026-08-18 → `RC-MYCAP-01` §5.1.*

---

## L. Security posture

**Target: a new short article, or a section in `RC-INST-01`**

67 security fixes at 15.0.0+: 8 Critical, 34 Major, 15 Medium, 10 Minor. Individually these are "patch promptly" and not KB content. Collectively they support one piece of durable guidance worth writing once.

Patterns worth stating:

- **Stored and Reflected XSS via user input** is by far the most common class — field labels, survey instructions, DAG names, Project Bookmark URLs, Messenger conversations, Descriptive Popup link text, MLM content, uploaded CSVs for DAGs and bulk user creation. The lesson for `RC-FD-08` and `RC-DSGN-01`: **user-supplied HTML in field labels and instructions is a recurring attack surface**, which is worth knowing before recommending raw HTML as a design technique.
- **Remote Code Execution via stored logic** recurred at 15.0.4, 15.0.32 and 16.0.39 — all through calculations, branching logic, DQ rule logic or report filter logic. This is the security rationale behind the 17.0.2 change blocking JavaScript in logic, and makes that change worth documenting as a deliberate hardening rather than an arbitrary restriction.
- **Third-party library vulnerabilities** drove a steady stream of fixes: Axios (SSRF), PDFJS (arbitrary JS execution, exploitable by survey participants), DOMPurify inside TinyMCE, Underscore.js, and an unnamed PHP library. Relevant to any local policy on pinning or vendoring.
- **Two unauthenticated issues** stand out because they don't require a logged-in attacker: **16.0.37** an Unauthenticated Open Mail Relay on a survey-related page, noted as existing in **all REDCap versions**; and **15.5.36** a Stored XSS on a File Repository page exploitable by survey participants.
- **MyCap's backend API had repeated participant-impersonation flaws via a shared signing key** (16.0.19, again 16.0.36), plus unauthenticated study-code enumeration (16.0.39) and SQL injection (15.5.39, 16.0.39). If `RC-MYCAP-01` says anything about the security model of the app-to-server channel, it should reflect that this area has needed several rounds of fixes.
- **Cookie flags** were not reliably set on 2FA Trust Cookies or Survey Login session cookies (both 16.0.25) — relevant to `RC-SURV-10` and `RC-CC-03`.
- **Salt values could be brute-forced** (15.0.39), which has implications for anything deriving from project or system salts.

**Suggested deliverable:** a short "Security & Patching" article stating that REDCap ships security fixes in most releases, that LTS and Standard receive them in parallel, that the changelog labels severity, and that running an unpatched instance is the single largest controllable risk — with the version-directory blocking (16.0.16) and old-version-directory removal (15.5.36) as concrete practices. This is genuinely useful for the audience `RC-INST-01` addresses.

---

## Deliberately excluded

Roughly 1,000 of the 1,076 routine bug fixes are transient defects with no durable lesson: a button that didn't render, a dialog that didn't close, a column that sorted wrong, a fatal error in one page for one release. They were fixed, the fix is in every current version, and documenting them would make articles harder to read without making any reader more capable.

The filter applied: an entry earns a place only if **(a)** it changes what a reader should believe about how a feature behaves, **(b)** it defines a version window where documented behaviour did not hold, or **(c)** it silently affected data, rights or delivery in a way a user could not have detected at the time.

---

## Suggested order of work

1. ~~Agree a caveat convention~~ — **done.** The `> **Version caveat (range):**` blockquote is specified in the kb-creation skill, with rules on what qualifies.
2. ~~`RC-CALC-01` §5.2 — the `age_at_date()` window~~ — **done.**
3. ~~`RC-IMP-04` — the silent-drop cluster~~ — **done**, including the version-independent recommendation to sort import files by record ID.
4. ~~`RC-INFRA-01` — Unicode Transformation~~ — **done**, alongside the charset and PHP prerequisites.
5. ~~`RC-RAND-03` — allocation not freed~~ — **done**, with the other three allocation-integrity defects.
6. **Security posture article — still outstanding.** The one item from this report not yet actioned in any form. The 67 security fixes remain undocumented as a group; the patterns are recorded in Section L below.

---

## Caveats on this report

- Affected-version windows are only as good as the changelog's own provenance. 86 entries state when a bug emerged; for the rest, the fix version is a **lower bound on when it was fixed**, not evidence of when it started. Windows above are stated only where provenance exists, and hedged where it doesn't.
- Standard and LTS version numbers are not comparable. Where the changelog names both lines (e.g. "15.0.35 LTS and 15.5.5 Standard"), both are preserved above; elsewhere the earliest version across the merged set is shown, which may be from either line.
- No article bodies were read in full for this pass beyond the `age_at_date()` and "known issue" checks. Confirm the target section before adding a caveat.

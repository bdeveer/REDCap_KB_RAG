# KB Update To-Do — REDCap 17.4.1 → 17.5.4

> **Complete — all items worked, closed 2026-10-09.** The KB's high-water mark is now **17.5.4 Standard / 17.3.18 LTS**. Two things are still outstanding and are carried in `PROJECT-TODO.md`: REDCap login protection (P0) is written from release notes only and needs verifying on a REDCap+ instance; and the 2FA re-enrolment recommendation asks admins to confirm on a test account that a reset issues a new secret.

**Generated:** 2026-10-09
**Source:** `ChangeLog_Standard_2026-10-09.csv` + `ChangeLog_LTS_2026-10-09.csv`
**Current releases:** Standard **17.5.4** (2026-10-08) · LTS **17.3.18** (2026-10-08)
**Previous review:** `KB-UPDATE-TODO-17.4.1.md` (closed 2026-09-02) and `KB-GOTCHAS-FROM-BUGFIXES-17.4.1.md`

---

## Scope & method

- **Version floor:** everything above Standard 17.4.1 and LTS 17.3.7 — Standard 17.4.2 → 17.5.4 (2026-08-20 → 10-08; 17.5.0 opens a new Standard minor line) and LTS 17.3.8 → 17.3.18.
- **All change types included**, bug and security fixes too — unlike the 17.4.1 review, which scoped them out. This partly answers the "sweep excluded changelog rows" item in `PROJECT-TODO.md` for this window.
- Standard and LTS logs were merged and de-duplicated on normalised description text; each item is attributed to the **earliest** version it shipped in. 355 rows → **199 unique entries**: 1 New Feature (REDCap+), 20 Improvement, 9 Change, 136 Bug fix, 2 Major bug fix, 31 security fixes (1 critical, 17 major, 12 medium, 1 minor).
- "Not covered" claims were confirmed by a literal string search against `kb/`.

**Severity key**

| Tag | Meaning |
|---|---|
| **NEW** | No KB coverage exists |
| **WRONG** | Existing KB text is now factually incorrect |
| **GAP** | Existing article is correct but silent on the change |
| **MINOR** | Cosmetic / UI-polish; update only when the article is next touched |

---

## Summary

| Priority | Items | Effort | Status |
|---|---|---|---|
| P0 — Major feature additions | 2 | Medium | ✅ Done 2026-10-09 (login protection pending verification) |
| P1 — Wrong or materially incomplete | 6 | Small–medium | ✅ Done 2026-10-09 |
| P2 — Gaps worth filling | 20 | Small | ✅ Done 2026-10-09 |
| P3 — Minor / cosmetic | 6 | Trivial | ✅ Done 2026-10-09 |
| Gotchas (bug & security fixes) | 6 clusters | Medium | ✅ Done 2026-10-09 |
| No doc impact | ~150 | — | — |

No new articles are needed — everything fits into existing ones.

---

## P0 — Major feature additions

- [x] **Enforce REDCap login protection** *(17.5.0, REDCap+)* — **NEW** — `RC-SURV-10`, `RC-PROJ-03`, public-reports coverage, `RC-PLUS-01` — *done 2026-10-09, pending verification*
  Written: `RC-SURV-10` §5 (new section; Security Settings and later renumbered), `RC-EXPRT-06` §4.2, `RC-PROJ-03` §5.5, `RC-PLUS-01` §4. Each carries a REDCap+ tag and a release-notes-only scope note. Left open in the articles: whether it covers the Public Survey, and whether the 8-data-point threshold still applies to logged-in dashboard viewers.
  New Survey Login option: uses REDCap's standard login flow instead of matching stored field values. Optional prefill of page-1 fields from login attributes (username, first/last name, email…), which can be made readonly/hidden with action tags. Under any "X & Table-based" authentication, an optional **"Allow access for internal users only"** blocks Table-based (external) users. The same protection can be applied to any **public report** or **public project dashboard** via an "Enabled REDCap login protection" button beneath it. Non-Table-based auth: a person with no REDCap account can still get in if they pass authentication.
  Related fixes: Return Code mistakenly requested under this mode with Save & Return enabled (fixed 17.5.4); URL-parameter prefill not working with Survey Login enabled (fixed 17.3.14).
  **Verification debt:** same as the other REDCap+ articles — the maintaining instance has no subscription. Add a scope note.

- [x] **`@HIDEDATEPICKER` action tag** *(17.5.0)* — **NEW** — `RC-AT-07`, `RC-AT-01` (tag table + category table), redcap-syntax / redcap-dd-* skill references — *done 2026-10-09*
  `RC-AT-07` new §3 (later sections renumbered), `RC-AT-01` both tables, `meta/KB-KEYWORD-MAP.md`, and the action-tag dictionary in `redcap-data-dictionary/scripts/parse_dd.py`. No other skill carries an action-tag list.
  Hides the calendar/time-picker icon on date, time and datetime fields. Does **not** hide the Now/Today button — pair with `@HIDEBUTTON` for that. Same release replaced the datepicker icons with a Font Awesome icon (17.5.0).

---

## P1 — Wrong or materially incomplete

- [x] **RC-INFRA-03 — release-line tables** — **WRONG** — Add the 17.5.x Standard line (17.5.0 on 2026-09-17) and LTS 17.3.8–17.3.18; move "current" to 17.5.4 / 17.3.18; bump *Verified Against*. Consider using the 17.3.10 critical RCE (below) as the worked example for "keeping current is the main risk control". — *done 2026-10-09*
  Tables updated; 16.0.x is still receiving fixes (16.0.55), so the old 'through 2026-08-13' end date was wrong. Added the 2026-09-09 and 2026-10-08 same-day examples and the 17.3.10 RCE to §7.
- [x] **MyCap App Settings tab renamed** *(17.5.0)* — **WRONG** — `RC-MYCAP-05` "Notification Settings" is now **"Additional Settings"**, and also holds the new **"Allow participants to send messages to the project user(s)"** toggle (participants still receive announcements and messages). — *done 2026-10-09*
  RC-MYCAP-05 §2, §3.5, §4 and two Q&As; tab name also fixed in RC-MYCAP-02 and -08.
- [x] **MyCap logging identity** *(17.5.3)* — **WRONG** — `RC-LOG-01`, `RC-MYCAP-05`: MyCap submissions now log the user as `[mycap respondent]` and the description as `(MyCap - API)` rather than `(API)`, in both Logging and the Data History popup. — *done 2026-10-09*
  RC-LOG-01 Username row + Q&A; RC-MYCAP-05 Q&A. Was a gap rather than wrong: RC-LOG-01 had no MyCap coverage at all.
- [x] **Custom Record Dashboards management page** *(17.5.3)* — **WRONG** — `RC-NAV-REC-04`, `RC-NAV-UI-02`: users with Project Design rights get a **"Manage"** link next to Record Status Dashboard on the project menu — list, create, edit, delete. The Record Status Dashboard's buttons also changed; re-check the article's description of them. — *done 2026-10-09*
  RC-NAV-REC-04 new §4.3; RC-NAV-UI-02 menu row. The changelog does not say which buttons changed, so the article says only that they did.
- [x] **Always-blocked upload extensions** *(17.3.18 LTS)* — **WRONG** — `RC-CC-05` "Restricted File Types": `php, phtml, php3, php4, php5, phar, cgi, shtml, shtm, pht` are now rejected regardless of configuration. — *done 2026-10-09*
  RC-CC-05 new subsection + caveat. Also shipped in 16.0.55 LTS. Default blocklist already had `php` but none of the variants.
- [x] **Map of Users** *(17.3.18 LTS)* — **WRONG** — `RC-CC-14`: the map stopped working; the page now explains how to obtain and store your own Google Maps API key. — *done 2026-10-09*
  RC-CC-14 note + Q&A. Also in 17.5.4 Standard.

---

## P2 — Gaps worth filling

### Surveys, e-Consent & forms

- [x] **Piping into the survey title** *(17.5.3)* — `RC-SURV-02` §3.2, `RC-PIPE-01`: works for existing records only (public surveys excluded); evaluated on page load, not live. — *done 2026-10-09*
  RC-SURV-02 §3.2 + caveat; RC-PIPE-01 location list.
- [x] **e-Consent placement field** *(17.4.3)* — `RC-SURV-08`: the Descriptive field chosen under "Placement of consent form" **cannot be the only field** on the instrument, or the certification-page PDF won't generate. Also (17.3.14): longitudinal setup now validates that the PDF snapshot save-to field belongs to the selected event. — *done 2026-10-09*
  RC-SURV-08 field description. The 17.3.14 save-to-field validation note was not added — it is a fix, not documented behaviour.
- [x] **Instrument snapshot annotations** *(17.5.0)* — `RC-FD-02` (and revision-history coverage): the Online Designer snapshot button accepts an optional comment and attachment, viewable on Project Revision History; the comment is editable afterwards. — *done 2026-10-09*
  Landed in RC-FD-08 §6.2 and the RC-FD-06 toolbar table, where snapshots are actually documented — not RC-FD-02.
- [x] **Accessibility** *(17.4.2, 17.5.4)* — `RC-SURV-11`: readonly calc fields keyboard-accessible and announced as read-only; signature/file-upload prompts announced as dialog buttons; navigation separated from main content on all pages; survey banner landmark fixed; "Skip to login form" link on the login page. — *done 2026-10-09*
  RC-SURV-11 §3.1 and §3.2 tables; scope line moved to 17.5.4 / 17.3.18.

### MyCap

- [x] **"Partial MyCap Response" status** *(17.5.0)* — `RC-MYCAP-02`/`-05`: incomplete Save & Return task submissions get a dedicated status and a record banner (start + entry dates) until the participant completes a full sync. Also clarify (17.4.3) that "Allow save and complete later?" behaves differently by task schedule. — *done 2026-10-09*
  RC-MYCAP-02 new §5.3 + caveat. MyCap articles had no prior Save & Return coverage.
- [x] **Fixed schedules hide "Number of days to delay"** *(17.5.3)* — `RC-MYCAP-03`: a delay overrides a fixed schedule, so the input is hidden. The article's Delay Onset text should say it doesn't apply to Fixed. — *done 2026-10-09*
  RC-MYCAP-03 §4 + caveat (value overrides fixed dates below 17.5.3).
- [x] **Media in Descriptive fields** *(17.4.3)* — `RC-MYCAP-02`: MyCap tasks now support attachments and embedded media in Descriptive fields. — *done 2026-10-09*
  RC-MYCAP-02 field compatibility table.
- [x] **Production-mode warnings** *(17.4.3, 17.5.3)* — `RC-MYCAP-03`/`-08`: new prompts warn that editing active schedules can make completed tasks reappear, and that live changes can't be previewed before release. — *done 2026-10-09*
  RC-MYCAP-03 gotcha, pointing to RC-MYCAP-08.
- [x] **QR code popup** *(17.4.3)* — `RC-MYCAP-04`: auto-scrolls to show the QR code. (Could be P3.) — *done 2026-10-09*
  RC-MYCAP-04 QR Code definition.

### Control Center & administration

- [x] **Change Username** *(17.5.0)* — `RC-CC-07`: Browse Users gains a "Change Username" button (logged) that rewrites the username everywhere **except** `redcap_log_event*` / `redcap_log_view`, plus a "History" button. Early bugs fixed in 17.5.1 (could recreate an account under the old name; users with history couldn't be deleted) — cite 17.5.1 as the safe floor. Sponsor change errored in 17.5.0 only (fixed 17.5.3). — *done 2026-10-09*
  RC-CC-07 new subsection + 17.5.0 caveat (sponsor bug 17.5.0–17.5.2 included); synonyms added.
- [x] **"Fix Legacy Image/File URL" page** *(17.3.12 LTS)* — `RC-CC-*` / `RC-INFRA-*`: regenerates `doc_id_hash` URLs broken by the 17.3.11 / 17.4.5 hash security fix. Upgrades from 17.3.14 onward fix them automatically (completed in 17.3.18), so only intermediate versions need the manual tool. Affects rich-text images and pasted file-download links created before 15.7.3. — *done 2026-10-09*
  RC-CC-02 new section with versions for all three lines (17.4.6 / 17.3.12 / 16.0.51) and the auto-repair timeline.
- [x] **API token masking** *(17.5.0)* — `RC-CC-02`: API token fields on General Configuration are now password-masked. — *done 2026-10-09*
  RC-CC-02 note above the General Configuration intro.
- [x] **`disable_functions` recommendation** *(17.5.4)* — `RC-CC-02` / `RC-INFRA-01`: Configuration Check recommends adding dangerous PHP functions (`system`, `exec`, …) to `disable_functions` in php.ini. — *done 2026-10-09*
  RC-CC-02 Secondary Tests; RC-INFRA-01 new §4a.3b.
- [x] **Version Redirect** *(17.3.10–17.3.18)* — `RC-CC-02`, `RC-INFRA-01`: NGINX guidance now uses a 404 fallback in the default location block (the old `redcap_redirect.php` fallback could trigger IP bans); Apache test also checks `rewrite_module`; `AllowOverride` note added to the mod_rewrite step. — *done 2026-10-09*
  RC-CC-02 and RC-INFRA-01 — refinements by version on both lines, plus NGINX IP-ban caveat.
- [x] **To-Do List email logging** *(17.5.1)* — `RC-CC-09`: To-Do request emails have their own Email Logging category and filter option. — *done 2026-10-09*
  RC-CC-09 §6 step 4.
- [x] **Expire Surveys cron logging** *(17.5.1)* — survey-expiration coverage: each expired survey is now logged in `redcap_log_event`. — *done 2026-10-09*
  RC-SURV-03 §4.3.
- [x] **Admin password-reset logging** *(17.4.2, 17.3.14)* — `RC-CC-07`: admin-triggered reset emails are logged, and the "Password last reset via password reset email on X" text records when the user completed the reset. — *done 2026-10-09*
  RC-CC-07 Account Actions.

### Records, randomization & project lifecycle

- [x] **Move to production with randomized records** *(17.4.4)* — `RC-RAND-03`, `RC-PROJ-01`: extra warning in the dialog. Also (17.3.13): admins can no longer upload a development allocation table once in production — previously the buttons only looked disabled. — *done 2026-10-09*
  RC-RAND-03 new §7.2a; pointer in RC-PROJ-01 §2.2.
- [x] **Record List Cache lock** *(17.3.16 LTS)* — `RC-PROJ-01`: renaming records and changing DAG assignment are blocked while the cache is in "Processing" status. — *done 2026-10-09*
  RC-PROJ-01 §5.4.
- [x] **CDP result summary & navigation** *(17.4.2)* — CDIS mapping articles: collapsible results summary, sorted categories, sticky headers. Low priority. — *done 2026-10-09*
  RC-CDIS-02 §6.3 table row.

---

## P3 — Minor / cosmetic — ✅ *done 2026-10-09*

Datepicker icon folded into `RC-AT-07` §3 (P0 pass); the others went to `RC-FD-11`, `RC-CC-07`, `RC-DE-02`, `RC-CC-08` and `RC-LOG-01` §3.1.

- [x] Datepicker icons replaced with Font Awesome (17.5.0) — fold into the `@HIDEDATEPICKER` edit.
- [x] Quick Modify Field(s) selection more visible, Escape handling improved (17.4.4) — `RC-FD-11`.
- [x] Browse Users / Add Users page restyle (17.5.0) — `RC-CC-07`.
- [x] Section Navigation box slides under the form on narrow windows (17.3.18).
- [x] Custom validation tooltips for Data Type / Display Name were swapped (fixed 17.4.3).
- [x] Browser "Save as PDF" export option now logged (17.3.16) — `RC-LOG-01`.

---

## Gotchas from bug & security fixes

Append these to `KB-GOTCHAS-FROM-BUGFIXES-17.4.1.md` (or start a 17.5.4 companion), and push the durable ones into the articles named.

### Logic & calculation evaluation — `RC-BL-*`, `RC-CALC-*`, redcap-syntax skill — ✅ *done 2026-10-09*

Applied to RC-BL-01/02/05, RC-CALC-02, RC-AT-07/08/09, RC-ALERT-01; recorded as section M of `KB-GOTCHAS-FROM-BUGFIXES-17.4.1.md`; redcap-syntax gained a comments rule (`syntax-core.md` §3) and a version-defect check (`fix-mode.md` 4f, plus `export_redcap_version` in the allowed tools). The alert-logic comments item from the Alerts cluster was covered here too.


- [x] **Long logic always True** — logic with more than ~200–300 AND/OR clauses evaluated to True. Emerged 17.3.1 Standard; fixed 17.3.8 LTS.
- [x] **Inline comments in logic** could fail to evaluate in various places (fixed 17.3.18), including alert logic, which could stop alerts from firing (fixed 17.3.14).
- [x] **Quotes in string literals** — apostrophes or quotes inside static text or label values in logic/calcs generated invalid JavaScript (fixed 17.3.18).
- [x] **`0` treated as blank** for integer/number fields on repeating events, and blanks as non-blank, in client-side branching (fixed 17.3.18).
- [x] **X-instance smart variables on dates with Missing Data Codes** returned wrong results in the browser only, not server-side (fixed 17.3.13).
- [x] **All calc fields recalculated on any change** instead of only dependent ones (fixed 17.3.16) — relevant to performance on large forms.
- [x] Related: CALCTEXT HTML stripped when piped on another page of a multipage survey (fixed 17.3.14); `@IF` making PDFs very slow (fixed 17.3.10); `@INLINE-PREVIEW` broken in 17.4.2 only (fixed 17.4.3).

> ✅ *All clusters below done 2026-10-09 — recorded as section N of `KB-GOTCHAS-FROM-BUGFIXES-17.4.1.md`.*

### Alerts & ASIs — section I

- [x] **Duplicate alert sends** — scheduled alerts re-sent multiple times after restarts or upgrades, due to duplicate recurrence rows (fixed 17.3.14).
- [x] ASI reminders mis-scheduled with time-lag-from-date + re-evaluate (fixed 17.3.14).
- [x] MLM language IDs with uppercase letters ignored in alerts/ASIs → default language sent (fixed 17.3.8). Also `RC-MLM-01`.
- [x] Rich-text embedded images broken in outgoing emails, 17.5.1–17.5.3 Standard only (fixed 17.5.4).
- [x] Notification Log hid overdue one-time notifications and shifted recurring dates (fixed 17.3.14) — `RC-ALERT-02`.

### Survey form status & Save & Return — section G

- [x] Imports / Project XML with only the record ID on the first instrument set its Form Status to `0` (red) instead of blank (fixed 17.3.9).
- [x] Return codes not reserved atomically, so under concurrency a code could be reused or attached to the wrong response (fixed 17.3.14).

### Access & export rights — sections C and D

- [x] DAG administration routes didn't require the `data_access_groups` privilege — all versions (fixed 17.3.14).
- [x] Project XML API export bypassed the full-export privilege check (fixed 17.3.11) — `RC-API-*` Project XML export.
- [x] Delete links in Data History for READONLY / non-editable File Upload fields (fixed 17.3.14).
- [x] User-role CSV upload accepted usernames with leading/trailing spaces that then couldn't be removed (fixed 17.3.13) — `RC-USER-02`.

### Import, export & structure

- [x] JSON exports of large projects with repeating forms/events came back empty from memory exhaustion (fixed 17.3.14).
- [x] Project XML generated before 17.3.0 failed to import on 17.3.0+ when event/DAG names had accented characters (fixed 17.3.13); MyCap-enabled XML imports failed (fixed 17.3.14); MyCap participants couldn't join XML-created projects (fixed 17.3.10). — `RC-PROJ-05`.
- [x] Arms couldn't be downloaded from Define My Events with fewer than two events (fixed 17.3.9) — longitudinal articles / skills.
- [x] Data Quality rule export with checkbox fields wrongly reported "no export privileges", 17.3.6 / 17.4.0 → fixed 17.3.11.
- [x] Copy Project didn't carry over the "Record-level Locking Enhancement" setting (fixed 17.3.9); admin-performed copies used the admin's email as the From address for ASIs/alerts (fixed 17.3.14).

### Security posture — section L and `RC-INFRA-03`

- [x] **Critical (17.3.10):** unauthenticated remote code execution via survey passthrough routing — 13.3.0 and higher, needs only a valid survey hash.
- [x] **Major (17.3.14):** fail-open `SUPER_USER` check could grant full admin rights (all versions); weak randomness in 2FA TOTP secrets (all versions); Control Center POST tampering could write protected config values (17.3.10, 17.3.14); two MyCap SQL injections (13.0.0+).
- [x] **Major (17.3.11):** deterministic AES-CBC IV in the encryption helper; predictable project salts; weak MyCap code randomness; legacy document-hash acceptance; hook-loader file inclusion.
- [x] **Major (17.3.18):** SSRF in content fetching; project-settings authorization weakness; stored XSS in record-locking customization; the upload-extension block (see P1).
- [x] Medium: CSS injection in HTML filtering, path traversal in AI "Summarize Data" (15.0.0+), plus a batch of stored/reflected XSS in admin pages (17.3.9–17.3.18).
- [x] Framing: the 17.3.11 hash fix is what broke legacy image/file URLs — tie this to the "Fix Legacy Image/File URL" P2 item so admins understand why the links broke.

---

## Suggested order of work

1. P0 Survey Login / login protection (largest; carries a REDCap+ scope note).
2. P0 `@HIDEDATEPICKER` — small, and feeds the skills.
3. Logic-evaluation gotchas → `RC-BL-*`, `RC-CALC-*`, redcap-syntax references.
4. MyCap batch (P1 rename + logging, P2 items).
5. Control Center & admin items.
6. `RC-INFRA-03` tables and security framing; append the gotchas file.
7. Bump *Verified Against* only on articles actually edited.

---

## Caveats

- REDCap+ items can't be verified against the maintaining instance (no subscription).
- Article matching was done by keyword search plus hand review, not version pinning — the `PROJECT-TODO.md` pinning item still applies.
- LTS-first attribution: many fixes shipped the same day on both lines; the version cited is the earliest one, often the LTS number.

# KB Update To-Do — Randomization, checked against REDCap 17.6.1

> **Complete — applied 2026-11-23.** A topic review rather than a full changelog pass: only the randomization articles, checked against a live 17.6.1 Standard instance and the Standard changelog. Contributed by a KB user via GitHub issue #4.
>
> **Maintainer verification (2026-11-23), against REDCap 17.5.9 Standard source, read-only:** the FAQ entries behind every P1/P2 item (`Help/help_content.php`: one randomization event per record across all arms, pre-randomization arm, scheduling caveat, Dashboard unblinding and Randomize strata/PHI warnings, Setup downloads, templates not for production, calc fields not strata, DAG or field for site, trigger fires once, all-users option needs extra testing, deletion frees the allocation, production tables append-only, no model limit, Mobile App); `[rand-time]` help string `random_151` and `Randomization::getSmartVariableData()` (server time, user format only); `ProjectGeneral/change_project_status.php` (P1 #5: keeping records on the move to production clears each model's randomization field on its event and frees used production slots; the records themselves are kept); `ProjectGeneral/create_project.php` (Copy Project strips randomization field values); `Classes/MultiLanguage.php` (MLM UI tab has a Randomization group). Changelog-only items (17.5.7 concurrency fix and log primary key, 17.3.0 CSV export, 15.x caveats, 15.5.0 citation, ACG <16.1.0) were taken from the contributor's review and not re-checked. LTS fix versions still not looked up.
>
> **Not applied, by design:** the "missing data codes as DAG choices" (<15.6.1) and "false strata error" (<16.0.5) caveats are routine UI bugs that fail the writing-rules bar for a version caveat. The DQ real-time pointer was not added to the DQ article (the caveat lives in `RC-RAND-03` §3a). `RC-PROJ-05` does not cover Copy Project, so the Copy Project note went to `RC-RAND-03` §7.3 only. `RC-MOB-01` already listed randomization as unsupported.

**Generated:** 2026-11-19
**Articles in scope:** `RC-RAND-01`, `RC-RAND-02`, `RC-RAND-03`, `RC-PIPE-13`
**Current release:** Standard **17.6.1** (2026-11-14)
**Previous coverage:** `RC-RAND-01`/`02` and `RC-PIPE-13` verified against 17.4.1 / 17.3.7 LTS; `RC-RAND-03` against 17.5.4 / 17.3.18 LTS (all by changelog review, pages not re-captured). Randomization items from earlier reviews: `KB-GOTCHAS-FROM-BUGFIXES-17.4.1.md` §F and `KB-UPDATE-TODO-17.5.4.md` "Records, randomization & project lifecycle".

---

## Scope & method

- **Sources:**
  1. The built-in **Help & FAQ** of a 17.6.1 Standard instance: the "Randomization Module" section, the "Randomization Privileges" entries in the user-rights section, and the Mobile App randomization entry.
  2. The built-in **smart variable help** of the same instance (the Randomization group).
  3. The **Standard changelog** (community site, viewed 2026-11-19): every row above 15.4.4 whose text matches `randomi[sz]`, `allocation` or `rand-number|rand-time|rand-utc`. **28 rows.** All change types included, bug and security fixes too.
  4. Lessons from real projects (UAT automation and reporting on two longitudinal trials, 17.5.x), marked *(field)*.
- **Not done:** the LTS changelog was not reviewed. LTS version numbers for the bug-fix caveats below still need looking up; earlier reviews quoted LTS numbers (e.g. 15.5.23, 16.0.23), so do the same when applying them.
- **Not observed live:** whether moving to production clears randomization values on existing records. `RC-RAND-02` §4.6 step 14 says it does; the 17.4.4 dialog warning (already in `RC-RAND-03` §7.2a) is consistent with that, but nobody has watched it happen on 17.6.1. See P1 item 5.
- Changelog and FAQ wording is paraphrased here, not copied; see `LICENSING.md` on text from official REDCap sources.

**Severity key** — same as the earlier reviews.

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
| P1 — Wrong or materially incomplete | 5 | Small–medium | ✅ Done 2026-11-23 |
| P2 — Gaps worth filling | 9 | Small | ✅ Done 2026-11-23 |
| P3 — Minor / cosmetic | 9 | Trivial | ✅ Done 2026-11-23 |
| Gotchas (bug fixes) | 6 | Small | ✅ Done 2026-11-23 |
| Metadata | 4 articles | Trivial | ✅ Done 2026-11-23 |
| No doc impact | 9 changelog rows | — | — |

No new articles are needed.

---

## P1 — Wrong or materially incomplete

- [x] **`RC-PIPE-13`: `[rand-time]` is server time, not the user's timezone.** **WRONG.**
  The 17.6.1 smart-variable help says `[rand-time]` is the **server** date/time and that, when piped, only its **format** follows the viewing user's date/time display preferences. The article says three times that it is converted to the user's timezone: §2 "UTC Time" (REDCap "records randomization in UTC and provides conversion to the user's local timezone"), §4 "Server Time vs. UTC Time" ("displayed according to the user's timezone preference") and §5 Q2 ("displays in the user's local timezone"). `RC-RAND-03` §6 already has it right ("Uses server time (not local device time)").
  Fix: reword all three to "server time; format follows the user's date/time display preference"; keep the `:value` guidance. Also check §6's "`:value` … ignores the user's timezone preferences" — `:value` ignores the display **format**.

- [x] **`RC-RAND-01` §3 + §4 Q&A, `RC-RAND-02` step 4: one randomization event per record, across all arms; pre-randomization arm pattern.** **WRONG (incomplete).**
  The FAQ says the randomization field is enabled for randomization on **only one event per record, counting all arms**. Its suggested workaround: a **pre-randomization arm** holding eligibility, demographics and the forms up to randomization; after randomization staff add the record to the right study arm. A record can belong to several arms, but the scheduling module only schedules events in one.
  The articles currently say multi-arm designs must "randomize outside REDCap, or the project must be redesigned" (`RC-RAND-01` §3 "Multi-arm longitudinal projects", §4 Q "Can I randomize records into different arms…"). That leaves out the documented workaround. Add the one-event rule and the pre-randomization arm pattern, plus the scheduling caveat. Keep "records can't move between arms automatically" — still true.

- [x] **`RC-RAND-01` §3 "Randomization User Rights", `RC-USER-03`: Dashboard can unblind; Randomize exposes strata.** **GAP (study integrity / PHI).**
  From the FAQ's user-privileges entries:
  - **Dashboard** shows which records went to each group, so it **can unblind** a blinded study.
  - **Randomize** lets the user view and edit the **stratification fields** in the randomization dialog even without form-level rights to them. If a stratum is PHI (e.g. location), the user sees it regardless of form rights.
  - **Setup** also covers downloading allocation tables, not only uploading.
  Add these to the rights table's "What it allows" column and to the blinded-study guidance in the Open vs. Blinded decision table ("Who needs the decode key?"). Check `RC-USER-03`'s randomization privileges entry for the same.

- [x] **`RC-RAND-03` §3a: concurrent randomization could double-assign or overwrite** *(below 17.5.7 Standard)*. **Gotcha → caveat.**
  Randomizing a record that already had an allocation, or two simultaneous randomize requests for the same record, could cause a database error, and one request could overwrite the allocation another had just assigned. This is an allocation-integrity defect of the same kind as the four already in §3a; add it there, with the LTS version once looked up. Reconciling the allocation table against the log (already advised in §3a) is the check.

- [x] **`RC-RAND-02` §4.6 step 14 / `RC-RAND-03` §7.2a: confirm what happens to randomized values on the move to production.** **Verification.**
  `RC-RAND-02` says the values are cleared; `RC-RAND-03` §7.2a says to "decide deliberately whether to keep those records", which reads as if they survive. Both can be true (records kept, randomization field cleared), but the two articles should say the same thing. Observe it once on a development project with a randomized test record, then align the wording in both articles and in `RC-PROJ-01` §2.2.

---

## P2 — Gaps worth filling

- [x] **Trigger logic randomizes a record only once** — `RC-RAND-02` §4.5, `RC-RAND-03` §3.2. FAQ: once randomized, saving the record again while the logic is still true does not re-randomize it. The FAQ also says the "all users (including survey respondents)" option deserves extra testing; add that to the table's "when to use" text.

- [x] **Template allocation tables are templates only** — `RC-RAND-01` "Allocation Tables", `RC-RAND-02` step 9. FAQ: the tables REDCap generates from the model are templates and must not be used for randomization in production. The articles call it a "template" but never say not to use its rows.

- [x] **Calculated fields can't be strata** — `RC-RAND-01` §3 Stratification row and §4 Q1, `RC-RAND-02` step 2 and the pre-flight checklist. FAQ workaround: a single-choice field beside the calculated field, filled in by hand from the calculation, used as the stratum.

- [x] **Site stratification by DAG *or* by a dedicated field** — `RC-RAND-01` §3 "Sites / Groups (Multi-site)" says it is "a special form of stratification using … DAG". The FAQ (and `RC-RAND-02` step 8c) also allow a dedicated single-choice site field. Align `RC-RAND-01`.

- [x] **Deleting a randomized record frees its allocation** — `RC-RAND-03` §7 or §9. FAQ: deleting a randomized record, whichever position it had, returns its allocation to the pool for a future record. §3a only describes the old bug where it didn't; state the normal behaviour plainly, and note the consequence: deleting test records in production returns their slots.

- [x] **`RC-RAND-03` §6: replace the "consult the smart variable documentation" note** with the syntax, or a direct pointer to `RC-PIPE-13`: `[rand-number:n]`, `[rand-time:n]`, `[rand-utc-time:n]`, `[rand-time:n:value]`; no number = model 1. Confirmed in the 17.6.1 smart-variable help (its examples are `[rand-number:2]` and `[rand-time:2:value]`).

- [x] **Copying a project doesn't copy randomized values** *(15.8.4)* — `RC-RAND-03` §7.3, `RC-PROJ-05` if it covers Copy Project. Since 15.8.4, copying a project with all its records does not copy the randomization field's value for records that were already randomized. §7.3 offers "cloning the project and starting over" as an escape route; say that the clone starts with those records un-randomized. Also below 15.8.4: Copy Project could fail outright (redirect to Home) when randomization was used with PDF Snapshots or e-Consent.

- [x] **Allocation additions are append-only** — `RC-RAND-03` §7.1. FAQ: in production the allocation tables lock; an admin can append rows but cannot change rows already there. §7.1 says "appends" but not that existing rows are immutable (the per-slot actions in §7.2 are the only way to change a slot).

- [x] **Randomization form recurring at later events** *(field)* — `RC-RAND-03` §9 or `RC-RAND-01` §3. When the instrument holding the randomization field is also designated on later events (yearly visits, etc.), reports and logic must read the field from the randomization event. An empty or `0` value on a later event otherwise marks a randomized participant as "not randomized". Seen on a production trial's tracker.

---

## P3 — Minor / cosmetic

- [x] **Dashboard CSV Export** *(17.3.0)* — `RC-RAND-03` §5: a CSV Export button sits above the dashboard table.
- [x] **Randomize result dialog** *(field, 17.5.8)* — `RC-RAND-03` §3.1: after confirming, the result message ("… was randomized … assigned the value …") has its own Close button inside the dialog content, not in the button bar. Matters for anyone scripting UAT against the form.
- [x] **Log entry carries the allocation row's primary key** *(17.5.7)* — `RC-RAND-03` §7 (admins): the randomization log entry now includes the primary key of the allocation-table row that was assigned; not visible to normal users, useful when querying the log table.
- [x] **No limit on the number of models** — `RC-RAND-02` §1 "A note on multiple randomization models" (FAQ).
- [x] **Mobile App** — `RC-RAND-01` or `RC-RAND-03`: one line pointing to `RC-MOB-01` (which already lists randomization as unsupported). FAQ reason: the app works offline and can't reach the allocation table, so the Randomize button isn't shown.
- [x] **Saving the model erases test data in the randomization variable** — `RC-RAND-02` step 8d already says so; mirror it in `RC-RAND-01` §3 "Randomization Model" so it's visible before setup.
- [x] **Export dialog cites the randomization publication** *(15.5.0)* — `RC-RAND-03` or `RC-EXPRT-01`: with randomization set up, the data export dialog mentions the REDCap randomization paper that may need citing in manuscripts.
- [x] **Multi-Language Management covers randomization** *(17.5.4)* — `RC-MLM-01`, if it lists covered features.
- [x] **ACG CSV import showed randomization privilege changes wrongly** *(below 16.1.0)* — the Access Control Groups article, version caveat: the review dialog misreported API and Randomization privilege changes.

---

## Gotchas (bug fixes) → `RC-RAND-03` §3a or the relevant article

Standard versions shown; add LTS equivalents when applying.

- [x] **Admin Auto-fill filled the randomization field** *(below 15.6.0)* — using Auto-fill on a form holding the randomization field gave it a value and could disrupt allocation for that record. Worth a line in §3a: a test record with a value no allocation explains may come from this.
- [x] **Strata failing a real-time Data Quality rule** *(below 15.5.5)* — randomization could fail and leave the record in an inconsistent state if a stratum value broke a custom DQ rule with real-time execution. §3a, plus a pointer in the DQ real-time execution article.
- [x] **Missing Data Codes offered as DAG choices** *(below 15.6.1)* — with DAGs and Missing Data Codes, the randomization dialog's DAG drop-down listed the missing-data codes as choices.
- [x] **"Randomize record" log events survived Erase all data** *(below 15.7.0)* — with automatic triggers, erasing all data in development (or deleting all records on the move to production) left the randomization log events behind. Relevant to the §3a advice to reconcile the log against the allocation table.
- [x] **False error under the strata drop-down** *(below 16.0.5)* — creating a stratified model in a longitudinal project could show a spurious error under the strata field selector. `RC-RAND-02` step 8b.
- [x] **Wrong error viewing allocations in Analysis/Cleanup** *(below 17.6.0)* — viewing an allocation table in Analysis/Cleanup status showed the wrong explanation of why it was blocked. `RC-RAND-03` §7, or `RC-PROJ-01` under Analysis/Cleanup.

Already covered elsewhere and needing no new text: randomize-and-lock partial randomization (17.4.1 gotchas §F, as 15.5.23; Standard fix 15.9.2) and strata label clicks (§F, as 16.0.23; Standard fixes 17.0.2 and 17.0.3).

---

## Metadata

- [x] `RC-RAND-01`, `RC-RAND-02`, `RC-RAND-03`, `RC-PIPE-13`: set **Verified Against** to 17.6.1 (Standard) once the items above are applied, noting which sources were captured (Help & FAQ and smart-variable help — captured; Randomization pages themselves — not re-captured). Bump **Version** and **Last Updated**.
- [x] `RC-RAND-03` §11 "Version & Change Notes": its "Section 4.2 (automatic trigger behavior)" reference points at the wrong section — trigger behaviour is §3.2.

---

## No doc impact

- 17.5.7 security fixes that list Randomization among many affected areas (CSRF, authorization, rate limits on randomization previews, CSV/XML output injection) — no user-visible behaviour to document beyond "upgrade".
- 17.1.4 — allocation upload error message not shown correctly.
- 17.0.6 — fatal error when an External Module calls the `redcap_module_randomize_record` hook.
- 15.7.0 — fatal error exporting an allocation file in edge cases.
- 15.5.6 — faster upload of large allocation tables.
- 17.0.0 — the Project Migration Tool (REDCap+) migrates randomization assignments and allocation tables; already in `RC-PLUS-02`, so only check that the RC-RAND articles' "cloning" advice links to it as the way to keep randomization when moving instances.

# Claude Skills Review — 2026-10-09

> **Status (2026-10-09):** all findings below were worked through on branch `skills-cleanup`. The 13 skills became 11 (the three syntax skills merged into `redcap-syntax`); data dictionary code is shared via `redcap-data-dictionary/scripts/dd_common.py`; codebook-reader is PDF-only; connector safety rules live in `CONNECTOR-RULES.md`. Skills are installed as junctions in `~/.claude/skills`. This file is kept as the record of what was found.

This is a review of the 13 skills in `claude skills/`, done before installing them into Claude Code (`~/.claude/skills`). Each finding was checked against the KB in `kb/`. The scripts were run on Windows with Python 3.14 against test CSVs (BOM, CRLF line endings, quoted commas, checkbox, matrix, a 200 KB HTML label, API-style headers). No repo files were changed during the review.

Tags: **[Bug]** wrong output, a crash, or a mistake in the REDCap facts · **[Cleanup]** stale, duplicated or unclear · **[Enhancement]** worth adding.

## Summary

| Skill (folder) | Verdict | Main issue |
|---|---|---|
| kb-search | Minor cleanup | Cowork path; the domain table covers only 16 of 43 domains; the trigger is too broad |
| kb-creation (`redcap-kb-builder`) | Needs rework | The article template no longer matches the real articles; Cowork/Mac paths; points to a skill that doesn't exist |
| kb-update (`redcap-kb-updater`) | Needs rework | Cowork paths; never regenerates `kb (YAML)/`; uses the wrong Last Updated format |
| redcap-syntax-builder | Minor cleanup | Wrong rule for `+` with blanks; uses datediff for age; `'today'` unquoted |
| redcap-syntax-fixer | Minor cleanup | Same facts wrong; suggests a `NOT` keyword that doesn't exist |
| redcap-syntax-reader | Minor cleanup | Same facts wrong; its trigger overlaps the fixer |
| redcap-data-dictionary | Minor cleanup | Wrong descriptions of several action tags (e.g. `@NOMISSING`) |
| redcap-dd-builder | Needs rework | Drops alignment and some validation; `--append` produces CSVs REDCap rejects and can silently blank rows |
| redcap-dd-fixer | Needs rework | Its "fixes" break logic (lowercases names, breaks apostrophes); keeps a stale copy of the parser |
| redcap-codebook-reader | Needs rework | Tells users to download the wrong PDF; the ligature fix corrupts text; event data it promises is never filled in |
| redcap-longitudinal-builder | Needs rework | Wrong Arms header; puts `unique_event_name` in the Events CSV; crashes on Windows |
| redcap-longitudinal-structure | Minor cleanup | Rows with missing columns are silently dropped; crashes on Windows |
| redcap-project-analyzer | Needs rework | Uses connector names that don't exist; pastes the token into scripts; no explicit read-only rule |

## Problems shared across skills

1. **Leftovers from Claude.ai and Cowork.** Paths like `/sessions/.../mnt/...`, `/mnt/user-data/uploads|outputs`, `/Users/bas/...`, `/tmp`, `present_files`, `pip install --break-system-packages`, "download link". Relative paths like `kb (YAML)/` also stop working once a skill is installed under `~/.claude/skills`. **Fix:** use absolute Windows paths to the repo and Claude Code conventions.
2. **Windows console crash.** Every script that prints ⚠ ✓ → • crashes with `UnicodeEncodeError` when its output is piped, which is how Claude Code runs it (cp1252). `fix_dd.py` writes the CSV and *then* crashes, so you get a file but no change log. **Fix:** add `sys.stdout.reconfigure(encoding="utf-8")` at startup, or print ASCII only.
3. **Wrong facts copied into several skills.** The KB has since been corrected:
   - `+` treats a blank as 0. `sum()` returns blank only when every input is blank (16.0.41+). See RC-CALC-01 §6.3, lines 209–212, tested on 16.0.49.
   - For age, use `age_at_date()`, not `datediff(...,'y')` (RC-CALC-01 §11).
   - In `@CALCDATE`, write `'today'` / `'now'` in quotes (RC-AT-09 §4.4).
   - A plain `[checkbox]` pipes as comma-separated labels (RC-PIPE-02). It is not a pipe-delimited raw value.
4. **The same code and content kept in several places.**
   - Four separate DD readers, with three copies of `parse_choices` and `VALID_FIELD_TYPES`.
   - Two copies of `parse_dd.py`, the fixer's being older.
   - Two identical copies of `references/functions.md`.
   - About half the syntax content repeated across the three syntax skills.
5. **Triggers that overlap.** codebook-reader and data-dictionary; syntax-reader and syntax-fixer; longitudinal-structure and longitudinal-builder; kb-search ("when in doubt, use this skill") competes with everything.
6. **Inputs only accept CSV display headers.** Files using API column names (`field_name`, `select_choices_or_calculations`, …) fail with a misleading "Could not decode" error.
7. **Leftovers that should not be installed.** `*-workspace/` eval folders (committed to git, including full copies of KB articles), `*.skill` zip files, the empty `test_write` file. README:180 and :212 describe them wrongly ("Cowork skills").
8. **Missed chance to use the connectors.** Several skills ask for CSV uploads or ask the user questions that the REDCap MCP connectors could answer directly, read-only:
   - `export_metadata` (fields, types, checkbox codes)
   - `export_project_info` (is it longitudinal)
   - `export_arms`, `export_events`
   - `export_instrument_event_mappings`
   - `export_repeating_instruments_events`

   Any `import_*` should be offered only on dev, test and training connectors, with explicit confirmation, never on production connectors.

---

## KB maintenance

Shared: none of the three skills mentions `kb (YAML)/`. But `ServiceNow ETL/kb_to_servicenow.py:46` reads `kb (YAML)/`, so "run the ETL to check for synonym collisions" checks old data unless `convert_to_yaml_kb.py` is run first.

### kb-search — minor cleanup
- [Bug] `SKILL.md:13` uses a Cowork KB path. Hardcode `C:\Users\bd593\Documents\RCRAG\REDCap_KB_RAG\kb`.
- [Bug] `:86`, `:95` say "check REFERENCE-MAP", but `kb/KB-REFERENCE-MAP.md` is now an 11-line "Moved" stub.
- [Bug] `:59` refers to ⚠️ "unwritten" markers, which `meta/KB-INDEX.md` doesn't have.
- [Cleanup] `:17-36`: the domain table covers 16 of 43 domains (API, CC, PIPE, MYCAP and others are missing). Point to `meta/KB-INDEX.md` instead.
- [Cleanup] `:23`, `:44` say "RC-BL-01 through 04", but BL-05 exists. `:36-37` has no blank line after the table, so the next paragraph renders inside it.
- [Cleanup] `:4`: "When in doubt, use this skill" is too greedy. Add "do NOT use for" boundaries against the syntax and DD skills.
- [Enhancement] Use `meta/KB-KEYWORD-MAP.md` and a Grep over the Synonyms rows. Search `kb/` only, never `kb (YAML)/`, which holds duplicates.

### kb-creation (name `redcap-kb-builder`) — needs rework
- [Bug] `:2`: the name doesn't match the folder. `:3` refers to a `redcap-kb-refiner` skill that doesn't exist (the update skill is called `redcap-kb-updater`).
- [Bug] `:28-34`, `:42`, `:302-303`: Cowork paths, `/mnt/user-data/uploads`, `present_files`, and the Mac path `/Users/bas/...`. Reading a .docx needs the docx skill or pandoc.
- [Bug] `:106-120`: the template no longer matches the real articles (checked against RC-BL-02 and RC-CC-25):
  - Real articles start with a bold title line.
  - The header table has no `Field | Value` header row. The first row is `| **Article ID** | [self-link] |`.
  - Author is `[See KB-SOURCE-ATTESTATION.md](...)`.
  - Last Updated is `YYYY-MM`.
  - Cross-references are `[ID — Title](file.md)` links.
  - Headings are `## N. Title` with `---` separators, and definitions are bold paragraphs, not H2 headings (`:149`).
- [Bug] `:143` cites RC-VER-01, which doesn't exist. The article is RC-INFRA-03.
- [Bug] `:222`, `:224`: `KB-GAPS-TODO.md` is at the repo root, not in `kb/`. `:212`: the synonym-collision check needs the YAML regenerated first.
- [Bug] `:76`, `:408`: the skill tells Claude to edit its own slug table, so the installed copy and the repo copy will drift apart.
- [Cleanup] Stale details: `:102` calls the BL series "the most recent"; `:323` has an outdated .docx note; `:317` says KB-INDEX is alphabetical, but it isn't.
- [Cleanup] At 413 lines it is too long. Move the version caveats (`:168-190`), Synonyms (`:194-212`), No images (`:241-266`) and the slug table (`:350-413`) into `references/`. Add a real template file copied from RC-BL-02.
- [Enhancement] Add the after-writing steps: `convert_to_yaml_kb.py`, `add_crosslinks.py`, `build_dependency_graph.py`.

### kb-update (name `redcap-kb-updater`) — needs rework
- [Bug] `:2`: the name doesn't match the folder. `:15-18`, `:26`, `:101`: the same Cowork, Mac and docx path problems as kb-creation.
- [Bug] `:109`: wrong path for KB-GAPS-TODO.md. `:92` says "current year"; it should be `YYYY-MM`.
- [Bug] `:99`: there is no step to regenerate `kb (YAML)/` after an edit, even though README:162 says to.
- [Cleanup] It refers to the sibling skill three different ways (`:49`, `:120`, `:134`). `:122` finds the sibling by globbing for its SKILL.md; it should call the skill by name.
- [Cleanup] `:83` only updates "Related Articles". It should also update the header's Related Topics row.
- [Enhancement] When a title changes, grep `kb/` for the old title. Inbound links embed the title.

---

## Syntax

Shared:
- The two copies of `references/functions.md` (builder and fixer) are byte-identical, and both are out of date:
  - It says "as of 16.1.3".
  - It has the wrong `+` blank rule.
  - It doesn't say `sum()` of all-blank inputs returns blank.
  - It is missing `random(min,max)` (17.0.3+).
  - It is missing the `age_at_date` version caveat.
  - It lists minimum argument counts for `concat`/`concat_ws` that the KB doesn't support.
- **Recommendation:** merge the three into one `redcap-syntax` skill with build, fix and explain modes, plus `references/functions.md` and `references/syntax-core.md`. This fixes the trigger overlap and the drift between copies.

### redcap-syntax-builder — minor cleanup
- [Bug] `:145-147`, `:156-157` give the wrong `+` blank rule. To keep a total blank until all inputs are filled, use `if(isblankormissingcode(...) or ..., "", [a]+[b]+[c])`.
- [Bug] `:168-169` computes age with `datediff(...,'y')`. Use `age_at_date()`.
- [Bug] `:230`, `:254` write `today` unquoted in `@CALCDATE`.
- [Bug] `:110`, `:304` describe a plain `[checkbox]` as a pipe-delimited raw string.
- [Cleanup] Missing: `@CALCTEXT` apostrophe escaping (RC-AT-09 §3.4), smart variables as return values, and event smart-variable prefixes like `[previous-event-name][field]` (RC-PIPE-09).
- [Cleanup] The evals are only in `redcap-syntax-builder-workspace/`. Move them into the skill and drop the workspace and the `.skill` zip.
- [Enhancement] Step 2 (`:36-82`) asks 4+ questions up front. With a connector and project ID, it could answer them itself using `export_project_info`, `export_events`, `export_instrument_event_mappings`, `export_repeating_instruments_events` and `export_metadata`.

### redcap-syntax-fixer — minor cleanup
- [Bug] `:83` suggests a "NOT construct". REDCap has no NOT keyword; use `<>` (RC-BL-03).
- [Bug] `:167` contradicts itself about plain checkbox references. `:141` has `today` unquoted.
- [Cleanup] Missing checks:
  - Mixed AND/OR without parentheses (AND binds first, RC-BL-03).
  - `+` versus `sum()` blank handling.
  - `age_at_date()` without its 3rd argument, which fails silently on 17.0.6–17.1.1 (RC-CALC-01 §5.2).
- [Cleanup] `:209` hardcodes "Bas". The description (`:3-12`) has no "not for writing new or explaining" boundary.
- [Cleanup] Remove `redcap-syntax-fixer.skill` and `redcap-syntax-fixer-workspace/`. Keep `evals/`.
- [Enhancement] Step 4: check field names, event names, event designations and repeat setup against the live project, using the read-only connector exports.
- [Enhancement] Evals are missing cases for checkbox syntax, instance qualifiers, `'M'` vs `'m'`, AND/OR precedence and `+` with blanks.

### redcap-syntax-reader — minor cleanup
- [Bug] `:87` gives the wrong `+` blank rule. `:123`, `:130` have `today` unquoted.
- [Cleanup] The description (`:3-11`) overlaps the fixer: "whether it is correct", "why is my calculation blank" and "any snippet containing square brackets" will pull in fixer requests. Add explicit handoffs to the fixer and builder.
- [Cleanup] It has no functions.md, so it can't explain `find()` argument order, `log()` defaults, or the missing-data-code functions.
- [Cleanup] `:203` says instance qualifiers on non-repeating fields "return blank", while the fixer says they are "silently ignored". Pick one.
- [Cleanup] Add RC-BL-04, RC-PIPE-02 and RC-PIPE-09 to the article list (`:221-230`). The IDs already listed are valid.
- [Enhancement] It has no evals.

---

## Data dictionary

Shared:
- `--text` output crashes on Windows (see shared problem 2).
- It only accepts CSV display headers (shared problem 6).
- `import_metadata` has no dry-run mode and replaces the whole DD. So "validate by import" can only mean importing into a scratch project on dev or test.

**Recommendation:**
- Create one shared DD module (encoding fallback, `csv.field_size_limit`, header aliases, `parse_choices`, column constants) and use it from all four skills.
- Fold codebook-reader's CSV path into redcap-data-dictionary. Keep codebook-reader only for PDFs, or replace its PDF parsing with connector exports.
- Keep the builder and fixer as separate skills, sharing one validator.

### redcap-data-dictionary — minor cleanup
- [Bug] `parse_dd.py:45-76` describes several action tags wrongly:
  - `@NOMISSING` turns off missing-data codes for the field (RC-PROJ-04 §7.6). It does not force completeness.
  - `@CALCTEXT`/`@CALCDATE` go on text fields, and the value is stored (RC-AT-09).
  - `@HIDEBUTTON` hides the Today/Now button.
  - `@MAXCHOICE` caps how many records can choose an option.
  - `@BARCODE` doesn't exist.
  - `@HIDESUBMIT-SURVEY` comes from an external module.
- [Bug] The wrong `@NOMISSING` claim is repeated at SKILL.md:116, 124, 163 and `parse_dd.py:414`. The suggested "@NOMISSING on sub-options" fix for required checkboxes does nothing.
- [Bug] `parse_dd.py:336` only finds lowercase `[var]` references. The "arm" event check (`:338`, `:168`) skips variables like `[alarm]`.
- [Cleanup] "RC-AT-01 not yet written" (SKILL.md:128, `parse_dd.py:43`) is stale. Point to RC-AT-01 to 11 instead of keeping a hand-made list.
- [Cleanup] SKILL.md:53 (column H) is missing `signature`/`enhanced_signature` for file fields and `number` for sliders (RC-FD-08 §5.7).
- OK: the 18 columns and their order match RC-FD-08, and it handled the BOM, quoted commas and the 200 KB field.

### redcap-dd-builder — needs rework
- [Bug] SKILL.md:236 says `alignment`, but the script reads `custom_alignment` (`build_dd.py:250`), so alignment is silently dropped.
- [Bug] `build_dd.py:232` keeps validation only for text fields, which loses file `signature` and slider `number`.
- [Bug] `:233`: a number in the JSON (`"validation_min": 0`) crashes it.
- [Bug] `--append` adds rows at the end of the file. Adding fields to an existing form therefore splits the form, and REDCap rejects the upload.
- [Bug] `--append` onto a file with API headers writes the existing rows out blank (`:322`). This is silent data loss.
- [Bug] `read_existing_dd` has no `field_size_limit`, so it crashes on large HTML fields.
- [Cleanup] `url` (SKILL.md:161) isn't in the KB. The 26-character limit is a recommendation, not a hard rule (`build_dd.py:142`). The `kb (YAML)/` path is stale (SKILL.md:222).
- [Enhancement] Check matrix groups: rows contiguous, identical choices, radio/checkbox only.

### redcap-dd-fixer — needs rework
- [Bug] `fix_dd.py:257` lowercases variable names without updating references like `[Age]`. This breaks logic and contradicts SKILL.md:175 ("never rename").
- [Bug] `:127` replaces every `"` with `'`, which breaks apostrophes: `"O'Brien"` becomes `'O'Brien'`.
- [Bug] `:175`: the `@CALCTEXT` pattern stops at the first `)`, so in nested calls the outer quotes are never fixed.
- [Bug] `:188`: `normalize_yesno_flag` silently blanks any value it doesn't recognise. `:423`: `--output` with no value raises IndexError.
- [Bug] Its `parse_dd.py` is an older copy of the data-dictionary parser: no `field_size_limit`, unused constants, missing checks. Delete it and use the shared module.
- [Cleanup] `evals.json` points to `/sessions/...` files that don't exist. Eval 2 calls matrix fields "text".

### redcap-codebook-reader — needs rework
- [Bug] SKILL.md:59, :83 and `codebook_report.py:11` tell users to use "Download PDF of All Instruments". That export is the blank instrument forms. The codebook is under Project Setup or the left menu → Codebook (RC-FD-05 §3).
- [Bug] SKILL.md:175-177 promise event assignments and repeat setup from the PDF, but `instr["events"]` is never filled in and `is_repeating` is never set.
- [Bug] `:293-298`: the ligature fix corrupts text ("Thank you!" becomes "Thank youfi", "Item#3" becomes "Itemff3").
- [Bug] `:694`: the PDF choice parser drops negative codes (-77), glues letter codes onto the previous label, and loses min/max written inside the parentheses.
- [Bug] `:559` skips every field whose name ends in `_complete`. It should only skip `{form}_complete`.
- [Bug] `--llm-context` cuts off branching logic at 120 characters, labels at 100 and choices at 12, and keeps only tag names. That defeats its "every field" purpose.
- Not tested: PDF mode end-to-end (pdfplumber isn't installed and there is no sample PDF). The helper functions were unit-tested.

---

## Longitudinal and project analyzer

### redcap-longitudinal-builder — needs rework
- [Bug] `generate_longitudinal.py:307` crashes on Windows before any file is written (`:284`, `:286`, `:307`).
- [Bug] `:163`: the Arms header is `arm_num,arm_name`. It should be `arm_num,name` (RC-IMP-09 §2, RC-API-17).
- [Bug] `:194`: the Events CSV fills in `unique_event_name` and leaves out `custom_event_label`. `unique_event_name` should be left blank: RC-API-20:27 says a provided name is treated as modifying an existing event.
- [Bug] `:51-74`: no handling for truncation or name collisions in unique event names (REDCap appears to shorten the name part, so check this against a real export). Duplicate event names in the same arm are not detected (`:107`).
- [Bug] `:319` writes `Arms.csv` even for a single-arm project, which contradicts SKILL.md:226/232 and RC-IMP-09:27.
- [Bug] `:96-99` warns that missing arms "will be auto-added", but `:159` never adds them. `:222` writes mapping rows for unknown events with a blank `arm_num`.
- [Cleanup] SKILL.md:97 uses the relative path `kb (YAML)/`. `:221`, `:238` use `/tmp`. `:260` is a Cowork-ism.
- [Enhancement] Export the current arms, events and mappings before building, since a mapping upload replaces the whole mapping. Offer `import_*` only on dev, test and training connectors, with confirmation.

### redcap-longitudinal-structure — minor cleanup
- [Bug] `parse_longitudinal.py:43-46`: a short row raises `None.strip()`. The broad `except` reports it as an encoding error, the events file is dropped, and the report says "No structural issues".
- [Bug] `:115-124`: a decimal `day_offset` (28.5) is shown as Day 0, and its visit window is hidden.
- [Bug] `:380`, `:407`, `:436`, `:440`: Windows console crash.
- [Cleanup] `:126-133` drops `custom_event_label` and `event_id`. `:136` doesn't sort events on the same day by `unique_event_name`. `:367-373` is dead code. SKILL.md:45 uses a Cowork path.
- [Cleanup] Its triggers (SKILL.md:9-14) are too broad. Limit it to reading or explaining existing structure.
- [Enhancement] Accept JSON from the live exports (`export_arms`, `export_events`, `export_instrument_event_mappings`). The keys match the CSV columns.

### redcap-project-analyzer — needs rework
- [Bug] SKILL.md:62, :103-104 use connector names `redcap-prod`, `redcap-test` and `redcap-dev`. `redcap-prod` doesn't exist; real connector names live in the local connector map (`~/.claude/redcap-connectors.md`), outside the repo. The tool names it uses are correct.
- [Bug] `:64-65`, `:67-153` make raw Python `requests` the default in Claude Code. That puts the token in chat and in script text (`:71`, `:123`), which contradicts `:395`.
- [Bug] `:105` asks for the instance only "if ambiguous". It should always ask, show the API URL, and flag production instances.
- [Bug] Nothing forbids `import_*`, `delete_*` or `export_records`. Add an explicit read-only rule.
- [Bug] `:259` treats `purpose = 0` as "not set". 0 is probably Practice/Just for fun; confirm this (the KB doesn't list the codes).
- [Bug] `:255`: survey-enabled instruments can't be detected from `export_instruments`, so that check can't run as written.
- [Bug] `:229`: the field-reference regex misses `[field(1)]` and counts `[event_arm_1]` as a field.
- [Cleanup] `:124` uses `/tmp`. `:267` uses the relative path `kb (YAML)/`. `:302` says "download link". `:206-210` duplicates `:284-289`.
- [Enhancement] Call `check_connection` first. Use the connector's default token or a token passed per call, and never echo it.

---

## Suggested order of work

1. **Delete the leftovers:** the `*-workspace/` folders, `*.skill` zips, `test_write` and the fixer's `parse_dd.py`. Fix README:180 and :212.
2. **Fix the shared problems:** the UTF-8 stdout line in every script, absolute Windows paths, and removing the Cowork-isms.
3. **Correct the wrong REDCap facts** in the three syntax skills, `functions.md` and the action-tag table.
4. **Rework the dangerous ones before use:**
   - project-analyzer: connector names, token handling, read-only rule.
   - dd-fixer: renaming and quote replacement.
   - dd-builder: `--append`.
   - longitudinal-builder: headers.
5. **Consolidate:**
   - One `redcap-syntax` skill.
   - A shared DD module.
   - Fold codebook-reader's CSV path into data-dictionary.
   - Align the KB skills' names with their folders.
6. **Add the connector features** (read-only exports first).
7. **Install,** copying only `SKILL.md`, `scripts/`, `references/` and `evals/`.

# Writing Playwright tests for REDCap

Practical notes for writing automated browser tests (Playwright) against a REDCap
instance: where to find ready-made test specifications, how to set test projects up
quickly, how to read REDCap's pages reliably, and the gotchas that make tests flaky or wrong.

This folder sits outside the KB articles (`kb/`) on purpose: it is a working guide
for test authors, not an end-user article, and it is not fed to the RAG/ServiceNow pipeline.

> **Run tests only against a development or test REDCap instance**, never production.
> Tests create projects, records and users, and change project settings.

Where a statement below was checked on a live instance, it says so (REDCap v17.5.6 Standard,
October 2026). Everything else is drawn from the RSVC material and should be confirmed on your version.

---

## 1. Start from the RSVC feature tests

The REDCap Consortium's **Regulatory & Software Validation Committee (RSVC)** publishes
step-by-step test specifications for REDCap's core functionality. They are the best
starting point for any REDCap test: someone has already worked out the setup, the steps
and the expected results.

| Resource | What it is |
|---|---|
| [vanderbilt-redcap/redcap_rsvc](https://github.com/vanderbilt-redcap/redcap_rsvc) | Gherkin `.feature` files, one per functional requirement, plus the project XML and data dictionaries they import. `main` = the last validated LTS package; `staging` = work in progress. |
| [vanderbilt-redcap/redcap_cypress_docker](https://github.com/vanderbilt-redcap/redcap_cypress_docker) | The toolkit RSVC runs the features with (Cypress + a Dockerized REDCap with test accounts). Useful to see how steps are implemented. |
| RSVC validation package (per LTS release, on the REDCap Consortium site) | Functional Requirements Specification, execution report (which tests are automated, manual or N/A, with pass/fail), and a viewer per test. |
| Baker TA et al., *Consortium-Driven Rapid Software Validation for REDCap*, J Clin Transl Sci 2024, doi:10.1017/cts.2024.671 | Background on the method. |

**How the repo is organised**

- `Feature Tests/<Tier>/<Feature name>_<n>/<FRS ID> - <title>.feature` — e.g.
  `Feature Tests/B/Branching Logic_9/B.4.9.0100. - Branching Logic.feature`.
- `Files/` — the project XML files (`Project_4.9.xml`) and modified data dictionaries
  (`dictionaries/Project_4.9.modified.csv`) the scenarios import.
- Requirement IDs (`B.4.9.0100.`) tie a test back to the Functional Requirements
  Specification; scenario IDs add a suffix (`B.4.9.0100.100`).
- Tiers: **A** core, admin-level · **B** core, project-level · **C** non-core maintained
  by RSVC · **D** site-managed · **E** external modules (always the site's responsibility).

For the LTS 17.3 package, 336 requirements were listed: 280 tested automatically, 20 manually,
36 not applicable or redundant.

**What the features are — and are not.** They verify that a feature *works* (the
happy path plus logging). Branching logic, for example, is one requirement with two
scenarios: fields hide/show on a public survey and a data entry form, the erase prompt
appears, the editor and drag-and-drop builder work, and a Data Dictionary upload carries
logic. They do not probe edge cases (blank vs zero, checkbox comparisons, comments in
logic). Write those yourself — section 6 shows a pattern.

---

## 2. From a Gherkin scenario to a Playwright test

Two options:

1. **Plain Playwright tests**, using the `.feature` file as the specification. Simplest; recommended by default.
2. **Keep the Gherkin** and run it with [`playwright-bdd`](https://github.com/vitalets/playwright-bdd),
   writing each step definition once. Worth it when many RSVC scenarios will be reused as-is, or when
   non-developers read and review the scenarios.

Typical step → Playwright mapping:

| Gherkin step (RSVC wording) | Playwright |
|---|---|
| `I should see the field labeled "Name"` | `await expect(page.locator('#ptname-tr')).toBeVisible()` (row ids, see §4) |
| `I should NOT see the field labeled "Name"` | `await expect(page.locator('#ptname-tr')).toBeHidden()` |
| `I click on the button labeled "Save"` | `await page.getByRole('button', { name: 'Save' }).click()` |
| `I click on the link labeled "Designer"` | `await page.getByRole('link', { name: 'Designer' }).click()` |
| `I select the radio option "Choice101" for the field labeled …` | `await page.getByLabel('Choice101').check()` |
| `I should see "…"` | `await expect(page.getByText('…')).toBeVisible()` |
| `I create a new project … choosing file "Project_4.9.xml"` | do it through the API instead (§3) |
| `I login to REDCap with the user "Test_Admin"` | reuse a saved login session (§5) |

Example — the survey part of `B.4.9.0100.100` (field names from `Project_4.9.xml`; illustrative):

```ts
import { test, expect } from '@playwright/test';

test('B.4.9.0100.100 – hidden fields stay hidden on the public survey', async ({ page }) => {
  await page.goto(process.env.PUBLIC_SURVEY_URL!);   // fetched with the API (§3)
  for (const field of ['ptname', 'textbox', 'text2', 'notesbox']) {
    await expect(page.locator(`#${field}-tr`)).toBeHidden();
  }
  await page.getByLabel('Choice101').check();         // radio_button_manual = 101
  await expect(page.locator('#descriptive_text_file-tr')).toBeVisible();
});
```

---

## 3. Set test projects up through the API, not the UI

Clicking through *New Project → upload XML → designate instruments* is slow and the
most fragile part of any UI test. Do setup through the REDCap API and keep the browser for
what can only be seen on a page.

- **Create a project**: `content=project` with a **Super API token** creates a project
  and returns that project's own API token. A super token can only create projects; everything
  else needs the project token. A project can also be created from an ODM/XML file
  (the `odm` parameter), including survey settings.
- **Load fields**: `content=metadata` import. *Verified 17.5.6:* the JSON import is read **by column
  position**, so every Data Dictionary column must be present, in Data Dictionary order —
  `field_name, form_name, section_header, field_type, field_label, select_choices_or_calculations,
  field_note, text_validation_type_or_show_slider_number, text_validation_min, text_validation_max,
  identifier, branching_logic, required_field, custom_alignment, question_number, matrix_group_name,
  matrix_ranking, field_annotation`. Leaving one out shifts the rest and produces confusing errors.
- **Load records**: `content=record` import. Checkbox options are separate columns: `cond___1`, `cond___2`.
- **Get a survey link**: `content=surveyLink` (per record/instrument) or the public survey URL —
  lets you test survey pages without logging in.
- **Clean up**: the API **cannot delete projects**. Reuse long-lived test projects (re-import their
  metadata and records at the start of a run) instead of creating one per test, or delete them in the UI.
- Keep tokens out of the code: read them from environment variables or a secret manager at run time.

---

## 4. Reading REDCap pages reliably

- **Field rows** (*verified 17.5.6*): on data entry forms each field is a table row with id
  `<field_name>-tr` (e.g. `#age-tr`). Branching logic hides the row with `display:none`, so
  `toBeHidden()` / `toBeVisible()` on the row is a dependable visibility check — including for
  descriptive fields, which makes a descriptive field with branching logic a cheap "probe" for a
  logic expression.
- Many visibility checks can be done in one call on the page:
  `page.$$eval('tr[id$="-tr"]', rows => rows.filter(r => getComputedStyle(r).display !== 'none').map(r => r.id))`.
- Prefer accessible locators (`getByRole`, `getByLabel`, `getByText`) for buttons, links and choice
  labels; use the `-tr` ids for whole-field visibility. Inspect your version's DOM before relying on
  input names for radio/checkbox controls — check them rather than assuming.
- Pages run JavaScript after load (branching logic, calculations, action tags). Use Playwright's
  auto-waiting assertions (`expect(...).toBeHidden()`) rather than reading state immediately.

---

## 5. Logging in

- **Public surveys need no login** — the quickest way to test survey-side behaviour.
- For everything else, log in **once** in a setup project and reuse the saved session
  (`storageState`) across tests. Use a dedicated test account on the test instance — never a
  personal or production account — and supply its credentials through environment variables or CI secrets.
- Test accounts with different user rights (designer, data entry only, DAG-restricted) let the same
  tests check permission behaviour.

---

## 6. Pattern: logic truth tables (server and client)

For testing logic expressions themselves (branching logic, filters, alerts), a data-driven table
works better than one scripted scenario per expression:

1. Import a handful of records that cover the interesting states: a value, zero, blank, a form
   that was never saved, checkboxes explicitly `0`.
2. For each expression, list the records the documentation says it is true for.
3. Check it in up to four places:
   - **Server-side** — API `content=record` export with `filterLogic=<expression>` (the same engine as
     reports, alerts and survey invitations).
   - **Import validation** — the metadata import with the expression as `branching_logic` (the same
     checks as a Data Dictionary upload).
   - **Online Designer validator** — `POST Design/logic_validate.php?pid=<pid>` with `logic=<expression>`,
     from a logged-in page; returns `1` when valid. It only validates, it saves nothing.
   - **On the form** (Playwright) — a descriptive field per expression with that branching logic; open
     each record's form and read which `-tr` rows are visible.
4. Compare. Server and form can disagree (see §7), which is exactly what this catches.

---

## 7. Gotchas that break tests (or make them lie)

*Verified on 17.5.6 unless noted.*

- **Invalid `filterLogic` returns every record, with no error.** A typo in a filter makes an export
  look like "everything matched". Validate the expression first (logic validator or a metadata import)
  before trusting a filtered result. An unknown variable name, by contrast, returns no records.
- **Native browser dialogs.** Some REDCap errors are `alert()` popups, not page elements — e.g. the
  Online Designer rejecting invalid branching logic on Save. Playwright dismisses dialogs automatically
  unless you handle them, so the test sees "nothing happened". Register
  `page.on('dialog', d => { messages.push(d.message()); d.accept(); })` and assert on the message.
- **The erase prompt** (from RSVC B.4.9.0100.100): on a data entry form, when branching logic is about to
  hide fields that already hold values, REDCap shows a dialog ("…requires that some fields be hidden from
  view") with **Erase** / cancel. On surveys there is no prompt. A test entering data that triggers hiding
  must answer it.
- **Comments in logic** are accepted only on a line of their own. A comment after logic on the same line
  (`[age]>=18 // adult`) is a syntax error for the validator and the metadata import, and makes a
  filter match every record.
- **Checkbox options compared to blank differ by context.** `[cb(1)]=''` is true for unchecked options on
  the data entry form but never true server-side. Test unchecked with `='0'`.
- **Two blank fields are equal**: `[a]=[b]` is true when both are empty.
- **Capitalised variable names** (`[Age]`) are rejected by both the Online Designer and the metadata import.
- **Data Dictionary/API import is stricter than the Online Designer** in places: an apostrophe inside a
  quoted comparison value (`[site]="O'Brien"`) passes the designer's validator but fails the import.
- **Leave-page prompts.** Navigating away from a form with unsaved changes raises a "Leave without saving
  changes" dialog (RSVC steps click through it explicitly).

---

## 8. Checklist for a new test

- [ ] Find the closest RSVC feature (by functional area or requirement ID) and read its scenarios.
- [ ] Reuse its project XML / dictionary, or define a minimal one for the test.
- [ ] Set up the project and records through the API; reuse a long-lived project where possible.
- [ ] Log in once with a test account, or use a public survey link.
- [ ] Assert on `-tr` rows for visibility; accessible locators for actions.
- [ ] Handle native dialogs and the erase / leave-page prompts.
- [ ] Record the REDCap version tested; re-run after upgrades.

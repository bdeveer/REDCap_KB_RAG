

**Form Display Logic**

| **Article ID** | [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md) |
|---|---|
| **Domain** | Form Display Logic |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights to configure |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Form Display Logic behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md); [RC-PIPE-05 — Smart Variables: User](RC-PIPE-05_Smart-Variables-User.md); [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md); [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) |
| **Synonyms** | what is form display logic; control which instruments a user can open; gray out or hide a form conditionally; enable a form only when a condition is met; form display logic vs branching logic; data entry equivalent of survey queue; disable forms until prerequisites are met; how to set up form display logic |

---

## 1. Overview

Form Display Logic is an advanced feature that allows project designers to control which data entry instruments are accessible to users based on conditional logic. It is the data entry equivalent of the Survey Queue: just as the Survey Queue controls which surveys a participant can access and in what order, Form Display Logic controls which instruments a data entry user can open and when.

When a condition is met, the form is **enabled** and accessible. When it is not met, the form is **disabled** — grayed out and unclickable — but still visible by default. Optionally, disabled forms can be hidden from the left-hand menu and the Record Home Page.

**This article is written for project designers** who configure Form Display Logic. Data entry users only experience its effects: they see forms that are enabled, grayed out, or hidden depending on what the designer has set up. Designers configure Form Display Logic in the **Online Designer**, using the **Form Display Logic** button (a dropdown with **Edit Form Display Logic**, **Upload Form Display Logic Setup (CSV)** and **Download Form Display Logic Setup (CSV)**) — not in Project Setup. The CSV download and upload are useful for bulk editing or reuse across projects.

---

## 2. Key Concepts & Definitions

**Form Display Logic**

Conditional logic applied at the instrument level. A condition (written in standard REDCap logic syntax) determines whether a specific form-event combination is enabled or disabled for data entry.

**Enabled vs. Disabled**

When a form's condition evaluates to **true**, the form is enabled — users can open and edit it normally. When the condition evaluates to **false**, the form is disabled — it is grayed out and inaccessible for data entry, but still visible on the page.

**OR Rule for Multiple Conditions**

A single form can appear in multiple condition rows. If the same form is listed more than once, **the form will be enabled if at least one of its conditions evaluates to true**. Multiple conditions for the same form combine with OR logic, not AND.

**Evaluation Context (Event and Instance)**

REDCap's own help text describes Form Display Logic as evaluated at the record level. In practice, each condition is evaluated in the context of the form it controls — that form's **event** and, for repeating events or repeating instruments, its **instance**. This means:

- Instance smart variables such as `[current-instance]` and `[previous-instance]` work, for example `[field][previous-instance] = "1"` or `[field2][current-instance] > 30`. Forms in individual instances can be enabled or disabled independently rather than uniformly across the record. This applies to repeating events (15.3.2+) and to repeating instruments.
- For anything that must be checked **record-wide** — the same answer no matter which event or instance the form sits in — use explicit `[event_name][field_name]` references (e.g., `[consent_arm_1][consent_yn]`), so the result does not depend on where the form is.

> **MyCap exception:** when a condition applies to MyCap tasks, it is evaluated at the **first instance**. If a MyCap condition must look at the most recent instance of a repeating form, use `[last-instance]` explicitly.

---

## 3. Where Form Display Logic Takes Effect

Form Display Logic affects the data entry user interface in three locations:

- **Record Status Dashboard** — disabled forms show a grayed-out dot; users cannot click through to the instrument.
- **Record Home Page** — disabled forms are grayed out in the instrument list.
- **Left-hand Data Collection menu** — disabled forms appear in the form list but cannot be navigated to.

It is also enforced beyond the links themselves:

- **Direct links.** Opening a disabled form by a bookmarked or pasted link does not open it — REDCap sends the user to the next enabled form, or to the Record Home Page.
- **New repeating instances.** While the condition is false, users cannot add a new instance of a repeating form.
- **Everyone, including administrators.** Form Display Logic applies to every user, REDCap administrators included. It only ever removes access: it never grants access to an instrument that the user's rights deny.
- **Not in Draft Preview.** Form Display Logic is switched off while a user is in Draft Preview, so test it on real records rather than in Draft Preview.

> **Version caveat (17.6 Standard; not in 17.3 or 16.0 LTS):** embedded repeating-instance tables respect Form Display Logic only on the 17.6 Standard line. On LTS, do not rely on Form Display Logic to keep instances of a disabled form out of those tables; check them with a test user, or upgrade.

> **Important:** Form Display Logic does **not** affect data imports. Imported records bypass all Form Display Logic and write directly to the database regardless of whether a form would be disabled in the UI. Form Display Logic also has **no effect on the Survey Queue** and does **not** block survey links or survey invitations — a participant with a link can still open the survey. It affects surveys only through **Survey Auto-Continue**, for conditions whose **Apply to** setting includes **Survey Auto-Continue** (see Section 4).

---

## 4. Configuring Form Display Logic

Form Display Logic is managed in the **Online Designer**: click the **Form Display Logic** button and choose **Edit Form Display Logic**. Each condition defines the forms (and, in longitudinal projects, events) it controls, the logic, and an **Apply to** setting with up to three options: **Data Entry Forms**, **Survey Auto-Continue** and **MyCap Tasks**. **Apply to** is set per condition. The **Survey Auto-Continue** option appears only when surveys are enabled in the project, and **MyCap Tasks** only when MyCap is enabled.

In the CSV (see Section 9), each row carries these columns:

| Column | Description |
|---|---|
| `form_name` | The internal instrument name (as it appears in the Data Dictionary). |
| `event_name` | **Longitudinal projects only.** The event to which this condition applies. **Leave blank to apply the condition to all events** where the form appears. Classic projects have no `event_name` column. |
| `control_condition` | The REDCap logic expression. When this evaluates to true, the form is enabled. |
| `apply_to_data_entry` | `y` or `n` — whether this condition affects the standard data entry UI (**Data Entry Forms**). |
| `apply_to_survey_autocontinue` | `y` or `n` — whether this condition affects Survey Auto-Continue behavior. |
| `apply_to_mycap_tasks` | `y` or `n` — whether this condition affects MyCap task availability. |

Conditions use the same logic syntax as branching logic and calculated fields. See [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) for the full syntax reference.

---

## 5. Optional Settings

Two optional global settings modify how disabled forms are displayed:

**Keep forms enabled if they contain data**

This setting is **off by default**. When enabled, it overrides Form Display Logic for forms that already have data — only empty forms (those with a gray status icon) will be disabled. Any form that contains at least one saved value remains accessible even if the condition is false. This protects against accidentally locking users out of partially completed forms when logic conditions change.

**Hide forms that are disabled**

When enabled, disabled forms are hidden rather than grayed out in the left-hand Data Collection menu and on the Record Home Page. They are **not** hidden on the Record Status Dashboard, where they still show as grayed out. This reduces visual clutter for users who should not interact with certain forms at all, rather than simply being prevented from entering data.

These two settings can be combined: you can hide disabled forms while keeping data-containing forms accessible.

### 5.1 Where Each Condition Applies *(15.7.3+)*

Form Display Logic can drive three separate surfaces: **data entry forms**, **Survey Auto-Continue**, and **MyCap**. Which conditions apply to which surface depends on your version.

| Version | Behaviour |
| --- | --- |
| Below 15.7.3 | Survey Auto-Continue and MyCap were **project-wide toggles**. Enabling either applied it to **every** FDL condition in the project — all or nothing |
| 15.7.3 and higher | Each condition is set **individually** to apply to data entry forms, to Survey Auto-Continue, and/or to MyCap |

> **Note on upgrading:** if the Survey Auto-Continue or MyCap settings were enabled before the upgrade, REDCap applied that setting to **every** FDL condition in the project during the upgrade, preserving the previous behaviour. That is the correct migration, but it means a project upgraded from below 15.7.3 starts with the setting switched on everywhere — review the conditions individually if you want the finer control the feature offers.

MyCap support arrived slightly earlier as the project-wide **"Enable support for MyCap App"** checkbox in the FDL setup dialog (15.5.1), which is a practical way to disable specific MyCap tasks conditionally.

**How MyCap uses the conditions.** If no condition in the project applies to MyCap Tasks, Form Display Logic has no effect in MyCap. Once **any** condition applies to MyCap Tasks, MyCap uses only the MyCap-flagged conditions: a task is shown only if one of its MyCap-flagged conditions is true, and a task whose form has no MyCap-flagged condition is not shown. A condition with MyCap Tasks set to `n` never makes a task visible. To keep a task always available alongside other MyCap conditions, give it its own condition with MyCap Tasks set to `y` and an always-true logic such as `[record_id]<>""`.

> **Version caveat (≤16.1.7, MyCap only):** With an instrument enabled for MyCap appearing in **multiple** FDL conditions, FDL stopped working for that MyCap task in the app (fixed 16.1.8), and in longitudinal MyCap projects with many events the same situation could make publishing a new MyCap version fail (fixed 17.1.1).

> **Version caveat (≤16.0.3, Survey Auto-Continue):** With Survey Auto-Continue enabled across multiple sequential surveys, participants taking surveys back to back could have surveys **skipped** by FDL when they should not have been — particularly within a repeating event. A first fix in 15.5.27 LTS / 16.0.2 Standard made the problem worse in some cases before it was properly resolved in 16.0.4.

> **Version caveat (17.4.0+ Standard; not in 17.3 LTS):** the form pickers in the Form Display Logic dialog are searchable (type to filter), which makes instruments easier to find in projects with many forms. On the 17.3 LTS line they are plain multi-select lists; scroll the list, or use the CSV download to review which forms each condition covers.

---

## 6. Using Smart Variables in Conditions

Form Display Logic supports smart variables in its condition expressions, making it possible to control form access based on who is currently logged in — not just what data is in the record.

The most commonly used user smart variables in Form Display Logic are:

| Smart Variable | Returns | Common Use |
|---|---|---|
| `[user-name]` | The logged-in user's REDCap username | Restrict a form to specific named users (e.g., PI only) |
| `[user-role-id]` | Numeric ID of the user's assigned role | Block or allow access by role |
| `[user-role-name]` | Unique role name within the project | Preferred over role ID if the project may be copied |
| `[user-dag-name]` | Unique name of the user's Data Access Group | Site-specific form access in multi-site projects |

> **Critical — `[user-role-id]` breaks when a project is copied:** Role IDs are unique across the entire REDCap installation and change when a project is copied. After a copy, the old IDs match nobody:
>
> - **Allow-list conditions** (`[user-role-id]='X'`) stop enabling the form for anyone.
> - **Exclusion conditions** (`[user-role-id]<>'X'`) stop excluding anyone — so blinded users, for example, **gain access** to forms they were meant to be kept out of, with no error or warning.
>
> Use `[user-role-name]` (the unique role name, which is kept when roles are copied with the project), or re-check every role condition after each copy.

See [RC-PIPE-05 — Smart Variables: User](RC-PIPE-05_Smart-Variables-User.md) for the full reference.

---

## 7. Limitations

**Evaluation depends on where the form sits.** Conditions are evaluated in the form's own event and instance (see Section 2), so the same unqualified field reference can give different results in different events or instances. For record-wide checks, reference data in a specific event using the `[event_name][field_name]` syntax (e.g., `[consent_arm_1][consent_yn]`).

**No effect on data imports.** Form Display Logic operates only in the data entry UI. Any data imported via the Data Import Tool or API bypasses Form Display Logic entirely.

**No effect on Survey Queue, survey links or invitations.** The Survey Queue evaluates its own conditions independently. Form Display Logic cannot prevent a survey from appearing in a queue, and it does not block a participant from opening a survey link or invitation. It affects only Survey Auto-Continue, for conditions whose **Apply to** setting includes **Survey Auto-Continue**.

**Forms remain visible when disabled.** By default, disabled forms are grayed out but still visible. The "Hide forms that are disabled" optional setting hides them in the left-hand menu and on the Record Home Page, but they still show (grayed out) on the Record Status Dashboard.

---

## 8. Real-World Examples

The following patterns are drawn from actual project implementations, with usernames and role IDs replaced by generic placeholders. They are shown as rows of a **longitudinal** project's CSV; in a classic project the `event_name` column does not exist.

---

### Example 1: Consent Gate

**Goal:** Most data collection forms should be inaccessible until the participant has consented.

```
form_name,event_name,control_condition,...
adverse_event,,[consent_arm_1][consent_yn]='1',...
demographics,screening_arm_1,[consent_arm_1][consent_yn]='1',...
blood_labs,baseline_arm_1,[consent_arm_1][consent_yn]='1',...
```

When `event_name` is blank, the condition applies to all events where the form appears. This is a common gate pattern: lock all forms until a single consent field is checked.

---

### Example 2: Post-Randomization Gate with Role-Based Blinding

**Goal:** Follow-up assessment forms should only be enabled after the participant has been randomized. Additionally, certain user roles (e.g., blinded coordinators) must be excluded from the condition so they remain blocked even after randomization.

```
form_name,event_name,control_condition,...
moca,3_month_arm_1,"[randomization_arm_1][rand_group]<>'' and [user-role-id]<>'ROLE_BLIND_A' and [user-role-id]<>'ROLE_BLIND_B'",...
event_log,4week_call_arm_1,"[randomization_arm_1][rand_group]<>'' and [user-role-id]<>'ROLE_BLIND_A' and [user-role-id]<>'ROLE_BLIND_B'",...
```

This pattern combines a data-driven condition (`rand_group<>''`) with user role exclusions. Blinded users are kept locked out even when data conditions are met.

> **Critical:** exclusions written with `[user-role-id]` stop working if the project is copied — the blinded roles get new IDs and gain access. Write them with `[user-role-name]` instead (see Section 6).

---

### Example 3: Treatment-Arm–Specific Forms

**Goal:** Certain forms (e.g., an inpatient exercise log) only apply to participants in a specific treatment arm and should be disabled for controls.

```
form_name,event_name,control_condition,...
inpatient_exercise,,[randomization_arm_1][rand_group]='2',...
home_visit,,[randomization_arm_1][rand_group]='2',...
outpatient_exercise,,[randomization_arm_1][rand_group]='2',...
```

These forms are disabled for everyone until randomization happens and enabled only for participants assigned to group 2.

---

### Example 4: Complex Eligibility Gate

**Goal:** The randomization form should only become accessible after all eligibility criteria are confirmed and consent is recorded.

```
form_name,event_name,control_condition,...
randomization,randomization_arm_1,"[screening_arm_1][eligcks_age] = '1' and
[screening_arm_1][eligcks_ejectfract] = '1' and
(sum([screening_arm_1][eligcks_symptoms(1)],[screening_arm_1][eligcks_symptoms(2)])>=1) and
[consent_arm_1][consent_yn]='1' and
[consent_arm_1][consent_date]<>'' and
[screening_arm_1][sppb_gait_score]>=1",...
```

Complex multi-field eligibility conditions using `sum()` and inequality operators can be used to create sophisticated gates that ensure data integrity before a critical form becomes available.

---

### Example 5: Named-User Allow-List

**Goal:** A finalization checklist form should only be accessible to the PI and designated coordinators, regardless of role.

```
form_name,event_name,control_condition,...
finalize_checklist,event_forms_arm_1,"[user-name]='pi.researcher' or [user-name]='coord.site1@example.org' or [user-role-id]='ROLE_PI_EQUIV'",...
```

This approach allows specific users by username and also includes a role-based fallback. Note: prefer `[user-role-name]` over `[user-role-id]` if the project may be copied in the future.

---

### Example 6: Sequential Form Unlock

**Goal:** A study completion form should only become available after an intervention completion form is fully saved.

```
form_name,event_name,control_condition,...
study_completion,event_forms_arm_1,"[interv_reas]<>'' and [interv_date]<>'' and [intervention_completion_complete]='2'",...
```

The `_complete` field for any instrument is a standard REDCap completion status field (0 = Incomplete, 1 = Unverified, 2 = Complete). This pattern chains form completion to form access.

---

### Example 7: Always-On Baseline (Enroll in FDL Without Restricting)

**Goal:** Include forms in Form Display Logic without actually restricting data entry access or Survey Auto-Continue. The forms should always be accessible for all records.

Raw file content (longitudinal project — the six-column header applies to longitudinal projects only):

```
form_name,event_name,control_condition,apply_to_data_entry,apply_to_survey_autocontinue,apply_to_mycap_tasks
demographics,,"[record_id]<>""""",y,y,n
contact_info,,"[record_id]<>""""",y,y,n
```

In a spreadsheet each condition cell reads `[record_id]<>""`, which evaluates to true for every record because `record_id` is always populated. This is effectively a permanent-enable condition. It is useful when you want to:

- Enroll a form in Form Display Logic without restricting access in data entry or Survey Auto-Continue.
- Establish a baseline entry for a form that you plan to tighten later, without changing the CSV structure at that point.

These rows have MyCap Tasks set to `n`, so they do **not** make anything visible in MyCap. If any other condition in the project applies to MyCap Tasks, MyCap uses only the MyCap-flagged conditions, and a task whose only conditions are `n` for MyCap is not shown. To keep a MyCap task always available, set `apply_to_mycap_tasks` to `y` on its always-true row (see Section 5.1).

> **Note:** In the raw CSV file every `"` inside a cell is doubled and the cell is wrapped in quotes, so `[record_id]<>""` is written `"[record_id]<>"""""`. A spreadsheet shows it correctly; see Section 9 before editing the file in a plain text editor.

---

## 9. The Form Display Logic CSV

Form Display Logic can be downloaded as a CSV and uploaded to another project or used for bulk editing. The columns depend on the project type:

- **Longitudinal projects:** six columns — `form_name`, `event_name`, `control_condition`, `apply_to_data_entry`, `apply_to_survey_autocontinue`, `apply_to_mycap_tasks`.
- **Classic (non-longitudinal) projects:** five columns — the same list without `event_name`. A file that contains an `event_name` column is rejected in a classic project.

**Download:** In the Online Designer, click **Form Display Logic** → **Download Form Display Logic Setup (CSV)**.

**Upload:** Edit the file in a spreadsheet application, then use **Form Display Logic** → **Upload Form Display Logic Setup (CSV)**. This is the fastest way to set up Form Display Logic in a new project that mirrors an existing one. When uploading:

- The upload **replaces all existing conditions** in the project; it does not add to them. Download the current setup first if you may need it back.
- The two optional settings (**Keep forms enabled if they contain data**, **Hide forms that are disabled**) are not in the CSV; set them in the dialog.
- Flags must be a lowercase `y`. Anything else — including `Y` or `yes` — counts as `n`.
- A row with all three flags `n` is rejected.
- Rows with identical condition text are combined into one condition covering all their forms and events.
- Uploading a file with no condition rows offers to delete all existing conditions.

**One row per form-event-condition combination.** A single form can appear in multiple rows (different events or different conditions). Remember: multiple rows for the same form combine with OR logic — the form is enabled if any condition is true.

**Quotes in the raw file.** The file follows standard CSV quoting: every `"` inside a cell is doubled, and the cell is wrapped in quotes. So the condition `[record_id]<>""` is written `"[record_id]<>"""""` in the raw file. Spreadsheet applications (Excel, Google Sheets, LibreOffice) handle this transparently and show the correct expression. Hand-typing the quotes in a plain text editor is error-prone — a wrong count makes the upload fail or changes the logic — so download the file and edit it in a spreadsheet instead.

**Delimiter.** The file uses the CSV delimiter set in your REDCap user profile preferences (comma by default). Upload with the same delimiter.

**Copying projects.** Copy Project has a Form Display Logic option that copies the conditions to the new project, and the project XML (used to create a project from an XML file) includes Form Display Logic. Either way, re-check any `[user-role-id]` conditions afterwards (see Section 6).

For the full column-by-column reference, accepted values, an annotated example, and common mistakes, see **[RC-IMP-08 — Form Display Logic CSV — Column Reference and Format Guide](RC-IMP-08_Form-Display-Logic-CSV.md) — Form Display Logic CSV**.

---

## 10. Common Questions

**Q: What is the difference between Form Display Logic and field-level branching logic?**

**A:** Branching logic operates at the field level — it shows or hides individual fields within an instrument. Form Display Logic operates at the instrument level — it enables or disables access to an entire form. They are independent features and can be used simultaneously. A form can be enabled by Form Display Logic but still show or hide individual fields based on branching logic once a user opens it.

**Q: If a form is disabled, can a user still see that it exists?**

**A:** By default, yes. Disabled forms are grayed out but remain visible on the Record Status Dashboard, Record Home Page, and the left-hand menu. The "Hide forms that are disabled" optional setting hides them in the left-hand menu and on the Record Home Page; they still appear, grayed out, on the Record Status Dashboard. Either way, opening a disabled form by a direct link sends the user to the next enabled form or the Record Home Page.

**Q: What happens if a form has two conditions and only one is true?**

**A:** The form is enabled. Multiple conditions for the same form combine with OR logic — if at least one condition is true, the form is accessible.

**Q: Does Form Display Logic prevent data from being imported into a disabled form?**

**A:** No. Form Display Logic applies only to the data entry user interface. Data imported via the Data Import Tool or API bypasses Form Display Logic entirely and writes to the database regardless of whether a form would be disabled in the UI.

**Q: Can I use Form Display Logic to control which forms appear in the Survey Queue?**

**A:** No. Form Display Logic has no effect on the Survey Queue, and it does not block survey links or invitations. The Survey Queue manages its own access logic independently. Form Display Logic affects surveys only through Survey Auto-Continue, for conditions whose **Apply to** setting includes **Survey Auto-Continue**.

**Q: My project will be copied to use in a new study. Should I use `[user-role-id]` or `[user-role-name]` in my conditions?**

**A:** Use `[user-role-name]`. Role IDs are unique across the entire REDCap installation and change when a project is copied. Unique role names are kept when the roles are copied with the project. If you use role IDs and then copy the project, allow-list conditions stop enabling the form for anyone and exclusion conditions stop excluding anyone — blinded users gain access — until you update every role ID reference in the new project.

**Q: Can I use Form Display Logic in a classic (non-longitudinal) project?**

**A:** Yes. In a classic project the CSV has five columns with no `event_name` column at all; a file that includes `event_name` is rejected. Remove the column (do not just leave it blank) when moving a CSV from a longitudinal project. All other functionality works the same way.

**Q: Do administrators bypass Form Display Logic?**

**A:** No. It applies to every user, administrators included. It only restricts: it never opens an instrument that a user's rights deny.

---

## 11. Common Mistakes & Gotchas

> **Critical — using role IDs when the project may be copied.** Role IDs change on copy, and role-based logic then breaks silently in two different ways. Allow-list conditions (`[user-role-id]='X'`) stop enabling the form for anyone. Exclusion conditions (`[user-role-id]<>'X'`) stop excluding — so blinded users **gain access** to forms they must not see. Use `[user-role-name]` (unique role names are kept when roles are copied), or re-check every role condition after each copy.

**Forgetting the OR rule for multi-condition forms.** If you add two rows for the same form expecting both conditions to be required simultaneously (AND behavior), the form will actually be enabled when either condition is true. To require multiple simultaneous conditions, combine them in a single condition row using `and`.

**Assuming Form Display Logic protects data from imports.** A form being disabled in the UI does not prevent data from being written to that form via import. Form Display Logic is a UI control only — it does not enforce data integrity at the database level.

**Not testing with users in different roles.** Because Form Display Logic can include user-based smart variables, behavior can differ based on who is logged in. Always test with accounts assigned to each relevant user role to verify that access is correctly granted or blocked for each role.

**Leaving event_name blank unintentionally.** If `event_name` is blank, the condition applies to all events where the form appears. This is often what you want for a site-wide gate (like consent), but can accidentally disable or enable a form across events you did not intend. Review blank event_name rows carefully.

**Relying on unqualified references for record-wide checks.** Conditions are evaluated in the form's own event and instance, so `[current-instance]` and `[previous-instance]` work, but an unqualified field reference can give different results in different events or instances. For a check that must hold across the whole record, use an explicit `[event_name][field_name]` reference.

**Editing the CSV in a plain text editor or script.** Every `"` inside a cell is doubled in the raw file and the cell is wrapped in quotes, so `[record_id]<>""` is written `"[record_id]<>"""""`. Writing the condition back with the wrong number of quotes makes the upload fail or changes the logic. Download the file and edit it in a spreadsheet rather than hand-typing quotes; if you script against it, use a proper CSV library.

**Uploading a partial CSV.** An upload replaces every existing condition. Uploading a file with only the new rows deletes all the others. Download the full setup, add to it, and upload the complete file.

**Typing flags as `Y` or `yes`.** Only a lowercase `y` counts; anything else is treated as `n`, and a row with all three flags `n` is rejected.

---

## 12. Related Articles

- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (field-level logic vs. form-level logic)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (the logic language used in conditions)
- [RC-BL-05 — Branching Logic — Longitudinal Projects](RC-BL-05_Branching-Logic-in-Longitudinal-Projects.md) (event-based field references used in conditions)
- [RC-PIPE-05 — Smart Variables: User](RC-PIPE-05_Smart-Variables-User.md) (user-based variables usable in Form Display Logic conditions)
- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) (where Form Display Logic visually takes effect)
- [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) (related feature not affected by Form Display Logic)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (instrument-level access rights, a related access control mechanism)

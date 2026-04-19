RC-FDL-01

**Form Display Logic**

| **Article ID** | RC-FDL-01 |
|---|---|
| **Domain** | Form Display Logic |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights to configure |
| **Prerequisite** | RC-BL-02 — Branching Logic: Syntax & Atomic Statements |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-BL-01 — Branching Logic Overview; RC-PIPE-05 — Smart Variables: User; RC-NAV-REC-04 — Record Status Dashboard; RC-SURV-07 — Survey Queue |

---

# 1. Overview

Form Display Logic is an advanced feature that allows project designers to control which data entry instruments are accessible to users based on conditional logic. It is the data entry equivalent of the Survey Queue: just as the Survey Queue controls which surveys a participant can access and in what order, Form Display Logic controls which instruments a data entry user can open and when.

When a condition is met, the form is **enabled** and accessible. When it is not met, the form is **disabled** — grayed out and unclickable — but still visible by default. Optionally, disabled forms can be completely hidden.

**This article is written for project designers** who configure Form Display Logic. Data entry users only experience its effects: they see forms that are enabled, grayed out, or hidden depending on what the designer has set up. Designers configure Form Display Logic from the Project Setup area; it can also be exported and imported as a CSV file for bulk editing or reuse across projects.

---

# 2. Key Concepts & Definitions

**Form Display Logic**

Conditional logic applied at the instrument level. A condition (written in standard REDCap logic syntax) determines whether a specific form-event combination is enabled or disabled for data entry.

**Enabled vs. Disabled**

When a form's condition evaluates to **true**, the form is enabled — users can open and edit it normally. When the condition evaluates to **false**, the form is disabled — it is grayed out and inaccessible for data entry, but still visible on the page.

**OR Rule for Multiple Conditions**

A single form can appear in multiple condition rows. If the same form is listed more than once, **the form will be enabled if at least one of its conditions evaluates to true**. Multiple conditions for the same form combine with OR logic, not AND.

**Record-Level Evaluation**

Form Display Logic conditions are evaluated at the record level — not within the context of a specific event or repeating instance. This means only standard cross-event references work in conditions; relative smart variables are not supported (see Section 7, Limitations).

---

# 3. Where Form Display Logic Takes Effect

Form Display Logic affects the data entry user interface in three locations:

- **Record Status Dashboard** — disabled forms show a grayed-out dot; users cannot click through to the instrument.
- **Record Home Page** — disabled forms are grayed out in the instrument list.
- **Left-hand Data Collection menu** — disabled forms appear in the form list but cannot be navigated to.

> **Important:** Form Display Logic does **not** affect data imports. Imported records bypass all Form Display Logic and write directly to the database regardless of whether a form would be disabled in the UI. Similarly, Form Display Logic has **no effect on the Survey Queue** — it cannot prevent a survey from appearing in a queue sequence. It can, however, affect the **Survey Auto-Continue** feature if the corresponding checkbox is enabled in the Form Display Logic settings.

---

# 4. Configuring Form Display Logic

Form Display Logic is managed from the Project Setup area. Each condition row defines:

| Column | Description |
|---|---|
| `form_name` | The internal instrument name (as it appears in the Data Dictionary). |
| `event_name` | The event to which this condition applies. **Leave blank to apply the condition to all events** where the form appears. |
| `control_condition` | The REDCap logic expression. When this evaluates to true, the form is enabled. |
| `apply_to_data_entry` | `y` or `n` — whether this condition affects the standard data entry UI. |
| `apply_to_survey_autocontinue` | `y` or `n` — whether this condition affects Survey Auto-Continue behavior. |
| `apply_to_mycap_tasks` | `y` or `n` — whether this condition affects MyCap task availability. |

Conditions use the same logic syntax as branching logic and calculated fields. See RC-BL-02 — Branching Logic: Syntax & Atomic Statements for the full syntax reference.

---

# 5. Optional Settings

Two optional global settings modify how disabled forms are displayed:

**Keep forms enabled if they contain data**

When enabled, this setting overrides Form Display Logic for forms that already have data — only empty forms (those with a gray status icon) will be disabled. Any form that contains at least one saved value remains accessible even if the condition is false. This protects against accidentally locking users out of partially completed forms when logic conditions change.

**Hide forms that are disabled**

When enabled, disabled forms are completely hidden rather than merely grayed out. Hidden forms do not appear in the Data Collection menu or on the Record Home Page. This reduces visual clutter for users who should not interact with certain forms at all, rather than simply being prevented from entering data.

These two settings can be combined: you can hide disabled forms while keeping data-containing forms accessible.

---

# 6. Using Smart Variables in Conditions

Form Display Logic supports smart variables in its condition expressions, making it possible to control form access based on who is currently logged in — not just what data is in the record.

The most commonly used user smart variables in Form Display Logic are:

| Smart Variable | Returns | Common Use |
|---|---|---|
| `[user-name]` | The logged-in user's REDCap username | Restrict a form to specific named users (e.g., PI only) |
| `[user-role-id]` | Numeric ID of the user's assigned role | Block or allow access by role |
| `[user-role-name]` | Unique role name within the project | Preferred over role ID if the project may be copied |
| `[user-dag-name]` | Unique name of the user's Data Access Group | Site-specific form access in multi-site projects |

> **Caution with `[user-role-id]`:** Role IDs are unique across the entire REDCap installation and change when a project is copied. If you use role IDs in Form Display Logic and later copy the project, those IDs will be invalid in the new project. Use `[user-role-name]` in place of `[user-role-id]` when you anticipate copying the project.

See RC-PIPE-05 — Smart Variables: User for the full reference.

---

# 7. Limitations

**Record-level evaluation only.** Form Display Logic conditions are evaluated in the context of the record as a whole, not in the context of a specific event or repeating instance. This means:

- You can reference data from a specific event using the standard `[event_name][field_name]` syntax (e.g., `[consent_arm_1][consent_yn]`).
- You **cannot** use relative smart variables — those with the words "current", "next", or "previous" in their name, such as `[current-instance]`, `[next-event-name]`, or `[previous-event-name]`.

**No effect on data imports.** Form Display Logic operates only in the data entry UI. Any data imported via the Data Import Tool or API bypasses Form Display Logic entirely.

**No effect on Survey Queue.** The Survey Queue evaluates its own conditions independently. Form Display Logic cannot prevent a survey from appearing in a queue or being triggered. It can affect Survey Auto-Continue if that option is checked.

**Forms remain visible when disabled.** By default, disabled forms are grayed out but still visible. If you want them fully hidden, enable the "Hide forms that are disabled" optional setting.

---

# 8. Real-World Examples

The following patterns are drawn from actual project implementations, with usernames and role IDs replaced by generic placeholders.

---

## Example 1: Consent Gate

**Goal:** Most data collection forms should be inaccessible until the participant has consented.

```
form_name,event_name,control_condition,...
adverse_event,,[consent_arm_1][consent_yn]='1',...
demographics,screening_arm_1,[consent_arm_1][consent_yn]='1',...
blood_labs,baseline_arm_1,[consent_arm_1][consent_yn]='1',...
```

When `event_name` is blank, the condition applies to all events where the form appears. This is a common gate pattern: lock all forms until a single consent field is checked.

---

## Example 2: Post-Randomization Gate with Role-Based Blinding

**Goal:** Follow-up assessment forms should only be enabled after the participant has been randomized. Additionally, certain user roles (e.g., blinded coordinators) must be excluded from the condition so they remain blocked even after randomization.

```
form_name,event_name,control_condition,...
moca,3_month_arm_1,"[randomization_arm_1][rand_group]<>'' and [user-role-id]<>'ROLE_BLIND_A' and [user-role-id]<>'ROLE_BLIND_B'",...
event_log,4week_call_arm_1,"[randomization_arm_1][rand_group]<>'' and [user-role-id]<>'ROLE_BLIND_A' and [user-role-id]<>'ROLE_BLIND_B'",...
```

This pattern combines a data-driven condition (`rand_group<>''`) with user role exclusions. Blinded users are kept locked out even when data conditions are met.

---

## Example 3: Treatment-Arm–Specific Forms

**Goal:** Certain forms (e.g., an inpatient exercise log) only apply to participants in a specific treatment arm and should be disabled for controls.

```
form_name,event_name,control_condition,...
inpatient_exercise,,[randomization_arm_1][rand_group]='2',...
home_visit,,[randomization_arm_1][rand_group]='2',...
outpatient_exercise,,[randomization_arm_1][rand_group]='2',...
```

These forms are disabled for everyone until randomization happens and enabled only for participants assigned to group 2.

---

## Example 4: Complex Eligibility Gate

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

## Example 5: Named-User Allow-List

**Goal:** A finalization checklist form should only be accessible to the PI and designated coordinators, regardless of role.

```
form_name,event_name,control_condition,...
finalize_checklist,event_forms_arm_1,"[user-name]='pi.researcher' or [user-name]='coord.site1@example.org' or [user-role-id]='ROLE_PI_EQUIV'",...
```

This approach allows specific users by username and also includes a role-based fallback. Note: prefer `[user-role-name]` over `[user-role-id]` if the project may be copied in the future.

---

## Example 6: Sequential Form Unlock

**Goal:** A study completion form should only become available after an intervention completion form is fully saved.

```
form_name,event_name,control_condition,...
study_completion,event_forms_arm_1,"[interv_reas]<>'' and [interv_date]<>'' and [intervention_completion_complete]='2'",...
```

The `_complete` field for any instrument is a standard REDCap completion status field (0 = Incomplete, 1 = Unverified, 2 = Complete). This pattern chains form completion to form access.

---

# 9. The Form Display Logic CSV

Form Display Logic can be exported as a CSV and re-imported to another project or used for bulk editing. The exported file includes the six columns described in Section 4.

**Export:** Use the Export button in the Form Display Logic interface to download the current configuration.

**Import:** The CSV can be edited in any spreadsheet application and uploaded back into REDCap. This is the fastest way to set up Form Display Logic in a new project that mirrors an existing one.

**One row per form-event-condition combination.** A single form can appear in multiple rows (different events or different conditions). Remember: multiple rows for the same form combine with OR logic — the form is enabled if any condition is true.

---

# 10. Common Questions

**Q: What is the difference between Form Display Logic and field-level branching logic?**

**A:** Branching logic operates at the field level — it shows or hides individual fields within an instrument. Form Display Logic operates at the instrument level — it enables or disables access to an entire form. They are independent features and can be used simultaneously. A form can be enabled by Form Display Logic but still show or hide individual fields based on branching logic once a user opens it.

**Q: If a form is disabled, can a user still see that it exists?**

**A:** By default, yes. Disabled forms are grayed out but remain visible on the Record Status Dashboard, Record Home Page, and the left-hand menu. If you want disabled forms to be completely invisible, enable the "Hide forms that are disabled" optional setting.

**Q: What happens if a form has two conditions and only one is true?**

**A:** The form is enabled. Multiple conditions for the same form combine with OR logic — if at least one condition is true, the form is accessible.

**Q: Does Form Display Logic prevent data from being imported into a disabled form?**

**A:** No. Form Display Logic applies only to the data entry user interface. Data imported via the Data Import Tool or API bypasses Form Display Logic entirely and writes to the database regardless of whether a form would be disabled in the UI.

**Q: Can I use Form Display Logic to control which forms appear in the Survey Queue?**

**A:** No. Form Display Logic has no effect on the Survey Queue. The Survey Queue manages its own access logic independently. Form Display Logic can optionally affect Survey Auto-Continue if that checkbox is enabled in the settings.

**Q: My project will be copied to use in a new study. Should I use `[user-role-id]` or `[user-role-name]` in my conditions?**

**A:** Use `[user-role-name]`. Role IDs are unique across the entire REDCap installation and change when a project is copied. Role names are unique within a project and are preserved when the project is copied. If you use role IDs in your Form Display Logic and then copy the project, you will need to update all role ID references in the new project.

**Q: Can I use Form Display Logic in a classic (non-longitudinal) project?**

**A:** Yes. In a classic project, the `event_name` column is not applicable — leave it blank and the condition applies to all instances of the form. All other functionality works the same way.

---

# 11. Common Mistakes & Gotchas

**Using role IDs when the project may be copied.** Role IDs change on copy. If your Form Display Logic uses `[user-role-id]` and the project is duplicated, all role-based logic will break silently — forms will appear disabled for everyone (since the old IDs no longer match). Always prefer `[user-role-name]` for role-based conditions.

**Forgetting the OR rule for multi-condition forms.** If you add two rows for the same form expecting both conditions to be required simultaneously (AND behavior), the form will actually be enabled when either condition is true. To require multiple simultaneous conditions, combine them in a single condition row using `and`.

**Assuming Form Display Logic protects data from imports.** A form being disabled in the UI does not prevent data from being written to that form via import. Form Display Logic is a UI control only — it does not enforce data integrity at the database level.

**Not testing with users in different roles.** Because Form Display Logic can include user-based smart variables, behavior can differ based on who is logged in. Always test with accounts assigned to each relevant user role to verify that access is correctly granted or blocked for each role.

**Leaving event_name blank unintentionally.** If `event_name` is blank, the condition applies to all events where the form appears. This is often what you want for a site-wide gate (like consent), but can accidentally disable or enable a form across events you did not intend. Review blank event_name rows carefully.

**Using relative smart variables.** Variables like `[current-instance]`, `[next-event-name]`, or `[previous-event-name]` will not work in Form Display Logic because conditions are evaluated at the record level, not within the context of a specific event or repeating instance.

---

# 12. Related Articles

- RC-BL-01 — Branching Logic: Overview & Scope (field-level logic vs. form-level logic)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (the logic language used in conditions)
- RC-BL-05 — Branching Logic in Longitudinal Projects (event-based field references used in conditions)
- RC-PIPE-05 — Smart Variables: User (user-based variables usable in Form Display Logic conditions)
- RC-NAV-REC-04 — Record Status Dashboard & Other Record Links (where Form Display Logic visually takes effect)
- RC-SURV-07 — Survey Queue (related feature not affected by Form Display Logic)
- RC-USER-03 — User Rights: Configuring User Privileges (instrument-level access rights, a related access control mechanism)

STYLE-GUIDE

**REDCap Project Design Style Guide**

| **Document ID** | STYLE-GUIDE |
|---|---|
| **Domain** | Project Design Conventions |
| **Applies To** | All REDCap project designers and reviewers |
| **Prerequisite** | None |
| **Version** | 1.2 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-08 — Field Alignment; RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments and Events Setup; RC-OPS-01 — Operational Request Management Projects |

---

# 1. Overview

This document records the preferred design conventions for REDCap projects built or supported by this team. It is a living document — add new principles as they are agreed upon.

These are defaults, not mandates. Individual projects may deviate when there is a good reason, but deviations should be intentional and documented, not accidental.

**How to use this guide:**

- **New project designers** — read this before building your first instrument. These conventions exist because they reduce common mistakes and create a more consistent experience for data entry users and analysts.
- **Reviewers** — use this as a checklist when reviewing a new data dictionary or instrument design before a project goes into production.
- **Contributors** — if you encounter a recurring design decision that isn't covered here, add a new section. Include the convention, the rationale, and any exceptions.

---

# 2. Field Alignment (Column N — Custom Alignment)

REDCap supports four alignment codes: `LH`, `LV`, `RH`, and `RV`. See RC-FD-08 Section 5.12 for a full explanation of what each code does visually.

The short version:
- **L (Left)** = field spans full page width
- **R (Right)** = field is approximately half-width (right side of page)
- **H (Horizontal)** = label and input are side by side
- **V (Vertical)** = label sits above the input

The default when the column is left blank is `RV`.

## 2.1 Notes fields (`notes` field type)

**Convention: use `LH` or `LV`**

A `notes` field with `RH` or `RV` alignment renders at roughly half the page width, which makes the text area cramped and difficult to type in. Setting alignment to `LH` or `LV` gives the text area the full page width.

There is rarely a good reason to use a half-width notes field. If you are using one, consider whether a single-line `text` field would be more appropriate.

## 2.2 Radio and checkbox fields

**Convention: `LV` for longer lists, `LH` for short lists**

The Vertical/Horizontal component controls whether answer choices are stacked (V) or displayed in a single row (H). As a rule of thumb:

- 2–4 short choices → `LH` (horizontal, full width) reads cleanly
- 5 or more choices, or long choice labels → `LV` (vertical, full width) is easier to scan

The Left/Right component controls which side of the page choices appear on. Left (`L`) is generally preferred as it aligns with natural reading direction and gives more visual space.

## 2.3 Text, dropdown, yesno, truefalse

**Convention: leave blank (accept `RV` default) unless there is a layout reason to change**

These field types are compact and the width difference between Left and Right alignment is less impactful than with `notes` fields. Accept the default unless you are deliberately composing a specific layout.

## 2.4 Consistency within an instrument

**Convention: avoid mixing Left and Right fields in the same section without a clear layout purpose**

Alternating between full-width and half-width fields creates a visually fragmented form. If you are setting alignment on any field, consider whether the surrounding fields should also be aligned consistently.

---

# 3. Project Structure

## 3.1 Do not use longitudinal mode if each form is only used once

**Convention: use longitudinal mode only when instruments are repeated across multiple events**

Longitudinal mode is designed for studies where participants complete the same instruments at multiple time points (e.g., baseline, month 3, month 6). If your project has multiple forms but each form is used at a single point in time (e.g., a Screening form, an Enrollment form, and a Follow-up form — each completed once), a classic (non-longitudinal) project achieves the same result with less configuration overhead.

Using longitudinal mode for a single-arm, single-instance-per-form project adds unnecessary complexity: event setup, event-scoped branching logic syntax, and a more confusing record status dashboard — with no functional benefit.

**Use longitudinal mode when:**
- The same instrument is completed by the same participant at more than one time point, OR
- You need to track scheduling windows, multiple arms, or event-based branching logic

**Use classic mode when:**
- Each instrument is completed exactly once per participant, regardless of how many instruments exist

**Exception:** Some institutions use longitudinal mode for purely structural reasons (e.g., to use repeated instruments without repeating events). If you have a specific architectural reason, document it in the project notes.

---

# 4. Field Notes vs. Field Annotations

## 4.1 Field Note (Column G) — for data entry users only

**Convention: use the Field Note for short, user-facing clarifications about how to fill in the field**

The Field Note appears below the variable on the form and is visible to anyone completing the instrument — data entry staff and survey participants alike. Use it to answer the question the user is likely to ask at the moment they see the field.

Common uses:
- Units of measure (e.g., `mg/L`, `mmol/mol`, `kg`)
- Date format reminders (e.g., `YYYY-MM-DD`)
- Scope clarifications (e.g., `Include prescribed medications only`)
- Range expectations (e.g., `Normal range: 4.0–11.0`)

Keep it brief. A Field Note that runs to multiple sentences will be ignored. If the field needs more explanation than a line or two, consider whether the instrument design or the field label should be doing more of that work.

## 4.2 Field Annotation (Column R) — for designers only

**Convention: use the Field Annotation box for notes intended for other project designers, not for data entry users**

Field Annotation content is visible only in the Data Dictionary and the Online Designer — it is never shown on the form. This makes it the right place for:
- Design rationale (e.g., `Mapped to variable X in the source dataset`)
- Outstanding questions or to-dos (e.g., `Confirm unit with PI before go-live`)
- Coding notes (e.g., `Raw value 99 = missing per protocol`)

Field Annotations can be combined with action tags in the same cell. When doing so, put the plain-text note first and the action tags after, separated by a space or line break. Action tags always begin with `@` and are not affected by surrounding text.

Example annotation cell containing both a note and action tags:
```
Confirm unit with PI. @HIDDEN-SURVEY @READONLY
```

> **Important:** Never put user-facing instructions in the Field Annotation — they will not be seen by the person filling in the form. Use the Field Note (Column G) for anything the data entry user needs to read.

---

# 5. Branching Logic Design

## 5.1 Do not hardcode user identifiers in branching logic

**Convention: never use hardcoded usernames, NetIDs, or system IDs as branching logic conditions**

A common pattern for hiding admin-only fields is to write branching logic that checks whether the currently logged-in user matches a known identifier:

```
[reviewer_field] = 'abc123' or [reviewer_field] = 'xyz456'
```

This approach creates several problems. If staff change or leave, every branching logic expression that references their ID must be updated manually, across every instrument it appears in. The identifiers also end up embedded in the data dictionary, creating an informal personnel record that is hard to audit and potentially privacy-sensitive.

**Preferred approach: use a role-based or configurable field**

Instead of hardcoding identifiers, collect the reviewer's identity in a dedicated field and gate visibility on a role or a flag value that is easy to update:

- Use a dropdown or radio field (e.g., `reviewer_role`) populated with role names rather than personal identifiers.
- Gate admin-only fields on `[reviewer_role] = 'admin'` instead of on a specific person's username.
- If the set of reviewers is small and changes rarely, consider a single configuration field at the project level whose value can be updated without touching the data dictionary.

**Rationale:** Hardcoded IDs tie the instrument design to specific individuals, make maintenance error-prone, and expose personnel information in the data dictionary. Role-based logic survives staff turnover without requiring structural changes.

**Exception:** In a tightly controlled internal tool where the reviewer list is stable and the project owner accepts the maintenance burden, hardcoded identifiers may be acceptable as a short-term convenience. Document the intent in the Field Annotation so future designers understand why it is there.

## 5.2 Use a descriptive field to display a conditional warning or alert

**Convention: use a `descriptive` field type with branching logic to surface warnings inline on the form**

When a user makes a combination of choices that requires an action or creates a likely error, a descriptive field with targeted branching logic can display a warning directly on the form — no external notification needed. Example: show a warning only when a user selects "No" for an end-date waiver but then leaves the end date field blank.

```
[ongoing] = '2' and [enddate] = ''
```

The descriptive field is shown only when that condition is true, and it can include styled HTML (e.g., red text) to make the warning visually distinct.

**Rationale:** Inline warnings catch data entry errors at the moment they occur, reducing cleanup later. They are less intrusive than required-field validation, which blocks form submission entirely, and more visible than post-submission alerts.

**Tip:** Keep the warning label short and action-oriented (e.g., "You selected 'No' to ongoing access but no end date was entered. Please enter an end date above or change your selection."). Style with `<span style="color:red;font-weight:bold;">` for visibility.

## 5.3 Admin-only review sections: gate with a reviewer identity field, not user rights alone

**Convention: when a form contains fields that only an administrator should see, use a dedicated reviewer identity field as the branching logic gate — in addition to any user rights restrictions**

Admin-only review fields (e.g., reviewer notes, status codes, internal dates) can be hidden from data entry users by placing them behind branching logic that checks a reviewer-identity field. The reviewer enters their own identifier into that field, which unlocks the admin section.

```
[reviewer_field] <> ''
```

This is distinct from relying on REDCap's user rights alone. User rights prevent editing, but they do not hide fields from view. Branching logic provides the visual hiding.

**Rationale:** Combining user rights (to prevent unauthorized editing) with branching logic (to prevent visual exposure of internal fields) gives a cleaner experience for requesters completing a survey and a clearer separation of concerns in the form layout.

**Note:** See Section 5.1 for guidance on what value to check in the reviewer identity field — prefer role-based values over hardcoded personal identifiers.

## 5.4 Always add branching logic to "Other (specify)" free-text fields

**Convention: any free-text field paired with an "Other" choice must have branching logic that hides it when that choice is not selected**

A radio or dropdown field that includes an "Other (specify)" option typically has a companion free-text field for the specified value. Without branching logic on that companion field, it is visible at all times — even when the respondent has not selected "Other." This produces spurious blank fields in the dataset and clutters the form unnecessarily.

The branching logic on the "Other (specify)" field should match the exact code assigned to the "Other" choice in the parent field:

```
[parent_field] = '666'
```

Adjust to match whatever code your project assigns to the "Other" choice.

**Do not embed the field name in the choice label as a substitute.** A pattern sometimes seen is writing the companion field name directly in the choice label (e.g., `666, Other — {specify_field}`). REDCap does not parse curly-brace or similar notation in choice labels — the text renders literally and the field remains unconditionally visible. Use standard branching logic on the companion field instead.

**Rationale:** When the free-text field is hidden unless "Other" is selected, a blank value unambiguously means "not applicable." When it is always visible, a blank value is ambiguous — it could mean not applicable, not answered, or overlooked. Branching logic eliminates that ambiguity and keeps forms clean.

## 5.5 Do not mark a field as required when the requirement is conditional

**Convention: if a field is only meaningful based on another field's value, use branching logic to hide it when not applicable — not the "Required" flag**

REDCap's Required flag blocks form completion until the field contains a value. When a required field is always visible but only sometimes relevant, users must enter a placeholder ("N/A", "none", "-") to save the form, which pollutes the dataset and complicates analysis.

Common examples where this pattern causes problems:

- A "Deviation Description" field required on every test case, even when the test result is "Pass" (no deviation exists)
- A "Modification Approved By" field required on version 1.0 of a document (no modifications have been made)
- A "Reason for early withdrawal" field required even for participants who completed the study

**Preferred approach:** Use branching logic to show the field only when it is applicable. When a field is hidden by branching logic, REDCap does not enforce the Required constraint — the field is treated as not applicable.

```
// Show Deviation Description only when the test failed
[pass_fail] = '0'
```

If you want to enforce entry without blocking form save, use the inline warning pattern from Section 5.2 instead.

**Rationale:** Required-always fields that are conditionally relevant train users to enter meaningless placeholder values. Branching logic is the correct mechanism for conditional data entry — it keeps the dataset clean and the form free of fields that don't apply in context.

---

# 6. Repeating Instruments

## 6.1 Use custom form labels to identify repeating instrument instances

**Convention: set the custom form label on repeating instruments to display the key identifying field(s) for that instance**

When an instrument repeats, the record status dashboard shows each instance as "Instance 1", "Instance 2", etc. by default. Adding a custom form label that pipes in a meaningful field (e.g., the user's name, a project title, or a date) makes it immediately clear what each instance contains without opening it.

Example custom form label for a user request instrument:
```
[institutional_id], [user_name]
```

Example for a project request instrument:
```
[projectname] ([server_field]), pid: [pid]
```

**Rationale:** When a record has many repeating instances, unlabeled instances are difficult to navigate. Custom form labels cost nothing to set up and significantly reduce confusion during data review.

**Where to set it:**

- **Repeating instruments** — Project Setup → Enable optional modules and customizations → Repeating instruments (Enable / Modify). In the popup, enter the piping expression in the custom label field next to the instrument name. This is the only place this label can be configured; it is not available in the Online Designer. (RC-LONG-02 §4–6)
- **Repeating events** — The custom label field in the repeating instruments popup is greyed out for events set to "Repeat entire event." Instead, set the label in **Define My Events** using the **Custom Event Label** column. (RC-LONG-01 §4.2, RC-LONG-02 §6)

---

# 7. Field and Form Hygiene

## 7.1 Every field must have a label

**Convention: no field should have a blank field label**

REDCap allows a field to be saved with an empty label, but doing so creates a blank space on the form that gives the respondent no indication of what the field is for. This most commonly happens with companion fields added late in the design process (e.g., a file upload added to hold a generated PDF, or a "specify" text field placed after a radio option).

Check for unlabeled fields before the project goes live. A quick way to audit: export the data dictionary and filter for rows where the `field_label` column is blank (excluding the record ID field, which is legitimately label-free in some configurations).

**Common causes:**
- Companion "Other (specify)" fields where the designer assumed the parent choice label was sufficient
- File upload fields added as an afterthought to hold generated outputs or summary documents
- Descriptive fields used as spacers, left blank intentionally — these should at minimum contain a comment in the Field Annotation documenting their purpose

**Rationale:** Unlabeled fields are confusing to data entry users and future designers alike. They signal an incomplete design and make it hard to distinguish intentional placeholders from accidental omissions.

## 7.2 Audit instrument-event and repeating-instrument settings across all arms

**Convention: when a project has multiple arms, verify that repeating instrument configuration is consistent across all arms that use the same workflow structure**

In a multi-arm project where each arm represents a parallel lifecycle phase or patient cohort with the same event structure, the repeating instrument settings should generally be identical across arms. A common oversight is configuring a repeating instrument in Arms 2–4 while leaving it non-repeating in Arm 1 — because Arm 1 was built first and the repeating configuration was added later without being back-applied.

The result is that one arm has a different data collection capacity than the others: Arm 1 records can only have one instance, while Arms 2–4 records can have many. This inconsistency is difficult to detect from the form UI and only becomes apparent when a user tries to add a second instance in Arm 1 and cannot.

**How to check:** Project Setup → Repeating Instruments and Events → review the list of configured repeating instruments. Each entry shows the event name and arm. Verify that equivalent events in every arm appear in the list if they should repeat.

---

# 8. Related Articles

- RC-FD-08 — Field Alignment and Custom Alignment Codes
- RC-LONG-01 — Longitudinal Project Setup
- RC-LONG-02 — Repeated Instruments and Events Setup
- RC-OPS-01 — Using REDCap as an Operational Request Management System

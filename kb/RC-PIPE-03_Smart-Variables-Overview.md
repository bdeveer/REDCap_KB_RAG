RC-PIPE-03

**Smart Variables — Overview**

| **Article ID** | RC-PIPE-03 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All REDCap project types |
| **Prerequisite** | RC-PIPE-01 — Piping Basics, Syntax & Field Types |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-01 — Piping Basics, Syntax & Field Types; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers; RC-PIPE-04 — Piping in Emails & Notifications; RC-BL-01 — Branching Logic Overview & Scope |

---

# 1. Overview

Smart variables are bracket expressions that reference system-level information in REDCap rather than participant-entered field values. They use the same `[bracket]` syntax as regular piping but resolve to context-dependent data — the current user's name, the current event, a survey link, a record's data access group, and more. This article provides a category-level overview of all smart variable groups available in REDCap.

New smart variables are added with each REDCap release. For a complete, version-specific listing, use the embedded help text accessible from any green "Smart Variables" button found in the Online Designer, survey settings, and alert configuration screens.

---

# 2. Key Concepts & Definitions

**Smart Variable**

A bracket expression that resolves to system-level or context-level information rather than a stored participant data value. Smart variables are recognized in the same locations as regular piping: field labels, field notes, descriptive text, email bodies, and logic expressions.

**Context-Dependent**

Smart variables return different values depending on who is viewing the form, which record is open, which event or instance is active, and similar runtime conditions. The same smart variable expression may return different results for different users or at different points in a study.

**Instance Qualifier**

A smart variable used as a prefix to a variable name bracket, directing REDCap to retrieve that variable's value from a specific instance within a repeated instrument or event series. Covered in detail in RC-PIPE-02.

**:hideunderscore Modifier**

By default, if a piped value is blank or null, REDCap displays six underscore characters (`______`) as a visual placeholder. Appending `:hideunderscore` inside the brackets suppresses this behavior and renders the blank as invisible instead — for example, `[record-name:hideunderscore]`. This modifier works with both field variables and smart variables.

---

# 3. Smart Variable Categories

## 3.1 User

Smart variables in this category return information about the REDCap user currently interacting with the system. Useful for personalizing data entry forms or emails based on who is logged in.

Examples of what these variables can return: the user's REDCap username, their first or last name, their email address, and which Data Access Group (DAG) the current user belongs to.

## 3.2 Record

These smart variables reference metadata about the record currently being viewed or edited — not the participant-entered data fields, but record-level properties managed by REDCap.

Examples: the record's unique identifier, the record's assigned Data Access Group, and a URL to the record's calendar page (if applicable).

## 3.3 Form

Form smart variables reference properties of the instrument (form) that is currently open. They do not return participant data — they return information about the instrument itself.

Examples: the instrument's name, a direct link to the current form for the current record, and the form's completion status.

## 3.4 Survey

Survey smart variables are similar to form smart variables but focus specifically on the survey aspect of an instrument. They are most useful in confirmation emails and automated survey invitations.

Examples: a direct link to the survey itself, the corresponding survey queue link for the current record, the survey's start timestamp, stop timestamp, and total completion duration.

## 3.5 Event & Arm

These smart variables enable dynamic event and arm references. While it is possible to hard-code a specific event name in a pipe reference (e.g., `[event_1_arm_1][variable_name]`), event smart variables allow you to reference events relative to the current context — for example, the previous event.

Examples: the name of the current event, the current arm number, the arm label, and relative event references such as the previous event or next event.

> **Note:** Hard-coded event references (e.g., `[event_1_arm_1][variable_name]`) are covered in RC-PIPE-02. Event smart variables extend that capability by allowing references that do not require knowing the specific event name in advance.

## 3.6 Repeating Instruments and Events

These smart variables serve two functions: (1) the instance qualifier smart variables covered in RC-PIPE-02 (`[first-instance]`, `[last-instance]`, `[previous-instance]`, `[next-instance]`), and (2) an additional smart variable that references a new, not-yet-created instance. The latter is useful for generating links or pre-populating default values that will apply to a new instance when it is created.

## 3.7 Aggregate Functions, Charts, and Tables

These smart variables are associated with REDCap's Project Dashboard feature. They allow project designers to build custom charts and summary tables on the dashboard using aggregated data from the project.

This category is more advanced and is primarily used by administrators and power users building project-level dashboards. Full documentation is available in REDCap's embedded help text.

## 3.8 Optional Parameters for Aggregate Functions, Charts, and Tables

These smart variables act as modifiers or extensions to the aggregate function category above. They refine how aggregate smart variables behave — for example, filtering which records are included in a count or which event's data is aggregated.

## 3.9 Randomization

These smart variables expose information about a record's randomization assignment. They are only relevant to projects with REDCap's Randomization module enabled.

Examples: the randomization number assigned to the record (`[rand-number]`), the server date/time at which the record was randomized (`[rand-time]`), and the equivalent UTC timestamp (`[rand-utc-time]`). Each variable also supports a `:value` suffix to return a raw `YYYY-MM-DD HH:MM:SS` formatted value suitable for use in logic or calculated fields rather than display contexts. Projects with more than one randomization can use `:n` (e.g., `[rand-number:2]`) to reference a specific one.

## 3.10 Project Dashboards

If a project uses public Project Dashboards, these smart variables provide access codes and URLs for those dashboards. They require the unique dashboard name (e.g., `D-XXXXXXXXXX`) found on the dashboard configuration page.

Examples: `[dashboard-url:D-9264XJ8HE7]` returns the dashboard's web address; `[dashboard-link:D-9264XJ8HE7:View Dashboard]` generates a clickable HTML link with custom text.

## 3.11 Public Reports

If a project has published public reports with access codes, this category provides the access code for a specified report. It requires the unique report name (e.g., `R-XXXXXXXXXX`) found on the My Reports & Exports page.

## 3.12 MyCap

If a project uses REDCap's MyCap mobile application for participant data collection, this category provides smart variables specific to the MyCap context — such as participant-facing links and MyCap-specific metadata.

## 3.13 Miscellaneous

The Miscellaneous category is primarily relevant for REDCap administrators rather than project designers. These smart variables expose information about the REDCap installation and the project itself.

Examples: the current REDCap version number, the project's unique Project ID, the base URL of the REDCap installation, and similar system-level metadata.

---

# 4. Where Smart Variables Can Be Used

Smart variables are recognized in the same locations as regular piping:

- Field labels, field notes, and descriptive text in instruments
- Survey confirmation text and survey completion messages
- Email bodies in confirmation emails, survey invitations, and Alerts & Notifications
- Branching logic conditions (certain smart variables, such as `[is-survey]`, are specifically designed for logic contexts)
- Action tag values (e.g., `@DEFAULT` and `@CALCTEXT`)

Not all smart variables are meaningful in all contexts. For example, survey-specific smart variables (survey start time, survey queue link) are only useful in survey-related email fields, not in branching logic.

---

# 5. Finding the Complete Smart Variable Reference

REDCap's built-in help text is the authoritative and most up-to-date source for smart variable documentation, as new variables are added with each release. Access it via any green "Smart Variables" button, found in:

- The Online Designer (top-right floating help menu)
- Survey settings
- Alert & Notification configuration screens

The embedded help text lists every available smart variable, its syntax, its category, and usage notes.

---

# 6. Common Questions

**Q: What is a smart variable in REDCap?**

**A:** A smart variable is a bracket expression — like `[record-name]` or `[survey-url]` — that resolves to system-level information rather than a participant's entered data. Smart variables use the same piping syntax as regular field references but pull from REDCap's runtime context instead of the data entry record.

**Q: Where can I find a complete list of all smart variables?**

**A:** Use the green "Smart Variables" button in the Online Designer, survey settings, or alert configuration screens. The embedded help text is updated with each REDCap release and is the most reliable reference.

**Q: Can I use smart variables in branching logic?**

**A:** Yes, some smart variables are specifically designed for use in logic conditions. A common example is `[is-survey]`, which returns 1 if the current instrument is being accessed as a survey, and 0 if accessed as a standard data entry form. This allows you to show or hide fields depending on the access context.

**Q: What is the difference between a form smart variable and a survey smart variable?**

**A:** Form smart variables reference the instrument as a data collection form accessible to REDCap users — properties like the form name or a direct link to the form for a given record. Survey smart variables reference the same instrument specifically in its survey (public-facing) context — properties like the survey link for a participant, the survey queue link, and timestamps for when the survey was started and completed.

**Q: Can smart variables be used in the same expression as a regular variable pipe reference?**

**A:** Yes. Smart variables and regular variable references can coexist in the same text. For example, a field label might read: "Dear `[participant-name]`, you are enrolled in `[event-label]`." The two types of references are independent and each resolves on its own.

**Q: Are smart variables the same as piping modifiers?**

**A:** No. Piping modifiers (`:value`, `:label`, `:checked`, etc.) are suffixes appended to a regular variable name to change what value is returned from that variable. Smart variables are standalone bracket expressions that reference system-level information unrelated to any specific data field. Some smart variables are used as qualifiers (prefixed before a variable name, like `[first-instance][visit_date]`) but are still distinct from modifiers.

---

# 7. Common Mistakes & Gotchas

**Using smart variables outside of supported locations.** Not every smart variable works in every context. Survey-specific smart variables placed in branching logic do not resolve correctly. Test smart variable placement in a development project before using it in production.

**Relying on smart variables in a version-specific way without checking the embedded help.** REDCap adds new smart variables frequently. Documentation from external sources (including this KB) may lag behind the actual REDCap version in use at your institution. Always verify against the built-in help text.

**Confusing event smart variables with hard-coded event references.** Hard-coding an event name like `[event_1_arm_1]` requires you to know the specific event name at design time. Event smart variables (e.g., referencing the "previous event" dynamically) allow more flexible references that adapt to the record's current event context. Use whichever approach matches your design intent.

**Using smart variables in Data Quality rules.** Smart variables are supported in DQ rule logic, but they significantly increase the time required for rules to complete. Avoid using them in DQ rules unless necessary, and be prepared for longer run times when they are present.

**Using MyCap smart variables in non-MyCap projects.** MyCap smart variables only resolve correctly if the project has MyCap enabled and the participant is accessing data through the MyCap app. Using them in a standard web survey produces blank or unexpected output.

---

# 8. Related Articles

- RC-PIPE-01 — Piping Basics, Syntax & Field Types (core piping syntax and field type behavior)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (instance qualifier smart variables; cross-event piping)
- RC-PIPE-04 — Piping in Emails & Notifications (using smart variables in confirmation emails, invitations, and alerts)
- RC-PIPE-06 — Smart Variables: Record (record-level metadata smart variables)
- RC-PIPE-13 — Smart Variables: Randomization (smart variables for capturing randomization metadata)
- RC-PIPE-15 — Smart Variables: Public Reports (smart variables for linking to public reports)
- RC-PIPE-17 — Smart Variables: Miscellaneous (miscellaneous smart variables not covered in other sub-articles)
- RC-BL-01 — Branching Logic Overview & Scope (using smart variables in logic conditions)

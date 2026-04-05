RC-PIPE-07

**Smart Variables: Form**

| **Article ID** | RC-PIPE-07 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers; RC-PIPE-08 — Smart Variables: Survey |

---

# 1. Overview

Form smart variables return metadata about the data entry form (instrument) currently being displayed. They reference properties of the form itself — such as its name, label, and whether it is being viewed as a standard data entry form — rather than the participant data entered within the form. Use these variables to create dynamic form labels, generate links to other forms, and conditionally display content based on which instrument is active.

---

# 2. Key Concepts & Definitions

**Instrument / Form**

An instrument (also called a form) is a structured template within REDCap that defines a set of fields for data collection. The same instrument can be accessed as a standard data entry form (by REDCap users) or as a survey (by external participants). Form smart variables specifically refer to the instrument in its data entry context.

**Instrument Name (Unique Name)**

A unique identifier for an instrument within a project. The instrument name is configured in the Online Designer and is used in piping, logic, and system references. Example: `demographics`, `visit_data_form`, `adverse_events`. Instrument names are unique within a project but are not human-readable.

**Instrument Label (Display Name)**

The human-readable title of an instrument, also configured in the Online Designer. Example: "Demographics", "Visit Data", "Adverse Events". The label is what users and participants see in the interface.

**Data Entry Form vs. Survey**

The same instrument can be accessed in two ways: as a data entry form (by logged-in REDCap users with permissions) or as a survey (by external participants with a survey link or QR code). Form smart variables are relevant when the instrument is accessed as a data entry form. For survey-specific information, see RC-PIPE-08.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Is Form | `[is-form]` | Returns 1 if the current instrument is being accessed as a standard data entry form; returns 0 if accessed as a survey. Useful in branching logic to show/hide fields based on access context. | 1 (or 0) |
| Instrument Name | `[instrument-name]` | The unique identifier name of the current instrument. Returns blank if not in an instrument context. | demographics |
| Instrument Label | `[instrument-label]` | The human-readable label (display name) of the current instrument. Returns blank if not in an instrument context. | Demographics |
| Form URL (Specified Instrument) | `[form-url:instrument]` | The web address (URL) of the specified data entry form for the current record and event. Replace `instrument` with the unique form name. Can be combined with event prefix: `[event-name][form-url:visit_data_form]`. | https://... |
| Form Link (Specified Instrument) | `[form-link:instrument]` or `[form-link:instrument:Custom Text]` | An HTML web link to the specified data entry form for the current record/event. Replace `instrument` with the unique form name. Optionally add custom link text; if omitted, defaults to the form label. Can be used as `[form-link:Custom Text]` when instrument is assumed (on a form), or `[form-link]` in survey invitations. Can be combined with event prefix: `[next-event-name][form-link:visit_data_form]`. | Visit Data Form or Click here to enter data |

---

# 4. Usage Notes

**Using `[is-form]` in Branching Logic**

The `[is-form]` smart variable is designed to detect the access context. Use it in branching logic to show or hide fields based on whether the form is being accessed as a data entry form or survey. For example: `[is-form]=1` displays fields only in the data entry context, while `[is-form]=0` displays them only in survey mode.

**Form URL and Form Link Requirements**

To use `[form-url:instrument]` or `[form-link:instrument]`, you must know the unique form name. This can be found in the Online Designer under the form settings. If you use an incorrect instrument name, the link will not function.

**Event Prefix for Longitudinal Projects**

In longitudinal projects, you can prepend an event name to a form link to reference a form in a different event:
- `[baseline_arm_1][form-link:demographics]` generates a link to the Demographics form in the Baseline event.
- `[next-event-name][form-link:visit_data_form]` generates a link to the form in the next event.

See RC-PIPE-02 for detailed information on event prefixes.

**Form Link Customization**

When using `[form-link:instrument:Custom Text]`, replace "Custom Text" with your desired link label. For example:
- `[form-link:demographics:Click to enter demographics]`
- `[form-link:visit_1_assessment:Complete Visit Assessment]`

Without the custom text parameter, the link defaults to the form's label.

**Context-Dependent Instrument Variables**

`[instrument-name]` and `[instrument-label]` return blank if you reference them outside of an instrument context (e.g., in a dashboard, a separate email, or a data quality rule not tied to a specific form). They are most useful within field notes or descriptive text on the form itself.

**Survey Invitations and Form Links**

In a survey invitation email, you can use `[form-link]` (without specifying an instrument) and REDCap will assume the current form. You can also use `[form-link:Custom Text]` if you want custom link text. This is convenient for survey confirmation emails that link back to a data entry form.

---

# 5. Common Questions

**Q: How do I create a link from one form to another within the same record?**

**A:** Use `[form-link:instrument]` where `instrument` is the unique form name of the target form. For example, in the Demographics form, you might include a note that says "After completing demographics, proceed to `[form-link:visit_data_form]`." You can also customize the link text: `[form-link:visit_data_form:Click here to enter visit data]`.

**Q: What is the difference between `[instrument-name]` and `[instrument-label]`?**

**A:** `[instrument-name]` is the unique identifier used internally by REDCap (e.g., "demographics"). `[instrument-label]` is the human-readable display name (e.g., "Demographics"). Use the name when you need to reference the form in logic or other system contexts; use the label when you want to display readable text to users.

**Q: Can I use `[is-form]` in branching logic to hide survey-specific fields?**

**A:** Yes. For example, `[is-form]=1` shows a field only when the instrument is accessed as a data entry form, while `[is-form]=0` shows it only in survey mode. This allows you to customize the data collection experience based on how the form is being accessed.

**Q: I need to link to a form in a different event (longitudinal project). How do I do that?**

**A:** Use an event prefix before the form-link. For example: `[next-event-name][form-link:visit_data_form]` links to the Visit Data form in the next event. Or hard-code the event name: `[event_1_arm_2][form-link:demographics]`. See RC-PIPE-02 for more information on event prefixes.

**Q: What happens if I use an incorrect instrument name in `[form-link:instrument]`?**

**A:** REDCap will not generate a valid link. The link may display incorrectly or not function. Always verify the exact instrument name in the Online Designer before using it in a form-link smart variable.

**Q: Can I use form smart variables in survey invitations sent via email?**

**A:** Yes. `[instrument-label]` and `[form-link]` work in survey invitation emails. `[is-form]` also works and will return 0 (since the survey is being accessed in survey mode, not form mode). However, form-specific context variables like `[instrument-name]` may not resolve correctly outside the form itself.

---

# 6. Common Mistakes & Gotchas

**Using incorrect or typo'd instrument names in form links.** If you type `[form-link:demograhics]` instead of `[form-link:demographics]`, the link will not function. Always copy the exact instrument name from the Online Designer, or test the link thoroughly before deploying to production.

**Confusing form smart variables with survey smart variables.** Form variables like `[form-link]` and `[form-url]` are designed for data entry forms. Survey-specific smart variables (survey links, survey queue links, survey timestamps) are covered in RC-PIPE-08. Using form variables in a survey context may not produce the expected result. Use the appropriate smart variable type for your context.

**Assuming `[instrument-name]` and `[instrument-label]` always have values.** These variables return blank if you reference them outside of an instrument context. Do not rely on them in emails, dashboards, or data quality rules. Use them only in field labels, field notes, and descriptive text within the form itself.

**Not testing form links before deployment.** Form links can break if an instrument is renamed or deleted. After creating a form link, test it in a development environment to confirm it functions correctly before moving to production.

**Using form links in non-longitudinal projects without understanding event context.** In non-longitudinal projects (single-arm, single-event), form links work without event prefixes. In longitudinal projects, you must either specify the event or use event smart variables like `[next-event-name]`. Omitting the event in a longitudinal project may result in unexpected behavior.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (event prefixes and cross-event linking)
- RC-PIPE-08 — Smart Variables: Survey (survey-specific smart variables for comparison)
- RC-PIPE-09 — Smart Variables: Event & Arm (event smart variables for longitudinal projects)

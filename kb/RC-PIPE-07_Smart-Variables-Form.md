

**Smart Variables: Form**

| **Article ID** | [RC-PIPE-07 — Smart Variables: Form](RC-PIPE-07_Smart-Variables-Form.md) |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — smart variable behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md); [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md) |
| **Synonyms** | [form-link] smart variable; how to build a link to a data entry form with [form-url]; form smart variables for the instrument name [instrument-name]; [instrument-label] and [is-form] smart variables; pipe a link to a specific instrument with [form-link:instrument]; create a direct link to an instrument for a record; form-level smart variables for data entry forms; difference between [form-link] and [form-url] |

---

## 1. Overview

Form smart variables return metadata about the data entry form (instrument) currently being displayed. They reference properties of the form itself — such as its name, label, and whether it is being viewed as a standard data entry form — rather than the participant data entered within the form. Use these variables to create dynamic form labels, generate links to other forms, and conditionally display content based on which instrument is active.

---

## 2. Key Concepts & Definitions

**Instrument / Form**

An instrument (also called a form) is a structured template within REDCap that defines a set of fields for data collection. The same instrument can be accessed as a standard data entry form (by REDCap users) or as a survey (by external participants). Form smart variables specifically refer to the instrument in its data entry context.

**Instrument Name (Unique Name)**

A unique identifier for an instrument within a project. The instrument name is configured in the Online Designer and is used in piping, logic, and system references. Example: `demographics`, `visit_data_form`, `adverse_events`. Instrument names are unique within a project but are not human-readable.

**Instrument Label (Display Name)**

The human-readable title of an instrument, also configured in the Online Designer. Example: "Demographics", "Visit Data", "Adverse Events". The label is what users and participants see in the interface.

**Data Entry Form vs. Survey**

The same instrument can be accessed in two ways: as a data entry form (by logged-in REDCap users with permissions) or as a survey (by external participants with a survey link or QR code). Form smart variables are relevant when the instrument is accessed as a data entry form. For survey-specific information, see [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md).

---

## 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Is Form | `[is-form]` | Returns 1 only on a data entry form page; returns 0 on survey pages and also in alerts, PDFs, background processing and the API. Useful in branching logic to show/hide fields based on access context. | 1 (or 0) |
| Instrument Name | `[instrument-name]` | The unique identifier name of the current instrument: the data entry form or survey page being viewed, the instrument that triggered an alert, or the survey's instrument in a survey invitation. Returns blank where there is no current instrument. | demographics |
| Instrument Label | `[instrument-label]` | The human-readable label (display name) of the current instrument. Resolves in the same places as `[instrument-name]` (forms, survey pages, alerts, survey invitations). Returns blank where there is no current instrument. | Demographics |
| Form URL (Specified Instrument) | `[form-url:instrument]` | The web address (URL) of the specified data entry form for the current record and event. Replace `instrument` with the unique form name. Always points to the data entry form (for project users, who must log in), even when piped on a survey. Can be combined with event prefix: `[event-name][form-url:visit_data_form]`. | https://... |
| Form Link (Specified Instrument) | `[form-link:instrument]` or `[form-link:instrument:Custom Text]` | An HTML web link to the specified data entry form for the current record/event. Replace `instrument` with the unique form name. Optionally add custom link text; if omitted, defaults to the form label. Can be used as `[form-link]` or `[form-link:Custom Text]` wherever there is a current form (a data entry form, an alert, a survey invitation). Always opens the data entry form (for project users, who must log in), in a new tab. Can be combined with event prefix: `[next-event-name][form-link:visit_data_form]` and instance qualifier: `[form-link:visit_data_form][last-instance]`. | Visit Data Form or Click here to enter data |

---

## 4. Usage Notes

**Using `[is-form]` in Branching Logic**

The `[is-form]` smart variable is designed to detect the access context. Use it in branching logic to show or hide fields based on whether the form is being accessed as a data entry form or survey. For example: `[is-form]=1` displays fields only in the data entry context, while `[is-form]=0` displays them only in survey mode. Note that `[is-form]` is also 0 outside a data entry form page — in alerts, PDFs, background processing and the API — so `[is-form]=0` does not on its own mean "this is a survey".

**Form URL and Form Link Requirements**

To use `[form-url:instrument]` or `[form-link:instrument]`, you must know the unique form name. This can be found in the Online Designer under the form settings. Copy it exactly: where there is a current form (a data entry form, an alert, a survey invitation), REDCap treats an unrecognised first parameter as custom link text. For example, `[form-link:demograhics]` produces a working link to the *current* form labelled "demograhics" — not to the form you meant. Where there is no current form, the link may not work at all. Always test the link.

**Event Prefix for Longitudinal Projects**

In longitudinal projects, a form link without an event prefix uses the current event. To link to a form in a different event, prepend a unique event name or an event smart variable:
- `[baseline_arm_1][form-link:demographics]` generates a link to the Demographics form in the Baseline event.
- `[next-event-name][form-link:visit_data_form]` generates a link to the form in the next event.

See [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) for detailed information on event prefixes.

**Linking to a Specific Instance**

For repeating instruments, append an instance qualifier to a form link or form URL:
- `[form-link:visit][last-instance]` opens the last existing instance.
- `[form-link:visit][2]` opens instance 2.
- `[form-link:visit][new-instance]` opens a new, empty instance of the repeating form.

**Form Links Do Not Grant Access**

Form links open in a new browser tab. Building a link does not give anyone access: the person clicking it must log in to REDCap and have user rights to that form, that record and its Data Access Group. Do not send form links to participants — use a survey link instead.

**Form Link Customization**

When using `[form-link:instrument:Custom Text]`, replace "Custom Text" with your desired link label. For example:
- `[form-link:demographics:Click to enter demographics]`
- `[form-link:visit_1_assessment:Complete Visit Assessment]`

Without the custom text parameter, the link defaults to the form's label.

**Context-Dependent Instrument Variables**

`[instrument-name]` and `[instrument-label]` resolve to the current instrument on data entry forms and survey pages, in alerts (the instrument that triggered the alert) and in survey invitations (the survey's instrument). They return blank only where there is no current instrument (e.g., a dashboard or a data quality rule not tied to a specific form).

**Survey Invitations and Form Links**

In a survey invitation email, you can use `[form-link]` (without specifying an instrument) and REDCap will assume the current form. You can also use `[form-link:Custom Text]` if you want custom link text. This is convenient for survey confirmation emails that link back to a data entry form. Remember that the link opens the data entry form, so it is only useful to project users who can log in, not to participants.

---

## 5. Common Questions

**Q: How do I create a link from one form to another within the same record?**

**A:** Use `[form-link:instrument]` where `instrument` is the unique form name of the target form. For example, in the Demographics form, you might include a note that says "After completing demographics, proceed to `[form-link:visit_data_form]`." You can also customize the link text: `[form-link:visit_data_form:Click here to enter visit data]`.

**Q: What is the difference between `[instrument-name]` and `[instrument-label]`?**

**A:** `[instrument-name]` is the unique identifier used internally by REDCap (e.g., "demographics"). `[instrument-label]` is the human-readable display name (e.g., "Demographics"). Use the name when you need to reference the form in logic or other system contexts; use the label when you want to display readable text to users.

**Q: Can I use `[is-form]` in branching logic to hide survey-specific fields?**

**A:** Yes. For example, `[is-form]=1` shows a field only when the instrument is accessed as a data entry form, while `[is-form]=0` shows it only in survey mode. This allows you to customize the data collection experience based on how the form is being accessed.

**Q: I need to link to a form in a different event (longitudinal project). How do I do that?**

**A:** Use an event prefix before the form-link. For example: `[next-event-name][form-link:visit_data_form]` links to the Visit Data form in the next event. Or hard-code the event name: `[event_1_arm_2][form-link:demographics]`. See [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) for more information on event prefixes.

**Q: What happens if I use an incorrect instrument name in `[form-link:instrument]`?**

**A:** Where there is a current form (a data entry form, an alert, a survey invitation), REDCap treats the unrecognised name as custom link text, so you get a working link to the *current* form with your typo as its label — not a link to the form you meant. Where there is no current form, the link may not work. Always copy the exact instrument name from the Online Designer and test the link.

**Q: Can I use form smart variables in survey invitations sent via email?**

**A:** Yes. `[instrument-name]`, `[instrument-label]` and `[form-link]` work in survey invitation emails and refer to the survey's instrument; in alerts they refer to the instrument that triggered the alert. `[is-form]` returns 0 in emails, since no data entry form page is being viewed. Keep in mind that `[form-link]` opens the data entry form, so it is useful only to project users.

---

## 6. Common Mistakes & Gotchas

**Using incorrect or typo'd instrument names in form links.** If you type `[form-link:demograhics]` instead of `[form-link:demographics]` on a form, in an alert or in an invitation, REDCap reads "demograhics" as link text and produces a working link to the *current* form labelled "demograhics" — easy to miss, because the link works. Always copy the exact instrument name from the Online Designer and test the link before deploying to production.

**Confusing form smart variables with survey smart variables.** `[form-link]` and `[form-url]` always point to the data entry form (for project users, who must log in), even when piped on a survey; `[instrument-name]` and `[instrument-label]`, by contrast, also work on surveys. Survey-specific smart variables (survey links, survey queue links, survey timestamps) are covered in [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md). Using form variables in a survey context may not produce the expected result. Use the appropriate smart variable type for your context.

**Assuming `[instrument-name]` and `[instrument-label]` always have values.** They resolve on forms, survey pages, alerts and survey invitations, but return blank where there is no current instrument, such as dashboards or data quality rules not tied to a form.

**Assuming `[is-form]=0` means a survey.** `[is-form]` is 1 only on a data entry form page. It is also 0 in alerts, PDFs, background processing and the API. Use `[is-survey]=1` when you specifically mean "on a survey page".

**Expecting a form link to grant access.** A form link only opens the form; the person still has to log in and have rights to the form, the record and its Data Access Group.

**Not testing form links before deployment.** Form links can break if an instrument is renamed or deleted. After creating a form link, test it in a development environment to confirm it functions correctly before moving to production.

**Using form links in non-longitudinal projects without understanding event context.** In non-longitudinal projects (single-arm, single-event), form links work without event prefixes. In longitudinal projects, a form link without an event prefix uses the current event. If you mean a different event, add a unique event name or an event smart variable such as `[next-event-name]`.

---

## 7. Related Articles

- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (overview of all smart variable categories)
- [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) (event prefixes and cross-event linking)
- [RC-PIPE-08 — Smart Variables: Survey](RC-PIPE-08_Smart-Variables-Survey.md) (survey-specific smart variables for comparison)
- [RC-PIPE-09 — Smart Variables: Event & Arm](RC-PIPE-09_Smart-Variables-Event-and-Arm.md) (event smart variables for longitudinal projects)

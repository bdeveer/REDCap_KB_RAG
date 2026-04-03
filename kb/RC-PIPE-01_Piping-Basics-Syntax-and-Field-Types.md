RC-PIPE-01

**Piping — Basics, Syntax & Field Types**

| **Article ID** | RC-PIPE-01 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-02 — Online Designer |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers; RC-PIPE-03 — Smart Variables Overview; RC-PIPE-04 — Piping in Emails & Notifications; RC-BL-01 — Branching Logic Overview & Scope |

---

# 1. Overview

This article introduces REDCap's piping feature — what it is, how its basic syntax works, where piped values can appear in a project, and what each field type produces when piped. It is the entry point for the Piping knowledge base series and focuses on single-instrument, non-longitudinal projects. Advanced scenarios involving longitudinal projects, repeated instruments, and piping modifiers are covered in RC-PIPE-02.

---

# 2. Key Concepts & Definitions

**Piping**

The collective term for any REDCap feature that takes a value entered in one variable and displays or uses it somewhere else in the project. Piping is not a single UI button — it is a syntax convention that REDCap recognizes wherever text is rendered.

**Variable**

The unique identifier assigned to each field in a REDCap instrument. Variable names are set by the project designer in the Online Designer or Data Dictionary. In piping syntax, the variable name is what goes inside the brackets.

**Pipe Reference**

A variable name wrapped in square brackets — for example, `[first_name]` — placed inside a field label, option label, field note, or descriptive text field. When REDCap renders that text, it substitutes the bracket expression with the current stored value of that variable.

**Blank Substitution**

When a pipe reference resolves to a variable that has not yet been filled in, REDCap displays a blank space in place of the missing value. This is expected behavior, not an error.

**Smart Variables**

A set of bracket expressions that reference system-level information rather than participant data — for example, the current user's name, the current event, or the current instance number. Smart variables use the same bracket syntax as regular piping. They are covered in RC-PIPE-03.

---

# 3. Piping Syntax

The core piping syntax is:

```
[variable_name]
```

Opening square bracket + the variable's exact variable name + closing square bracket.

To pipe a value into another field's label, locate the target field in the Online Designer, open its edit dialog, place the bracket expression anywhere in the **Field Label** text, and save. REDCap substitutes the expression with the live value whenever the instrument is rendered.

**Example:**

Field 1 — variable name: `first_name`, label: "What is your first name?"

Field 2 — label configured as: "What is `[first_name]`'s date of birth?"

When a participant types "John" into Field 1, Field 2 displays: "What is John's date of birth?"

## 3.1 Variable Naming Recommendations

If you plan to use piping or branching logic heavily, apply these conventions when naming variables:

- **Keep names short.** `dob` is preferable to `date_of_birth`.
- **Keep names human-readable.** `fname` is preferable to `fn14zh`.
- **Add situational context when relevant.** If you collect blood pressure at multiple visits, use `bp_v1`, `bp_v2` rather than generic names.
- **Be consistent.** Once you adopt a pattern like `bp_v1`, continue it — do not switch to `bp_visit2` for subsequent variables.

Consistent, readable variable names make piping references easier to write, review, and maintain. If you need a quick reference for variable names already in your project, open the Codebook under Project Home and Design (see RC-FD-05 — Codebook).

---

# 4. Where Piping Can Be Used

Piping works anywhere REDCap displays text. The most common locations are:

**Field labels.** The question text shown to data entry users or survey respondents. This is the most common piping location.

**Choice option labels.** The visible labels for radio buttons, dropdowns, or checkbox options. For example, a radio button question "Where was `[first_name]`'s injury?" can have options labeled "`[first_name]`'s leg", "`[first_name]`'s arm", and "`[first_name]`'s head".

**Field notes.** The helper text displayed below a field during data entry. For example, a field note on an email address field could read "`[first_name]`'s primary email".

**Descriptive text fields.** A field type that displays text without capturing any data. Piping into descriptive text fields is useful for building summary displays — for example, showing a participant's entered values back to them mid-instrument.

**Survey completion text.** The message shown after a participant submits a survey. Piping participant information (such as their name) into the completion message personalizes the experience.

**Emails and notifications.** Survey confirmation emails, survey invitations, and alerts can all contain piped values. See RC-PIPE-04 — Piping in Emails & Notifications.

For a comprehensive reference of all supported locations, use REDCap's embedded help text, accessible via the purple help button in the field edit menu, the floating top-right menu in the Online Designer, or the "Design your data collection instruments" link on the Project Setup page.

---

# 5. What Each Field Type Pipes

Different field types produce different output when piped. The table below shows the default piped value for each field type.

| **Field Type** | **Default Piped Value** | **Example** |
|---|---|---|
| Text box | Entered value (raw text or number) | John |
| Notes box | Entered value (full text) | This is note box text |
| Calculated field | Result of the calculation | 12 |
| Dropdown | Label of the selected option | Vanilla |
| Radio buttons | Label of the selected option | Chocolate |
| Checkboxes | Label(s) of all checked options, comma-separated | Vanilla, Chocolate |
| Yes – No | Label of the selected option | Yes |
| True – False | Label of the selected option | True |
| Signature | Internal reference value (not the image itself) | 430002 |
| File upload | Internal reference value (not the filename) | 24578 |
| Slider | Numerical value at the slider position | 66 |
| Descriptive text | Nothing — no value is captured in this field type | n/a |
| Section header | Nothing — no value is captured in this field type | n/a |
| Dynamic query (SQL) | Label of the selected option | Vanilla |
| Matrix — radio buttons | Label of the selected option (per row) | Strawberry |
| Matrix — checkboxes | Label(s) of checked options (per row) | Vanilla, Chocolate |

> **Note:** Matrix fields can only be piped by row. To display values from an entire matrix, pipe each row individually — there is no single bracket expression that captures a whole matrix at once.

> **Note:** To pipe the raw coded value instead of the display label (for dropdowns, radio buttons, checkboxes, yes/no, true/false, and SQL fields), use the `:value` modifier. Modifiers are covered in RC-PIPE-02.

---

# 6. Blanks and Timing

## 6.1 When Values Are Blank

When REDCap evaluates a pipe reference and the referenced variable has no stored value, it substitutes a blank — the field label renders with an empty space where the value would appear. For example: "What is \_\_\_\_\_'s date of birth?"

This is not an error. It is expected behavior whenever the source variable is empty.

## 6.2 Same-Instrument Timing

If the source variable and the piping reference live on the same instrument, the displayed value updates in real time as the participant types. There is no need to save and reload.

## 6.3 Cross-Instrument Timing

If the source variable lives on a different instrument from the field that references it, the piped value only refreshes after: (1) data has been entered in the source instrument, (2) the record has been saved, and (3) the destination instrument has been reloaded or opened fresh.

## 6.4 Avoiding Blank Displays

If you do not want to display a question or label when the source variable is empty, use branching logic to hide the destination field until the source variable is filled in.

**Example branching logic** on the destination field: `[fname] <> ""`
(This means: only show this field if `fname` is not empty.)

## 6.5 Variable Order Matters

Place the source variable above the destination variable in the instrument. REDCap renders instruments top to bottom. If a pipe reference points to a variable that appears later in the instrument, the value will typically be blank when the destination field is first displayed, because the participant has not yet reached and completed the source field.

Combining correct ordering with branching logic produces instruments that flow cleanly and predictably.

---

# 7. Common Questions

**Q: What is piping in REDCap?**

**A:** Piping is the feature that lets you take a value entered in one field and display it in another part of the project — in a field label, option label, field note, descriptive text, or email. The syntax is a variable name wrapped in square brackets: `[variable_name]`.

**Q: Where do I put piping syntax in the Online Designer?**

**A:** In the Field Label, choice option labels, or Field Note of any field. For a descriptive text field, put it in the field label (since that is the only displayed content). Type the bracket expression directly into those text areas and save.

**Q: Why does my piped field show a blank instead of the value?**

**A:** The most common reasons are: (1) the source variable has not been filled in yet; (2) the source variable is on a different instrument and the current instrument was opened before data was saved there; or (3) the source variable appears below the destination variable in the instrument. Check ordering and save state first.

**Q: Can I pipe a value into a field's choice options (radio buttons, dropdowns)?**

**A:** Yes. Place the pipe reference directly in the choice label text when editing the field in the Online Designer. Each option label can contain its own pipe reference.

**Q: Does piping work in surveys and data entry forms equally?**

**A:** Yes. The same bracket syntax works in both survey and data entry (non-survey) instruments. The rendered result is the same regardless of how the instrument is being accessed.

**Q: Can I use piping in calculated fields?**

**A:** No — calculated fields use REDCap's calculation syntax, not piping. You reference other variables in a calculation expression without brackets, using a different syntax. Branching logic and action tags use a related but distinct syntax. See RC-BL-01 — Branching Logic Overview & Scope for the shared logic syntax.

**Q: What does REDCap display when I pipe a checkbox field?**

**A:** By default, REDCap displays a comma-separated list of all checked option labels — for example, "Vanilla, Chocolate". If no options are checked, the display is blank. To display unchecked options or specific choices, use checkbox modifiers covered in RC-PIPE-02.

---

# 8. Common Mistakes & Gotchas

**Pointing a pipe reference to a variable that appears later in the instrument.** If the source variable is below the destination field, the destination field renders with a blank on first load. Users rarely scroll back up to see it update. Place source variables above destination fields.

**Forgetting to save before reloading a cross-instrument reference.** If the source variable is on a different instrument, the piped value only refreshes after the source record is saved and the destination instrument is reopened. Opening the destination instrument first produces a blank.

**Piping into a field that uses coded values when you need the label.** The default piped value for dropdowns, radio buttons, and similar fields is the display label, not the raw code. If your downstream logic or display needs the raw code, use the `:value` modifier (see RC-PIPE-02). Mixing up labels and codes produces confusing output.

**Using piping references in field types that do not display text.** Piping syntax placed inside validation settings, field widths, or other non-text configuration fields has no effect and is ignored by REDCap.

**Assuming blank means broken.** A blank in a piped label is almost always a timing or ordering issue, not a configuration error. Check that the source variable is filled in and that the instrument has been reloaded after saving.

---

# 9. Related Articles

- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (cross-event piping, repeated instrument scenarios, :value and other modifiers)
- RC-PIPE-03 — Smart Variables Overview (system-level bracket expressions)
- RC-PIPE-04 — Piping in Emails & Notifications (confirmation emails, survey invitations, alerts)
- RC-FD-02 — Online Designer (where piping references are configured)
- RC-FD-05 — Codebook (quick reference for variable names when building pipe references)
- RC-BL-01 — Branching Logic Overview & Scope (using the same bracket syntax in logic conditions)

RC-FD-07

**Field Embedding**

| **Article ID** | RC-FD-07 |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; works on both instruments and surveys; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-02 — Online Designer |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FD-02 — Online Designer; RC-FD-06 — Online Designer Instrument and Field Management; RC-BL-01 — Branching Logic Overview & Scope |

---

# 1. Overview

This article covers field embedding — a REDCap feature that allows form designers to reposition where a field visually appears on an instrument or survey by embedding it inside another field's label. Field embedding does not change a field's variable name, data storage, or behavior; it only changes where the field renders on screen. The two most common applications are embedding a text box next to a specific answer choice, and using a table in a descriptive field to arrange multiple fields in a grid layout.

---

# 2. Key Concepts & Definitions

**Field Embedding**

A technique that repositions how a field renders on an instrument by referencing its variable name, in curly braces, inside the label of another field. The embedded field appears at the location of the curly-brace reference rather than in its normal sequential position in the field list.

**Descriptive Field**

A field type in REDCap that displays text, images, or HTML to the user but collects no data. Descriptive fields are the most common container for field embedding because their labels can hold Rich Text content — including tables — and curly-brace references to other fields.

**Variable Name**

The unique identifier assigned to a REDCap field at creation. Variable names are used everywhere in REDCap to reference a specific field: in branching logic, calculated fields, piping, and field embedding. Variable names cannot contain spaces.

**Curly-Brace Syntax**

The embedding reference format: `{variable_name}`. Placing this token in any field's label causes the referenced field to render at that location. The curly-brace syntax is specific to field embedding and is distinct from the square-bracket syntax used in branching logic (`[variable_name]`).

**Rich Text Editor**

The editor available within a descriptive field's label that allows HTML content — including formatted tables — to be created using a visual interface. Tables built in the Rich Text Editor are the primary tool for creating grid-style layouts with field embedding.

**@PLACEHOLDER**

An action tag that displays hint text inside an empty text-box field — similar to the grayed-out placeholder text in a web form. When a field is embedded inline (for example, next to a choice label), @PLACEHOLDER helps users understand what to enter without a separate visible label cluttering the layout.

> **Note:** Action tags are special keywords beginning with `@` that modify field behavior. They are entered in the **Action Tags / Field Annotation** section of the field edit dialog. A dedicated article covering action tags is planned — see ⚠️ RC-AT-01.

---

# 3. How Field Embedding Works

The embedding mechanism is straightforward: any field that will be embedded must already exist on the same instrument. You then reference it from another field's label using curly braces.

**Basic rules:**

- The embedded field must exist before it can be referenced. You cannot reference a variable that has not yet been created.
- The curly-brace reference and the embedded field must be on the same instrument. You cannot embed a field from a different instrument. On multi-page surveys, both the host field and the embedded field must also be on the same survey page — being on the same instrument but a different page is not sufficient.
- A field can only be embedded in one location per instrument. If you place `{variable_name}` in multiple labels on the same instrument, the behavior is unpredictable.
- Embedding only affects the visual position of the field on screen — data is still stored under the field's original variable name.
- The embedded field retains all its normal properties: validation, required status, branching logic, and action tags continue to apply.

**Syntax:**

```
{variable_name}
```

Place this token exactly where you want the field to appear — in the middle of a sentence, next to a choice label, or inside a table cell.

> **Important:** Use curly braces `{ }` for field embedding. Do not confuse this with square brackets `[ ]`, which are used in branching logic and piping syntax.

**Icons modifier:**

To display the standard field icons (Data History, Field Comments, and Missing Data Codes) next to an embedded field, append `:icons` to the variable name inside the braces:

```
{variable_name:icons}
```

Icons are not shown by default — they only appear when the `:icons` suffix is explicitly included. The `:icons` modifier works only on data entry forms; icons do not appear when the instrument is viewed as a survey.

**Valid embedding locations:**

Fields can be embedded only in the Field Label, Field Note, Section Header, or Choice Label of another field on the same instrument. The following locations do not support field embedding:

- Drop-down choice labels
- Survey instructions, acknowledgment text, and queue text
- Outgoing emails, invitations, and alerts

**Embedding a descriptive field:**

It is possible to embed a descriptive field inside another field. Because descriptive fields have no data-entry element, embedding one simply relocates its label text to the new position. This is primarily useful when the descriptive field has branching logic — it allows a block of label text to appear conditionally at a specific location on the page.

**Testing embedded fields:**

The Preview Instrument button in the Online Designer provides a limited preview of how field embedding will look, but it is less accurate than viewing the actual instrument for a real or test record. Always test in a real record before finalizing the layout.

---

# 4. Field Embedding in Choices

One common use of field embedding is displaying a text box directly next to an answer choice — most often an "Other, please specify" option in a radio button or dropdown field.

## 4.1 Setup Overview

In this pattern, three elements work together:

1. **The choice field** (e.g., a radio button asking about race/ethnicity) includes an "Other" option and the embedded variable reference in that choice's label.
2. **The embedded text field** (e.g., `other1`) captures the free-text response and has its curly-brace reference placed next to the "Other" choice label.
3. **Branching logic** on the embedded text field hides it unless the user selects "Other" — preventing the text box from appearing for all respondents.

## 4.2 Placing the Embedding Reference

To embed a field next to a specific choice:

1. Open the choice field in the field edit dialog in the Online Designer.
2. In the **Choices** section, find the answer choice where you want the text box to appear (e.g., the row for "Other").
3. In that choice's label, type the curly-brace reference directly: `Other: {other1}`.
4. Save the field.

The text box for `other1` will now render inline, immediately to the right of the "Other" label.

## 4.3 Adding Branching Logic

Without branching logic, the embedded text field renders for all respondents regardless of whether they selected "Other." Add branching logic to the embedded field so it only appears when relevant:

1. In the Online Designer, open the branching logic editor for the embedded field (`other1`).
2. Set the condition to show the field only when the parent choice equals the "Other" coded value — for example: `[radio_choices] = '5'` (where 5 is the coded value for "Other").
3. Save.

> **Note:** The branching logic condition uses square-bracket syntax (`[radio_choices]`), while the embedding reference uses curly-brace syntax (`{other1}`). Both are required and serve different purposes.

## 4.4 Using @PLACEHOLDER

When a field is embedded inline, its label may not render visibly — the label is suppressed to keep the layout clean. Use the `@PLACEHOLDER` action tag to display hint text inside the text box so users understand what to enter:

1. Open the embedded text field (`other1`) in the field edit dialog.
2. In the **Action Tags / Field Annotation** field, type: `@PLACEHOLDER="Please specify"`
3. Save.

The text box will display "Please specify" as greyed-out hint text when empty.

---

# 5. Field Embedding in Table Format

A second common application is arranging multiple fields in a grid, making dense forms — such as demographics sections — more compact and easier to read.

## 5.1 How It Works

In this pattern, a **descriptive field** acts as a visual container. Its label is edited using the Rich Text Editor to create an HTML table. Each table cell that should contain a data-entry field holds a curly-brace reference to that field's variable name. The referenced fields render inside the cells when the instrument is viewed.

## 5.2 Setup Steps

1. In the Online Designer, create all the fields you intend to embed (e.g., `first_name`, `last_name`, `dob`, `mrn`). These fields can be placed anywhere in the instrument field list — their position in the list does not affect where they render once embedded.
2. Create a **Descriptive** field where you want the table to appear.
3. Open the descriptive field's label and switch to the **Rich Text Editor**.
4. Insert a table with the layout you want (number of rows and columns appropriate for your fields).
5. In each cell that should hold a data-entry field, type the curly-brace reference: e.g., `{first_name}`.
6. In cells that serve as row or column headers, type plain label text (e.g., "First Name").
7. Save the descriptive field.

> **Tip:** Add `@PLACEHOLDER` action tags to each embedded field with a brief hint (e.g., `@PLACEHOLDER="First"`, `@PLACEHOLDER="Last"`). Because the embedded fields' own labels are suppressed, placeholders help users understand each cell's purpose without adding extra label text to the table.

## 5.3 Multiple Descriptive Fields

Large demographics sections are often split across two or more descriptive fields, each containing a separate table. This keeps each table manageable in size and allows section breaks or instructional text to appear between them. Each descriptive field operates independently — fields embedded in the first table do not interfere with fields embedded in the second.

---

# 6. Common Questions

**Q: Can I embed the same field in more than one location on the same instrument?**

**A:** No. A variable reference should appear only once per instrument. If `{variable_name}` is placed in multiple field labels on the same instrument, REDCap's behavior is undefined — the field may render in an unexpected location or not render at all. Embed each field in exactly one location.

**Q: Can I embed a field from a different instrument?**

**A:** No. Field embedding only works within the same instrument. Both the container field (holding the curly-brace reference) and the embedded field must exist on the same instrument.

**Q: Does field embedding change where the data is stored?**

**A:** No. Data is always stored under the field's original variable name regardless of where the field visually appears. Embedding only affects the rendered position on screen.

**Q: Can I use field embedding on surveys as well as data entry instruments?**

**A:** Yes. Field embedding works identically on surveys and standard data entry instruments. The same curly-brace syntax applies in both contexts.

**Q: Can I embed a field without adding branching logic?**

**A:** Yes — branching logic is not required for field embedding. It is commonly added in the "embedding next to a choice" pattern to hide the embedded field unless the relevant choice is selected, but it is a separate, optional layer. If you omit branching logic, the embedded field renders for all users at all times.

**Q: What is the difference between curly braces and square brackets in REDCap?**

**A:** Curly braces `{variable_name}` are the field embedding syntax — they control visual position on screen. Square brackets `[variable_name]` are the logic and piping syntax — they are used in branching logic, calculated fields, and piping to reference a field's value. The two syntaxes serve entirely different purposes and are not interchangeable.

**Q: Does field embedding work in the REDCap Mobile App?**

**A:** No. Field embedding is not supported in the REDCap Mobile App. If a project with embedded fields is downloaded to the Mobile App, the fields will not display in their embedded positions — the instrument will look different from how it appears in the web browser.

**Q: Can a field that is itself embedded serve as a host for other embedded fields?**

**A:** Partially. A field cannot be embedded inside its own Field Label, and a field cannot be embedded in another field's Field Label or Field Note if that second field is also embedded elsewhere — doing so produces an error when the instrument is viewed. However, a field *can* be embedded into a Choice Label of a multiple-choice field (radio or checkbox, but not a drop-down) that is itself embedded elsewhere. REDCap refers to this as compound embedding.

---

# 7. Common Mistakes & Gotchas

**Using square brackets instead of curly braces.** The most frequent mistake when first learning field embedding is typing `[variable_name]` (branching logic syntax) instead of `{variable_name}` (embedding syntax). Square brackets in a field label are interpreted as piping, not embedding. The field will not reposition — the reference will be replaced by the field's current value, which is likely blank. Always use curly braces for embedding.

**Embedding a field that does not yet exist.** REDCap will not flag an unrecognised variable name in a curly-brace reference at save time. If the variable name is misspelled or the field has not been created yet, the curly-brace token will simply not render — the embedded field will be absent from the form with no error message. Always create the target field first, then add the embedding reference.

**Expecting the field's label to display alongside the embedded field.** When a field is embedded, its own label text does not render at the embedding location. Only the field input element (text box, radio buttons, etc.) appears. If you need a visible label, include it in the container field's label text, adjacent to the curly-brace reference, or use `@PLACEHOLDER` to add inline hint text. Note that the field's label is still used when viewing reports and exported data, even though it is suppressed on the instrument — always give embedded fields a meaningful Field Label so that reports remain interpretable.

**Placing the embedding reference and the embedded field on different instruments.** If you add `{variable_name}` to a field on Instrument A, but `variable_name` belongs to Instrument B, the reference will silently fail. Both fields must be on the same instrument.

**Forgetting to add branching logic in the "Other, please specify" pattern.** If branching logic is omitted, the embedded text box renders for every respondent — not just those who selected "Other." Always pair the embedding reference with appropriate branching logic when the field should be conditional.

**The host field's branching logic hides all fields embedded within it.** If the host field (the one containing the curly-brace references) has its own branching logic and that logic evaluates to FALSE, all fields embedded inside it will also be hidden — they are treated as part of the host field. On data entry forms (not surveys), if any embedded field has a saved value when the host field is being hidden, REDCap will prompt "Erase current value of the field?" for each affected embedded field. If the user clicks Cancel for any of these prompts, the host field will remain visible rather than being hidden.

**The Record ID field cannot be embedded.** The first field in a REDCap project (the record identifier) is a special system field and cannot be repositioned via field embedding.

**Field embedding does not work in the REDCap Mobile App.** If a project with embedded fields is loaded into the Mobile App, the fields will not render in their embedded positions — the layout will look different from what is configured on the web instrument.

---

# 8. Related Articles

- RC-FD-02 — Online Designer (the tool used to create fields and configure embedding)
- RC-FD-06 — Online Designer Instrument and Field Management (managing field order and instrument structure)
- RC-BL-01 — Branching Logic Overview & Scope (frequently used alongside field embedding to control field visibility)
- RC-BL-02 — Branching Logic Syntax & Atomic Statements (writing the logic conditions used with embedded fields)
- ⚠️ RC-AT-01 — Action Tags (covers @PLACEHOLDER and other action tags used to refine embedded field behavior)

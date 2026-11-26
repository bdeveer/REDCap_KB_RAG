

**Online Designer – Advanced Options: Quick-Modify, Field Navigator, and Custom CSS**

| **Article ID** | [RC-FD-11 — Online Designer – Advanced Options: Quick-Modify, Field Navigator, and Custom CSS](RC-FD-11_Advanced-Online-Designer-Options.md) |
|---|---|
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Online Designer multi-field actions, Field Navigator and custom CSS behaviour checked against source code; pages not re-captured. Multi-field Delete and Convert were also live-checked earlier |
| **Prerequisite** | [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) |
| **Version** | 1.5 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md); [RC-FD-07 — Field Embedding](RC-FD-07_Field-Embedding.md); [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md); [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md); [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)|
| **Synonyms** | edit multiple fields at once; quick modify fields bulk action; jump to a field by variable name; field navigator in the online designer; add custom css to an instrument; style a form or survey with css; bulk apply changes to selected fields; advanced online designer shortcuts; background image on a survey disappeared; where to host an image used in survey css |

---

## 1. Overview

This article covers three advanced capabilities of the Online Designer instrument editor that experienced designers use to work more efficiently on larger instruments:

- **Quick-modify field(s)** — a bulk-action toolbar that lets you select multiple fields at once and apply the same change (move, copy, delete, edit branching logic, set alignment, and more) across all of them in one operation.
- **Field Navigator** — a keyboard-accessible widget for jumping directly to any field by variable name, without scrolling through a long instrument.
- **Custom CSS styling** — a per-instrument CSS editor that injects additional styling into the rendered data entry form.

All three features are accessed from within an open instrument in the Online Designer. The one exception is the Field Navigator keyboard shortcut, which also works from the instrument list on newer versions (see Section 3.2).

---

## 2. Quick-Modify Field(s)

### 2.1 What It Does

Quick-modify is a multi-field selection and bulk-action system built into the instrument editor. Instead of opening each field individually to make the same change across many fields, you select the fields you want, then apply a single action to all of them at once.

Common use cases include bulk-setting alignment on a group of choice fields, applying the same action tag to a set of text boxes, copying a block of fields to reuse in another instrument, or mass-deleting fields during a redesign.

### 2.2 Activating the Toolbar

Check the checkbox in the **upper-right corner** of any field card in the instrument editor, or **Ctrl-click** (Windows/Linux) / **Cmd-click** (Mac) the field. As soon as at least one field is selected, the **Quick-modify field(s) toolbar** opens as a pop-over attached to the current field. A **Show:** setting in the toolbar lets you place it **On Side** (the default) or **Overlaid** on the field. You can continue checking additional field checkboxes to grow the selection. Selected fields are visually highlighted. The record ID field cannot be selected.

Bulk actions are only available while the instrument can be edited: in Development, or in Draft Mode for a production project.

To clear the entire selection without taking any action, click the **Clear selection** button (×) in the toolbar.

### 2.3 Available Actions

The toolbar is organized into two rows. The top row contains the primary structural actions; the bottom row contains property-level bulk actions.

#### Primary actions (top row)

| Action | Description | Constraints |
| --- | --- | --- |
| **Copy** | Copies all selected fields and inserts them at a position you choose | Placement options: after each original field, or all together after the last selected field (not available when the selection mixes matrix and non-matrix fields). Tick **Replace the selection with the newly created fields** to have the copies selected afterwards. New names are generated automatically: a trailing number is incremented, keeping any zero-padding (`q01` → `q02`, or the next free number), otherwise `_2` is added. Renaming is optional but recommended |
| **Move** | Moves all selected fields to a position you choose, on this or another instrument | All or nothing: the button is disabled unless every selected field is outside a matrix, or every selected field belongs to the same matrix group |
| **Delete** | Deletes all selected fields | Asks for confirmation. In Production the deletion goes into the draft like any other change and needs review if the fields hold data. The data is no longer accessible but is not purged, and it can reappear if a field with the same variable name is created again (see [RC-FD-06](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md)). A randomization field (allocation or strata) cannot be deleted, and including one stops the whole batch. Delete and Move are disabled for a MyCap baseline date field |
| **Convert** | Converts selected fields into a matrix group | Fields must be adjacent to each other, must all be Radio, Yes/No, True/False or Checkbox (these can be mixed), and must not already belong to a matrix group. Every field takes the first field's type (Checkbox stays Checkbox; anything else becomes Radio) and choices, so the other fields' choices are overwritten. Field notes and custom alignment are cleared on all selected fields, and section headers are removed except the first. Check that all choices are identical first |
| **Edit Branching Logic** | Opens a bulk branching logic dialog | Three modes: clear the logic on all selected fields, copy the current field's logic to the others, or set new logic on all of them (replacing what was there) |
| **Edit Action Tags** | Opens the action tag editor for all selected fields | Modes: clear, add (appended to existing tags), deactivate, reactivate, or copy from the current field. Useful for applying the same tag (e.g., `@HIDDEN-SURVEY`) to many fields at once |
| **Edit Choices** | Opens a bulk choices editor | Only available when all selected fields are choice-type fields (radio, dropdown, checkbox, yes-no, true-false). Modes: copy the current field's choices to the others, append choices, or convert the field type to radio, checkbox or dropdown (with an autocomplete option). Yes/No and True/False fields are skipped; a matrix field applies the change to its whole group, and a matrix cannot be converted to dropdown |

#### Property-level actions (bottom row)

| Action | Description | Constraints |
| --- | --- | --- |
| **Required ON / OFF** | Marks all selected fields as required or not required | Descriptive fields are skipped. OFF asks for confirmation |
| **Identifier ON / OFF** | Marks all selected fields as PHI identifiers or clears that flag | Descriptive fields are skipped. OFF asks for confirmation |
| **Set Alignment** | Applies one of four alignment codes to all selected fields: **RV** (Right/Vertical), **RH** (Right/Horizontal), **LV** (Left/Vertical), **LH** (Left/Horizontal) | Matrix fields are skipped. See [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) Section 5.12 for a full explanation of alignment codes |

> **Version caveat (17.x):** Copy's third placement option, **Copy to clipboard**, and the matching **Paste fields** button exist in 17.x but not in 16 LTS. They let you paste the copied fields into another instrument, another project or another REDCap instance. On 16 LTS, copy the fields on the same instrument and **Move** the copies to another instrument, or use the Data Dictionary to transfer fields to another project.

#### Keyboard shortcuts (toolbar open)

| Key | Action |
| --- | --- |
| **↑ / ↓** | Go to the previous / next selected field |
| **Ctrl/Cmd + ↑ / ↓** | Expand the selection up / down |
| **Space** | Open the Modify selection panel (Section 2.5) |
| **Backspace** | Deselect the current field |
| **Escape** | Close the toolbar |

### 2.4 Navigating Within the Selection

Once you have multiple fields selected, two small **prev / next** arrows appear in the toolbar. These scroll the page to each selected field in order, which is useful for verifying your selection on long instruments before committing to a bulk action.

From 17.4.4 (Standard), the selection controls are more prominent, and pressing **Escape** is handled more consistently when working in the toolbar.

> **Version caveat (present in 17.6 Standard, not in 17.3 LTS):** when the Modify selection panel (Section 2.5) is open, **Escape** closes that panel first rather than the whole toolbar. On 17.3 LTS, close the panel with its own button if you want to keep the toolbar and your place in it.

### 2.5 Expanding the Selection with the Modify Selection Panel

For instruments with many fields, manually checking individual checkboxes is slow. The **Modify selection** control in the Quick-modify toolbar opens the **selection expansion panel**, which lets you build or refine your selection by direction and field type filter.

> **Version caveat (present in 17.6 Standard, not in 17.3 LTS):** the control is a labelled **Modify selection…** button. On 17.3 and 16 LTS it is a list-check icon next to the **Clear selection** button.

#### Direction controls

| Option | Behavior |
| --- | --- |
| **All** | Selects all fields on the instrument (top to bottom) |
| **Top** | Expands selection upward from the current field |
| **Bottom** | Expands selection downward from the current field |
| **First to Last** | Selects all fields between the first and last currently-selected field |
| **Up** | Selects all fields between the current field and the next selected field above it |
| **Down** | Selects all fields between the current field and the next selected field below it |

#### Field type filters

The panel has an **Include** row and an **Exclude** row of field type filters, 20 in all: Radio, Yes/No, True/False, Dropdown, Checkbox, Text (any validation), Number (any numeric validation), Date/Time, Email, Phone, Notes (textarea), Signature, Slider, File upload, Descriptive, Calculated, SQL, Matrix fields, Required and Identifier.

When a filter is active, only fields matching (or, in the Exclude row, not matching) that type within the chosen direction are affected. This lets you do things like "select all email text boxes on this instrument" in two clicks.

#### Add vs. Replace

- **Add new selections** — adds the matching fields to your current selection without clearing existing selections.
- **Replace existing selections** — discards the current selection and replaces it entirely with the fields matching the current direction and type filter.

---

## 3. Field Navigator

### 3.1 What It Does

The Field Navigator is a "Go to field" widget that lets you jump directly to any field in the instrument editor by typing part of its variable name or label. On instruments with dozens or hundreds of fields, this eliminates the need to scroll.

### 3.2 Accessing It

The Field Navigator appears in the floating **help/tips panel** on the right side of the instrument editor (labeled "Field Navigator" with a compass icon). You can also activate it at any time using the keyboard shortcut:

- **CTRL-G** on Windows/Linux
- **CMD-G** on Mac

> **Version caveat (present in 17.6 Standard, not in 17.3 LTS):** Ctrl/Cmd-G also works from the instrument list. On 17.3 and 16 LTS, open an instrument first, then press the shortcut.

### 3.3 How to Use It

Type a variable name or part of a label into the Go to field search box. REDCap matches against both variable names and field labels. The list covers every instrument in the project, with the current instrument first. Picking a field on the current instrument scrolls the editor to it and selects it; picking one on another instrument opens that instrument. The selected field is then available as the starting point for a Quick-modify expansion (see Section 2.5).

---

## 4. Custom CSS Styling

### 4.1 What It Does

Each instrument in the Online Designer has an optional **Custom CSS** editor. CSS entered here is injected into the rendered data entry form for that instrument only. It is not applied when the instrument is shown as a survey; surveys use the separate Custom CSS on the Survey Settings page (see the box below). This allows designers to apply visual styling — hiding elements, changing font sizes, adding spacing, colorizing section headers — beyond what REDCap's built-in alignment and section header settings provide.

Custom CSS is **instrument-scoped**: CSS saved on one instrument does not affect other instruments in the project.

> **Important — there are two separate Custom CSS controls, not one.** From **15.5.0** REDCap has both:
>
> - **Form-level CSS** — set on the field-level Online Designer page, described in this section. Applies to the **data entry form** only.
> - **Survey-level CSS** — set on the **Survey Settings** page for an individual survey. Applies to the **survey page** only.
>
> They are independent. CSS entered in one does **not** apply to the other, so an instrument used both as a form and as a survey needs both if you want consistent styling in each context.

Two consequences of that split are easy to be caught by:

| Behaviour | Form-level CSS | Survey-level CSS |
| --- | --- | --- |
| Subject to **Draft Mode** in production | **Yes** — changes require approval, and the draft review page shows a side-by-side comparison | **No** — changes take effect immediately |
| Copyable to other instruments | No — and **Copy instrument** does not carry it over. It is kept when the whole project is copied and is included in the project XML export | **Yes** — via **"Copy design to other surveys"** on the Survey Settings page |

The draft-mode asymmetry is the one that surprises people: in a production project, editing form CSS goes through review while editing survey CSS is live immediately.

> **Critical — REDCap does not guarantee its own selectors.** Both CSS settings carry this warning verbatim: *"Use with caution. Please note that targeting internal REDCap elements (e.g., specific classes or IDs) may break without notice, as updates to REDCap can change or remove these elements at any time. Stability of these selectors across versions is not guaranteed, and any changes to them will not be announced in advance."*
>
> Given REDCap ships roughly weekly, treat custom CSS that targets internal classes as something to re-check after upgrades — it will fail silently and visually, not with an error. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

### 4.2 Accessing the CSS Editor

Open an instrument in the Online Designer. Near the instrument's action toolbar (same row as the Survey settings button), look for the palette icon button labeled **"Add custom CSS styling"** (or **"Edit custom CSS styling"** if CSS has already been saved for this instrument). Clicking it opens the CSS Editor dialog.

### 4.3 Writing CSS

The CSS editor accepts standard CSS. Important rules:

- **Do not include `<style>` tags** — REDCap wraps your CSS in a `<style>` block automatically when rendering the page. If you include the tags yourself, REDCap silently removes them; the CSS inside still works, but leave them out so the saved CSS is what you see.
- **Standard CSS comments are supported** using the `/* your comment here */` syntax. Comments are ignored during processing and have no effect on rendering.
- **Host any image the CSS loads somewhere you control.** A `background-image: url(...)` pointing at a free image-hosting site works until that site deletes the image or a respondent's network blocks it. Use a file your institution hosts, such as a public link to a file in the project's File Repository.
- There is a **Fullscreen Mode** button in the editor dialog for working with longer stylesheets.
- Click **Update & Close Editor** when finished to save and close the dialog. The CSS is saved when you return to the instrument editor.

### 4.4 Where the CSS Is Applied

The CSS applies to the **rendered data entry form** — what staff see when entering data in the instrument. It does not affect the survey page (use the survey's own Custom CSS in **Survey Settings** for that), nor how the instrument looks inside the Online Designer itself.

### 4.5 Stability Warning

> **⚠️ Use with caution.** CSS that targets specific REDCap internal element classes or IDs (e.g., `.rc-field-label`, `#questiontable`) may **break without notice**. REDCap updates can change or remove internal class names at any time, and changes of this kind are not announced in the release notes. Stability of selectors targeting internal REDCap structure is not guaranteed across REDCap versions.

For the most durable CSS, target the `id` attributes that REDCap generates from your own variable names (e.g., `#my_variable_name-tr` for a field's row, or `#my_variable_name-sh-tr` for its section header row) rather than internal REDCap class names, as variable-based IDs are stable as long as you don't rename the variable.

### 4.6 Relationship to the Data Dictionary and Survey Settings

The **Survey Settings bulk CSV export/import** has a `custom_css` column. It holds the **survey-level** CSS, not the form-level CSS described in this section. If your institution uses bulk Survey Settings import to manage project configurations, this column can be used to transfer or apply survey CSS programmatically. Form-level CSS travels with the project XML export or a project copy. See [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) for more on the Survey Settings page.

---

## 5. Common Questions

**Q: I selected 20 fields, but the Move button is disabled. What happened?**

**A:** Move is all or nothing. It is only available when every selected field is outside a matrix, or every selected field belongs to the same matrix group. A selection that mixes matrix and non-matrix fields, or spans two matrix groups, cannot be moved. Split the selection and move each group separately. A MyCap baseline date field in the selection also disables Move.

**Q: The Convert to Matrix button is greyed out even though I have several radio fields selected. Why?**

**A:** Three conditions must all be true: the fields must be directly adjacent to each other in the instrument (no other fields between them), they must all be Radio, Yes/No, True/False or Checkbox, and none of them may already belong to a matrix group. If any field in the selection fails one of these conditions, the Convert button is unavailable.

**Q: My custom CSS works on the data entry form but has no effect on the survey. Why?**

**A:** Form-level CSS from the Online Designer applies to the data entry form only. The survey page uses its own Custom CSS, set on the survey's **Survey Settings** page. Add the CSS there too. The two pages have different HTML structures, so a selector that works on the data entry form may need adjusting for the survey.

**Q: Can I share CSS between instruments or apply one stylesheet to the whole project?**

**A:** No. The CSS editor is per-instrument. If you need the same styling across all instruments, you would need to add the same CSS to each one. An alternative approach is to use a REDCap External Module that supports project-wide custom CSS injection, if one is available on your instance.

**Q: Does the Field Navigator search field labels or only variable names?**

**A:** The Go to field widget searches both variable names and field labels, across all instruments in the project. Typing part of either will match fields, so you can search by the question text if you don't remember the variable name.

---

## 6. Common Mistakes & Gotchas

- **Including `<style>` tags in the CSS editor**: the editor expects raw CSS rules. REDCap silently removes `<style>` tags, so the CSS still works, but leave them out so what you save matches what runs.

- **Expecting bulk alignment to behave the same on every field type**: the Left codes (LV, LH) also affect text boxes, notes, dropdowns, file upload and slider fields, placing the input under the label on the left. The Vertical/Horizontal part only matters for radio and checkbox fields. Bulk alignment skips matrix fields.

- **Accepting Quick-modify Copy's generated names without a look**: REDCap names the copies automatically (incrementing a trailing number such as `q01` → `q02`, or adding `_2`). The names are unique and usable, but review them so they stay meaningful.

- **Using Quick-modify Delete without checking for data**: in Production, deletion goes into Draft Mode like any other change, and fields holding data need review before the change is approved — after which that data is no longer accessible. In Development, deletion is immediate, including any test data. Always confirm the fields are empty or that the data is intentionally disposable before bulk-deleting.

- **Loading images from a third-party image host**: CSS such as `background-image: url("https://<free-image-host>/abc.png")` depends on a site the project doesn't control. If the image is removed, or a respondent's institution or country blocks the host, the background disappears with no error. This happens on surveys sent to many organizations, where some networks block the host. Host the image yourself (for example, a public File Repository link) and reference that URL. The same applies to `<style>` blocks placed in descriptive field labels to style a survey.

- **Forgetting that CSS selectors targeting internal REDCap class names can break**: if a REDCap upgrade removes or renames a class your CSS relies on, the styling silently stops working (or causes visual glitches). Keep a record of any custom CSS in use so it can be re-evaluated after version upgrades.

---

## 7. Related Articles

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (prerequisite — overview and Development vs. Production behavior)
- [RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) (prerequisite — field types, alignment, field notes, field annotation, individual field editing)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (alternative tool for bulk restructuring that Quick-modify cannot perform, such as splitting instruments)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (alignment code reference in Section 5.12)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (background on branching logic editing, used by the Quick-modify branching logic action)
- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) (background on action tags, used by the Quick-modify action tag editor)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) (Survey Settings bulk CSV, which exposes the `custom_css` column)

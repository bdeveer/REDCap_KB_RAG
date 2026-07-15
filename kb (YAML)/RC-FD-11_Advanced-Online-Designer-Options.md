---
id: RC-FD-11
title: 'Online Designer – Advanced Options: Quick-Modify, Field Navigator, and Custom
  CSS'
domain: Form Design
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
prerequisites:
- RC-FD-02 — Online Designer
- RC-FD-06 — Online Designer – Instrument and Field Management
version: '1.0'
last_updated: '2026-05-06'
related:
- id: RC-FD-03
  title: Data Dictionary
- id: RC-FD-07
  title: Field Embedding
- id: RC-FD-08
  title: 'Data Dictionary: Column Reference & Advanced Techniques'
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
- id: RC-AT-01
  title: 'Action Tags: Overview'
tags:
- form design
- instruments
synonyms:
- edit multiple fields at once
- quick modify fields bulk action
- jump to a field by variable name
- field navigator in the online designer
- add custom css to an instrument
- style a form or survey with css
- bulk apply changes to selected fields
- advanced online designer shortcuts
---

# 1. Overview

This article covers three advanced capabilities of the Online Designer instrument editor that experienced designers use to work more efficiently on larger instruments:

- **Quick-modify field(s)** — a bulk-action toolbar that lets you select multiple fields at once and apply the same change (move, copy, delete, edit branching logic, set alignment, and more) across all of them in one operation.
- **Field Navigator** — a keyboard-accessible widget for jumping directly to any field by variable name, without scrolling through a long instrument.
- **Custom CSS styling** — a per-instrument CSS editor that injects additional styling into the rendered form or survey page.

All three features are accessed from within an open instrument in the Online Designer. They are not available from the instrument list view.

---

# 2. Quick-Modify Field(s)

## 2.1 What It Does

Quick-modify is a multi-field selection and bulk-action system built into the instrument editor. Instead of opening each field individually to make the same change across many fields, you select the fields you want, then apply a single action to all of them at once.

Common use cases include bulk-setting alignment on a group of choice fields, applying the same action tag to a set of text boxes, copying a block of fields to reuse in another instrument, or mass-deleting fields during a redesign.

## 2.2 Activating the Toolbar

Check the checkbox in the **upper-right corner** of any field card in the instrument editor. As soon as at least one field is selected, the **Quick-modify field(s) toolbar** appears as a sticky bar at the top of the instrument editor. You can continue checking additional field checkboxes to grow the selection. Selected fields are visually highlighted.

To clear the entire selection without taking any action, click the **Clear selection** button (×) in the toolbar.

## 2.3 Available Actions

The toolbar is organized into two rows. The top row contains the primary structural actions; the bottom row contains property-level bulk actions.

### Primary actions (top row)

| Action | Description | Constraints |
| --- | --- | --- |
| **Copy** | Copies all selected fields and inserts them at a position you choose | Provides a prompt to place the copies; you will need to rename variable names afterward since all names must be unique |
| **Move** | Moves all selected fields to a position you choose | Certain field-type combinations cannot be moved together; matrix group fields can only be moved to positions within their own matrix group |
| **Delete** | Permanently deletes all selected fields | Irreversible; fields with data in Production cannot be deleted |
| **Convert** | Converts selected fields into a matrix group | Fields must be adjacent to each other, must all be of type Radio or Checkbox, and must not already belong to a matrix group |
| **Edit Branching Logic** | Opens the branching logic editor pre-populated with the selected fields | Lets you write or update the same logic across multiple fields in sequence |
| **Edit Action Tags** | Opens the action tag editor for all selected fields | Useful for applying the same tag (e.g., `@HIDDEN-SURVEY`) to many fields at once |
| **Edit Choices** | Opens a bulk choices editor | Only available when all selected fields are choice-type fields (radio, dropdown, checkbox, yes-no, true-false) |

### Property-level actions (bottom row)

| Action | Description | Constraints |
| --- | --- | --- |
| **Required ON / OFF** | Marks all selected fields as required or not required | — |
| **Identifier ON / OFF** | Marks all selected fields as PHI identifiers or clears that flag | — |
| **Set Alignment** | Applies one of four alignment codes to all selected fields: **RV** (Right/Vertical), **RH** (Right/Horizontal), **LV** (Left/Vertical), **LH** (Left/Horizontal) | See [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) Section 5.12 for a full explanation of alignment codes |
| **Set Validation** | Sets a text box validation type for all selected fields | Only applies to Text Box fields; has no effect on other field types |
| **Edit Sliders** | Opens the slider configuration editor | Only applies when all selected fields are Slider type |
| **Edit Field Notes** | Opens a field note editor for all selected fields | Applies the same note text to every selected field |

## 2.4 Navigating Within the Selection

Once you have multiple fields selected, two small **prev / next** arrows appear in the toolbar. These scroll the page to each selected field in order, which is useful for verifying your selection on long instruments before committing to a bulk action.

## 2.5 Expanding the Selection with the QEES Panel

For instruments with many fields, manually checking individual checkboxes is slow. The **expand** button (↕ icon) in the Quick-modify toolbar opens the **selection expansion panel**, which lets you build or refine your selection by direction and field type filter.

### Direction controls

| Option | Behavior |
| --- | --- |
| **All** | Selects all fields on the instrument (top to bottom) |
| **Top** | Expands selection upward from the current field |
| **Bottom** | Expands selection downward from the current field |
| **First to Last** | Selects all fields between the first and last currently-selected field |
| **Up** | Selects all fields between the current field and the next selected field above it |
| **Down** | Selects all fields between the current field and the next selected field below it |

### Field type inclusion filters

The inclusion row limits which field types are included in the expansion. Available filters: Radio, Yes/No, True/False, Dropdown, Checkbox, Text (any validation), Number (any numeric validation), Date/Time, Email, Phone, Notes (textarea), Signature, Slider.

When a filter is active, only fields matching that type (within the chosen direction) are added. This lets you do things like "select all email text boxes on this instrument" in two clicks.

### Add vs. Replace

- **Add** — adds the matching fields to your current selection without clearing existing selections.
- **Replace** — discards the current selection and replaces it entirely with the fields matching the current direction and type filter.

---

# 3. Field Navigator

## 3.1 What It Does

The Field Navigator is a "Go to field" widget that lets you jump directly to any field in the instrument editor by typing part of its variable name or label. On instruments with dozens or hundreds of fields, this eliminates the need to scroll.

## 3.2 Accessing It

The Field Navigator appears in the floating **help/tips panel** on the right side of the instrument editor (labeled "Field Navigator" with a compass icon). You can also activate it at any time using the keyboard shortcut:

- **CTRL-G** on Windows/Linux
- **CMD-G** on Mac

## 3.3 How to Use It

Type a variable name or part of a label into the Go to field search box. REDCap will match against field variable names and scroll the instrument editor to the matching field, selecting it in the process. The selected field is then available as the starting point for a Quick-modify expansion (see Section 2.5).

---

# 4. Custom CSS Styling

## 4.1 What It Does

Each instrument in the Online Designer has an optional **Custom CSS** editor. CSS entered here is injected into the rendered data entry form and survey page for that instrument only. This allows designers to apply visual styling — hiding elements, changing font sizes, adding spacing, colorizing section headers — beyond what REDCap's built-in alignment and section header settings provide.

Custom CSS is **instrument-scoped**: CSS saved on one instrument does not affect other instruments in the project.

## 4.2 Accessing the CSS Editor

Open an instrument in the Online Designer. Near the instrument's action toolbar (same row as the Survey settings button), look for the palette icon button labeled **"Add custom CSS styling"** (or **"Edit custom CSS styling"** if CSS has already been saved for this instrument). Clicking it opens the CSS Editor dialog.

## 4.3 Writing CSS

The CSS editor accepts standard CSS. Important rules:

- **Do not include `<style>` tags** — REDCap wraps your CSS in a `<style>` block automatically when rendering the page. If you include the tags yourself, they will appear as literal text.
- **Standard CSS comments are supported** using the `/* your comment here */` syntax. Comments are ignored during processing and have no effect on rendering.
- There is a **Fullscreen Mode** button in the editor dialog for working with longer stylesheets.
- Click **Update & Close Editor** when finished to save and close the dialog. The CSS is saved when you return to the instrument editor.

## 4.4 Where the CSS Is Applied

The CSS applies to the **rendered data entry form and survey page** — what users see when filling in the instrument. It does not affect how the instrument looks inside the Online Designer itself.

## 4.5 Stability Warning

> **⚠️ Use with caution.** CSS that targets specific REDCap internal element classes or IDs (e.g., `.rc-field-label`, `#questiontable`) may **break without notice**. REDCap updates can change or remove internal class names at any time, and changes of this kind are not announced in the release notes. Stability of selectors targeting internal REDCap structure is not guaranteed across REDCap versions.

For the most durable CSS, target the `id` attributes that REDCap generates from your own variable names (e.g., `#row-my_variable_name`) rather than internal REDCap class names, as variable-based IDs are stable as long as you don't rename the variable.

## 4.6 Relationship to the Data Dictionary and Survey Settings

Custom CSS is stored internally and is also exposed in the **Survey Settings bulk CSV export/import** as the `custom_css` column. If your institution uses bulk Survey Settings import to manage project configurations, this column can be used to transfer or apply CSS programmatically. See [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) for more on the Survey Settings page.

---

# 5. Common Questions

**Q: I selected 20 fields and clicked Move, but only some of them moved. What happened?**

**A:** Certain field combinations cannot be moved together. Most commonly, matrix group fields cannot be moved outside their matrix group — they can only be repositioned within it. REDCap will move compatible fields and skip those it cannot move. Review your selection for matrix fields and move those separately from within the matrix editor.

**Q: The Convert to Matrix button is greyed out even though I have several radio fields selected. Why?**

**A:** Three conditions must all be true: the fields must be directly adjacent to each other in the instrument (no other fields between them), they must all be of type Radio or Checkbox, and none of them may already belong to a matrix group. If any field in the selection fails one of these conditions, the Convert button is unavailable.

**Q: My custom CSS works in Development but looks wrong on the survey. Why?**

**A:** The CSS editor applies the same CSS to both the data entry form (staff view) and the survey page (participant view). However, the two pages have different HTML structures — a selector that targets a data entry element may not exist on the survey page, and vice versa. Test CSS on both views, or scope your selectors to the view you intend to style.

**Q: Can I share CSS between instruments or apply one stylesheet to the whole project?**

**A:** No. The CSS editor is per-instrument. If you need the same styling across all instruments, you would need to add the same CSS to each one. An alternative approach is to use a REDCap External Module that supports project-wide custom CSS injection, if one is available on your instance.

**Q: Does the Field Navigator search field labels or only variable names?**

**A:** The Go to field widget searches both variable names and field labels. Typing part of either will match fields, so you can search by the question text if you don't remember the variable name.

---

# 6. Common Mistakes & Gotchas

- **Including `<style>` tags in the CSS editor**: the editor only accepts raw CSS rules. Adding `<style>` tags causes them to appear as literal text on the rendered form, which looks wrong and may break layout.

- **Applying bulk alignment to fields that don't support alignment**: alignment codes (RV, RH, LV, LH) only have a visible effect on choice fields (radio, checkbox, dropdown). Applying them to text boxes or notes fields via Quick-modify does no harm but also does nothing visible.

- **Assuming Quick-modify Copy creates usable duplicates immediately**: copied fields retain their original variable names with a numeric suffix added by REDCap, but you still need to review and update each variable name to confirm it is meaningful and unique before moving on.

- **Using Quick-modify Delete without checking for data**: in Production mode, fields with data cannot be deleted and REDCap will block the action — but in Development mode, deletion is immediate and permanent including any test data. Always confirm the fields are empty or that the data is intentionally disposable before bulk-deleting.

- **Forgetting that CSS selectors targeting internal REDCap class names can break**: if a REDCap upgrade removes or renames a class your CSS relies on, the styling silently stops working (or causes visual glitches). Keep a record of any custom CSS in use so it can be re-evaluated after version upgrades.

---

# 7. Related Articles

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (prerequisite — overview and Development vs. Production behavior)
- [RC-FD-06 — Online Designer – Instrument and Field Management](RC-FD-06_Online-Designer-Instrument-and-Field-Management.md) (prerequisite — field types, alignment, field notes, field annotation, individual field editing)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (alternative tool for bulk restructuring that Quick-modify cannot perform, such as splitting instruments)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (alignment code reference in Section 5.12)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)(background on branching logic editing, used by the Quick-modify branching logic action)
- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)(background on action tags, used by the Quick-modify action tag editor)
- [RC-SURV-02 — Survey Settings: Basic Options & Design](RC-SURV-02_Survey-Settings-Basic-Options-and-Design.md) (Survey Settings bulk CSV, which exposes the `custom_css` column)

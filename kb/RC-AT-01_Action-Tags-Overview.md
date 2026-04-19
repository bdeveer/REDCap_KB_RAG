RC-AT-01

**Action Tags — Overview**

| **Article ID** | RC-AT-01 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-02 — Online Designer; foundational Project Build & Management knowledge |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-02 through RC-AT-07 (category articles); RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary |

---

# 1. Overview

This article introduces REDCap's action tags feature — what action tags are, why they exist, how to find the ones available in your project, and the three ways to add them to a field. It is the entry point for the Action Tags knowledge base series.

---

# 2. Key Concepts & Definitions

**Action Tag**

A short keyword starting with `@` that is placed in the *Action Tags / Field Annotation* box of a REDCap field. Action tags modify the standard behavior of that field. For example, `@HIDDEN` hides the field from view; `@WORDLIMIT=10` caps input at ten words.

**Parameter**

Some action tags require additional information to function. Parameters are placed immediately after the tag name, inside quotes or parentheses depending on the tag. For example, `@HIDECHOICE='1'` hides the option with raw value `1`. Tags without parameters (e.g., `@HIDDEN`) are used on their own.

**Raw Value**

The internal code assigned to each option in a radio button, dropdown, or checkbox field. Raw values are set in the Online Designer and are distinct from the option labels that users see. Several action tags use raw values in their parameters.

**Field Annotation**

Free-form notes that can be placed in the same *Action Tags / Field Annotation* box alongside any action tag. Annotations are only visible in the Online Designer and the Data Dictionary — they are never shown to data entry users or survey participants, and they have no effect on field behavior. Use annotations for designer-facing notes: design rationale, outstanding questions, variable mapping notes, or reminders about protocol decisions.

> **Do not confuse with the Field Note.** The Field Note (a separate field attribute) is visible to everyone completing the instrument. The Field Annotation is visible to designers only. If you need to communicate something to the person filling in the form — such as units of measure or format instructions — use the Field Note, not the Field Annotation. See RC-FD-06 Section 7.8–7.9 and the project STYLE-GUIDE.md for guidance on which to use when.

**External Module Action Tags**

Third-party External Modules can introduce additional action tags beyond REDCap's standard set. The Action Tags series covers only the action tags that ship with REDCap.

---

# 3. What Action Tags Do

Action tags were introduced to change the default behavior of individual REDCap fields without requiring additional buttons or settings in the interface. The system is intentionally lightweight and extensible: new action tags are added with REDCap upgrades, and as of version 15.x there are over fifty standard tags.

Every action tag shares three characteristics:

- **They change field behavior.** Each tag modifies something specific — hiding a field, capping word count, pre-filling a value, and so on.
- **They are situational.** Most tags only work for specific field types or in specific contexts (e.g., survey mode only). Adding a tag to an incompatible field type typically has no effect; no error is generated.
- **Their effects can be combined.** Multiple action tags can be placed in the same annotation box, separated by spaces. Their effects stack.

---

# 4. Finding Available Action Tags

The action tags available to you depend on your REDCap version and any External Modules installed on your instance. The built-in reference is the most reliable way to see what is available.

Red **@ Action Tags** buttons appear in several places throughout REDCap:

- The Project Setup page
- The Online Designer (top-right corner of the instrument field list)
- The *Edit Field* popup for any individual field

All of these buttons open the same popup, which lists every currently available action tag along with a description of its purpose and usage. When opened from the *Edit Field* popup, the list also shows an **Add** button that inserts the selected tag directly into the annotation box.

> **Pro tip:** Select *View text on separate page* (top-right of the popup) to open the reference in a new browser tab so you can keep it open while configuring fields.

> **Pro tip:** New action tags are added with each REDCap upgrade. Check this reference after every upgrade to see what is new.

---

# 5. How to Add an Action Tag

There are three ways to add action tags to a field.

## 5.1 Individually — Edit Field Dialog

Open the *Edit Field* popup in the Online Designer and type the action tag into the red *Action Tags / Field Annotation* box. Tags always start with `@`. Some need only their name (e.g., `@HIDDEN`); others require a parameter (e.g., `@HIDECHOICE='1'`).

## 5.2 In Bulk — Quick-Modify Field(s)

Most fields in the Online Designer have a checkbox in their top-right corner. Selecting one or more of these checkboxes opens the *Quick-Modify Field(s)* popup. Click the **@** button within that popup to open the *Edit Action Tags?* menu, which applies changes to all selected fields at once:

| Option | Effect |
|---|---|
| **Clear** | Removes all action tags from the selected fields |
| **Add** | Adds the entered action tags to all selected fields |
| **Deactivate** | Temporarily disables action tags (useful during testing) |
| **Reactivate** | Re-enables any deactivated action tags |
| **Copy** | Copies the action tags from the last-checked field to all other selected fields |
| **Edit** | Opens the standard edit dialog for the last-checked field only |

Click **Apply** to confirm any changes.

## 5.3 Via the Data Dictionary

The *Action Tags / Field Annotation* column (column R in Excel) in the Data Dictionary accepts action tags exactly as the Online Designer does. However, most spreadsheet applications interpret the `@` character as a formula prefix and may prevent editing. To work around this, format column R as **Text** before making edits.

---

# 6. Action Tag Quick Reference

Use this table to quickly find which article covers a specific action tag.

| Action Tag | Category | Article | Purpose |
|---|---|---|---|
| `@HIDDEN` | Visibility | RC-AT-02 | Hide a field from view |
| `@HIDDEN-SURVEY` | Visibility | RC-AT-02 | Hide in survey mode only |
| `@HIDDEN-FORM` | Visibility | RC-AT-02 | Hide in data entry form only |
| `@HIDDEN-APP` | Visibility | RC-AT-02 | Hide in Mobile App only |
| `@HIDDEN-PDF` | Visibility | RC-AT-02 | Hide from PDF exports |
| `@READONLY` | Visibility | RC-AT-02 | Make a field non-editable |
| `@READONLY-SURVEY` | Visibility | RC-AT-02 | Read-only in survey mode only |
| `@READONLY-FORM` | Visibility | RC-AT-02 | Read-only in data entry form only |
| `@READONLY-APP` | Visibility | RC-AT-02 | Read-only in Mobile App only |
| `@RANDOMORDER` | Radio/Dropdown | RC-AT-03 | Randomize option display order |
| `@HIDECHOICE` | Radio/Dropdown | RC-AT-03 | Hide specific options |
| `@SHOWCHOICE` | Radio/Dropdown | RC-AT-03 | Show only specific options |
| `@MAXCHOICE` | Radio/Dropdown | RC-AT-03 | Limit selections per option |
| `@NONEOFTHEABOVE` | Checkbox | RC-AT-04 | Enforce mutually exclusive options |
| `@MAXCHECKED` | Checkbox | RC-AT-04 | Limit maximum checked boxes |
| `@PASSWORDMASK` | Free Text | RC-AT-05 | Obscure text entry display |
| `@FORCE-MINMAX` | Free Text | RC-AT-05 | Enforce min/max bounds hard |
| `@WORDLIMIT` | Free Text | RC-AT-05 | Cap maximum word count |
| `@CHARLIMIT` | Free Text | RC-AT-05 | Cap maximum character count |
| `@RICHTEXT` | Free Text | RC-AT-05 | Enable formatting in notes box |
| `@PLACEHOLDER` | Free Text | RC-AT-05 | Display hint text in field |
| `@NOW` | Autofill | RC-AT-06 | Fill with current date/time |
| `@NOW-SERVER` | Autofill | RC-AT-06 | Fill with server date/time |
| `@NOW-UTC` | Autofill | RC-AT-06 | Fill with UTC date/time |
| `@TODAY` | Autofill | RC-AT-06 | Fill with current date |
| `@TODAY-SERVER` | Autofill | RC-AT-06 | Fill with server date |
| `@TODAY-UTC` | Autofill | RC-AT-06 | Fill with UTC date |
| `@LONGITUDE` | Autofill | RC-AT-06 | Fill with device longitude |
| `@LATITUDE` | Autofill | RC-AT-06 | Fill with device latitude |
| `@USERNAME` | Autofill | RC-AT-06 | Fill with current username |
| `@CONSENT-VERSION` | Autofill | RC-AT-06 | Fill with e-consent version |
| `@DEFAULT` | Autofill | RC-AT-06 | Pre-fill on first load |
| `@SETVALUE` | Autofill | RC-AT-06 | Pre-fill on every load |
| `@PREFILL` | Autofill | RC-AT-06 | Legacy alias for @SETVALUE |
| `@HIDEBUTTON` | Cosmetic | RC-AT-07 | Hide Today/Now button |
| `@INLINE` | Cosmetic | RC-AT-07 | Display uploaded file inline |
| `@INLINE-PREVIEW` | Cosmetic | RC-AT-07 | Display with toggle button |
| `@IF` | Conditional | RC-AT-08 | Apply action tags conditionally based on logic |
| `@CALCTEXT` | Calculation | RC-AT-09 | Calculate text values from expressions |
| `@CALCDATE` | Calculation | RC-AT-09 | Calculate date values from expressions |
| `@LANGUAGE-CURRENT-FORM` | Language | RC-AT-10 | Capture current language in data entry form |
| `@LANGUAGE-CURRENT-SURVEY` | Language | RC-AT-10 | Capture current language in survey |
| `@LANGUAGE-SET` | Language | RC-AT-10 | Switch language based on field value |
| `@LANGUAGE-SET-FORM` | Language | RC-AT-10 | Switch language in data entry form only |
| `@LANGUAGE-SET-SURVEY` | Language | RC-AT-10 | Switch language in survey only |
| `@LANGUAGE-FORCE` | Language | RC-AT-10 | Force page to render in specified language |
| `@LANGUAGE-FORCE-FORM` | Language | RC-AT-10 | Force language in data entry form only |
| `@LANGUAGE-FORCE-SURVEY` | Language | RC-AT-10 | Force language in survey only |
| `@LANGUAGE-MENU-STATIC` | Language | RC-AT-10 | Keep language menu always visible in survey |
| `@APPUSERNAME-APP` | Mobile App | RC-AT-11 | Fill with mobile app username |
| `@BARCODE-APP` | Mobile App | RC-AT-11 | Enable barcode/QR code scanning |
| `@IMAGEUPLOAD-APP` | Mobile App | RC-AT-11 | Sync images from server to app |
| `@HIDESUBMIT` | External Module | RC-AT-EM-01 | Hide all save/submit buttons (HIDESUBMIT module) |
| `@HIDESUBMIT-FORM` | External Module | RC-AT-EM-01 | Hide buttons on data entry forms (HIDESUBMIT module) |
| `@HIDESUBMIT-SURVEY` | External Module | RC-AT-EM-01 | Hide buttons on surveys (HIDESUBMIT module) |
| `@HIDESUBMIT-NEXT` | External Module | RC-AT-EM-01 | Hide Next/Previous buttons (HIDESUBMIT module) |
| `@HIDESAVE` | External Module | RC-AT-EM-01 | Hide save button only (HIDESUBMIT module) |
| `@HIDESAVE-FORM` | External Module | RC-AT-EM-01 | Hide save on forms only (HIDESUBMIT module) |
| `@HIDESAVE-SURVEY` | External Module | RC-AT-EM-01 | Hide save on surveys only (HIDESUBMIT module) |

---

# 7. Scope of This Series

The Action Tags knowledge base series is organized by tag category:

| Article | Category | Tags Covered |
|---|---|---|
| RC-AT-02 | Visibility | `@HIDDEN`, `@READONLY` and all situational variants |
| RC-AT-03 | Radio/Dropdown | `@RANDOMORDER`, `@HIDECHOICE`, `@SHOWCHOICE`, `@MAXCHOICE` |
| RC-AT-04 | Checkbox | `@NONEOFTHEABOVE`, `@MAXCHECKED` |
| RC-AT-05 | Free Text | `@PASSWORDMASK`, `@FORCE-MINMAX`, `@WORDLIMIT`, `@CHARLIMIT`, `@RICHTEXT`, `@PLACEHOLDER` |
| RC-AT-06 | Autofill | `@NOW`, `@TODAY`, `@LONGITUDE`, `@LATITUDE`, `@USERNAME`, `@CONSENT-VERSION`, `@DEFAULT`, `@SETVALUE` |
| RC-AT-07 | Cosmetic | `@HIDEBUTTON`, `@INLINE`, `@INLINE-PREVIEW` |
| RC-AT-08 | Conditional | `@IF` |
| RC-AT-09 | Calculation | `@CALCTEXT`, `@CALCDATE` |
| RC-AT-10 | Language | `@LANGUAGE-*` family (9 tags for multi-language projects) |
| RC-AT-11 | Mobile App | `@APPUSERNAME-APP`, `@BARCODE-APP`, `@IMAGEUPLOAD-APP` |
| RC-AT-EM-01 | External Module | `@HIDESUBMIT`, `@HIDESAVE` and related variants (HIDESUBMIT module) |

---

# 8. Common Questions

**Q: How do I know if an action tag is available on my REDCap instance?**

**A:** Click any red **@ Action Tags** button in your project. Only tags available in your current version and module configuration appear in the list.

**Q: Can action tags interfere with branching logic?**

**A:** Some can. `@HIDDEN` overrides branching logic — a field tagged with `@HIDDEN` is always hidden, regardless of branching logic conditions. See RC-AT-02 for details.

**Q: Will adding an unsupported action tag to a field cause an error?**

**A:** Typically no. REDCap silently ignores action tags applied to incompatible field types.

---

# 9. Related Articles

- RC-AT-02 — @HIDDEN & @READONLY
- RC-AT-03 — Radio/Dropdown Action Tags
- RC-AT-04 — Checkbox Action Tags
- RC-AT-05 — Free Text Action Tags
- RC-AT-06 — Autofill Action Tags
- RC-AT-07 — Cosmetic Action Tags
- RC-AT-08 — @IF: Conditional Logic
- RC-AT-09 — @CALCTEXT & @CALCDATE: Calculations
- RC-AT-10 — Language Action Tags
- RC-AT-11 — Mobile App Action Tags
- RC-AT-EM-01 — External Module Action Tags (HIDESUBMIT)
- RC-FD-02 — Online Designer
- RC-FD-03 — Data Dictionary

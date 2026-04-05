RC-AT-01

**Action Tags — Overview**

| **Article ID** | RC-AT-01 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-02 — Online Designer; foundational Project Build & Management knowledge |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-02 — @HIDDEN & @READONLY; RC-AT-03 — Radio/Dropdown Action Tags; RC-AT-04 — Checkbox Action Tags; RC-AT-05 — Free Text Action Tags; RC-AT-06 — Autofill Action Tags; RC-AT-07 — Cosmetic Action Tags; RC-AT-08 — @IF; RC-AT-09 — Calculation Action Tags; RC-AT-10 — Language Action Tags; RC-AT-11 — Mobile App Action Tags; RC-AT-12 — HIDESUBMIT External Module; RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary |

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

Free-form notes that can be placed in the same *Action Tags / Field Annotation* box alongside any action tag. Annotations are only visible in the Online Designer and have no effect on field behavior.

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

The table below lists every action tag covered in this series, the field types it applies to, and the article where it is documented. Use this table to quickly locate the right article for any tag.

**Native REDCap Action Tags**

| Action Tag | Applies To | Parameters | Article |
|---|---|---|---|
| `@HIDDEN` | All field types | None | RC-AT-02 |
| `@HIDDEN-SURVEY` | All field types | None | RC-AT-02 |
| `@HIDDEN-FORM` | All field types | None | RC-AT-02 |
| `@HIDDEN-APP` | All field types | None | RC-AT-02 |
| `@HIDDEN-PDF` | All field types | None | RC-AT-02 |
| `@READONLY` | All field types | None | RC-AT-02 |
| `@READONLY-SURVEY` | All field types | None | RC-AT-02 |
| `@READONLY-FORM` | All field types | None | RC-AT-02 |
| `@READONLY-APP` | All field types | None | RC-AT-02 |
| `@RANDOMORDER` | Radio, Dropdown, Checkbox | None | RC-AT-03 |
| `@HIDECHOICE` | Radio, Dropdown, Checkbox | Raw value(s) to hide; piping supported | RC-AT-03 |
| `@SHOWCHOICE` | Radio, Dropdown, Checkbox | Raw value(s) to show; piping supported | RC-AT-03 |
| `@MAXCHOICE` | Radio, Dropdown, Checkbox, Matrix | Per-option limits | RC-AT-03 |
| `@MAXCHOICE-SURVEY-COMPLETE` | Radio, Dropdown, Checkbox | Per-option limits (completed surveys only) | RC-AT-03 |
| `@NONEOFTHEABOVE` | Checkbox only | Raw value(s) of "none" option | RC-AT-04 |
| `@MAXCHECKED` | Checkbox only | Maximum number of selections | RC-AT-04 |
| `@PASSWORDMASK` | Text box | None | RC-AT-05 |
| `@FORCE-MINMAX` | Text box (with min/max validation) | None | RC-AT-05 |
| `@WORDLIMIT` | Text box, Notes box | Maximum word count | RC-AT-05 |
| `@CHARLIMIT` | Text box, Notes box | Maximum character count | RC-AT-05 |
| `@RICHTEXT` | Notes box | None | RC-AT-05 |
| `@PLACEHOLDER` | Text box, Notes box | Display text | RC-AT-05 |
| `@NOW` | Text box | None | RC-AT-06 |
| `@NOW-SERVER` | Text box | None | RC-AT-06 |
| `@NOW-UTC` | Text box | None | RC-AT-06 |
| `@TODAY` | Text box | None | RC-AT-06 |
| `@TODAY-SERVER` | Text box | None | RC-AT-06 |
| `@TODAY-UTC` | Text box | None | RC-AT-06 |
| `@LONGITUDE` | Text box | None | RC-AT-06 |
| `@LATITUDE` | Text box | None | RC-AT-06 |
| `@USERNAME` | Text box | None | RC-AT-06 |
| `@CONSENT-VERSION` | Text box | None | RC-AT-06 |
| `@DEFAULT` | Text, Notes, Radio, Dropdown, Checkbox, Slider | Value, raw value, pipe, or smart variable | RC-AT-06 |
| `@SETVALUE` | Text, Notes, Radio, Dropdown, Checkbox, Slider | Value, raw value, pipe, or smart variable | RC-AT-06 |
| `@PREFILL` | Text, Notes, Radio, Dropdown, Checkbox, Slider | Legacy alias for `@SETVALUE` | RC-AT-06 |
| `@SAVE-PROMPT-EXEMPT` | Any | None | RC-AT-06 |
| `@SAVE-PROMPT-EXEMPT-WHEN-AUTOSET` | Any | None | RC-AT-06 |
| `@HIDEBUTTON` | Text box (with date/datetime validation) | None | RC-AT-07 |
| `@INLINE` | File upload | None, width, or width+height | RC-AT-07 |
| `@INLINE-PREVIEW` | File upload, Descriptive | None | RC-AT-07 |
| `@DOWNLOAD-COUNT` | Text box, Notes box (counter field) | Variable name of File Upload or Descriptive field | RC-AT-07 |
| `@NOMISSING` | Any | None | RC-AT-07 |
| `@IF` | Any | Condition, true-branch tags, false-branch tags | RC-AT-08 |
| `@CALCTEXT` | Text box | Formula expression | RC-AT-09 |
| `@CALCDATE` | Text box (date/datetime validation) | Source, offset, unit | RC-AT-09 |
| `@LANGUAGE-CURRENT-FORM` | Text box, Radio, Dropdown | None | RC-AT-10 |
| `@LANGUAGE-CURRENT-SURVEY` | Text box, Radio, Dropdown | None | RC-AT-10 |
| `@LANGUAGE-SET` | Radio, Dropdown | None | RC-AT-10 |
| `@LANGUAGE-SET-FORM` | Radio, Dropdown | None | RC-AT-10 |
| `@LANGUAGE-SET-SURVEY` | Radio, Dropdown | None | RC-AT-10 |
| `@LANGUAGE-FORCE` | Any | Language ID (quoted) | RC-AT-10 |
| `@LANGUAGE-FORCE-FORM` | Any | Language ID (quoted) | RC-AT-10 |
| `@LANGUAGE-FORCE-SURVEY` | Any | Language ID (quoted) | RC-AT-10 |
| `@LANGUAGE-MENU-STATIC` | Any (survey pages) | None | RC-AT-10 |
| `@APPUSERNAME-APP` | Text box | None | RC-AT-11 |
| `@BARCODE-APP` | Text box | None | RC-AT-11 |
| `@SYNC-APP` | File upload, Signature | None | RC-AT-11 |

**External Module Action Tags**

> ⚠️ The following tags require an External Module to be installed and enabled. They are not available in vanilla REDCap.

| Action Tag | Module | Parameters | Article |
|---|---|---|---|
| `@HIDESUBMIT` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDESUBMIT-FORM` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDESUBMIT-SURVEY` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDESUBMITONLY` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDESUBMITONLY-FORM` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDESUBMITONLY-SURVEY` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDEREPEAT` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDEREPEAT-FORM` | HIDESUBMIT Action Tags | None | RC-AT-12 |
| `@HIDEREPEAT-SURVEY` | HIDESUBMIT Action Tags | None | RC-AT-12 |

## 6.1 Scope of This Series

The Action Tags knowledge base series is organized by tag category:

| Article | Category | Tags Covered |
|---|---|---|
| RC-AT-02 | Hiding & Read-Only | `@HIDDEN`, `@READONLY`, and all situational variants |
| RC-AT-03 | Radio/Dropdown | `@RANDOMORDER`, `@HIDECHOICE`, `@SHOWCHOICE`, `@MAXCHOICE`, `@MAXCHOICE-SURVEY-COMPLETE` |
| RC-AT-04 | Checkbox | `@NONEOFTHEABOVE`, `@MAXCHECKED` |
| RC-AT-05 | Free Text | `@PASSWORDMASK`, `@FORCE-MINMAX`, `@WORDLIMIT`, `@CHARLIMIT`, `@RICHTEXT`, `@PLACEHOLDER` |
| RC-AT-06 | Autofill | `@NOW`/`@TODAY` families, `@LONGITUDE`, `@LATITUDE`, `@USERNAME`, `@CONSENT-VERSION`, `@DEFAULT`, `@SETVALUE`, `@PREFILL`, `@SAVE-PROMPT-EXEMPT`, `@SAVE-PROMPT-EXEMPT-WHEN-AUTOSET` |
| RC-AT-07 | Cosmetic & Utility | `@HIDEBUTTON`, `@INLINE`, `@INLINE-PREVIEW`, `@DOWNLOAD-COUNT`, `@NOMISSING` |
| RC-AT-08 | Conditional Logic | `@IF` |
| RC-AT-09 | Calculations | `@CALCTEXT`, `@CALCDATE` |
| RC-AT-10 | Language | `@LANGUAGE-CURRENT-*`, `@LANGUAGE-SET-*`, `@LANGUAGE-FORCE-*`, `@LANGUAGE-MENU-STATIC` |
| RC-AT-11 | Mobile App | `@APPUSERNAME-APP`, `@BARCODE-APP`, `@SYNC-APP` |
| RC-AT-12 | External Module: HIDESUBMIT | `@HIDESUBMIT`, `@HIDESUBMITONLY`, `@HIDEREPEAT`, and all variants |

> **Note on External Module tags:** Action tags provided by External Modules are not part of vanilla REDCap and only appear and function when the relevant module is installed on your instance and enabled for your project. RC-AT-12 documents the HIDESUBMIT Action Tags module. If you see action tags in your project's reference popup that are not listed in this series, they are likely provided by another External Module installed at your institution.

---

# 7. Common Questions

**Q: How do I know if an action tag is available on my REDCap instance?**

**A:** Click any red **@ Action Tags** button in your project. Only tags available in your current version and module configuration appear in the list. Tags added by disabled or uninstalled External Modules will not appear.

**Q: Can action tags interfere with branching logic?**

**A:** Some can. `@HIDDEN` in particular overrides branching logic — a field tagged with `@HIDDEN` is always hidden, regardless of any branching logic condition. Other tags do not interact with branching logic directly. See RC-AT-02 for details.

**Q: Will adding an unsupported action tag to a field cause an error?**

**A:** Typically no. REDCap silently ignores action tags applied to incompatible field types. No error is generated — the tag simply has no effect.

---

# 8. Related Articles

- RC-AT-02 — @HIDDEN & @READONLY: hiding fields and making fields read-only
- RC-AT-03 — Radio/Dropdown Action Tags: controlling options in structured fields
- RC-AT-04 — Checkbox Action Tags: enforcing checkbox selection rules
- RC-AT-05 — Free Text Action Tags: constraining and enhancing text and notes boxes
- RC-AT-06 — Autofill Action Tags: pre-populating field values automatically
- RC-AT-07 — Cosmetic & Utility Action Tags: adjusting display of date fields, file uploads, and download tracking
- RC-AT-08 — @IF: applying action tags conditionally based on field values or user context
- RC-AT-09 — Calculation Action Tags: @CALCTEXT and @CALCDATE for computed text and date values
- RC-AT-10 — Language Action Tags: capturing, setting, and forcing the display language in MLM projects
- RC-AT-11 — Mobile App Action Tags: barcode scanning, app username capture, and image syncing
- RC-AT-12 — HIDESUBMIT External Module Action Tags: conditionally hiding save and submit buttons
- RC-FD-02 — Online Designer: where action tags are configured
- RC-FD-03 — Data Dictionary: alternative method for adding action tags in bulk

---
id: RC-DE-02
title: Basic Data Entry
domain: Data Entry
applies_to:
- All REDCap project types
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — data entry
  form behaviour checked against source code; pages not re-captured
prerequisites:
- RC-DE-01 — Record Creation & the Record Home Page
version: '1.3'
last_updated: 2026-11
related:
- id: RC-DE-01
  title: Record Creation & the Record Home Page
- id: RC-DE-04
  title: Editing Data & Audit Trail
- id: RC-NAV-REC-01
  title: Record Navigation Overview
tags:
- data entry
synonyms:
- how do i enter data into a redcap form
- fill out an instrument and save it
- what do the field types mean during data entry
- set form status complete or incomplete
- required fields and branching logic data entry
- basic data entry mechanics
- save options on a data entry form
- enter values into a redcap instrument
---

# 1. Overview

This article covers the mechanics of entering data into a REDCap
instrument. It explains the field types you will encounter, how required
fields and branching logic work, how to set form status, and all
available save options. Understanding these mechanics is required before
entering any data in REDCap.

---

# 2. Key Concepts & Definitions

**Instrument (Form)**

A structured data-entry page within a REDCap project. Each instrument
contains one or more fields (variables). Instruments are opened by
selecting a status dot on the Record Home Page or Record Status
Dashboard.

**Field (Variable)**

A single data-entry element within an instrument. Each field has a type
that determines how data is entered and validated. Field names (variable
names) are how REDCap identifies data internally and in exports.

**Form Status**

A mandatory dropdown field at the bottom of every REDCap instrument,
labeled 'Complete?'. Its value determines the color of the
instrument's status dot. Setting form status is optional for the study
team but strongly recommended for tracking instrument completion.

**Required Field**

A field marked with a red asterisk (\*) that the project designer has
designated as required. On a data entry form, REDCap saves the instrument
even if a required field is empty and then displays a warning that can be
dismissed — required fields are a soft constraint on data entry forms (for
every user, administrators included). Surveys enforce them.

**Branching Logic**

A project-level configuration that conditionally shows or hides fields
based on the values of other fields. Fields appear or disappear as data
is entered; if a field that is about to be hidden already has a value,
REDCap asks you what to do with it (see Section 5).

**Save Options**

REDCap does not auto-save. Data is only committed to the database when
the user explicitly saves the form using one of the save buttons at the
bottom of every instrument. Users with read-only access to an instrument
see no save buttons.

---

# 3. Field Types

REDCap fields fall into two broad categories: structured (constrained
input) and unstructured (free text).

## 3.1 Structured Field Types

Structured fields restrict input to a defined set of options or a
validated format. They reduce entry errors and improve data consistency.

| **Field Type** | **How It Works** |
| --- | --- |
| Radio button | Select exactly one option from a visible list. Cannot be deselected by clicking again — use the **reset** link next to the field to clear it. |
| Yes - No / True - False | Two-option radio buttons with fixed labels (stored as 1/0). They also have a **reset** link. |
| Dropdown | Select exactly one option from a collapsed list. More compact than radio buttons for long option lists. |
| Checkbox | Select one or more options independently. Each checkbox option is stored as a separate 0/1 variable in the dataset. |
| Slider | Drag a handle along a scale to select a numeric value. Commonly used for visual analog scales (e.g., pain scores). |
| File upload | Attach a file (PDF, image, etc.) to the record. One file per field per instance. |
| Signature | Capture a drawn signature in the browser. Stored as a PNG image file. |
| Calculated field | Read-only; REDCap computes the value from other fields as you enter data. You cannot type into it. |
| Descriptive text | Displays text, an image or a file for information only. Collects no data. |

## 3.2 Unstructured Field Types

Unstructured fields accept free-text input. They can be configured with
optional validation to enforce a format without restricting the user to
a predefined list.

| **Field Type** | **How It Works** |
| --- | --- |
| Text box | Single-line free-text entry. Can have validation applied (see below). |
| Notes box | Multi-line free-text entry. No validation options. Used for comments, narratives, or open-ended responses. |

**Text Box Validation Types**

A text box can be configured with a validation rule that restricts
accepted input to a specific format. REDCap checks the format as you
leave the field and shows an error if the value does not match. Note:
format enforcement is a hard stop — an invalid value is not saved, though
the rest of the form still saves — but min/max range constraints are **soft** by default —
REDCap warns the user but allows out-of-range values to be saved. Add
the `@FORCE-MINMAX` action tag to make a range constraint a hard stop.

| **Validation Type** | **What It Enforces** |
| --- | --- |
| Date (various formats) | Requires a valid date. Available in multiple regional formats (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, etc.). |
| Time | Requires a valid time value (HH:MM; variants such as HH:MM:SS and MM:SS also exist). |
| Number | Requires a numeric value. Variants fix the number of decimal places or accept a comma as the decimal separator. Optionally accepts a min/max range — soft warning by default; use `@FORCE-MINMAX` to enforce. |
| Integer | Requires a whole number (no decimals). |
| Email | Requires a valid email address format. |
| Phone number | Requires a phone number format. North American format by default; other countries' formats may be enabled. |
| Zipcode / postal code | Requires a US ZIP code format; postal-code formats for other countries may be enabled. |

Which validation types appear is controlled by your REDCap administrators,
so the list on your instance may be shorter or longer than this table.

> **Version caveat (17.4.0+):** From 17.4.0 administrators can also define custom validation types, so you may see formats on your instance that are not listed here. If a text box rejects a value and you do not recognise the format, check the field's validation in the Online Designer or ask the project designer.

---

# 4. Required Fields

A required field is marked with a red asterisk (\*) next to the field
label. If you save the instrument while a required field is empty,
REDCap **saves the data first**, then reloads the form with a message
that the data was successfully saved but some required fields are empty,
listing them. Choose **Okay** to go back and fill them in, or **Ignore**
to continue to wherever your save button was taking you.

- Required fields hidden by branching logic or by `@HIDDEN-FORM` are not
    checked.
- On surveys, required fields are enforced: the participant cannot move
    on until they are answered.


> **Important:** Required fields are a soft constraint on data entry forms, for every user (administrators included). The data is already saved when the warning appears, so the field can stay empty. If your study protocol requires these fields to be filled, enforce compliance through team training and data quality checks — not solely through REDCap's required-field mechanism.


---

# 5. Branching Logic

Branching logic allows the project designer to conditionally show or
hide fields based on the current values of other fields in the same
instrument (or in some configurations, other instruments).

- Fields hidden by branching logic do not appear on the form. If a field
    that is about to be hidden already contains a value, REDCap prompts
    you to choose:
    - **Erase** — the value is cleared and the field is hidden. The
        erasure becomes permanent when you save the form. If the field
        holds an uploaded file, the prompt warns that the file will be
        permanently deleted.
    - **Keep All** — the value is kept and the field stays visible,
        marked with an indicator that branching logic would normally
        hide it.

- On surveys there is no prompt: values in fields hidden by branching
    logic are erased automatically. A field holding a missing-data code
    is also erased without a prompt.

- If the project setting **Prevent branching logic from hiding fields
    that have values** is enabled, REDCap does not hide fields that
    already contain a value.

- Fields revealed by branching logic appear dynamically as you enter
    data — no page reload required.

- **Example:** a 'Are you pregnant?' question may be hidden when
    'Male' is selected in a Sex field. The field reappears if the
    answer changes.

- Apart from choosing **Keep All** for a field that already has a value,
    you cannot override branching logic during data entry. If a field you
    expect to see is not visible, it means the logic condition has not
    been met based on current values.


> **Troubleshooting:** If a field seems to be missing from an instrument, check whether branching logic may be hiding it before reporting it as a bug. Changing an earlier field value may reveal it.


---

# 6. Form Status

Every instrument has a Form Status dropdown at the bottom, labeled
'Complete?'. This field controls the color of the instrument's status
dot in the Record Home Page and Record Status Dashboard.

| **Form Status Value** | **Dot Color** | **Meaning & Who Sets It** |
| --- | --- | --- |
| (no data saved) | Grey | No data has been entered. Default state. Set automatically by REDCap. |
| Incomplete | Red | Data has been saved but status has not been updated. Default for any saved form. Set automatically by REDCap. |
| Unverified | Yellow | Data entry complete but not yet verified. Set manually by the study team. |
| Complete | Green | Data entry verified and complete. Set manually by the study team. |

- Only grey and red are enforced automatically by REDCap. Yellow and
    green must be set manually.

- Using yellow and green is optional, but strongly recommended for
    projects with many instruments — it makes it easy to distinguish
    instruments that have been reviewed from those that have only been
    partially filled.

- Survey completions have their own status dots (orange checkmark =
    partial survey, green checkmark = completed survey). These are set
    automatically and are separate from the manual form status described
    here.

- On repeating instruments or events, a **blue stacked dot** means the
    record has several instances of that instrument with different
    statuses. Select it to see the individual instances.

> **Version caveat (17.6 Standard; not in 17.3 LTS or 16.0 LTS):** In MyCap projects a **purple dot**, labelled **Partial MyCap Response**, marks an instrument a participant has started but not finished in the MyCap app. If you are on an LTS release you will not see this dot; check the instrument's data directly instead.

---

# 6a. Navigating a Long Form

## Section Navigation *(16.1.5+)*

On data entry forms, a **Section Navigation** box is displayed on the right-hand side of the page. It lists the form's section headers and lets you jump straight to any section rather than scrolling.

It appears automatically — there is nothing to enable — and is most useful on long instruments where the section headers are the only structural landmarks.

> **Version caveat (≤17.0.x):** Opening the REDCap Messenger panel while viewing a data entry form could leave the Section Navigation box **overlapping the form**, obscuring fields and making them difficult to complete. Fixed in 17.0.0. Separately, on forms with a large number of section headers some headers were not reachable from the box (fixed 17.2.1). On some forms, the box could also cover part of the data entry table and block entry; from 17.5.4 Standard / 17.3.18 LTS its positioning was reworked so it sits to the right of the form and is hidden on very narrow (mobile-width) windows rather than covering fields. If the box covers fields on an older version, widen the browser window or scroll the page.

> **Version caveat (16.0 LTS):** Section Navigation is not present on the 16.0 LTS line. Scroll the form, or use the section headers, to move through long instruments.

For jumping to an individual *field* rather than a section, the Online Designer offers a Field Navigator — see [RC-FD-11 — Online Designer Advanced Options](RC-FD-11_Advanced-Online-Designer-Options.md).

---

# 7. Saving Data


> **Critical:** REDCap does not auto-save. If you navigate away from a form with unsaved changes, REDCap shows a **SAVE YOUR CHANGES?** prompt so you can save or leave without saving — but closing the browser tab, or choosing to leave without saving, loses all unsaved data on the current form.


Every instrument has the following core save options at the bottom of the page (users with read-only access to the instrument see none of them):

| **Save Option** | **What Happens After Saving** |
| --- | --- |
| Save and Exit Form | Saves the form and returns you to the Record Home Page for that record. |
| Save and Stay | Saves the form and remains on the current instrument. Use when making multiple edits or reviewing your entry. |
| Save and Go To Next Form | Saves the form and opens the next instrument for the same record (and event). |
| Save and Exit Record | Saves the form and returns you to the Add/Edit Records page. Use when you are done with this record entirely. |
| Save and Go to Next Record | Saves the form and opens the **Record Home Page** of the next record (in the same arm, and within your Data Access Group if you are in one) — not the same instrument. Use for working through records one after another. |

> **Note:** These core options are available in all instruments. Additional save options appear in specific contexts — for surveys (Save & Mark Survey as Complete) and for repeating instruments (Save & Go To Next Instance, Save & Add New Instance). See [RC-DE-11 — Instrument Save Options](RC-DE-11_Instrument-Save-Options.md) for the complete reference.

> **Warning:** Selecting Cancel on an instrument discards all unsaved changes on that form and returns you to the Record Home Page. If you have changed anything, REDCap asks you to confirm first; once confirmed, there is no undo.


---

# 8. Common Questions

**Q: A required field has a red asterisk but I need to save the form
without filling it in. Can I?**

**A:** Yes, on a data entry form. REDCap saves the data first and then
shows a message listing the empty required fields; choose **Ignore** to
carry on. REDCap will not block the save. However, your study's data
quality rules may flag this for follow-up. On surveys, required fields
are enforced.

**Q: A field I expected to see on the form is not there. What
happened?**

**A:** The field is likely hidden by branching logic. Check whether an
earlier field that controls the logic has been filled in correctly. The
hidden field will appear once the branching condition is met.

**Q: What is the difference between the grey dot and the red dot?**

**A:** Grey means no data has been saved to that instrument at all. Red
means data has been saved but the Form Status dropdown is still set to
'Incomplete' (the default). A single saved value is enough to turn a
grey dot red.

**Q: Do I have to set the form status to 'Complete' after every
entry?**

**A:** No. It is optional. However, using yellow and green statuses makes it
much easier to track which records have been reviewed versus just
entered, especially in large projects with many instruments.

**Q: What does 'Save and Go to Next Record' do if I am on the last
record?**

**A:** The form is saved, and where you land depends on the project. If
record auto-numbering is enabled, REDCap opens the Record Home Page for
a new, auto-numbered record. Otherwise it takes you to the record
selection page with a message that there is no next record. Either way
you leave the current form.

**Q: Can I enter data in checkboxes by selecting multiple options?**

**A:** Yes. Checkboxes allow any number of options to be selected
independently. Each checkbox option is stored as a separate yes/no
binary variable in the dataset export.

**Q: What happens to a field hidden by branching logic — is the data
deleted?**

**A:** Not automatically on a data entry form. When branching logic is
about to hide a field that has a value, REDCap asks you to **Erase** the
value or **Keep All**. If you erase it, the value is deleted when you
save the form, and if the field becomes visible again it starts empty.
If you keep it, the field stays visible with an indicator. On surveys,
values in hidden fields are erased without a prompt. Projects can also
enable **Prevent branching logic from hiding fields that have values**.

---

# 9. Common Mistakes & Gotchas

- Losing data by closing the browser: REDCap does not auto-save.
    Always use one of the save buttons before navigating away, and do not
    choose to leave without saving at the **SAVE YOUR CHANGES?** prompt
    unless you mean to discard your edits.

- Clicking **Erase** without thinking: when branching logic is about to
    hide a field that has a value, **Erase** deletes that value (and any
    uploaded file) once you save. Choose **Keep All** if you are unsure.

- Expecting 'Save and Go to Next Record' to open the same instrument:
    it opens the next record's Record Home Page.

- Ignoring required field warnings: dismissing the warning is allowed,
    but doing so repeatedly without filling the field will cause data
    quality issues. Build a habit of completing required fields before
    saving.

- Not setting form status: teams that skip the yellow/green status on
    complex projects quickly lose track of which forms have been
    reviewed versus just filled in. Decide on a form status convention
    before data collection begins.

- Confusing grey and red: grey = zero data saved; red = some data
    saved but status not updated. Both are coded as 0 in the dataset but
    have different visual meanings.

- Selecting 'Save and Exit Record' when you meant 'Save and Exit
    Form': these take you to different places. 'Save and Exit Form'
    returns to the Record Home Page; 'Save and Exit Record' returns to
    the Add/Edit Records page.

- Assuming a hidden field is a bug: if a field is not visible, check
    branching logic before reporting a problem. It may be intentionally
    hidden based on another field's value.

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-03 — Import Records API](RC-API-03_Import-Records.md)** — import or update field values programmatically without using the data entry UI
- **[RC-API-12 — Export File API](RC-API-12_Export-File.md)** — download a file stored in a File Upload field programmatically
- **[RC-API-13 — Import File API](RC-API-13_Import-File.md)** — upload a file to a File Upload field programmatically
- **[RC-API-14 — Delete File API](RC-API-14_Delete-File.md)** — delete a file stored in a File Upload field programmatically

---


# 10. Related Articles

- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) (prerequisite)

- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md) (how project
    structure affects data entry)

- [RC-DE-04 — Editing Data & Audit Trail](RC-DE-04_Editing-Data-and-Audit-Trail.md) (editing saved data, history
    log)

- [RC-NAV-REC-01 — Record Navigation Overview](RC-NAV-REC-01_Record-Navigation-Overview.md) (dot color reference)

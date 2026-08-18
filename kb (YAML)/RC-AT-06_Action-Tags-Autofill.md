---
id: RC-AT-06
title: Autofill Action Tags
domain: Action Tags
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- 'RC-AT-01 — Action Tags: Overview'
version: '1.1'
last_updated: 2026-08
related:
- id: RC-AT-01
  title: 'Action Tags: Overview'
- id: RC-AT-05
  title: Free Text Action Tags
- id: RC-LONG-01
  title: Longitudinal Project Setup
- id: RC-FD-02
  title: Online Designer
tags:
- action tags
synonyms:
- '@NOW and @TODAY action tags'
- '@DEFAULT action tag'
- '@SETVALUE action tag'
- '@USERNAME action tag'
- how do i auto fill a field with today's date
- how do i set a default value on a field
- prefill a field value on page load
- auto populate the current date and time
- capture the username automatically into a field
---

# 1. Overview

This article covers action tags that automatically populate field values when a form or survey is first loaded: the `@NOW` and `@TODAY` families, device-based tags, user-based tags, and the flexible `@DEFAULT` and `@SETVALUE` tags.

Autofill tags only populate values on page load if the field is currently empty. Existing values are never overwritten (except by `@SETVALUE`, which always overwrites).

---

# 2. Date & Time Autofill Tags

These tags fill text boxes with date and/or time values. All have no parameters.

| Tag | Fills with | Notes |
|---|---|---|
| `@NOW` | Current date/time from user's device | Use for date-time fields |
| `@NOW-SERVER` | Current date/time from REDCap server | Better for multi-timezone scenarios |
| `@NOW-UTC` | Current date/time in UTC | Consistent reference |
| `@TODAY` | Current date from user's device | Use for date-only fields |
| `@TODAY-SERVER` | Current date from REDCap server | For multi-timezone scenarios |
| `@TODAY-UTC` | Current date in UTC | Consistent reference |

**Applies to:** Text box and notes box with corresponding date/time validation.

**Use case:** Timestamp fields, survey completion dates, or any field where the current date/time is the expected value.

---

# 3. Device & User Autofill Tags

| Tag | Fills with | Notes |
|---|---|---|
| `@LONGITUDE` | Device longitude | Subject to privacy settings; may be blank or inaccurate |
| `@LATITUDE` | Device latitude | Subject to privacy settings; may be blank or inaccurate |
| `@USERNAME` | Current REDCap username | Fills with "survey-participant" when accessed via survey |
| `@CONSENT-VERSION` | E-consent version number | Only applies to surveys with e-consent framework enabled |

**Applies to:** Text box (varies by tag).

> **Note on location accuracy:** Device location depends on privacy settings. Many devices allow users to disable location services or reduce accuracy. VPNs can also return incorrect values. Treat location data as approximate.

---

# 4. @DEFAULT — Pre-fill on First Load

Pre-fills a field only when the form has never had data entered (status is "grey/incomplete"). Once the respondent saves data, `@DEFAULT` no longer applies.

**Applies to:** Text box, notes box, radio button, dropdown, checkbox, slider fields.

**Use case:** Setting expected default values that respondents may override.

## 4.1 Static Values in Text/Notes Boxes

```
@DEFAULT='Green'
```

## 4.2 Raw Values in Radio/Dropdown/Checkbox

```
@DEFAULT='2'
```

For multiple selections in checkboxes:

```
@DEFAULT='1,2'
```

## 4.3 Dynamic Values — Piping

Pre-fill with a value from another field in the same record:

```
@DEFAULT='[email]'
```

## 4.4 Dynamic Values — Smart Variables

Pre-fill with a system value:

```
@DEFAULT='[user-fullname]'
```

## 4.5 Longitudinal Projects

Carry forward a value from the previous event:

```
@DEFAULT='[previous-event-name][rx1]'
```

Pre-fills the field with the value of `rx1` from the most recent prior event. Requires understanding of longitudinal projects (see [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md)).

---

# 5. @SETVALUE — Pre-fill on Every Load

Like `@DEFAULT`, but fills the field every time the form is loaded, overwriting any existing value. Use when the field should always reflect the most current value on load.

**Syntax:** Identical to `@DEFAULT`.

**Use case:** Tracking the last user to touch a form, or always pulling the most recent data from another field.

**Backward compatibility note:** Older REDCap versions used `@PREFILL` (which still works but is deprecated).

---

# 5a. Suppressing the "Save your changes?" Prompt

Autofill tags create a specific nuisance: `@DEFAULT`, `@SETVALUE`, `@TODAY` and `@NOW` all write a value into a field the moment the page loads. REDCap sees that as an unsaved change, so a user who opens a form and immediately navigates away is warned about losing changes they never made. Two action tags added in **15.2.0** address this.

| Action tag | Effect |
| --- | --- |
| `@SAVE-PROMPT-EXEMPT` | Changes to this field's value never trigger the "Save your changes?" prompt, whenever they occur |
| `@SAVE-PROMPT-EXEMPT-WHEN-AUTOSET` | Narrower: only the **initial** setting of the value counts as exempt, and only when the field was blank at page load. A later change by the user does trigger the prompt |

`@SAVE-PROMPT-EXEMPT-WHEN-AUTOSET` is the one that pairs with the tags in this article — it exists precisely to stop `@DEFAULT`, `@SETVALUE`, `@TODAY` and `@NOW` from provoking the warning, while still warning about genuine edits.

The canonical use for the broader `@SAVE-PROMPT-EXEMPT` is a bookkeeping field whose value only matters alongside real data — REDCap's own example is a "Last modified by" field carrying both `@READONLY` and `@SETVALUE="[user-name]"`.

> **Important:** Neither tag suppresses the prompt for the *page*. They only remove that one field's ability to trigger it. If any other field on the page has been modified, the prompt still appears.

> **Warning — possible silent data loss.** These tags disable the safety net for the fields that carry them. A user who navigates away without saving loses the value in an exempted field with no warning. That is the intended trade-off, but confine it to fields whose value genuinely does not matter on its own.

> **Version caveat (≤16.1.6):** With `@SAVE-PROMPT-EXEMPT` on an **auto-complete dropdown**, selecting a choice by typing the full label and tabbing out — rather than clicking from the dropdown list — still triggered the prompt. Fixed in 16.1.7.

# 6. Combining Autofill Tags with Visibility Tags

Autofill tags are often combined with `@HIDDEN` or `@READONLY` variants:

```
@NOW @HIDDEN
```

Creates a hidden timestamp recording when a form was first loaded.

```
@USERNAME @READONLY
```

Pre-populates with the current user's username and locks it to prevent manual edits.

---

# 7. Common Questions

**Q: When should I use @DEFAULT versus @SETVALUE?**

**A:** Use `@DEFAULT` when you expect the field to be filled once and then potentially updated by the respondent. Use `@SETVALUE` when the field should always reflect a freshly computed or looked-up value on every load.

**Q: Can I use piped variables and smart variables in @DEFAULT/@SETVALUE?**

**A:** Yes. Any valid piped field reference (e.g., `[email]`) or smart variable (e.g., `[user-fullname]`) can be used as the parameter.

**Q: What is the difference between @NOW and @TODAY?**

**A:** `@NOW` fills both date and time. `@TODAY` fills date only. If your field has a date-only validation, use `@TODAY`.

**Q: Do autofill tags work during data import?**

**A:** No. These tags only execute when a form is loaded in a browser. They do not run during API uploads or Data Import Tool uploads.

---

# 8. Common Mistakes

**Using `@SETVALUE` on fields where respondents expect data to persist.** Unlike `@DEFAULT`, `@SETVALUE` replaces the value every time the form loads. Avoid on fields where users expect their previous entries to remain.

**Using `@NOW` on a date-only field.** If the field has a date-only validation, use `@TODAY` instead. `@NOW` on a date-only field will still populate the date, but the time component is discarded.

**Applying `@TODAY` or `@NOW` to a field with no date validation.** Both tags will autofill any text field regardless of whether date or datetime validation is set. If the field has no validation, REDCap fills it with a date or datetime string on first load — but does not enforce the format on save. Users can overwrite the autofilled value with free text, and REDCap will accept it. Over time this produces inconsistently formatted data in what was intended to be a timestamp field. For reliable timestamp capture, always set the matching validation type: `date_mdy` (or `date_ymd`, `date_dmy`) for `@TODAY` fields, and `datetime_ymd` (or another datetime variant) for `@NOW` fields. The validation enforces format consistency on every entry, not only the autofilled ones. If you need a reliable date anchor for calculations but want to keep a visible field without format restrictions, see the hidden anchor field pattern in [RC-FD-10 — Advanced Workflow Patterns: Multi-Stage Review and Operational Processing](RC-FD-10_Advanced-Workflow-Patterns-Multi-Stage-Review-and-Operational-Processing.md).

**Expecting autofill tags to populate during data import.** These tags run only when a form is loaded in the browser.

---

# 9. Related Articles

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-AT-05 — Free Text Action Tags](RC-AT-05_Action-Tags-Free-Text.md)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (for the [previous-event-name] example)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)

RC-AT-06

**Action Tags — Autofill**

| **Article ID** | RC-AT-06 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **REDCap Version** | 15.9.1 |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-02 — @HIDDEN & @READONLY; RC-LONG-01 — Longitudinal Project Setup; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers autofill action tags — tags that automatically populate a field value when a form or survey is loaded in a browser. Autofill tags do not require any user input; they insert values such as the current date and time, the user's login name, or a value pulled from elsewhere in the project.

All autofill tags share one behavior: they only activate when a form is loaded in a browser. They do not run during API writes, data imports, or background processes.

---

# 2. Key Concepts & Definitions

**Autofill**

The automatic population of a field value on page load. Autofill action tags insert a pre-determined value without any user action.

**Piping**

Inserting the value of one field into another by referencing it as `[variable_name]`. Piped values can be used as parameters in `@DEFAULT` and `@SETVALUE`.

**Smart Variable**

A predefined reference to project or session metadata — for example, `[user-fullname]` returns the logged-in user's full name; `[previous-event-name]` returns the name of the most recently completed event in a longitudinal project. Smart variables can be used in `@DEFAULT` and `@SETVALUE` parameters. Use the green *Smart Variables* button in REDCap for the full list.

---

# 3. Text-Specific Autofill Tags

The following tags pre-fill a specific dynamic value into a text or notes box when the form loads. None of them have parameters. If the field already contains a value, these tags do not overwrite it.

**Applies to:** Text box and notes box. Best practice is to apply the relevant date, date-time, or other validation to the target field.

| Tag | What it pre-fills | Notes |
|---|---|---|
| `@NOW` | Current date and time from the user's device/browser | Matches the field's date-time validation if set |
| `@NOW-SERVER` | Current date and time from the REDCap server | Useful when respondents span multiple time zones |
| `@NOW-UTC` | Current date and time in UTC/GMT | Consistent reference regardless of device or server location |
| `@TODAY` | Current date from the user's device/browser | Does not fill a time component |
| `@TODAY-SERVER` | Current date from the REDCap server | Same as `@NOW-SERVER` but date only |
| `@TODAY-UTC` | Current date in UTC/GMT | Same as `@NOW-UTC` but date only |
| `@LONGITUDE` | Longitude of the user's device | Subject to device privacy settings; may be blank or inaccurate |
| `@LATITUDE` | Latitude of the user's device | Subject to device privacy settings; may be blank or inaccurate |
| `@USERNAME` | REDCap username of the current user | Fills with `survey-participant` when accessed via survey link |
| `@CONSENT-VERSION` | Version number of the active e-consent framework | Only works in surveys with the e-consent framework enabled |

> **Location accuracy note:** `@LONGITUDE` and `@LATITUDE` rely on device-level permissions. Many devices allow users to disable or reduce location accuracy. VPNs and similar tools can return incorrect coordinates. Treat these values as approximate.

> **Survey access note:** `@USERNAME` fills with `survey-participant` when a respondent accesses the instrument via a public survey link (i.e., without logging in to REDCap).

## 3.1 Combining Autofill Tags with @HIDDEN and @READONLY

Autofill tags are frequently combined with visibility and read-only tags to create fields that populate automatically but are not visible or editable by the user. Common examples:

**Hidden timestamp:**
```
@NOW @HIDDEN
```
Records the time the form was first loaded without displaying the field to the user. REDCap tracks survey completion time automatically but not start time — this combination provides a start timestamp.

**Locked username:**
```
@USERNAME @READONLY
```
Pre-populates the field with the current user's username and prevents them from editing it, creating a reliable record of who first opened the form.

---

# 4. @DEFAULT and @SETVALUE

These are the most flexible autofill action tags. Unlike the text-specific tags above, they work across multiple field types and accept static values, raw values, piped variables, and smart variables as parameters.

**Key difference:**

- `@DEFAULT` only fills a field if the form status is "grey" (no data entered yet). It will not overwrite existing data.
- `@SETVALUE` fills the field every time the form is loaded, regardless of whether data is already present. It overwrites existing values.

Use `@DEFAULT` when a field should be pre-filled once and then potentially updated by the respondent. Use `@SETVALUE` when the field should always reflect the most current value on load.

> **Backward compatibility note:** In older REDCap versions, `@PREFILL` was the equivalent of `@SETVALUE`. Both names still work, but `@SETVALUE` is preferred for new projects.

**Applies to:** Text boxes, notes boxes, radio buttons, dropdowns, checkboxes, and slider fields.

## 4.1 Static Text Values (Text Boxes and Notes Boxes)

Place the desired text between quotes after an equals sign:

```
@DEFAULT='Green'
```

Most characters are valid. Single and double quotes cannot appear within the value, as they are used to delimit it.

## 4.2 Raw Values (Radio Buttons, Dropdowns, and Checkboxes)

Use the raw value of the option to pre-select — not the label:

**Single selection (radio button or dropdown):**
```
@DEFAULT='2'
```

**Multiple selections (checkbox):**
```
@DEFAULT='1,2'
```

Alphabetic raw values (e.g., country codes) are also valid:
```
@DEFAULT='USA'
```

## 4.3 Piped Values

Reference a field stored elsewhere in the same record using its variable name in brackets:

```
@DEFAULT='[email]'
```

This pre-fills the field with the value stored in the `email` field for the same record. In a non-longitudinal project, this references the same event; in a longitudinal project, it references the current event.

## 4.4 Smart Variables

Reference project or session metadata using smart variable syntax:

```
@DEFAULT='[user-fullname]'
```

Pre-fills the field with the full name of the currently logged-in user, as stored in their REDCap profile.

## 4.5 Combining Piping and Smart Variables — Longitudinal Example

In a longitudinal project, `@DEFAULT` can carry forward a value from the previous event using the `[previous-event-name]` smart variable:

```
@DEFAULT='[previous-event-name][rx1]'
```

This tells REDCap to look up the value of `rx1` from the most recently completed prior event and pre-fill it in the current event. This is useful for medication lists or other data that changes minimally between time points — respondents can review and update rather than re-entering from scratch.

> **Prerequisites:** This pattern requires familiarity with longitudinal project structure, piping, and smart variables. See RC-LONG-01, the piping training course, and the smart variables reference in REDCap.

---

# 5. Common Questions

**Q: What is the difference between @NOW and @TODAY?**

**A:** `@NOW` fills both the date and the time. `@TODAY` fills the date only. Match the tag to the field's validation type: use `@TODAY` for date-validated fields and `@NOW` for date-time-validated fields.

**Q: When should I use @DEFAULT versus @SETVALUE?**

**A:** Use `@DEFAULT` when the field should be pre-filled once on first open and then potentially changed by the respondent. Use `@SETVALUE` when the field should always reflect a freshly computed or looked-up value, such as always tracking the most recent user to open the form.

**Q: Do autofill tags run during data import or API writes?**

**A:** No. Autofill tags only execute when a form is loaded in a browser. They have no effect during API writes, the Data Import Tool, or any background process.

**Q: Can @DEFAULT or @SETVALUE pre-fill an entire record at once?**

**A:** No. These tags only activate when the specific form containing the tagged field is loaded in a browser. To pre-fill an entire record, every instrument must be opened and saved individually — or values must be written directly via import or API.

**Q: What happens if @USERNAME is used in a survey accessed via a public link?**

**A:** The field is pre-filled with the literal text `survey-participant`. REDCap has no way to identify the individual respondent through an anonymous survey link.

---

# 6. Common Mistakes & Gotchas

**Using @SETVALUE when @DEFAULT was intended.** `@SETVALUE` overwrites existing data every time the form loads. If a respondent has updated a field and the form is reopened, their edit will be overwritten. Use `@DEFAULT` unless overwriting is intentional.

**Using @NOW on a date-only field.** The time component is discarded, which can be confusing. Use `@TODAY` for date-only fields.

**Relying on @LATITUDE / @LONGITUDE for accurate location data.** Device privacy settings, VPNs, and GPS accuracy limitations all affect these values. Treat them as supplementary information rather than precise coordinates.

**Expecting autofill tags to fire during import.** They do not. If pre-populating records at scale, use the Data Import Tool or API directly — autofill tags will not fire until the form is opened in a browser.

---

# 7. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-02 — @HIDDEN & @READONLY: commonly combined with autofill tags to create hidden or locked auto-populated fields
- RC-LONG-01 — Longitudinal Project Setup: required background for the `[previous-event-name]` carry-forward example
- RC-FD-02 — Online Designer: where action tags and field settings are configured

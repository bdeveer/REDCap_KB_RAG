RC-AT-04

**Action Tags — Checkboxes**

| **Article ID** | RC-AT-04 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-03 — Radio/Dropdown Action Tags; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers two action tags designed specifically for checkbox fields: `@NONEOFTHEABOVE`, which enforces mutual exclusivity between a designated "none" option and all other choices, and `@MAXCHECKED`, which limits how many options can be selected at once. Both tags address a common data quality problem — checkboxes allow unrestricted multi-select by default, and these tags add rules that keep responses unambiguous.

---

# 2. Key Concepts & Definitions

**Checkbox Field**

A REDCap field type that allows respondents to select multiple options simultaneously. Unlike radio buttons and dropdowns, checkboxes have no built-in selection limits.

**Raw Value**

The internal code assigned to each checkbox option, set in the Online Designer. `@NONEOFTHEABOVE` references raw values to identify the designated "none" option(s).

---

# 3. @NONEOFTHEABOVE

Designates one or more checkbox options as mutually exclusive "none of the above" options. If a respondent tries to check a designated option alongside any other option, REDCap displays a prompt asking them to either clear the other selections or cancel.

Without this tag, nothing prevents a respondent from checking both "None of the above" and a substantive answer — introducing ambiguity in the dataset that cannot be resolved after the fact.

**Applies to:** Checkbox fields only. Has no effect on radio buttons or dropdowns (which are already single-select).

**Common uses:** Any checkbox question that includes a "none of the above," "not applicable," or "I prefer not to answer" option.

**Syntax — single designated option:**
```
@NONEOFTHEABOVE='99'
```

A numeric raw value can also be used without quotes:
```
@NONEOFTHEABOVE=99
```

**Syntax — multiple designated options:**
```
@NONEOFTHEABOVE='99, 98'
```

When multiple options are designated, they are also mutually exclusive with each other — only one of them can be selected at a time.

> **Example:** If raw values `99` ("None of the above") and `98` ("I don't watch American Football") are both designated, a respondent can select either one but not both simultaneously.

---

# 4. @MAXCHECKED

Limits the maximum number of checkbox options that can be simultaneously checked. Once the limit is reached, all remaining unchecked options are disabled until the respondent unchecks one of the selected options.

**Applies to:** Checkbox fields only.

**Common uses:** "Select up to three" questions where you want the limit enforced rather than just instructed.

**Syntax:**
```
@MAXCHECKED='3'
```

The parameter is the maximum number of simultaneous selections permitted. The tag enforces an upper limit only — it does not enforce a minimum. There is currently no standard action tag to require a minimum number of checked options.

---

# 5. Combining @NONEOFTHEABOVE and @MAXCHECKED

Both tags can be used on the same checkbox field simultaneously. Place them in the annotation box separated by a space:

```
@NONEOFTHEABOVE='99' @MAXCHECKED='3'
```

The tags operate independently and do not interfere with each other. `@NONEOFTHEABOVE` manages the mutual exclusivity of the designated option; `@MAXCHECKED` manages the maximum number of simultaneous selections.

---

# 6. Common Questions

**Q: Can @NONEOFTHEABOVE be used on a radio button or dropdown?**

**A:** No. Radio buttons and dropdowns are inherently single-select — a "none of the above" option in those field types is just another option and works correctly without any action tag.

**Q: With @MAXCHECKED, can a respondent select zero options?**

**A:** Yes. `@MAXCHECKED` enforces a ceiling, not a floor. A respondent can check none, one, or any number up to the defined maximum. There is currently no standard action tag to enforce a minimum.

**Q: Can @NONEOFTHEABOVE designate multiple options, and how do they interact?**

**A:** Yes. Multiple raw values can be designated: `@NONEOFTHEABOVE='99, 98'`. All designated options are mutually exclusive with every other checkbox option and with each other — only one designated option can be selected at a time.

---

# 7. Common Mistakes & Gotchas

**Using @NONEOFTHEABOVE on a radio button or dropdown.** This tag has no effect on those field types. It is only meaningful on checkboxes.

**Using option labels instead of raw values.** `@NONEOFTHEABOVE` requires the raw value of the designated option, not its display label. Check the field's option list in the Online Designer to find the correct raw value.

**Confusing @MAXCHECKED with a minimum requirement.** `@MAXCHECKED` only limits the maximum. A value of `@MAXCHECKED='3'` means "no more than three" — it does not mean "exactly three."

---

# 8. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-03 — Radio/Dropdown Action Tags: `@HIDECHOICE`, `@SHOWCHOICE`, and `@MAXCHOICE` also apply to checkboxes
- RC-FD-02 — Online Designer: where raw values and field options are configured

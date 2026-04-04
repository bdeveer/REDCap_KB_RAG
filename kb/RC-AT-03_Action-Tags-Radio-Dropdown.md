RC-AT-03

**Action Tags — Radio Button & Dropdown**

| **Article ID** | RC-AT-03 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-04 — Checkbox Action Tags; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers action tags designed for structured field types — radio buttons, dropdowns, and (where noted) checkboxes. These tags control the order and availability of choices, and allow limits to be placed on how many times an option can be selected across all records in a project.

> **Note:** With the exception of `@MAXCHOICE`, none of the action tags in this article work on matrix fields.

---

# 2. Key Concepts & Definitions

**Raw Value**

The internal code assigned to each option in a structured field. Raw values are set in the Online Designer and are distinct from the option labels users see. `@HIDECHOICE`, `@SHOWCHOICE`, and `@MAXCHOICE` all reference raw values in their parameters.

**Structured Field Type**

A field type with a predefined set of selectable options: radio buttons, dropdowns, and checkboxes. Matrix fields are a special case — most action tags in this article do not support them.

---

# 3. @RANDOMORDER

Randomly reorders the display of options in a radio button, dropdown, or checkbox field every time the page loads. The raw values and stored data are unaffected — only the visual sequence changes.

**Applies to:** Radio buttons, dropdowns, checkboxes. Does not work on matrix fields.

**Common uses:** Reducing order bias in surveys, where respondents may systematically favor earlier-listed options.

**Syntax** (no parameters):
```
@RANDOMORDER
```

The number of possible orderings depends on the number of options. A field with five options has 120 permutations; a yes/no field has 2.

---

# 4. @HIDECHOICE

Hides one or more specific options in a structured field while preserving those options in existing records where they were already selected. This is useful when an option becomes unavailable (e.g., a registration slot closes, a staff member leaves) but removing it from the field definition would delete historical data.

- For existing records where the hidden option is already selected, the option continues to display normally.
- For new data entry, the hidden option is not visible and cannot be selected.

> **Note:** If a record with a previously selected hidden option is opened, the hidden option displays. However, if the user deselects it and saves, the option will no longer be available on subsequent opens.

**Applies to:** Radio buttons, dropdowns, checkboxes.

**Syntax — single option:**
```
@HIDECHOICE='1'
```

**Syntax — multiple options:**
```
@HIDECHOICE='1, 2'
```

Use the raw value of the option, not the label. Separate multiple raw values with commas inside a single set of quotes.

---

# 5. @SHOWCHOICE

The inverse of `@HIDECHOICE`. Where `@HIDECHOICE` starts from a default of showing all options and hides the listed ones, `@SHOWCHOICE` starts from a default of hiding all options and shows only the listed ones.

Use `@SHOWCHOICE` when the list of options to hide is longer than the list to show. The end result for the user is identical regardless of which tag is used — the choice is purely one of convenience based on which list is shorter.

**Applies to:** Radio buttons, dropdowns, checkboxes.

**Syntax** (identical to `@HIDECHOICE`):
```
@SHOWCHOICE='3'
@SHOWCHOICE='3, 4'
```

> **Note:** If `@HIDECHOICE` and `@SHOWCHOICE` both target the same option on the same field, `@SHOWCHOICE` wins — that option will be shown.

---

# 6. @MAXCHOICE

Sets a maximum number of times a given option can be selected across all records in the project. Once the limit is reached, the option is greyed out and cannot be selected by new respondents.

`@MAXCHOICE` is project-wide, not per-record. It checks counts on page load by tallying saved records. If two respondents load the same form simultaneously when only one slot remains, both may be able to select the limited option — this is a known limitation but occurs rarely in practice.

**Applies to:** Radio buttons, dropdowns, checkboxes, and matrix fields (the only tag in this article that works on matrix fields).

**Common uses:** Class or event registration with per-option seat limits.

**Syntax:**
```
@MAXCHOICE(1=25,2=30,3=30)
```

Each entry maps a raw value to a maximum count: `raw_value=limit`. Separate entries with commas. Options not listed have no cap.

**Example — single option limit:**
```
@MAXCHOICE(1=25)
```

## 6.1 Combining @MAXCHOICE with Other Tags

- **@MAXCHOICE + @HIDECHOICE:** Hides an option entirely once its limit is reached, rather than greying it out. Requires manual monitoring — when the limit is hit, `@HIDECHOICE` must be added manually for that option.
- **@MAXCHOICE + @RANDOMORDER:** Randomizes the display order of options while still enforcing per-option limits, reducing the tendency for respondents to select the first available item.

---

# 7. Common Questions

**Q: Does @HIDECHOICE affect the stored data for records that already have the hidden option selected?**

**A:** No. Existing records retain their stored value. `@HIDECHOICE` only prevents new selections of the hidden option. Existing records display the option normally until it is deselected and saved, at which point it becomes inaccessible.

**Q: Can @SHOWCHOICE and @HIDECHOICE be used on the same field at the same time?**

**A:** Yes, but `@SHOWCHOICE` takes precedence when both tags target the same option. In practice, mixing the two tags on the same field is uncommon and can be confusing to maintain.

**Q: Does @RANDOMORDER affect the stored raw value when an option is selected?**

**A:** No. `@RANDOMORDER` changes only the visual display order. The raw values assigned to each option remain fixed, and the stored value is always the raw value of the selected option regardless of where it appeared on screen.

**Q: Does @MAXCHOICE work in real time across concurrent users?**

**A:** No. The count is checked on page load based on saved records. Two users simultaneously submitting the last available slot can both succeed. Design your project with this in mind for high-traffic registration scenarios.

---

# 8. Common Mistakes & Gotchas

**Using option labels instead of raw values in parameters.** `@HIDECHOICE`, `@SHOWCHOICE`, and `@MAXCHOICE` all require raw values, not labels. If the raw value for "Fall Quarter" is `1`, use `@HIDECHOICE='1'`, not `@HIDECHOICE='Fall Quarter'`.

**Applying these tags to matrix fields.** `@RANDOMORDER`, `@HIDECHOICE`, and `@SHOWCHOICE` do not work on matrix fields. Only `@MAXCHOICE` supports matrix fields.

**Relying on @MAXCHOICE for strict slot enforcement.** Due to the page-load timing of count checks, concurrent submissions can exceed defined limits. For strict capacity control, consider alternative approaches such as closing the survey or using automated alerts to monitor counts.

---

# 9. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-04 — Checkbox Action Tags: `@NONEOFTHEABOVE` and `@MAXCHECKED`, which are specific to checkboxes
- RC-FD-02 — Online Designer: where action tags and field options are configured

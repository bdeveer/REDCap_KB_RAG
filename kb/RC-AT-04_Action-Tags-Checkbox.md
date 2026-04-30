RC-AT-04

**Checkbox Action Tags**

| **Article ID** | RC-AT-04 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Overview; RC-AT-03 — Radio/Dropdown Tags; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers action tags designed specifically for checkbox fields: `@NONEOFTHEABOVE` and `@MAXCHECKED`. These tags enforce selection rules that improve data quality.

---

# 2. @NONEOFTHEABOVE

Designates one or more options as mutually exclusive "none of the above" choices. If a respondent tries to select a designated option alongside other options, REDCap displays a prompt asking them to either clear the other selections or cancel.

This prevents ambiguous data where a "none of the above" response is combined with substantive answers.

> **Important:** This tag only works on **checkbox** fields, not radio buttons or dropdowns.

**Syntax — single option:**
```
@NONEOFTHEABOVE='99'
```

**Syntax — without quotes (numeric raw value):**
```
@NONEOFTHEABOVE=99
```

**Syntax — multiple options:**
```
@NONEOFTHEABOVE='99, 98'
```

Use the raw value of the option(s). Multiple designated options are mutually exclusive with each other as well.

**Negative integers as raw values:**

Negative integers (e.g., `-9`, `-99`) are valid raw values and work correctly with `@NONEOFTHEABOVE`. A common convention is to reserve a negative value specifically for "Prefer not to say" or "Not applicable" options, keeping them visually and semantically distinct from substantive answer codes:

```
@NONEOFTHEABOVE='-9'
```

Using a consistent negative coding scheme across a project makes it easy to identify and filter these responses in reports and exports.

**Use cases:**
- Survey questions with a "None of the above" option that should not be combined with other answers.
- "Prefer not to say" or "Not applicable" responses that must remain mutually exclusive with substantive answers.

---

# 3. @MAXCHECKED

Limits the maximum number of checkboxes that can be simultaneously selected. Once the limit is reached, remaining unchecked options are disabled until the respondent unchecks one of the selected options.

> **Note:** This enforces a ceiling only. It does not require a minimum number of selections. There is currently no action tag to enforce a minimum.

**Syntax:**
```
@MAXCHECKED='3'
```

The parameter is the maximum number of simultaneously selected checkboxes.

**Use case:** Survey questions where respondents are asked to "select up to 3 options" — the tag enforces the limit automatically.

---

# 4. Combining @NONEOFTHEABOVE and @MAXCHECKED

These two tags can be used together on the same checkbox field without conflict:

```
@NONEOFTHEABOVE='99' @MAXCHECKED='3'
```

Both operate independently and do not interfere with each other.

---

# 5. Common Questions

**Q: Can @NONEOFTHEABOVE be used on radio buttons or dropdowns?**

**A:** No. These field types are inherently single-select and do not need this tag. It only works on checkboxes.

**Q: Does @MAXCHECKED require a minimum number of selections?**

**A:** No. It only sets a maximum. A respondent can select 0, 1, 2, or 3 options (if the limit is 3). To enforce a minimum, you would need to use branching logic or custom validation.

**Q: What happens if a respondent selects a "none of the above" option along with other options?**

**A:** REDCap displays a prompt asking the respondent to either clear the other selections or cancel their action. The form does not save until they resolve the conflict. This ensures data integrity — the record cannot have both "none of the above" and substantive answers simultaneously.

**Q: Can I have multiple "none of the above" options on the same checkbox field?**

**A:** Yes. Use `@NONEOFTHEABOVE='99, 98, 97'` to designate multiple options as mutually exclusive. They are all mutually exclusive with each other as well as with any non-designated options.

**Q: If I add @MAXCHECKED after respondents have already selected more than the limit, what happens?**

**A:** When those respondents return to the form, any excess selections remain checked and visible (the tag does not retroactively remove selections). However, they will not be able to select additional unchecked options until they uncheck enough to fall below the limit.

---

# 6. Common Mistakes & Gotchas

**Forgetting that @NONEOFTHEABOVE only works on checkboxes.** Trying to use it on radio buttons or dropdowns will have no effect, and no error is raised. Verify the field type before applying the tag.

**Designating the wrong raw value as "none of the above."** If the raw value in `@NONEOFTHEABOVE` does not match an actual option's raw value, the tag will silently fail. Double-check the coded value in the field's choices list.

**Assuming @MAXCHECKED prevents saving when over the limit.** The limit is enforced by disabling unchecked options, not by preventing form submission. A respondent cannot check additional options, but if they somehow exceed the limit (e.g., via data import or editing via the API), the saved data will reflect the excess.

---

# 7. Related Articles

- RC-AT-01 — Action Tags Overview
- RC-AT-03 — Radio/Dropdown Action Tags
- RC-FD-02 — Online Designer

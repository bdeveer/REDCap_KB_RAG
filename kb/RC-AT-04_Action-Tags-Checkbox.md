RC-AT-04

**Checkbox Action Tags**

| **Article ID** | RC-AT-04 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
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

**Use case:** Survey questions with a "None of the above" option that should not be combined with other answers.

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

---

# 6. Related Articles

- RC-AT-01 — Action Tags Overview
- RC-AT-03 — Radio/Dropdown Action Tags
- RC-FD-02 — Online Designer

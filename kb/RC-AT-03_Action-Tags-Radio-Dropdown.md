RC-AT-03

**Radio & Dropdown Action Tags**

| **Article ID** | RC-AT-03 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Overview; RC-AT-04 — Checkbox Tags; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers action tags designed for radio button and dropdown fields: `@RANDOMORDER`, `@HIDECHOICE`, `@SHOWCHOICE`, and `@MAXCHOICE`. These tags do not work on matrix fields (except `@MAXCHOICE`).

---

# 2. @RANDOMORDER

Randomizes the visual order of options every time a page loads. The underlying raw values and stored data are unaffected — only the display order changes.

**Use case:** Preventing option-order bias in surveys (e.g., respondents systematically choosing the first option).

**Syntax:**
```
@RANDOMORDER
```

**Notes:**
- Works on radio buttons, dropdowns, and checkboxes
- A yes/no field has 2 possible permutations; a 5-option field has 120
- No parameters required

---

# 3. @HIDECHOICE

Hides one or more specific options from a field while preserving those options in records where they were already selected.

> **Note:** If a respondent with a hidden option selected opens the form and saves it without changes, the hidden option is preserved. If they deselect and reselect, the hidden option becomes unavailable.

**Syntax — single option:**
```
@HIDECHOICE='1'
```

**Syntax — multiple options:**
```
@HIDECHOICE='1, 2'
```

Use the raw value of the option(s), not the label. Separate multiple values with commas.

**Use case:** Marking class spots as filled in a registration form, or hiding expired options while preserving historical selections.

---

# 4. @SHOWCHOICE

The inverse of `@HIDECHOICE`. Starts with all options hidden and shows only the listed ones.

Use `@SHOWCHOICE` when the number of options to hide is larger than the number to show — it is cleaner to list what to show.

**Syntax:**
```
@SHOWCHOICE='1, 2, 3'
```

> **Note:** If both `@HIDECHOICE` and `@SHOWCHOICE` target the same option, `@SHOWCHOICE` takes precedence and the option will be shown.

---

# 5. @MAXCHOICE

Limits how many times a given option can be selected across all project records. Once the limit is reached, the option is greyed out and unavailable to new respondents.

**Syntax:**
```
@MAXCHOICE(1=25,2=30,3=30)
```

Each entry is `raw_value=limit`. Separate multiple entries with commas.

**Important:** `@MAXCHOICE` checks counts on page load only, not in real time. If two respondents load the form simultaneously when one slot remains, both may be able to select it.

**Use case:** Class registration with limited spots, event sign-ups with capacity limits.

**Combining with other tags:**

- `@MAXCHOICE` + `@HIDECHOICE`: Hides the greyed-out option entirely (requires manual monitoring)
- `@MAXCHOICE` + `@RANDOMORDER`: Randomizes option order while enforcing limits

---

# 6. Common Questions

**Q: Can these tags be combined?**

**A:** Yes. For example, `@MAXCHOICE(1=25) @RANDOMORDER` enforces a limit while randomizing order.

**Q: Do these tags work on matrix fields?**

**A:** `@RANDOMORDER`, `@HIDECHOICE`, and `@SHOWCHOICE` do not work on matrix fields. `@MAXCHOICE` is the exception and does work on matrix fields.

---

# 7. Related Articles

- RC-AT-01 — Action Tags Overview
- RC-AT-04 — Checkbox Action Tags
- RC-FD-02 — Online Designer

RC-CALC-02

**Calculated Fields**

| **Article ID** | RC-CALC-02 |
|---|---|
| **Domain** | Calculations & Special Functions |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-02 — Online Designer; RC-BL-02 — Branching Logic: Syntax & Atomic Statements |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CALC-01 — Special Functions Reference; RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE; RC-FD-03 — Data Dictionary; RC-FD-08 — Data Dictionary: Column Reference |

---

# 1. Overview

This article covers REDCap's **Calculated Field** — a dedicated field type whose value is computed automatically from a formula rather than entered manually. Calculated fields always return a number. If you need a calculation that produces a text result, use `@CALCTEXT`. If you need to compute a date, use `@CALCDATE` or the `datediff()` family of functions. This article explains how to create and configure calculated fields, how formulas work, when the value updates, and how calculated fields compare to the `@CALCTEXT` and `@CALCDATE` action tags.

For the full reference on Special Functions that can be used inside formulas (such as `datediff()`, `round()`, `sum()`, and `if()`), see RC-CALC-01 — Special Functions Reference.

---

# 2. Key Concepts & Definitions

**Calculated Field**

A REDCap field type (field type = `calc`) that stores the result of a formula expression. The value is computed automatically and cannot be edited by users. The result must be a number — either an integer or a decimal.

**Formula**

The expression entered into a calculated field that determines its value. Formulas use the same variable reference syntax and operators as REDCap branching logic, plus Special Functions. A formula must resolve to a numeric value; non-numeric results are not stored.

**Recalculation**

The process by which REDCap recomputes a calculated field's value whenever its inputs change. Recalculation happens automatically in certain contexts — see Section 5 for the full list.

**Read-Only**

Calculated fields are read-only for all users, regardless of user rights. Users cannot click into the field and type a value. The displayed value is always the result of the formula.

**Data Quality Rule H**

A built-in Data Quality rule that re-evaluates all calculated fields across all records in a project. Running rule H forces recalculation even for records where the form has not been opened recently.

---

# 3. Creating a Calculated Field

## 3.1 Online Designer

1. Open the instrument in the **Online Designer**.
2. Click **Add Field** (or edit an existing field with the pencil icon).
3. In the **Field Type** dropdown, select **Calculated Field**.
4. Enter a **Field Label** — the text displayed above the computed value.
5. Enter a **Variable Name** following REDCap naming rules (lowercase letters, numbers, underscores; no spaces).
6. Enter the formula in the **Calculation Equation** box. Use the **Special Functions** button in the toolbar to browse available functions.
7. Click **Save**.

> **Tip:** The Online Designer validates formula syntax when you save. If your formula references an unknown variable or has unbalanced brackets, the designer will flag the error and prevent saving. However, it does not verify that the formula logic is correct — test your formula against real or realistic data before going to Production.

## 3.2 Data Dictionary

In the Data Dictionary CSV, a calculated field is defined as follows:

| **Column** | **Value** |
|---|---|
| Field Type | `calc` |
| Choices, Calculations, OR Slider Labels | The formula expression |
| Text Validation Type | Leave blank |
| Text Validation Min / Max | Leave blank |

The formula goes in the **Choices, Calculations, OR Slider Labels** column — the same column used for answer choices on radio/dropdown fields. Leave all validation columns empty; calculated fields do not support validation.

> **Important:** When editing a formula in Excel before uploading the Data Dictionary, avoid using double quotation marks inside the formula — Excel may corrupt them during CSV export. Use single quotes for any quoted values within the formula, or verify the exported file in a plain text editor before uploading.

---

# 4. Formula Syntax

Calculated field formulas use the same syntax as REDCap branching logic:

- **Variable references:** `[variable_name]` — references the value of another field in the same record
- **Arithmetic operators:** `+`, `-`, `*`, `/`, `^` (exponent — wrap both base and exponent in parentheses: `([base])^([exponent])`)
- **Parentheses:** control order of operations, same as standard math
- **Special Functions:** `datediff()`, `round()`, `sum()`, `if()`, and others — see RC-CALC-01

**Examples:**

| **Goal** | **Formula** |
|---|---|
| Sum two scores | `[score_a]+[score_b]` |
| BMI from kg and cm (1 decimal) | `round(([weight]*10000)/(([height])^(2)), 1)` |
| Age in whole years | `age_at_date([dob], [visit_date])` |
| Days since baseline | `datediff([baseline_date], 'today', 'd')` |
| Total from three items, blank if any item is blank | `[item1]+[item2]+[item3]` |
| Total that calculates even with some items blank | `sum([item1], [item2], [item3])` |

> **Cross-event references in longitudinal projects:** To reference a field from a different event, use the standard cross-event syntax: `[unique_event_name][variable_name]`. Example: `datediff([baseline_arm_1][baseline_date], 'today', 'd')`.

---

# 5. The Numeric-Only Constraint

**Calculated fields must always return a number.** This is the single most important constraint of the field type. Formulas that produce text strings, date strings, or mixed outputs will not store a value — the field will appear blank.

This constraint has two practical consequences:

**If you need text output** — use `@CALCTEXT` on a Text Box field instead. `@CALCTEXT` can return conditional text strings, display labels, or a mix of text and numbers. See RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE.

**If you need a date output** — use `@CALCDATE` on a Text Box field with date validation. `@CALCDATE` returns a formatted date string by adding or subtracting time from a source date. If you only need the *number of days* between two dates (a numeric result), you can use `datediff()` in a regular calculated field. See RC-AT-09 and RC-CALC-01.

| **Need** | **Solution** |
|---|---|
| A numeric result (integer or decimal) | Calculated Field |
| A text result (labels, categories, conditional text) | Text Box + `@CALCTEXT` |
| A date result (computed follow-up date, deadline) | Text Box with date validation + `@CALCDATE` |
| Number of days/years between two dates | Calculated Field with `datediff()` |

---

# 6. When Values Update

A calculated field's value is recomputed in three contexts:

**During data entry (real-time).** When a user is actively entering data on a form, calculated fields update instantly as input values change — without saving the form or refreshing the page.

**During data import.** When records are imported via the Data Import Tool or API, REDCap recalculates all calculated fields whose input variables are included in the import file. Fields not included in the import are not recalculated.

**When Data Quality rule H is run.** Rule H specifically targets calculated fields across all records in the project. Running rule H forces REDCap to evaluate every calculated field expression for every record, correcting any stale values. This is useful after making formula changes, after bulk imports, or when formula dependencies have changed.

> **Note:** Calculated fields are not updated when you edit a branching logic condition, rename a field, or make other project design changes. Run Data Quality rule H after any design changes that affect a formula to ensure all stored values are current.

---

# 7. Display Behavior and Read-Only Enforcement

**Display.** During data entry, the calculated value is displayed in the field as soon as all input variables have values. If any input variable is blank, the displayed value depends on the formula: a `sum()` of blanks returns 0; arithmetic with `+` returns blank if any operand is blank. The stored value matches what is displayed.

**Decimal places.** REDCap stores and displays however many decimal places the formula produces. If you want a specific number of decimal places, wrap the formula in `round()`, `roundup()`, or `rounddown()`. Example: `round([weight]/([height])^(2)*703, 1)` stores and displays one decimal place.

**Read-only.** All users see a calculated field as read-only regardless of their user rights. The field appears with a grey background or as non-editable text. There is no user right or project setting that makes a calculated field editable.

**Storage.** The computed value is stored in the database when the form is saved. The formula itself is not stored per-record — only the numeric result is. If you later change the formula, existing records retain the old computed value until Data Quality rule H is run or the record is opened and re-saved.

---

# 8. Common Questions

**Q: What is the difference between a Calculated Field and a Text Box with @CALCTEXT?**

**A:** A Calculated Field can only store a number. A Text Box with `@CALCTEXT` can store text, numbers, or date strings. Both are read-only and update in the same contexts (real-time, import, Data Quality rule H). Use a Calculated Field for numeric results. Use `@CALCTEXT` when you need to output text — for example, a risk category label, a yes/no interpretation, or a concatenated value.

**Q: My calculated field is showing blank. Why?**

**A:** The most common causes are: (1) one or more input variables is blank — if you use `+` operators, any blank input makes the whole expression blank; (2) the formula result is not a number (e.g., the formula produces a text string or date); (3) the formula references a variable that doesn't exist or is spelled incorrectly. Check the formula in the Online Designer's syntax validator and test it against a record where all inputs are filled in.

**Q: Can I use a calculated field to compute a date — for example, a follow-up appointment 30 days after baseline?**

**A:** Not directly. A Calculated Field returns a number, not a formatted date string. `datediff([baseline_date], 'today', 'd')` will return the number of days between two dates, which is numeric and valid for a Calculated Field. But if you want to store and display an actual follow-up date (e.g., "2026-05-15"), use a Text Box with date validation and `@CALCDATE([baseline_date], 30, 'd')` instead.

**Q: Does changing a formula update all existing records automatically?**

**A:** No. Changing a formula in the Online Designer updates how future calculations are performed but does not retroactively recalculate existing records. To update all existing records after a formula change, run Data Quality rule H from the Data Quality module.

**Q: Can I use branching logic to control whether a calculated field is visible?**

**A:** Yes. Branching logic can be applied to a calculated field just like any other field — if the logic is false, the field is hidden and its stored value is cleared. Be careful: if branching logic hides a calculated field after a value has been computed, the stored value is deleted.

**Q: Can a calculated field reference fields from other instruments?**

**A:** Yes. Any variable within the same record can be referenced in a formula, regardless of which instrument it belongs to. In longitudinal projects, use the cross-event syntax to reference fields from other events: `[event_name][variable_name]`.

**Q: Can I use if() inside a calculated field to return different numbers based on a condition?**

**A:** Yes. The `if()` function is fully supported in calculated fields. Example: `if([bmi]>=30, 1, 0)` returns 1 if BMI is 30 or above, otherwise 0. Both return values must be numbers — if either return value is a text string, the result will not store.

**Q: How do I control how many decimal places the calculated field displays?**

**A:** Wrap your formula in a rounding function. `round(formula, 2)` rounds to 2 decimal places, `round(formula, 0)` gives a whole number, `rounddown(formula, 1)` always rounds down to 1 decimal. Without a rounding function, REDCap stores and displays the full precision of the result.

---

# 9. Common Mistakes & Gotchas

**Expecting a text result to be stored.** Formulas that produce a non-numeric result — including text strings, date strings, or empty strings — will not store a value in the calculated field. The field will appear blank. If you need a non-numeric result, switch to a Text Box field with `@CALCTEXT` or `@CALCDATE`.

**Using + instead of sum() when some inputs may be blank.** If any variable in `[a]+[b]+[c]` is blank, the entire expression returns blank — not a partial sum. This is often unexpected when scoring instruments where some items are optional. Use `sum([a], [b], [c])` to get a result even when some inputs are blank. Be aware that `sum()` silently excludes blank values from the total, which can produce a misleadingly high score if many items are empty.

**Not running Data Quality rule H after a formula change.** Editing a formula updates future calculations but leaves existing records with their old computed values. Stale values persist until the record is opened and saved, or until rule H is run. After any formula change in a project with existing data, run rule H to synchronize all records.

**Forgetting parentheses in exponentiation.** REDCap requires both the base and the exponent to be individually wrapped in parentheses: `([base])^([exponent])`. Writing `[height]^2` will not compute correctly. The correct form is `([height])^(2)`.

**Editing formulas in Excel before Data Dictionary upload.** Excel can corrupt special characters — including single and double quotes — when saving CSV files. A formula that looks correct in Excel may fail to parse when uploaded. After editing a formula in Excel, always open the saved CSV in a plain text editor to verify the formula is intact before uploading.

---

# 10. Related Articles

- RC-CALC-01 — Special Functions Reference (full reference for `datediff()`, `round()`, `sum()`, `if()`, and all other functions usable in formulas)
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE (for text output or date output calculations)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (the shared variable reference and operator syntax)
- RC-FD-02 — Online Designer (where calculated fields are created and formulas entered)
- RC-FD-03 — Data Dictionary (bulk field creation including calculated fields)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (column layout for the `calc` field type)
- RC-DE-02 — Basic Data Entry (how calculated field values appear during data entry)

RC-AT-09

**Action Tags — @CALCTEXT and @CALCDATE: Calculation Action Tags**

| **Article ID** | RC-AT-09 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview; familiarity with REDCap calculated fields |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-06 — Autofill Action Tags; RC-AT-08 — @IF; RC-DE-05 — Field Validations |

---

# 1. Overview

`@CALCTEXT` and `@CALCDATE` are action tags that turn a standard Text Box field into a calculated field — one whose value is computed automatically from other field values rather than entered manually. Unlike the built-in **Calculated Field** type, these tags work inside ordinary Text Boxes and offer expanded output options (text strings, conditional text, and date arithmetic).

Both tags behave like calculated fields in key ways: the field is not editable by users, the value updates in real time during data entry, and the value can be updated via data import or when Data Quality rule H is run.

> **Do not use @CALCTEXT or @CALCDATE inside @IF.** The calculation tags operate in more contexts than `@IF` does (real-time recalculation, imports, Data Quality rules). Nesting them inside `@IF` produces unpredictable results. See RC-AT-08 for guidance on `@IF`.

---

# 2. Key Concepts & Definitions

**Calculated Field**

A REDCap field type whose value is determined by a formula rather than user input. The built-in Calculated Field type returns numeric values only. `@CALCTEXT` and `@CALCDATE` extend this concept to text strings and date values respectively.

**if() Function**

A logical function used inside `@CALCTEXT` and `@CALCDATE` expressions. Syntax: `if(condition, value_if_true, value_if_false)`. Equivalent to the IF formula in spreadsheet applications.

**Escaping**

When text inside `@CALCTEXT` contains a quote character that matches the surrounding delimiter, a backslash must precede it to prevent a parsing error — e.g., `'The user\'s guide'`.

---

# 3. @CALCTEXT

`@CALCTEXT` evaluates a logical expression and outputs the result as text into a Text Box field. The expression is typically built around an `if()` function, but any valid REDCap formula that returns a value can be used.

**Applies to:** Text Box fields only. Does not work on any other field type.

**Syntax:**
```
@CALCTEXT(expression)
```

The expression is placed inside the parentheses and follows standard REDCap formula syntax (the same syntax used in the formula field of a Calculated Field).

## 3.1 Basic Example — Conditional Text Output

Output the word "male" or "female" based on a coded sex field:

```
@CALCTEXT(if([sex]='1', 'male', 'female'))
```

## 3.2 Returning Numbers

The return value does not have to be text. A numeric expression is valid:

```
@CALCTEXT(if([age] >= 18, 'adult', 5*[other_field]))
```

This outputs `'adult'` for participants 18 or older, or a calculated number for others.

## 3.3 Returning Piped Values and Smart Variables

Field variables and Smart Variables can be used as return values directly (without quotes):

```
@CALCTEXT(if([age] >= 18, [dob], [event-label]))
```

> **Restriction:** Field variables and Smart Variables **cannot** be piped inside quotes in the return value. `@CALCTEXT(if([x]='1', 'Value: [other_field]', ''))` will not substitute `[other_field]` — it will output the literal string `Value: [other_field]`. Use the variable as a standalone return value, not embedded in a quoted string.

## 3.4 Escaping Quotes in Text Output

If the output text contains a single apostrophe and the surrounding delimiter is also a single apostrophe, escape it with a backslash:

```
@CALCTEXT(if([field]='4', 'The user\'s guide', 'something else'))
```

Alternatively, use double quotes as the outer delimiter when the text contains apostrophes (no escaping needed):

```
@CALCTEXT(if([field]='4', "The user's guide", 'something else'))
```

---

# 4. @CALCDATE

`@CALCDATE` calculates a new date or datetime value by adding or subtracting a specified amount of time from a source date field. It is used for computing follow-up dates, deadlines, or scheduled time points relative to a baseline date.

**Applies to:** Text Box fields with date, datetime, or datetime_seconds validation. Both the source field and the result field must have date or datetime validation.

**Syntax:**
```
@CALCDATE(source, offset, unit)
```

| Parameter | Description |
|---|---|
| `source` | A date/datetime field variable, or an `if()` expression that returns a date/datetime value. In longitudinal projects, include the event: `[baseline_event][visit_date]`. |
| `offset` | A number (integer or decimal) to add. Use a negative number to subtract (go back in time). |
| `unit` | A quoted string specifying the unit: `'y'` (years), `'M'` (months), `'d'` (days), `'h'` (hours), `'m'` (minutes), `'s'` (seconds). |

> **Year and month lengths:** `'y'` uses 365.2425 days per year. `'M'` uses 30.44 days per month. For precise day-count calculations, use `'d'` instead.

## 4.1 Basic Example — Add Days

Calculate a date 7 days after a visit date:

```
@CALCDATE([visit_date], 7, 'd')
```

## 4.2 Subtracting Time

Calculate a date 30 days before a deadline:

```
@CALCDATE([deadline_date], -30, 'd')
```

## 4.3 Longitudinal Projects — Cross-Event Reference

Reference a date field from a specific event:

```
@CALCDATE([baseline_event][visit_date], 7, 'd')
```

## 4.4 Using 'now' or 'today' as the Source

The keywords `now` and `today` can be used as the source parameter. They use the **server time**, not the user's local device time:

```
@CALCDATE(today, 14, 'd')
```

This calculates a date 14 days from the current server date. Be aware that if users are in a different timezone from the server, the date may differ from their local today.

## 4.5 Using an if() Expression as the Source

The source can be a logical expression that resolves to a date value:

```
@CALCDATE(if([use_alt_date]='1', [alt_date], [primary_date]), 30, 'd')
```

---

# 5. Comparison: @CALCTEXT / @CALCDATE vs. Built-in Calculated Field

| Feature | Built-in Calculated Field | @CALCTEXT / @CALCDATE |
|---|---|---|
| Output type | Numeric only | Text or date/datetime |
| Conditional logic | Not supported | Supported via `if()` |
| Real-time update | Yes | Yes |
| Updates via data import | Yes | Yes |
| Updates via Data Quality rule H | Yes | Yes |
| Field type required | Calculated Field | Text Box |
| Editable by users | No | No |

Use the built-in Calculated Field when you need a numeric result. Use `@CALCTEXT` or `@CALCDATE` when you need text output, conditional text, or date arithmetic.

---

# 6. Common Questions

**Q: Can @CALCTEXT output a blank value?**

**A:** Yes. Use an empty string as the return value: `@CALCTEXT(if([field]='1', 'Yes', ''))`. The field will display blank when the false condition is met.

**Q: When does @CALCDATE update its value?**

**A:** The same contexts as a built-in calculated field: in real time during data entry on the form, during a data import, and when Data Quality rule H is run. The value is not updated by API writes directly to the field itself.

**Q: Can I use @CALCTEXT on a field with validation (e.g., integer validation)?**

**A:** The tag works on Text Box fields regardless of validation, but the output must match the validation format. If the computed text does not match the validation rule, the value will be rejected. Use text-only fields (no validation) unless you are certain the output will always conform.

**Q: What is the difference between @CALCDATE and just using a Calculated Field for dates?**

**A:** The built-in Calculated Field type returns a number. Date arithmetic in a Calculated Field returns the number of days between dates, not a formatted date value. `@CALCDATE` returns an actual date string in the format expected by the field's validation, making it directly usable as a displayed date.

---

# 7. Common Mistakes & Gotchas

**Piping a variable inside quotes in @CALCTEXT.** Writing `@CALCTEXT(if([x]='1', 'Hello [name]', ''))` will output the literal text `Hello [name]`, not the value of `[name]`. Use the variable as a standalone return value outside quotes: `@CALCTEXT(if([x]='1', [name], ''))`.

**Using @CALCTEXT or @CALCDATE inside @IF.** This combination is explicitly unsupported and produces unpredictable behavior. Apply calculation tags directly to the field without wrapping them in `@IF`.

**Source or result field missing date validation for @CALCDATE.** Both fields must have date, datetime, or datetime_seconds validation. Without this, `@CALCDATE` will not function correctly.

**Forgetting that 'now' and 'today' use server time.** If your REDCap server is in a different timezone from your users, `@CALCDATE(today, ...)` may produce a date that is one day off. Use `'d'` offsets cautiously when timezone alignment matters.

**Not escaping apostrophes in text output.** If `@CALCTEXT` output contains an apostrophe and you used apostrophes as delimiters, escape it: `'it\'s'` or switch to double quotes: `"it's"`.

---

# 8. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-06 — Autofill Action Tags: `@DEFAULT` and `@SETVALUE` for pre-filling values at page load
- RC-AT-08 — @IF: conditional action tag logic; note that @CALCTEXT and @CALCDATE cannot be nested inside @IF
- RC-DE-05 — Field Validations: date and datetime validations required by @CALCDATE

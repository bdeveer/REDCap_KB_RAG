---
id: RC-AT-09
title: 'Action Tags — @CALCTEXT and @CALCDATE: Calculation Action Tags'
domain: Action Tags
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — action
  tag behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-AT-01 — Action Tags: Overview'
- familiarity with REDCap calculated fields
version: '1.4'
last_updated: 2026-11
related:
- id: RC-AT-01
  title: 'Action Tags: Overview'
- id: RC-AT-06
  title: Autofill Action Tags
- id: RC-AT-08
  title: 'Action Tags: @IF — Conditional Logic'
- id: RC-DE-05
  title: Field Validations
tags:
- action tags
synonyms:
- '@CALCTEXT action tag'
- '@CALCDATE action tag'
- how do i make a calculated text field
- calculate a date difference with an action tag
- turn a text box into a calculated field
- conditional text output with @CALCTEXT
- date arithmetic action tag
- calc field that returns text instead of a number
---

# 1. Overview

`@CALCTEXT` and `@CALCDATE` are action tags that turn a standard Text Box field into a calculated field — one whose value is computed automatically from other field values rather than entered manually. Unlike the built-in **Calculated Field** type, these tags work inside ordinary Text Boxes and offer expanded output options (text strings, conditional text, and date arithmetic).

Both tags behave like calculated fields in key ways: the field is not editable by users, the value updates in real time during data entry, and the value is recalculated when the record is saved or its input fields are imported. Data Quality rule H lists out-of-date values and updates them when you click **Fix calcs now**.

The field is read-only only while the calculation is active. A tag that cannot run — for example `@CALCDATE` on a Text Box without date validation — does nothing, and the field stays editable.

> **Do not use @CALCTEXT or @CALCDATE inside @IF.** The calculation tags operate in more contexts than `@IF` does (real-time recalculation, imports, Data Quality rules). Nesting them inside `@IF` produces unpredictable results. See [RC-AT-08 — Action Tags: @IF — Conditional Logic](RC-AT-08_Action-Tags-Conditional-IF.md) for guidance on `@IF`.

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

> **Version caveat (below 17.5.1 Standard / 17.3.14 LTS):** A `@CALCTEXT` field that outputs **HTML tags**, piped onto a **different page** of the same multipage survey, had all its HTML stripped. It displayed correctly when piped on the field's own page. On affected versions, pipe it on the same page or upgrade.

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

**Applies to:** Text Box fields with date, datetime, or datetime_seconds validation. The result field must have one of these validations (any format — YMD, MDY or DMY); without it, nothing is calculated. The source should also be a date or datetime field: REDCap reads the source date's format from the first date-validated field in the first parameter, and assumes YMD if there is none.

**Syntax:**
```
@CALCDATE(source, offset, unit)
```

| Parameter | Description |
|---|---|
| `source` | A date/datetime field variable, or an `if()` expression that returns a date/datetime value. In longitudinal projects, include the event: `[baseline_event][visit_date]`. |
| `offset` | A number (integer or decimal) to add. Use a negative number to subtract (go back in time). |
| `unit` | A quoted string specifying the unit: `'y'` (years), `'M'` (months), `'d'` (days), `'h'` (hours), `'m'` (minutes), `'s'` (seconds). Units are case-sensitive (`'M'` is months, `'m'` is minutes); any other value gives a blank result. |

> **Year and month lengths:** `'y'` uses 365.2425 days per year. `'M'` uses 30.44 days per month. For precise day-count calculations, use `'d'` instead.

If the source field holds a missing data code instead of a date, the result is blank.

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

The literals `'today'` and `'now'` (in single quotes) can be used as the source parameter. They use the **server time**, not the user's local device time:

```
@CALCDATE('today', 14, 'd')
```

This calculates a date 14 days from the current server date. Be aware that if users are in a different timezone from the server, the date may differ from their local today.

## 4.5 Using an if() Expression as the Source

The source can be a logical expression that resolves to a date value:

```
@CALCDATE(if([use_alt_date]='1', [alt_date], [primary_date]), 30, 'd')
```

---

> **Critical — version caveat (below 15.0.18 Standard): displayed value could disagree with stored value.** A date or datetime field using `@CALCDATE` could produce a value **off by several hours**, and — the part that makes this dangerous — the form or survey **displayed the incorrect value while the stored value differed**. A discrepancy between what a user sees and what is saved undermines trust in every calculated field on the instrument, and would not be caught by reviewing the screen. Fixed in 15.0.18. If `@CALCDATE` values were captured on an earlier version and precision matters, verify the stored data rather than the display.

---

# 5. Comparison: @CALCTEXT / @CALCDATE vs. Built-in Calculated Field

| Feature | Built-in Calculated Field | @CALCTEXT / @CALCDATE |
|---|---|---|
| Output type | Numeric only | Text or date/datetime |
| Conditional logic | Supported via `if()` (numeric results only) | Supported via `if()` |
| Real-time update | Yes | Yes |
| Recalculated when input fields are imported | Yes | Yes |
| Data Quality rule H finds stale values and fixes them on **Fix calcs now** | Yes | Yes |
| Field type required | Calculated Field | Text Box |
| Editable by users | No | No |

Use the built-in Calculated Field when you need a numeric result. Use `@CALCTEXT` or `@CALCDATE` when you need text output, conditional text, or date arithmetic.

---

# 6. Common Questions

**Q: Can @CALCTEXT output a blank value?**

**A:** Yes. Use an empty string as the return value: `@CALCTEXT(if([field]='1', 'Yes', ''))`. The field will display blank when the false condition is met.

**Q: When does @CALCDATE update its value?**

**A:** The same contexts as a built-in calculated field (this applies equally to `@CALCTEXT`):

- **During data entry** — in real time on the form or survey.
- **On save** — REDCap recalculates these fields on the server, including dependent `@CALCTEXT`/`@CALCDATE` fields on other instruments and events of the record.
- **On import** (Data Import Tool or API) — when an input field is imported, the calculated field is recalculated, unless the project's option to turn off auto-calculations is enabled. Values imported directly into the calculated field itself are ignored, with a warning.
- **Data Quality rule H** — lists out-of-date calculated values and updates them when you click **Fix calcs now**.

**Q: Can I use @CALCTEXT on a field with validation (e.g., integer validation)?**

**A:** The tag works on Text Box fields regardless of validation, but REDCap does not enforce the field's validation on `@CALCTEXT` output — a value that doesn't fit the validation is still saved. Leave validation off unless you are certain the output will always conform. On a date or datetime-validated field, the output is cut to the length of the date format, so return a properly formatted date or use `@CALCDATE` instead.

**Q: How do I display the best available value when data may come from multiple sources?**

**A:** Use nested `if()` inside `@CALCTEXT` to build a priority-ordered fallback chain. The expression checks each source in order and returns the first one that is non-blank:

```
@CALCTEXT(if([source_a]<>'', [source_a], if([source_b]<>'', [source_b], [source_c])))
```

This pattern is useful in operational or administrative projects where a value might be populated automatically from an integrated external system, manually entered by staff if the integration is unavailable, or carried over from a historical field as a last resort. Each `if()` layer checks whether the higher-priority source has a value; if it does, that value is returned and the remaining layers are skipped. You can chain as many layers as needed. Note that if all sources are blank, the outermost false branch (here `[source_c]`) is returned — which may itself be blank. If you need an explicit fallback label for the all-blank case, wrap the outermost false value in a quoted string: `..., if([source_c]<>'', [source_c], 'Not available')))`.

**Q: What is the difference between @CALCDATE and just using a Calculated Field for dates?**

**A:** The built-in Calculated Field type returns a number. Date arithmetic in a Calculated Field returns the number of days between dates, not a formatted date value. `@CALCDATE` returns an actual date string in the format expected by the field's validation, making it directly usable as a displayed date.

---

# 7. Common Mistakes & Gotchas

**Piping a variable inside quotes in @CALCTEXT.** Writing `@CALCTEXT(if([x]='1', 'Hello [name]', ''))` will output the literal text `Hello [name]`, not the value of `[name]`. Use the variable as a standalone return value outside quotes: `@CALCTEXT(if([x]='1', [name], ''))`.

**Using @CALCTEXT or @CALCDATE inside @IF.** This combination is explicitly unsupported and produces unpredictable behavior. Apply calculation tags directly to the field without wrapping them in `@IF`.

**Source or result field missing date validation for @CALCDATE.** Both fields should have date, datetime, or datetime_seconds validation. Without it on the result field, nothing is calculated and the field stays editable; without it on the source, REDCap assumes the source is in YMD format.

**Forgetting that `'now'` and `'today'` use server time.** If your REDCap server is in a different timezone from your users, `@CALCDATE('today', ...)` may produce a date that is one day off. Use `'d'` offsets cautiously when timezone alignment matters.

**Not escaping apostrophes in text output.** If `@CALCTEXT` output contains an apostrophe and you used apostrophes as delimiters, escape it: `'it\'s'` or switch to double quotes: `"it's"`.

**Cross-event source fields in @CALCDATE breaking silently after schema changes.** When `@CALCDATE` references a field from a different event using the `[event_name][field_name]` syntax — for example, `@CALCDATE([baseline_arm_1][enrol_date], 45, 'd')` — the expression depends on two identifiers that are easy to change accidentally: the event's unique name and the field's variable name. If the baseline event is renamed (which regenerates its unique event name) or the source field is renamed, every `@CALCDATE` field referencing it returns blank with no error or warning. This failure mode is especially consequential when multiple downstream fields all chain from the same source (e.g., a randomisation date used to calculate several visit windows). Before moving a project to production, document all cross-event field references in `@CALCDATE` and `@CALCTEXT` expressions. Treat the referenced event names and field names as frozen — equivalent to a primary key — and apply a branching logic audit whenever either is changed.

**`[previous-instance]` accumulator chains are easy to get wrong.** When `@CALCTEXT` fields in a repeating instrument use `[previous-instance]` to build accumulated values (see [RC-PIPE-10 — Smart Variables: Repeating Instruments and Events](RC-PIPE-10_Smart-Variables-Repeating-Instruments-and-Events.md) §7), each instance depends on the one before it. REDCap recalculates dependent fields when a source field is saved, but chains across instances are fragile: after a user edits instance 2 when instances 3–5 already exist, check that the later instances show the expected values. Data Quality rule H can find stale values and fix them with **Fix calcs now**; if your instance has a recalculation external module installed, that is another option.

---

# 8. Related Articles

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-AT-06 — Autofill Action Tags](RC-AT-06_Action-Tags-Autofill.md): `@DEFAULT` and `@SETVALUE` for pre-filling values at page load
- [RC-AT-08 — Action Tags: @IF — Conditional Logic](RC-AT-08_Action-Tags-Conditional-IF.md) — @IF: conditional action tag logic; note that @CALCTEXT and @CALCDATE cannot be nested inside @IF
- [RC-DE-05 — Field Validations](RC-DE-05_Field-Validations.md): date and datetime validations required by @CALCDATE

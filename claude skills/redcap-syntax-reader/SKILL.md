---
name: redcap-syntax-reader
description: >
  Interpret, explain, and differentiate REDCap syntax expressions. Use this skill whenever a user
  pastes or asks about a REDCap expression and wants to know what it does, what type it is, or
  whether it is correct. Covers all four REDCap expression types: branching logic (true/false),
  calculated fields (number), @CALCTEXT (text or number), and @CALCDATE (date). Also trigger on
  questions like "what does this expression mean?", "is this valid REDCap syntax?", "why is my
  calculation blank?", or "what's the difference between a calc field and @CALCTEXT?". If the user
  shares any snippet containing square brackets, operators, or action tag syntax like @CALCTEXT or
  @CALCDATE, use this skill.
---

# REDCap Syntax Reader

This skill helps you interpret and explain REDCap expressions. The goal is always to give the user a clear, plain-language explanation of what an expression does, what it returns, and where it is used — plus any gotchas worth noting.

---

## Step 1: Identify the expression type

Look at the expression and classify it as one of the four types below. The type determines how you explain it.

### The Four Types

| Type | What it returns | Where it is used | How to recognize it |
|---|---|---|---|
| **Logic** | True or false | Branching logic, report filters, survey invitations, alerts, Data Quality rules, inside `if()` conditions | Contains comparison operators (`=`, `<>`, `>`, `>=`, `<`, `<=`) with no surrounding action tag; or boolean functions like `contains()`, `isnumber()` |
| **Calculation** (calc field) | A number | Calculated Field type (`calc` in Data Dictionary) | Pure arithmetic or numeric functions — `+`, `-`, `*`, `/`, `^`, `round()`, `datediff()`, `sum()`, `mean()`, `if()` returning numbers. No `@CALCTEXT` or `@CALCDATE` wrapper. |
| **@CALCTEXT** | Text or a number | Text Box field with `@CALCTEXT` action tag | Starts with `@CALCTEXT(...)` |
| **@CALCDATE** | A date | Text Box field with date/datetime validation and `@CALCDATE` action tag | Starts with `@CALCDATE(...)` |

**When context is ambiguous:** An expression like `[score_a] + [score_b]` could be a calculated field formula or the inside of a `@CALCTEXT`. Ask the user where it appears if it's not obvious, or explain both possibilities.

---

## Step 2: Explain the expression

Walk through the expression in plain language. Cover:

1. **What it does** — in plain words, what will REDCap compute or evaluate?
2. **What it returns** — a number, text, a date, or true/false?
3. **Where it belongs** — what field type or context is this expression valid in?
4. **Any notable gotchas** — common mistakes that apply to this specific expression.

Tailor the depth to the user. A project builder who already knows REDCap doesn't need the basics spelled out; a researcher seeing their first formula needs more context.

---

## Type reference: Logic (true/false)

**What it is:** An expression that evaluates to either true (field shows) or false (field hides, condition not met). This is the core language of branching logic.

**Anatomy:** `[variable] operator value`
- Variable: any field variable, e.g. `[age]`, `[consent_status]`
- Operator: `=`, `<>` (not equal), `>`, `>=`, `<`, `<=`
- Value: a number, a quoted string `'enrolled'`, an empty string `''`, or another variable

**Boolean operators:** `AND` / `OR` join multiple statements. AND requires all to be true; OR requires at least one.

**Functions in logic:** Any Special Function can be used in logic. The return value is then compared — e.g., `datediff([dob], 'today', 'y') >= 18` computes an age in years and then checks if it is 18 or more (returns true/false). Boolean-returning functions like `contains([name], 'taylor')` or `isnumber([age])` can stand alone in logic.

**Where logic is used (and where it isn't):**
Logic expressions are valid in: branching logic (show/hide fields), report filters, survey invitations, alerts and notifications, and Data Quality rules. Logic is also used as the condition inside `if()` functions in calculations.

Logic is **not** used for field-level validation constraints (e.g., enforcing that a number falls within a range, or that a date is in the past). REDCap handles those natively through the field's validation settings in the Online Designer or Data Dictionary. Don't suggest logic syntax as a solution for input validation.

**Key gotchas:**
- Empty (`''`) ≠ zero (`0`). An unanswered field and a field containing the number 0 are different states.
- Text comparisons are case-sensitive: `[status]='Enrolled'` will not match `'enrolled'`.
- Use single quotes in any expression that may be edited in Excel (double quotes are corrupted on CSV export/import).
- AND and OR together require parentheses to control evaluation order. Without them, AND takes precedence — which may not be what was intended.
- REDCap validates syntax, not logic. An impossible condition like `[age]>15 and [age]<10` will save without error but the field will never appear.

---

## Type reference: Calculation (calc field)

**What it is:** A formula entered into a Calculated Field (field type = `calc`). The result is computed automatically and stored. **Must return a number** — if the formula produces text or a date, the field stores blank.

**Anatomy:** Any combination of:
- Variable references: `[variable_name]`
- Arithmetic: `+`, `-`, `*`, `/`, `^` (exponent — requires `([base])^([exponent])` with parentheses around both)
- Numeric functions: `round()`, `sum()`, `mean()`, `datediff()`, `age_at_date()`, `if()` (when both return values are numbers), `sqrt()`, `abs()`, `min()`, `max()`, etc.

**Key gotchas:**
- `[a]+[b]+[c]` returns blank if **any** variable is blank. Use `sum([a],[b],[c])` if partial results are acceptable. But if you want the calculation to remain blank until all fields are filled in, the simpler alternative is to just make the source fields required — REDCap will then enforce complete data entry before the formula has anything to work with.
- `sum()`, `mean()`, etc. silently skip blank values — they don't treat blank as zero.
- Exponentiation: `([height])^(2)` is required, not `[height]^2`.
- Want to output text instead? That requires `@CALCTEXT`, not a calc field.
- Want to output a date? That requires `@CALCDATE`, not a calc field. (A calc field can return the *number* of days between dates via `datediff()`, but not a formatted date.)
- Values update in real time during data entry, during data import, and when Data Quality rule H is run. Changing a formula does **not** automatically update existing records — run rule H after a formula change.

---

## Type reference: @CALCTEXT

**What it is:** An action tag placed on a **Text Box field** that computes a value and writes it into the field automatically. Unlike a calc field, it can return text strings, numbers, or field values. The field is not editable by users.

**Syntax:** `@CALCTEXT(expression)`

The expression can be:
- An `if()` function: `@CALCTEXT(if([sex]='1', 'male', 'female'))`
- A numeric formula: `@CALCTEXT([score_a]+[score_b])`
- A field reference: `@CALCTEXT([preferred_name])`

**Key gotchas:**
- Field variables **cannot** be embedded inside quoted strings. `@CALCTEXT(if([x]='1', 'Hello [name]', ''))` outputs the literal text `Hello [name]`, not the value of `[name]`. Use the variable as a standalone return value: `@CALCTEXT(if([x]='1', [name], ''))`.
- Do **not** nest `@CALCTEXT` inside `@IF`. The two tags operate in different contexts; combining them produces unpredictable results.
- If the output text must match field validation (e.g., an integer field), the computed value must conform. A text result in an integer-validated field will be rejected.
- Updates in the same contexts as a calc field: real-time during data entry, data import, and Data Quality rule H.

---

## Type reference: @CALCDATE

**What it is:** An action tag placed on a **Text Box field with date or datetime validation** that computes a date by adding or subtracting time from a source date. Returns a formatted date string (not a number).

**Syntax:** `@CALCDATE(source, offset, unit)`

| Parameter | What it is |
|---|---|
| `source` | A date/datetime field variable, `today`, `now`, or an `if()` expression returning a date |
| `offset` | A number — positive to go forward in time, negative to go back |
| `unit` | `'y'` (years), `'M'` (months), `'d'` (days), `'h'` (hours), `'m'` (minutes), `'s'` (seconds) |

**Examples:**
- `@CALCDATE([visit_date], 7, 'd')` — 7 days after visit date
- `@CALCDATE([deadline], -30, 'd')` — 30 days before deadline
- `@CALCDATE(today, 14, 'd')` — 14 days from today (server date)
- `@CALCDATE([baseline_event][visit_date], 7, 'd')` — 7 days after a date from a specific longitudinal event

**Key gotchas:**
- Both the **source field** and the **result field** must have date, datetime, or datetime_seconds validation. Without this, `@CALCDATE` will not work correctly.
- **Best practice: source and destination should use the same date format.** If `[visit_date]` is a `date_ymd` field, the result field should also be `date_ymd`. Mixing formats (e.g., `date_ymd` source into a `datetime_ymd` result field) can cause unexpected output or display issues.
- `today` and `now` use **server time**, not the user's local clock. In multi-timezone deployments, this can shift the computed date by one day.
- `'y'` uses 365.2425 days as one year; `'M'` uses 30.44 days as one month. For precise scheduling (e.g., exactly 90 days), use `'d'` instead.
- Do **not** nest `@CALCDATE` inside `@IF`.

---

## Advanced variable reference syntax

These patterns extend the basic `[variable_name]` syntax and appear across all four expression types. Recognise them so you can explain what they reference.

### Longitudinal: cross-event references

In a longitudinal project, a plain `[variable_name]` always refers to the **same event** as the field being evaluated. To reference a field in a **different event**, prepend the unique event name in its own brackets:

```
[unique_event_name][variable_name]
```

The two bracket pairs sit immediately adjacent — no space or operator between them.

| Situation | Syntax | Example |
|---|---|---|
| Field in the same event | `[variable_name]` | `[consent_status]='1'` |
| Field in a different event | `[unique_event_name][variable_name]` | `[baseline_arm_1][consent_status]='1'` |

The unique event name comes from **Project Setup → Define My Events** (the Unique Event Name column). It is auto-generated from the event label and arm number, e.g. `baseline_arm_1`, `followup_4wk_arm_2`.

**Key gotchas:**
- A cross-event field that has never been saved returns `''` (empty string), not `0`. Use `<>''` to test whether it has been filled in at all.
- **Renaming an event silently changes its unique event name.** Any logic referencing the old name will stop working without any error message. Always audit branching logic and calculations after renaming an event.
- If an instrument is designated to events in multiple arms, a reference to `[baseline_arm_1][field]` returns blank for records in Arm 2 — because that arm has no `baseline_arm_1` event.

---

### Repeating instruments and events: instance references

Within a repeating instrument, a plain `[variable_name]` references the **current instance**. To reference a specific instance, append an instance qualifier in its own brackets immediately after the variable name:

```
[variable_name][instance_qualifier]
```

In a longitudinal project, combine event prefix and instance qualifier:

```
[unique_event_name][variable_name][instance_qualifier]
```

**Instance qualifiers:**

| Qualifier | What it references |
|---|---|
| `[1]`, `[2]`, … | A fixed, specific instance number |
| `[current-instance]` | The current instance (same as no qualifier) |
| `[previous-instance]` | The instance immediately before the current one |
| `[next-instance]` | The instance immediately after the current one |
| `[first-instance]` | The first (lowest-numbered) instance |
| `[last-instance]` | The most recently created instance |

**Examples:**
- `[med_name][1]='Aspirin'` — checks whether instance 1's medication name is Aspirin
- `[visit_status][previous-instance]='complete'` — checks if the prior instance was marked complete
- `[baseline_arm_1][phq9_total][last-instance]` — PHQ-9 total from the last instance at baseline

**Key gotchas:**
- `[previous-instance]` returns blank when evaluated in instance 1 (no prior instance exists). Handle this with conditional logic if needed.
- `[last-instance]` is dynamic — it changes as new instances are added. Don't rely on it when a stable, fixed reference is required.
- Instance qualifiers only work in projects that actually use repeating instruments or events. In non-repeating contexts they return blank.

---

## Choosing the right type (quick reference)

When explaining an expression to a user who seems unsure which type to use, offer this guide:

| You want to output... | Use |
|---|---|
| A number (score, BMI, age in years, days since baseline) | Calculated Field |
| Text (a category label, an interpretation, conditional wording) | Text Box + `@CALCTEXT` |
| A mix (text in some conditions, number in others) | Text Box + `@CALCTEXT` |
| A date (follow-up appointment, deadline, time point) | Text Box with date validation + `@CALCDATE` |
| A true/false condition (to show/hide a field, filter records) | Branching logic / logic expression |

---

## Related KB articles

- RC-BL-02 — Branching Logic: Syntax & Atomic Statements
- RC-BL-03 — Branching Logic: Combining Statements
- RC-BL-05 — Branching Logic: Longitudinal Projects (cross-event references)
- RC-CALC-01 — Special Functions Reference
- RC-CALC-02 — Calculated Fields
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE
- RC-AT-08 — Action Tags: @IF
- RC-PIPE-10 — Smart Variables: Repeating Instruments and Events (instance qualifiers)

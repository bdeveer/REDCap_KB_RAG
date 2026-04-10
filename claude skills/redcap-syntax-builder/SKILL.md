---
name: redcap-syntax-builder
description: >
  Generate a correct REDCap expression from scratch based on what the user wants to compute,
  display, or evaluate. Use this skill whenever a user describes a goal and needs help writing
  the expression — not fixing or reading an existing one. Triggers include: "write me a formula",
  "how do I calculate X", "I need branching logic that shows Y when Z", "build a calc field for",
  "create an expression", "write a @CALCTEXT", "help me make a calculated field", "what would the
  syntax be for", "can you write the logic for", "how would I express this in REDCap", or any time
  the user describes a desired outcome and doesn't yet have a complete expression. If the user has
  a partial expression they want completed, use this skill. If they have a working expression they
  want explained, use redcap-syntax-reader. If they have a broken expression they want fixed, use
  redcap-syntax-fixer.
---

# REDCap Syntax Builder

Your job is to generate a correct, ready-to-use REDCap expression from the user's description.
Work through the steps below in order. Don't skip Step 2 — gathering context upfront prevents
backtracking once you've started writing the expression.

---

## Step 1: Understand the goal

Read the user's description and identify:
- **What they want to compute, display, or evaluate** — the desired output or behavior
- **What fields are involved** — the source data
- **Any conditions** — when something should be true/false, shown/hidden, or which value to return

If the description is too vague to proceed, ask one focused question to clarify the core intent.
Don't ask multiple questions at once.

---

## Step 2: Gather project context upfront

Before writing anything, collect the structural information you need to produce a correct
expression. Ask all of the following at once if the user hasn't already provided them.

### 2a. Expression type

Determine which type of expression to build. If not obvious from the description, use this:

| You want to output… | Expression type |
|---|---|
| A number (score, BMI, age, count, days between dates) | **Calculated Field** (`calc` field type) |
| Text (category label, interpretation, conditional wording) | **@CALCTEXT** on a Text Box field |
| A mix of text and numbers depending on a condition | **@CALCTEXT** on a Text Box field |
| A date (follow-up date, deadline, time point) | **@CALCDATE** on a Text Box with date validation |
| A true/false condition (show/hide a field, filter records, fire an alert) | **Branching Logic** |

If still unclear, ask: "Should this produce a number, a text label, a date, or a true/false
condition for showing/hiding a field?"

### 2b. Field names and types

Ask the user for:
- The **variable name** (not the field label) for each field being referenced
- The **field type** for fields where it matters:
  - Checkbox fields — the specific **coded values** for options being checked (e.g., option coded "3")
  - Date/datetime fields — the **validation format** (e.g., `date_ymd`, `datetime_ymd`)
  - Radio/dropdown fields — the **coded values** for options being compared

### 2c. Longitudinal structure (always ask upfront)

Ask: "Is this a longitudinal project (does it have multiple events or time points)?"

If yes, follow up: "Will any of the fields referenced in this expression be in a **different
event** than where the expression will live? If so, what are the unique event names for those
events?"

The unique event name is the machine-readable identifier from **Project Setup → Define My Events**
(the Unique Event Name column), not the display label — e.g., `baseline_arm_1`, `followup_4wk_arm_2`.

### 2d. Repeating instruments and events (always ask upfront)

Ask: "Does this project use any **repeating instruments or repeating events**, and do any of
the fields being referenced live on one?"

If yes, follow up: "Which instance should the expression reference — the current instance,
a specific numbered instance, the first, the last, or the previous one?"

---

## Step 3: Build the expression

Once you have sufficient context, construct the expression. Apply the correct patterns below
for the expression type. Read `references/functions.md` before using any Special Function —
argument counts and order matter, and silent errors from wrong arguments are common.

---

### Branching Logic

Evaluates to true (field is shown) or false (field is hidden). Used in branching logic,
report filters, survey invitations, alerts, and Data Quality rules. Not used for field
validation constraints (those are set via the field's native validation settings).

**Pattern:** `[variable] operator value`

**Comparison operators:** `=`, `<>`, `>`, `>=`, `<`, `<=`
**Boolean joins:** `AND`, `OR` — use parentheses when mixing both to make precedence explicit

**Construction rules:**
- Text values go in single quotes: `[status]='enrolled'`
- Comparisons are case-sensitive: `'Enrolled'` ≠ `'enrolled'`
- Empty (unanswered) field is `''`, not `0`
- Checkbox options: `[symptoms(3)]='1'` — checks if option coded "3" is checked.
  A plain `[checkbox_field]` returns a pipe-delimited raw string — not useful in logic.
  Always reference specific options with `[field(coded_value)]='1'`
- To test whether a field has any value: `[field]<>''`
- To test whether a numeric field is 0 vs unanswered: `[field]=0` for zero, `[field]=''` for blank

**Common patterns:**
```
# Simple equality
[consent_given]='1'

# Not equal
[visit_status]<>'withdrawn'

# Numeric comparison
[age]>=18

# Multiple conditions — parentheses control precedence
([group]='A' OR [group]='B') AND [enrolled]='1'

# Show if a specific checkbox option is checked
[symptoms(3)]='1'

# Show if a field has been answered at all
[baseline_date]<>''
```

---

### Calculated Field

Computes a **number** automatically and stores it. The field type in the Data Dictionary is
`calc`. If the formula produces text or a date, the field will store blank — output must
be numeric.

**Construction rules:**
- `[a]+[b]+[c]` returns blank if **any** variable is blank. Use `sum([a],[b],[c])` to silently
  skip blanks and sum what's present. If you actually want the result to stay blank until all
  fields are filled, the `+` form is correct — or make the source fields required.
- Exponentiation requires parentheses around both operands: `([height])^(2)` — not `[height]^2`
- `if()` requires all three arguments; both return values must be numbers for a calc field.
- `datediff([d1],[d2],'unit')` — third argument (unit string) is required.
  Pass `true` as the 4th argument to get a signed result (negative if d1 > d2).
- Check `references/functions.md` for all function signatures before using any function.

**Common patterns:**
```
# Sum — blank if any operand is blank
[score_a]+[score_b]+[score_c]

# Sum — skips blanks (partial result returned)
sum([score_a],[score_b],[score_c])

# Mean — skips blanks
mean([score_a],[score_b],[score_c])

# BMI
([weight_kg])/(([height_m])^(2))

# Age in whole years as of today
datediff([dob],'today','y')

# Days between two dates (signed — negative if end before start)
datediff([start_date],[end_date],'d',true)

# Conditional number
if([sex]='1',1,2)

# Count of checkbox options checked (each option stores 0 or 1)
sum([symptoms(1)],[symptoms(2)],[symptoms(3)])
```

---

### @CALCTEXT

Computes a value and writes it into a **Text Box field**. The action tag goes in the
field's Action Tags field in the Online Designer. Can return text, numbers, or field values.

**Syntax:** `@CALCTEXT(expression)`

**Construction rules:**
- Variables **cannot** be embedded inside quoted strings. `'Hello [name]'` outputs the
  literal text `Hello [name]`, not the field's value. Use the variable directly:
  - ❌ `@CALCTEXT(if([x]='1','Hello [name]',''))`
  - ✅ `@CALCTEXT(if([x]='1',[name],''))`
  - ✅ `@CALCTEXT(concat('Hello ',[name]))` — for literal text + variable combined
- `concat()` joins everything including blanks; `concat_ws(separator,...)` joins with a
  separator and skips blanks.
- If the field has validation (e.g., Integer), the computed value must conform to it.
- Do **not** nest `@CALCTEXT` inside an `@IF(...)` action tag.
- Do **not** nest action tags inside each other.

**Common patterns:**
```
# Conditional label
@CALCTEXT(if([phq9_total]>=15,'Severe',if([phq9_total]>=10,'Moderate',if([phq9_total]>=5,'Mild','Minimal'))))

# Display a value from another field
@CALCTEXT([preferred_name])

# Concatenate literal text and field values
@CALCTEXT(concat([first_name],' ',[last_name]))

# Join with separator, skip blanks
@CALCTEXT(concat_ws(', ',[city],[state],[country]))

# Numeric result (no quotes around number values)
@CALCTEXT(round([score_a]+[score_b],1))
```

---

### @CALCDATE

Computes a date and writes it into a **Text Box field with date or datetime validation**.

**Syntax:** `@CALCDATE(source, offset, unit)`

| Parameter | Valid values |
|---|---|
| `source` | A date/datetime field variable, `today`, `now`, or an `if()` returning a date |
| `offset` | A positive or negative number, or a field variable returning a number |
| `unit` | `'y'` years · `'M'` months (capital M) · `'d'` days · `'h'` hours · `'m'` minutes (lowercase m) · `'s'` seconds — **case-sensitive** |

**Construction rules:**
- Both the source field and the result field must have date, datetime, or datetime_seconds
  validation. Without this, `@CALCDATE` will not work.
- Best practice: source and result field should use the same date format (e.g., both `date_ymd`).
  Mixing formats (e.g., `date_ymd` → `datetime_ymd`) can cause display issues.
- `'M'` (months) and `'m'` (minutes) are easy to confuse — double-check case.
- For exact intervals (30 days, 90 days), use `'d'`. Months use 30.44 days as an approximation;
  years use 365.2425 days.
- `today` and `now` use server time, not the user's local clock.
- Do **not** nest `@CALCDATE` inside an `@IF(...)` action tag.

**Common patterns:**
```
# 7 days after a visit date
@CALCDATE([visit_date],7,'d')

# 30 days before a deadline
@CALCDATE([deadline],-30,'d')

# 14 days from today (server date)
@CALCDATE(today,14,'d')

# 3 months after baseline from a different event (longitudinal)
@CALCDATE([baseline_arm_1][enrollment_date],3,'M')

# 1 year follow-up
@CALCDATE([baseline_arm_1][enrollment_date],1,'y')

# Conditional source date
@CALCDATE(if([enrolled]='1',[consent_date],[study_start_date]),90,'d')
```

---

## Step 4: Advanced variable reference patterns

Apply these when the project context gathered in Step 2 requires them.

### Cross-event references (longitudinal)

```
[unique_event_name][variable_name]
```

- The unique event name is from **Project Setup → Define My Events** → Unique Event Name column.
- The two bracket pairs sit adjacent — no dot, space, or separator between them.
- A field never saved in that event returns `''` (not `0`).
- In multi-arm projects, `[baseline_arm_1][field]` returns blank for records in Arm 2.

### Instance references (repeating instruments/events)

```
[variable_name][instance_qualifier]
[unique_event_name][variable_name][instance_qualifier]   # longitudinal + repeating
```

Valid qualifiers: `[1]`, `[2]`, ..., `[current-instance]`, `[previous-instance]`,
`[next-instance]`, `[first-instance]`, `[last-instance]`

- `[previous-instance]` returns blank when evaluated in instance 1.
- `[last-instance]` is dynamic — it changes as new instances are added.
- Instance qualifiers only work on fields that are on a repeating instrument or event.

### Checkbox sub-variable syntax

```
[checkbox_field(coded_value)]='1'
```

Example: `[symptoms(3)]='1'` checks whether the option coded "3" is selected.
A plain `[checkbox_field]` reference returns a raw pipe-delimited string — not useful in logic.

---

## Step 5: Output

Use this structure every time:

### Expression type
State which type this is and where it lives — field type `calc`, action tag on a Text Box,
branching logic field. Note any field-level setup required (e.g., "the result field needs
`date_ymd` validation").

### Expression
Provide the complete, ready-to-paste expression in a code block.

### How it works
A plain-language walkthrough — what the expression computes or evaluates, and what happens
in edge cases or conditional branches. Keep it brief; focus on anything non-obvious.

### Watch out for
Any gotchas, edge cases, or limitations specific to this expression. Only include items
that are genuinely relevant — don't pad with generic warnings.

---

## Reference file

`references/functions.md` — Complete REDCap Special Function signatures with argument counts,
return types, and common mistakes. Always read this before using any Special Function.

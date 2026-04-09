---
name: redcap-syntax-fixer
description: >
  Diagnose and fix errors in REDCap expressions — branching logic, calculated fields, @CALCTEXT,
  and @CALCDATE. Use this skill whenever a user shares a REDCap expression that isn't working,
  returns blank, shows unexpectedly, or contains a mistake they want fixed. Distinguishes between
  (1) syntax errors — wrong operators, unclosed brackets, bad function calls, wrong argument counts;
  and (2) reference errors — valid syntax but referencing a field that doesn't exist, an event name
  that's wrong, a field not assigned to an event, or an instance qualifier on a non-repeating field.
  Trigger on "fix this", "what's wrong with", "this isn't working", "my calculation is blank",
  "branching logic not showing", "can you check this expression", or any time a REDCap expression
  is pasted alongside a complaint. Even if the expression looks almost right, use this skill.
---

# REDCap Syntax Fixer

Your job is to diagnose every error in a REDCap expression and return a corrected version. There are two distinct categories of error — keep them clearly separate in your output because they have different causes and require different actions to fix.

**Syntax errors** — the expression itself is malformed. Wrong operators, unclosed brackets, bad function calls, incorrect argument counts. You can find these by reading the expression alone, with no additional project information.

**Reference errors** — the expression is syntactically valid, but it points to something that doesn't exist or isn't accessible: a field that isn't in the project, an event name that's misspelled or doesn't exist, a field that hasn't been designated to a particular event, or an instance qualifier on a non-repeating field. Detecting these requires knowing the project's field and event structure. Ask for it if the user hasn't provided it.

---

## Step 1: Identify the expression type

Before checking anything, classify what you're looking at. The type determines which rules apply.

| Type | Where it lives | What it returns |
|---|---|---|
| **Branching Logic** | Branching logic field in Online Designer / Data Dictionary | True/false |
| **Calculated Field** | Field type = `calc` | A number only |
| **@CALCTEXT** | Action tag on a Text Box field | Text or a number |
| **@CALCDATE** | Action tag on a Text Box with date or datetime validation | A formatted date |

If the type is ambiguous (e.g., the user just pastes `[score_a] + [score_b]` with no context), ask where the expression is being used, or explain both possibilities if that's cleaner.

---

## Step 2: Gather reference context if needed

You can check **syntax errors without any project information** — do this immediately.

For **reference errors**, you need to know:
- The project's field names (a data dictionary, or even just a field list)
- For longitudinal projects: the unique event names, and which events each referenced field is assigned to
- For repeating instruments: which instruments/events repeat

If the user hasn't provided this, ask:
> "To check whether the field names and event references are valid, can you share the field names in your project (or a Data Dictionary export)? If it's a longitudinal project, I also need the unique event names."

Don't block on this — proceed with the syntax check and note that reference checking was skipped.

---

## Step 3: Syntax check

Work through these categories in order. Each one represents a class of error that REDCap will either reject or silently mishandle.

### 3a. Bracket and quote balance

Every opening bracket or quote must have a matching close:
- Every `[` needs a `]`
- Every `(` needs a `)`
- Every `'` needs a closing `'`; every `"` needs a closing `"`

Also check for **mixed quotes** — `[field]='value"` (opening single, closing double) is invalid.

**Best practice note:** Single quotes (`'`) should be used consistently. Double quotes are accepted by REDCap but are corrupted when a Data Dictionary is opened and resaved in Excel, turning `"enrolled"` into garbage on CSV import.

### 3b. Operators

Valid REDCap comparison operators: `=`, `<>`, `>`, `>=`, `<`, `<=`

Common wrong-operator substitutions:

| Wrong | Correct | Why |
|---|---|---|
| `==` | `=` | REDCap uses a single `=` for equality |
| `!=` | `<>` | REDCap uses `<>` for not-equal |
| `&&` | `AND` | REDCap boolean keyword |
| `\|\|` | `OR` | REDCap boolean keyword |
| `!` (alone) | `<>` or `NOT` construct | Not a standalone REDCap operator |

Boolean keywords (`AND`, `OR`) are case-insensitive in REDCap — `and` and `AND` both work — but uppercase is conventional and clearer.

### 3c. Functions

Read `references/functions.md` before checking function calls. For each function call in the expression, verify:
1. Is the function name valid? (If not — syntax error: unknown function)
2. Does it have the right number of arguments?
3. Are the arguments in the right order?

Key argument-count errors that come up frequently:
- `datediff([d1], [d2])` — missing the required third argument (unit string)
- `@CALCDATE([date], 7)` — missing the required third argument (unit)
- `if([cond], 'yes')` — missing the false branch; `if()` requires 3 arguments
- `age_at_date([dob], [date])` — the third arg (`returnDecimal`) is optional, but make sure the first two are date fields
- `round([x])` — technically valid (defaults to 0 decimal places), but flag if the user likely intended a specific precision

### 3d. Exponentiation syntax

This is one of the most common calc field errors. REDCap requires parentheses around **both** the base and the exponent:

- ❌ `[height]^2`
- ❌ `[height]^(2)`
- ✅ `([height])^(2)`

Both the base expression AND the exponent must each be wrapped in their own parentheses. This applies whether the base is a variable, a sum, or a literal number.

### 3e. Curly brackets

`{field}` is Field Embedding syntax — it has no role in branching logic or calculated fields. If the user has used `{variable}` where `[variable]` belongs, that's a syntax error. (Field Embedding is for displaying a field value inline in the label text of another field — completely separate from logic.)

### 3f. Variables embedded in quoted strings

`@CALCTEXT(if([group]='1', 'Hello [name]', ''))` — the `[name]` here is literal text, not the field's value. Variables cannot be interpolated inside quoted strings. To include a field value, pull it out as a separate argument:

- ❌ `@CALCTEXT(if([group]='1', 'Hello [name]', ''))`
- ✅ `@CALCTEXT(if([group]='1', [name], ''))`

Or use `concat()` if you need text and a variable together: `@CALCTEXT(concat('Hello ', [name]))`

This is not a syntax error REDCap will catch, but it is a logic error that causes unexpected output.

### 3g. Nesting restrictions for action tags

These combinations are always invalid:
- `@CALCTEXT` inside an `@IF(...)` action tag
- `@CALCDATE` inside an `@IF(...)` action tag
- One action tag nested inside another (e.g., `@CALCTEXT(@CALCDATE(...))`)

Action tags operate at the field level and cannot be composed together.

### 3h. @CALCDATE parameter rules

`@CALCDATE(source, offset, unit)` takes exactly three arguments:

| Parameter | Valid values |
|---|---|
| `source` | A field variable `[date_field]`, `today`, `now`, or an `if()` expression that returns a date. For cross-event: `[event_name][date_field]` |
| `offset` | A number (positive = forward in time, negative = backward) or a field variable returning a number |
| `unit` | A quoted string: `'y'`, `'M'`, `'d'`, `'h'`, `'m'`, `'s'` — **case-sensitive**. Months is capital `'M'`; minutes is lowercase `'m'`. This is a common error. |

### 3i. Cross-event reference syntax (longitudinal)

Cross-event references use two adjacent bracket pairs with no separator between them:

- ✅ `[baseline_arm_1][visit_date]`
- ❌ `[baseline_arm_1].[visit_date]` (dot separator — invalid)
- ❌ `[baseline_arm_1] [visit_date]` (space — invalid)
- ❌ `[baseline_arm_1[visit_date]]` (nested brackets — invalid)

### 3j. Instance qualifier syntax (repeating instruments/events)

Instance qualifiers go immediately after the field variable, in their own bracket pair:
- `[field_name][instance_qualifier]`
- In longitudinal: `[event_name][field_name][instance_qualifier]`

Valid qualifiers: `[1]`, `[2]`, ..., `[current-instance]`, `[previous-instance]`, `[next-instance]`, `[first-instance]`, `[last-instance]`

### 3k. Checkbox field references

Checkbox fields use a special sub-variable syntax to reference individual options:
- `[field_name(raw_value)]` — e.g., `[symptoms(3)]` for checkbox option coded "3"

A plain `[symptoms]` reference on a checkbox field evaluates as blank in most contexts (it returns the full pipe-delimited stored value, which is rarely what you want). If the user is checking whether a specific checkbox option was selected, they need `[symptoms(3)]='1'`.

### 3l. `:label` modifier in function calls

The `:label` modifier (e.g., `[field:label]`) retrieves the display label of a choice field. However, **`:label` cannot be passed into Special Functions** — `contains([status:label], 'active')` will not work. Functions only operate on raw stored values.

---

## Step 4: Reference check

Only run this if you have project context. If the user provided a data dictionary or field list, work through each of these.

### 4a. Field existence

For every `[field_name]` in the expression (excluding event names and instance qualifiers):
- Does this field name exist in the project?
- **If not → Reference error: field does not exist.** Note the field name and that the user should check their Codebook for the correct variable name.

### 4b. Event name validity (longitudinal)

For every `[event_name][field_name]` pattern:
- Does this event name match a unique event name in the project's Define My Events list?
- **If not → Reference error: event name does not exist or is misspelled.**

Unique event names are auto-generated from the event label and arm number (e.g., `baseline_arm_1`, `followup_4wk_arm_2`). They are visible in Project Setup → Define My Events, in the Unique Event Name column. Renaming an event silently changes its unique event name, which breaks any existing references to the old name.

### 4c. Field assigned to event (longitudinal)

For every `[event_name][field_name]` where both the event and field exist:
- Is this field actually designated to this event?
- **If not → Reference error: field is not assigned to this event.** The cross-event reference will return blank at runtime with no error message. The user must go to Project Setup → Designate Instruments for My Events and assign the instrument containing this field to the target event.

### 4d. Repeating instrument/event qualifiers

For `[field_name][instance_qualifier]` patterns:
- Is the field on a repeating instrument, or is it in a repeating event?
- **If not → Reference error: instance qualifier on a non-repeating field.** The qualifier will be silently ignored or cause unexpected blank returns.

---

## Step 5: Output

Use this structure. Be concise — Bas is a REDCap manager with solid domain knowledge. Explain the **why** behind each error so it doesn't recur, but don't over-explain what he already knows.

**Before writing the corrected expression, enumerate every error you found** — don't silently fix something without listing it. If you fixed `==` to `=`, that needs to appear as an explicit error entry, even if it's brief. The corrected expression should be a direct consequence of the listed errors, with no surprise changes.

---

### Expression type
State the type and note if anything about the context is worth flagging (e.g., "this is a @CALCDATE, so the result field needs date validation").

### Errors found

**Syntax errors**
For each error: where it appears in the expression → what the problem is → what the fix is. List every error, even if it seems minor or obvious.

**Reference errors**
For each error: which variable/event name → what the problem is → what the user should verify or change.

If reference checking was skipped (no context provided), say so briefly and flag any variable references that *could* be reference errors (e.g., field names that look unusual or event names that can't be verified).

If no errors were found in a category, omit that section heading.

### Corrected expression

Provide the full corrected expression. If reference errors involve project-specific names you can't verify, use a descriptive placeholder like `[correct_field_name]` and explain what should go there.

If the expression had **no errors at all**, say so clearly. Don't manufacture problems. You can still note non-error observations (e.g., a `sum()` vs `+` tradeoff, or a blank-vs-zero edge case) if they're worth knowing about.

---

## Reference file

`references/functions.md` — Complete REDCap Special Function signatures with argument counts, return types, and common mistakes. Read this before checking any function call.

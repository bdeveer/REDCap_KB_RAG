# Write Mode — Build an Expression From a Goal

Generate a correct, ready-to-use REDCap expression from the user's description (or complete a
partial one). Work through the steps in order. Don't skip Step 2 — gathering context upfront
prevents backtracking once you've started writing.

Rules referenced here (operators, quoting, blank handling, checkbox / cross-event / instance syntax,
@CALCDATE parameters) are in `syntax-core.md`. Function signatures are in `functions.md` — read it
before using any Special Function.

---

## Step 1: Understand the goal

Identify:
- **What they want to compute, display, or evaluate** — the desired output or behavior
- **What fields are involved** — the source data
- **Any conditions** — when something should be true/false, shown/hidden, or which value to return

If the description is too vague to proceed, ask one focused question about the core intent. Don't
ask multiple questions at once at this stage.

---

## Step 2: Gather project context upfront

Collect what you need before writing. Ask all of the following at once if the user hasn't already
provided them. (If the user named a connector and project, you may instead look these up — see
"Optional: live-project validation" in `SKILL.md`.)

### 2a. Expression type

Use the "Choosing the right type" table in `syntax-core.md` §1. If still unclear, ask: "Should this
produce a number, a text label, a date, or a true/false condition for showing/hiding a field?"

### 2b. Field names and types

Ask for:
- The **variable name** (not the field label) for each field being referenced
- The **field type** where it matters:
  - Checkbox fields — the **coded values** of the options being tested (e.g., option coded "3")
  - Date/datetime fields — the **validation format** (e.g., `date_ymd`, `datetime_ymd`)
  - Radio/dropdown fields — the **coded values** being compared

### 2c. Longitudinal structure (always ask)

"Is this a longitudinal project (does it have multiple events or time points)?"

If yes: "Will any referenced fields be in a **different event** than where the expression will live?
If so, what are the unique event names for those events?" (Unique event name from Project Setup →
Define My Events, e.g., `baseline_arm_1` — not the display label.) If the user wants "the previous
visit" or "the first visit" rather than a fixed event, consider an event smart-variable prefix
(`syntax-core.md` §8).

### 2d. Repeating instruments and events (always ask)

"Does this project use any **repeating instruments or repeating events**, and do any referenced
fields live on one?"

If yes: "Which instance should the expression reference — the current instance, a specific
numbered instance, the first, the last, or the previous one?"

---

## Step 3: Build the expression

Apply the rules in `syntax-core.md` for the chosen type, then the patterns below.

### Branching Logic

Pattern: `[variable] operator value`. Text values in single quotes; blank is `''`; checkbox options
via `[field(code)]='1'`; parentheses whenever AND and OR are mixed.

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

# Show only at the Baseline event (event smart variable)
[event-label]='Baseline'
```

### Calculated Field

Output must be numeric. Choose the blank behavior deliberately (`syntax-core.md` §4).

```
# Sum — blanks count as 0 (always returns a number)
[score_a]+[score_b]+[score_c]

# Sum — skips blanks; blank only if all are blank
sum([score_a],[score_b],[score_c])

# Sum — stays blank until every item is answered
if(isblankormissingcode([score_a]) or isblankormissingcode([score_b]) or isblankormissingcode([score_c]), "", [score_a]+[score_b]+[score_c])

# Mean — skips blanks
mean([score_a],[score_b],[score_c])

# BMI
([weight_kg])/(([height_m])^(2))

# Age in whole years as of today (calendar-accurate; datediff 'y' is a 365.2425-day approximation)
# Pass the 3rd argument explicitly on 17.0.6–17.1.1, where omitting it fails silently (RC-CALC-01 §5.2)
age_at_date([dob],'today',false)

# Days between two dates (signed — negative if end before start)
datediff([start_date],[end_date],'d',true)

# Conditional number
if([sex]='1',1,2)

# Count of checkbox options checked (each option stores 0 or 1)
sum([symptoms(1)],[symptoms(2)],[symptoms(3)])
```

### @CALCTEXT

Variables never inside quoted strings; escape apostrophes (`\'`) or use double quotes; smart
variables can be returned directly.

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

# Text containing an apostrophe
@CALCTEXT(if([role]='4','The participant\'s guardian',''))

# Return a smart variable
@CALCTEXT(if([age]>=18,[dob],[event-label]))

# Value from the previous event where this field's instrument is designated
@CALCTEXT([previous-event-name][weight])
```

### @CALCDATE

Three arguments; `'M'` months vs `'m'` minutes; both fields need date validation.

```
# 7 days after a visit date
@CALCDATE([visit_date],7,'d')

# 30 days before a deadline
@CALCDATE([deadline],-30,'d')

# 14 days from today (server date)
@CALCDATE('today',14,'d')

# 3 months after baseline from a different event (longitudinal)
@CALCDATE([baseline_arm_1][enrollment_date],3,'M')

# 1 year follow-up
@CALCDATE([baseline_arm_1][enrollment_date],1,'y')

# Conditional source date
@CALCDATE(if([enrolled]='1',[consent_date],[study_start_date]),90,'d')
```

### Advanced references

Apply cross-event (`syntax-core.md` §6), instance-qualifier (§7), and smart-variable (§8) syntax as
the Step 2 answers require.

---

## Step 4 (optional): Validate against the live project

If the user named a connector and project, confirm the connector (flag production), then use only
the read-only metadata tools listed in `SKILL.md` to confirm every field name, checkbox code, event
name, designation, and repeat setting used in the expression. Report anything that didn't match.

---

## Step 5: Output

Use this structure every time:

### Expression type
State which type this is and where it lives — field type `calc`, action tag on a Text Box,
branching logic field. Note any field-level setup required (e.g., "the result field needs
`date_ymd` validation").

### Expression
The complete, ready-to-paste expression in a code block.

### How it works
A brief plain-language walkthrough — what it computes or evaluates and what happens in edge cases
or conditional branches. Focus on anything non-obvious.

### Watch out for
Gotchas, edge cases, or limitations specific to this expression. Only items that are genuinely
relevant — don't pad with generic warnings. If live validation was run, say what was confirmed.

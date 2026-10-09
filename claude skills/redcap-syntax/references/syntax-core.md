# REDCap Syntax — Core Reference

Shared rules for all three modes (write, fix, explain). Special Function signatures live in
`functions.md`; this file covers everything else.

---

## 1. Expression types

| Type | Where it lives | What it returns | How to recognise it |
|---|---|---|---|
| **Branching Logic** (logic) | Branching logic field in Online Designer / Data Dictionary; also report filters, survey invitations, alerts, Data Quality rules, and the condition inside `if()` | True/false | Comparison operators (`=`, `<>`, `>`, `>=`, `<`, `<=`) with no action-tag wrapper; or boolean functions like `contains()`, `isnumber()` standing alone |
| **Calculated Field** | Field type = `calc` | A number only | Arithmetic or numeric functions — `+`, `-`, `*`, `/`, `^`, `round()`, `datediff()`, `sum()`, `mean()`, `if()` returning numbers. No action-tag wrapper |
| **@CALCTEXT** | Action tag on a Text Box field | Text or a number | Starts with `@CALCTEXT(...)` |
| **@CALCDATE** | Action tag on a Text Box with date, datetime, or datetime_seconds validation | A formatted date | Starts with `@CALCDATE(...)` |

**Ambiguous context:** `[score_a] + [score_b]` could be a calc formula or the inside of a
`@CALCTEXT`. Ask where it lives, or explain both.

### Choosing the right type

| You want to output… | Use |
|---|---|
| A number (score, BMI, age, count, days between dates) | **Calculated Field** (`calc`) |
| Text (category label, interpretation, conditional wording) | **@CALCTEXT** on a Text Box |
| A mix of text and numbers depending on a condition | **@CALCTEXT** on a Text Box |
| A date (follow-up date, deadline, time point) | **@CALCDATE** on a Text Box with date validation |
| A true/false condition (show/hide a field, filter records, fire an alert) | **Branching Logic** |

Logic is **not** used for field-level validation constraints (range checks, "date must be in the
past") — REDCap handles those natively through the field's validation settings.

REDCap validates syntax, not logic: an impossible condition like `[age]>15 and [age]<10` saves
without error, but the field never appears (RC-BL-03).

---

## 2. Operators

**Comparison:** `=`, `<>`, `>`, `>=`, `<`, `<=`
**Boolean:** `AND`, `OR` — case-insensitive (`and` works); uppercase is conventional.
**Arithmetic:** `+`, `-`, `*`, `/`, `^`

**Precedence:** AND binds before OR (RC-BL-03). `[a]='1' OR [b]='1' AND [c]='1'` means
`[a]='1' OR ([b]='1' AND [c]='1')`. Whenever AND and OR are mixed, add explicit parentheses.

**No NOT keyword and no `!`** (RC-BL-03). Express negation with `<>`, or for a checkbox option with
`[field(code)]='0'`.

| Wrong (other languages) | Correct | Why |
|---|---|---|
| `==` | `=` | REDCap uses a single `=` for equality |
| `!=` | `<>` | REDCap uses `<>` for not-equal |
| `&&` | `AND` | REDCap boolean keyword |
| `\|\|` | `OR` | REDCap boolean keyword |
| `!` / `NOT` | `<>` (or `[cb(code)]='0'`) | REDCap has no `!` and no standalone `NOT` keyword |

**Exponentiation** needs parentheses around **both** base and exponent:
`([height])^(2)` — not `[height]^2`, not `[height]^(2)`. This applies whether the base is a
variable, a sum, or a literal.

---

## 3. Quoting rules

- Text values go in quotes: `[status]='enrolled'`. Single and double quotes are both accepted
  (RC-BL-02).
- **Prefer single quotes.** Excel corrupts double quotes when a Data Dictionary CSV is edited and
  resaved, breaking logic on import (RC-BL-02, RC-CALC-02).
- Mixed delimiters (`[field]='value"`) are invalid — every opening quote needs a matching close.
- Numbers may be quoted or unquoted — `[age]=18` and `[age]='18'` both work (RC-BL-02).
- Text comparisons are **case-sensitive**: `'Enrolled'` does not match `'enrolled'`.
- Blank (unanswered) is `''`.
- `'today'` and `'now'` are quoted strings when used as a date argument (e.g., in `@CALCDATE`,
  `datediff`, `age_at_date`). They use server time.
- **Variables and smart variables are not interpolated inside quotes.** `'Hello [name]'` outputs the
  literal text `Hello [name]`. Use the variable as its own argument, or `concat('Hello ',[name])`
  (RC-AT-09 §3.3).
- **Apostrophes in @CALCTEXT text output** (RC-AT-09 §3.4): if the text contains `'` and the
  delimiter is also `'`, escape it with a backslash — `'The user\'s guide'` — or use double quotes
  as the delimiter — `"The user's guide"`. (Double quotes carry the Excel caveat above.)
- `{field}` is Field Embedding syntax — it has no role in logic or calculations. Use `[field]`.
- The `:label` modifier (`[field:label]`) cannot be passed into Special Functions —
  `contains([status:label],'active')` will not work; functions operate on raw stored values.
- **Inline comments:** text from `//` or `#` to the end of a line is ignored (RC-BL-02 §3.6).
  Keep apostrophes and quotes out of comments, and don't let a comment be the whole of the logic —
  both have a long defect history. Below 17.5.4 Standard / 17.3.18 LTS, comments could break
  evaluation on forms and surveys, and below 17.5.1 / 17.3.14 they could stop alerts firing.

---

## 4. Blank handling

- Blank (`''`) is not zero (`0`). Test answered vs unanswered with `[field]<>''` / `[field]=''`; test
  for zero with `[field]=0`.
- `[a]+[b]+[c]` treats a blank as 0, so it always returns a number (0 if all are blank). `sum([a],[b],[c])` skips blanks and returns blank only if **every** input is blank (16.0.41+; earlier versions returned 0). Neither waits for all fields to be filled in. To keep the total blank until every field has a value, test explicitly:
  `if(isblankormissingcode([a]) or isblankormissingcode([b]) or isblankormissingcode([c]), "", [a]+[b]+[c])`
  (RC-CALC-01 §6.3 — tested on 16.0.49.)
- `sum()`, `mean()`, and similar aggregate functions skip blank values — they don't treat blank as zero.
- A calc field whose `if()` returns `''` stores blank — expected behavior, not an error.
- A calc field whose formula produces text or a date stores blank.
- A cross-event field never saved in that event returns `''` (not `0`).
- `[previous-instance]` returns blank in instance 1; `[previous-event-name]` returns blank in the
  first event and `[next-event-name]` in the last (RC-PIPE-09, RC-PIPE-10).

---

## 5. Checkbox syntax

```
[checkbox_field(coded_value)]='1'    # option checked
[checkbox_field(coded_value)]='0'    # option not checked
```

Example: `[symptoms(3)]='1'` checks whether the option coded "3" is selected. Each option is a
sub-variable storing 1 (checked) or 0 (unchecked) (RC-BL-04).

A plain `[checkbox_field]` without the code in parentheses does not reference any option in logic (RC-BL-04). When piped into text it shows the checked labels, comma-separated (RC-PIPE-02).

"None of options 1–3 checked": `[field(1)]='0' AND [field(2)]='0' AND [field(3)]='0'` (RC-BL-04).
Count of checked options: `sum([symptoms(1)],[symptoms(2)],[symptoms(3)])`.

---

## 6. Cross-event references (longitudinal)

In a longitudinal project a plain `[variable]` refers to the **same event** as the field being
evaluated. To reach another event, prepend the unique event name:

```
[unique_event_name][variable_name]
```

- ✅ `[baseline_arm_1][visit_date]`
- ❌ `[baseline_arm_1].[visit_date]` (dot), ❌ `[baseline_arm_1] [visit_date]` (space),
  ❌ `[baseline_arm_1[visit_date]]` (nested)

The unique event name comes from **Project Setup → Define My Events** (Unique Event Name column),
auto-generated from the event label and arm — e.g., `baseline_arm_1`, `followup_4wk_arm_2`. Not the
display label.

Gotchas (RC-BL-05, RC-AT-09 §7):
- A field never saved in that event returns `''`.
- A field not designated to that event returns blank at runtime with no error message.
- In multi-arm projects, `[baseline_arm_1][field]` returns blank for records in Arm 2.
- **Renaming an event silently changes its unique event name**; every reference to the old name
  goes blank with no warning. Treat referenced event and field names as frozen once in use.

For relative (dynamic) event references, see the event smart variables in §8.

---

## 7. Instance qualifiers (repeating instruments/events)

Within a repeating instrument, plain `[variable]` means the current instance. To reach another
instance, append a qualifier in its own brackets immediately after the variable:

```
[variable_name][instance_qualifier]
[unique_event_name][variable_name][instance_qualifier]   # longitudinal + repeating
```

| Qualifier | References |
|---|---|
| `[1]`, `[2]`, … | A fixed instance number |
| `[current-instance]` | The current instance (same as no qualifier) |
| `[previous-instance]` | The instance before the current one — blank in instance 1 |
| `[next-instance]` | The instance after the current one (calculated; may have no data yet) |
| `[first-instance]` | The first (lowest-numbered) instance |
| `[last-instance]` | The last (highest-numbered) instance — dynamic, changes as instances are added (RC-PIPE-10) |

Examples:
- `[med_name][1]='Aspirin'`
- `[visit_status][previous-instance]='complete'`
- `[baseline_arm_1][phq9_total][last-instance]`
- `[previous-event-name][field][current-instance]` (RC-PIPE-10)

Gotchas:
- Instance qualifiers only make sense on fields on a repeating instrument or in a repeating event. On
  a non-repeating field the KB documents no reliable result — treat it as a mistake and remove the
  qualifier.
- `[new-instance]` cannot be appended to field variables — only to `[survey-link]`, `[survey-url]`,
  `[survey-access-code]`, `[form-link]`, `[form-url]` (RC-PIPE-10).
- Don't rely on `[last-instance]` when a stable reference is required.
- `[previous-instance]` accumulator chains in `@CALCTEXT` don't recalculate other instances
  automatically when one instance is edited (RC-AT-09 §7).

---

## 8. Smart variables in expressions

Smart variables use the same bracket syntax as fields but resolve to runtime context.

**Event smart variables** (RC-PIPE-09) — `[event-name]`, `[event-label]`, `[previous-event-name]`,
`[next-event-name]`, `[first-event-name]`, `[last-event-name]`:
- **Standalone** they return a property of the event: `[event-label]='Baseline'` in branching logic.
- **Prepended to a field** they act as a dynamic event prefix: `[previous-event-name][weight]>100`.
  Prepended, they find the closest previous/next/first/last event **where that field's instrument is
  designated** — which may differ from the standalone result if instruments aren't in every event.
- `[previous-event-name]` is blank in the first event; `[next-event-name]` is blank in the last.
- Hard-coded `[baseline_arm_1][weight]` is fixed; `[first-event-name][weight]` adapts.

**Instance smart variables** (RC-PIPE-10) are also usable standalone:
`if([current-instance]=1, "First response", "Later response")`.

**Record smart variables** (RC-PIPE-06) — e.g., `[record-name]`, `[record-dag-name]` — are usable
in logic: `[record-dag-name]='site_b'`.

**As @CALCTEXT return values** (RC-AT-09 §3.3): field variables and smart variables can be returned
directly, unquoted — `@CALCTEXT(if([age]>=18, [dob], [event-label]))`, `@CALCTEXT([record-name])`.
They cannot be piped inside a quoted string.

---

## 9. Calculated field rules

- Output must be numeric; text or date output stores blank. Need text → `@CALCTEXT`; need a date →
  `@CALCDATE`. (A calc field can return the *number* of days between dates via `datediff()`.)
- `if()` requires all three arguments; both return values must be numbers for a calc field.
- `datediff([d1],[d2],'unit')` — the unit is required. Pass `true` as the 4th argument for a signed
  result (negative if d1 > d2).
- Age: `age_at_date([dob],'today',false)` gives calendar-accurate whole years; `datediff(...,'y')` is a
  365.2425-day approximation. Pass the 3rd argument of `age_at_date` explicitly on 17.0.6–17.1.1,
  where omitting it fails silently (RC-CALC-01 §5.2).
- Values update in real time during data entry, during data import, and when Data Quality rule H is
  run. Changing a formula does **not** update existing records — run rule H afterward.

---

## 10. @CALCTEXT rules (RC-AT-09 §3)

- `@CALCTEXT(expression)` goes on a **Text Box only**; the field becomes non-editable.
- Can return text, numbers, field values, or smart variables. `''` returns blank.
- No variables inside quoted strings; escape apostrophes (both in §3).
- `concat()` joins everything including blanks; `concat_ws(separator,...)` joins with a separator and
  skips blanks.
- If the field has validation (e.g., Integer), the computed value must conform or it is rejected.
- Updates in the same contexts as a calc field (data entry, import, rule H).

---

## 11. @CALCDATE rules (RC-AT-09 §4)

**Syntax:** `@CALCDATE(source, offset, unit)` — exactly three arguments.

| Parameter | Valid values |
|---|---|
| `source` | A date/datetime field variable, `'today'`, `'now'` (in single quotes; server time), or an `if()` returning a date. Cross-event: `[event_name][date_field]` |
| `offset` | A positive or negative number (forward/back in time), or a field variable returning a number |
| `unit` | `'y'` years · `'M'` months (capital M) · `'d'` days · `'h'` hours · `'m'` minutes (lowercase m) · `'s'` seconds — **case-sensitive** |

- Both source and result fields must have date, datetime, or datetime_seconds validation, or
  `@CALCDATE` will not work.
- Best practice: source and result use the same date format (e.g., both `date_ymd`); mixing formats
  (e.g., `date_ymd` → `datetime_ymd`) can cause display issues.
- `'M'` (months) vs `'m'` (minutes) is a common error — double-check case.
- `'y'` = 365.2425 days, `'M'` = 30.44 days. For exact intervals (30, 90 days) use `'d'`.
- `'today'`/`'now'` use server time; in multi-timezone deployments the date can be one day off.

---

## 12. Action tag nesting

Always invalid:
- `@CALCTEXT` or `@CALCDATE` inside an `@IF(...)` action tag (RC-AT-08, RC-AT-09) — the calculation
  tags run in more contexts (real-time, import, rule H) than `@IF`, so results are unpredictable.
- One action tag nested inside another (e.g., `@CALCTEXT(@CALCDATE(...))`).

The `if()` **function** inside `@CALCTEXT`/`@CALCDATE` is fine — it's the `@IF` **action tag** that
can't wrap them.

---

## 13. Related KB articles

- RC-BL-01 — Branching Logic: Overview & Scope
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements
- RC-BL-03 — Branching Logic: Combining Statements
- RC-BL-04 — Branching Logic: Structured Fields & Checkboxes
- RC-BL-05 — Branching Logic: Longitudinal Projects
- RC-CALC-01 — Special Functions Reference
- RC-CALC-02 — Calculated Fields
- RC-AT-08 — Action Tags: @IF
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE
- RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers
- RC-PIPE-06 — Smart Variables: Record
- RC-PIPE-09 — Smart Variables: Event and Arm
- RC-PIPE-10 — Smart Variables: Repeating Instruments and Events

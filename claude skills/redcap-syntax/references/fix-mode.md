# Fix Mode — Diagnose and Correct an Expression

Diagnose every error in a REDCap expression and return a corrected version. Keep two categories
clearly separate in the output — they have different causes and different fixes.

**Syntax errors** — the expression itself is malformed or misuses REDCap syntax: wrong operators,
unclosed brackets, bad function calls, wrong argument counts, wrong unit case. Detectable from the
expression alone.

**Reference errors** — the syntax is valid, but it points to something that doesn't exist or isn't
accessible: a field not in the project, a misspelled or nonexistent event name, a field not
designated to that event, an instance qualifier on a non-repeating field, a checkbox code that
doesn't exist. Detecting these requires the project's structure.

Rule details are in `syntax-core.md` (section numbers given below). Read `functions.md` before
checking any function call.

---

## Step 1: Identify the expression type

Classify it with the type table in `syntax-core.md` §1 — the type determines which rules apply. If
ambiguous (e.g., a bare `[score_a] + [score_b]`), ask where it is used or explain both possibilities.

---

## Step 2: Gather reference context if needed

Check **syntax immediately** — no project information needed.

For **reference errors** you need:
- The project's field names (a data dictionary or just a field list), plus checkbox codes if
  checkbox options are referenced
- For longitudinal projects: unique event names and which events each referenced field is
  designated to
- For repeating setups: which instruments/events repeat

If missing, ask:
> "To check whether the field names and event references are valid, can you share the field names in your project (or a Data Dictionary export)? If it's a longitudinal project, I also need the unique event names."

Or, if the user named a connector and project, use live validation (Step 5). Don't block on this —
proceed with the syntax check and note that reference checking was skipped.

---

## Step 3: Syntax check

Work through every category. Each is a class of error REDCap either rejects or silently mishandles.

**3a. Bracket and quote balance** — every `[` has `]`, every `(` has `)`, every quote closes with the
same quote type (no `'value"`). Recommend single quotes (`syntax-core.md` §3).

**3b. Operators** (§2) — `==`→`=`, `!=`→`<>`, `&&`→`AND`, `||`→`OR`, `!`/`NOT`→`<>` (no NOT keyword
in REDCap, RC-BL-03). **Mixed AND/OR without parentheses:** AND binds before OR, so
`[a]='1' OR [b]='1' AND [c]='1'` means `[a]='1' OR ([b]='1' AND [c]='1')`. If that's probably not
what the user meant, flag it as a logic error and add explicit parentheses.

**3c. Functions** — for each function call (check `functions.md`):
1. Is the name valid? (If not — unknown function.)
2. Right number of arguments?
3. Arguments in the right order?

Frequent argument errors:
- `datediff([d1], [d2])` — missing the required third argument (unit string)
- `@CALCDATE([date], 7)` — missing the required third argument (unit)
- `if([cond], 'yes')` — missing the false branch; `if()` requires 3 arguments
- `age_at_date([dob], [date])` — the third arg (`returnDecimal`) is optional, but on 17.0.6–17.1.1 omitting it fails silently (blank result). Recommend passing it explicitly (`false` for whole years), and make sure the first two are date fields
- `datediff([dob], ..., 'y')` used for **age** — not a syntax error, but `'y'` is a 365.2425-day approximation; suggest `age_at_date()` instead
- `round([x])` — valid (defaults to 0 decimal places), but flag if the user likely intended a specific precision
- `today` unquoted as a date argument — should be `'today'`

**Blank handling — `+` vs `sum()`** (§4): if the complaint is about blanks or zeros in a total, check which form they used. `+` treats a blank as 0 (always returns a number); `sum()` skips blanks and returns blank only if every input is blank (16.0.41+). If they want the total to stay blank until every input is filled, neither works on its own — wrap it: `if(isblankormissingcode([a]) or ..., "", [a]+[b])` (RC-CALC-01 §6.3).

**3d. Exponentiation** (§2) — both base and exponent in their own parentheses:
❌ `[height]^2`, ❌ `[height]^(2)`, ✅ `([height])^(2)`.

**3e. Curly brackets** — `{variable}` is Field Embedding syntax and has no role in logic or
calculations; it should be `[variable]`.

**3f. Variables inside quoted strings** (§3) — `@CALCTEXT(if([group]='1', 'Hello [name]', ''))`
outputs the literal `Hello [name]`. Fix: `@CALCTEXT(if([group]='1', [name], ''))` or
`concat('Hello ', [name])`. REDCap won't flag this — it's a logic error causing unexpected output.

**3g. Unescaped apostrophes in @CALCTEXT text** (§3) — `'The user's guide'` breaks parsing. Fix:
`'The user\'s guide'` or `"The user's guide"` (RC-AT-09 §3.4).

**3h. Action-tag nesting** (§12) — `@CALCTEXT`/`@CALCDATE` inside an `@IF(...)` action tag, or one
action tag inside another, is always invalid.

**3i. @CALCDATE parameters** (§11) — exactly three arguments; unit is case-sensitive: `'M'` months,
`'m'` minutes (a very common error); both fields need date/datetime validation.

**3j. Cross-event syntax** (§6) — two adjacent bracket pairs, no dot, space, or nesting:
✅ `[baseline_arm_1][visit_date]`; ❌ `[baseline_arm_1].[visit_date]`.

**3k. Instance qualifier syntax** (§7) — qualifier in its own brackets after the variable
(`[field][previous-instance]`; longitudinal `[event][field][qualifier]`); only the valid qualifiers;
`[new-instance]` never on a field variable.

**3l. Checkbox references** (§5) — a plain `[symptoms]` on a checkbox field does not reference any
option in logic (RC-BL-04). To test option "3": `[symptoms(3)]='1'` (or `='0'` for unchecked).

**3m. `:label` in functions** (§3) — `contains([status:label],'active')` won't work; functions only
see raw stored values.

**3n. Type/return mismatch** (§9–§11) — a calc field returning text or a date stores blank; suggest
`@CALCTEXT`/`@CALCDATE`. A calc `if()` returning `''` gives blank — expected, not an error.

---

## Step 4: Reference check

Only with project context (user-provided or from live validation).

**4a. Field existence** — every `[field_name]` (excluding event names, smart variables, and instance
qualifiers) exists? If not → **field does not exist**; check the Codebook for the correct variable
name.

**4b. Checkbox codes** — every `[field(code)]` uses a code defined in that field's choices, and the
field is actually a checkbox?

**4c. Event name validity** — every `[event_name][field]` uses a unique event name from Define My
Events? If not → **event name does not exist or is misspelled**. Renaming an event silently changes
its unique event name, breaking old references.

**4d. Field designated to event** — the field's instrument is designated to that event? If not →
**field not assigned to this event**; it returns blank at runtime with no error. Fix in Project Setup
→ Designate Instruments for My Events.

**4e. Repeating qualifiers** — for `[field][qualifier]`, is the field on a repeating instrument or in
a repeating event? If not → **instance qualifier on a non-repeating field**; the KB documents no
reliable result — remove the qualifier.

**4f. Version-specific defects** — if the expression is valid and the references check out but it
still misbehaves *on the form or survey*, ask which REDCap version the instance runs (or read it via
`export_redcap_version` during live validation) and check this table. Each row was a silent wrong
result, not an error message. Name the defect and the fix version rather than "correcting" valid
syntax.

| Symptom | Affected versions | KB |
|---|---|---|
| Very long logic (~200–300+ `and`/`or` clauses) always True | 17.3.1–17.4.1 Std / 17.3.5–17.3.7 LTS | RC-BL-01 §4a |
| Logic or calc with inline comments fails to evaluate | below 17.5.4 Std / 17.3.18 LTS | RC-BL-02 §3.6 |
| Alert with comment lines never fires | below 17.5.1 Std / 17.3.14 LTS | RC-ALERT-01 §3.2 |
| Comparison text containing `'` or `"` silently does nothing | below 17.5.4 Std / 17.3.18 LTS | RC-BL-02 §3.3 |
| `0` treated as blank (and blank as not) for number/integer fields on a repeating event | below 17.5.4 Std / 17.3.18 LTS | RC-BL-02 §6 |
| X-instance qualifier on a date field with a Missing Data Code gives an odd result on the page only | below 17.5.0 Std / 17.3.13 LTS | RC-BL-05 §5.3 |
| `@CALCTEXT` HTML stripped when piped on another page of a multipage survey | below 17.5.1 Std / 17.3.14 LTS | RC-AT-09 §3.3 |
| Every calc on the form recalculates on any change (slow forms) | below 17.5.3 Std / 17.3.16 LTS | RC-CALC-02 §6 |

"Page only" defects are a strong clue: if Data Quality rule H or an import computes the right value
but the form shows the wrong one, suspect the version before the expression.

---

## Step 5 (optional): Validate against the live project

If the user named a connector and project: confirm the connector first and say if it is
**production**. Then, using only the read-only tools listed in `SKILL.md`:
- `export_metadata` → field names, field types, checkbox/radio codes, validation (4a, 4b, 3i)
- `export_project_info` → longitudinal? repeating enabled?
- `export_events` → unique event names (4c)
- `export_instrument_event_mappings` → designations (4d)
- `export_repeating_instruments_events` → repeat setup (4e)
- `export_redcap_version` → instance version (4f)

Never import, delete, or export records.

---

## Step 6: Output

Be concise — assume the user knows REDCap unless they signal otherwise. Explain the **why** behind
each error so it doesn't recur. When the user asked "why", make the explanation fuller.

**Before writing the corrected expression, enumerate every error you found** — don't silently fix
anything. If you changed `==` to `=`, it appears as an explicit entry. The corrected expression
should follow directly from the listed errors, with no surprise changes.

### Expression type
State the type and anything worth flagging (e.g., "this is a @CALCDATE, so the result field needs
date validation").

### Errors found

**Syntax errors** — for each: where it appears → what's wrong → the fix. List every error, however
minor.

**Reference errors** — for each: which variable/event/code → what's wrong → what to verify or change.

If reference checking was skipped, say so briefly and flag references that *could* be wrong (unusual
field names, unverifiable event names). If live validation ran, say which connector and what was
confirmed. Omit a category heading if it has no errors.

### Corrected expression
The full corrected expression. For project-specific names you can't verify, use a descriptive
placeholder like `[correct_field_name]` and explain what goes there.

If there were **no errors at all**, say so clearly. Don't manufacture problems. You may still note
non-error observations (e.g., a `sum()` vs `+` tradeoff, a blank-vs-zero edge case) if worth knowing.

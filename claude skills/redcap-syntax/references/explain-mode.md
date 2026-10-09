# Explain Mode — Read and Interpret an Expression

Give the user a clear, plain-language explanation of what an expression does, what it returns,
and where it is used — plus any gotchas worth noting. The rules behind each point are in
`syntax-core.md`; function behavior is in `functions.md` (read it before explaining any function
call — argument meaning and defaults matter).

If, while explaining, you find an actual error, say so plainly and switch to Fix-mode output for
that part (`fix-mode.md`). Don't bury an error inside an explanation.

---

## Step 1: Identify the expression type

Classify it with the "How to recognise it" column in `syntax-core.md` §1: logic (true/false),
calculated field (number), @CALCTEXT (text or number), @CALCDATE (date). If it could be either a calc
formula or the inside of a @CALCTEXT, ask where it appears or explain both.

---

## Step 2: Explain the expression

Walk through it in plain language, covering:

1. **What it does** — what REDCap will compute or evaluate, piece by piece for nested expressions
   (work from the innermost function outward, or condition by condition for nested `if()`).
2. **What it returns** — a number, text, a date, or true/false — including what it returns when
   inputs are blank (`syntax-core.md` §4).
3. **Where it belongs** — which field type or context it is valid in.
4. **Notable gotchas** — only those that apply to *this* expression.

Tailor depth to the user: a project builder doesn't need the basics; a researcher seeing their first
formula needs more context.

### What to point out, by type

**Logic** — anatomy `[variable] operator value`; AND means all must be true, OR at least one; AND
binds before OR, so say how an unparenthesized mix actually evaluates (§2). Functions can feed
logic, e.g., `age_at_date([dob],'today',false)>=18` computes whole-year age then compares. Boolean
functions like `contains([name],'taylor')` or `isnumber([age])` can stand alone. Note blank vs zero,
case-sensitive text, and that REDCap validates syntax, not logic (an impossible condition saves
without error). Logic is used in branching logic, report filters, survey invitations, alerts, Data
Quality rules, and inside `if()` — not for field validation constraints.

**Calculated field** — what the arithmetic produces; how blanks behave (`+` vs `sum()`, §4); that
exponents need `([base])^(exponent)` form; that output must be numeric (text/date → blank); and when
values update — data entry, import, Data Quality rule H, not automatically after a formula change
(§9).

**@CALCTEXT** — which branch returns what; that quoted text containing `[var]` is literal, not piped;
apostrophe escaping (`\'`); that smart variables like `[event-label]` or `[record-name]` can be
returned directly; validation must accept the output (§10).

**@CALCDATE** — source, offset, and unit in plain words ("90 days after the baseline visit date");
`'M'` vs `'m'`; approximations for `'y'`/`'M'`; server time for `'today'`/`'now'`; both fields need
date validation and ideally the same format (§11).

**Advanced references** — translate each into words:
- `[baseline_arm_1][weight]` → "weight from the Baseline event (Arm 1)"; blank if never saved there,
  not designated there, or the record is in another arm (§6).
- `[med_name][last-instance]` → "medication name from the last (highest-numbered) instance — changes
  as instances are added"; `[previous-instance]` is blank in instance 1 (§7).
- `[previous-event-name][heart_rate]` → "heart rate from the closest earlier event where that
  field's instrument is designated" — not necessarily the immediately preceding event (§8).
- `[symptoms(3)]='1'` → "option coded 3 of the symptoms checkbox is checked" (§5).

---

## Output format

### Type
One line: the expression type, what it returns, and where it lives.

### What it does
Plain-language walkthrough. For long or nested expressions, break it into numbered parts or a short
condition → result table.

### Edge cases
What happens with blanks, first instance/event, other arms, or values outside the expected range —
only those relevant to this expression.

### Watch out for
Genuinely relevant gotchas only. If something is actually wrong, state it here as an error and give
the corrected expression (Fix-mode rules apply).

For a conceptual question with no expression (e.g., "calc field vs @CALCTEXT?"), answer from the
type tables in `syntax-core.md` §1 with a short example of each.

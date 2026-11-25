---
id: RC-BL-02
title: Branching Logic — Syntax & Atomic Statements
domain: Branching Logic
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — branching
  logic syntax checked against source code; §3–§8 live-tested on v17.5.6; pages not
  re-captured
prerequisites:
- 'RC-BL-01 — Branching Logic: Overview & Scope'
version: '1.4'
last_updated: 2026-11
related:
- id: RC-BL-01
  title: 'Branching Logic: Overview & Scope'
- id: RC-BL-03
  title: 'Branching Logic: Combining Statements'
- id: RC-BL-04
  title: 'Branching Logic: Structured Fields & Checkboxes'
- id: RC-FD-03
  title: Data Dictionary
tags:
- branching logic
synonyms:
- how do i write a branching logic statement
- redcap logic syntax operators
- what operators can i use in branching logic
- how to reference a field in branching logic
- single condition logic statement
- branching logic brackets and quotes
- greater than less than equals in redcap logic
- how to write a simple conditional expression
- how do i add comments to branching logic
- 'annotate logic with // or # comments'
- why is my branching logic comment a syntax error
- can i use != in redcap branching logic
- compare two fields only when both are filled in
---

# 1. Overview

This article covers the REDCap logic syntax in detail — the operators,
brackets, quotes, and boolean keywords that make up valid logic
expressions — and explains how to construct an atomic logic statement:
the simplest, single-condition statement that forms the building block
of all branching logic.

---

# 2. Key Concepts & Definitions

**Atomic Logic Statement**

The simplest possible logic expression in REDCap. It always has exactly
three parts: a variable, an operator, and a comparison value. Example:
\[age\]\>=18.

**Variable Reference**

A reference to a REDCap field, written as the field's variable name
enclosed in square brackets. Example: \[dob\], \[consent\_status\].
Variables can only reference values within the same record.

**Operator**

A symbol that defines the comparison relationship between a variable and
a value. REDCap supports equality, inequality, and numeric comparison
operators.

**Comparison Value**

The value on the right-hand side of an operator. Can be a number, a
quoted text string, an empty string (to test for blank), or another
variable reference.

**Raw Value**

For structured field types (radio buttons, dropdowns, checkboxes),
REDCap stores the coded option value — not the display label — in
the dataset. Logic statements must reference raw values, not labels.

---

# 3. Syntax Language Reference

## 3.1 Math Operators

REDCap supports standard arithmetic operators for use in calculated
fields and numeric comparisons. These operate on numbers only.

| **Operator** | **Meaning** | **Example** |
| --- | --- | --- |
| + | Addition | [score_a]+[score_b] |
| - | Subtraction | [total]-[deductions] |
| * | Multiplication | [dose]*[weight] |
| / | Division | [total]/[count] |
| ^ | Exponent | ([base])^(2) |
| = | Equals | [status]=1 |

When raising a value to a power, put both the base and the exponent in parentheses — `([base])^(2)`, not `[base]^2`.

## 3.2 Comparison Operators

Comparison operators are the most common operators in branching logic.
They compare a variable to a value and return true or false.

| **Operator** | **Meaning** | **Example** |
| --- | --- | --- |
| = | Equal to | [gender]='1' |
| <> | Not equal to | [status]<>0 |
| > | Greater than | [age]>18 |
| >= | Greater than or equal to | [age]>=18 |
| < | Less than | [bmi]<25 |
| <= | Less than or equal to | [bmi]<=25 |

`!=` is also accepted as "not equal to" and behaves exactly like `<>`, including being true when the field is blank. `<>` remains the conventional form in REDCap documentation.

Write each operator exactly as shown. `==`, `=<` and `=>` are syntax errors — use `=`, `<=` and `>=`.

> **Best Practice:** Logic that hinges on a value being 0 or blank — `=0`, `<>0`, `=''` — can behave inconsistently. Where you can, write the logic to test for the value you actually want: `[status]=1` or `[nr_pregnancies]>0` rather than `[status]<>0`.

## 3.3 Quotation Marks

Any comparison value that is not a number must be enclosed in quotation
marks. Both single and double quotes are accepted.

```
// double quotes
[fav_color]="green"
                                                        
// single quotes — equivalent
[fav_color]='green'
                                                        
// empty string check (double quotes)
[email]<>""
                                                        
// empty string check (single quotes)
[email]<>''
```


> **Version caveat (below 17.5.4 Standard / 17.3.18 LTS):** In some cases, a comparison value or label containing an **apostrophe or quotation mark** — `[site]="O'Brien Clinic"` — generated invalid JavaScript on the form or survey, so the branching logic or calculation silently stopped working there. REDCap now escapes these characters. The fix is not in the 16.x LTS line, so it applies to every 16.x instance too. On older versions, avoid quote characters inside comparison values; compare against a coded value instead of label text.

> **Note:** Even on current versions, a Data Dictionary upload rejects logic like `[site]="O'Brien Clinic"` as a syntax error, although the Online Designer accepts it and it evaluates correctly. If logic will travel through the Data Dictionary, compare against a coded value instead.

> **Version caveat (16.x LTS):** The Online Designer also blocks `[site]="O'Brien Clinic"`, because the value leaves an odd number of quote characters in the logic. On a 16.x instance, compare against a coded value everywhere.

> **Best Practice:** If you plan to edit your logic via the Data Dictionary in Excel or another spreadsheet program, use single quotes throughout. Excel interprets double quotes as part of its own formula syntax, which can corrupt logic statements during CSV import/export.


## 3.4 Square Brackets \[ \] and Their Uses

Square brackets are used to reference three types of identifiers in
REDCap logic:

| **What Is Referenced** | **Syntax** | **Example** |
| --- | --- | --- |
| Regular field variable | [variable_name] | [first_name], [dob] |
| Checkbox sub-variable | [variable_name(raw_value)] | [conditions(3)] |
| Longitudinal event (advanced) | [event_name] | [baseline_arm_1] — covered in advanced series |
| Smart variable (advanced) | [smart_variable_name] | Covered in separate training |


> **Note:** Curly brackets { } are used exclusively by the Field Embedding feature and have no role in branching logic syntax. If you see curly brackets in a logic field, something has gone wrong.

Do not put spaces inside the brackets: write `[age]`, not `[ age ]`. The Online Designer rejects the spaced form. A Data Dictionary upload strips the spaces and shows a warning, so the logic you end up with is not exactly what you uploaded.


## 3.5 Boolean Operators

Boolean operators join two or more logic statements together. REDCap
supports AND and OR, written either all lowercase (`and`, `or`) or all
uppercase (`AND`, `OR`). Mixed case such as `And` or `Or` is a syntax
error.

| **Operator** | **Behavior** | **Example** |
| --- | --- | --- |
| AND / and | Both statements must be true for the combined statement to be true | [age]>=18 and [consent]='1' |
| OR / or | At least one statement must be true for the combined statement to be true | [country]='US' or [country]='CA' |

There is no NOT keyword. To exclude a value, use the not-equal operator
`<>` — for example `[country]<>'US'`.

`and` and `or` need a space on each side. `([age]>=18) and ([consent]='1')`
works; `([age]>=18)and([consent]='1')` is a syntax error. A line break
counts as a space, so splitting logic across lines is fine.

When AND and OR appear in the same statement, AND is evaluated before
OR, so parentheses are not strictly required. Use them anyway: they make
the intended grouping explicit and protect the logic from being misread
or mis-edited later. See [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md) for full details.

## 3.6 Inline Comments

Logic can carry comments, but **only on a line of their own**. A line that starts with `//` or `#` is ignored when the logic is evaluated, which lets you annotate long logic in the Logic Editor:

```
// consented adults with a site assigned
[consent]='1'
and [age]>=18
# site is filled in
and [site]<>''
```

A comment placed **after logic on the same line** — `[age]>=18 // adult` — is a syntax error. The Online Designer refuses to save it and a Data Dictionary upload rejects it, with either `//` or `#`. Used as a report filter or an API `filterLogic` value, the same logic fails silently and matches every record.

> **Version caveat (16.x LTS):** REDCap administrators are not blocked by the Online Designer's syntax check — they see a warning but can still save logic with a syntax error, including a trailing comment or a misspelled variable. Ordinary project users are blocked. If you are an administrator on a 16.x instance, treat the warning as an error and fix the logic before saving.

Comments are worth using on any logic someone else will maintain, but they have the longest defect history of any logic feature — a run of fixes from 13.6.1 to 17.5.4 covering comments in calculations, Form Display Logic, `@IF`, alerts and Data Dictionary uploads. Two rules keep them safe on any version:

- Put every comment on its own line, never after logic.
- Avoid apostrophes and quotation marks inside comments.

> **Version caveat (below 17.5.4 Standard / 17.3.18 LTS):** Logic or calculations containing inline comments could fail to evaluate in some places and return an error. Alert logic with comment lines could fail to trigger the alert (fixed earlier, in 17.5.1 Standard / 17.3.14 LTS). If logic that works without its comments fails with them on an older instance, remove the comments.

---

# 4. The Atomic Logic Statement

Every logic statement — no matter how complex — is built from atomic
statements. An atomic statement always has exactly three parts:

| **Part** | **What It Is** | **Examples** |
| --- | --- | --- |
| 1. Variable | A reference to a field in the current record, written in square brackets | [age] [consent_date] [exclusion_q3] |
| 2. Operator | Defines the comparison relationship | = <> > >= < <= |
| 3. Comparison value | What the variable is being compared to | 18 'yes' [other_var] '' |

The comparison value can be one of the following types:

| **Comparison Value Type** | **Format** | **Example** |
| --- | --- | --- |
| Number | No quotes needed; quotes accepted with = and <>, but leave them off with <, >, <= and >= | [age]>=18 |
| Text string | Must be enclosed in single or double quotes | [status]='enrolled' |
| Empty / blank | Two quotes with nothing between them | [email]<>'' |
| Another variable | Variable name in square brackets | [email1]=[email2] |

---

# 5. Worked Examples

**Example 1 — Equality: Show field only if age is exactly 18**


> [age]=18


The field is shown only when the value of \[age\] equals exactly 18. Any
other value hides the field.

**Example 2 — Greater Than or Equal: Show field for adults**


> [age]>=18


The field is shown when \[age\] is 18 or any higher number. The field is
hidden for values below 18.

**Example 3 — Not Equal: Show field for any non-zero number of
pregnancies**


> [nr_pregnancies]<>0


The field is shown when \[nr\_pregnancies\] is any value other than 0
(e.g., 1, 2, 3). Important: 0 (numeric zero) and '' (empty/blank) are
not the same thing. Zero is a data value; empty means no data has been
entered at all.

> **Best Practice:** Logic built on "not 0" can behave inconsistently when the field is blank or 0. When \[nr\_pregnancies\] is a number-validated field, test for the positive case instead: \[nr\_pregnancies\]\>0 shows the field only for 1, 2, 3 and so on.

**Example 4 — Empty Check: Show a field only after email is entered**


> [email]<>''


The field is hidden while \[email\] is blank and appears as soon as
\[email\] contains any value. This pattern is commonly used to reveal a
follow-up question, such as an email-consent checkbox, once the
respondent has supplied an address. To do the reverse — show a warning
or reminder while \[email\] is still blank — use \[email\]=''.

**Example 5 — Comparing Two Variables**


> [email_primary]=[email_secondary]


The field is shown when the value of \[email\_primary\] exactly matches
the value of \[email\_secondary\]. Useful for validating that two fields
have the same entry (e.g., email confirmation).

Two blank fields also count as a match, so this statement is true before
either email has been entered. To match only real entries, add a blank
check: \[email\_primary\]=\[email\_secondary\] and \[email\_primary\]\<\>''.


> **Important:** REDCap validates that your logic syntax is correct (valid operators, properly closed brackets, known variable names), but it does not validate whether the logic makes sense for your study. A statement like [age]=999 is syntactically valid but will never match any realistic data. Always test your logic against real or realistic test data.


---

# 6. Empty vs. Zero --- A Critical Distinction

One of the most common logic errors in REDCap is treating an empty field
as equivalent to a field containing zero. They are not the same.

| **State** | **What It Means** | **How to Test For It** |
| --- | --- | --- |
| Empty / blank | No data has been entered into this field at all. The field has never been saved with a value. | [field]='' (equals empty string) |
| Zero (numeric) | The user actively entered the value 0 into a number field. Zero is a data value. | [field]=0 |

> **Best Practice:** In practice, logic that tests for 0 or for blank can behave inconsistently. Where you can, write the logic to test for the positive case — the value you actually want — rather than for 0 or blank. For a count, `[field]>0` is more dependable than `[field]<>0`; for a coded yes/no, `[field]=1` is more dependable than `[field]<>0`. Always confirm 0 and blank behaviour with test records.

> **Version caveat (below 17.5.4 Standard / 17.3.18 LTS, and all 16.x LTS):** For **integer and number fields on a repeating event**, client-side branching logic could treat `0` as blank and blank as non-blank — exactly the distinction this section depends on. The fix is not in the 16.x LTS line. If logic testing `=0` or `=''` misbehaves on a repeating event on an affected instance, upgrade (17.3.18 LTS or later); the stored data is unaffected.

> **Note:** Using [nr_pregnancies]<>0 will evaluate to true for both an empty field AND for values like 1, 2, 3. If you specifically want a field that has been filled in with a non-zero number, test for the positive case: [nr_pregnancies]>0 on a number-validated field.


---

# 7. Common Questions

**Q: Do I need to use quotes around numbers in logic statements?**

**A:** It depends on the operator. With `=` and `<>`, REDCap accepts
numbers with or without quotes (e.g., \[age\]=18 and \[age\]='18' both
work). With `<`, `>`, `<=` and `>=`, leave numbers unquoted and use them
on number-validated fields — \[age\]\>=18, not \[age\]\>='18'. A quoted
number, or a field without number validation, can make the comparison
come out wrong.

**Q: Are variable names in logic case-sensitive?**

**A:** Yes. Variable names in REDCap are always lowercase (REDCap
enforces this at field creation), and logic does not fold case to
match them, so a capitalized reference matches no field at all. Both
the Online Designer's logic editor and a Data Dictionary upload reject
`[Age]` as a syntax error, so it cannot be saved (on 16.x LTS,
administrators get only a warning — see the version caveat in §3.6). Used as a report
filter or API `filterLogic`, it fails silently and matches every
record. Text string comparison values are case-sensitive too.
\[status\]='Enrolled' will not match a stored value of 'enrolled'
(lowercase e).

**Q: Can I reference a field from a different record in my logic?**

**A:** No. Logic statements can only reference fields within the same
record. You cannot write logic that says 'show this field if the value
in record 2 is X'. All variable references are scoped to the current
record.

**Q: Can I use a function like datediff() as the comparison value?**

**A:** Yes — REDCap functions can be used in logic statements.
However, functions are an advanced topic outside the scope of this basic
series. See the dedicated functions training for details.

**Q: What happens if I reference a variable name that doesn't exist?**

**A:** The Online Designer's logic validator will flag the statement as
invalid and will not save it. In the Data Dictionary, an invalid
variable reference will cause an upload error. The exception is logic
that was already in the project unchanged: if a field's invalid logic is
identical to what is currently saved, a Data Dictionary re-upload only
warns about it and does not block the upload, so old errors can survive
round trips. Fix any logic the upload warns about. (On 16.x LTS,
administrators can also save invalid logic in the Online Designer — see
the version caveat in §3.6.) Always verify variable
names against the Codebook ([RC-FD-05 — Codebook](RC-FD-05_Codebook.md)) before writing logic.

---

# 8. Common Mistakes & Gotchas

- Comparing text without quotes: \[status\]=enrolled is invalid ---
    enrolled must be quoted as 'enrolled'. Unquoted non-numeric values
    cause syntax errors.

- Using double quotes in Excel-edited Data Dictionary files: Excel
    corrupts double-quoted strings in CSV files. Use single quotes
    ('value') instead of double quotes ("value") whenever the Data
    Dictionary will be edited in a spreadsheet program.

- Treating empty as zero: an empty field and a field containing 0 are
    different states, and logic that tests for either can behave
    inconsistently. Test for the positive case — the value you want —
    where you can, e.g. \[count\]\>0 rather than \[count\]\<\>0.

- **Using operators from other languages:** `==`, `=<` and `=>` are
    syntax errors. Use `=`, `<=` and `>=`. There is no NOT keyword; use
    `<>` for not-equal.

- **Mixed-case or unspaced and/or:** `And`, `Or` and
    `([a]=1)and([b]=1)` are syntax errors. Write `and`/`or` (or
    `AND`/`OR`) with a space on each side.

- **Putting a comment after logic on the same line:** `[age]>=18 // adult`
    is a syntax error, so the Online Designer and Data Dictionary upload
    reject it. Move the comment to its own line above or below the logic.

- **Forgetting that two blanks are equal:** `[email1]=[email2]` is true
    while both fields are still empty. Add `and [email1]<>''` when only
    real matches should count.

- Using curly brackets for variable references: curly brackets { } are
    for Field Embedding only. Variable references always use square
    brackets \[\]. Writing {variable} in a logic field will not work.

- Not testing logic against realistic data: REDCap validates syntax,
    not meaning. A statement can be syntactically valid but logically
    impossible (e.g., a range where min \> max). Always run test records
    to confirm the field shows and hides as intended.

---

# 9. Related Articles

- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (prerequisite)

- [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md) (AND, OR, parentheses)

- [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md)

- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (where branching logic is configured
    per field)

- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (bulk logic editing via CSV)

- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) (look up variable names and raw values when
    writing logic)

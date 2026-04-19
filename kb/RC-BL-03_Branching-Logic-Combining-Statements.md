RC-BL-03

**Branching Logic — Combining Statements**

| **Article ID** | RC-BL-03 |
| --- | --- |
| **Domain** | Branching Logic |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-BL-02 — Syntax & Atomic Statements |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-BL-02 — Syntax & Atomic Statements; RC-BL-04 — Structured Fields; RC-BL-01 — Overview |

# 1. Overview

This article explains how to combine multiple atomic logic statements
using AND, OR, and parentheses. Combined statements unlock more precise
and flexible branching conditions. Understanding how each operator
affects evaluation is essential for writing logic that behaves as
intended.

# 2. Key Concepts & Definitions

**Compound Statement**

A logic expression that joins two or more atomic statements using AND or
OR. A compound statement evaluates as a single true/false result.

**AND**

A boolean operator that joins two statements. The combined statement is
true only if ALL joined statements are individually true. If any single
statement is false, the whole expression is false.

**OR**

A boolean operator that joins two statements. The combined statement is
true if AT LEAST ONE joined statement is true. The combined statement is
false only when all joined statements are false.

**Parentheses**

Grouping symbols that control the order in which logic statements are
evaluated. Statements inside parentheses are evaluated first, before
those outside. Essential when AND and OR are used together in the same
expression.

**Short-Circuit Evaluation**

REDCap evaluates logic statements left to right. For AND, evaluation
stops at the first false statement (the result cannot be true). For OR,
evaluation stops at the first true statement (the result cannot be
false). This affects performance in large logic chains but not
correctness.

# 3. The AND Operator

**AND** joins two statements. The combined result is true only when
**all** joined statements are true.

## 3.1 Basic AND

+----------------------------------------------------------+
| \[sky\]=\'blue\' and \[grass\]=\'green\'                 |
|                                                          |
| // True only when BOTH conditions are met simultaneously |
+----------------------------------------------------------+

## 3.2 Chaining Multiple ANDs

+----------------------------------------------------------------+
| \[sky\]=\'blue\' and \[grass\]=\'green\' and \[water\]=\'wet\' |
|                                                                |
| // True only when ALL THREE conditions are met                 |
+----------------------------------------------------------------+

## 3.3 Common Use: Defining a Numeric Range

AND is the natural operator for expressing a range — a value must be
both above a lower bound AND below an upper bound.

+-----------------------------------------+
| \[age\]\>=35 and \[age\]\<=45           |
|                                         |
| // True for ages 35, 36, 37 \... 44, 45 |
|                                         |
| // False for age 34 or age 46           |
+-----------------------------------------+

## 3.4 Impossible AND Statements

It is possible to write an AND statement that can never be true.
REDCap\'s syntax checker will not catch this — it only validates
syntax, not logic.

+--------------------------------------------------------------------------+
| // IMPOSSIBLE: a single value cannot equal both 35 and 45 simultaneously |
|                                                                          |
| \[age\]=35 and \[age\]=45                                                |
|                                                                          |
| // IMPOSSIBLE: a number cannot be both greater than 15 and less than 10  |
|                                                                          |
| \[age\]\>15 and \[age\]\<10                                              |
+--------------------------------------------------------------------------+

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Warning:** An impossible AND statement means the field it governs will never appear to any user. The Online Designer will accept it without error. Always test logic with actual records.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3.5 Always-True AND Statements

The reverse is also possible — a statement that is always true,
causing the field to always show regardless of data values:

+------------------------------------------------------------------+
| // ALWAYS TRUE: age is always either \>= 35 or \<= 35            |
|                                                                  |
| \[age\]\>=35 and \[age\]\<=35 // Only true when age = exactly 35 |
|                                                                  |
| // If you intended a range, this might not be what you wanted    |
+------------------------------------------------------------------+

# 4. The OR Operator

**OR** joins two statements. The combined result is true when **at least
one** joined statement is true.

## 4.1 Basic OR

+----------------------------------------------------------------------+
| \[sky\]=\'blue\' or \[sky\]=\'black\'                                |
|                                                                      |
| // True when sky is either blue OR black (or both, if that were      |
| possible)                                                            |
+----------------------------------------------------------------------+

## 4.2 Chaining Multiple ORs

+----------------------------------------------------------------+
| \[country\]=\'US\' or \[country\]=\'CA\' or \[country\]=\'MX\' |
|                                                                |
| // True when country is any one of the three values            |
+----------------------------------------------------------------+

## 4.3 Common Use: Checking a Set of Checkbox Conditions

OR is natural for \'at least one of these applies\' conditions — for
example, showing a follow-up question when any of several checkboxes is
checked:

+----------------------------------------------------------------------+
| \[hypertension(1)\]=\'1\' or \[diabetes(1)\]=\'1\' or                |
| \[cancer(1)\]=\'1\'                                                  |
|                                                                      |
| // True when at least one of the three conditions is checked         |
|                                                                      |
| // (Checkbox syntax is covered fully in RC-BL-04)                    |
+----------------------------------------------------------------------+

## 4.4 Always-True OR Statements

OR statements are easy to make always-true by accident. A number is
always either \>= 35 or \<= 35 — so this statement evaluates to true
for every possible value:

+---------------------------------------------------------+
| // ALWAYS TRUE: every number is either \>= 35 or \<= 35 |
|                                                         |
| \[age\]\>=35 or \[age\]\<=35                            |
+---------------------------------------------------------+

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Always-true OR statements are harder to spot than always-false AND statements. Be especially careful when using OR with numeric comparison operators.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------

# 5. Combining AND and OR

When AND and OR appear in the same expression, the order of evaluation
matters. Without parentheses, AND is evaluated before OR (following
standard boolean operator precedence). Using parentheses explicitly
controls which conditions are grouped.

## 5.1 Why Parentheses Are Essential

Consider these two statements — identical tokens, different
parentheses, different behavior:

+----------------------------------------------------------------------+
| // Statement A                                                       |
|                                                                      |
| \[age\]\>=35 and (\[gender\]=\'female\' or \[hair\]=\'green\') and   |
| \[coffee\]=\'hot\'                                                   |
|                                                                      |
| // Requires: age \>= 35 AND (female OR green hair) AND coffee = hot  |
|                                                                      |
| // 3 independent conditions, one of which is itself a 2-way OR       |
|                                                                      |
| // Statement B                                                       |
|                                                                      |
| (\[age\]\>=35 and \[gender\]=\'female\') or (\[hair\]=\'green\' and  |
| \[coffee\]=\'hot\')                                                  |
|                                                                      |
| // Requires: EITHER (age \>= 35 AND female) OR (green hair AND hot   |
| coffee)                                                              |
|                                                                      |
| // Two independent 2-way AND groups, joined by OR                    |
+----------------------------------------------------------------------+

The only difference is where the parentheses are placed. The field will
show for entirely different populations depending on which statement is
used.

## 5.2 Rules for Parentheses

- Statements inside parentheses are always evaluated first.

- Parentheses can be nested: the innermost group is evaluated first.

- Every opening parenthesis must have a matching closing parenthesis.
    Mismatched parentheses cause a syntax error.

- When in doubt, add more parentheses — extra grouping does not
    change logic if placed correctly, but prevents misinterpretation.

## 5.3 Reference: AND vs. OR Behavior

  -------------- -------------------------------- ------------------------------
  **Operator**   **Result is TRUE when\...**      **Result is FALSE when\...**
  AND            All joined conditions are true   Any one condition is false
  OR             At least one condition is true   All conditions are false
  -------------- -------------------------------- ------------------------------

# 6. Worked Examples

**Example 1 — Age range with AND**

  -------------------------------
  \[age\]\>=18 and \[age\]\<=65
  -------------------------------

Show the field only for participants aged 18 to 65 inclusive. If age is
17 or 66+, the field is hidden.

**Example 2 — Multiple status options with OR**

  -------------------------------------------------------------------------
  \[enrollment\_status\]=\'active\' or \[enrollment\_status\]=\'pending\'
  -------------------------------------------------------------------------

Show the field when enrollment status is either \'active\' or
\'pending\'. Hidden for all other status values.

**Example 3 — Compound: age range AND consent given**

  -----------------------------------------------------
  \[age\]\>=18 and \[age\]\<=65 and \[consent\]=\'1\'
  -----------------------------------------------------

All three conditions must be true simultaneously: participant is 18--65
AND has given consent.

**Example 4 — Grouped OR within AND**

  -------------------------------------------------------------
  \[age\]\>=18 and (\[country\]=\'US\' or \[country\]=\'CA\')
  -------------------------------------------------------------

The participant must be 18 or older AND be from either the US or Canada.
The parentheses ensure the OR is evaluated as a unit before the AND.

**Example 5 — Two independent groups joined by OR**

  ----------------------------------------------------------------------------------------------------------------
  (\[diabetes(1)\]=\'1\' and \[insulin\_use\]=\'1\') or (\[hypertension(1)\]=\'1\' and \[bp\_medication\]=\'1\')
  ----------------------------------------------------------------------------------------------------------------

The field appears for participants who have diabetes AND use insulin, OR
for participants who have hypertension AND take blood pressure
medication.

# 7. Common Questions

**Q: Does REDCap differentiate between uppercase AND/OR and lowercase
and/or?**

**A:** No. REDCap accepts both AND and and, OR and or. The behavior is
identical regardless of case. Consistent casing improves readability but
has no functional effect.

**Q: What is the default evaluation order when AND and OR are mixed
without parentheses?**

**A:** AND has higher precedence than OR — it is evaluated first.
However, relying on implicit precedence is error-prone. Always use
parentheses to make the grouping explicit when AND and OR appear in the
same expression.

**Q: Can I chain more than two conditions with AND or OR?**

**A:** Yes. You can chain as many conditions as needed: \[a\]=1 and
\[b\]=2 and \[c\]=3 and \[d\]=4 is valid. The same applies to OR chains.
For very long chains, consider whether the logic can be simplified or
whether a calculated field would be more maintainable.

**Q: REDCap accepted my logic without error, but the field never shows.
What should I check?**

**A:** Check for an impossible condition — most commonly an AND
statement where the conditions cannot both be true simultaneously (e.g.,
a value that must be both \> 15 and \< 10). Also check whether any of
the referenced fields are themselves hidden by other branching logic,
which would prevent the condition from ever being met.

**Q: Can I use NOT as a standalone keyword instead of \<\>?**

**A:** REDCap does not support a standalone NOT keyword the way some
programming languages do. Use the \<\> operator to express \'not equal
to\'.

# 8. Common Mistakes & Gotchas

- Omitting parentheses when mixing AND and OR: without parentheses,
    AND takes precedence over OR. A statement that looks like it should
    test two groups may not behave as expected. Always parenthesize when
    combining both operators.

- Writing always-false AND ranges: \[age\]\>15 and \[age\]\<10 can
    never be true. No value is simultaneously greater than 15 and less
    than 10. The field will never appear.

- Writing always-true OR ranges: \[age\]\>=35 or \[age\]\<=35 is
    always true for any numeric input. This effectively removes the
    condition.

- Expecting REDCap to validate logical correctness: REDCap only checks
    syntax — valid brackets, known variable names, recognized
    operators. Logical impossibilities pass validation silently. Always
    test with real records.

- Missing a closing parenthesis: mismatched parentheses cause a syntax
    error. Count opening and closing parentheses carefully in complex
    statements, or build compound logic incrementally and test each
    step.

# 9. Related Articles

- RC-BL-02 — Syntax & Atomic Statements (prerequisite)

- RC-BL-04 — Branching Logic for Structured Fields & Checkboxes

- RC-BL-01 — Branching Logic Overview & Scope

RC-BL-04

**Branching Logic — Structured Fields & Checkboxes**

| **Article ID** | RC-BL-04 |
| --- | --- |
| **Domain** | Branching Logic |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-BL-02 — Syntax & Atomic Statements |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-BL-02 — Syntax & Atomic Statements; RC-BL-03 — Combining Statements; RC-FD-05 — Codebook; RC-DE-02 — Basic Data Entry |

---

# 1. Overview

This article explains how to write branching logic for structured field
types — fields with a predefined set of options. It covers the concept
of raw values, the distinction between single-choice and multiple-choice
(checkbox) fields, and the special sub-variable syntax required to
reference individual checkbox options.

---

# 2. Key Concepts & Definitions

**Structured Field**

A field type that restricts user input to a predefined set of options.
Because the possible values are known and controlled, structured fields
are particularly reliable anchors for branching logic.

**Raw Value**

The coded internal value REDCap stores for each option in a structured
field. Every option in a radio button, dropdown, or checkbox field is
defined as a raw value paired with a display label. Logic statements
must always compare against raw values, not display labels.

**Single-Choice Field**

A structured field type that stores exactly one selected value. Radio
buttons, dropdowns, Yes/No, True/False, and sliders are all
single-choice fields. The selected option\'s raw value is stored as a
single variable.

**Multiple-Choice Field (Checkbox)**

REDCap\'s checkbox field type, which allows multiple options to be
selected simultaneously. Unlike single-choice fields, checkboxes store
each option as a separate binary sub-variable rather than as a single
value.

**Checkbox Sub-Variable**

The individual variable created for each option in a checkbox field. A
checkbox with 5 options creates 5 sub-variables. Sub-variables are
referenced in logic using the format \[variable\_name(raw\_value)\].
Each sub-variable has a value of 1 (checked) or 0 (unchecked).

---

# 3. Raw Values --- What They Are and How to Find Them

Every option in a radio button, dropdown, or checkbox field is defined
using a \'raw value, label\' format. The raw value is what REDCap stores
in the database and what you must use in logic statements.

## 3.1 How REDCap Defines Options

In the Online Designer, options are entered one per line in the format:

+---------------------------------------------------+
| raw\_value, Display Label                         |
|                                                   |
| // Example — a radio button with three options: |
|                                                   |
| 1, Strongly Agree                                 |
|                                                   |
| 2, Agree                                          |
|                                                   |
| 3, Disagree                                       |
+---------------------------------------------------+

Raw values are typically integers, but they can be any text string. The
raw value is **unique within the field** — no two options in the same
field can share a raw value.

## 3.2 Where to Look Up Raw Values

- **Codebook (RC-FD-05):** The Codebook displays all options for every
    field in human-readable format, including raw values. This is the
    fastest reference when writing logic.

- **Online Designer:** Open the field\'s edit dialog. The choices
    section shows raw values paired with labels.

- **Data Dictionary:** The Choices, Calculations, OR Slider Labels
    column contains all option definitions in raw value, label format.

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** Always use the raw value in logic statements, never the display label. If the label is \'Strongly Agree\' and the raw value is 1, write \[field\]=\'1\' — not \[field\]=\'Strongly Agree\'. Labels can be changed by the project designer at any time; raw values are stable.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

# 4. Single-Choice Fields in Branching Logic

Single-choice fields store exactly one value — the raw value of the
selected option. Writing logic for them follows the standard atomic
statement pattern.

## 4.1 Supported Single-Choice Field Types

  ------------------ --------------------------------------- ---------------------
  **Field Type**     **Stored Value**                        **Logic Example**
  Radio button       Raw value of selected option            \[gender\]=\'1\'
  Dropdown           Raw value of selected option            \[country\]=\'US\'
  Yes / No           \'1\' = Yes, \'0\' = No                 \[consent\]=\'1\'
  True / False       \'1\' = True, \'0\' = False             \[eligible\]=\'1\'
  Slider             The numeric position value selected     \[pain\_score\]\>=7
  Calculated field   The numeric result of the calculation   \[bmi\]\>=25
  ------------------ --------------------------------------- ---------------------

## 4.2 Bonus: File Upload and Signature Fields

File Upload and Signature fields do not store a traditional value, but
you can use them in logic to check whether a file has been attached or a
signature captured:

+-------------------------------------------------------------------+
| \[consent\_form\]\<\>\'\' // True when a file has been uploaded   |
|                                                                   |
| \[signature\]\<\>\'\' // True when a signature has been captured  |
|                                                                   |
| \[consent\_form\]=\'\' // True when no file has been uploaded yet |
+-------------------------------------------------------------------+

You cannot compare the file contents — only the presence or absence of
the file.

---

# 5. Checkbox Fields in Branching Logic

Checkbox fields require a different syntax because they store data
differently from all other field types. Understanding this distinction
is essential for writing correct checkbox logic.

## 5.1 How Checkboxes Store Data

A checkbox field with N options creates N separate sub-variables in the
REDCap dataset — one per option. Each sub-variable stores only two
values:

- 1 — the option is checked (selected)

- 0 — the option is unchecked (default state)

Example: a checkbox field named \[conditions\] with three options:

+-----------------+
| 1, Diabetes     |
|                 |
| 2, Hypertension |
|                 |
| 3, Cancer       |
+-----------------+

This creates three sub-variables: \[conditions(1)\], \[conditions(2)\],
\[conditions(3)\]. Each is independently 0 or 1.

## 5.2 Checkbox Sub-Variable Syntax

To reference a specific checkbox option in logic, place the raw value of
that option inside parentheses within the variable name:

+----------------------------------------------------------------+
| Format: \[variable\_name(raw\_value)\]                         |
|                                                                |
| Examples:                                                      |
|                                                                |
| \[conditions(1)\]=\'1\' // Is the Diabetes option checked?     |
|                                                                |
| \[conditions(2)\]=\'1\' // Is the Hypertension option checked? |
|                                                                |
| \[conditions(3)\]=\'0\' // Is the Cancer option NOT checked?   |
+----------------------------------------------------------------+

## 5.3 Comparing Radio vs. Checkbox Syntax

  ------------------------------------------ ------------------ -------------------------------------------------------------------------------
  **Scenario**                               **Radio Button**   **Checkbox**
  Option with raw value 12 is selected       \[radio\]=12       \[checkbox(12)\]=\'1\'
  Option with raw value 12 is NOT selected   \[radio\]\<\>12    \[checkbox(12)\]=\'0\'
  Field has no selection (empty)             \[radio\]=\'\'     Not directly testable as a single expression — check each option separately
  ------------------------------------------ ------------------ -------------------------------------------------------------------------------

## 5.4 Practical Checkbox Logic Patterns

Show a follow-up field when at least one of several checkbox options is
checked:

+----------------------------------------------------------------------+
| \[conditions(1)\]=\'1\' or \[conditions(2)\]=\'1\' or                |
| \[conditions(3)\]=\'1\'                                              |
|                                                                      |
| // True when Diabetes OR Hypertension OR Cancer is checked           |
+----------------------------------------------------------------------+

Show a field only when a specific combination of checkboxes is checked:

+--------------------------------------------------------------+
| \[conditions(1)\]=\'1\' and \[conditions(2)\]=\'1\'          |
|                                                              |
| // True only when BOTH Diabetes AND Hypertension are checked |
+--------------------------------------------------------------+

Show a field when a specific option is explicitly NOT checked:

+----------------------------------------------------------------------+
| \[conditions(3)\]=\'0\'                                              |
|                                                                      |
| // True when Cancer is NOT checked (i.e., option is unchecked or     |
| never shown)                                                         |
+----------------------------------------------------------------------+

  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Warning:** Do not switch a checkbox field to a radio button field (or vice versa) after branching logic has been written that references it. The sub-variable syntax for checkboxes is incompatible with the single-value syntax for radio buttons. Any existing logic referencing that field will break and must be rewritten.
  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

---

# 6. Common Questions

**Q: How do I find the raw values for a field\'s options?**

**A:** Open the Codebook (RC-FD-05) and navigate to the field. The
Codebook displays all options in raw value, label format. Alternatively,
open the field in the Online Designer\'s edit dialog and check the
Choices section.

**Q: Does it matter whether I quote raw values in logic? For example,
\[gender\]=\'1\' vs \[gender\]=1?**

**A:** For numeric raw values, REDCap accepts both quoted and unquoted
forms. \[gender\]=\'1\' and \[gender\]=1 are functionally equivalent.
Using single quotes is recommended for consistency, especially when the
Data Dictionary may be edited in spreadsheet software.

**Q: Can I check whether none of the checkbox options are checked?**

**A:** Not directly with a single expression. You must check each option
individually: \[field(1)\]=\'0\' and \[field(2)\]=\'0\' and
\[field(3)\]=\'0\'. This evaluates to true only when all listed options
are unchecked.

**Q: A radio button option has the label \'Yes\' and raw value \'1\'.
Should I write \[field\]=\'Yes\' or \[field\]=\'1\'?**

**A:** Always use the raw value: \[field\]=\'1\'. Logic compares against
stored values, not display labels. Display labels can be changed at any
time; raw values are permanent.

**Q: Why can\'t I check whether a checkbox field has any checked options
by writing \[field\]\<\>\'\'?**

**A:** Unlike text fields and single-choice fields, checkbox fields do
not have a single stored value that represents \'something is
selected\'. Each option is a separate binary sub-variable. To check
whether any option is selected, you must OR together checks on each
sub-variable: \[field(1)\]=\'1\' or \[field(2)\]=\'1\' etc.

**Q: I changed a radio button field to a checkbox. Now my branching
logic is broken. How do I fix it?**

**A:** Any logic that used radio syntax (e.g., \[field\]=2) must be
rewritten in checkbox syntax (e.g., \[field(2)\]=\'1\'). Open each
affected field in the Online Designer, review the branching logic, and
update the syntax. The Data Dictionary can speed this up if many fields
are affected.

---

# 7. Common Mistakes & Gotchas

- Using the display label instead of the raw value:
    \[gender\]=\'Male\' will not work if \'Male\' is a label and \'1\'
    is the raw value. Always verify raw values in the Codebook before
    writing logic.

- Forgetting parentheses in checkbox syntax: \[conditions\]=1 is radio
    button syntax. For checkboxes, it must be \[conditions(1)\]=\'1\'.
    Without the parentheses and raw value, the logic will not reference
    any checkbox sub-variable.

- Switching field type after logic is written: changing a field from
    radio to checkbox (or vice versa) breaks all existing logic
    referencing that field. The syntax is incompatible. Plan field types
    carefully before data collection begins.

- Treating checkbox \'unchecked\' as empty: an unchecked checkbox
    option stores 0, not \'\' (empty). Testing \[field(1)\]=\'\' will
    not behave as expected. Use \[field(1)\]=\'0\' to test for
    unchecked.

- Assuming checkbox logic mirrors radio logic: the most common mistake
    for users familiar with radio buttons is writing checkbox logic
    without the sub-variable syntax. The field name alone does not refer
    to any single value for a checkbox field.

---

# 8. Related Articles

- RC-BL-02 — Syntax & Atomic Statements (prerequisite — covers
    operators, quotes, brackets)

- RC-BL-03 — Combining Logic Statements (AND, OR, parentheses ---
    often needed with checkbox logic)

- RC-BL-01 — Branching Logic Overview & Scope

- RC-FD-05 — Codebook (the fastest way to look up raw values for any
    field)

- RC-DE-02 — Basic Data Entry (explains how branching logic appears
    during data entry)

RC-BL-02

**Branching Logic -- Syntax & Atomic Statements**

  -------------------- ------------------------------------------------------------------------------------------------------------------------
  **Article ID**       RC-BL-02
  **Domain**           Branching Logic
  **Applies To**       All REDCap project types; requires Project Design and Setup rights
  **Prerequisite**     RC-BL-01 --- Branching Logic Overview & Scope
  **Version**          1.0
  **Last Updated**     2025
  **Author**           REDCap Support
  **Related Topics**   RC-BL-01 --- Overview; RC-BL-03 --- Combining Statements; RC-BL-04 --- Structured Fields; RC-FD-03 --- Data Dictionary
  -------------------- ------------------------------------------------------------------------------------------------------------------------

**1. Overview**

This article covers the REDCap logic syntax in detail --- the operators,
brackets, quotes, and boolean keywords that make up valid logic
expressions --- and explains how to construct an atomic logic statement:
the simplest, single-condition statement that forms the building block
of all branching logic.

**2. Key Concepts & Definitions**

**Atomic Logic Statement**

The simplest possible logic expression in REDCap. It always has exactly
three parts: a variable, an operator, and a comparison value. Example:
\[age\]\>=18.

**Variable Reference**

A reference to a REDCap field, written as the field\'s variable name
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
REDCap stores the coded option value --- not the display label --- in
the dataset. Logic statements must reference raw values, not labels.

**3. Syntax Language Reference**

**3.1 Math Operators**

REDCap supports standard arithmetic operators for use in calculated
fields and numeric comparisons. These operate on numbers only.

  -------------- ---------------- ---------------------------
  **Operator**   **Meaning**      **Example**
  \+             Addition         \[score\_a\]+\[score\_b\]
  \-             Subtraction      \[total\]-\[deductions\]
  \*             Multiplication   \[dose\]\*\[weight\]
  /              Division         \[total\]/\[count\]
  \^             Exponent         \[base\]\^2
  =              Equals           \[status\]=1
  -------------- ---------------- ---------------------------

**3.2 Comparison Operators**

Comparison operators are the most common operators in branching logic.
They compare a variable to a value and return true or false.

  -------------- -------------------------- ------------------
  **Operator**   **Meaning**                **Example**
  =              Equal to                   \[gender\]=\'1\'
  \<\>           Not equal to               \[status\]\<\>0
  \>             Greater than               \[age\]\>18
  \>=            Greater than or equal to   \[age\]\>=18
  \<             Less than                  \[bmi\]\<25
  \<=            Less than or equal to      \[bmi\]\<=25
  -------------- -------------------------- ------------------

**3.3 Quotation Marks**

Any comparison value that is not a number must be enclosed in quotation
marks. Both single and double quotes are accepted.

+----------------------------------------------------------+
| \[fav\_color\]=\"green\" // double quotes                |
|                                                          |
| \[fav\_color\]=\'green\' // single quotes --- equivalent |
|                                                          |
| \[email\]\<\>\"\" // empty string check (double quotes)  |
|                                                          |
| \[email\]\<\>\'\' // empty string check (single quotes)  |
+----------------------------------------------------------+

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Best Practice:** If you plan to edit your logic via the Data Dictionary in Excel or another spreadsheet program, use single quotes throughout. Excel interprets double quotes as part of its own formula syntax, which can corrupt logic statements during CSV import/export.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.4 Square Brackets \[ \] and Their Uses**

Square brackets are used to reference three types of identifiers in
REDCap logic:

  ------------------------------- -------------------------------- -----------------------------------------------------
  **What Is Referenced**          **Syntax**                       **Example**
  Regular field variable          \[variable\_name\]               \[first\_name\], \[dob\]
  Checkbox sub-variable           \[variable\_name(raw\_value)\]   \[conditions(3)\]
  Longitudinal event (advanced)   \[event\_name\]                  \[baseline\_arm\_1\] --- covered in advanced series
  Smart variable (advanced)       \[smart\_variable\_name\]        Covered in separate training
  ------------------------------- -------------------------------- -----------------------------------------------------

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Curly brackets { } are used exclusively by the Field Embedding feature and have no role in branching logic syntax. If you see curly brackets in a logic field, something has gone wrong.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**3.5 Boolean Operators**

Boolean operators join two or more logic statements together. REDCap
supports AND, OR, and NOT (expressed as \<\>). Both uppercase and
lowercase are accepted.

  ------------------ --------------------------------------------------------------------------- ------------------------------------------
  **Operator**       **Behavior**                                                                **Example**
  AND / and          Both statements must be true for the combined statement to be true          \[age\]\>=18 and \[consent\]=\'1\'
  OR / or            At least one statement must be true for the combined statement to be true   \[country\]=\'US\' or \[country\]=\'CA\'
  \<\> (not equal)   True when the variable does NOT equal the comparison value                  \[email\]\<\>\'\'
  ------------------ --------------------------------------------------------------------------- ------------------------------------------

Combining AND and OR in the same statement requires parentheses to
control evaluation order. See RC-BL-03 for full details.

**4. The Atomic Logic Statement**

Every logic statement --- no matter how complex --- is built from atomic
statements. An atomic statement always has exactly three parts:

  ---------------------- -------------------------------------------------------------------------- ---------------------------------------------
  **Part**               **What It Is**                                                             **Examples**
  1\. Variable           A reference to a field in the current record, written in square brackets   \[age\] \[consent\_date\] \[exclusion\_q3\]
  2\. Operator           Defines the comparison relationship                                        = \<\> \> \>= \< \<=
  3\. Comparison value   What the variable is being compared to                                     18 \'yes\' \[other\_var\] \'\'
  ---------------------- -------------------------------------------------------------------------- ---------------------------------------------

The comparison value can be one of the following types:

  --------------------------- --------------------------------------------- -------------------------
  **Comparison Value Type**   **Format**                                    **Example**
  Number                      No quotes needed (quotes also accepted)       \[age\]\>=18
  Text string                 Must be enclosed in single or double quotes   \[status\]=\'enrolled\'
  Empty / blank               Two quotes with nothing between them          \[email\]\<\>\'\'
  Another variable            Variable name in square brackets              \[email1\]=\[email2\]
  --------------------------- --------------------------------------------- -------------------------

**5. Worked Examples**

**Example 1 --- Equality: Show field only if age is exactly 18**

  ------------
  \[age\]=18
  ------------

The field is shown only when the value of \[age\] equals exactly 18. Any
other value hides the field.

**Example 2 --- Greater Than or Equal: Show field for adults**

  --------------
  \[age\]\>=18
  --------------

The field is shown when \[age\] is 18 or any higher number. The field is
hidden for values below 18.

**Example 3 --- Not Equal: Show field for any non-zero number of
pregnancies**

  --------------------------
  \[nr\_pregnancies\]\<\>0
  --------------------------

The field is shown when \[nr\_pregnancies\] is any value other than 0
(e.g., 1, 2, 3). Important: 0 (numeric zero) and \'\' (empty/blank) are
not the same thing. Zero is a data value; empty means no data has been
entered at all.

**Example 4 --- Empty Check: Show warning when email field is blank**

  -------------------
  \[email\]\<\>\'\'
  -------------------

The field is shown when \[email\] contains any value at all. It
disappears the moment the user types anything into \[email\]. This
pattern is commonly used to display warnings or reminders for fields
that have not yet been filled in.

**Example 5 --- Comparing Two Variables**

  -----------------------------------------
  \[email\_primary\]=\[email\_secondary\]
  -----------------------------------------

The field is shown when the value of \[email\_primary\] exactly matches
the value of \[email\_secondary\]. Useful for validating that two fields
have the same entry (e.g., email confirmation).

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** REDCap validates that your logic syntax is correct (valid operators, properly closed brackets, known variable names), but it does not validate whether the logic makes sense for your study. A statement like \[age\]=999 is syntactically valid but will never match any realistic data. Always test your logic against real or realistic test data.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Empty vs. Zero --- A Critical Distinction**

One of the most common logic errors in REDCap is treating an empty field
as equivalent to a field containing zero. They are not the same.

  ---------------- ----------------------------------------------------------------------------------------------- --------------------------------------
  **State**        **What It Means**                                                                               **How to Test For It**
  Empty / blank    No data has been entered into this field at all. The field has never been saved with a value.   \[field\]=\'\' (equals empty string)
  Zero (numeric)   The user actively entered the value 0 into a number field. Zero is a data value.                \[field\]=0 or \[field\]=\'0\'
  ---------------- ----------------------------------------------------------------------------------------------- --------------------------------------

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Note:** Using \[nr\_pregnancies\]\<\>0 will evaluate to true for both an empty field AND for values like 1, 2, 3. If you specifically want to test for a field that has been actively filled in with a non-zero number, combine conditions: \[nr\_pregnancies\]\<\>\'\' and \[nr\_pregnancies\]\<\>0.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**7. Common Questions**

**Q: Do I need to use quotes around numbers in logic statements?**

**A:** Not strictly. REDCap accepts numbers with or without quotes
(e.g., \[age\]=18 and \[age\]=\'18\' both work). However, wrapping
numbers in single quotes is considered best practice because it is
consistent and avoids ambiguity.

**Q: Are variable names in logic case-sensitive?**

**A:** No. Variable names in REDCap are always lowercase (REDCap
enforces this), and logic syntax treats them case-insensitively.
However, text string comparison values are case-sensitive.
\[status\]=\'Enrolled\' will not match a stored value of \'enrolled\'
(lowercase e).

**Q: Can I reference a field from a different record in my logic?**

**A:** No. Logic statements can only reference fields within the same
record. You cannot write logic that says \'show this field if the value
in record 2 is X\'. All variable references are scoped to the current
record.

**Q: Can I use a function like datediff() as the comparison value?**

**A:** Yes --- REDCap functions can be used in logic statements.
However, functions are an advanced topic outside the scope of this basic
series. See the dedicated functions training for details.

**Q: What happens if I reference a variable name that doesn\'t exist?**

**A:** The Online Designer\'s logic validator will flag the statement as
invalid and will not save it. In the Data Dictionary, an invalid
variable reference will cause an upload error. Always verify variable
names against the Codebook (RC-FD-05) before writing logic.

**8. Common Mistakes & Gotchas**

-   Comparing text without quotes: \[status\]=enrolled is invalid ---
    enrolled must be quoted as \'enrolled\'. Unquoted non-numeric values
    cause syntax errors.

-   Using double quotes in Excel-edited Data Dictionary files: Excel
    corrupts double-quoted strings in CSV files. Use single quotes
    (\'value\') instead of double quotes (\"value\") whenever the Data
    Dictionary will be edited in a spreadsheet program.

-   Treating empty as zero: an empty field and a field containing 0 are
    different states. Test for them separately when both matter to your
    logic.

-   Using curly brackets for variable references: curly brackets { } are
    for Field Embedding only. Variable references always use square
    brackets \[\]. Writing {variable} in a logic field will not work.

-   Not testing logic against realistic data: REDCap validates syntax,
    not meaning. A statement can be syntactically valid but logically
    impossible (e.g., a range where min \> max). Always run test records
    to confirm the field shows and hides as intended.

**9. Related Articles**

-   RC-BL-01 --- Branching Logic Overview & Scope (prerequisite)

-   RC-BL-03 --- Combining Logic Statements (AND, OR, parentheses)

-   RC-BL-04 --- Branching Logic for Structured Fields & Checkboxes

-   RC-FD-02 --- Online Designer (where branching logic is configured
    per field)

-   RC-FD-03 --- Data Dictionary (bulk logic editing via CSV)

-   RC-FD-05 --- Codebook (look up variable names and raw values when
    writing logic)

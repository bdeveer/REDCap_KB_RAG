RC-CALC-01

**Special Functions Reference**

| **Article ID** | RC-CALC-01 |
|---|---|
| **Domain** | Calculations & Special Functions |
| **Applies To** | All REDCap project types; functions are available wherever REDCap logic or calculations are used |
| **Prerequisite** | RC-BL-01 — Branching Logic: Overview & Scope |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-BL-02 — Branching Logic: Syntax & Atomic Statements; RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE; RC-PIPE-03 — Smart Variables Overview |

---

# 1. Overview

REDCap provides a library of built-in functions — called Special Functions — that can be used wherever logic or calculations are written in the platform. This includes branching logic, calculated fields, report filters, survey invitations, alerts, and the Data Quality module. Functions perform operations that go beyond simple comparisons: calculating the difference between two dates, extracting parts of a date, rounding numbers, manipulating text strings, and applying conditional logic. This article is a complete reference for all available Special Functions as of REDCap 16.1.3.

---

# 2. Key Concepts & Definitions

**Special Function**

A built-in operation in REDCap's logic and calculation syntax that takes one or more inputs (called parameters) and returns a value. Functions are identified by their name followed by parentheses containing the parameters — e.g., `datediff([date1], [date2], 'd')`.

**Parameter**

A value passed into a function that the function operates on. Parameters are separated by commas inside the parentheses. Some parameters are required; others are optional and have defaults when omitted.

**Return Value**

The value a function produces. Depending on the function, this may be a number, a date, a text string, or a boolean (true/false). In branching logic, functions that return a number are typically used inside a comparison statement (e.g., `datediff([dob], 'today', 'y') >= 18`). In calculated fields, the function's return value is stored directly.

**Boolean**

A value that is either true (1) or false (0). Several functions — primarily text and missing data functions — return a boolean. In branching logic, a function returning true will satisfy the condition; returning false will not.

**Haystack / Needle**

Terminology REDCap uses in text functions. The "haystack" is the larger text being searched; the "needle" is the text being looked for within it.

**Missing Data Code**

A project-defined code indicating that a value is intentionally absent (e.g., "UNK" for unknown). Missing Data Codes are configured in Project Setup under Additional Customizations. Several functions specifically handle these codes.

---

# 3. Where Special Functions Can Be Used

Special Functions work in any location in REDCap where logic or calculations are written:

| **Context** | **Typical Use** |
|---|---|
| Branching Logic | Use a function's return value as part of a show/hide condition |
| Calculated Fields | Use a function as the entire calculation expression |
| Report Filters | Filter records based on a function's result |
| Survey Invitations | Control invitation timing or eligibility using date/logic functions |
| Alerts & Notifications | Trigger or suppress alerts based on a function's result |
| Data Quality Module | Define custom data quality rules using function logic |
| Action Tags (@CALCTEXT, @CALCDATE) | Drive dynamic field population |

> **Note on piping:** You cannot pipe the choice label of a multiple choice field into a Special Function. Using the `:label` modifier (e.g., `[my_field:label]`) to pass a display label as a function parameter will not work. Use the raw field variable instead.

---

# 4. Conditional Function

## 4.1 if()

**Syntax:** `if(CONDITION, value_if_true, value_if_false)`

Evaluates a condition and returns one of two values depending on whether the condition is true or false. This is REDCap's equivalent of an if/then/else statement.

- If `CONDITION` evaluates as true, the first value is returned.
- If `CONDITION` evaluates as false, the second value is returned.

**Example:** `if([weight] > 100, 44, 11)` returns 44 if weight is greater than 100, otherwise returns 11.

`if()` can be nested inside other functions or used as a parameter within another `if()` to handle multiple conditions.

---

# 5. Date and DateTime Functions

## 5.1 datediff()

**Syntax:** `datediff([date1], [date2], "units", returnSignedValue)`

Calculates the difference between two dates or datetimes.

**Units options:**
- `'y'` — years (1 year = 365.2425 days)
- `'M'` — months (1 month = 30.44 days)
- `'d'` — days
- `'h'` — hours
- `'m'` — minutes
- `'s'` — seconds

The `returnSignedValue` parameter must be `true` or `false` (default: `false`). When `false`, the result is always positive regardless of which date is larger. When `true`, the result is negative if `date2` is earlier than `date1`.

You may use the literal `'today'` or `'now'` as either date parameter.

**Common use:** `datediff([date1], 'today', 'd')` — number of days between a field's date and today.

## 5.2 age_at_date()

**Syntax:** `age_at_date([date_of_birth], [other_date], returnDecimal)`

Calculates a person's age in years using their date of birth and another specified date. Returns an integer by default. To get a decimal value (e.g., 0.24 years for a newborn), add `true` as the third parameter. If datetime fields are provided, the time component is ignored — only the date portion is used.

## 5.3 dayoftheweek()

**Syntax:** `dayoftheweek([date])`

Returns an integer corresponding to the day of the week for a given date or datetime:
1 = Monday, 2 = Tuesday, 3 = Wednesday, 4 = Thursday, 5 = Friday, 6 = Saturday, 7 = Sunday.

You may use `'today'` or `'now'` as the date parameter.

## 5.4 year(), month(), day()

Extract individual components from a date or datetime field:

| **Function** | **Returns** | **Example** |
|---|---|---|
| `year([date])` | The year as a 4-digit number | `year([dob])` → 1985 |
| `month([date])` | The month as a number (1–12) | `month([visit_datetime])` → 3 |
| `day([date])` | The day of the month (1–31) | `day([visit_date])` → 15 |

You may use `'now'` or `'today'` (in quotes) instead of a field variable in any of these functions.

---

# 6. Numeric Functions

## 6.1 Rounding

| **Function** | **Behavior** | **Example** |
|---|---|---|
| `round(number, decimals)` | Rounds to nearest | `round(14.384, 1)` → 14.4 |
| `roundup(number, decimals)` | Always rounds up | `roundup(14.384, 1)` → 14.4 |
| `rounddown(number, decimals)` | Always rounds down | `rounddown(14.384, 1)` → 14.3 |

If the `decimals` parameter is omitted, it defaults to 0 (rounding to a whole number).

## 6.2 Mathematical Operations

| **Function** | **Description** | **Example** |
|---|---|---|
| `sqrt(number)` | Square root | `sqrt([height])` |
| `(number)^(exponent)` | Exponentiation | `(4)^(3)` → 64; `([weight]+43)^(2)` |
| `abs(number)` | Absolute value | `abs(-7.1)` → 7.1 |
| `exponential(number)` | e raised to the power of a number | `exponential(1)` → 2.718... |
| `log(number, base)` | Logarithm | `log(100, 10)` → 2; omit base for natural log |
| `mod(dividend, divisor)` | Remainder of integer division | `mod(10, 4)` → 2 |

> **Important:** For exponents, the surrounding parentheses on both the base and the exponent are required. `4^3` will not work — it must be `(4)^(3)`.

## 6.3 Aggregate Functions

These functions operate on a set of two or more values. Blank values are always ignored and excluded from the calculation.

| **Function** | **Description** | **Example** |
|---|---|---|
| `min(n1, n2, ...)` | Lowest value in the set | `min([score1], [score2], [score3])` |
| `max(n1, n2, ...)` | Highest value in the set | `max([score1], [score2], [score3])` |
| `mean(n1, n2, ...)` | Average of the set | `mean([score1], [score2], [score3])` |
| `median(n1, n2, ...)` | Median of the set | `median([score1], [score2], [score3])` |
| `sum(n1, n2, ...)` | Sum of the set | `sum([score1], [score2], [score3])` |
| `stdev(n1, n2, ...)` | Standard deviation of the set | `stdev([score1], [score2], [score3])` |

There is no limit to the number of values that can be passed into these functions.

> **sum() vs. the + operator:** `sum()` will produce a result even if some (or all) of the variables are blank — blank values are simply skipped. If you need a calculation that only fires when *all* variables are filled in, use the `+` operator instead: `[var1]+[var2]+[var3]`. With the `+` operator, if any variable is blank the entire expression returns blank, making incomplete data visible rather than silently partial.

## 6.4 Type-Checking Functions

| **Function** | **Returns true if...** |
|---|---|
| `isnumber(value)` | The value is an integer or floating-point decimal |
| `isinteger(value)` | The value is a whole number without decimals |

---

# 7. Missing Data Code Functions

These functions are only meaningful in projects where Missing Data Codes have been defined (Project Setup → Additional Customizations).

| **Function** | **Returns true if...** |
|---|---|
| `isblankormissingcode(value)` | The field is blank/null OR the value is any Missing Data Code |
| `isblanknotmissingcode(value)` | The field is blank/null AND the value is NOT a Missing Data Code |
| `ismissingcode(value)` | The value is any Missing Data Code |
| `hasmissingcode(value, 'codes')` | The value is a Missing Data Code AND matches one of the codes listed (comma-delimited string in the second parameter) |

**Example:** `hasmissingcode([age], 'NASK,NI,UNK')` returns true if `[age]` is one of those three specific codes.

---

# 8. Text Functions

> **Important constraint:** Text functions should not be used on date or datetime fields that use MDY or DMY date formatting. They work correctly on date fields using YMD formatting.

## 8.1 Searching Within Text

| **Function** | **Returns** | **Example** |
|---|---|---|
| `contains(haystack, needle)` | true if needle is found anywhere in haystack (case-insensitive) | `contains([name], "taylor")` |
| `not_contain(haystack, needle)` | true if needle is NOT found in haystack (case-insensitive) | `not_contain([name], "smith")` |
| `starts_with(haystack, needle)` | true if haystack begins with needle (case-insensitive) | `starts_with([name], "rob")` |
| `ends_with(haystack, needle)` | true if haystack ends with needle (case-insensitive) | `ends_with([name], "taylor")` |
| `find(needle, haystack)` | Position of needle in haystack (1-based); returns 0 if not found | `find('y', [last_name])` → 3 for "Taylor" |

## 8.2 Extracting and Manipulating Text

| **Function** | **Returns** | **Example** |
|---|---|---|
| `left(text, n)` | Leftmost n characters | `left([last_name], 3)` → "Tay" for "Taylor" |
| `right(text, n)` | Rightmost n characters | `right([last_name], 4)` → "ylor" for "Taylor" |
| `mid(text, start, n)` | n characters starting at position start (1-based) | `mid([last_name], 2, 3)` → "ayl" for "Taylor" |
| `length(text)` | Number of characters in the string | `length([last_name])` → 6 for "Taylor" |
| `trim(text)` | Removes leading and trailing spaces | `trim(' hello ')` → "hello" |
| `upper(text)` | Converts to uppercase | `upper('John Doe')` → "JOHN DOE" |
| `lower(text)` | Converts to lowercase | `lower('John Doe')` → "john doe" |
| `replace_text(haystack, search, replace)` | Replaces all occurrences of search with replace | `replace_text([field1], "Taylor", "Harris")` |

## 8.3 Combining Text

| **Function** | **Returns** | **Example** |
|---|---|---|
| `concat(text, text, ...)` | Joins all items into one string | `concat([first_name], ' ', [last_name])` → "Rob Taylor" |
| `concat_ws(separator, text, text, ...)` | Joins items with a separator between each; skips empty values | `concat_ws(" and ", [veggie1], [veggie2], "Tomatoes")` → "Peas and Carrots and Tomatoes" |

---

# 9. Practical Examples

| **Goal** | **Expression** |
|---|---|
| Days between a date field and today | `datediff([date1], 'today', 'd')` |
| Person's age in whole years | `age_at_date([date_of_birth], [other_date])` |
| BMI from metric values (cm, kg), 1 decimal | `round(([weight]*10000)/(([height])^(2)), 1)` |
| BMI from English values (lb, in), 1 decimal | `round(([weight]/(([height])^(2))*703), 1)` |
| Strip a prefix+dash from record name (e.g., '4890-2318' → '2318') | `mid([record-name], find('-', [record-name])+1, length([record-name])-find('-', [record-name])+1)` |
| Convert first + last name to username format ('john_doe') | `lower(concat(trim([first_name]), '_', trim([last_name])))` |
| Add leading zeros to an integer (e.g., '7' → '007') | `right(concat('00', [my_integer]), 3)` |

---

# 10. Common Questions

**Q: Where can I access the Special Functions list in REDCap?**

A: Open the Online Designer and click into any field's branching logic or calculated field editor. The Logic Editor toolbar includes a "Special Functions" button that opens the complete reference list. It is also accessible from the Codebook page.

**Q: Can I use datediff() in branching logic, not just calculated fields?**

A: Yes. Any Special Function can be used in branching logic. The function's return value is used as part of a comparison — for example, `datediff([visit_date], 'today', 'd') > 30` will evaluate as true or false and control field visibility accordingly.

**Q: What's the difference between datediff() and age_at_date()?**

A: `datediff()` is a general-purpose date subtraction function that works in any units (days, months, years, hours, etc.) and can return signed or unsigned values. `age_at_date()` is specifically designed to calculate a person's age and correctly handles calendar-accurate age calculation (e.g., whether a birthday has passed in a given year). For calculating age, use `age_at_date()`. For other date differences, use `datediff()`.

**Q: Why do my aggregate functions (sum, mean, etc.) give unexpected results?**

A: Blank values are silently excluded from all aggregate calculations. If a field has no value, it is not counted — so `mean([a], [b], [c])` with only `[a]` and `[b]` filled in will return the average of just those two values, not divide by 3. This is intentional behavior. Use `isblankormissingcode()` in branching logic to handle fields where blank values need special treatment.

**Q: What's the difference between sum() and just adding variables together with +?**

A: `sum([a], [b], [c])` will return a result even if some variables are blank — blanks are skipped and the remaining values are totaled. By contrast, `[a]+[b]+[c]` returns blank if *any* of the variables is blank. Use `sum()` when partial totals are acceptable. Use `+` when you want the result to be blank until all inputs are filled in.

**Q: Can I nest functions inside other functions?**

A: Yes. REDCap functions can be nested to any reasonable depth. For example, `round(datediff([dob], 'today', 'y'), 0)` rounds the result of datediff, and `lower(concat(trim([first_name]), '_', trim([last_name])))` nests trim, concat, and lower together. Parentheses must be balanced.

**Q: Can I use 'today' or 'now' in date functions?**

A: Yes. The literals `'today'` and `'now'` (in single quotes) can be used in `datediff()`, `dayoftheweek()`, `year()`, `month()`, and `day()` instead of a field variable. `'today'` resolves to the current date; `'now'` resolves to the current date and time.

**Q: Do text functions work on date fields?**

A: Only on date fields using YMD formatting. Text functions should not be used on date or datetime fields formatted as MDY or DMY — the results will be unreliable. If you need to extract parts of a date, use `year()`, `month()`, or `day()` instead.

**Q: What is the difference between contains() and find()?**

A: `contains()` returns true or false and is used in branching logic or boolean conditions. `find()` returns the position (a number) of the needle within the haystack — useful when you need to know *where* in a string something appears, such as finding the position of a dash to then use with `mid()`.

---

# 11. Common Mistakes & Gotchas

**Forgetting parentheses around both the base and exponent.** For exponentiation, `(base)^(exponent)` is required. Writing `4^3` without the surrounding parentheses will not calculate correctly. Both the base and the exponent must each be wrapped in their own parentheses: `(4)^(3)`.

**Using `:label` as a function parameter.** It is not possible to pass the display label of a multiple choice field into a Special Function using the `:label` modifier (e.g., `contains([field:label], 'value')`). Only the raw stored value of a field can be passed into functions. Use the field variable directly without any modifier.

**Expecting blank fields to affect aggregate results.** `sum()`, `mean()`, `min()`, `max()`, `median()`, and `stdev()` all silently skip blank values. If a field is unanswered, it is excluded from the calculation entirely — it does not count as zero. If zero is the intended value for unanswered fields, that must be handled separately (e.g., using `if()`). For `sum()` specifically: if you need the total to remain blank until *all* inputs are filled in, use the `+` operator instead (`[var1]+[var2]+[var3]`), which returns blank as soon as any operand is blank.

**Using text functions on MDY/DMY date fields.** Functions like `left()`, `right()`, `find()`, and `contains()` should not be used on date or datetime fields with MDY or DMY formatting. The string representation of the date differs from what the function expects. Use `year()`, `month()`, and `day()` for date component extraction.

**Expecting datediff() to return whole years accurately for age.** `datediff()` with units `'y'` uses 365.2425 days as one year, which is an approximation. For accurate age-in-years (i.e., whether a birthday has actually passed), use `age_at_date()` instead.

**Misreading log() base behavior.** `log(number, base)` — if the base is omitted or not numeric, it defaults to base *e* (natural log), not base 10. To get a base-10 log, you must explicitly write `log([value], 10)`.

---

# Related Articles

- RC-BL-01 — Branching Logic: Overview & Scope
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements
- RC-BL-03 — Branching Logic: Combining Statements
- RC-AT-09 — Action Tags: @CALCTEXT & @CALCDATE
- RC-PIPE-03 — Smart Variables Overview
- RC-ALERT-01 — Alerts & Notifications Setup

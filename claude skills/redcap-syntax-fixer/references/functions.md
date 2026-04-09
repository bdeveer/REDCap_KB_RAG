# REDCap Special Functions Reference

All functions available in REDCap as of version 16.1.3. Use this when checking whether a function name is valid and whether the argument count is correct.

---

## Conditional

| Function | Signature | Args | Returns |
|---|---|---|---|
| `if()` | `if(condition, value_if_true, value_if_false)` | 3 required | Same type as the return values |

`if()` can be nested. All three arguments are required — omitting the false branch is a syntax error.

---

## Date and DateTime

| Function | Signature | Args | Returns | Notes |
|---|---|---|---|---|
| `datediff()` | `datediff(date1, date2, 'unit')` or `datediff(date1, date2, 'unit', returnSigned)` | 3 required, 4th optional | Number | `returnSigned` is `true` or `false` (default: `false`). Without it, result is always positive. |
| `age_at_date()` | `age_at_date(date_of_birth, other_date)` or `age_at_date(date_of_birth, other_date, returnDecimal)` | 2 required, 3rd optional | Number (years) | `returnDecimal=true` gives fractional years. Time component of datetime fields is ignored. |
| `dayoftheweek()` | `dayoftheweek(date)` | 1 required | Number (1=Mon … 7=Sun) | Accepts `'today'` or `'now'` |
| `year()` | `year(date)` | 1 required | Number (4-digit year) | Accepts `'today'` or `'now'` |
| `month()` | `month(date)` | 1 required | Number (1–12) | Accepts `'today'` or `'now'` |
| `day()` | `day(date)` | 1 required | Number (1–31) | Accepts `'today'` or `'now'` |

**Unit strings for `datediff()` and `@CALCDATE` — case-sensitive:**

| Unit string | Meaning |
|---|---|
| `'y'` | Years (1 year = 365.2425 days — approximation; use `age_at_date()` for accurate age) |
| `'M'` | Months (capital M — 1 month = 30.44 days) |
| `'d'` | Days |
| `'h'` | Hours |
| `'m'` | Minutes (lowercase m — easy to confuse with `'M'` for months) |
| `'s'` | Seconds |

⚠️ `'M'` (months) vs `'m'` (minutes) is a frequent mistake. Both are accepted without error — the wrong unit will silently produce wrong results.

**`'today'` and `'now'`:** These literals can be used instead of a field variable in any date function. They resolve to the server's current date/time, not the user's local clock.

---

## Numeric — Rounding

| Function | Signature | Args | Returns | Notes |
|---|---|---|---|---|
| `round()` | `round(number, decimals)` | 1 required, 2nd optional (defaults to 0) | Number | Standard rounding |
| `roundup()` | `roundup(number, decimals)` | 1 required, 2nd optional (defaults to 0) | Number | Always rounds away from zero |
| `rounddown()` | `rounddown(number, decimals)` | 1 required, 2nd optional (defaults to 0) | Number | Always rounds toward zero |

---

## Numeric — Mathematical

| Function | Signature | Args | Returns | Notes |
|---|---|---|---|---|
| `sqrt()` | `sqrt(number)` | 1 required | Number | |
| `abs()` | `abs(number)` | 1 required | Number | Absolute value |
| `exponential()` | `exponential(number)` | 1 required | Number | e^number |
| `log()` | `log(number, base)` | 1 required, 2nd optional | Number | Omitting base → natural log (base e), NOT base 10. For base-10: `log([x], 10)` |
| `mod()` | `mod(dividend, divisor)` | 2 required | Number | Remainder of integer division |
| `^` (exponent) | `(base)^(exponent)` | N/A — operator | Number | **Both base and exponent must each be wrapped in their own parentheses.** `[x]^2` is wrong; `([x])^(2)` is correct. |

---

## Numeric — Aggregate (operate on a set of values; blank values are silently skipped)

| Function | Signature | Args | Returns |
|---|---|---|---|
| `sum()` | `sum(n1, n2, ...)` | 2+ required | Number |
| `mean()` | `mean(n1, n2, ...)` | 2+ required | Number |
| `median()` | `median(n1, n2, ...)` | 2+ required | Number |
| `stdev()` | `stdev(n1, n2, ...)` | 2+ required | Number |
| `min()` | `min(n1, n2, ...)` | 2+ required | Number |
| `max()` | `max(n1, n2, ...)` | 2+ required | Number |

⚠️ **Blank values are excluded silently.** `mean([a], [b], [c])` with only `[a]` filled in returns the value of `[a]` alone, not `[a]/3`. This differs from `+` arithmetic: `[a]+[b]+[c]` returns blank the moment any variable is blank.

---

## Type-Checking

| Function | Signature | Returns true if… |
|---|---|---|
| `isnumber()` | `isnumber(value)` | The value is an integer or decimal |
| `isinteger()` | `isinteger(value)` | The value is a whole number |

---

## Missing Data Code Functions

These are only meaningful in projects where Missing Data Codes have been configured (Project Setup → Additional Customizations).

| Function | Signature | Returns true if… |
|---|---|---|
| `isblankormissingcode()` | `isblankormissingcode(value)` | Field is blank OR value is any Missing Data Code |
| `isblanknotmissingcode()` | `isblanknotmissingcode(value)` | Field is blank AND NOT a Missing Data Code |
| `ismissingcode()` | `ismissingcode(value)` | Value is any Missing Data Code |
| `hasmissingcode()` | `hasmissingcode(value, 'codes')` | Value matches one of the listed codes (comma-delimited in second arg) |

---

## Text — Searching

| Function | Signature | Returns |
|---|---|---|
| `contains()` | `contains(haystack, needle)` | true/false — case-insensitive |
| `not_contain()` | `not_contain(haystack, needle)` | true/false — case-insensitive |
| `starts_with()` | `starts_with(haystack, needle)` | true/false — case-insensitive |
| `ends_with()` | `ends_with(haystack, needle)` | true/false — case-insensitive |
| `find()` | `find(needle, haystack)` | Number — 1-based position; 0 if not found |

⚠️ Note argument order for `find()`: needle first, haystack second (opposite of `contains()`).

---

## Text — Extracting and Manipulating

| Function | Signature | Returns |
|---|---|---|
| `left()` | `left(text, n)` | First n characters |
| `right()` | `right(text, n)` | Last n characters |
| `mid()` | `mid(text, start, n)` | n characters starting at position start (1-based) |
| `length()` | `length(text)` | Character count |
| `trim()` | `trim(text)` | String with leading/trailing spaces removed |
| `upper()` | `upper(text)` | Uppercase string |
| `lower()` | `lower(text)` | Lowercase string |
| `replace_text()` | `replace_text(haystack, search, replace)` | String with all occurrences of search replaced |

⚠️ Text functions should not be used on date/datetime fields with MDY or DMY formatting. Use `year()`, `month()`, `day()` for date component extraction instead.

---

## Text — Combining

| Function | Signature | Returns |
|---|---|---|
| `concat()` | `concat(text, text, ...)` | All items joined into one string (including blanks) |
| `concat_ws()` | `concat_ws(separator, text, text, ...)` | Items joined with separator; blank values are skipped |

---

## Quick Reference: Required Argument Counts

| Function | Min args | Max args |
|---|---|---|
| `if()` | 3 | 3 |
| `datediff()` | 3 | 4 |
| `age_at_date()` | 2 | 3 |
| `dayoftheweek()` | 1 | 1 |
| `year()` / `month()` / `day()` | 1 | 1 |
| `round()` / `roundup()` / `rounddown()` | 1 | 2 |
| `sqrt()` / `abs()` / `exponential()` | 1 | 1 |
| `log()` | 1 | 2 |
| `mod()` | 2 | 2 |
| `sum()` / `mean()` / `median()` / `stdev()` / `min()` / `max()` | 2 | unlimited |
| `isnumber()` / `isinteger()` | 1 | 1 |
| `isblankormissingcode()` / `isblanknotmissingcode()` / `ismissingcode()` | 1 | 1 |
| `hasmissingcode()` | 2 | 2 |
| `contains()` / `not_contain()` / `starts_with()` / `ends_with()` | 2 | 2 |
| `find()` | 2 | 2 |
| `left()` / `right()` | 2 | 2 |
| `mid()` | 3 | 3 |
| `length()` / `trim()` / `upper()` / `lower()` | 1 | 1 |
| `replace_text()` | 3 | 3 |
| `concat()` | 2 | unlimited |
| `concat_ws()` | 3 | unlimited |
| `@CALCDATE()` | 3 | 3 |

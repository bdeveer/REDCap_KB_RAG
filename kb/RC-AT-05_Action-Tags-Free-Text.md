RC-AT-05

**Action Tags — Free Text**

| **Article ID** | RC-AT-05 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **REDCap Version** | 15.9.1 |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-06 — Autofill Action Tags; RC-FD-02 — Online Designer; RC-DE-05 — Field Validations |

---

# 1. Overview

This article covers action tags that modify the behavior of text boxes and notes boxes — REDCap's two free-text field types. These tags control input visibility, enforce length constraints, enable rich text formatting, and display placeholder hints. None of the tags in this article alter the stored data itself; they only affect how the field accepts or presents input.

---

# 2. Key Concepts & Definitions

**Text Box**

A single-line free-text field. Supports optional validation types (number, date, email, etc.) and optional minimum/maximum bounds. Most action tags in this article apply specifically to text boxes.

**Notes Box**

A multi-line free-text field intended for longer responses. Some action tags in this article work on notes boxes; others are text box only.

**Validation**

A type constraint applied to a text box that limits what values are considered valid (e.g., integer, date_mdy, email). Certain action tags in this article only function when a relevant validation is present.

---

# 3. @PASSWORDMASK

Obscures text entered into a text box by replacing visible characters with dots, similar to a password field. The data is stored normally and is fully visible in reports and data exports — only the on-screen display during data entry is masked.

**Applies to:** Text box only. Has no effect on notes boxes.

**Common uses:** Social Security numbers, dates of birth, passcodes, and other values where shoulder-surfing is a concern.

**Syntax** (no parameters):
```
@PASSWORDMASK
```

> **Important:** `@PASSWORDMASK` is a display feature, not a security or encryption feature. The data is stored in plain text and is accessible in reports, the Codebook, and exports.

---

# 4. @FORCE-MINMAX

Text boxes with a numeric or date validation can define minimum and/or maximum bounds. By default, REDCap shows a warning when a user enters an out-of-range value but allows them to dismiss it and continue. `@FORCE-MINMAX` converts that warning into a hard block — users cannot save or advance until the entered value falls within the defined range.

**Applies to:** Text box with a validation that includes a minimum, a maximum, or both. Has no effect on fields without min/max bounds or on notes boxes.

**Common uses:** Age ranges, medication dosages, lab result ranges, or any numeric field with a known allowable window.

**Syntax** (no parameters):
```
@FORCE-MINMAX
```

> **Setup note:** Min/max bounds are defined in the *Edit Field* menu for the text box, in the validation section. Both the validation type and the bounds must be set before `@FORCE-MINMAX` has any effect.

---

# 5. @WORDLIMIT

Sets a maximum number of words that can be entered in a text or notes box. REDCap counts words by the spaces between them: "garage door" counts as two words; "garage-door" or "garagedoor" counts as one. The remaining word count is displayed below the field as the user types.

**Applies to:** Text box and notes box.

**Syntax:**
```
@WORDLIMIT=10
```
or equivalently:
```
@WORDLIMIT="10"
```

> **Note:** `@WORDLIMIT` and `@CHARLIMIT` cannot be used on the same field. Use one or the other.

> **Note:** This limit is enforced only during browser-based data entry and survey submission. It does not apply to values written via the API or the Data Import Tool.

---

# 6. @CHARLIMIT

Sets a maximum number of characters that can be entered in a text or notes box. All characters count toward the limit, including spaces and special characters. The remaining character count is displayed below the field.

**Applies to:** Text box and notes box.

**Syntax:**
```
@CHARLIMIT=30
```
or equivalently:
```
@CHARLIMIT="30"
```

> **Note:** `@CHARLIMIT` and `@WORDLIMIT` cannot be used on the same field.

> **Note:** Enforced only during browser-based data entry and surveys; not enforced during data import.

---

# 7. @RICHTEXT

Adds a rich text editing toolbar to a notes box, enabling common formatting options such as bold, italic, underline, and bulleted lists — similar to a basic word processor. Without this tag, notes boxes accept only plain text.

**Applies to:** Notes box only. Has no effect on plain text boxes.

**Common uses:** Open-ended feedback fields, comment boxes, or any question where respondents may benefit from structured formatting in their response.

**Syntax** (no parameters):
```
@RICHTEXT
```

> **Best practice:** Use left alignment for the notes box (set via *Custom Alignment* in the Edit Field menu). Left-aligned notes boxes display the full rich text toolbar. Right-aligned notes boxes display a more compact toolbar variant. Left alignment also gives respondents more horizontal space.

---

# 8. @PLACEHOLDER

Displays hint text inside an empty text or notes box. The hint appears in grey and disappears the moment the user starts typing. The placeholder text is never stored — if the field is submitted empty, no value is saved.

**Applies to:** Text box and notes box.

**Common uses:** Date format reminders (e.g., "D-M-Y"), examples of expected input (e.g., "e.g. Pig, Goat, Cow"), or brief inline instructions.

**Syntax:**
```
@PLACEHOLDER='Please be brief'
```

> **Note:** Single and double quotes cannot be used within the placeholder text, as REDCap uses these characters to delimit the value.

> **Note:** `@PLACEHOLDER` only displays hint text. It does not set a default value. To pre-fill a value that is saved when the field is submitted, use `@DEFAULT` (see RC-AT-06).

---

# 9. Common Questions

**Q: Does @PASSWORDMASK encrypt the data?**

**A:** No. The data is stored in plain text. `@PASSWORDMASK` only masks the display during data entry in the browser. The value is fully readable in reports, exports, and the Codebook.

**Q: Can @WORDLIMIT and @CHARLIMIT be used together on the same field?**

**A:** No. These two tags are mutually exclusive. Choose the constraint type that best fits your use case.

**Q: Does @FORCE-MINMAX work if no validation is set?**

**A:** No. `@FORCE-MINMAX` requires a validation type with a defined minimum or maximum. If the field has no validation or no bounds, the tag has no effect.

**Q: Will the rich text formatting from @RICHTEXT be preserved in exports?**

**A:** It depends on the export format. Rich text content is stored as HTML in the database. Some export formats (e.g., CSV) will include the raw HTML markup. Consider whether downstream analysis tools can handle HTML content before enabling `@RICHTEXT`.

**Q: If I use @PLACEHOLDER and the respondent leaves the field blank, will the placeholder text be saved?**

**A:** No. `@PLACEHOLDER` is purely cosmetic — it never saves. A blank field submission results in no stored value.

---

# 10. Common Mistakes & Gotchas

**Treating @PASSWORDMASK as a security control.** The tag masks the display but does not encrypt or protect the stored data. Use REDCap's user rights and export restrictions for actual data security.

**Using @WORDLIMIT and @CHARLIMIT together.** These tags conflict. Only one can be active on a field at a time; REDCap will not generate an error, but the behavior will be unpredictable.

**Expecting @FORCE-MINMAX to work without a validation.** The tag requires a validation type with min/max bounds defined. Without it, the warning behavior is unchanged.

**Confusing @PLACEHOLDER with @DEFAULT.** `@PLACEHOLDER` shows hint text but never saves. `@DEFAULT` pre-fills a real value that is saved on submission. Use `@PLACEHOLDER` for display hints; use `@DEFAULT` when you need a saved default.

---

# 11. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-06 — Autofill Action Tags: `@DEFAULT` and `@SETVALUE` for pre-filling saved values
- RC-DE-05 — Field Validations: configuring validation types and min/max bounds required by `@FORCE-MINMAX`
- RC-FD-02 — Online Designer: where action tags and field settings are configured

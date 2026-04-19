RC-AT-05

**Free Text Action Tags**

| **Article ID** | RC-AT-05 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Overview; RC-AT-06 — Autofill Tags; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers action tags that constrain, enhance, or modify the behavior of text boxes and notes boxes: `@PASSWORDMASK`, `@FORCE-MINMAX`, `@WORDLIMIT`, `@CHARLIMIT`, `@RICHTEXT`, and `@PLACEHOLDER`.

---

# 2. @PASSWORDMASK

Obscures text entry by replacing displayed characters with dots, similar to a password field. The underlying data is stored normally and is fully visible in reports, exports, and the Codebook — only the on-screen display is masked.

**Applies to:** Text box only.

**Syntax:**
```
@PASSWORDMASK
```

**Use case:** Social Security numbers, dates of birth, passcodes — any sensitive value where you want to prevent shoulder-surfing during data entry.

---

# 3. @FORCE-MINMAX

Text boxes with numeric or date validation can define minimum and/or maximum bounds. By default, REDCap warns users about out-of-range values but allows them to proceed. `@FORCE-MINMAX` makes that warning a hard block — users cannot save or advance until an in-range value is entered.

**Applies to:** Text box with a validation that defines a minimum, maximum, or both.

**Syntax:**
```
@FORCE-MINMAX
```

**Use case:** Age ranges in pediatric studies, medication dosages with strict limits, or any measurement with a known allowable range.

---

# 4. @WORDLIMIT

Limits the maximum number of words in a text or notes box. REDCap counts words by spaces between them ("garage door" = 2 words; "garage-door" = 1 word). The remaining word count is displayed below the field.

> **Note:** `@WORDLIMIT` and `@CHARLIMIT` are mutually exclusive. Use one or the other.

> **Note:** Enforced only during data entry and surveys, not during API or Data Import Tool uploads.

**Applies to:** Text box and notes box.

**Syntax:**
```
@WORDLIMIT=10
```

---

# 5. @CHARLIMIT

Limits the maximum number of characters in a text or notes box. All characters count (letters, spaces, punctuation). The remaining character count is displayed below the field.

> **Note:** Mutually exclusive with `@WORDLIMIT`.

> **Note:** Not enforced during data import.

**Applies to:** Text box and notes box.

**Syntax:**
```
@CHARLIMIT=30
```

---

# 6. @RICHTEXT

Adds a rich text toolbar to a notes box, enabling bold, italic, bullets, and other formatting options. Without this tag, notes boxes accept only plain text.

**Applies to:** Notes box only.

**Syntax:**
```
@RICHTEXT
```

**Best practice:** Use left alignment for notes boxes (set via *Custom Alignment* in the Edit Field menu). Left-aligned notes boxes display the full toolbar; right-aligned boxes show a compact version. Left alignment also provides more horizontal space.

---

# 7. @PLACEHOLDER

Displays hint text inside an empty field. The hint appears in grey and disappears when the user starts typing. The placeholder text is never saved — it is purely a UI hint.

**Applies to:** Text box and notes box.

**Syntax:**
```
@PLACEHOLDER='Please be brief'
```

> **Note:** Single and double quotes cannot be used within the placeholder text.

> **Note:** To pre-fill a value that is saved when the field is submitted, use `@DEFAULT` or `@SETVALUE` instead (see RC-AT-06).

**Use case:** Date format reminders, suggested answer formats, or brief instructions visible within the field.

---

# 8. Common Mistakes

**Using `@WORDLIMIT` and `@CHARLIMIT` on the same field.** These are mutually exclusive; only one can be active.

**Expecting `@PASSWORDMASK` to encrypt data.** It only masks the display — data is stored and exported in plain text.

**Confusing `@PLACEHOLDER` with `@DEFAULT`.** `@PLACEHOLDER` is a hint that is never saved; `@DEFAULT` pre-fills with a value that will be saved.

**Expecting limits to apply to imported data.** `@WORDLIMIT` and `@CHARLIMIT` are enforced only during browser-based data entry and surveys, not during API or import uploads.

---

# 9. Related Articles

- RC-AT-01 — Action Tags Overview
- RC-AT-06 — Autofill Action Tags
- RC-FD-02 — Online Designer

---
id: RC-AT-05
title: Free Text Action Tags
domain: Action Tags
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — action
  tag behaviour checked against source code; pages not re-captured
prerequisites:
- 'RC-AT-01 — Action Tags: Overview'
version: '1.1'
last_updated: 2026-11
related:
- id: RC-AT-01
  title: 'Action Tags: Overview'
- id: RC-AT-06
  title: Autofill Action Tags
- id: RC-FD-02
  title: Online Designer
tags:
- action tags
synonyms:
- '@PASSWORDMASK action tag'
- '@WORDLIMIT action tag'
- '@CHARLIMIT action tag'
- '@RICHTEXT action tag'
- '@PLACEHOLDER action tag'
- '@FORCE-MINMAX action tag'
- how do i mask text entry like a password
- how do i limit characters or words in a text box
- add placeholder text to a field
- enable a rich text editor on a notes box
---

# 1. Overview

This article covers action tags that constrain, enhance, or modify the behavior of text boxes and notes boxes: `@PASSWORDMASK`, `@FORCE-MINMAX`, `@WORDLIMIT`, `@CHARLIMIT`, `@RICHTEXT`, and `@PLACEHOLDER`.

---

# 2. @PASSWORDMASK

Obscures text entry by replacing displayed characters with dots, similar to a password field. The underlying data is stored normally and shows unmasked everywhere outside the entry field itself — in PDFs, reports, exports and anywhere the value is piped. Only the on-screen display in the text box is masked.

**Applies to:** Text box only. `@PASSWORDMASK` cannot be combined on the same field with `@LATITUDE`, `@LONGITUDE` or `@CONSENT-VERSION`; use only one of these tags per field.

**Syntax:**
```
@PASSWORDMASK
```

**Use case:** Social Security numbers, dates of birth, passcodes — any sensitive value where you want to prevent shoulder-surfing during data entry.

---

# 3. @FORCE-MINMAX

Text boxes with numeric or date validation can define minimum and/or maximum bounds. By default, REDCap warns users about out-of-range values but allows them to proceed. `@FORCE-MINMAX` makes that warning a hard block — users cannot save or advance until an in-range value is entered.

Unlike the other tags in this article, `@FORCE-MINMAX` is also enforced on API and Data Import Tool uploads: out-of-range values are rejected. Missing data codes are still accepted.

**Applies to:** Text box with a validation that defines a minimum, maximum, or both.

**Syntax:**
```
@FORCE-MINMAX
```

**Use case:** Age ranges in pediatric studies, medication dosages with strict limits, or any measurement with a known allowable range.

---

# 4. @WORDLIMIT

Limits the maximum number of words in a text or notes box. REDCap counts words by spaces between them ("garage door" = 2 words; "garage-door" = 1 word). The remaining word count is displayed below the field.

> **Note:** Use `@WORDLIMIT` or `@CHARLIMIT`, not both. If a field has both, `@CHARLIMIT` wins and `@WORDLIMIT` is ignored.

> **Note:** Enforced only during data entry and surveys, not during API or Data Import Tool uploads. Text pasted into the field that goes over the limit is cut to the limit.

**Applies to:** Text box and notes box.

**Syntax:**
```
@WORDLIMIT=10
```

---

# 5. @CHARLIMIT

Limits the maximum number of characters in a text or notes box. All characters count (letters, spaces, punctuation). The remaining character count is displayed below the field.

> **Note:** Use instead of `@WORDLIMIT`, not alongside it. If a field has both, `@CHARLIMIT` wins.

> **Note:** Not enforced during API or Data Import Tool uploads. Text pasted into the field that goes over the limit is cut to the limit.

**Applies to:** Text box and notes box.

**Syntax:**
```
@CHARLIMIT=30
```

---

# 6. @RICHTEXT

Adds a rich text toolbar to a notes box, enabling bold, italic, bullets, and other formatting options. Without this tag, notes boxes accept only plain text.

The formatted text is stored as HTML. Data exports therefore contain the HTML tags (for example `<p>` and `<strong>`), while PDFs of the instrument show the text without the tags. Plan for this if the data will be analysed outside REDCap. Image upload in the editor is not available on public surveys.

**Applies to:** Notes box only.

**Syntax:**
```
@RICHTEXT
```

**Best practice:** Use left alignment for notes boxes (set via *Custom Alignment* in the Edit Field menu). Left-aligned notes boxes display the full toolbar; right-aligned boxes show a compact version. Left alignment also provides more horizontal space.

---

# 7. @PLACEHOLDER

Displays hint text inside an empty field. The hint appears in grey and disappears when the user starts typing. The placeholder text is never saved — it is purely a UI hint.

**Applies to:** Text box, notes box, and drop-down fields set to auto-complete.

**Syntax:**
```
@PLACEHOLDER='Please be brief'
```

> **Note:** The placeholder text cannot contain the same quote character that wraps it, but it can contain the other one. To use an apostrophe, wrap the text in double quotes: `@PLACEHOLDER="Patient's initials"`.

> **Note:** The placeholder text supports piping, so it can show a value from another field.

> **Note:** To pre-fill a value that is saved when the field is submitted, use `@DEFAULT` or `@SETVALUE` instead (see [RC-AT-06 — Autofill Action Tags](RC-AT-06_Action-Tags-Autofill.md)).

**Use case:** Date format reminders, suggested answer formats, or brief instructions visible within the field.

---

# 8. Common Mistakes

**Using `@WORDLIMIT` and `@CHARLIMIT` on the same field.** Only one can be active: `@CHARLIMIT` wins and `@WORDLIMIT` is ignored.

**Expecting `@PASSWORDMASK` to encrypt data.** It only masks the display in the entry field — data is stored in plain text and shows unmasked in PDFs, reports, exports and piping.

**Confusing `@PLACEHOLDER` with `@DEFAULT`.** `@PLACEHOLDER` is a hint that is never saved; `@DEFAULT` pre-fills with a value that will be saved.

**Expecting limits to apply to imported data.** `@WORDLIMIT` and `@CHARLIMIT` are enforced only during browser-based data entry and surveys, not during API or import uploads. `@FORCE-MINMAX` is the exception: it is enforced on imports too.

**Expecting clean text from `@RICHTEXT` in exports.** The value is stored as HTML, so exported data includes the HTML tags.

---

# 9. Related Articles

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-AT-06 — Autofill Action Tags](RC-AT-06_Action-Tags-Autofill.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)

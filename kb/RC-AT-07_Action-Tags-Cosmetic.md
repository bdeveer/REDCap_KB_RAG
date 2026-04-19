RC-AT-07

**Cosmetic Action Tags**

| **Article ID** | RC-AT-07 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Overview; RC-AT-05 — Free Text Tags; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers action tags that adjust the visual display of certain field types without changing the underlying data: `@HIDEBUTTON`, `@INLINE`, and `@INLINE-PREVIEW`.

---

# 2. @HIDEBUTTON

Text boxes with a date or date-time validation automatically display a **Today** or **Now** button that fills the current date/time with a single click. `@HIDEBUTTON` removes that button.

**Applies to:** Text box with date or date-time validation only.

**Syntax:**
```
@HIDEBUTTON
```

**Use case:** Date of birth fields, historical dates, or any date field where "today" is unlikely to be the correct answer and the button would be misleading.

---

# 3. @INLINE

Renders an uploaded file directly within the form, inline with other fields, instead of just showing the file name.

**Supported formats:** PDF, JPG, JPEG, GIF, PNG, TIF, BMP. DICOM and other specialized formats are not supported.

**Applies to:** File upload fields only.

`@INLINE` supports three forms:

## 3.1 @INLINE without parameters

Displays the file at 100% width of the containing area:

```
@INLINE
```

## 3.2 @INLINE with one parameter

Sets the display width; height scales proportionally:

```
@INLINE(50)
```

Use a whole number for pixels or append `%` for a percentage of screen width:

```
@INLINE(50%)
```

## 3.3 @INLINE with two parameters

Sets both width and height independently (may distort aspect ratio):

```
@INLINE(50,100)
@INLINE(50%,100%)
```

> **Recommendation:** Test `@INLINE` thoroughly before deploying. Results vary based on file type, file dimensions, and the viewing device.

---

# 4. @INLINE-PREVIEW

A compromise between default (filename only) and `@INLINE` (always displayed). Adds a toggle button to the file upload field: a magnifier icon shows the file; an × icon hides it.

**Applies to:** File upload fields and descriptive fields.

**Syntax:**
```
@INLINE-PREVIEW
```

**Use case:** Sensitive images or large PDFs that should be viewable on demand but not always visible.

---

# 5. Displaying Files via Piping

A file upload field's inline display can also be referenced elsewhere in a form using a piped reference with the `:inline` qualifier:

```
[logo:inline]
```

This displays the file inline as if `@INLINE` (without parameters) were applied, without requiring the tag on the upload field itself.

---

# 6. Common Mistakes

**Not testing `@INLINE` across devices.** Pixel-based sizing looks very different on high-density smartphone screens versus standard monitors. Always test on representative devices.

**Using `@INLINE` with unsupported file formats.** DICOM and other specialized formats are not supported. The file can still be uploaded and downloaded — it simply cannot be rendered inline.

**Expecting `@INLINE` to work on files that are purely text.** Text files (TXT, CSV) cannot be displayed inline; only image and PDF formats are supported.

---

# 7. Related Articles

- RC-AT-01 — Action Tags Overview
- RC-AT-05 — Free Text Action Tags
- RC-FD-02 — Online Designer

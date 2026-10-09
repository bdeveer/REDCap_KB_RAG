

**Cosmetic Action Tags**

| **Article ID** | [RC-AT-07 — Cosmetic Action Tags](RC-AT-07_Action-Tags-Cosmetic.md) |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version (`@HIDEDATEPICKER` requires 17.5.0+) |
| **Verified Against** | REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)|
| **Version** | 1.1 |
| **Last Updated** | 2026-10 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md); [RC-AT-05 — Free Text Action Tags](RC-AT-05_Action-Tags-Free-Text.md); [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) |
| **Synonyms** | @HIDEBUTTON action tag; @HIDEDATEPICKER action tag; how do i hide the calendar icon on a date field; remove the date picker from a date or time field; @INLINE action tag; @INLINE-PREVIEW action tag; how do i remove the today now button from a date field; how do i show an uploaded file inline on the form; display image or pdf inline instead of a download link; cosmetic action tags for field display |

---

## 1. Overview

This article covers action tags that adjust the visual display of certain field types without changing the underlying data: `@HIDEBUTTON`, `@HIDEDATEPICKER`, `@INLINE`, and `@INLINE-PREVIEW`.

---

## 2. @HIDEBUTTON

Text boxes with a date or date-time validation automatically display a **Today** or **Now** button that fills the current date/time with a single click. `@HIDEBUTTON` removes that button.

**Applies to:** Text box with date or date-time validation only.

**Syntax:**
```
@HIDEBUTTON
```

**Use case:** Date of birth fields, historical dates, or any date field where "today" is unlikely to be the correct answer and the button would be misleading.

---

## 3. @HIDEDATEPICKER

Text boxes with date, time or date-time validation display a calendar/clock picker icon to the right of the field. `@HIDEDATEPICKER` hides that icon, so the value must be typed.

**Applies to:** Text box with date, time or date-time validation.

**Syntax:**
```
@HIDEDATEPICKER
```

`@HIDEDATEPICKER` does **not** hide the **Today**/**Now** button. To remove both, use the two tags together:

```
@HIDEDATEPICKER @HIDEBUTTON
```

**Use case:** Dates that are easier to type than to pick — such as a date of birth decades in the past — or fields where the picker's default to the current month invites careless entry.

> **Version caveat (below 17.5.0):** `@HIDEDATEPICKER` does not exist before REDCap 17.5.0 (Standard). On older instances, and on the 17.3.x LTS line, the tag is ignored and the picker icon still shows. The same release also replaced the picker icon with a Font Awesome icon, so the icon looks different on 17.5.0+.

---

## 4. @INLINE

Renders an uploaded file directly within the form, inline with other fields, instead of just showing the file name.

**Supported formats:** PDF, JPG, JPEG, GIF, PNG, TIF, BMP. DICOM and other specialized formats are not supported.

**Applies to:** File upload fields only.

`@INLINE` supports three forms:

### 4.1 @INLINE without parameters

Displays the file at 100% width of the containing area:

```
@INLINE
```

### 4.2 @INLINE with one parameter

Sets the display width; height scales proportionally:

```
@INLINE(50)
```

Use a whole number for pixels or append `%` for a percentage of screen width:

```
@INLINE(50%)
```

### 4.3 @INLINE with two parameters

Sets both width and height independently (may distort aspect ratio):

```
@INLINE(50,100)
@INLINE(50%,100%)
```

> **Recommendation:** Test `@INLINE` thoroughly before deploying. Results vary based on file type, file dimensions, and the viewing device.

---

## 5. @INLINE-PREVIEW

A compromise between default (filename only) and `@INLINE` (always displayed). Adds a toggle button to the file upload field: a magnifier icon shows the file; an × icon hides it.

**Applies to:** File upload fields and descriptive fields.

**Syntax:**
```
@INLINE-PREVIEW
```

**Use case:** Sensitive images or large PDFs that should be viewable on demand but not always visible.

---

## 6. Displaying Files via Piping

A file upload field's inline display can also be referenced elsewhere in a form using a piped reference with the `:inline` qualifier:

```
[logo:inline]
```

This displays the file inline as if `@INLINE` (without parameters) were applied, without requiring the tag on the upload field itself.

---

## 7. Common Questions

**Q: Can I use @INLINE with a video or audio file?**

**A:** No. `@INLINE` supports only static image and PDF formats (JPG, PNG, GIF, TIF, BMP, PDF). Video and audio files cannot be displayed inline; only the filename will show.

**Q: What is the difference between @INLINE and @INLINE-PREVIEW?**

**A:** `@INLINE` displays the file immediately and always (at 100% width by default or a specified size). `@INLINE-PREVIEW` adds a toggle button so the file is hidden by default and displayed on demand. Use `@INLINE-PREVIEW` for sensitive images or large files you want respondents to view only if needed.

**Q: If I use @HIDEBUTTON on a date field, can respondents still manually enter a date?**

**A:** Yes. `@HIDEBUTTON` only hides the "Today" or "Now" button; respondents can still type or use a date picker to enter a date manually (depending on the field validation and browser support).

**Q: What is the difference between @HIDEBUTTON and @HIDEDATEPICKER?**

**A:** They hide different controls. `@HIDEBUTTON` hides the **Today**/**Now** button; `@HIDEDATEPICKER` (17.5.0+) hides the calendar/clock picker icon. Neither stops the respondent typing a value. Use both together to leave only the text box.

**Q: Can I use @INLINE to display a PDF that is dynamically piped from another field?**

**A:** No. `@INLINE` displays a file upload field's content based on what is already uploaded to that specific field. You cannot pipe a filename from another field. To reference a file from elsewhere, use the piped syntax `[field:inline]` on a descriptive field instead.

**Q: Does @INLINE work on mobile devices or in the REDCap Mobile App?**

**A:** `@INLINE` works on mobile browsers, but rendering and sizing may vary significantly depending on the device screen size and the file format. Test on representative devices. The tag has no effect in the REDCap Mobile App unless the Mobile App displays files in a context that supports inline rendering (functionality varies by app version).

---

## 8. Common Mistakes

**Not testing `@INLINE` across devices.** Pixel-based sizing looks very different on high-density smartphone screens versus standard monitors. Always test on representative devices.

**Using `@INLINE` with unsupported file formats.** DICOM and other specialized formats are not supported. The file can still be uploaded and downloaded — it simply cannot be rendered inline.

**Expecting `@HIDEDATEPICKER` to remove the Today/Now button.** It hides only the picker icon. Add `@HIDEBUTTON` as well if the button should go too.

**Using `@HIDEDATEPICKER` on an instance below 17.5.0.** The tag is silently ignored — REDCap does not warn about unrecognised action tags. Check the instance version before relying on it, particularly on the LTS line.

**Expecting `@INLINE` to work on files that are purely text.** Text files (TXT, CSV) cannot be displayed inline; only image and PDF formats are supported.

---

## 9. Related Articles

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-AT-05 — Free Text Action Tags](RC-AT-05_Action-Tags-Free-Text.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)

RC-AT-07

**Action Tags — Cosmetic**

| **Article ID** | RC-AT-07 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **REDCap Version** | 15.9.1 |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-FD-02 — Online Designer; RC-DE-05 — Field Validations |

---

# 1. Overview

This article covers action tags that affect how certain field types are displayed or behave at the form level: hiding the auto-populated date/time button on date fields, rendering uploaded files inline, tracking download counts for file attachments, and suppressing the missing data code icon for specific fields.

---

# 2. @HIDEBUTTON

Text boxes with a date or date-time validation automatically display a **Today** or **Now** button. When clicked, this button fills the field with the current date (or date and time) without the user having to type or use the date picker. `@HIDEBUTTON` removes this button from the field.

**Applies to:** Text box with a date or date-time validation. Has no effect on other field types or on text boxes without date validation.

**Common uses:** Date of birth fields, historical dates, or any date field where "today" is rarely the correct answer and the button could mislead users or encourage lazy data entry.

**Syntax** (no parameters):
```
@HIDEBUTTON
```

---

# 3. @INLINE

File upload fields display only the name of the uploaded file by default. `@INLINE` renders the uploaded file — an image or PDF — directly within the form, immediately above the download link.

**Applies to:** File upload fields only.

**Supported file formats:** PDF, JPG, JPEG, GIF, PNG, TIF, BMP. DICOM and other specialized formats are not supported.

> **Recommendation:** Test `@INLINE` thoroughly before deploying. Display results vary based on file type, file dimensions, and the device used to view the form. This tag can significantly alter the look and feel of an instrument.

## 3.1 @INLINE Without Parameters

Displays the file at 100% width of the containing area. Images maintain their native aspect ratio. PDFs display at a default height of 300 pixels.

```
@INLINE
```

## 3.2 @INLINE With One Parameter — Width

Sets the display width of the file. Height scales proportionally to maintain the aspect ratio.

**Pixel width** — sets an absolute maximum width in pixels. Actual appearance may vary by screen density (e.g., high-DPI mobile screens vs. standard monitors):
```
@INLINE(50)
```

**Percentage width** — sets the width relative to the screen width. The image always scales to the defined proportion of the available space:
```
@INLINE(50%)
```

## 3.3 @INLINE With Two Parameters — Width and Height

Sets both width and height independently. This overrides the aspect ratio and may distort images. Use with caution.

All four combinations of pixels and percentages are valid:

```
@INLINE(50,100)
@INLINE(50%,100)
@INLINE(50,100%)
@INLINE(50%,100%)
```

The first value is width; the second is height.

## 3.4 Displaying Uploaded Files via Piping

An uploaded file can also be displayed inline elsewhere in a project — in other fields or instruments — by appending the `:inline` qualifier to a pipe expression rather than using `@INLINE` on the upload field itself.

For a file upload field with variable name `logo`:

```
[logo:inline]
```

This renders the file using the same default display as `@INLINE` without parameters. For more information on piping see the piping training course.

---

# 4. @INLINE-PREVIEW

A compromise between the default display (filename only) and `@INLINE` (always visible). Adds a toggle button next to the file upload field: a magnifier icon shows the file; an × icon hides it again. The file is hidden by default and only displayed when the user clicks the toggle.

**Applies to:** File upload fields and descriptive fields.

**Common uses:** Sensitive images or large PDFs that should be viewable on demand but do not need to occupy space at all times. Also useful for forms where multiple file uploads would create visual clutter if all rendered inline by default.

**Syntax** (no parameters):
```
@INLINE-PREVIEW
```

---

# 5. @DOWNLOAD-COUNT

Automatically increments a counter field by 1 whenever someone downloads the file attached to a specified File Upload field or Descriptive field. This provides a lightweight way to track how many times a file has been accessed without external analytics.

**Applies to:** The `@DOWNLOAD-COUNT` tag is placed on a **Text Box or Notes Box** field (the counter field). The parameter specifies the variable name of the File Upload or Descriptive field whose downloads are being tracked.

**Syntax:**
```
@DOWNLOAD-COUNT(my_upload_field)
```

Replace `my_upload_field` with the variable name of the field whose downloads you want to count. The counter increments when the download link is clicked on a data entry form, survey page, or report.

**Behavior details:**
- If the counter field currently has no value or contains a non-integer, its value is set to `1` on the first download.
- Each subsequent download increments the existing integer by 1.
- Downloads are counted regardless of who performs them — staff via the form, survey respondents, or anyone viewing a report.

> **Context requirement:** The counter field and the File Upload/Descriptive field must be in the same context. In a longitudinal project, they must be on the same event. In a repeating instrument, they must be on the same repeating instrument.

> **Inline PDF limitation:** If a PDF is displayed inline via `@INLINE` or `@INLINE-PREVIEW`, users may download it using the browser's built-in download arrow (which is generated by the browser, not by REDCap). These browser-native downloads are **not** counted by `@DOWNLOAD-COUNT` — only clicks on REDCap's own file download link are tracked.

---

# 6. @NOMISSING

Disables the **missing data code** feature for a specific field. When a project has custom missing data codes configured (set up in Additional Customizations on the Project Setup page), REDCap displays an **M** icon next to each eligible field, allowing users to enter a missing data code instead of a real value. Adding `@NOMISSING` to a field hides that M icon for that field, effectively opting it out of the missing data code workflow.

**Applies to:** Any field type in a project where missing data codes have been enabled. Has no effect in projects where missing data codes are not configured.

**Common uses:** Fields that should never receive a missing data code — for example, auto-populated fields (`@USERNAME`, `@TODAY`, calculated fields) where a missing data code would be meaningless or disruptive.

**Syntax** (no parameters):
```
@NOMISSING
```

---

# 7. Common Questions

**Q: Does @HIDEBUTTON affect the date picker widget as well as the Today/Now button?**

**A:** No. `@HIDEBUTTON` only removes the Today/Now quick-fill button. The calendar/date picker widget that appears when the user clicks into the field is unaffected.

**Q: Can @INLINE display DICOM files or other medical imaging formats?**

**A:** No. `@INLINE` supports only PDF, JPG, JPEG, GIF, PNG, TIF, and BMP. DICOM and other formats can still be uploaded and downloaded — they simply cannot be rendered inline in the browser.

**Q: What is the difference between @INLINE and @INLINE-PREVIEW?**

**A:** `@INLINE` always renders the uploaded file directly in the form as soon as the page loads. `@INLINE-PREVIEW` hides the file by default and lets the user toggle visibility with a button click.

**Q: Does @INLINE work on descriptive fields?**

**A:** No. `@INLINE` works only on file upload fields. For descriptive fields, use `@INLINE-PREVIEW` or embed an image using HTML in the field label.

**Q: Does @DOWNLOAD-COUNT track downloads when a file is viewed inline via @INLINE?**

**A:** Only partially. Clicks on REDCap's download link are counted. Downloads triggered by the browser's built-in download button (visible when a PDF is displayed inline) are not counted, because that action is handled by the browser, not REDCap.

**Q: Does @NOMISSING affect data exports or reports?**

**A:** No. `@NOMISSING` only removes the M icon from the data entry interface. It has no effect on how data is exported or displayed in reports.

---

# 8. Common Mistakes & Gotchas

**Applying @HIDEBUTTON to a field without a date validation.** The tag has no effect without a date or date-time validation on the text box.

**Using @INLINE without testing on representative devices.** Pixel-based sizing looks very different on high-density screens (e.g., smartphones) compared to standard monitors. Percentage-based sizing adapts to screen width but may still produce unexpected results depending on content type. Always test before deploying.

**Setting two-parameter @INLINE values that distort aspect ratio.** When both width and height are specified, REDCap does not maintain the original aspect ratio. Images can appear stretched or compressed. Use single-parameter `@INLINE` unless a specific width-height ratio is intentional.

**Expecting @INLINE to work on DICOM files.** The REDCap browser interface cannot render DICOM images inline regardless of how `@INLINE` is configured. This is a browser limitation, not a REDCap configuration issue.

**Placing @DOWNLOAD-COUNT on the wrong field.** The tag goes on the counter (Text or Notes) field, not on the File Upload field. A common mistake is placing it on the upload field itself, where it has no effect.

**Using @NOMISSING in a project without missing data codes.** The tag has no effect if the project has not configured custom missing data codes in Additional Customizations. Check the Project Setup page to confirm the feature is enabled.

---

# 9. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-DE-05 — Field Validations: date and date-time validations required by `@HIDEBUTTON`
- RC-FD-02 — Online Designer: where action tags and field settings are configured

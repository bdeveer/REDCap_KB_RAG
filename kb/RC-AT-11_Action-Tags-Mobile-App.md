RC-AT-11

**Action Tags — Mobile App Action Tags**

| **Article ID** | RC-AT-11 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | REDCap Mobile App only; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview; REDCap Mobile App must be installed and project initialized |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-02 — @HIDDEN & @READONLY |

---

# 1. Overview

REDCap provides three action tags designed exclusively for use in the **REDCap Mobile App**. These tags extend mobile data collection with barcode/QR scanning, automatic capture of the mobile user's identity, and syncing of uploaded images from the server to the app.

> **Mobile App only.** All three tags in this article function only within the REDCap Mobile App. They have no effect on browser-based data entry forms or survey pages.

---

# 2. @APPUSERNAME-APP

Sets a field's value to the **app username** of the person currently using the mobile app. The app username is the credential used to log in to the mobile app, which may differ from the user's REDCap server username.

This is the mobile equivalent of `@USERNAME` (which captures the REDCap server username). Use `@APPUSERNAME-APP` when you need to identify who entered data in the field via the app specifically.

**Applies to:** Text Box fields.

**Syntax** (no parameters):
```
@APPUSERNAME-APP
```

> **Note:** If the same field has `@USERNAME` and `@APPUSERNAME-APP`, they will conflict. Use the appropriate tag for the context in which data will be collected (browser vs. mobile app), or use `@USERNAME` for browser-based entry and keep `@APPUSERNAME-APP` on a separate field.

---

# 3. @BARCODE-APP

Enables the device's camera to capture a **barcode or QR code** value and store it in the tagged field. When the user taps the field in the mobile app, a scan button appears. Activating it opens the camera; once a code is detected, the decoded value is stored in the field automatically.

**Applies to:** Text Box fields.

**Syntax** (no parameters):
```
@BARCODE-APP
```

**Common uses:** Scanning participant wristbands, specimen labels, drug vials, or equipment tags to capture identifiers without manual typing — reducing transcription errors in field or clinical settings.

> **Camera permission required.** The device must grant the REDCap Mobile App permission to access the camera before scanning can occur. If permission is denied, the scan button will not function.

---

# 4. @SYNC-APP

When a project is initialized in the REDCap Mobile App and a File Upload or Signature field has `@SYNC-APP`, any image files uploaded to a record on the REDCap server will be sent down to the app so they are viewable when editing that record offline.

Without this tag, images uploaded via the browser are not automatically pushed to the app — users in the field would see the field but not the image content.

**Applies to:** File Upload fields and Signature fields.

**Syntax** (no parameters):
```
@SYNC-APP
```

**Common uses:** Making reference images (e.g., body maps, consent forms, photo IDs) available to field staff who collect data offline via the app.

> **Storage consideration:** Syncing images increases the amount of data downloaded to each device during synchronization. In projects with many large files, this can slow sync times and consume significant device storage.

---

# 5. Common Questions

**Q: Do mobile app action tags do anything on browser-based forms or surveys?**

**A:** No. `@APPUSERNAME-APP`, `@BARCODE-APP`, and `@SYNC-APP` are all silently ignored when a form is opened in a web browser.

**Q: What is the difference between @USERNAME and @APPUSERNAME-APP?**

**A:** `@USERNAME` captures the REDCap server username (the login used on the REDCap website). `@APPUSERNAME-APP` captures the username used to log in to the mobile app, which is set up separately and may be different. In some configurations both usernames are the same, but they are not guaranteed to match.

**Q: Can @BARCODE-APP store any type of barcode format?**

**A:** The REDCap Mobile App supports standard 1D barcodes (UPC, EAN, Code 128, etc.) and 2D codes (QR codes, Data Matrix). The decoded value is stored as a text string regardless of format.

---

# 6. Common Mistakes & Gotchas

**Expecting mobile app tags to work in the browser.** These tags have no effect outside the REDCap Mobile App. Confirm that data collection actually occurs via the app before adding these tags.

**Using @SYNC-APP on non-image file types.** The tag is designed for image and signature files. Behavior with other file types (PDFs, Word documents, etc.) may be unpredictable or files may not sync as expected.

**Not accounting for increased sync time with @SYNC-APP.** In projects with many records and large attached images, enabling sync can significantly extend the time required to synchronize the app with the server, particularly on slow connections.

---

# 7. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-02 — @HIDDEN-APP and @READONLY-APP: hiding and locking fields specifically in the mobile app
- RC-AT-06 — Autofill Action Tags: `@USERNAME` for capturing the server username on browser-based forms

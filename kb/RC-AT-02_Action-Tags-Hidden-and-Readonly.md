RC-AT-02

**Action Tags — @HIDDEN & @READONLY**

| **Article ID** | RC-AT-02 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-03 — Radio/Dropdown Action Tags; RC-BL-01 — Branching Logic Overview; RC-FD-02 — Online Designer |

---

# 1. Overview

This article covers the two most widely used action tags in REDCap: `@HIDDEN`, which hides a field from view, and `@READONLY`, which displays a field but prevents edits. Both tags have a family of situational variants that restrict their effect to specific contexts (survey mode, form mode, mobile app, PDF). Understanding how to combine these variants — and how they interact with each other — allows fine-grained control over what users see and can edit across different access modes.

---

# 2. Key Concepts & Definitions

**Variant**

A version of an action tag that applies its effect only in a specific context. For example, `@HIDDEN-SURVEY` hides a field only when the instrument is opened as a survey, while the base `@HIDDEN` tag hides it everywhere.

**Combining Action Tags**

Multiple action tags can be placed in the same *Action Tags / Field Annotation* box, separated by spaces. The effects of all listed tags apply simultaneously.

---

# 3. @HIDDEN

`@HIDDEN` hides the target field across the entire REDCap interface — data entry forms, surveys, and the mobile app. The field continues to exist and any stored data is retained, but users cannot see or interact with it directly.

> **Important:** `@HIDDEN` overrides any branching logic attached to the same field. A field tagged with `@HIDDEN` is always hidden, regardless of branching logic conditions.

**Common uses:**

- **Preserving deprecated fields.** When a field is no longer needed but its historical data should be retained, `@HIDDEN` removes it from view without deleting it or its data.
- **Hiding calculated fields.** Score calculations can be hidden so that users cannot see intermediate values during data entry.
- **Honeypot fields.** A hidden field can detect automated survey bots. Real participants cannot interact with the field; bots typically do, filling it in and flagging themselves.

## 3.1 @HIDDEN Variants

The base `@HIDDEN` tag hides a field everywhere. The following variants restrict hiding to a specific context:

| Tag | Where it hides the field |
|---|---|
| `@HIDDEN` | Everywhere (data entry forms, surveys, mobile app) |
| `@HIDDEN-SURVEY` | Only when the instrument is opened as a survey |
| `@HIDDEN-FORM` | Only when the instrument is opened by a user in REDCap (not survey mode) |
| `@HIDDEN-APP` | Only in the REDCap Mobile App |
| `@HIDDEN-PDF` | Only in PDF exports generated from the instrument |

> **Note:** `@HIDDEN-PDF` is the only way to exclude a field from generated PDFs. The base `@HIDDEN` tag does not affect PDF output.

## 3.2 Combining @HIDDEN Variants

Multiple `@HIDDEN` variants can be placed on the same field, separated by spaces. For example, to hide a field in surveys and in the mobile app but leave it visible during normal form-based data entry:

```
@HIDDEN-SURVEY @HIDDEN-APP
```

---

# 4. @READONLY

`@READONLY` displays a field normally but prevents users from modifying its value. Read-only fields appear slightly greyed out to signal that they cannot be edited. This is useful when a value needs to be visible for reference but should not be changed by the person entering data.

**Common uses:**

- **Protecting pre-loaded data.** Records pre-populated via data import (e.g., contact information) can be locked so users cannot accidentally alter values that drive survey invitations or other automations.
- **Displaying auto-filled values.** A field populated by an autofill action tag can be shown for reference without allowing manual edits.

## 4.1 @READONLY Variants

Like `@HIDDEN`, `@READONLY` has context-specific variants:

| Tag | Where the field becomes read-only |
|---|---|
| `@READONLY` | Everywhere |
| `@READONLY-SURVEY` | Only when the instrument is opened as a survey |
| `@READONLY-FORM` | Only when the instrument is opened by a user in REDCap |
| `@READONLY-APP` | Only in the REDCap Mobile App |

## 4.2 Combining @READONLY Variants

Multiple `@READONLY` variants can be combined on the same field. For example, to make a field read-only in survey mode and in the mobile app, but editable when a staff member opens the form in REDCap:

```
@READONLY-SURVEY @READONLY-APP
```

---

# 5. Combining @HIDDEN and @READONLY Variants

The two tag families can be mixed freely on the same field. This enables nuanced configurations that behave differently depending on who is accessing the instrument and how.

**Example — Contact information visible to staff, hidden from survey respondents and PDFs:**

A record is pre-loaded with a participant's email address. Study staff should be able to see it (but not edit it). Survey respondents should not see it at all. It should not appear in printed PDFs.

```
@READONLY-FORM @HIDDEN-SURVEY @HIDDEN-PDF
```

> **Caution:** Using the base `@HIDDEN` tag alongside `@READONLY-FORM` will override the read-only behavior entirely — the field will be hidden for everyone, not just survey respondents. Use the situational variants to achieve fine-grained control.

---

# 6. Common Questions

**Q: Does @HIDDEN prevent a field's data from appearing in reports or exports?**

**A:** No. `@HIDDEN` only hides the field in the data entry and survey interface. The field's value still appears in reports, the Codebook, and data exports. Use user rights and export settings to restrict data access.

**Q: Can @READONLY be bypassed via API or data import?**

**A:** Yes. `@READONLY` and `@READONLY-FORM` affect only the browser-based data entry interface. They do not block writes from the API or the Data Import Tool. This can be intentional — for example, allowing automated processes to update a field that staff should not be able to edit manually.

**Q: Does @HIDDEN-PDF affect the Compact PDF (survey PDF) as well as the standard instrument PDF?**

**A:** Yes. `@HIDDEN-PDF` applies to all PDF exports generated from the instrument, regardless of format.

**Q: What is the difference between @HIDDEN and branching logic for hiding a field?**

**A:** Branching logic hides a field conditionally — based on values entered in other fields — and clears the hidden field's value when it is hidden. `@HIDDEN` hides a field unconditionally and does not clear the stored value. Use branching logic when visibility should change dynamically during data entry. Use `@HIDDEN` when a field should always be hidden (or hidden only in a specific context).

---

# 7. Common Mistakes & Gotchas

**Using `@HIDDEN` to hide a field from PDFs.** The base `@HIDDEN` tag does not affect PDF output. Use `@HIDDEN-PDF` explicitly.

**Mixing `@HIDDEN` with `@READONLY-FORM`.** If you want staff to see a field as read-only while hiding it from survey respondents, use `@READONLY-FORM @HIDDEN-SURVEY`, not `@HIDDEN`. A bare `@HIDDEN` overrides everything and hides the field from staff as well.

**Assuming `@READONLY` prevents all writes.** `@READONLY` blocks manual edits in the browser. It does not block API writes or data imports. Design accordingly if you need a true data integrity lock.

**Expecting `@HIDDEN` to interact with branching logic.** `@HIDDEN` overrides branching logic on the same field. If a field has both `@HIDDEN` and branching logic, it will always be hidden — the branching logic condition is never evaluated.

---

# 8. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-03 — Radio/Dropdown Action Tags: `@HIDECHOICE`, `@SHOWCHOICE`, and related tags
- RC-AT-06 — Autofill Action Tags: `@READONLY` is commonly combined with autofill tags
- RC-BL-01 — Branching Logic Overview: how `@HIDDEN` interacts with branching logic
- RC-DE-02 — Basic Data Entry: how hidden and read-only fields appear during data entry

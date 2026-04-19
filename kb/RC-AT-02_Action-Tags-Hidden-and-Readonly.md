RC-AT-02

**@HIDDEN & @READONLY — Visibility Control**

| **Article ID** | RC-AT-02 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Overview; RC-AT-03 — Radio/Dropdown Tags; RC-FD-02 — Online Designer; RC-BL-01 — Branching Logic Overview |

---

# 1. Overview

This article covers the most commonly used action tags: `@HIDDEN` and `@READONLY`, along with their situational variants. These tags control field visibility and editability across different REDCap contexts.

---

# 2. @HIDDEN — Hiding Fields

`@HIDDEN` hides a field from view. The field and its data still exist in the project; users simply cannot see or interact with it.

> **Important:** `@HIDDEN` overrides branching logic. A field tagged with `@HIDDEN` is always hidden, regardless of any branching logic conditions.

**Common uses:**

- Preserving deprecated fields without deleting historical data
- Hiding calculated fields so users cannot see intermediate values
- Creating honeypot fields in surveys to detect automated bot submissions

## 2.1 Situational Variants

| Tag | Where it hides |
|---|---|
| `@HIDDEN` | Everywhere (form, survey, Mobile App, PDFs) |
| `@HIDDEN-SURVEY` | Only when accessed as a survey |
| `@HIDDEN-FORM` | Only when accessed as a data entry form |
| `@HIDDEN-APP` | Only in the REDCap Mobile App |
| `@HIDDEN-PDF` | Only in PDF exports (the only way to exclude from PDFs) |

## 2.2 Combining Variants

Multiple variants can be combined. For example, to hide a field in surveys and in the Mobile App:

```
@HIDDEN-SURVEY @HIDDEN-APP
```

---

# 3. @READONLY — Making Fields Non-Editable

`@READONLY` displays a field normally but prevents any changes to its value. Read-only fields appear slightly greyed out.

**Common uses:**

- Displaying pre-loaded contact information that staff can review but not edit
- Showing calculated or piped values for reference without allowing modification

## 3.1 Situational Variants

| Tag | Where it's read-only |
|---|---|
| `@READONLY` | Everywhere (form, survey, Mobile App) |
| `@READONLY-SURVEY` | Only in surveys |
| `@READONLY-FORM` | Only in data entry forms |
| `@READONLY-APP` | Only in the REDCap Mobile App |

## 3.2 Combining Variants

Multiple read-only variants can be combined:

```
@READONLY-FORM @READONLY-APP
```

---

# 4. Combining @HIDDEN and @READONLY

These two tag families can be mixed to achieve fine-grained control. For example, to show a field as read-only to staff but hide it from surveys and exclude it from PDFs:

```
@READONLY-FORM @HIDDEN-SURVEY @HIDDEN-PDF
```

> **Caution:** Using a bare `@HIDDEN` tag alongside `@READONLY-FORM` will override the read-only behavior — the field will be hidden from staff entirely. Always use specific variants to achieve your intended effect.

---

# 5. Common Questions

**Q: Does @HIDDEN prevent the field's data from appearing in reports or exports?**

**A:** No. `@HIDDEN` only hides the field in the data entry and survey interface. Data still appears in reports, the Codebook, and data exports. Use user rights and export settings to restrict data access.

**Q: What happens if I use @HIDDEN on a field that also has branching logic?**

**A:** The `@HIDDEN` tag always wins. The field will be hidden regardless of the branching logic conditions. This is by design — `@HIDDEN` provides absolute hiding.

**Q: Can I temporarily disable @HIDDEN without removing it?**

**A:** Yes. Use the *Quick-Modify Field(s)* bulk editor to **Deactivate** the tag, then **Reactivate** it later. This is useful during instrument testing.

---

# 6. Common Mistakes

**Using `@HIDDEN` when you meant `@HIDDEN-PDF`.** The bare `@HIDDEN` tag does not exclude a field from PDFs. You must use `@HIDDEN-PDF` specifically.

**Mixing bare `@HIDDEN` with `@READONLY` variants.** A bare `@HIDDEN` overrides all read-only variants on the same field. Use specific variants (`@HIDDEN-FORM`, etc.) instead.

**Adding `@READONLY` to a field expecting users to enter data and assuming the field will still appear on surveys.** `@READONLY` displays the field but prevents editing. If you meant to hide it from one context but keep it editable elsewhere, use context-specific variants like `@READONLY-FORM` and `@HIDDEN-SURVEY` instead of applying a bare `@READONLY` to all contexts.

---

# 7. Related Articles

- RC-AT-01 — Action Tags Overview
- RC-FD-02 — Online Designer (where these tags are applied)
- RC-BL-01 — Branching Logic Overview (understand how @HIDDEN overrides logic)



**@HIDDEN & @READONLY — Visibility Control**

| **Article ID** | [RC-AT-02 — @HIDDEN & @READONLY — Visibility Control](RC-AT-02_Action-Tags-Hidden-and-Readonly.md) |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — action tag behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)|
| **Version** | 1.1 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md); [RC-AT-03 — Radio & Dropdown Action Tags](RC-AT-03_Action-Tags-Radio-Dropdown.md); [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md)|
| **Synonyms** | @HIDDEN action tag; @READONLY action tag; how do i hide a field with an action tag; how do i make a field read only; @HIDDEN-FORM and @HIDDEN-SURVEY tags; @READONLY-FORM and @READONLY-SURVEY tags; hide a field on the survey but not the form; make a field uneditable for data entry |

---

## 1. Overview

This article covers the most commonly used action tags: `@HIDDEN` and `@READONLY`, along with their situational variants. These tags control field visibility and editability across different REDCap contexts.

---

## 2. @HIDDEN — Hiding Fields

`@HIDDEN` hides a field from view. The field and its data still exist in the project; users simply cannot see or interact with it. This applies to every user, including REDCap administrators — there is no override that shows a hidden field on the page. Values set on a hidden field by `@DEFAULT`, `@SETVALUE` or a calculation are still saved.

> **Important:** `@HIDDEN` overrides branching logic for visibility. A field tagged with `@HIDDEN` is always hidden, regardless of any branching logic conditions.

> **Warning — branching logic still runs on hidden fields.** Even though you cannot see it, a hidden field's branching logic is still evaluated. If the logic is false and the field already has a value, that value is affected just as for a visible field: on a survey it is erased without any message, and on a data entry form the user is asked whether to erase the value of a field they cannot see. Do not put branching logic on hidden fields whose values must be kept.

If every field on a survey page is hidden, that page is skipped and the respondent goes straight to the next one.

**Common uses:**

- Preserving deprecated fields without deleting historical data
- Hiding calculated fields so users cannot see intermediate values
- Creating honeypot fields in surveys to detect automated bot submissions

> **Tip — honeypot field:** A field tagged `@HIDDEN` or `@HIDDEN-SURVEY` is still part of the survey page, just not displayed. Automated bots tend to fill in every field they find, while human respondents never see it. Add an optional text field such as `hp_check` with `@HIDDEN-SURVEY`, then flag or filter out responses where it has a value (for example with a report filter `[hp_check] <> ""`).

> **Note:** Hiding a field controls what is displayed, not who can access the data. Do not put data on a survey instrument that the respondent must not see — keep it on a separate data entry form instead, and use user rights to control staff access.

### 2.1 Situational Variants

| Tag | Where it hides |
|---|---|
| `@HIDDEN` | On the data entry form, the survey and the Mobile App (see the PDF note below) |
| `@HIDDEN-SURVEY` | Only when accessed as a survey |
| `@HIDDEN-FORM` | Only when accessed as a data entry form |
| `@HIDDEN-APP` | Only in the REDCap Mobile App |
| `@HIDDEN-PDF` | In all PDFs of the instrument (the only way to exclude a field from PDFs that staff download) |

> **PDFs:** PDFs that project users download (for example from the data entry form) still print `@HIDDEN` and `@HIDDEN-SURVEY` fields. Only `@HIDDEN-PDF` removes a field from those PDFs. PDFs that survey respondents download themselves, and e-Consent PDFs given to participants, leave out `@HIDDEN` and `@HIDDEN-SURVEY` fields. If a field must never appear on any PDF, add `@HIDDEN-PDF`.

### 2.2 Combining Variants

Multiple variants can be combined. For example, to hide a field in surveys and in the Mobile App:

```
@HIDDEN-SURVEY @HIDDEN-APP
```

---

## 3. @READONLY — Making Fields Non-Editable

`@READONLY` displays a field normally but prevents any changes to its value. Read-only fields appear slightly greyed out, and their **reset** link and date picker are not shown. A read-only field still saves the value it holds — for example one set by `@DEFAULT`, `@SETVALUE` or piping. On a Notes box with `@RICHTEXT`, `@READONLY` shows the formatted text in a read-only editor.

**Common uses:**

- Displaying pre-loaded contact information that staff can review but not edit
- Showing calculated or piped values for reference without allowing modification

### 3.1 Situational Variants

| Tag | Where it's read-only |
|---|---|
| `@READONLY` | Everywhere (form, survey, Mobile App) |
| `@READONLY-SURVEY` | Only in surveys |
| `@READONLY-FORM` | Only in data entry forms |
| `@READONLY-APP` | Only in the REDCap Mobile App |

### 3.2 Combining Variants

Multiple read-only variants can be combined:

```
@READONLY-FORM @READONLY-APP
```

---

## 4. Combining @HIDDEN and @READONLY

These two tag families can be mixed to achieve fine-grained control. For example, to show a field as read-only to staff but hide it from surveys and exclude it from PDFs:

```
@READONLY-FORM @HIDDEN-SURVEY @HIDDEN-PDF
```

> **Caution:** Using a bare `@HIDDEN` tag alongside `@READONLY-FORM` will override the read-only behavior — the field will be hidden from staff entirely. Always use specific variants to achieve your intended effect.

---

## 5. Common Questions

**Q: Does @HIDDEN prevent the field's data from appearing in reports or exports?**

**A:** No. `@HIDDEN` only hides the field in the data entry and survey interface. Data still appears in reports, the Codebook, and data exports. Use user rights and export settings to restrict data access.

**Q: What happens if I use @HIDDEN on a field that also has branching logic?**

**A:** The `@HIDDEN` tag always wins for visibility — the field stays hidden regardless of the branching logic conditions. But the branching logic is still evaluated: if it is false and the field has a value, a survey erases that value silently and a data entry form asks the user to erase a value they cannot see. Avoid branching logic on hidden fields whose values must be kept.

**Q: Does @HIDDEN keep a field off the PDF?**

**A:** Not for PDFs that project users download — those still show `@HIDDEN` fields. Add `@HIDDEN-PDF` to leave the field out of all PDFs. PDFs that survey respondents download, and participant e-Consent PDFs, already leave out `@HIDDEN` and `@HIDDEN-SURVEY` fields.

**Q: Can I temporarily disable @HIDDEN without removing it?**

**A:** Yes. Use the *Quick-Modify Field(s)* bulk editor to **Deactivate** the tag, then **Reactivate** it later. This is useful during instrument testing.

---

## 6. Common Mistakes

**Using `@HIDDEN` when you meant `@HIDDEN-PDF`.** The bare `@HIDDEN` tag does not exclude a field from PDFs that project users download (only from respondent-downloaded and participant e-Consent PDFs). To keep a field off every PDF, use `@HIDDEN-PDF`.

**Adding branching logic to a hidden field that stores a value.** Branching logic is still evaluated on hidden fields. If it turns false, the stored value can be erased — silently on a survey. Leave branching logic off hidden fields whose values must be kept.

**Mixing bare `@HIDDEN` with `@READONLY` variants.** A bare `@HIDDEN` overrides all read-only variants on the same field. Use specific variants (`@HIDDEN-FORM`, etc.) instead.

**Adding `@READONLY` to a field expecting users to enter data and assuming the field will still appear on surveys.** `@READONLY` displays the field but prevents editing. If you meant to hide it from one context but keep it editable elsewhere, use context-specific variants like `@READONLY-FORM` and `@HIDDEN-SURVEY` instead of applying a bare `@READONLY` to all contexts.

**Marking a field as required and `@HIDDEN-SURVEY` and expecting it to be enforced during survey completion.** REDCap only enforces the required flag in the context where the field is visible. (The reverse also holds: a required field with `@HIDDEN-FORM` is still enforced on the survey, where it is visible.) A field with both `required = 'y'` and `@HIDDEN-SURVEY` will not prompt the survey respondent to fill it in — the required constraint is effectively inactive during survey completion. This matters in hybrid forms that serve as both a survey (for initial collection) and a data entry form (for ongoing staff management). Fields that must be completed by staff in data entry mode, but should be invisible to survey respondents, should be marked required — but be aware that records created through the survey will have those fields blank until staff fill them in.

---

## 7. Related Articles

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (where these tags are applied)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (understand how @HIDDEN overrides logic)

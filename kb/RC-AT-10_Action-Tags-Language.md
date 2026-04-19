RC-AT-10

**Action Tags — Language Action Tags**

| **Article ID** | RC-AT-10 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | REDCap projects with Multi-Language Management (MLM) enabled |
| **Prerequisite** | RC-AT-01 — Action Tags Overview; Multi-Language Management must be configured in the project |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-08 — @IF |

---

# 1. Overview

REDCap's **Multi-Language Management (MLM)** feature allows a project to be presented in multiple languages. Users and survey respondents can switch between languages using buttons at the top of the page. The language action tags extend this system by allowing language detection, selection, and forcing to be driven by field values and logic rather than only by manual button clicks.

> **Prerequisite:** All language action tags require Multi-Language Management to be enabled and at least one additional language to be configured in the project. These tags have no effect in projects without MLM enabled.

---

# 2. Language Action Tag Summary

| Tag | Context | Purpose |
|---|---|---|
| `@LANGUAGE-CURRENT-FORM` | Data entry forms | Captures the currently active language into a field |
| `@LANGUAGE-CURRENT-SURVEY` | Surveys | Captures the currently active language into a field |
| `@LANGUAGE-SET` | Both | Uses a dropdown/radio field value to switch the active language |
| `@LANGUAGE-SET-FORM` | Data entry forms only | Same as `@LANGUAGE-SET` but limited to forms |
| `@LANGUAGE-SET-SURVEY` | Surveys only | Same as `@LANGUAGE-SET` but limited to surveys |
| `@LANGUAGE-FORCE` | Both | Forces the page to render in a specified language |
| `@LANGUAGE-FORCE-FORM` | Data entry forms only | Same as `@LANGUAGE-FORCE` but limited to forms |
| `@LANGUAGE-FORCE-SURVEY` | Surveys only | Same as `@LANGUAGE-FORCE` but limited to surveys |
| `@LANGUAGE-MENU-STATIC` | Surveys | Keeps the language selection menu always visible |

---

# 3. Capturing the Current Language

### @LANGUAGE-CURRENT-FORM

Captures the currently active language on a **data entry form** and stores it in the tagged field. The field value is always updated to reflect the current language, making it possible to branch on language or carry it forward to other forms.

**Applies to:** Text Box fields (no validation), or Drop-down / Radio Button fields whose coded values match the language IDs defined in MLM (e.g., `en`, `fr`, `de`).

**Syntax** (no parameters):
```
@LANGUAGE-CURRENT-FORM
```

**Has no effect on survey pages** — use `@LANGUAGE-CURRENT-SURVEY` for surveys.

### @LANGUAGE-CURRENT-SURVEY

Same as `@LANGUAGE-CURRENT-FORM`, but captures the language **only on survey pages**. For multi-page surveys, the tag must be present on a field within each page where language capture is relevant (e.g., for branching on language within the same survey).

**Applies to:** Same field types as `@LANGUAGE-CURRENT-FORM`.

**Syntax** (no parameters):
```
@LANGUAGE-CURRENT-SURVEY
```

---

# 4. Controlling Language via a Field Value

### @LANGUAGE-SET

When placed on a **Drop-down or Radio Button** field, this tag makes the field act as the language selector. Selecting an option in the field switches the entire page to the corresponding language — the same as clicking the language buttons at the top of the page.

The field's coded values must match the language IDs configured in MLM (e.g., `en` for English, `fr` for French).

**Applies to:** Drop-down and Radio Button fields only.

**Syntax** (no parameters):
```
@LANGUAGE-SET
```

**Tip:** This field can be pre-populated (e.g., by embedding a participant's language ID in a survey URL) to automatically set the language when the survey opens, without requiring the participant to make a selection.

### @LANGUAGE-SET-FORM

Same as `@LANGUAGE-SET`, but the language switching effect is limited to **data entry forms** only. The field has no effect when the instrument is opened as a survey.

### @LANGUAGE-SET-SURVEY

Same as `@LANGUAGE-SET`, but the language switching effect is limited to **survey pages** only.

---

# 5. Forcing a Language

### @LANGUAGE-FORCE

Forces the data entry form or survey page to render in a specified language when the field is present on the instrument. The language must be active and configured in MLM. When the forced language loads successfully, the language selector at the top of the page is hidden.

The tag is evaluated when the form or survey loads.

**Applies to:** Any field type.

**Syntax:**
```
@LANGUAGE-FORCE="de"
```

The language ID must be placed inside single or double quotes. Piping is supported — the language ID can be drawn from another field:

```
@LANGUAGE-FORCE="[preferred_language]"
```

> **Tip for "locking in" a language:** Combining `@LANGUAGE-CURRENT-FORM/SURVEY` on a source field with `@LANGUAGE-FORCE` that reads from that source field creates a pattern where the language selected by the participant persists across subsequent pages.

### @LANGUAGE-FORCE-FORM

Same as `@LANGUAGE-FORCE` but applies only to **data entry forms**, not surveys.

### @LANGUAGE-FORCE-SURVEY

Same as `@LANGUAGE-FORCE` but applies only to **survey pages**, not data entry forms.

---

# 6. @LANGUAGE-MENU-STATIC

When present on any field of a survey page in a project with MLM active (with at least two active languages), the language selection menu remains visible at all times on that page — it does not collapse after a language button has been clicked.

**Applies to:** Any field type, survey pages only.

**Syntax** (no parameters):
```
@LANGUAGE-MENU-STATIC
```

---

# 7. Common Questions

**Q: Can I capture the language on one form and use it to force the language on a later form?**

**A:** Yes. Use `@LANGUAGE-CURRENT-FORM` to store the active language into a field, then reference that field in `@LANGUAGE-FORCE` on subsequent instruments.

**Q: Do language action tags work if MLM is not enabled?**

**A:** No. All language action tags are silently ignored in projects without Multi-Language Management configured.

**Q: Can @LANGUAGE-FORCE be conditional?**

**A:** Yes. Use it inside an `@IF` tag to force different languages based on a condition: `@IF([lang]='fr', @LANGUAGE-FORCE-SURVEY="fr", @LANGUAGE-FORCE-SURVEY="en")`.

**Q: What happens if the language ID specified in @LANGUAGE-FORCE does not exist in the project?**

**A:** The tag has no effect — the page renders in the default language, and the language selector remains visible.

**Q: Can I use @LANGUAGE-SET to allow users to select their language and have it persist across forms in a longitudinal project?**

**A:** Yes. Combine `@LANGUAGE-SET` on a field in an early form (to let users select their language) with `@LANGUAGE-FORCE` on subsequent forms that reads the stored language value. This creates a persistent language preference throughout the project.

---

# 8. Common Mistakes & Gotchas

**Using @LANGUAGE-CURRENT-FORM on a survey page.** The `-FORM` variant has no effect on surveys. Use `@LANGUAGE-CURRENT-SURVEY` for survey pages.

**Using @LANGUAGE-SET on a Text Box field.** `@LANGUAGE-SET` and its variants work only on Drop-down and Radio Button fields whose coded values match language IDs.

**Forgetting to configure language IDs in MLM first.** All these tags depend on language IDs (e.g., `en`, `fr`) that must be defined in Multi-Language Management before the tags can function. A mismatch between the tag parameter and the configured ID will cause the tag to silently fail.

**Omitting @LANGUAGE-CURRENT-SURVEY on multi-page surveys.** The tag captures the language only on the page where it is placed. For multi-page surveys, add it to each page where the language value is needed for branching or downstream use.

---

# 9. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-08 — @IF: using @LANGUAGE-FORCE conditionally based on other field values

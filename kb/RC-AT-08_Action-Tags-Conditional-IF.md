RC-AT-08

**Action Tags — @IF: Conditional Action Tag Logic**

| **Article ID** | RC-AT-08 |
|---|---|
| **Domain** | Action Tags |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-AT-01 — Action Tags Overview; familiarity with branching logic syntax |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-AT-01 — Action Tags Overview; RC-AT-02 — @HIDDEN & @READONLY; RC-AT-03 — Radio/Dropdown Action Tags; RC-AT-06 — Autofill Action Tags; RC-BL-01 — Branching Logic Overview |

---

# 1. Overview

`@IF` is a meta action tag that applies different action tags to a field depending on a logical condition. Instead of hard-coding a single behavior for a field, `@IF` evaluates a condition when the page loads and then activates one set of action tags if the condition is true and a different set if it is false.

This allows a single field to behave differently for different records, users, data access groups, or events — without building separate instruments or using branching logic workarounds.

> **Important:** The condition inside `@IF` is evaluated once when the page loads. It is **not** re-evaluated in real time as the user enters data on the page.

---

# 2. Key Concepts & Definitions

**Condition**

A logical expression using the same syntax as REDCap branching logic — e.g., `[field_name] = '1'`. Both field variables and Smart Variables may be used. The condition evaluates to true or false at page load.

**True branch**

The action tag(s) to apply when the condition evaluates to true. Multiple action tags can be listed, separated by spaces.

**False branch**

The action tag(s) to apply when the condition evaluates to false. Use an empty pair of quotes (`''`) as a placeholder if no action tags should apply in the false case.

---

# 3. Syntax

```
@IF(condition, action_tags_if_true, action_tags_if_false)
```

- The **condition** uses standard branching logic syntax.
- The **true branch** and **false branch** are separated from the condition and from each other by commas.
- To apply **no action tags** in one branch, use `''` (two apostrophes or two double-quotes) as a placeholder.
- To apply **multiple action tags** in a branch, list them separated by spaces — do not use commas between tags within a branch.

---

# 4. Examples

## 4.1 Simple Case — Hide or Show

Hide a field for records in one data access group; leave it visible for all others:

```
@IF([dag-name] = 'site_a', @HIDDEN, '')
```

When the condition is true (the current record is in DAG "site_a"), the field is hidden. For all other records, no action tag is applied and the field displays normally.

## 4.2 Multiple Action Tags in One Branch

Apply both `@HIDECHOICE` and `@READONLY` when a condition is met:

```
@IF([status] = '1', @HIDECHOICE='3' @READONLY, '')
```

When `status` equals `1`, choice `3` is hidden and the field is read-only. Note that `@HIDECHOICE='3'` and `@READONLY` are separated by a space inside the branch — **not** by a comma.

## 4.3 Different Behavior in Each Branch

Apply one action tag when true and a different one when false:

```
@IF([consent] = '1', @READONLY, @HIDDEN)
```

If consent is recorded, the field is read-only (visible but not editable). If consent is not yet recorded, the field is hidden entirely.

## 4.4 Nested @IF

`@IF` can be nested inside another `@IF` to handle more than two conditions:

```
@IF([role] = '1', @HIDDEN, @IF([role] = '2', @READONLY, ''))
```

For role 1: hidden. For role 2: read-only. For all other roles: no restriction.

## 4.5 Multiple @IF on the Same Field

Multiple independent `@IF` tags can be placed on the same field, separated by spaces. All conditions are evaluated independently at page load:

```
@IF([site] = 'east', @HIDDEN-SURVEY, '') @IF([lang] = 'fr', @READONLY, '')
```

---

# 5. PDF Behavior

`@IF` is also evaluated when generating a PDF of an instrument or survey. This means PDF-specific action tags (such as `@HIDDEN-PDF`) can be placed inside `@IF` branches and will be applied correctly in the generated PDF.

---

# 6. Limitations

**Not evaluated in real time.** The condition is checked once when the page loads. If a user changes a field value that the condition depends on, `@IF` will not re-evaluate until the page is reloaded.

**Do not use @CALCTEXT or @CALCDATE inside @IF.** The calculation action tags operate in contexts (real-time recalculation, data import, Data Quality rules) that `@IF` does not. Placing them inside an `@IF` branch produces unexpected results. See RC-AT-09 for guidance on calculation tags.

**Avoid complex nesting.** Deeply nested `@IF` statements are difficult to read and maintain. If logic becomes complex, consider restructuring the project design or using branching logic to control field visibility separately.

---

# 7. Common Questions

**Q: Can I use Smart Variables in the @IF condition?**

**A:** Yes. Both field variables (e.g., `[age]`) and Smart Variables (e.g., `[user-dag-name]`) are valid in the condition. This makes it possible to apply different action tags based on the current user's role, DAG membership, or event.

**Q: Does @IF work in surveys?**

**A:** Yes. The condition is evaluated when the survey page loads, using whatever data is available for that record at that point in time.

**Q: What happens if both the true and false branches are empty?**

**A:** Using `''` in both branches (`@IF([field]='1', '', '')`) has no practical effect — no action tags are applied in either case. This is valid but unnecessary.

**Q: Can @IF be combined with other action tags placed directly on the field (outside @IF)?**

**A:** Yes. A field can have both standalone action tags and `@IF` tags. The standalone tags always apply; the `@IF` tags add or layer additional behavior conditionally.

---

# 8. Common Mistakes & Gotchas

**Using commas to separate action tags within a branch.** Tags inside a branch must be separated by spaces, not commas. `@IF([x]='1', @HIDDEN, @READONLY-SURVEY @HIDDEN-PDF, '')` is incorrect because the false branch appears to have two items separated by a comma. Write it as `@IF([x]='1', @HIDDEN, @READONLY-SURVEY @HIDDEN-PDF)` or use `''` as a placeholder: `@IF([x]='1', @HIDDEN, '')`.

**Expecting real-time re-evaluation.** `@IF` evaluates at page load only. A field that is hidden by `@IF` based on another field's value will not become visible if the user changes that other field during the same session — the page must reload.

**Nesting @CALCTEXT or @CALCDATE inside @IF.** This combination is explicitly not supported. Use calculation action tags directly on the field without wrapping them in `@IF`.

**Forgetting the `''` placeholder.** If one branch should apply no action tags, use `''` as an explicit placeholder. An empty branch (missing parameter) causes a syntax error and the tag will not function.

---

# 9. Related Articles

- RC-AT-01 — Action Tags Overview: what action tags are and how to add them
- RC-AT-02 — @HIDDEN & @READONLY: commonly used inside @IF branches
- RC-AT-03 — Radio/Dropdown Action Tags: `@HIDECHOICE` and `@SHOWCHOICE` support piping and @IF
- RC-AT-06 — Autofill Action Tags: autofill tags can be applied conditionally via @IF
- RC-AT-09 — Calculation Action Tags: @CALCTEXT and @CALCDATE; do not nest inside @IF
- RC-BL-01 — Branching Logic Overview: condition syntax is the same as branching logic

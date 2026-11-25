---
id: RC-AT-03
title: Radio & Dropdown Action Tags
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
- id: RC-AT-04
  title: Checkbox Action Tags
- id: RC-FD-02
  title: Online Designer
tags:
- action tags
synonyms:
- '@RANDOMORDER action tag'
- '@HIDECHOICE action tag'
- '@SHOWCHOICE action tag'
- '@MAXCHOICE action tag'
- '@MAXCHOICE-SURVEY-COMPLETE action tag'
- how do i randomize the order of radio button choices
- how do i hide a dropdown option with an action tag
- limit how many times a choice can be selected across records
- action tags for radio buttons and dropdowns
---

# 1. Overview

This article covers action tags designed for radio button and dropdown fields: `@RANDOMORDER`, `@HIDECHOICE`, `@SHOWCHOICE`, `@MAXCHOICE` and `@MAXCHOICE-SURVEY-COMPLETE`. Despite the article title, `@HIDECHOICE`, `@SHOWCHOICE` and the two `@MAXCHOICE` tags also work on checkbox, yes/no and true/false fields. On matrix fields, `@RANDOMORDER` is ignored; see the matrix question in section 6 for how the others behave.

> **Note:** These tags affect the data entry form and survey only. A PDF of the instrument always lists every choice, in the original order, whatever these tags say.

---

# 2. @RANDOMORDER

Randomizes the visual order of options every time a page loads. The underlying raw values and stored data are unaffected — only the display order changes.

**Use case:** Preventing option-order bias in surveys (e.g., respondents systematically choosing the first option).

**Syntax:**
```
@RANDOMORDER
```

**Notes:**
- Works on radio buttons, dropdowns, and checkboxes
- A yes/no field has 2 possible permutations; a 5-option field has 120
- No parameters required

---

# 3. @HIDECHOICE

Hides one or more specific options from a field while preserving those options in records where they were already selected.

> **Note:** If a record already has a now-hidden option saved, that option stays visible on the form so the existing answer is not lost, and saving without changes preserves it. It disappears only once a different answer has been saved and the page is reloaded.

**Syntax — single option:**
```
@HIDECHOICE='1'
```

**Syntax — multiple options (one tag, comma-separated, in quotes):**
```
@HIDECHOICE='1, 2'
```

Use the raw value of the option(s), not the label. To hide several options, list them all in one `@HIDECHOICE` tag, comma-separated and inside quotes. Do not repeat the tag: if a field has `@HIDECHOICE='1' @HIDECHOICE='2'`, only the first tag is used and option 2 stays visible.

**Use case:** Marking class spots as filled in a registration form, or hiding expired options while preserving historical selections.

---

# 4. @SHOWCHOICE

The inverse of `@HIDECHOICE`. Starts with all options hidden and shows only the listed ones.

Use `@SHOWCHOICE` when the number of options to hide is larger than the number to show — it is cleaner to list what to show.

**Syntax:**
```
@SHOWCHOICE='1, 2, 3'
```

> **Note:** If both `@HIDECHOICE` and `@SHOWCHOICE` target the same option, `@SHOWCHOICE` takes precedence and the option will be shown.

---

# 5. @MAXCHOICE

Limits how many times a given option can be selected across all project records. Once the limit is reached, the option is unavailable to new respondents: on radio buttons and checkboxes it is greyed out and cannot be selected, and in a dropdown it is removed from the list. If every option is full, the field shows "[no choices available]".

**Syntax:**
```
@MAXCHOICE(1=25,2=30,3=30)
```

Each entry is `raw_value=limit`. Separate multiple entries with commas. A limit of 0 (e.g., `@MAXCHOICE(1=0)`) makes the option unavailable straight away.

**How the count works:** the count is kept per event. It includes every record in the project, across all Data Access Groups and repeating instances, and it includes values that arrived by data import. In a longitudinal project, the same field on two different events has two separate counts.

**What happens when a choice fills up while someone has the page open:** REDCap checks the limit again when the form or survey is saved. If the chosen option has filled up in the meantime, that answer is not saved and the person is told to choose a different option.

> **Important:** The limit applies to data entry forms and surveys only. Data imports and the API are not checked against `@MAXCHOICE` and can push an option past its limit.

**@MAXCHOICE-SURVEY-COMPLETE:** works the same way and uses the same syntax, but counts only completed survey responses. Partial responses and data entered on the data entry form do not count towards the limit.

```
@MAXCHOICE-SURVEY-COMPLETE(1=25,2=30,3=30)
```

**Use case:** Class registration with limited spots, event sign-ups with capacity limits.

**Combining with other tags:**

- `@MAXCHOICE` + `@HIDECHOICE`: Hides the greyed-out option entirely (requires manual monitoring)
- `@MAXCHOICE` + `@RANDOMORDER`: Randomizes option order while enforcing limits

---

# 6. Common Questions

**Q: Can these tags be combined?**

**A:** Yes. For example, `@MAXCHOICE(1=25) @RANDOMORDER` enforces a limit while randomizing order.

**Q: Do these tags work on matrix fields?**

**A:** Partly. `@RANDOMORDER` is ignored on matrix fields. `@HIDECHOICE` and `@SHOWCHOICE` remove the button for the hidden option in that field's row only; the matrix column and its header stay, because other rows share them. `@MAXCHOICE` works on matrix fields.

**Q: If I use @HIDECHOICE, will the hidden option still be visible to a respondent who already selected it?**

**A:** Yes. If a record already has a hidden option saved, that option remains visible for that record so the existing answer is kept. It is removed only after a different answer has been saved and the page is reloaded.

**Q: How does @MAXCHOICE handle simultaneous form submissions?**

**A:** REDCap checks the limit when the page loads and again when it is saved. If two people open the form when one spot remains and one saves first, the second person's answer for that field is not saved and they are told to choose another option. Data imports and the API are not checked against the limit.

**Q: Can I use @SHOWCHOICE to show options dynamically based on branching logic?**

**A:** Not on the same page. The list of options is worked out when the page loads and does not change as other answers on that page change. It can differ from record to record or event to event if you wrap the tag in `@IF` or pipe a value saved earlier into it, for example `@IF([group]='1', @SHOWCHOICE='1, 2', @SHOWCHOICE='3, 4')`. To react to answers on the same page, use branching logic on separate fields instead.

---

# 7. Common Mistakes & Gotchas

**Using the option label instead of the raw value in @HIDECHOICE or @SHOWCHOICE.** These tags require the raw coded value (e.g., `'1'`, `'2'`) not the display label. If you enter the label by mistake, the tag will silently fail and all options will remain visible.

**Repeating @HIDECHOICE or @SHOWCHOICE for each option.** Only the first tag on the field is used. Put all the raw values in one tag, comma-separated and in quotes: `@HIDECHOICE='1, 2'`.

**Assuming @MAXCHOICE also limits imports.** The limit is enforced on data entry forms and surveys, including a re-check when the page is saved. Data imports and API writes are not checked and can take an option past its limit. If capacity is strict, check counts before importing.

**Assuming @MAXCHOICE counts across events.** Each event has its own count. If the same field is used on several events, each event can reach the limit separately.

**Mixing @HIDECHOICE and @SHOWCHOICE without understanding precedence.** If both tags target the same option, `@SHOWCHOICE` wins and the option displays. This can be counterintuitive if you intended `@HIDECHOICE` to hide something universally.

**Assuming @HIDECHOICE removes an option from data exports and reports.** `@HIDECHOICE` is a display-only tag — it hides options from the data entry form and surveys but has no effect on exports or the Custom Reports module. Hidden coded values are still present in the data and will appear in exports as-is. If a record was saved with a now-hidden option, that value shows up in every export and report filter just like any other choice. When building reports on fields that use `@HIDECHOICE`, do not assume the hidden values are absent from the data.

---

# 8. Related Articles

- [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)
- [RC-AT-04 — Checkbox Action Tags](RC-AT-04_Action-Tags-Checkbox.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md)

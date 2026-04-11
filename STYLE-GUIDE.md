# REDCap Project Design Style Guide

This document records the preferred design conventions for REDCap projects built or supported by this team. It is a living document — add new principles here as they are agreed upon.

These are defaults, not mandates. Individual projects may deviate when there is a good reason, but deviations should be intentional and documented, not accidental.

---

## How to use this guide

- **New project designers** — read this before building your first instrument. These conventions exist because they reduce common mistakes and create a more consistent experience for data entry users and analysts.
- **Reviewers** — use this as a checklist when reviewing a new data dictionary or instrument design before a project goes into production.
- **Contributors** — if you encounter a recurring design decision that isn't covered here, add a new section. Include the principle, the rationale, and any exceptions.

---

## 1. Field Alignment (Column N — Custom Alignment)

REDCap supports four alignment codes: `LH`, `LV`, `RH`, and `RV`. See RC-FD-08 Section 5.12 for a full explanation of what each code does visually.

The short version:
- **L (Left)** = field spans full page width
- **R (Right)** = field is approximately half-width (right side of page)
- **H (Horizontal)** = label and input are side by side
- **V (Vertical)** = label sits above the input

The default when the column is left blank is `RV`.

### 1.1 Notes fields (`notes` field type)

**Convention: use `LH` or `LV`**

A `notes` field with `RH` or `RV` alignment renders at roughly half the page width, which makes the text area cramped and difficult to type in. Setting alignment to `LH` or `LV` gives the text area the full page width.

There is rarely a good reason to use a half-width notes field. If you are using one, consider whether a single-line `text` field would be more appropriate.

### 1.2 Radio and checkbox fields

**Convention: `LV` for longer lists, `LH` for short lists**

The Vertical/Horizontal component controls whether answer choices are stacked (V) or displayed in a single row (H). As a rule of thumb:

- 2–4 short choices → `LH` (horizontal, full width) reads cleanly
- 5 or more choices, or long choice labels → `LV` (vertical, full width) is easier to scan

The Left/Right component controls which side of the page choices appear on. Left (`L`) is generally preferred as it aligns with natural reading direction and gives more visual space.

### 1.3 Text, dropdown, yesno, truefalse

**Convention: leave blank (accept `RV` default) unless there is a layout reason to change**

These field types are compact and the width difference between Left and Right alignment is less impactful than with `notes` fields. Accept the default unless you are deliberately composing a specific layout.

### 1.4 Consistency within an instrument

**Convention: avoid mixing Left and Right fields in the same section without a clear layout purpose**

Alternating between full-width and half-width fields creates a visually fragmented form. If you are setting alignment on any field, consider whether the surrounding fields should also be aligned consistently.

---

## 2. Project Structure

### 2.1 Do not use longitudinal mode if each form is only used once

**Convention: use longitudinal mode only when instruments are repeated across multiple events**

Longitudinal mode is designed for studies where participants complete the same instruments at multiple time points (e.g., baseline, month 3, month 6). If your project has multiple forms but each form is used at a single point in time (e.g., a Screening form, an Enrollment form, and a Follow-up form — each completed once), a classic (non-longitudinal) project achieves the same result with less configuration overhead.

Using longitudinal mode for a single-arm, single-instance-per-form project adds unnecessary complexity: event setup, event-scoped branching logic syntax, and a more confusing record status dashboard — with no functional benefit.

**Use longitudinal mode when:**
- The same instrument is completed by the same participant at more than one time point, OR
- You need to track scheduling windows, multiple arms, or event-based branching logic

**Use classic mode when:**
- Each instrument is completed exactly once per participant, regardless of how many instruments exist

**Exception:** Some institutions use longitudinal mode for purely structural reasons (e.g., to use repeated instruments without repeating events). If you have a specific architectural reason, document it in the project notes.

---

## 3. [Future principles — add here]

As new conventions are agreed upon, add them as numbered sections following the same structure:

- **Convention statement** (the rule)
- **Rationale** (why this matters)
- **Exceptions** (when it's acceptable to deviate)

---
id: RC-BL-01
title: Branching Logic — Overview & Scope
domain: Branching Logic
applies_to:
- All REDCap project types
- requires Project Design and Setup rights
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- RC-FD-02 — Online Designer
version: '1.2'
last_updated: 2026-08
related:
- id: RC-BL-02
  title: 'Branching Logic: Syntax & Atomic Statements'
- id: RC-BL-03
  title: 'Branching Logic: Combining Statements'
- id: RC-BL-04
  title: 'Branching Logic: Structured Fields & Checkboxes'
- id: RC-FD-02
  title: Online Designer
tags:
- branching logic
synonyms:
- how do i show a field only when another answer is selected
- conditional field visibility
- what is branching logic in redcap
- hide a question based on a previous answer
- where do i set up branching logic
- make fields appear conditionally
- show hide fields on a form
- intro to branching logic
---

# 1. Overview

This article introduces REDCap's branching logic feature — what it does, where it is used across the platform, how to access the branching logic editor, and what is out of scope for the basic series. It is the entry point for the Branching Logic knowledge base series.

---

# 2. Key Concepts & Definitions

**Branching Logic**

A feature that conditionally shows or hides a specific field in a REDCap instrument based on a logic statement. If the statement evaluates to true, the field is shown. If it evaluates to false, the field is hidden. Branching logic is configured per field in the Online Designer or Data Dictionary.

**Logic Statement**

A conditional expression written in REDCap's logic syntax that evaluates to either true or false. Logic statements compare field values using operators (e.g., `[age]>=18`). The same syntax is shared across multiple REDCap features beyond branching logic.

**Logic Syntax**

The language REDCap uses for all logic statements — branching logic, calculated fields, survey invitations, alerts, reports, and more. Though commonly called "branching logic syntax," the syntax is more accurately a shared logic language used across the platform. This series uses the terms interchangeably.

**True / False Outcome**

Every logic statement in REDCap resolves to either true or false. In branching logic specifically, true = show the field and false = hide the field. Other features use the same true/false outcome to trigger different actions (e.g., send or suppress a survey invitation).

---

# 3. What Branching Logic Does

The branching logic feature has one job: show or hide a specific field based on whether a logic statement is true or false.

- If the statement is true: the field is visible to the user.
- If the statement is false: the field is hidden and its stored value is cleared automatically.
- Branching logic is evaluated dynamically as data is entered — fields appear and disappear without a page reload.
- The user cannot override or bypass branching logic during data entry.

> **Important:** When branching logic hides a field, any value previously stored in that field is automatically deleted. This is intentional behavior — it prevents orphaned data from remaining in hidden fields. Design your logic carefully to avoid inadvertently clearing data.

---

# 4. Where the Logic Syntax Is Used Across REDCap

The same logic syntax that powers branching logic is also used in several other REDCap features. Understanding this shared foundation makes it easier to learn each feature.

| **Feature** | **How Logic Is Used** | **Outcome Type** |
|---|---|---|
| Branching Logic (Online Designer) | Show or hide a specific field in an instrument | True = show field; False = hide field |
| Survey Invitations | Determine whether to send a survey invitation to a participant | True = send invitation; False = suppress |
| Survey Queue | Determine whether a participant can proceed to the next survey in a queue | True = allow; False = skip |
| Reports | Filter which records appear in a saved report | True = include record; False = exclude |
| Project Dashboards | Filter which records appear in a dashboard | True = include; False = exclude |
| Alerts & Notifications | Determine whether to trigger an automated alert | True = send alert; False = suppress |
| Calculated Fields | Perform arithmetic operations on field values | Numerical result (not true/false) |
| Action Tags (selected) | Drive dynamic behavior such as default values or date comparisons | Varies by action tag |

> **Note:** Calculated fields and action tags use the same logic syntax but do not produce a true/false outcome. Calculated fields always return a number. Action tags use the syntax for a range of non-boolean purposes. Calculated fields are covered in [RC-CALC-02 — Calculated Fields](RC-CALC-02_Calculated-Fields.md). Action tags that use logic syntax are covered in the RC-AT series — start with [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) — Action Tags Overview.

---

# 4a. Version Caveats Affecting Branching Logic

Three defects are worth knowing because each produced a **wrong result rather than a visible failure**.

> **Critical — fields that should have been hidden were not (below 16.0.27 Standard).** Some forms and surveys displayed a branching logic error popup where no real problem existed, **and in some cases fields that branching logic should have hidden were shown**. The second half is a data-exposure concern: a participant or user could see a question intended to be hidden from them. Fixed in 16.0.27.

> **Version caveat (below 16.0.40 Standard):** Branching logic or calculated fields containing a **`$` character** stopped working entirely and could display an error on the page. Fixed in 16.0.40.

> **Version caveat (below 15.4.5 Standard):** Form Display Logic rules containing a **comment at the end of the logic** might not be interpreted correctly. Fixed in 15.4.5 — see [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md).

Comparisons against blank values have their own history of returning wrong results — see [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md) §5.5.

> **Note — JavaScript is no longer permitted in logic.** From 17.0.2, administrators cannot inject JavaScript into branching logic or calc/CALCTEXT equations. This closed a Remote Code Execution vector that recurred across three releases. If an inherited project relies on it, the logic stops working on 17.0.2 — see [RC-PROJ-04 — Project Setup: Additional Customizations](RC-PROJ-04_Project-Setup-Additional-Customizations.md).

---

# 5. Accessing the Branching Logic Editor

Branching logic for a specific field is configured in the Online Designer. There are two paths:

## 5.1 From the Instrument Field List

- In the Online Designer, open the instrument that contains the field you want to add logic to.
- Locate the field in the instrument's field list.
- Click the branching logic icon (a fork/branch symbol) next to the field. This opens the branching logic editor for that field.

## 5.2 From the Field Edit Dialog

- In the Online Designer, open the field edit dialog for any field (click the pencil/edit icon).
- Scroll to the Branching Logic section within the dialog.
- Click **Open Branching Logic Editor** to open the dedicated editor, or type logic directly into the text field.

> **Tip:** The branching logic editor provides a drag-and-drop interface for building basic statements without typing syntax. For more complex or compound logic, typing directly into the syntax field is faster. Both methods produce identical results.

---

# 6. Scope of This Series

This knowledge base series covers the foundations of REDCap's logic syntax. The following topics are covered:

- Logic syntax elements: operators, brackets, quotes, boolean operators ([RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md))
- Writing atomic (single-condition) logic statements ([RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md))
- Combining statements with AND, OR, and parentheses ([RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md))
- Writing logic for structured field types including checkboxes ([RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md))

The following topics are outside the scope of this series. Each has its own dedicated article:

- Calculated fields and calculation syntax — [RC-CALC-02 — Calculated Fields](RC-CALC-02_Calculated-Fields.md)
- Action tags that use logic syntax — [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md)(start here for the full series)
- Smart variables — [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md)
- Field embedding (curly bracket syntax) — [RC-FD-07 — Field Embedding](RC-FD-07_Field-Embedding.md)
- Event-based logic in longitudinal projects — [RC-BL-05 — Branching Logic — Longitudinal Projects](RC-BL-05_Branching-Logic-in-Longitudinal-Projects.md)
- REDCap functions (e.g., datediff, rounddown) — [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md)

---

# 7. Common Questions

**Q: Does branching logic affect every feature in REDCap that uses a logic statement?**

**A:** No. Branching logic specifically controls field visibility within an instrument. The same logic syntax is used in other features (reports, alerts, survey invitations, etc.), but each feature applies the true/false result differently. A logic statement that works in branching logic will generally work syntactically in those other features, but the effect is different.

**Q: Can I use branching logic to show or hide an entire instrument (not just a field)?**

**A:** Not directly through branching logic. Branching logic operates at the field level. Showing or hiding an entire instrument based on conditions is handled through other features — for example, the Survey Queue (for surveys) or instrument-level access rights. See those dedicated articles.

**Q: What happens to data in a field when branching logic hides it?**

**A:** The data is cleared and deleted automatically. REDCap removes the stored value from the database whenever a field becomes hidden by branching logic. This is by design and cannot be overridden.

**Q: Can I write branching logic directly in the Data Dictionary instead of the Online Designer?**

**A:** Yes. The Data Dictionary CSV has a Branching Logic column where you can enter logic statements directly. This is often faster when applying logic to many fields at once. The syntax is identical to what you would type in the Online Designer editor.

**Q: Is branching logic case-sensitive?**

**A:** It depends on what you are comparing. Hard-coded text values (strings) in logic statements are case-sensitive. For example, `[fav_color]="green"` will not match if the user typed "Green" with a capital G. Variable names and boolean operators (AND, OR) are not case-sensitive.

---

# 8. Common Mistakes & Gotchas

**Assuming hidden fields retain their data.** When branching logic hides a field, its stored value is deleted. If a user triggers the hide condition after entering data, that data is gone. Test all logic thoroughly in Development mode before collecting real data.

**Applying branching logic in Production without testing.** The Online Designer's syntax checker validates that logic is syntactically correct, but it does not verify that it behaves as intended. Always test in a Development project or with test records before deploying.

**Confusing branching logic scope with instrument scope.** Branching logic only shows or hides individual fields. It cannot be used to show or hide an entire instrument.

**Expecting logic behavior to be the same in calculated fields.** Calculated fields use the same syntax but do not evaluate to true or false — they always return a number. The semantics are different even though the syntax looks similar.

---

# 9. Design Patterns

## 9.1 Checkbox Gate (Participation / Intent Gate)

A common survey design pattern is to place a single required checkbox at the top of a form — labelled something like "Yes, I would like to participate" or "I confirm I want to proceed" — and then apply `[gate_field(1)]=1` as the branching logic condition on every subsequent field. This has the effect of hiding all questions until the respondent explicitly opts in.

**Why use it:**
- It provides a clear, visible commitment step before the respondent sees the full form.
- It cleanly separates "did not opt in" records from "partial response" records — if the checkbox is unchecked, no other data can be captured.
- Because the gate field is required, the form cannot be saved unless the respondent actively checks it.

**How it works:**
```
[join_checkbox(1)] = 1
```

Apply this expression as the branching logic for every field that should only appear after the respondent confirms. All those fields remain hidden until the checkbox is checked; if the respondent unchecks it, any data they had entered in those fields is cleared automatically.

**Limitation:** This pattern uses branching logic at the field level. It does not prevent a respondent from submitting the form with only the gate checkbox checked and nothing else — if subsequent fields are not individually marked as required, the form can be saved in that state. Consider whether the context warrants making key downstream fields required in addition to the gate.

> **Note:** This pattern uses checkbox field syntax — see [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md) — Branching Logic for Structured Fields & Checkboxes for the `(option_code)` notation used with checkbox fields.

---

# 10. Related Articles

- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)(the logic language and writing your first statement)
- [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md)(AND, OR, parentheses)
- [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (where branching logic is configured)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (alternative location for writing logic in bulk)
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (explains how branching logic appears from the data entry user's perspective)
- [RC-FD-09 — Field Embedding: Advanced Layout Patterns & Workflow Design](RC-FD-09_Field-Embedding-Advanced-Patterns-and-Workflow-Design.md)(related pattern: embedding sub-fields inside radio choice labels alongside branching logic)

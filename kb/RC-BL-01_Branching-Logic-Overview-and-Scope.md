

**Branching Logic — Overview & Scope**

| **Article ID** | [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) |
|---|---|
| **Domain** | Branching Logic |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.5.4 (Standard) / v17.3.18 (LTS) — changelog review; page not re-captured. §7 case-sensitivity live-tested on v17.5.6 (Standard) |
| **Prerequisite** | [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) |
| **Version** | 1.6 |
| **Last Updated** | 2026-10 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md); [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md); [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md); [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md); [RC-PROJ-04 — Project Setup: Additional Customizations](RC-PROJ-04_Project-Setup-Additional-Customizations.md) |
| **Synonyms** | how do i show a field only when another answer is selected; conditional field visibility; what is branching logic in redcap; hide a question based on a previous answer; where do i set up branching logic; make fields appear conditionally; show hide fields on a form; intro to branching logic |

---

## 1. Overview

This article introduces REDCap's branching logic feature — what it does, where it is used across the platform, how to access the branching logic editor, and what is out of scope for the basic series. It is the entry point for the Branching Logic knowledge base series.

---

## 2. Key Concepts & Definitions

**Branching Logic**

A feature that conditionally shows or hides a specific field in a REDCap instrument based on a logic statement. If the statement evaluates to true, the field is shown. If it evaluates to false, the field is hidden. Branching logic is configured per field in the Online Designer or Data Dictionary.

**Logic Statement**

A conditional expression written in REDCap's logic syntax that evaluates to either true or false. Logic statements compare field values using operators (e.g., `[age]>=18`). The same syntax is shared across multiple REDCap features beyond branching logic.

**Logic Syntax**

The language REDCap uses for all logic statements — branching logic, calculated fields, survey invitations, alerts, reports, and more. Though commonly called "branching logic syntax," the syntax is more accurately a shared logic language used across the platform. This series uses the terms interchangeably.

**True / False Outcome**

Every logic statement in REDCap resolves to either true or false. In branching logic specifically, true = show the field and false = hide the field. Other features use the same true/false outcome to trigger different actions (e.g., send or suppress a survey invitation).

---

## 3. What Branching Logic Does

The branching logic feature has one job: show or hide a specific field based on whether a logic statement is true or false.

- If the statement is true: the field is visible to the user.
- If the statement is false: the field is hidden. What happens to a value already stored in that field depends on context — see the note below.
- Branching logic is evaluated dynamically as data is entered — fields appear and disappear without a page reload.
- The user cannot write logic exceptions for themselves during data entry, but on data entry forms they can decline the erase prompt described below.

> **Important:** When branching logic is about to hide a field that holds a value, the behavior differs by context.
>
> - **Data entry forms:** REDCap prompts the user before erasing the value. If the user cancels, the field remains visible and keeps its data.
> - **Survey pages:** there is no prompt. The field is hidden and its value erased automatically.
> - **Project setting override:** when **Prevent branching logic from hiding fields that have values** is enabled under Project Setup → Additional Customizations, any field containing a value is exempt from branching logic entirely and stays visible on both forms and surveys. See [RC-PROJ-04](RC-PROJ-04_Project-Setup-Additional-Customizations.md).
>
> Design logic on the assumption that survey data in hidden fields is lost, and that form data may or may not be, depending on what the user chose in the prompt.

---

## 4. Where the Logic Syntax Is Used Across REDCap

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

## 4a. Version Caveats Affecting Branching Logic

These defects are worth knowing because each produced a **wrong result rather than a visible failure**.

> **Critical — fields that should have been hidden were not (below 16.0.27 Standard).** Some forms and surveys displayed a branching logic error popup where no real problem existed, **and in some cases fields that branching logic should have hidden were shown**. The second half is a data-exposure concern: a participant or user could see a question intended to be hidden from them. Fixed in 16.0.27.

> **Version caveat (below 16.0.40 Standard):** Branching logic or calculated fields containing a **`$` character** stopped working entirely and could display an error on the page. Fixed in 16.0.40.

> **Version caveat (below 15.4.5 Standard):** Form Display Logic rules containing a **comment at the end of the logic** might not be interpreted correctly. Fixed in 15.4.5 — see [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md).

> **Version caveat (17.3.1–17.4.1 Standard / 17.3.5–17.3.7 LTS):** Logic containing more than roughly **200–300 `and`/`or` clauses** could fail to evaluate and **always return True** — so a field meant to be hidden was shown, or an alert or filter matched every record. Emerged in 17.3.1 Standard and was inherited by the 17.3.x LTS line; fixed in 17.4.2 Standard / 17.3.8 LTS, which handles far longer logic. Very long logic is usually generated (for example, a long list of eligible codes); on an affected version, split it or replace it with a lookup field.

> **Version caveat (below 17.5.4 Standard / 17.3.18 LTS):** Several client-side logic defects were fixed together. On forms and surveys: logic or calculations with **inline comments** could fail to evaluate in some situations; static text or label values containing an **apostrophe or quotation mark** could produce invalid JavaScript, so the logic silently did nothing; and on **repeating events**, integer and number fields could have **`0` treated as blank** (and blanks as non-blank). See [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) §3.3, §3.6 and §6. Independent of version, comments are only accepted on a line of their own; a comment after logic on the same line is a syntax error ([RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) §3.6).

> **Version caveat (below 17.5.0 Standard / 17.3.13 LTS):** Logic or calculations referencing a **date or datetime field that has a Missing Data Code**, with an X-instance smart variable appended (such as `[visit_date][last-instance]`), could return an unexpected result on the form or survey. Server-side evaluation (Data Quality rule H, calculations during import) was not affected. See [RC-BL-05 — Branching Logic in Longitudinal Projects](RC-BL-05_Branching-Logic-in-Longitudinal-Projects.md) §5.3.

Comparisons against blank values have their own history of returning wrong results — see [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md) §5.5.

> **Note — JavaScript is no longer permitted in logic.** From 17.0.2, administrators cannot inject JavaScript into branching logic or calc/CALCTEXT equations. This closed a Remote Code Execution vector that recurred across three releases. If an inherited project relies on it, the logic stops working on 17.0.2 — see [RC-PROJ-04 — Project Setup: Additional Customizations](RC-PROJ-04_Project-Setup-Additional-Customizations.md).

---

## 5. Accessing the Branching Logic Editor

Branching logic for a specific field is configured in the Online Designer. There are two paths:

### 5.1 From the Instrument Field List

- In the Online Designer, open the instrument that contains the field you want to add logic to.
- Locate the field in the instrument's field list.
- Select the branching logic icon (a fork/branch symbol) next to the field. This opens the branching logic editor for that field.

### 5.2 From the Field Edit Dialog

- In the Online Designer, open the field edit dialog for any field (select the pencil/edit icon).
- Scroll to the Branching Logic section within the dialog.
- Select **Open Branching Logic Editor** to open the dedicated editor, or type logic directly into the text field.

> **Tip:** The branching logic editor provides a drag-and-drop interface for building basic statements without typing syntax. For more complex or compound logic, typing directly into the syntax field is faster. Both methods produce identical results.

---

## 6. Scope of This Series

This knowledge base series covers the foundations of REDCap's logic syntax. The following topics are covered:

- Logic syntax elements: operators, brackets, quotes, boolean operators ([RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md))
- Writing atomic (single-condition) logic statements ([RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md))
- Combining statements with AND, OR, and parentheses ([RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md))
- Writing logic for structured field types including checkboxes ([RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md))

The following topics are outside the scope of this series. Each has its own dedicated article:

- Calculated fields and calculation syntax — [RC-CALC-02 — Calculated Fields](RC-CALC-02_Calculated-Fields.md)
- Action tags that use logic syntax — [RC-AT-01 — Action Tags: Overview](RC-AT-01_Action-Tags-Overview.md) (start here for the full series)
- Smart variables — [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md)
- Field embedding (curly bracket syntax) — [RC-FD-07 — Field Embedding](RC-FD-07_Field-Embedding.md)
- Event-based logic in longitudinal projects — [RC-BL-05 — Branching Logic — Longitudinal Projects](RC-BL-05_Branching-Logic-in-Longitudinal-Projects.md)
- REDCap functions (e.g., datediff, rounddown) — [RC-CALC-01 — Special Functions Reference](RC-CALC-01_Special-Functions-Reference.md)

---

## 7. Common Questions

**Q: Does branching logic affect every feature in REDCap that uses a logic statement?**

**A:** No. Branching logic specifically controls field visibility within an instrument. The same logic syntax is used in other features (reports, alerts, survey invitations, etc.), but each feature applies the true/false result differently. A logic statement that works in branching logic will generally work syntactically in those other features, but the effect is different.

**Q: Can I use branching logic to show or hide an entire instrument (not just a field)?**

**A:** Not directly through branching logic. Branching logic operates at the field level. Showing or hiding an entire instrument based on conditions is handled through other features — for example, the Survey Queue (for surveys) or instrument-level access rights. See those dedicated articles.

**Q: What happens to data in a field when branching logic hides it?**

**A:** It depends on context. On a survey page the value is erased automatically with no prompt. On a data entry form REDCap asks the user first, and the user can cancel, in which case the field stays visible with its value intact. The behavior can also be overridden project-wide: the **Prevent branching logic from hiding fields that have values** setting under Project Setup → Additional Customizations exempts any value-bearing field from branching logic altogether. See [RC-PROJ-04](RC-PROJ-04_Project-Setup-Additional-Customizations.md).

**Q: Can I write branching logic directly in the Data Dictionary instead of the Online Designer?**

**A:** Yes. The Data Dictionary CSV has a Branching Logic column where you can enter logic statements directly. This is often faster when applying logic to many fields at once. The syntax is identical to what you would type in the Online Designer editor.

**Q: Is branching logic case-sensitive?**

**A:** Yes, in both halves of a comparison.

- **Variable names are case-sensitive.** REDCap stores every variable name in lowercase, so a capitalized reference matches nothing. Both the Online Designer's logic editor and a Data Dictionary upload reject `[Age]` as a syntax error, so it cannot be saved as branching logic. Used as a report filter or API `filterLogic`, it fails silently and matches every record.
- **Hard-coded text values are case-sensitive.** `[fav_color]="green"` will not match a stored value of "Green".

Boolean operators are the exception: `and` and `AND`, `or` and `OR` are interchangeable.

---

## 8. Common Mistakes & Gotchas

**Assuming hidden fields always retain their data — or never do.** Both assumptions cause trouble. On surveys, a field hidden by branching logic loses its value silently, so a respondent who backtracks loses downstream answers. On data entry forms the user is prompted and may cancel, which means a hidden field *can* still hold a value. That second case is why Data Quality rule F (hidden fields containing values) exists and routinely finds records. Note that fields hidden by the `@HIDDEN` action tag family are a separate mechanism: those keep their values and continue to calculate. Test all logic thoroughly in Development mode before collecting real data.

**Applying branching logic in Production without testing.** The Online Designer's syntax checker validates that logic is syntactically correct, but it does not verify that it behaves as intended. Always test in a Development project or with test records before deploying.

**Confusing branching logic scope with instrument scope.** Branching logic only shows or hides individual fields. It cannot be used to show or hide an entire instrument.

**Expecting logic behavior to be the same in calculated fields.** Calculated fields use the same syntax but do not evaluate to true or false — they always return a number. The semantics are different even though the syntax looks similar.

---

## 9. Design Patterns

### 9.1 Checkbox Gate (Participation / Intent Gate)

A common survey design pattern is to place a single checkbox at the top of a form — labelled something like "Yes, I would like to participate" or "I confirm I want to proceed" — and then apply `[gate_field(1)]=1` as the branching logic condition on every subsequent field. This has the effect of hiding all questions until the respondent explicitly opts in. Note that marking the gate checkbox itself as required achieves nothing: REDCap ignores the required flag on checkbox fields, so the gate can be left unticked and the form still submitted. See [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md).

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

## 10. Related Articles

- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (the logic language and writing your first statement)
- [RC-BL-03 — Branching Logic: Combining Statements](RC-BL-03_Branching-Logic-Combining-Statements.md) (AND, OR, parentheses)
- [RC-BL-04 — Branching Logic: Structured Fields & Checkboxes](RC-BL-04_Branching-Logic-Structured-Fields-and-Checkboxes.md)
- [RC-FD-02 — Online Designer](RC-FD-02_Online-Designer.md) (where branching logic is configured)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (alternative location for writing logic in bulk)
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (explains how branching logic appears from the data entry user's perspective)
- [RC-FD-09 — Field Embedding: Advanced Layout Patterns & Workflow Design](RC-FD-09_Field-Embedding-Advanced-Patterns-and-Workflow-Design.md) (related pattern: embedding sub-fields inside radio choice labels alongside branching logic)

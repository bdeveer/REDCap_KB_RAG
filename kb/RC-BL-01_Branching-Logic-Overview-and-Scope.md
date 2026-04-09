RC-BL-01

**Branching Logic — Overview & Scope**

| **Article ID** | RC-BL-01 |
|---|---|
| **Domain** | Branching Logic |
| **Applies To** | All REDCap project types; requires Project Design and Setup rights |
| **Prerequisite** | RC-FD-02 — Online Designer |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-BL-02 — Syntax & Atomic Statements; RC-BL-03 — Combining Statements; RC-BL-04 — Structured Fields & Checkboxes; RC-FD-02 — Online Designer |

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

> **Note:** Calculated fields and action tags use the same logic syntax but do not produce a true/false outcome. Calculated fields always return a number. Action tags use the syntax for a range of non-boolean purposes. Calculated fields are covered in RC-CALC-02 — Calculated Fields *(coming soon)*. Action tags that use logic syntax are covered in the RC-AT series — start with RC-AT-01 — Action Tags Overview.

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

- Logic syntax elements: operators, brackets, quotes, boolean operators (RC-BL-02)
- Writing atomic (single-condition) logic statements (RC-BL-02)
- Combining statements with AND, OR, and parentheses (RC-BL-03)
- Writing logic for structured field types including checkboxes (RC-BL-04)

The following topics are outside the scope of this series. Each has its own dedicated article:

- Calculated fields and calculation syntax — RC-CALC-02 — Calculated Fields *(coming soon)*
- Action tags that use logic syntax — RC-AT-01 — Action Tags Overview (start here for the full series)
- Smart variables — RC-PIPE-03 — Smart Variables Overview
- Field embedding (curly bracket syntax) — RC-FD-07 — Field Embedding
- Event-based logic in longitudinal projects — RC-BL-05 — Branching Logic in Longitudinal Projects
- REDCap functions (e.g., datediff, rounddown) — RC-CALC-01 — Special Functions Reference

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

# 9. Related Articles

- RC-BL-02 — Branching Logic Syntax & Atomic Statements (the logic language and writing your first statement)
- RC-BL-03 — Combining Logic Statements (AND, OR, parentheses)
- RC-BL-04 — Branching Logic for Structured Fields & Checkboxes
- RC-FD-02 — Online Designer (where branching logic is configured)
- RC-FD-03 — Data Dictionary (alternative location for writing logic in bulk)
- RC-DE-02 — Basic Data Entry (explains how branching logic appears from the data entry user's perspective)

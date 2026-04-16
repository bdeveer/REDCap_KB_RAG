RC-DQ-01

**Data Quality Module**

| Field | Value |
|---|---|
| Article ID | RC-DQ-01 |
| Domain | Data Quality |
| Applies To | All REDCap projects |
| Prerequisite | RC-DE-02 — Basic Data Entry |
| Version | 1.2 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-BL-01 — Branching Logic: Overview & Scope; RC-BL-02 — Branching Logic: Syntax & Atomic Statements; RC-CALC-01 — Special Functions Reference; RC-CALC-02 — Calculated Fields |

---

# 1. Overview

The Data Quality module is a project-level tool that lets authorized users check their data for discrepancies. It provides a set of built-in default rules covering common data problems (blank required fields, out-of-range values, hidden fields retaining data, calculated field mismatches) and allows users to write their own custom rules using the same logic syntax as branching logic. Rules can be run on demand across all project records, or triggered automatically in real time whenever a data entry form is saved. Custom rules can be exported to CSV and imported from CSV, making it straightforward to migrate rule sets between projects or manage them in bulk. This article covers how to access and use the module, how the default rules work, how to write and configure custom rules, how to import and export rules, and how to interpret and manage results.

---

# 2. Key Concepts & Definitions

## Default Rules

Pre-built rules provided by REDCap that check for the most common categories of data discrepancy. Default rules (displayed in red text in the module) cannot be modified, reordered, or deleted. They are optional — you choose whether to execute them.

## Custom Rules

User-defined rules written using branching logic syntax that evaluate to true or false against each record. Any record for which the rule evaluates to true is returned as a discrepancy. Custom rules can be created, edited, reordered, deleted, exported, and imported.

## Discrepancy

A record (or record-event-instance combination) that a rule has identified as meeting the rule's condition. A discrepancy is not an error in the technical sense — it means the rule's logic evaluated to true for that record. Whether that represents a real data problem depends on the rule.

## Real-Time Execution

An optional setting on each custom rule that causes it to run automatically whenever a user saves a data entry form. If a violation is detected, REDCap displays a warning pop-up identifying the violated rules and the fields involved.

## Exclusion

A record-level flag that suppresses a specific discrepancy from appearing in future rule results. Excluded discrepancies are not deleted — they can be viewed and un-excluded at any time. Exclusion is appropriate when a discrepancy is known and expected (e.g., a legitimately missing required value due to eligibility).

## Rule H

The built-in default rule that detects calculated fields whose stored database value differs from their currently computed value. This mismatch can occur after a calculated field's formula is changed or after a data import that affects fields the calculation depends on. Rule H includes an auto-correct function that rewrites all affected stored values project-wide.

---

# 3. Accessing the Module & Executing Rules

The Data Quality module is found under **Applications** in the left-hand project menu.

The module displays all available rules in a table — default rules at the top (in red text), followed by any custom rules the project has defined. To run rules:

- Click **Execute** next to an individual rule to evaluate that rule across all project records.
- Use one of the bulk execution buttons to run multiple rules at once (see below).

After execution, REDCap shows a count of discrepancies found for each rule. Click **View** next to any rule to see the specific records (and event/instance details for longitudinal or repeating projects) that triggered it.

### Bulk Execution Options (REDCap 16+)

Starting in REDCap 16, three bulk execution options are available instead of a single "Execute All" button:

| Button | What It Runs |
|---|---|
| **Run all rules** | All default rules (A–H) and all custom rules |
| **Run all rules except A & B** | All default rules except Required Fields (A) and Identifier Fields (B), plus all custom rules |
| **Run all custom** | Custom rules only — default rules are skipped |

"Run all rules except A & B" is useful for routine data checks where identifier and required-field coverage is handled separately (e.g., by a dedicated data manager review), saving time on large datasets.

### Field Selector for Standard Rules (REDCap 16+)

Also introduced in REDCap 16, a field selector allows you to limit which fields the standard default rules are evaluated against. Instead of running a rule across every field in the project, you can select a specific field or a small set of fields. This is particularly useful for large projects where running a rule across all fields is slow — narrowing the scope to only the fields of interest significantly reduces completion time.

### User Rights

Users must have the **Data Quality** user right to access the module. Users without view or edit access to specific instruments will not see data from those instruments in discrepancy results, even if those fields are involved.

### Data Access Groups

If the project uses Data Access Groups (DAGs), discrepancy results are automatically filtered by group. Users assigned to a DAG see only discrepancies belonging to their own group. Users not assigned to a DAG (typically administrators) see discrepancies stratified by group.

---

# 4. Default Rules (A–H)

REDCap includes eight pre-defined default rules. They appear in red text and cannot be modified, reordered, or removed. Each covers a distinct category of data problem:

| Rule | What It Checks |
|---|---|
| A | Required fields that have been left blank |
| B | Fields marked as identifiers that contain data |
| C | Number-validated fields with values outside their specified min/max range |
| D | Date/datetime-validated fields with values outside their specified min/max range |
| E | Calculated fields whose stored value is blank |
| F | Multiple-choice fields with a saved value that no longer matches any current answer choice (occurs when choices are edited after data collection) |
| G | Fields currently hidden by branching logic that still have a saved value |
| H | Calculated fields whose stored value differs from their currently computed value |

> **Note:** Not all rules are relevant to every project. Rules B and E, for example, may produce no results if the project has no identifier-designated fields or no calculated fields, respectively.

---

# 5. Custom Rules

Custom rules extend the module beyond the defaults. They are written using the same syntax as branching logic and must evaluate to a boolean result (true or false). Any record for which the rule evaluates to true is flagged as a discrepancy.

### Syntax

Custom rule logic uses the same variable reference and operator conventions as branching logic:

- Field names are placed in square brackets: `[field_name]`
- For longitudinal projects, prepend the event name to target a specific event: `[event_name][field_name]`
- Standard comparison operators apply: `=`, `<>`, `<`, `>`, `<=`, `>=`
- Logical operators: `and`, `or`, `not`
- Special functions from RC-CALC-01 — Special Functions Reference may be used (e.g., `datediff`, `if`, `round`)

**Example:** Flag records where a participant is over 65 but the geriatric assessment instrument is blank:

```
[age] > 65 and [geriatric_screen] = ""
```

### Constraint

A custom rule must always evaluate to true or false — not to a numeric value. This is the key distinction from a calculated field, which must produce a number. The logic syntax is the same; the expected output type is different.

### Managing Custom Rules

Custom rules can be created, edited, deleted, and reordered from the bottom of the Data Quality module table. Order affects how rules appear in results and in the pop-up displayed during real-time execution.

---

# 6. Importing and Exporting Custom Rules

REDCap can export all custom rules from a project to a CSV file, and can import custom rules from a CSV file in the same format. This is useful for migrating rules between projects, maintaining a versioned rule set outside REDCap, or creating rules in bulk.

Default rules (A–H) are not included in the export — only custom rules are exported and importable.

### CSV Format

The export and import file uses a three-column CSV with a header row:

| Column | Description | Accepted Values |
|---|---|---|
| `rule_name` | Display name shown in the Data Quality module table | Any text string |
| `rule_logic` | The boolean logic expression for the rule | Valid REDCap branching logic syntax |
| `real_time_execution` | Whether to enable real-time execution for this rule | `y` to enable; empty or `n` to disable |

**Example file:**

```csv
rule_name,rule_logic,real_time_execution
"Age out of range","[age] < 0 or [age] > 120",n
"Consent missing for enrolled","[enrolled] = '1' and [consent_date] = ''",y
"Field not empty","[abs_rater_disc] <> """,y
```

### CSV Escaping for Empty-String Comparisons

REDCap rule logic frequently uses `""` to represent an empty string (e.g., `[field] <> ""` to check whether a field has a value). Because the entire `rule_logic` cell is enclosed in double quotes in the CSV, every literal `"` inside the cell must be escaped by doubling it.

The pattern is: one pair of double quotes in REDCap logic (`""`) becomes two pairs in the CSV cell (`""""`).

| REDCap logic | CSV cell value |
|---|---|
| `[field] <> ""` | `"[field] <> """"`  |
| `[field] = ""` | `"[field] = """"` |

Most spreadsheet applications handle this automatically when you save as CSV. If constructing the file programmatically or in a plain text editor, apply this escaping manually.

### Importing Rules

To import, navigate to the Data Quality module and use the import option. REDCap will add the imported rules to the bottom of the existing custom rule list — it does not replace existing rules. Review imported rules after loading to confirm logic and real-time settings are correct before executing.

> **Note:** Importing does not validate rule logic before saving. A rule with a syntax error will be imported but will fail when executed. Test imported rules individually before running them across the full dataset.

---

# 7. Real-Time Execution

Each custom rule has a **Real-Time Execution** checkbox. When enabled:

1. Every time a user clicks **Save** on a data entry form, REDCap evaluates all real-time-enabled rules against the record being saved — silently, in the background.
2. If any rule is violated, a warning pop-up appears listing the violated rules and the specific fields involved with their current values.
3. If no rules are violated, the form saves normally with no pop-up.

The user can acknowledge the warning and proceed — real-time execution is advisory, not blocking. Individual results displayed in the pop-up can be excluded so they will not appear again on future saves, even if the condition persists.

> **Important:** Real-time execution works only on **data entry forms**. It is not available for surveys. A user completing a survey will never see a data quality pop-up, regardless of rule configuration.

---

# 8. Excluding Discrepancies

Any individual discrepancy in the results list can be excluded. Excluding a discrepancy:

- Removes it from the count the next time the rule is executed
- Does not delete the underlying data
- Does not prevent the rule from detecting the same condition in other records

Excluded discrepancies are accessible at any time via the **view** link at the top of the results table for that rule. They can be un-excluded if the situation changes and the discrepancy should once again appear in results.

Exclusion is appropriate when a discrepancy reflects a known and accepted condition — for example, a required field that is intentionally left blank because the question was not applicable.

---

# 9. Rule H: Correcting Calculated Fields

Rule H deserves separate attention because it serves a specific remediation function — not just detection.

**When Rule H fires:** A calculated field's stored value (what is saved in the database) no longer matches what REDCap would compute if it recalculated the field today. Common causes:

- The calculated field's formula was edited after data was already collected
- A data import updated fields that calculated fields depend on, but did not trigger recalculation
- Records were created before a calculated field was added to the project

**How to use Rule H:**

1. Execute Rule H. REDCap returns a count of affected records.
2. Click **View** to see the specific records and fields.
3. An **Auto-correct** button appears. Clicking it recalculates and overwrites the stored value for all affected records project-wide.

> **Important:** Auto-correct updates all flagged calculated fields simultaneously across the entire project. Review the list of affected records before clicking. This action cannot be undone through the interface — it overwrites stored values.

> **Yale-specific:** [Note whether local policy requires supervisor review or audit trail documentation before running auto-correct in Production — leave blank until confirmed with Yale REDCap support team]

---

# 10. Common Questions

**Q: Do I need special user rights to access Data Quality?**
A: Yes. A user must have the Data Quality user right assigned in their project role. Users without this right will not see the module in the Applications menu.

**Q: Can I use special functions like `datediff()` in a custom rule?**
A: Yes. All special functions listed in RC-CALC-01 — Special Functions Reference are available in custom rule logic, just as they are in calculated fields.

**Q: Why does a real-time execution pop-up appear even after I've excluded the result?**
A: Real-time exclusions are per-record and per-rule. If the exclusion was applied to one record, it will not suppress the same violation on a different record. Verify that the exclusion was applied to the correct record.

**Q: Can surveys trigger real-time data quality rules?**
A: No. Real-time execution only fires when a user saves a data entry form through the normal REDCap interface. Survey submissions do not trigger real-time data quality checks.

**Q: My calculated field values look wrong after I changed the formula. What should I do?**
A: Run Rule H. It will identify all records where the stored value no longer matches the current formula. Use the Auto-correct button to update them all at once.

**Q: Can a user in a Data Access Group see discrepancies from other groups?**
A: No. Users assigned to a DAG see only discrepancies from their own group's records. Project administrators not assigned to a DAG see discrepancies stratified by group.

**Q: What happens if a field referenced in a custom rule is deleted from the project?**
A: The rule will likely fail to execute or return an error. Rules referencing deleted or renamed fields should be updated or removed from the Data Quality module.

**Q: Can I run Data Quality rules via the API?**
A: No. The Data Quality module does not expose rule execution through the REDCap API. Rules must be executed from the module interface.

**Q: Can I copy custom rules from one project to another?**
A: Yes. Export the rules from the source project as a CSV, then import that CSV into the destination project. Review and adjust any field names or event references that differ between projects before importing.

**Q: Does importing rules overwrite my existing custom rules?**
A: No. Importing appends the new rules to the bottom of the existing custom rule list. Existing rules are not modified or removed.

**Q: My project has hundreds of fields and running rules is slow. Is there a faster way?**
A: In REDCap 16 and later, use the field selector to limit standard default rules to specific fields rather than running them across the entire project. You can also use the "Run all custom" button to skip default rules entirely if only custom rule results are needed.

**Q: What is the difference between "Run all rules except A & B" and "Run all custom"?**
A: "Run all rules except A & B" still runs default rules C through H alongside all custom rules — it only skips the Required Fields (A) and Identifier Fields (B) checks. "Run all custom" skips all default rules and runs only the rules you have written yourself.

---

# 11. Common Mistakes & Gotchas

**Writing a rule that returns a value instead of true/false.** A custom rule must evaluate to a boolean. Writing `[bmi]` as a rule (which returns a number) will not work as expected. The rule must be a comparison: `[bmi] > 30`. If the rule produces no discrepancies or behaves unexpectedly, check that the logic resolves to true or false, not a numeric or text value.

**Clicking Auto-correct in Rule H without reviewing the affected records first.** Auto-correct rewrites calculated field values for every flagged record simultaneously. If the formula change was intentional but only applies to new records going forward, running Auto-correct will also update historical records — which may not be desired. Always review the Rule H results list before correcting.

**Assuming a pop-up means data was not saved.** Real-time execution warnings are advisory. REDCap still saves the record even when a violation is detected. The pop-up is a notification, not a block. Users may dismiss it and continue — the data is already saved.

**Excluding a discrepancy and expecting it to disappear from Rule H.** Rule H exclusions suppress the discrepancy from appearing in results but do not correct the underlying value mismatch. The stored value is still wrong. Use Auto-correct to fix the values; use exclusions only when the mismatch is known and acceptable.

**Expecting real-time rules to fire on survey completions.** Real-time execution is a data entry feature. Projects that collect data primarily via surveys will not benefit from real-time Data Quality rules unless data entry staff also use the form interface for review or corrections.

**Forgetting to escape double quotes when building the import CSV manually.** If you construct a rules CSV in a text editor or programmatically, empty-string comparisons in rule logic (`""`) must be written as `""""` inside a CSV-quoted field. Failing to escape them will cause the CSV parser to misread the row, resulting in a malformed or truncated rule. When building these files in code, use a proper CSV library rather than string concatenation to handle escaping automatically.

**Importing rules without testing them first.** REDCap does not validate rule logic on import — a rule with a syntax error will be saved but will fail when executed. After importing, execute each rule individually on a small dataset or test project before running across full production data.

---

# Related Articles

- RC-BL-01 — Branching Logic: Overview & Scope (custom rules use identical syntax)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (syntax reference for writing rules)
- RC-CALC-01 — Special Functions Reference (special functions available in custom rule logic)
- RC-CALC-02 — Calculated Fields (context for Rule H and calculated field behavior)
- RC-DE-02 — Basic Data Entry (context for real-time execution during form saves)
- RC-DE-04 — Editing Data & Audit Trail (audit trail behavior after Auto-correct)
- RC-DAG-01 — Data Access Groups (DAG filtering of discrepancy results)
- RC-USER-01 — User Rights: Overview (Data Quality user right)

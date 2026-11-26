---
id: RC-FD-12
title: Dynamic SQL Field Type
domain: Form Design
applies_to:
- All REDCap project types
- requires REDCap administrator access to create or modify
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Dynamic
  SQL field behaviour checked against source code; pages not re-captured
prerequisites:
- RC-FD-01 — Form Design Overview
- RC-FD-03 — Data Dictionary
version: '1.1'
last_updated: 2026-11
related:
- id: RC-FD-08
  title: 'Data Dictionary: Column Reference & Advanced Techniques'
- id: RC-CC-17
  title: 'Control Center: Database Query Tool'
tags:
- form design
- instruments
synonyms:
- what is a dynamic sql field
- dropdown populated by a sql query
- pull dropdown options from the database
- dsql field type in redcap
- list records from another project in a dropdown
- sql driven dropdown choices
- can dynamic sql auto-populate other fields
- how to set up a sql field type
---

# 1. Overview

Dynamic SQL (DSQL) is a special dropdown field type in REDCap where the list of selectable options is driven by the results of a SQL query against the REDCap backend database — rather than a fixed list of choices defined in the Data Dictionary. The query runs each time the page loads, pulling whatever values are currently in the source table and presenting them to the user as a standard dropdown.

Because DSQL fields query the database directly, they are significantly more powerful than ordinary dropdowns. They can pull participant records from another REDCap project, reference the user table to list project team members, or draw from any custom lookup table that has been loaded into the database — such as MedDRA term lists, institutional department directories, or procedure code tables.

DSQL appears in the Data Dictionary with field type `sql`. Non-administrator users see and use a DSQL field like any other dropdown during data entry, but they cannot choose the `sql` field type or edit an existing DSQL field in the Online Designer (the field shows a "CANNOT MODIFY 'SQL' FIELD" notice). Only REDCap administrators can create a DSQL field or change its query; Section 3.1 explains what non-administrators can still do with a Data Dictionary that contains DSQL fields.

> **Scope note — what DSQL cannot do:** DSQL populates the dropdown's option list only. It does not push data into other fields when a selection is made, and it does not trigger any downstream logic or auto-fill behavior. A common misconception is that DSQL can act as a lookup: the user selects a participant from the dropdown and other fields (name, date of birth, site) automatically populate. DSQL cannot do this. Functionality of that kind requires a custom external module or a Data Entry Trigger combined with API calls — and even with those approaches, achieving a seamless real-time experience is technically difficult given the way REDCap loads and renders pages.

> **Institution-specific:** There is no on/off setting for DSQL — any REDCap administrator can create a DSQL field. Institutions often have a local policy on who writes these queries and when they are allowed, and building and maintaining SQL queries requires database and SQL skills that not all administrators possess. Check with your REDCap administrators before designing a workflow that depends on DSQL.

---

# 2. Key Concepts & Definitions

## Dynamic SQL vs. Standard Dropdown

A standard `dropdown` field has a fixed choice list defined in Column F of the Data Dictionary — the options never change unless a designer edits and re-uploads the Data Dictionary. A DSQL field has no fixed choices; instead, it runs a SQL query at page load and builds its choice list from the query results. This makes DSQL well-suited for scenarios where the available options are themselves stored as data.

## Required Query Output Format

A DSQL query should return two columns per row:

1. **Raw value** — the value that is stored in REDCap when the user selects this option. This becomes the stored field value and is what branching logic and calculated fields evaluate.
2. **Label** — the human-readable text displayed to the user in the dropdown.

If the query returns only one column, that column is used as both the raw value and the label. Any columns after the second are ignored.

The query must begin with `SELECT`. Anything else at the start — a leading `--` comment, a `WITH` clause, or an opening parenthesis — gives an empty dropdown.

This mirrors the `raw_value, Display Label` format used in ordinary dropdown and radio choice lists. How the query arrives at these two columns — via joins, concatenation, filtering, or any other SQL logic — does not matter, as long as the output conforms to this structure.

## Page-Load Behavior

The DSQL query executes when the page (form or survey) loads. The dropdown is populated with whatever the query returns at that moment. If the source data changes after the page has loaded — for example, a new participant is added to the source project — the DSQL dropdown on the currently open page will not reflect that change. The user must reload the page to get a fresh query result.

This is an important workflow consideration: in high-throughput data entry scenarios where new source records are being added continuously, users should be instructed to reload the page before selecting from a DSQL field.

## Auto-Complete

DSQL fields can use REDCap's dropdown auto-complete feature, which allows users to type partial text to filter the visible options. It is optional: tick the auto-complete checkbox when editing the field in the Online Designer, or put `autocomplete` in the Text Validation Type column of the Data Dictionary. Turn it on for any DSQL field with more than a handful of options.

---

# 3. Administrator Responsibilities

## 3.1 Who Can Create or Edit DSQL Fields

Creating a DSQL field or changing its query requires REDCap administrator access. This restriction applies in all contexts:

- The Online Designer does not expose the `sql` field type to non-administrators. It cannot be selected from the field type menu by regular users, and existing DSQL fields cannot be edited by them.
- A non-administrator **can** upload a Data Dictionary that contains the project's existing DSQL fields, as long as each field's query in Column F (Choices, Calculations, OR Slider Labels) is unchanged. Other columns of those rows — field label, branching logic, field annotation and so on — can be changed.
- The upload is blocked if it adds a new DSQL field or changes the query of an existing one. The error tells the user to set Column F back to its original value.
- When an administrator uploads a Data Dictionary that adds or changes a DSQL query, REDCap shows a warning asking them to review the query before committing the changes.

> **Practical note for project teams:** Download the current Data Dictionary, make your changes, and leave Column F of every `sql` row exactly as it was. If you need a new DSQL field, add it as an ordinary `dropdown` with a placeholder choice (or leave it out) and ask your REDCap administrator to set the field type and query.

> **Version caveat (17.x, not 16 LTS):** When a non-administrator copies and pastes fields in the Online Designer, any DSQL field among them is refused with the message "SQL fields can only be added by REDCap admins". Ask an administrator to add the DSQL field instead.

> **Version caveat (17.x, not 16 LTS):** Project-level administrators (members of a Project Admin Group) are treated as non-administrators for DSQL: they cannot create or edit DSQL fields. Only a full REDCap administrator can. On 16 LTS, which has no Project Admin Groups, this does not arise. If you are a project-level administrator, route DSQL requests to a full administrator.

## 3.2 SQL Access Requirements

Writing a DSQL query requires knowledge of the REDCap backend database schema and SQL skills. The administrator must know which tables to query, what the relevant field names are, and how to join tables correctly. REDCap's database structure is stable across minor versions, but administrators should validate queries after major REDCap version upgrades.

The Control Center Database Query Tool ([RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md)) can be used to test and validate queries before embedding them in a DSQL field. It resolves smart variables such as `[data-table]` and `[project-id]`, but it has no record context, so `[record-name]` and other record-specific values come through blank there.

---

# 4. Common Use Cases

DSQL is most useful in three broad scenarios:

**Cross-project lookups** — pulling records from one REDCap project to use as selectable options in another. For example, a registration project holds a list of enrolled participants, and a data entry project uses a DSQL field to let staff select a participant by ID and name rather than typing freehand.

**User-driven dropdowns** — querying the REDCap user table to produce a list of users currently assigned to a project. This is useful for assignment fields (e.g., "Assigned to:") that should automatically reflect the current team without manual maintenance.

**External reference tables** — querying a custom lookup table that has been loaded into the REDCap database. Common examples include drug dictionaries, diagnosis code lists (such as MedDRA), department or site directories, and procedure code tables. These tables are typically loaded and maintained by the REDCap administrator outside of the normal project interface.

---

# 5. SQL Query Guidelines

## 5.1 Output Structure

The query must start with `SELECT` and should produce two columns in this order (a single column is used as both value and label; extra columns are ignored):

| Column | Purpose |
|--------|---------|
| First column | Raw value — stored in REDCap when selected |
| Second column | Label — shown to the user in the dropdown |

Use `SELECT a.value, <label_expression> AS label ...` as your basic pattern. Column names in the output do not matter — only position matters.

## 5.2 Querying REDCap Data

Project field values are stored in REDCap's data table(s) in an entity-attribute-value structure. To pull data from a specific project and field, filter on both `project_id` and `field_name`. Always use the `[data-table]` smart variable instead of hardcoding the table name — see Section 5.5.

```sql
SELECT record, value
FROM [data-table]
WHERE project_id = [project-id]
AND field_name = 'your_field_name'
```

To build a meaningful label from multiple fields, use `JOIN` statements to combine values across field names for the same record, then format them with `CONCAT_WS` or similar string functions.

## 5.3 Filtering Results

You can filter query results using any standard SQL `WHERE` clause logic. A particularly useful pattern is the **self-curating list**: filtering out records that have already been processed or linked in another project. This keeps the dropdown from growing unbounded and only shows records that are still actionable.

## 5.4 Ordering Results

Always include an `ORDER BY` clause. Without explicit ordering, the sequence of options in the dropdown is non-deterministic and may change between page loads.

## 5.5 The `[data-table]` Smart Variable

Older REDCap installations stored all project data in a single `redcap_data` table. As installations grew, REDCap introduced the ability to split data across multiple sub-tables (e.g., `redcap_data`, `redcap_data_1`, `redcap_data_2`, and so on) to improve performance at scale. A given project's records may live in any of these tables depending on how the installation is configured.

This means a DSQL query that hardcodes `FROM redcap_data` may be querying the wrong table and returning no results — or incorrect results — on installations that use sub-tables.

REDCap solves this with the `[data-table]` smart variable, which REDCap resolves to the correct table name before executing the query. **Always use `[data-table]` instead of hardcoding a table name.**

**Syntax:**

| Smart Variable | Resolves to |
|----------------|-------------|
| `[data-table]` | The data table for the **current project** (the project the DSQL field belongs to) |
| `[data-table:NNNN]` | The data table for **project ID NNNN** (a different project) |

Use `[data-table]` when the DSQL queries its own project's data. Use `[data-table:NNNN]` when querying data from a different project, substituting the actual numeric project ID for `NNNN`.

Querying the current project's own data:

```sql
SELECT record, value
FROM [data-table]
WHERE project_id = [project-id]
AND field_name = 'your_field_name'
```

Querying data from a different project (project ID 1234):

```sql
SELECT record, value
FROM [data-table:1234]
WHERE project_id = 1234
AND field_name = 'your_field_name'
```

> **Note:** When using `[data-table:NNNN]`, also include the matching `project_id = NNNN` filter in the `WHERE` clause. The smart variable resolves the table name; the `project_id` filter ensures you are selecting the right records within that table.

## 5.6 Other Smart Variables in DSQL Queries

Beyond `[data-table]`, other contextual REDCap smart variables can be embedded in a DSQL SQL statement. REDCap resolves them to their current values before executing the query, making it possible to write queries that respond to the context in which the DSQL field is being displayed.

Commonly useful smart variables in DSQL queries:

| Smart Variable | Resolves to |
|----------------|-------------|
| `[project-id]` | The numeric project ID of the current project |
| `[record-name]` | The record ID of the record currently being viewed |
| `[event-id]` | The numeric ID of the current event (longitudinal projects) |
| `[event-name]` | The unique name of the current event (longitudinal projects) |
| `[record-dag-name]` | The unique name of the current record's Data Access Group |

**Do not wrap these in quotes.** REDCap inserts `[record-name]`, `[event-id]`, `[event-name]` and `[record-dag-name]` already quoted, so write `WHERE record = [record-name]`, not `WHERE record = '[record-name]'`. `[project-id]` and `[data-table]` are inserted as plain values (a number and a table name).

**Where there is no current record.** On pages that are not tied to one record — reports, data exports that show labels, Data Quality, blank instrument PDFs and the Codebook — `[record-name]` resolves to blank. A query filtered only on `record = [record-name]` then returns nothing there. To fall back to the full list when there is no record, write the filter as `if([record-name] = '', 1=1, record = [record-name])`.

**Examples of when this is useful:**

- Use `[project-id]` instead of hardcoding the project ID when the DSQL queries its own project's data. This makes the query portable — if the project is copied or migrated, the query still resolves correctly without manual edits.
- Use `[record-name]` to filter query results to data associated with the current record. For example, a DSQL could present only the visits or specimens that belong to the record being entered, rather than the full list across all records.
- Use `[event-id]` or `[event-name]` to restrict results to data collected at a particular event, useful when a longitudinal project stores event-specific lookup data.

Example — query the current project's own data without hardcoding the project ID:

```sql
SELECT record, value
FROM [data-table]
WHERE project_id = [project-id]
AND field_name = 'your_field_name'
ORDER BY value;
```

> **Cross-reference:** See [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) for a full reference on available smart variables and their syntax.

---

# 6. SQL Examples

## Example 1: Participant Lookup with Name Label

This query pulls a participant identifier from one project and builds a label that combines the identifier with the participant's first and last name. The result appears in the dropdown as `P-1001 - Jane Smith`.

The raw value is the participant identifier; the label combines the identifier with the full name. Replace `1234` with the numeric project ID of the source project and the `field_name` values with the actual field names in that project. `[data-table:1234]` resolves to the correct data table for project 1234. Paste the query exactly as shown — it must begin with `SELECT`, so do not put comments above it.

```sql
SELECT
    a.value,
    CONCAT_WS(' - ', a.value, CONCAT_WS(' ', b.value, c.value)) AS label
FROM
    (SELECT record, value
     FROM [data-table:1234]
     WHERE project_id = 1234
       AND field_name = 'participant_id') a
JOIN
    (SELECT record, value
     FROM [data-table:1234]
     WHERE project_id = 1234
       AND field_name = 'first_name') b
    ON a.record = b.record
JOIN
    (SELECT record, value
     FROM [data-table:1234]
     WHERE project_id = 1234
       AND field_name = 'last_name') c
    ON a.record = c.record
GROUP BY a.value
ORDER BY a.value;
```

## Example 2: Self-Curating List (Only Unlinked Participants)

This query shows only participants from a source project who have not yet been linked in the target (current) project. As staff process participants and record their IDs in the target project, those participants disappear from the dropdown automatically on the next page load. This prevents double-assignment without requiring any manual maintenance of the choice list.

Replace `1234` with the numeric project ID of the source project and the `field_name` values with the actual field names in each project. `study_id` is the identifier in the source project; `linked_participant_id` is the field in the current project that holds the linked ID (the raw value from this dropdown once selected). `[data-table:1234]` resolves the source project's data table and `[data-table]` the current project's. As with Example 1, the query must begin with `SELECT`.

```sql
SELECT
    a.value,
    CONCAT_WS(', ', a.value, b.value) AS label
FROM
    (SELECT DISTINCT record, value
     FROM [data-table:1234]
     WHERE project_id = 1234
       AND field_name = 'study_id') a
JOIN
    (SELECT record, value
     FROM [data-table:1234]
     WHERE project_id = 1234
       AND field_name = 'last_name') b
    ON a.record = b.record
LEFT JOIN
    (SELECT record, value
     FROM [data-table]
     WHERE project_id = [project-id]
       AND field_name = 'linked_participant_id') c
    ON a.record = c.value
WHERE c.record IS NULL
ORDER BY a.value;
```

> **How the self-curating filter works:** The `LEFT JOIN` connects source records to any matching value in the target project's linking field. The `WHERE c.record IS NULL` condition then keeps only source records for which no matching entry was found in the target — i.e., records not yet linked. Once a source participant's ID is saved into `linked_participant_id` in the target project, they will no longer appear in the dropdown.

---

# 7. Performance Considerations

DSQL queries execute synchronously at page load. Slow or broad queries will delay the page from rendering for the user.

**Limit result set size.** Large option lists slow the dropdown and make it harder to use even with auto-complete. As a rough guideline, DSQL dropdowns with several hundred or more options will noticeably affect page load time. Filter the query to return only the options that are genuinely relevant at any given time.

**Multiple DSQL fields on one page are cumulative.** Each DSQL field on an instrument runs its own query at page load. Two or three DSQL fields on the same instrument will add up. Avoid placing multiple broad DSQL queries on the same page.

**Use indexes where possible.** If a DSQL is querying a custom lookup table, ensure the table is indexed on the columns used in the `WHERE` and `JOIN` clauses. REDCap's own tables (`redcap_data`) are indexed on `project_id` and `field_name`, which is why filtering on both is important.

**Test query performance before deploying.** Use the Database Query Tool ([RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md)) to run the query and review execution time before embedding it in a production project.

---

# 8. Common Questions

**Q: Can DSQL populate other fields automatically when the user makes a selection?**

**A:** No. DSQL controls only the contents of the dropdown option list. It does not push data into other fields, trigger calculations, or auto-fill anything when a user selects an option. This is a common expectation — particularly from users who want a "lookup" experience where selecting a participant from a dropdown fills in their name, site, or other details. That kind of behavior is outside what DSQL can do. Achieving it would require a custom external module, or a Data Entry Trigger combined with API calls to write values back into the record after a save. Even with those approaches, making the fill-in feel instantaneous and seamless is technically difficult because of how REDCap renders pages.

**Q: Can I use DSQL in a survey?**

**A:** Yes, DSQL fields work in surveys. The query runs when the survey page loads, just as it does in data entry mode. Be aware that survey participants typically cannot log back in and reload pages the way data entry staff can, so the page-load snapshot limitation is more consequential in survey contexts. DSQL in public surveys is generally not recommended unless the source data is stable.

**Q: Can branching logic reference a DSQL field?**

**A:** Yes. A DSQL field stores its selected value like any other dropdown — branching logic can reference it using the standard `[field_name] = 'raw_value'` syntax.

**Q: Can calculated fields reference a DSQL field?**

**A:** Yes, with the same caveats as any dropdown. The raw value stored by the DSQL selection is what the calculation formula will use.

**Q: Will the DSQL update if the source project data changes while the form is open?**

**A:** No. The dropdown is populated once at page load and does not refresh automatically. Users who need current data must reload the page.

**Q: Can I use DSQL on a longitudinal project?**

**A:** Yes. DSQL is a field type and is compatible with longitudinal projects. The query is not event-aware by default — it returns the same results regardless of which event the form is associated with — unless you filter it with `[event-id]` or `[event-name]` (Section 5.6).

**Q: Why can't I upload my Data Dictionary after adding a DSQL field?**

**A:** Only REDCap administrators can add a new DSQL field or change a DSQL query. If you are not an administrator, an upload that adds an `sql` row or changes the query in Column F of an existing one is blocked, and the error asks you to set Column F back to its original value. Ask your administrator to add the field or set the query.

**Q: Can I download and re-upload my project's Data Dictionary if it already contains DSQL fields?**

**A:** Yes. A non-administrator can upload a Data Dictionary that contains the project's existing DSQL fields, as long as each field's query in Column F is unchanged. You can change other columns of those rows, such as the field label, branching logic or field annotation. The safest approach is to start from a freshly downloaded Data Dictionary so Column F matches exactly.

**Q: What happens to DSQL fields when a project is copied or moved?**

**A:** Copying a project keeps the DSQL fields. The Copy Project page shows a notice with the number of Dynamic SQL fields and suggests checking whether their queries need changing to work in the new project — review any hardcoded project IDs in particular. The REDCap XML project export leaves out the dropdown options of DSQL fields, because they might include identifying data. In MyCap, a DSQL field is delivered as an ordinary dropdown with a fixed choice list.

> **Version caveat (17.x, not 16 LTS):** Project Migration (moving a project to another REDCap instance) converts DSQL fields into static dropdown fields; the notice on the migration page says so. After a migration, ask an administrator on the destination instance to set the field back to `sql` and enter a query if the list needs to stay dynamic.

---

# 9. Common Mistakes & Gotchas

**Returning the columns in the wrong order or number.** REDCap takes the first column as the raw value and the second as the label. A single column is used as both; any columns after the second are ignored. Select only what you need, in that order.

**Starting the query with something other than `SELECT`.** A leading `--` comment, a `WITH` clause or an opening parenthesis gives an empty dropdown. Put the query's explanation in the field note or a nearby descriptive field, or place comments after the `SELECT` line.

**Leaving Column F empty for an `sql` row.** A DSQL field needs a query in Column F of the Data Dictionary.

> **Version caveat (17.x, not 16 LTS):** The Data Dictionary upload warns "This Dynamic SQL field has no query provided in column F" for an `sql` row with an empty Column F. On 16 LTS there is no warning, so check every `sql` row has its query before uploading.

**Quoting smart variables.** `[record-name]`, `[event-id]`, `[event-name]` and `[record-dag-name]` are inserted already quoted; wrapping them in quotes yourself breaks the query. See Section 5.6.

**Making the record ID field a DSQL field.** The record ID field (the first field in the project) cannot be of type `sql`.

**No ORDER BY clause.** Omitting `ORDER BY` produces an unpredictably ordered dropdown that may present options in a different sequence on each page load. Always sort the output.

**Forgetting to filter on both `project_id` and `field_name`.** Querying `redcap_data` without both filters will return data from across the entire REDCap installation, producing an enormous and incorrect result set.

**Assuming the dropdown updates live.** The options are a snapshot taken at page load. Workflows that depend on real-time updates (e.g., a coordinator assigns a patient to a team member and expects a concurrent user's open form to immediately reflect the new availability) will not work as expected with DSQL.

**Hardcoding `redcap_data` instead of using `[data-table]`.** On installations that use data table sub-tables, a query written as `FROM redcap_data` may point to the wrong table and return no results. This is a silent failure — the DSQL field will simply appear empty. Always use `[data-table]` for the current project and `[data-table:NNNN]` for any other project. This also makes queries portable: if a project is migrated to a different installation or the table structure changes, the smart variable resolves correctly without requiring a manual query update.

**Building DSQL workflows without checking local policy.** Some institutions restrict who may write DSQL queries or when they are allowed. Confirm with your REDCap administrators before designing a workflow that depends on DSQL.

**Changing DSQL queries in the Data Dictionary as a non-administrator.** A non-administrator's upload is blocked if it adds an `sql` row or changes the query in Column F of an existing one; the error asks you to set Column F back to its original value. Other columns of DSQL rows can be changed. Ask an administrator for any change to the query itself.

**Not documenting SQL queries externally when they reference specific field names or table structures.** A DSQL query that joins on specific REDCap field names (e.g., filtering a user list by role or site using fields stored in the data table) silently breaks if those field names are ever renamed or the fields are moved. Unlike branching logic errors, a broken DSQL query produces no warning — the dropdown simply appears empty. For any DSQL field whose query references specific field variable names, role names, or project IDs, maintain an external record (a project documentation instrument, a README, or a comment in a nearby descriptive field) that identifies what the query depends on. Treat those field names and identifiers as frozen, and perform a DSQL audit whenever referenced fields are renamed or the data model changes.

**Hardcoding a numeric project ID in the WHERE clause when querying another project.** Even when `[data-table:NNNN]` is used correctly for the table name, it is easy to forget that the `project_id = NNNN` filter in the `WHERE` clause is still a hardcoded number. If the project is cloned, migrated to a different REDCap instance, or re-imported, the project ID will change but the WHERE clause will silently continue filtering on the old ID — returning either no results or the wrong records. Always document which external project ID a DSQL query targets, ideally in the field note or a nearby descriptive field (e.g., "SQL references project #1234 — update if migrated"). For cross-project queries, consider whether the target project is stable and long-lived before embedding its ID.

---

# 10. Related Articles

- [RC-FD-01 — Form Design Overview](RC-FD-01_Form-Design-Overview.md) (field type selection and form design tools)
- [RC-FD-03 — Data Dictionary](RC-FD-03_Data-Dictionary.md) (Data Dictionary upload workflow and safety practices)
- [RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques](RC-FD-08_Data-Dictionary-Column-Reference-and-Advanced-Techniques.md) (full column reference; notes on the `sql` field type code)
- [RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md) (tool for testing SQL queries before embedding them in a DSQL field)
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (how dropdown fields behave during data entry, including auto-complete)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (full reference for smart variables usable in DSQL queries)

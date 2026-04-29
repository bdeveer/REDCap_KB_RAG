RC-FD-12

**Dynamic SQL Field Type**

| **Article ID** | RC-FD-12 |
| --- | --- |
| **Domain** | Form Design |
| **Applies To** | All REDCap project types; requires REDCap administrator access to create or modify |
| **Prerequisite** | RC-FD-01 — Form Design Overview; RC-FD-03 — Data Dictionary |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques; RC-CC-17 — Control Center: Database Query Tool |

---

# 1. Overview

Dynamic SQL (DSQL) is a special dropdown field type in REDCap where the list of selectable options is driven by the results of a SQL query against the REDCap backend database — rather than a fixed list of choices defined in the Data Dictionary. The query runs each time the page loads, pulling whatever values are currently in the source table and presenting them to the user as a standard dropdown.

Because DSQL fields query the database directly, they are significantly more powerful than ordinary dropdowns. They can pull participant records from another REDCap project, reference the user table to list project team members, or draw from any custom lookup table that has been loaded into the database — such as MedDRA term lists, institutional department directories, or procedure code tables.

DSQL appears in the Data Dictionary with field type `sql` and is otherwise invisible to non-administrator users. Only REDCap administrators can create, modify, or upload Data Dictionaries that contain DSQL fields.

> **Scope note — what DSQL cannot do:** DSQL populates the dropdown's option list only. It does not push data into other fields when a selection is made, and it does not trigger any downstream logic or auto-fill behavior. A common misconception is that DSQL can act as a lookup: the user selects a participant from the dropdown and other fields (name, date of birth, site) automatically populate. DSQL cannot do this. Functionality of that kind requires a custom external module or a Data Entry Trigger combined with API calls — and even with those approaches, achieving a seamless real-time experience is technically difficult given the way REDCap loads and renders pages.

> **Availability note:** Not all REDCap installations support DSQL. The feature requires that an administrator explicitly enable it and have access to the backend database. Additionally, building and maintaining SQL queries requires database and SQL skills that not all administrators possess. Users who want to use DSQL should check with their local REDCap support team before designing a workflow that depends on it.

---

# 2. Key Concepts & Definitions

## Dynamic SQL vs. Standard Dropdown

A standard `dropdown` field has a fixed choice list defined in Column F of the Data Dictionary — the options never change unless a designer edits and re-uploads the Data Dictionary. A DSQL field has no fixed choices; instead, it runs a SQL query at page load and builds its choice list from the query results. This makes DSQL well-suited for scenarios where the available options are themselves stored as data.

## Required Query Output Format

Every DSQL query must return exactly two columns per row:

1. **Raw value** — the value that is stored in REDCap when the user selects this option. This becomes the stored field value and is what branching logic and calculated fields evaluate.
2. **Label** — the human-readable text displayed to the user in the dropdown.

This mirrors the `raw_value, Display Label` format used in ordinary dropdown and radio choice lists. How the query arrives at these two columns — via joins, concatenation, filtering, or any other SQL logic — does not matter, as long as the output conforms to this structure.

## Page-Load Behavior

The DSQL query executes when the page (form or survey) loads. The dropdown is populated with whatever the query returns at that moment. If the source data changes after the page has loaded — for example, a new participant is added to the source project — the DSQL dropdown on the currently open page will not reflect that change. The user must reload the page to get a fresh query result.

This is an important workflow consideration: in high-throughput data entry scenarios where new source records are being added continuously, users should be instructed to reload the page before selecting from a DSQL field.

## Auto-Complete

DSQL fields automatically use REDCap's dropdown auto-complete feature, which allows users to type partial text to filter the visible options. This behavior cannot be disabled and is always active.

---

# 3. Administrator Responsibilities

## 3.1 Who Can Create or Edit DSQL Fields

Creating or modifying a DSQL field requires REDCap administrator access. This restriction applies in all contexts:

- The Online Designer does not expose the `sql` field type to non-administrators. It cannot be selected from the field type menu by regular users.
- Uploading a Data Dictionary that contains one or more `sql`-type rows requires administrator access. If a non-administrator attempts to upload a Data Dictionary containing a DSQL field, REDCap will reject the upload.
- This restriction applies even if the non-administrator is downloading and re-uploading their own project's Data Dictionary. If the project contains DSQL fields, only an administrator can perform the upload.

> **Practical note for project teams:** If your project contains DSQL fields and you need to make Data Dictionary changes, coordinate with your REDCap administrator. The administrator can either perform the upload or temporarily replace DSQL rows with placeholder fields, let the non-administrator upload their changes, and then restore the DSQL configuration.

## 3.2 SQL Access Requirements

Writing a DSQL query requires knowledge of the REDCap backend database schema and SQL skills. The administrator must know which tables to query, what the relevant field names are, and how to join tables correctly. REDCap's database structure is stable across minor versions, but administrators should validate queries after major REDCap version upgrades.

The Control Center Database Query Tool (RC-CC-17) can be used to test and validate queries before embedding them in a DSQL field.

---

# 4. Common Use Cases

DSQL is most useful in three broad scenarios:

**Cross-project lookups** — pulling records from one REDCap project to use as selectable options in another. For example, a registration project holds a list of enrolled participants, and a data entry project uses a DSQL field to let staff select a participant by ID and name rather than typing freehand.

**User-driven dropdowns** — querying the REDCap user table to produce a list of users currently assigned to a project. This is useful for assignment fields (e.g., "Assigned to:") that should automatically reflect the current team without manual maintenance.

**External reference tables** — querying a custom lookup table that has been loaded into the REDCap database. Common examples include drug dictionaries, diagnosis code lists (such as MedDRA), department or site directories, and procedure code tables. These tables are typically loaded and maintained by the REDCap administrator outside of the normal project interface.

---

# 5. SQL Query Guidelines

## 5.1 Output Structure

The query must produce exactly two columns in this order:

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

```sql
-- Querying the current project's own data:
SELECT record, value
FROM [data-table]
WHERE project_id = [project-id]
AND field_name = 'your_field_name'

-- Querying data from a different project (project ID 1234):
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

**Examples of when this is useful:**

- Use `[project-id]` instead of hardcoding the project ID when the DSQL queries its own project's data. This makes the query portable — if the project is copied or migrated, the query still resolves correctly without manual edits.
- Use `[record-name]` to filter query results to data associated with the current record. For example, a DSQL could present only the visits or specimens that belong to the record being entered, rather than the full list across all records.
- Use `[event-id]` or `[event-name]` to restrict results to data collected at a particular event, useful when a longitudinal project stores event-specific lookup data.

```sql
-- Example: query the current project's own data without hardcoding the project ID
SELECT record, value
FROM [data-table]
WHERE project_id = [project-id]
AND field_name = 'your_field_name'
ORDER BY value;
```

> **Cross-reference:** See RC-PIPE-03 — Smart Variables Overview for a full reference on available smart variables and their syntax.

---

# 6. SQL Examples

## Example 1: Participant Lookup with Name Label

This query pulls a participant identifier from one project and builds a label that combines the identifier with the participant's first and last name. The result appears in the dropdown as `P-1001 - Jane Smith`.

```sql
-- Participant lookup: raw value is the participant identifier,
-- label combines identifier with full name.
-- Replace 1234 with the numeric project ID of the source project.
-- Replace field_name values with the actual field names in that project.
-- [data-table:1234] resolves to the correct data table for project 1234.

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

```sql
-- Self-curating participant list: shows only participants not yet linked
-- in the target (current) project.
-- Replace 1234 with the numeric project ID of the source project.
-- Replace field_name values with the actual field names in each project.
-- 'study_id' is the identifier in the source project.
-- 'linked_participant_id' is the field in the current project that holds
-- the linked ID (i.e., the raw value from this dropdown once selected).
-- [data-table:1234] resolves the source project's data table.
-- [data-table] resolves the current project's data table.

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

**Test query performance before deploying.** Use the Database Query Tool (RC-CC-17) to run the query and review execution time before embedding it in a production project.

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

**A:** Yes. DSQL is a field type and is compatible with longitudinal projects. The query itself is not event-aware — it queries the database and returns results regardless of which event the form is associated with.

**Q: Why can't I upload my Data Dictionary after adding a DSQL field?**

**A:** Uploading a Data Dictionary that contains `sql`-type rows requires administrator access. If you are not a REDCap administrator, your upload will be rejected. You will need to coordinate with an administrator to complete the upload.

**Q: Can I download and re-upload my project's Data Dictionary if it already contains DSQL fields?**

**A:** Not without administrator involvement. Even if you do not modify the DSQL rows, REDCap requires administrator credentials to upload any Data Dictionary that contains `sql`-type rows. Coordinate with your administrator before attempting a Data Dictionary upload on a project with existing DSQL fields.

---

# 9. Common Mistakes & Gotchas

**Returning more than two columns.** REDCap expects exactly two columns (raw value and label) from a DSQL query. If the query returns additional columns, behavior may be undefined or the field may not populate correctly. Select only what you need.

**No ORDER BY clause.** Omitting `ORDER BY` produces an unpredictably ordered dropdown that may present options in a different sequence on each page load. Always sort the output.

**Forgetting to filter on both `project_id` and `field_name`.** Querying `redcap_data` without both filters will return data from across the entire REDCap installation, producing an enormous and incorrect result set.

**Assuming the dropdown updates live.** The options are a snapshot taken at page load. Workflows that depend on real-time updates (e.g., a coordinator assigns a patient to a team member and expects a concurrent user's open form to immediately reflect the new availability) will not work as expected with DSQL.

**Hardcoding `redcap_data` instead of using `[data-table]`.** On installations that use data table sub-tables, a query written as `FROM redcap_data` may point to the wrong table and return no results. This is a silent failure — the DSQL field will simply appear empty. Always use `[data-table]` for the current project and `[data-table:NNNN]` for any other project. This also makes queries portable: if a project is migrated to a different installation or the table structure changes, the smart variable resolves correctly without requiring a manual query update.

**Building DSQL workflows without confirming the feature is enabled.** Some institutions disable DSQL for security reasons. Confirm availability with your REDCap support team before designing a workflow that depends on it.

**Editing DSQL rows in the Data Dictionary as a non-administrator.** Attempting to upload a Data Dictionary with `sql`-type rows without administrator privileges will fail. Note also: non-administrators should not modify the SQL content of existing DSQL rows even if they could upload the file — an incorrect query can break the field silently.

---

# 10. Related Articles

- RC-FD-01 — Form Design Overview (field type selection and form design tools)
- RC-FD-03 — Data Dictionary (Data Dictionary upload workflow and safety practices)
- RC-FD-08 — Data Dictionary: Column Reference & Advanced Techniques (full column reference; notes on the `sql` field type code)
- RC-CC-17 — Control Center: Database Query Tool (tool for testing SQL queries before embedding them in a DSQL field)
- RC-DE-02 — Basic Data Entry (how dropdown fields behave during data entry, including auto-complete)
- RC-PIPE-03 — Smart Variables Overview (full reference for smart variables usable in DSQL queries)

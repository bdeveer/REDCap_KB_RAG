RC-CC-17

**Database Query Tool**

| **Article ID** | RC-CC-17 |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap super-user administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-16 — Database Activity Monitor; RC-CC-15 — Top Usage Report |

---

# 1. Overview

The Database Query Tool allows REDCap administrators to run read-only SQL queries directly against REDCap's MySQL/MariaDB database from the browser. It is accessible under "Dashboards & Activity" in the Control Center sidebar and is intended for investigative queries, support troubleshooting, and ad-hoc data lookups without requiring command-line database access.

# 2. Query Restrictions

Only read-only query types are permitted. Queries must begin with one of:

- `SELECT`
- `SHOW`
- `EXPLAIN`

Any other query type (INSERT, UPDATE, DELETE, DROP, ALTER, etc.) is rejected. This restriction protects the database from accidental or unauthorized modification.

# 3. Query Context

A "Use query context" option allows the query to be run in the context of a specific project or scope, which may affect certain query behaviors or variable resolution. This is optional and depends on the nature of your query.

# 4. Entering and Running Queries

Administrators type their SQL into the query text box and execute it. Results are displayed in a table directly on the page. Multiple query rows can be added for running several queries in sequence.

**Example queries:**

- `SELECT project_id, project_name FROM redcap_projects WHERE status = 0`
- `SELECT COUNT(*) as record_count FROM redcap_data WHERE project_id = 123`
- `SELECT * FROM redcap_log_event WHERE user = 'username' LIMIT 100`

# 5. Custom Query Management

The tool supports saving, organizing, and reusing named custom queries, which is helpful for frequently-run investigative queries:

- **Add or edit custom queries** — through an in-page dialog where each query has a name and SQL text
- **Organize queries** — arrange queries into folders or groups for easier navigation
- **Export custom queries (CSV)** — download all custom queries as a CSV file for backup, documentation, or sharing
- **Import custom queries (CSV)** — upload a CSV to add or modify custom queries in bulk

### Custom Query CSV Format

The CSV format for importing/exporting includes columns for:
- Query name/title (descriptive label)
- SQL text (the query statement)

All imported queries must begin with `SELECT`, `SHOW`, or `EXPLAIN`. Imports containing other query types are rejected with an error message.

### Custom Query Best Practices

- Use descriptive names for your custom queries (e.g., "Count of Active Projects", "User Login History")
- Include comments in SQL text to document the purpose of complex queries
- Regularly export your custom query collection for backup
- Share useful queries with your team via CSV import

# 6. Database Table Reference

The right sidebar lists all REDCap database tables, providing a quick reference when composing queries. This reference covers all core REDCap tables, including:

- `redcap_projects` — project metadata (title, status, dates)
- `redcap_metadata` — field/instrument definitions (data dictionary)
- `redcap_data` — stored data entry values
- `redcap_log_event` — system audit log and activity records
- `redcap_user_information` — user accounts and profile data
- `redcap_alerts` — alert configurations and definitions
- `redcap_data_access_groups` — DAG (Data Access Group) definitions
- `redcap_auth` — authentication records and session data
- `redcap_surveys` — survey configurations
- `redcap_surveys_participants` — survey participant records
- `redcap_surveys_queue` — survey queue entries
- `redcap_events` — events in longitudinal projects
- `redcap_arms` — arms in longitudinal projects
- `redcap_instruments` — instrument/form definitions
- And many others covering every aspect of REDCap's data model

Click any table name in the sidebar to view its column structure and field definitions.

# 7. Common Use Cases

The Database Query Tool is helpful in these scenarios:

- Looking up a specific user's account details, permissions, or login history
- Counting records, projects, or users that meet specific criteria not exposed in the UI
- Verifying data integrity (e.g., checking if a specific field value exists across records)
- Troubleshooting support tickets by querying log data
- Generating ad-hoc reports not available through the standard reporting interface
- Auditing data changes by querying the audit log table
- Finding orphaned records or incomplete data structures
- Analyzing project configurations across multiple projects

# 8. Performance Considerations

Because the Database Query Tool provides direct database access, be mindful of performance:

- **Avoid large, unfiltered queries** — `SELECT * FROM redcap_log_event` without a WHERE clause can put significant load on the database server, especially if the audit log is large
- **Use LIMIT** — especially when exploring unfamiliar data, start with `LIMIT 100` or `LIMIT 10` to test before retrieving thousands of rows
- **Index awareness** — queries that filter on indexed columns (e.g., project_id, user_id) will perform much better than those filtering on unindexed fields
- **Avoid joins on large tables** — joining `redcap_data` with `redcap_log_event` without specific filtering can be slow
- **Run exploratory queries during off-peak hours** if possible

# 9. Access and Safety

This tool requires super-user administrator access. Because it provides direct database access:

- Queries should be composed carefully to avoid unexpected performance impacts
- REDCap's read-only enforcement prevents accidental data modification
- Only users with full administrator privileges can access this tool
- Consider documenting queries used for troubleshooting in case the same issue occurs later

# 10. Related Tools

- **Database Activity Monitor (RC-CC-16)** — to see real-time database processes and identify long-running queries
- **Top Usage Report (RC-CC-15)** — for pre-built usage statistics and analytics


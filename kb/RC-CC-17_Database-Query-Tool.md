

**Database Query Tool**

| **Article ID** | [RC-CC-17 — Control Center: Database Query Tool](RC-CC-17_Database-Query-Tool.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Database Query Tool behaviour checked against source code; checked live on v17.5.6 (read-only): the disabled notice and its default only |
| **Prerequisite** | REDCap super-user administrator access |
| **Version** | 1.5 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-16 — Control Center: Database Activity Monitor](RC-CC-16_Database-Activity-Monitor.md); [RC-CC-15 — Control Center: Top Usage Report](RC-CC-15_Top-Usage-Report.md)|
| **Synonyms** | control center database query tool; run read-only sql against the redcap database; query redcap mysql from the browser; ad-hoc sql lookups for troubleshooting; which sql statements are allowed in the query tool; investigate data with a database query; admin sql query interface redcap; read-only database access without command line; enable the database query tool; database query tool is disabled; query tool only shows 500 rows; database query tool results cut off at 500; return more than 500 rows from the query tool; raise the query tool row limit; export database query tool results to csv; download sql query results from the control center |

---

## 1. Overview

The Database Query Tool allows REDCap administrators to run read-only SQL queries directly against REDCap's MySQL/MariaDB database from the browser. It is accessible under "Dashboards & Activity" in the Control Center sidebar and is intended for investigative queries, support troubleshooting, and ad-hoc data lookups without requiring command-line database access.

---

> **Off by default.** A new 17.5.6 installation has the tool disabled (`database_query_tool_enabled` = `0`). Both the **Database Query Tool** and **Recent Errors** menu links open a notice saying the tool is currently disabled, with the query to run in the MySQL database:
>
> `UPDATE redcap_config SET value = '1' WHERE field_name = 'database_query_tool_enabled';`
>
> Reload the page afterward. This needs someone with database access; there is no setting for it in the Control Center. The rest of this article describes the tool once enabled; that part was checked against source code, not on a live instance.
>
> **Older installations may already have it on.** The upgrade to REDCap 12.3.0 switched the tool on automatically if the "MySQL Simple Admin" external module was enabled, and imported that module's saved queries as custom queries. If your server has been upgraded through 12.3.0, check whether the tool is enabled before assuming it is off.

---

## 2. Query Restrictions

Only read-only query types are permitted. Queries must begin with one of:

- `SELECT`
- `SHOW`
- `EXPLAIN`

Any other query type (INSERT, UPDATE, DELETE, DROP, ALTER, etc.) is rejected with a message beginning "Can only accept…". This restriction protects the database from accidental or unauthorized modification.

The first word of the query must be one of the three keywords. A query that starts with a comment, an opening parenthesis, a `WITH` clause or `DESCRIBE` is rejected too. Put comments after the first keyword, and use `SHOW COLUMNS FROM tablename` instead of `DESCRIBE tablename`.

---

## 3. Query Context

The **Use query context** option lets a query use REDCap Smart Variables, filled in from a chosen context: `[project-id]`, `[record-name]`, `[instrument-name]`, `[event-id]`, `[current-instance]` and `[user-name]`. Write the Smart Variable in the SQL (for example `WHERE project_id = [project-id]`) and the tool substitutes the value before running it. A toggle shows the query as it was actually executed, with the values filled in.

With a project context set, clicking a table name in the table list adds a `WHERE` filter for that project and uses the data or logging table the project actually lives in, so you don't have to look it up first.

Shortcut buttons on the Project Home, Record Home, data entry and survey pages open the tool with the context already set to that project, record, instrument or event. The option is not needed for queries that don't use Smart Variables.

---

## 4. Entering and Running Queries

Administrators type their SQL into the single query box and click **Execute**. Each run executes one statement; to run another query, replace the text and execute again. Results are displayed in a table directly on the page. Long values are cut short with a **show more** link, and values that point to another table (foreign keys) are shown as links. The **Export results (CSV)** button downloads the results as a CSV file (see Common Questions).

> **Results are capped at 500 rows by default.** A `SELECT` with no `LIMIT` clause returns at most 500 rows. When a result comes back with exactly 500 rows, the page shows a notice that more rows might exist and that `LIMIT 0,500` was added automatically. Treat such a list as incomplete. To get more, end the query with your own `LIMIT` and a higher number, for example `LIMIT 100000`. Any `LIMIT` anywhere in the query, including inside a subquery, replaces the 500-row default. `SHOW` and `EXPLAIN` results are never limited.
>
> **The cap applies to CSV exports too.** **Export results (CSV)** re-runs the same query, so an export of a query without `LIMIT` also stops at 500 rows. Add an explicit `LIMIT` before you export a full list.

> **Logging.** Every successful query run and every CSV export is recorded in REDCap's logging with the full SQL text. Queries that fail are not logged. Assume colleagues and auditors can see what you queried.

**Example queries:**

- `SELECT project_id, project_name FROM redcap_projects WHERE status = 0`
- `SELECT COUNT(*) as record_count FROM redcap_data WHERE project_id = 123`
- `SELECT * FROM redcap_log_event WHERE user = 'username' LIMIT 100`

### 4.1 Built-In System Query: Recent Errors

The Control Center sidebar includes a **Recent Errors** menu item under "Dashboards & Activity." It is shown only to administrators with "Access to all projects and data with maximum user privileges." Despite appearing as a distinct navigation link, it is not a separate tool — it simply opens the Database Query Tool with a pre-canned SQL query already loaded and executed. On REDCap 17.x the query is:

```sql
select * -- Recent Errors (retained for 30 days)
from redcap_error_log
where 1=1
order by error_id desc
```

This query returns all rows from `redcap_error_log`, sorted newest first (still subject to the 500-row default). The comment in the query (`-- Recent Errors (retained for 30 days)`) documents the retention window: REDCap automatically purges error log entries older than 30 days.

Because Recent Errors is just a convenience shortcut into the Database Query Tool, you can modify the query once it loads. On 17.x, add conditions to the existing `where` line with `and …` (`where 1=1 and …`), and add a `LIMIT` after `order by` for large logs.

> **Version caveat (REDCap 16.0.x LTS):** the 16.0.x query has no `where` line; it goes straight from `from redcap_error_log` to `order by error_id desc`. To filter, add your own `where …` line before `order by`. Adding `and …` on 16.0.x produces an SQL error.

---

## 5. Custom Query Management

The tool supports saving, organizing, and reusing named custom queries, which is helpful for frequently-run investigative queries:

- **Add or edit custom queries** — through an in-page dialog where each query has a name and SQL text. The dialog's **Add another query** button adds more query rows, so several saved queries can be created in one go
- **Run a saved query** — clicking a saved query's name runs it immediately
- **Organize queries** — arrange queries into folders or groups for easier navigation
- **Export custom queries (CSV)** — download all custom queries as a CSV file for backup, documentation, or sharing
- **Import custom queries (CSV)** — upload a CSV to add or modify custom queries in bulk. A preview is shown before the import is applied

#### Custom Query CSV Format

The CSV has three columns:

| Column | Contents |
|---|---|
| `query_title` | The query's descriptive name |
| `sql_query` | The SQL statement |
| `query_id` | The saved query's ID. A row whose ID matches an existing query updates that query; a blank ID creates a new query |

An import never deletes queries: queries missing from the file stay as they are. To remove one, delete it in the tool.

All imported queries must begin with `SELECT`, `SHOW`, or `EXPLAIN`. Imports containing other query types are rejected with an error message.

#### Custom Query Best Practices

- Use descriptive names for your custom queries (e.g., "Count of Active Projects", "User Login History")
- Include comments in SQL text to document the purpose of complex queries
- Regularly export your custom query collection for backup
- Share useful queries with your team via CSV import

---

> **Note (15.2.1):** CSV exports of a saved custom query's results include the **query title in the filename**, so a folder of exports remains identifiable rather than becoming a set of near-identical generic filenames.

---

## 6. Database Table Reference

The left-hand column, headed **REDCap database tables:**, lists every table in the database, with a filter box to narrow the list. It covers all core REDCap tables, including:

- `redcap_projects` — project metadata (title, status, dates)
- `redcap_metadata` — field/instrument definitions (data dictionary)
- `redcap_data`, `redcap_data2` … `redcap_data8` — stored data entry values. **One of several tables** — the first has no number, the rest are numbered, and a project's data lives in one specific table such as `redcap_data8`
- `redcap_log_event`, `redcap_log_event2` … `redcap_log_event15` — project audit log and activity records, likewise **split across several tables**, e.g. `redcap_log_event10`
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

> **Critical — data and logging tables are split, and which one a project uses varies.** REDCap distributes projects across several data tables and several logging tables for performance. A query written against `redcap_data` alone only finds projects stored in that first table, and returns nothing for the others. To find the tables a given project actually uses, open **Control Center → Edit Project Settings** for that project — the data table and logging table are named at the top of the page, alongside a **Move Project Data** tool. See [RC-CC-24 — Control Center: Edit Project Settings](RC-CC-24_Control-Center-Edit-Project-Settings.md). Alternatively, set **Use query context** to the project (section 3): clicking a table name then queries the project's own data or logging table.
>
> The set grows over time: **16.0.0 added two further data tables and three further log_event tables**. A query that enumerated the tables correctly before an upgrade may miss projects created afterwards, so do not hard-code the list.

Clicking a table name runs `select *` on that table and shows its first 500 rows. To see a table's columns and their types, run `SHOW COLUMNS FROM tablename` (`DESCRIBE` is not accepted).

---

## 7. Common Use Cases

The Database Query Tool is helpful in these scenarios:

- Looking up a specific user's account details, permissions, or login history
- Counting records, projects, or users that meet specific criteria not exposed in the UI
- Verifying data integrity (e.g., checking if a specific field value exists across records)
- Troubleshooting support tickets by querying log data
- Generating ad-hoc reports not available through the standard reporting interface
- Auditing data changes by querying the audit log table
- Finding orphaned records or incomplete data structures
- Analyzing project configurations across multiple projects

---

## 8. Performance Considerations

Because the Database Query Tool provides direct database access, be mindful of performance:

- **Avoid large, unfiltered queries** — `SELECT * FROM redcap_log_event` without a WHERE clause can put significant load on the database server, especially if the audit log is large
- **Use LIMIT** — especially when exploring unfamiliar data, start with `LIMIT 100` or `LIMIT 10` to test before retrieving thousands of rows
- **Expect at most 500 rows** — the tool shows 500 rows by default (section 4), so for full lists check whether you hit the cap
- **Index awareness** — queries that filter on indexed columns (e.g., project_id, user_id) will perform much better than those filtering on unindexed fields
- **Avoid joins on large tables** — joining `redcap_data` with `redcap_log_event` without specific filtering can be slow
- **Run exploratory queries during off-peak hours** if possible

---

## 9. Access and Safety

This tool requires super-user administrator access. Because it provides direct database access:

- Queries should be composed carefully to avoid unexpected performance impacts
- REDCap's read-only enforcement prevents accidental data modification
- Only administrators with the **Access to all projects and data with maximum user privileges** admin right can use this tool; other administrators who open it see a notice instead
- Every successful query and CSV export is logged with its full SQL (section 4)
- Consider documenting queries used for troubleshooting in case the same issue occurs later

---

## 10. Related Tools

- **Database Activity Monitor ([RC-CC-16 — Control Center: Database Activity Monitor](RC-CC-16_Database-Activity-Monitor.md))** — to see real-time database processes and identify long-running queries
- **Top Usage Report ([RC-CC-15 — Control Center: Top Usage Report](RC-CC-15_Top-Usage-Report.md))** — for pre-built usage statistics and analytics

---

## 11. Common Questions

**Q: What is the "Recent Errors" menu item in the Control Center?**
"Recent Errors" is a shortcut that opens the Database Query Tool with a pre-loaded query against `redcap_error_log`, sorted by most recent error first. It is not a standalone tool — it is simply a pre-canned `SELECT *` query with a 30-day retention window documented in the SQL comment, and only administrators with maximum user privileges see it. Once the page loads you can edit the query normally, for example to filter on a specific error type: on 17.x add `and …` to the existing `where` line; on 16.0.x LTS add a `where …` line before `order by` (section 4.1).

**Q: Can I run UPDATE or DELETE queries to fix data?**
No. The Database Query Tool only accepts read-only query types (SELECT, SHOW, EXPLAIN). Any attempt to run INSERT, UPDATE, DELETE, DROP, ALTER, or other write-based queries will be rejected. This restriction prevents accidental data modification. If you need to modify data, use the REDCap UI or contact your database administrator.

**Q: How do I know which table contains the data I am looking for?**
The left-hand column, **REDCap database tables:**, lists every table, with a filter box. Clicking a table name shows its first 500 rows; run `SHOW COLUMNS FROM tablename` to see its columns. For example, user information is in `redcap_user_information`, and data values are in `redcap_data` or one of its numbered siblings (`redcap_data2` … `redcap_data8`), depending on the project (section 6).

**Q: Can I save queries I write frequently?**
Yes. The tool supports saving named custom queries. Add or edit custom queries through the in-page dialog, give each query a descriptive name, and save it. You can then reuse that query without re-typing it. You can also organize queries into folders and export/import them as CSV files.

**Q: What is "Use query context" and when should I use it?**
It lets you use Smart Variables such as `[project-id]`, `[record-name]`, `[event-id]` or `[user-name]` in your SQL, filled in from the project, record, instrument or event you choose. Use it when you want one saved query to work for whichever project or record you are looking at; the shortcut buttons on Project Home, Record Home, data entry and survey pages set the context for you. With a project context, clicking a table name also filters to that project and picks the project's own data or logging table. Queries without Smart Variables don't need it.

**Q: Why does my query stop at exactly 500 rows?**
The Database Query Tool shows at most 500 rows by default when a `SELECT` has no `LIMIT` clause, and shows a notice that `LIMIT 0,500` was added automatically. A result of exactly 500 rows is almost always cut off. Add your own `LIMIT` with a higher number at the end of the query (for example `LIMIT 100000`) and run it again. An explicit `LIMIT` replaces the default, so the full result comes back. The same cap applies to **Export results (CSV)**.

**Q: How do I export the results of my query?**
The tool has an **Export results (CSV)** button for query results. Click it after the query runs to download the results as a CSV file. The export re-runs the query, so it is also capped at 500 rows unless the query has its own `LIMIT`. Results of an unsaved query download with a generic, timestamped filename such as `query_tool_export_2026-11-18_1755.csv`; results of a saved custom query include the query's title in the filename. If you run the same query on several servers, rename the files or add a column that identifies the server, because the generic filenames don't say where the data came from.

> **Version caveat (17.x vs REDCap 16.0.x LTS):** on 17.x, CSV export makes values safe to open in a spreadsheet: a value starting with `=`, `+`, `-` or `@` gets a leading apostrophe, and surrounding spaces are trimmed. A negative number therefore exports as `'-5` and an `@`-prefixed value as `'@…`. Strip the apostrophe before using such columns as numbers. On 16.0.x LTS values export exactly as stored, so a value beginning with `=` can be treated as a formula when the file is opened in Excel; import the file as text, or open it in a text editor, rather than double-clicking it.

---

## 12. Common Mistakes & Gotchas

**Running very large or unfiltered queries without a LIMIT clause.** A query like `SELECT * FROM redcap_log_event` with no WHERE clause or LIMIT can retrieve millions of rows, which will freeze your browser, consume significant memory, and put load on the database server. Always start with a LIMIT clause (e.g., `LIMIT 100`) when exploring unfamiliar data, and use specific WHERE clauses to narrow results.

**Treating a 500-row result as complete.** The tool shows 500 rows by default, and the cut is easy to miss. Notification lists, user audits and inventories are the usual victims: people past row 500 are missing, in the on-screen result and in the CSV export alike. For any query meant to return a complete list, end it with an explicit `LIMIT` well above the number of rows you expect (for example `LIMIT 100000`). To be sure, check the total with `SELECT COUNT(*)` on the same `FROM` and `WHERE`.

**Starting a query with a comment, `WITH` or `DESCRIBE`.** The query's first word must be `SELECT`, `SHOW` or `EXPLAIN`, so a query that opens with a `--` comment line, a parenthesis, a `WITH` clause or `DESCRIBE` is rejected with "Can only accept…". Move comments below the first line, rewrite `WITH` queries as subqueries, and use `SHOW COLUMNS FROM tablename` instead of `DESCRIBE`.

**Forgetting to filter on indexed columns.** Queries that filter on indexed columns (such as `project_id` or `user_id`) will perform much faster than queries that filter on unindexed fields. If a query takes a very long time, try restructuring it to filter on indexed columns first, or run the query during off-peak hours when database load is lower.

**Importing custom queries with non-SELECT statement types in CSV.** When importing custom queries from a CSV file, all queries must begin with SELECT, SHOW, or EXPLAIN. If your import includes UPDATE, DELETE, or other write-type queries, the entire import will be rejected. Verify all queries in your CSV before importing, or test the import in a non-production environment first.

---

## 13. Related Articles

- [RC-CC-16 — Control Center: Database Activity Monitor](RC-CC-16_Database-Activity-Monitor.md)
- [RC-CC-15 — Control Center: Top Usage Report](RC-CC-15_Top-Usage-Report.md)
- [RC-CC-21 — Control Center: Overview & Navigation](RC-CC-21_Control-Center-Overview.md)

RC-CC-16

**Database Activity Monitor**

| **Article ID** | RC-CC-16 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap super-user administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-15 — Top Usage Report; RC-CC-17 — Database Query Tool; RC-CC-12 — User Activity Log |

---

# 1. Overview

The Database Activity Monitor displays a real-time, enhanced view of the MySQL/MariaDB process list for the REDCap database server. It shows all active database queries currently being executed, which makes it useful for diagnosing database-level performance issues, identifying long-running queries, and understanding what is happening on the database server at any given moment.

---

# 2. Accessing the Monitor

The Database Activity Monitor is located in the REDCap Control Center under "Dashboards & Activity" in the sidebar. Requires super-user administrator access.

---

# 3. Display Information

The page header shows:
- Database server hostname
- Current server timestamp
- Total active processes (queries) at the time of the last refresh

---

# 4. Per-Process Information

For each active database process, the monitor displays:

- **REDCap Project ID** — the project associated with the query (if applicable)
- **User** — the REDCap username of the user whose action triggered the query
- **URL** — the REDCap page URL being executed (e.g., `/DataEntry/record_status_dashboard.php?pid=XXXX`)
- **Script Time (seconds)** — how long the overall REDCap page/script has been running
- **Query Time (seconds)** — how long the specific database query has been executing
- **Query text** — the SQL statement being executed (shown as full or partial)

---

# 5. Query Display Modes

Administrators can toggle between:

- **Partial queries** (default) — truncated for readability
- **Full queries** — complete SQL text for each process

---

# 6. Auto-Refresh

The page automatically reloads at a configurable interval. Administrators can select from:
- Every 10 seconds
- Every 30 seconds
- Every 60 seconds

The page continues auto-refreshing until the browser tab is closed or refreshed manually.

---

# 7. Killing a Process

Administrators can kill (terminate) a running MySQL process by clicking the kill button for that process. A confirmation dialog warns that:

- Killing a process will prevent that query from completing
- It may affect other queries in the same script
- This should be used carefully, only for genuinely problematic long-running queries

**Important:** Use this feature cautiously. Terminating database processes can have cascading effects on active user sessions and ongoing operations.

---

# 8. Common Use Cases

The Database Activity Monitor is helpful in these scenarios:

- A user reports a page is hanging — use the monitor to find and identify the blocking query
- Unexpected database load — identify which project or user is causing high activity
- Troubleshooting scheduled tasks or API calls generating slow queries
- Confirming whether a database issue has resolved after intervention
- Diagnosing performance bottlenecks during peak usage periods

---

# 9. Best Practices

- **Monitor periodically during peak usage** to establish baseline performance
- **Never kill a process without understanding its context** — verify the associated user and project first
- **Use shorter refresh intervals (10 seconds) only when actively troubleshooting** to reduce page load overhead
- **Keep the monitor open in a separate tab** during large data operations or batch imports to watch for bottlenecks

---

# 10. Access Requirements

This page requires full super-user administrator access. Because it provides visibility into all database activity across all users and projects, access should be restricted to trusted administrators.

---

# 11. Common Questions

**Q: What is the difference between "Script Time" and "Query Time"?**
Script Time is how long the overall REDCap page or script has been running. Query Time is how long the specific database query shown in that row has been executing. A query may have been running for 5 seconds while the overall script has been running for 20 seconds because other operations or queries completed before this one.

**Q: If I see a query that has been running for 10 minutes, should I kill it?**
Not necessarily. Very long-running queries sometimes indicate a legitimate large operation (bulk data export, report generation). Before killing a process, understand the context: who is the user, what project are they in, and what is the URL they are accessing. Only kill a process if you have confirmed it is problematic or stuck.

**Q: Can I see the query history or past queries?**
No. The Database Activity Monitor shows only currently active queries at the moment of the page load or auto-refresh. It does not log historical queries. To troubleshoot a query that ran in the past, use the Database Query Tool to examine log data, or check your database server logs if available.

**Q: Does the auto-refresh interval affect database performance?**
Yes. Very frequent auto-refresh (every 10 seconds) means the monitor itself is generating queries to fetch the process list. If you are using a 10-second refresh interval, you are adding some load to the database. Use a 10-second interval only when actively troubleshooting, and use 30 or 60 seconds for periodic monitoring.

**Q: What happens to the monitor if the database server becomes unavailable?**
If the database is down or unreachable, the monitor will not load and will display an error. The monitor cannot function without an active database connection, as it relies on the MySQL/MariaDB process list API.

---

# 12. Common Mistakes & Gotchas

**Killing a process without understanding its impact.** Terminating a database process can cause cascading effects. The query may have been initiated by a scheduled task, API call, or user action. Killing it can interrupt data imports, break user sessions, or leave partial data in an inconsistent state. Always verify the context before killing a process.

**Using a very short auto-refresh interval all the time.** Setting the monitor to refresh every 10 seconds is useful for active troubleshooting, but leaving it enabled 24/7 creates continuous database load. Switch to a 30 or 60-second interval when the issue has been resolved, or stop monitoring altogether if the problem has been identified and fixed.

**Assuming all long-running queries are problems.** Some queries are legitimately slow because they involve large datasets, complex joins, or intensive calculations. A 5-minute query may be normal for a large data export or complex report. Check the URL and understand what operation the user is performing before deciding a long query is a problem.

---

# 13. Related Articles

- RC-CC-15 — Top Usage Report
- RC-CC-17 — Database Query Tool
- RC-CC-12 — User Activity Log
- RC-CC-21 — Control Center Overview

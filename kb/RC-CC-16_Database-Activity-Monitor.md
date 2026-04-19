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

# 2. Accessing the Monitor

The Database Activity Monitor is located in the REDCap Control Center under "Dashboards & Activity" in the sidebar. Requires super-user administrator access.

# 3. Display Information

The page header shows:
- Database server hostname
- Current server timestamp
- Total active processes (queries) at the time of the last refresh

# 4. Per-Process Information

For each active database process, the monitor displays:

- **REDCap Project ID** — the project associated with the query (if applicable)
- **User** — the REDCap username of the user whose action triggered the query
- **URL** — the REDCap page URL being executed (e.g., `/DataEntry/record_status_dashboard.php?pid=XXXX`)
- **Script Time (seconds)** — how long the overall REDCap page/script has been running
- **Query Time (seconds)** — how long the specific database query has been executing
- **Query text** — the SQL statement being executed (shown as full or partial)

# 5. Query Display Modes

Administrators can toggle between:

- **Partial queries** (default) — truncated for readability
- **Full queries** — complete SQL text for each process

# 6. Auto-Refresh

The page automatically reloads at a configurable interval. Administrators can select from:
- Every 10 seconds
- Every 30 seconds
- Every 60 seconds

The page continues auto-refreshing until the browser tab is closed or refreshed manually.

# 7. Killing a Process

Administrators can kill (terminate) a running MySQL process by clicking the kill button for that process. A confirmation dialog warns that:

- Killing a process will prevent that query from completing
- It may affect other queries in the same script
- This should be used carefully, only for genuinely problematic long-running queries

**Important:** Use this feature cautiously. Terminating database processes can have cascading effects on active user sessions and ongoing operations.

# 8. Common Use Cases

The Database Activity Monitor is helpful in these scenarios:

- A user reports a page is hanging — use the monitor to find and identify the blocking query
- Unexpected database load — identify which project or user is causing high activity
- Troubleshooting scheduled tasks or API calls generating slow queries
- Confirming whether a database issue has resolved after intervention
- Diagnosing performance bottlenecks during peak usage periods

# 9. Best Practices

- **Monitor periodically during peak usage** to establish baseline performance
- **Never kill a process without understanding its context** — verify the associated user and project first
- **Use shorter refresh intervals (10 seconds) only when actively troubleshooting** to reduce page load overhead
- **Keep the monitor open in a separate tab** during large data operations or batch imports to watch for bottlenecks

# 10. Access Requirements

This page requires full super-user administrator access. Because it provides visibility into all database activity across all users and projects, access should be restricted to trusted administrators.


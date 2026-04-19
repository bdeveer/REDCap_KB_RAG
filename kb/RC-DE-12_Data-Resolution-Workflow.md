RC-DE-12

**Data Entry — Data Resolution Workflow**

| **Article ID** | RC-DE-12 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; requires the Data Resolution Workflow mode to be enabled |
| **Prerequisite** | RC-DE-08 — Field Comment Log |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-DE-02 — Basic Data Entry; RC-DE-04 — Editing Data & Audit Trail; RC-DE-08 — Field Comment Log |

---

# 1. Overview

This article covers REDCap's Data Resolution Workflow (DRW) — what it is, how it differs from the Field Comment Log, how to enable and configure it, and how to open, respond to, close, and review queries. The DRW is a structured issue-tracking system built directly into REDCap that allows study teams to flag data problems, assign them to specific users, track resolution status, and audit the entire process without leaving REDCap. It is best suited for projects with multiple data entry users, distributed teams, or regulatory requirements around data quality documentation. For simpler annotation needs, see RC-DE-08 — Field Comment Log.

> **Note:** The Data Resolution Workflow and the Field Comment Log are mutually exclusive modes. A project runs in one mode at a time. See Section 3 for how to switch between them.

---

# 2. Key Concepts & Definitions

**Data Resolution Workflow (DRW)**

A data quality management feature in REDCap that treats each annotation as a trackable issue (called a query) rather than a simple comment. Each query has a status, can be assigned to a specific user, and supports a structured back-and-forth resolution process. The full history of a query — who opened it, who responded, and what decisions were made — is stored in REDCap.

**Query**

The DRW equivalent of a field comment. A query is attached to a specific variable in a specific record and has a status that reflects where it is in the resolution process. The DRW interface uses the terms "query" and "issue" interchangeably in some contexts.

**Query Status**

Each query has one of the following statuses at any given time:

| Status | Meaning |
|---|---|
| Open / Unresolved (Unresponded) | Query has been opened; no response has been recorded yet |
| Open / Unresolved (Responded) | A response has been added but the query has not been closed |
| Closed / Resolved | The query has been marked as resolved |

**Verified Data Value**

A DRW designation indicating that a user has explicitly reviewed and confirmed that a variable's value is correct as entered. A verified value is not a query — it signals approval, not a problem. A verified value can be de-verified if circumstances change.

**De-verified Data Value**

The act of removing a previously applied verification from a data point. De-verification requires a comment and results in the data point being flagged for re-review.

**Data Resolution Dashboard**

A project-level view accessible from the application menu that displays all queries across all records and instruments. It is the primary tool for reviewing and managing outstanding issues across a project. Equivalent in purpose to the Field Comment Log application.

**Resolution Metrics**

A tab within the Data Resolution Dashboard that provides aggregate statistics about query activity — such as average time to close, most frequently queried variables, and team workload distribution. Useful for project management and identifying systemic data quality issues.

**Rule-Based Query**

A query generated from a multi-variable custom rule in the Data Quality module. Because the rule spans multiple variables, REDCap cannot attach the query to a single data point. Rule-based queries appear in the Data Resolution Dashboard but are not linked to a specific variable in a record.

---

# 3. Enabling and Configuring the Data Resolution Workflow

### 3.1 Choosing a Mode

REDCap projects support one of three tracking modes at a time:

| Mode | Description |
|---|---|
| Field Comment Log | Simple per-variable comments; no status tracking or assignment (default for most projects) |
| Data Resolution Workflow | Structured queries with status, assignment, and resolution tracking |
| None | All comment and query tracking features are disabled |

Switching modes does not convert existing data. Comments created under the Field Comment Log will not appear in the DRW dashboard, and queries created under DRW will not appear in the Field Comment Log application. Establish your mode before data collection begins and avoid switching mid-project.

### 3.2 Switching the Mode

1. Navigate to the **Project Setup** page for your project.
2. Scroll down to **Enable optional modules and customizations**.
3. Click **Additional customizations**.
4. Scroll to the section labeled **Enable the Field Comment Log or Data Resolution Workflow (Data Queries)?**
5. Select your desired mode.
6. Click **Save**.

### 3.3 DRW-Specific Settings

After enabling DRW, two additional settings become available in the same customization panel:

**Hide closed/verified data queries from Data Quality results.** When checked, any variable that already has a closed or verified query attached to it will be excluded from Data Quality module rule results. This is useful when you want Data Quality to surface only unprocessed issues — for example, finding all records with a missing birth date, but excluding those where the absence has already been verified or handled. Leave unchecked if you want Data Quality to flag all matching records regardless of query status.

**DRW user rights.** Enabling DRW adds a new user rights setting to every user and user role in the project. The default for new users is View Only — users will not be able to interact with queries until their rights are updated. See Section 4.

---

# 4. DRW User Rights

After DRW is enabled, each user in the project has a DRW-specific access level. These are managed through the standard User Rights or User Roles interface.

| Access Level | Can View Queries | Can Open Queries | Can Respond to Queries | Can Close Queries |
|---|---|---|---|---|
| No Access | No | No | No | No |
| View Only *(default for new users)* | Yes | No | No | No |
| Open Queries Only | Yes | Yes | No | No |
| Respond Only | Yes | No | Yes | No |
| Open and Respond | Yes | Yes | Yes | No |
| Open, Close, and Respond | Yes | Yes | Yes | Yes |

**Assigning rights in practice.** Align DRW rights with each user's role in the study. A data entry coordinator who identifies problems should be able to open and respond; a statistician who only needs visibility should have View Only; a data manager responsible for resolving issues needs Open, Close, and Respond access.

> **Note:** A user with No Access cannot see the Data Resolution Dashboard or any query icons within instruments. From their perspective, the DRW does not exist in the project.

For more information on managing user rights and roles, see the User Rights training series.

---

# 5. Opening Queries

### 5.1 Locating the Query Icon

Every variable in an instrument displays a small icon (depicted as a text balloon) next to the data entry area. This icon is present for every variable by default, but will not be shown if a variable is hidden by branching logic or embedded within another field using field embedding.

> **Note:** The DRW is not available in survey mode. Query icons appear only when a staff user accesses the instrument in data entry mode.

### 5.2 Verifying a Data Value

The first option presented when clicking the query icon is **Verified data value**. This option is selected by default.

To verify a value, click the query icon and then click **Verified data value**. Optionally, add a comment before confirming. Once verified, the text balloon is replaced by a green checkmark icon. The checkmark remains clickable and displays who performed the verification and when.

**De-verifying a value.** Click the green checkmark to open the verification panel. Select **De-verify the data value** and provide a required comment. After de-verification, the icon changes to indicate the data point is flagged for re-review. From this state, the variable can be re-verified or a query can be opened.

### 5.3 Opening a New Query

To open a query on a variable:

1. Click the text balloon icon next to the variable.
2. Select **Open a query** (the second option in the popup).
3. Enter a comment describing the issue — a comment is required.
4. Optionally, assign the query to another user in the project by selecting their name from the dropdown.
5. Optionally, notify the assigned user by checking the **Email** or **REDCap Messenger** notification boxes (messenger must be enabled for your REDCap installation).
6. Click **Open query** to submit.

After the query is opened, the text balloon is replaced by an icon indicating the query is in **Open / Unresolved (Unresponded)** status.

**Assignment best practices.** Establish team agreements about who opens queries, who can assign them, and who is responsible for responding. On small teams, leaving queries unassigned is common. On larger or distributed teams, explicit assignment prevents queries from going unnoticed.

### 5.4 Queries from the Data Quality Module

A second way to generate queries is through the **Data Quality** module:

- **Stock rules and single-variable custom rules** — If you run a Data Quality rule and open a query from the results, REDCap links the query to the relevant data point like a standard query.
- **Multi-variable custom rules** — If a custom rule references two or more variables, REDCap cannot determine which variable to attach the query to. It creates a **rule-based query** instead. Rule-based queries appear in the Data Resolution Dashboard but are not linked to a specific variable icon in a record. They behave the same as standard queries in all other respects.

---

# 6. Responding to and Closing Queries

### 6.1 Responding to a Query

To respond to an open query, click the query icon in the record (or use the Data Resolution Dashboard — see Section 7). The current query status and history are displayed.

1. Select **Reply with a response** and choose a response category from the dropdown. If no preset category fits, use **Other**.
2. Enter a required comment.
3. Optionally, attach a file.
4. Click to submit.

After a response is added, the query status changes to **Open / Unresolved (Responded)** and the icon updates to reflect this.

**Reassigning a query.** Select **Assign to other user** to transfer responsibility to a different project member. This works the same as the initial assignment when opening the query.

### 6.2 Closing a Query

Closing is available once a response has been recorded. To close:

1. Select **Close the query**.
2. Enter a required short comment confirming resolution.
3. Submit.

After closure, the query icon changes to the **Closed / Resolved** status. Closed queries can be reopened at any time by clicking the icon — this resets the status to **Open / Unresolved (Unresponded)**.

### 6.3 Sending Back for Further Attention

If a response was added but the issue is not yet resolved, use **Send back for further attention** instead of closing. This returns the query to **Open / Unresolved (Unresponded)** status with a required comment explaining why it was returned. Teams can cycle between responded and sent-back status as many times as needed. REDCap logs each transition.

---

# 7. Reviewing Queries

### 7.1 Data Resolution Dashboard

Navigate to **Resolve Issues** in the project application menu (located adjacent to the **Data Quality** link) to open the Data Resolution Dashboard. This view shows all queries in the project that the current user has rights to see.

**Dashboard columns:**

| Column | Content |
|---|---|
| View button | Opens the query popup directly from the dashboard — equivalent to clicking the icon in the record |
| Record | Record ID and, for longitudinal projects, the event the query is located in |
| Data Quality rule and/or field | The variable name or rule the query is attached to |
| User assigned | The project user currently assigned to the query |
| Days open | Number of days elapsed since the query was opened |
| First update | The first comment recorded for the query (typically the comment that opened it) |
| Last update | The most recent comment, if different from the first |

### 7.2 Filtering Queries

The dashboard supports the following filters. Multiple filters can be combined. Filters do not apply automatically — click **Apply filters** to update the results. Use the **Reset** link to clear all filters to their defaults.

| Filter | Description |
|---|---|
| Status type | Filter by query status (e.g., show only Unresponded queries) |
| Field and rules | Filter to a specific variable or Data Quality rule |
| Events | Filter to a single event (longitudinal projects only; one event at a time) |
| Data Access Group | Filter to queries from a specific DAG |
| Users | Filter to queries assigned to a specific user |

### 7.3 Exporting the Query Log

Click **Export** from the Data Resolution Dashboard to download all currently displayed queries as a CSV file. The export includes the first and last comment, total comment count, record ID, timestamps, and variable identification. For longitudinal and repeated-instruments projects, the export also includes event and instance information.

### 7.4 Resolution Metrics

A **Resolution Metrics** tab appears next to the **Resolve Issues** tab in the dashboard. It provides aggregate charts and statistics about query activity, including:

- Average time to close a query
- Query volume over time
- Which variables generate the most queries
- Team workload distribution by user

Use Resolution Metrics to identify recurring data entry problems (candidate fields for instrument redesign), to evaluate team performance on query resolution, and to document data quality activities for audits.

---

# 8. Common Questions

**Q: What is the difference between the Data Resolution Workflow and the Field Comment Log?**

**A:** Both allow you to annotate variables with comments. The Field Comment Log is simpler — comments have no status, cannot be assigned, and there is no resolution tracking. The DRW treats each annotation as a trackable issue (query) with a status, an assignee, a response thread, and a closure record. Use the Field Comment Log for lightweight notation; use the DRW when your team needs structured accountability and a documented resolution trail.

**Q: Can I use both the Field Comment Log and the DRW in the same project at the same time?**

**A:** No. A project operates in one mode at a time. If you switch from the Field Comment Log to the DRW (or vice versa), existing comments and queries are preserved in their respective systems but will not appear in the other system's interface. Switching mid-project is strongly discouraged.

**Q: A new user was added to the project but says they can't see any queries. Why?**

**A:** The default DRW user rights for new users is View Only — but View Only still requires that DRW be enabled for the project. If the user truly cannot see any query icons or the Resolve Issues link, check two things: (1) confirm DRW is enabled in Project Setup, and (2) confirm the user's DRW rights are not set to No Access in User Rights.

**Q: Can I open a query on a variable that is currently hidden by branching logic?**

**A:** No. Query icons are only displayed for variables that are currently visible on screen. If a variable is hidden by branching logic or embedded within another field, you cannot attach a query to it directly. You may need to temporarily satisfy the branching condition to make the variable visible, or document the issue using an alternative approach (such as a comment on a related visible field).

**Q: Who can reopen a closed query?**

**A:** Any user with Open, Close, and Respond rights can reopen a closed query by clicking its icon and selecting the appropriate action. The query returns to Open / Unresolved (Unresponded) status and REDCap logs the reopening event.

**Q: Will the Data Quality module find variables with closed or verified queries?**

**A:** By default, yes — the Data Quality module evaluates all variables regardless of query status. If you enable the **Hide closed/verified data queries from Data Quality results** setting (Project Setup → Additional customizations), variables with a closed or verified query will be excluded from Data Quality rule results. This setting only affects Data Quality rule results; it does not affect what is visible in the Data Resolution Dashboard.

**Q: Can I assign a query to a user who has No Access DRW rights?**

**A:** The assignment dropdown will show project members, but assigning a query to a user with No Access means they will not be able to see or act on it. Set appropriate DRW rights before establishing assignment workflows.

---

# 9. Common Mistakes & Gotchas

**Starting data collection before setting DRW user rights.** When DRW is enabled, all existing and new users default to View Only rights. Data entry staff who need to open queries will be unable to do so until rights are explicitly updated. Review and set DRW rights for every user or role before opening a project for data entry.

**Switching modes after data collection has begun.** Switching from the Field Comment Log to DRW (or the reverse) does not migrate existing annotations. Comments made under the Field Comment Log will not appear in the DRW dashboard, and vice versa. This creates a split record of data quality activity that complicates audits. Commit to one mode before data entry begins.

**Closing a query before the underlying issue is resolved.** Because closure requires only a short comment, it is easy to close a query prematurely. Closed queries can always be reopened, but doing so resets them to Unresponded status, losing the responded context. Establish team norms for what constitutes a resolvable issue before using the Close function.

**Expecting rule-based queries to link to a variable in the record.** Queries opened from multi-variable custom Data Quality rules are attached to the rule, not to a specific variable. These queries will not display a query icon next to any variable in the record. If your team expects to click on an icon in the record to manage a query, rule-based queries will be confusing — manage them exclusively through the Data Resolution Dashboard.

**Not using Resolution Metrics for project oversight.** Teams often focus on the Resolve Issues tab and overlook the Resolution Metrics tab entirely. The metrics can surface patterns that are not visible record-by-record — for example, a single variable that accounts for 40% of all queries, which might indicate an instrument design problem rather than a data entry problem.

---

# 10. Related Articles

- RC-DE-02 — Basic Data Entry (foundational data entry skills required before using the DRW)
- RC-DE-04 — Editing Data & Audit Trail (related audit features; the DRW is itself an audit trail for data quality decisions)
- RC-DE-08 — Field Comment Log (the simpler annotation alternative to the DRW; also covers setup shared between both modes)
- RC-DE-05 — Field Validations (field validations and DRW queries are often used together to document out-of-range or exceptional values)
- RC-DAG-01 — Data Access Groups (the DRW dashboard can be filtered by DAG; useful context for multi-site projects)

RC-CC-09

**To-Do List**

| **Article ID** | RC-CC-09 |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CC-01 — Notifications & Reporting; RC-PROJ-01 — Project Lifecycle: Status and Settings |

---

# 1. Overview

The To-Do List is the REDCap administrator's task queue for pending action items that require review or approval. Accessible from the top of the Control Center sidebar at `ToDoList/index.php`, the To-Do List displays requests generated automatically by REDCap when users perform actions requiring administrator review. This centralized queue helps administrators manage their workflow and ensure timely processing of critical tasks.

# 2. Active Requests

The main section of the To-Do List displays all pending tasks awaiting administrator action. 

**When empty:** If there are no pending items, the section displays "No requests to view."

**When populated:** Each active request displays:
- **Task type**: The category of request (e.g., "Approve draft changes")
- **Submission timestamp**: When the request was created
- **Requesting user**: The username or email of the user who initiated the action
- **Project title**: The name of the project associated with the request

Administrators can click on any request to view details and take action.

# 3. Common Task Types

The most common task type is **"Approve draft changes"**, which is automatically generated when a project in Production mode has pending design changes submitted for review. This ensures administrators review and approve all structural changes to production projects before they take effect.

Other task types may appear depending on system configuration and feature usage, such as:
- Copy project requests requiring approval
- Project creation requests requiring approval
- Other custom workflows configured at your institution

# 4. Completing Tasks

To complete a task, administrators click on the request to open it. 

**For draft change approvals:**
- Administrators are taken to the project's draft review page
- The page displays all pending design changes
- Administrators can approve or reject the proposed changes
- Feedback can be provided to the requesting user if changes are rejected

After the administrator takes action (approve or reject), the request moves from the Active Requests section to the Completed & Archived section.

# 5. Completed & Archived Requests

A paginated history of all previously handled requests is maintained for audit and reference purposes. Each archived entry shows:

- **Task type**: The type of request
- **Submission timestamp**: When the request was originally created
- **Requesting user**: The user who initiated the request
- **Project title**: The name of the associated project
- **Completion timestamp**: When the administrator finished processing the request
- **Completing administrator**: The name of the administrator who processed it

The archived list is paginated and searchable, making it easy to locate past requests for compliance and audit purposes.

# 6. Relationship to Draft Mode

The To-Do List is tightly integrated with REDCap's Production mode workflow. 

**How it works:**
1. A project is placed in Production mode to lock design and restrict changes
2. A user with appropriate permissions submits design changes via Draft Mode
3. REDCap automatically creates an "Approve draft changes" task in the To-Do List
4. The administrator is typically notified by email of the pending request
5. The administrator reviews and approves or rejects the changes
6. The changes take effect (if approved) or are returned for revision (if rejected)

This workflow ensures that production projects remain stable and that all design modifications are intentionally reviewed and approved before implementation. See RC-PROJ-01 for detailed information on Production mode and the draft change process.

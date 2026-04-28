RC-CC-09

**To-Do List**

| **Article ID** | RC-CC-09 |
| --- | --- |
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-CC-01 — Notifications & Reporting; RC-PROJ-01 — Project Lifecycle: Status and Settings |

---

# 1. Overview

The To-Do List is the REDCap administrator's task queue for pending action items that require review or approval. Accessible from the top of the Control Center sidebar at `ToDoList/index.php`, the To-Do List displays requests generated automatically by REDCap when users perform actions requiring administrator review. This centralized queue helps administrators manage their workflow and ensure timely processing of critical tasks.

---

# 2. Active Requests

The main section of the To-Do List displays all pending tasks awaiting administrator action. 

**When empty:** If there are no pending items, the section displays "No requests to view."

**When populated:** Each active request displays:
- **Task type**: The category of request (e.g., "Approve draft changes")
- **Submission timestamp**: When the request was created
- **Requesting user**: The username or email of the user who initiated the action
- **Project title**: The name of the project associated with the request

Administrators can click on any request to view details and take action.

---

# 3. Common Task Types

The most common task type is **"Approve draft changes"**, which is automatically generated when a project in Production mode has pending design changes submitted for review. This ensures administrators review and approve all structural changes to production projects before they take effect.

Other task types may appear depending on system configuration and feature usage, such as:
- Copy project requests requiring approval
- Project creation requests requiring approval
- Other custom workflows configured at your institution

---

# 4. Completing Tasks

To complete a task, administrators click on the request to open it. 

**For draft change approvals:**
- Administrators are taken to the project's draft review page
- The page displays all pending design changes
- Administrators can approve or reject the proposed changes
- Feedback can be provided to the requesting user if changes are rejected

After the administrator takes action (approve or reject), the request moves from the Active Requests section to the Completed & Archived section.

---

# 5. Completed & Archived Requests

A paginated history of all previously handled requests is maintained for audit and reference purposes. Each archived entry shows:

- **Task type**: The type of request
- **Submission timestamp**: When the request was originally created
- **Requesting user**: The user who initiated the request
- **Project title**: The name of the associated project
- **Completion timestamp**: When the administrator finished processing the request
- **Completing administrator**: The name of the administrator who processed it

The archived list is paginated and searchable, making it easy to locate past requests for compliance and audit purposes.

---

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

---

# 7. Common Questions

**Q: Where is the To-Do List located in the Control Center?**
The To-Do List is accessible from the top of the Control Center sidebar at `ToDoList/index.php`. It is listed under the main navigation and is typically one of the first items visible to administrators.

**Q: How do I know when there are pending requests in the To-Do List?**
The To-Do List often displays a count of pending items in the sidebar or on the icon. Additionally, administrators may receive email notifications when new tasks are added (depending on your system configuration). Check the To-Do List regularly or configure email alerts to stay aware of pending actions.

**Q: Can I reject a draft change proposal and request revisions?**
Yes. When reviewing draft changes, administrators can reject the proposal and provide feedback to the requesting user. The user will then need to revise their proposal and resubmit it for approval. Rejected changes do not take effect and must be resubmitted.

**Q: What happens to a completed request in the To-Do List?**
After an administrator takes action on a request (approves or rejects it), the request automatically moves from the Active Requests section to the Completed & Archived Requests section. The archived entry remains in the system for audit purposes, showing when and by whom the task was completed.

**Q: How long are completed requests retained in the archive?**
Completed requests are retained indefinitely in the system for audit and compliance purposes. You can access the full history of past requests at any time, filtered by date or other criteria. This historical record is important for documenting institutional review and approval workflows.

**Q: Can I create tasks in the To-Do List manually, or are all tasks generated automatically?**
Tasks are generated automatically by REDCap when specific actions occur (such as draft design changes being submitted). Administrators cannot manually create arbitrary tasks in the To-Do List. The list serves as a system-driven workflow queue, not a general task management tool.

---

# 8. Common Mistakes & Gotchas

**Missing draft change notifications.** Administrators may not realize that draft changes have been submitted if they don't check the To-Do List regularly and have not configured email notifications. Establish a routine to check the To-Do List daily, or configure your system to send email alerts when production projects have pending changes awaiting review.

**Accidentally rejecting changes without clear feedback.** If you reject a draft change proposal without providing detailed feedback, the requesting user may resubmit the same changes without understanding why they were rejected. Always include specific feedback explaining what needs to change or why the proposal was not approved.

**Forgetting that approved changes affect active projects immediately.** When you approve draft changes to a production project, the changes take effect immediately. Users currently working with the project may see the updated design in real-time. Communicate with your research teams about planned design changes, and consider scheduling approvals during maintenance windows or off-peak hours to minimize disruption.

**Archived requests becoming lost in pagination.** If your institution has many historical requests, the Completed & Archived Requests section becomes long and requires pagination. Use search and date filters to locate specific past requests rather than scrolling through pages.

---

# 9. Related Articles

- RC-CC-01 — Notifications & Reporting
- RC-PROJ-01 — Project Lifecycle: Status and Settings

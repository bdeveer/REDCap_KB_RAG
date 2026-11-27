

**To-Do List**

| **Article ID** | [RC-CC-09 — Control Center: To-Do List](RC-CC-09_To-Do-List.md) |
|---|---|
| **Domain** | Control Center (Admin) |
| **Applies To** | REDCap administrators |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — To-Do List request handling behaviour checked against source code; page sections, the email checkbox and Export list checked live on v17.5.6 (Standard), read-only; no requests were present, so request handling was not exercised live |
| **Prerequisite** | REDCap administrator access |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md); [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) |
| **Synonyms** | control center to-do list task queue; approve draft changes requests admin; pending administrator action items; where do i review user requests in redcap; approve project move to production; admin approval queue control center; export the to-do list; low priority pending requests; list of tasks awaiting administrator review; handle pending requests from users |

---

## 1. Overview

The To-Do List is the REDCap administrator's task queue for pending action items that require review or approval. Accessible from the top of the Control Center sidebar at `ToDoList/index.php`, the To-Do List displays requests generated automatically by REDCap when users perform actions requiring administrator review. This centralized queue helps administrators manage their workflow and ensure timely processing of critical tasks.

> **Version caveat (who can open it):** On 16.0 LTS only administrators with access to all projects can open the To-Do List. On 17.x, administrators with project-level admin rights can also open it, but they see only the requests for the projects they administer.

---

## 2. Pending Requests

The main section, **Pending Requests**, displays all pending tasks awaiting administrator action. Older documentation may call it Active Requests. A separate **Low Priority Pending Requests** section sits below it. Each section heading shows its count.

Above the lists are an **Enable email notifications for administrators** checkbox and an **Export list** button.

- **Enable email notifications for administrators** is a single system-wide setting, not a personal preference: ticking or unticking it changes notifications for every administrator, and the change is logged. It is on by default. On 17.x only full administrators see the checkbox.
- **Export list** downloads a CSV of all requests (pending, low priority and archived). The export is logged.

The To-Do List badge in the Control Center sidebar counts pending plus low-priority requests.

**When empty:** If there are no pending items, the section displays "No requests to view."

**When populated:** Each request row shows:
- **Request number**
- **Task type**: The category of request (e.g., "Approve draft changes")
- **Submission timestamp**: When the request was created
- **Project ID (PID)**: The project the request belongs to
- **Requesting user**: The user who initiated the action

Expand a row to see the project title and any comments. Each row has actions to process the request (approve), add a comment, move it to **Low Priority Pending Requests**, or archive it.

On 17.x each section has a free-text search box, and the low-priority and archived lists show 10 rows per page.

---

## 3. Common Task Types

The most common task type is **"Approve draft changes"**, which is automatically generated when a project in Production mode has pending design changes submitted for review. This ensures administrators review and approve all structural changes to production projects before they take effect.

Other task types appear depending on which features your system routes through administrator approval:
- Create project and copy project requests
- Move to production requests
- Delete project requests
- API token requests
- External Module activation requests
- MyCap enable requests
- Twilio and Mosio (SMS/voice) enable requests
- Public report and public project dashboard requests
- Data Mart revision requests
- Participant Compensation requests (17.x)
- Sponsor requests
- AI Chatbot enable requests (present in 17.6)

> **Institution-specific:** Which of these requests reach the To-Do List depends on how your administrators have configured the system (for example, whether users can move projects to production or create API tokens themselves). Check with your REDCap administrators.

---

## 4. Completing Tasks

To complete a task, administrators select the request to open it. For most request types the approval page opens in a pop-up on the To-Do List page. Archiving a request without approving it is, for most request types, how you decline it.

**For draft change approvals:**
- Administrators are taken to the project's draft review page
- The page displays all pending design changes
- Administrators can approve or reject the proposed changes
- Reject takes no comments: REDCap sends the requester a standard email saying the changes were rejected. The rejected changes stay in Draft Mode for the user to revise and resubmit. To explain why, email the user separately (the confirmation page offers an email link to the requester)

After the administrator takes action (approve or reject), the request moves from the Pending Requests section to the Completed & Archived section.

Requests also complete themselves when the requested action is done anywhere in REDCap (for example, an administrator approves the drafts from the project itself). Requesters can cancel their own pending move-to-production or delete-project request.

---

## 5. Completed & Archived Requests

A paginated history of all previously handled requests is maintained for audit and reference purposes. Each archived row shows the same columns as a pending request (request number, task type, submission timestamp, PID, requesting user) plus a **Status** column. Expand the row to see:

- **Project title**: The name of the associated project
- **Comments** added while the request was open
- **Completion timestamp**: When the request was completed
- **Completing administrator**: Who processed it

On 17.x the archived list is paginated and has a free-text search box, which is the quickest way to find a past request by PID, user or type.

> **Version caveat (16.0 LTS):** The archived list is paginated and sortable by column but has no search box. Sort by the column you need (for example, request time or PID), or use **Export list** and search the CSV.

---

## 6. Relationship to Draft Mode

The To-Do List is tightly integrated with REDCap's Production mode workflow. 

**How it works:**
1. A project is placed in Production mode to lock design and restrict changes
2. A user with appropriate permissions submits design changes via Draft Mode
3. REDCap automatically creates an "Approve draft changes" task in the To-Do List. If the changes qualify for automatic approval, they are applied straight away and no To-Do List task is created
4. The administrator is typically notified by email of the pending request (no administrator email is sent when the submitter is an administrator). From 17.5.1, these To-Do List request emails are logged under their own **To-Do List Request** category in Email Logging, which also has a matching filter option — useful for confirming a notification went out. On 17.3 and 16.0 LTS this category isn't there; look for the notification among the general email log entries instead
5. The administrator reviews and approves or rejects the changes
6. The changes take effect (if approved) or stay in Draft Mode for the user to revise and resubmit (if rejected)

This workflow ensures that production projects remain stable and that all design modifications are intentionally reviewed and approved before implementation. See [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) for detailed information on Production mode and the draft change process.

---

## 7. Common Questions

**Q: Where is the To-Do List located in the Control Center?**
The To-Do List is accessible from the top of the Control Center sidebar at `ToDoList/index.php`. It is listed under the main navigation and is typically one of the first items visible to administrators.

**Q: How do I know when there are pending requests in the To-Do List?**
The To-Do List often displays a count of pending items in the sidebar or on the icon. Additionally, administrators may receive email notifications when new tasks are added (depending on your system configuration). Check the To-Do List regularly or configure email alerts to stay aware of pending actions.

**Q: Can I reject a draft change proposal and request revisions?**
Yes, but **Reject** has no feedback field. REDCap sends the requesting user a standard email saying the changes were rejected, and the changes stay in Draft Mode, where the user can revise them and resubmit. Rejected changes do not take effect. To tell the user what needs to change, email them yourself; the confirmation page after rejecting has an email link to the requester.

**Q: What happens to a completed request in the To-Do List?**
After an administrator takes action on a request (approves or rejects it), the request automatically moves from the Pending Requests section to the Completed & Archived Requests section. The archived entry remains in the system for audit purposes, showing when and by whom the task was completed.

**Q: How long are completed requests retained in the archive?**
Completed requests are retained indefinitely in the system for audit and compliance purposes. You can access the full history of past requests at any time: on 17.x use the search box on the archived list; on 16.0 LTS sort the columns, or use **Export list** for the full CSV. This historical record is important for documenting institutional review and approval workflows.

**Q: Can I create tasks in the To-Do List manually, or are all tasks generated automatically?**
Tasks are generated automatically by REDCap when specific actions occur (such as draft design changes being submitted). Administrators cannot manually create arbitrary tasks in the To-Do List. The list serves as a system-driven workflow queue, not a general task management tool.

---

## 8. Common Mistakes & Gotchas

**Missing draft change notifications.** Administrators may not realize that draft changes have been submitted if they don't check the To-Do List regularly and have not configured email notifications. Establish a routine to check the To-Do List daily, or tick **Enable email notifications for administrators** at the top of this page.

**Rejecting changes without explaining why.** **Reject** sends only a standard "changes were rejected" email, so the requesting user may resubmit the same changes without knowing what was wrong. Always follow a rejection with your own email explaining what needs to change or why the proposal was not approved (the confirmation page has an email link to the requester).

**Forgetting that approved changes affect active projects immediately.** When you approve draft changes to a production project, the changes take effect immediately. Users currently working with the project may see the updated design in real-time. Communicate with your research teams about planned design changes, and consider scheduling approvals during maintenance windows or off-peak hours to minimize disruption.

**Archived requests becoming lost in pagination.** If your institution has many historical requests, the Completed & Archived Requests section becomes long and requires pagination. On 17.x use the search box to locate specific past requests rather than scrolling through pages; on 16.0 LTS sort by a column or search the **Export list** CSV.

---

## 9. Related Articles

- [RC-CC-01 — Control Center: Notifications & Reporting (Dashboard)](RC-CC-01_Control-Center-Notifications-and-Reporting.md)
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)

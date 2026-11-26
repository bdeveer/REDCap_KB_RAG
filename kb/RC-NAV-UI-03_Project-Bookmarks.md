

**Project Bookmarks**

| **Article ID** | [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) |
|---|---|
| **Domain** | Project Navigation |
| **Applies To** | All project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Project Bookmarks behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md), [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md), [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md), [RC-PROJ-04 — Project Setup: Additional Customizations](RC-PROJ-04_Project-Setup-Additional-Customizations.md), [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md), [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md), [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Synonyms** | how to add a bookmark to the project menu; create a custom link in the left-hand menu; how to link to an external website from redcap; restrict a bookmark to certain users or dags; pass the current record id to a bookmark url; adding navigation shortcuts to a project; how to link between related redcap projects; custom menu links for project managers; do project bookmarks copy with copy project |

---

## 1. Overview

Project Bookmarks is a project-level module that allows project managers to create custom navigation links that appear on the left-hand project menu. Each bookmark is a configurable web link — pointing to another page within REDCap, another REDCap project, or any external website — that users see and can click directly from the project menu. Bookmarks can be restricted to specific users or Data Access Groups, and can be configured to pass contextual information (such as the current record or project ID) to the destination URL. Projects that require users to navigate frequently between related tools, external data systems, or companion REDCap projects benefit from having direct links built into the project menu rather than relying on users to find and remember URLs separately.

---

## 2. Key Concepts & Definitions

### 2.1 Where Project Bookmarks Appear

Project Bookmarks are configured from the **Project Setup** page (**Set up project bookmarks (optional)** → **Add or edit bookmarks**), which requires the **Project Design and Setup** user right. Once a bookmark is saved, it appears as a clickable link in the **Project Bookmarks** section of the left-hand project menu for every user allowed to see it. The section only appears when the current user can see at least one bookmark; users with Project Design and Setup rights also get an **Edit** link in that section, which opens the setup page.

**Administrators** see every bookmark regardless of its User Access setting. When an administrator impersonates a user, the menu shows that user's view.

**Custom Application Links** are the system-wide equivalent: administrators create them in **Control Center → Custom Application Links**, and they appear at the bottom of the **Applications** section in every project. They can be limited to certain users or excluded from certain projects. Custom Application Links support Smart Variables only; field-variable piping works only in project bookmarks.

### 2.2 Link Types

Each bookmark has a **link type** that determines how the link behaves when clicked:

**Simple Link** — A standard HTML hyperlink that takes the user to the specified URL. The destination site receives no information about who is visiting. This is the appropriate choice for most use cases.

**REDCap Project Link** — A simplified option for linking to another REDCap project. Instead of entering a URL manually, the user selects a project from a list of REDCap projects they have access to. The link is then built automatically. This is useful for connecting related projects that users must navigate between frequently. For a regular user, the list shows all of their own projects (including those in Analysis/Cleanup or marked Completed). For an administrator, the list shows Development and Production projects that any user of the current project can access. When the user clicks a REDCap Project bookmark from inside a record, the record name (and event, in longitudinal projects) is always appended; **Append project ID to URL** has no effect on this link type.

**Advanced Link** — A developer-oriented option that uses an HTTP POST request to send an identity token (authkey) to the destination website, allowing the external site to verify who the REDCap user is. This requires that the destination site be developed or managed by someone who can write the necessary server-side code to receive and process the authkey. The option is only offered when the API is enabled on your REDCap server. See Section 4 for technical details.

### 2.3 User Access

By default, a bookmark is visible to **All users** in the project. Access can instead be restricted to **Selected users** or **Selected DAGs** (the DAG option is offered only if the project has Data Access Groups), in which case a list of users or DAGs appears for selection. Users or DAGs not in the selected list will not see the bookmark in their menu, and users who are not assigned to any DAG do not see DAG-restricted bookmarks. Removing a user from the project also removes them from bookmark user lists.

### 2.4 Piping in Bookmark URLs

Field variables and Smart Variables can be piped directly into the URL of a Project Bookmark:

- **Smart Variables** that do not require a record context (e.g., `[redcap-base-url]`) work in all situations.
- **Field variables** and **record-context Smart Variables** (e.g., `[record-name]`, `[previous-event-name]`) only resolve when the user is inside a record — for example, while viewing the Record Home Page or a data entry form. If the user is not in a record context when clicking the bookmark, these variables will not resolve.

### 2.5 Append Options

Two optional settings let a bookmark automatically append information to the URL:

**Append record info to URL** — When checked, REDCap appends the current record name and (for longitudinal projects) the current event name to the URL's query string in the form `record=RECORDNAME&event=UNIQUEEVENTNAME`. This works when the user clicks the bookmark while viewing a data collection form inside a record, or from the Record Home Page (where only the record name is appended, with no event). If the user is not inside a record, nothing is appended. This is useful when linking to an external system that can display record-specific information.

> **Privacy warning:** If record names in the project are themselves identifiers (e.g., social security numbers, medical record numbers), enabling this option will send those identifiers to the external site. Only use this option when you control or trust the destination site and have confirmed it is appropriate to share record names.

**Append project ID to URL** — When checked, REDCap appends `pid=PROJECTID` to the URL. This is useful when a single external website serves multiple REDCap projects and needs to distinguish which project the user is coming from.

---

## 3. How To

### 3.1 Navigate to Project Bookmarks

From within a project, go to **Project Setup** and, under **Set up project bookmarks (optional)**, click **Add or edit bookmarks**. This opens the Project Bookmarks setup page. Once at least one bookmark is visible, you can also use the **Edit** link in the **Project Bookmarks** section of the left-hand menu.

> Configuring Project Bookmarks requires the **Project Design and Setup** user right. Users without it will not see the configuration interface, though they still see the bookmarks they are allowed to see in the menu.

### 3.2 Add a New Bookmark

1. On the Project Bookmarks setup page, click **Add a new bookmark** (or click directly into the empty row at the bottom of the bookmarks table).
2. Fill in the **Link Label** — this is the text that will appear on the left-hand menu.
3. Enter the **Link URL** — the full web address of the destination page. For REDCap Project links, select the project from the dropdown instead of typing a URL.
4. Select the **Link Type** (Simple Link, Advanced Link, or REDCap Project). URLs starting with `javascript:` or `vbscript:` are not accepted.
5. Set **User Access** to "All users," "Selected users" or "Selected DAGs," and if restricting, select which users or DAGs can see the link.
6. Optionally check:
   - **Opens new window** — the link opens in a new browser tab/window
   - **Append record info to URL** — appends record name and event name (record context only)
   - **Append project ID to URL** — appends the project's pid
7. Click **Add** to save the bookmark.

### 3.3 Edit an Existing Bookmark

Click a bookmark's label or URL in the table to open it in an edit box, make the change, then click **Save**. Other options are changed in the same row. Changes are not saved until you click Save; clicking away from the field does not save them.

### 3.4 Reorder Bookmarks

Bookmarks can be dragged and reordered using the drag handle on the left side of each row. The order in the table matches the order they appear in the left-hand menu.

### 3.5 Delete a Bookmark

Click the **Delete** button in the rightmost column of the bookmark row and confirm the prompt. The bookmark is then removed.

Clicks on bookmarks are recorded in the project's Logging as "Click project bookmark".

---

## 4. Advanced Link — Technical Reference

The Advanced Link type is intended for scenarios where an external website needs to confirm the identity of the REDCap user who clicked the link. It is not a standard HTML anchor — it submits an HTTP POST request to the destination URL.

**How it works:**

1. When the user clicks an Advanced Link, REDCap generates an authkey and sends it to the destination URL via HTTP POST (the POST body contains a single field named `authkey`).
2. The destination site receives the authkey and posts it back to the REDCap API to confirm who the user is. This API request requires only two parameters: `authkey` (the value received) and `format` (response format: `csv`, `json`, or `xml`; defaults to `csv` if omitted). No API token is needed for this specific call. The authkey works only while the user's REDCap session is active, so the destination site should check it promptly.
3. REDCap validates the authkey and returns the following fields: `username`, `project_id`, `data_access_group_name`, `data_access_group_id`, and `callback_url`. If the authkey is invalid or the user's session has expired, REDCap returns `0`.
4. The external site can then use the returned values (e.g., the username) to verify identity and implement whatever user-specific logic it requires.

**Requirements:**
- The external site must be developed or maintained by someone with server-side programming skills.
- The external site must handle the POST request and API callback programmatically.
- The REDCap API is language-agnostic; the POST request can be made from any server-side language. No API token is required for the authkey validation call specifically.

If the steps above are unclear or not feasible for your team, the Advanced Link may not be a viable option. If you still wish to proceed, consider engaging a web developer who can write the necessary server-side script on the external site to handle the authkey exchange. If no developer is available, use a Simple Link instead.

---

## 5. Common Questions

**Q: Who can create and configure project bookmarks?**
Users with the **Project Design and Setup** user right. The setup page is reached from **Project Setup → Set up project bookmarks (optional) → Add or edit bookmarks**.

**Q: Can I link to a REDCap project I don't have access to?**
Not with a REDCap Project link. Regular users can only pick from their own projects. Administrators pick from Development and Production projects that any user of the current project can access.

**Q: Do project bookmarks appear for survey participants?**
No. Project Bookmarks appear in the left-hand project menu, which is only visible to authenticated REDCap users working within the project. Survey respondents do not see the project menu.

**Q: Can I use the same bookmark setup in multiple projects?**
Yes, by copying the project. **Copy Project** copies bookmarks when the **Project bookmarks** box is ticked (it is ticked by default when the project has bookmarks), and projects created from a template get the template's bookmarks. Bookmarks are not included in the REDCap Project (XML) export, so a project created from an XML file starts without them. For a system-wide link in every project, ask an administrator about Custom Application Links.

**Q: Who sees a bookmark limited to selected users or DAGs?**
Only the selected users, or members of the selected DAGs. Administrators always see every bookmark; impersonate a user to check what that user sees.

**Q: Can I use Smart Variables in the URL?**
Yes. Smart Variables that work outside a record context (such as `[redcap-base-url]` or `[project-id]`) can be used freely. Field variables and record-context Smart Variables only resolve when the user is in a record context.

**Q: What happens if the "Append record info" option is enabled but the user clicks the bookmark outside of a record?**
Nothing is appended to the URL. The user is taken to the base URL without any record or event parameters added. From the Record Home Page, the record name is appended but not the event.

**Q: Can I restrict a bookmark to a specific Data Access Group?**
Yes. Set User Access to "Selected DAGs" (offered only when the project has DAGs) and choose the groups. Users in groups not selected, and users not assigned to any DAG, will not see the bookmark.

---

## 6. Common Mistakes & Gotchas

**PHI in record names.** Enabling "Append record info to URL" sends the record name to the destination website. If record names contain identifiers such as medical record numbers or social security numbers, this constitutes a data disclosure. Confirm with your privacy officer before enabling this option for projects with identifiable record names.

**Advanced Link requires a developer.** The Advanced Link type generates an authkey that is useless unless the destination site has been specifically programmed to receive and validate it via the REDCap API. Do not select Advanced Link unless a developer who manages the destination site is involved.

**Bookmark labels that are too long.** The label appears in the left-hand menu, which has limited horizontal space. Very long labels may be truncated or wrap in a way that looks awkward. Keep labels short and descriptive.

**Links to other REDCap projects only list certain projects.** When a regular user creates a REDCap Project link, only that user's own projects appear in the selection list. An administrator's list shows Development and Production projects that any user of the current project can access.

**Restricted bookmarks disappear after Copy Project.** The copy keeps each bookmark's User Access setting but not its list of selected users or DAGs, so bookmarks limited to selected users or DAGs are hidden from non-admin users in the new project. After copying, open the bookmarks setup page in the new project and re-select the users or DAGs for each restricted bookmark.

**Field variables resolve only in record context.** Piping a field variable (e.g., `[my_field]`) into a bookmark URL will not work if the user clicks the bookmark from outside a record. Use Smart Variables that resolve globally (e.g., `[redcap-base-url]`) if the bookmark should work from anywhere in the project.

---

## 7. Related Articles

- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md)
- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md)
- [RC-PROJ-04 — Project Setup: Additional Customizations](RC-PROJ-04_Project-Setup-Additional-Customizations.md)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md)
- [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md)

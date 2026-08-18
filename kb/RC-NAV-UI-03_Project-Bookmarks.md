

**Project Bookmarks**

| **Article ID** | [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) |
|---|---|
| **Domain** | Project Navigation |
| **Applies To** | All project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md), [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md), [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md), [RC-PROJ-04 — Project Setup: Additional Customizations](RC-PROJ-04_Project-Setup-Additional-Customizations.md), [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md), [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md), [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) |
| **Synonyms** | how to add a bookmark to the project menu; create a custom link in the left-hand menu; how to link to an external website from redcap; restrict a bookmark to certain users or dags; pass the current record id to a bookmark url; adding navigation shortcuts to a project; how to link between related redcap projects; custom menu links for project managers |

---

## 1. Overview

Project Bookmarks is a project-level module that allows project managers to create custom navigation links that appear on the left-hand project menu. Each bookmark is a configurable web link — pointing to another page within REDCap, another REDCap project, or any external website — that users see and can click directly from the project menu. Bookmarks can be restricted to specific users or Data Access Groups, and can be configured to pass contextual information (such as the current record or project ID) to the destination URL. Projects that require users to navigate frequently between related tools, external data systems, or companion REDCap projects benefit from having direct links built into the project menu rather than relying on users to find and remember URLs separately.

---

## 2. Key Concepts & Definitions

### 2.1 Where Project Bookmarks Appear

Project Bookmarks are configured from the left-hand project menu under the **Project Bookmarks** section. Once a bookmark is created and saved, it appears as a clickable link in that section for all users who have access to it. The section only appears in the menu if at least one bookmark has been created for the project.

### 2.2 Link Types

Each bookmark has a **link type** that determines how the link behaves when clicked:

**Simple Link** — A standard HTML hyperlink that takes the user to the specified URL. The destination site receives no information about who is visiting. This is the appropriate choice for most use cases.

**REDCap Project Link** — A simplified option for linking to another REDCap project. Instead of entering a URL manually, the user selects a project from a list of REDCap projects they have access to. The link is then built automatically. This is useful for connecting related projects that users must navigate between frequently. Note that administrators can link to any project, while regular users can only link to projects they have access to.

**Advanced Link** — A developer-oriented option that uses an HTTP POST request to send an encrypted identity token (authkey) to the destination website, allowing the external site to verify who the REDCap user is. This requires that the destination site be developed or managed by someone who can write the necessary server-side code to receive and process the authkey. See Section 4 for technical details.

### 2.3 User Access

By default, a bookmark is visible to **all users** in the project. Access can instead be restricted to **selected users** or **selected Data Access Groups**, in which case a list of users or DAGs appears for selection. Users or DAGs not in the selected list will not see the bookmark in their menu.

### 2.4 Piping in Bookmark URLs

Field variables and Smart Variables can be piped directly into the URL of a Project Bookmark:

- **Smart Variables** that do not require a record context (e.g., `[redcap-base-url]`) work in all situations.
- **Field variables** and **record-context Smart Variables** (e.g., `[record-name]`, `[previous-event-name]`) only resolve when the user is inside a record — for example, while viewing the Record Home Page or a data entry form. If the user is not in a record context when clicking the bookmark, these variables will not resolve.

### 2.5 Append Options

Two optional settings let a bookmark automatically append information to the URL:

**Append record info to URL** — When checked, REDCap appends the current record name and (for longitudinal projects) the current event name to the URL's query string in the form `record=RECORDNAME&event=UNIQUEEVENTNAME`. This only works when the user clicks the bookmark while viewing a data collection form inside a record. If the user is not inside a record, nothing is appended. This is useful when linking to an external system that can display record-specific information.

> **Privacy warning:** If record names in the project are themselves identifiers (e.g., social security numbers, medical record numbers), enabling this option will send those identifiers to the external site. Only use this option when you control or trust the destination site and have confirmed it is appropriate to share record names.

**Append project ID to URL** — When checked, REDCap appends `pid=PROJECTID` to the URL. This is useful when a single external website serves multiple REDCap projects and needs to distinguish which project the user is coming from.

---

## 3. How To

### 3.1 Navigate to Project Bookmarks

From within a project, click **Project Bookmarks** in the left-hand menu. This opens the Project Bookmarks setup page.

> Configuring Project Bookmarks requires appropriate user rights. Users without the necessary privileges will not see the configuration interface, though they may still see published bookmarks in the menu.

### 3.2 Add a New Bookmark

1. On the Project Bookmarks setup page, click **Add a new bookmark** (or click directly into the empty row at the bottom of the bookmarks table).
2. Fill in the **Link Label** — this is the text that will appear on the left-hand menu.
3. Enter the **Link URL** — the full web address of the destination page. For REDCap Project links, select the project from the dropdown instead of typing a URL.
4. Select the **Link Type** (Simple Link, Advanced Link, or REDCap Project).
5. Set **User Access** to either "All users" or "Selected users." If "Selected users" is chosen, select which users or DAGs can see the link.
6. Optionally check:
   - **Opens new window** — the link opens in a new browser tab/window
   - **Append record info to URL** — appends record name and event name (record context only)
   - **Append project ID to URL** — appends the project's pid
7. Click **Add** to save the bookmark.

### 3.3 Edit an Existing Bookmark

Click on the label or URL of an existing bookmark row to edit it inline. Changes save automatically when you click away from the field.

### 3.4 Reorder Bookmarks

Bookmarks can be dragged and reordered using the drag handle on the left side of each row. The order in the table matches the order they appear in the left-hand menu.

### 3.5 Delete a Bookmark

Click the **Delete** button in the rightmost column of the bookmark row. The bookmark is removed immediately.

---

## 4. Advanced Link — Technical Reference

The Advanced Link type is intended for scenarios where an external website needs to confirm the identity of the REDCap user who clicked the link. It is not a standard HTML anchor — it submits an HTTP POST request to the destination URL.

**How it works:**

1. When the user clicks an Advanced Link, REDCap generates an encrypted authkey and sends it to the destination URL via HTTP POST (the POST body contains a single field named `authkey`).
2. The destination site receives the authkey and must immediately send it back to the REDCap API via a POST request. This API request requires only two parameters: `authkey` (the value received) and `format` (response format: `csv`, `json`, or `xml`). No API token is needed for this specific call.
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
Users need the appropriate project user right to access the Project Bookmarks setup page. Project-level access to this feature is typically tied to project design or setup rights. Contact your REDCap administrator if you are unsure whether you have this right.

**Q: Can I link to a REDCap project I don't have access to?**
Regular users can only link to REDCap projects they have access to. Administrators can select any project in the system when creating a REDCap Project link.

**Q: Do project bookmarks appear for survey participants?**
No. Project Bookmarks appear in the left-hand project menu, which is only visible to authenticated REDCap users working within the project. Survey respondents do not see the project menu.

**Q: Can I use the same bookmark setup in multiple projects?**
No, bookmarks are configured per project and do not carry over to other projects. You must set them up separately in each project where they are needed.

**Q: Can I use Smart Variables in the URL?**
Yes. Smart Variables that work outside a record context (such as `[redcap-base-url]` or `[project-id]`) can be used freely. Field variables and record-context Smart Variables only resolve when the user is in a record context.

**Q: What happens if the "Append record info" option is enabled but the user clicks the bookmark outside of a record?**
Nothing is appended to the URL. The user is taken to the base URL without any record or event parameters added.

**Q: Can I restrict a bookmark to a specific Data Access Group?**
Yes. When setting User Access to "Selected users," you can choose specific users or specific Data Access Groups. Users in groups not selected will not see the bookmark.

---

## 6. Common Mistakes & Gotchas

**PHI in record names.** Enabling "Append record info to URL" sends the record name to the destination website. If record names contain identifiers such as medical record numbers or social security numbers, this constitutes a data disclosure. Confirm with your privacy officer before enabling this option for projects with identifiable record names.

**Advanced Link requires a developer.** The Advanced Link type generates an authkey that is useless unless the destination site has been specifically programmed to receive and validate it via the REDCap API. Do not select Advanced Link unless a developer who manages the destination site is involved.

**Bookmark labels that are too long.** The label appears in the left-hand menu, which has limited horizontal space. Very long labels may be truncated or wrap in a way that looks awkward. Keep labels short and descriptive.

**Links to other REDCap projects only list accessible projects.** When creating a REDCap Project link, only projects the current user can access appear in the selection list. If you need to link to a project you cannot access, an administrator must create the bookmark.

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

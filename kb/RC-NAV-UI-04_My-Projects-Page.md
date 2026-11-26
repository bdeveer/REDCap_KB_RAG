

**My Projects Page**

| **Article ID** | [RC-NAV-UI-04 — My Projects Page](RC-NAV-UI-04_My-Projects-Page.md) |
|---|---|
| **Domain** | Navigation — UI |
| **Applies To** | All REDCap users |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — My Projects page behaviour (including the Completed-project listing and access, checked earlier) checked against source code; pages not re-captured |
| **Prerequisite** | None |
| **Version** | 1.3 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md); [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md); [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md); [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) |
| **Synonyms** | where is the list of all my projects; how to find a project after logging in; organize my projects into folders; search and sort my project list; the landing page after i log into redcap; how to access a project i have rights to; my projects page features; managing many redcap projects |

---

## 1. Overview

The My Projects page is the usual landing page after login. (Brand-new users, and users whose first visit to My Projects was less than a week ago, land on the **Home** tab instead.) It lists every project the current user has access to and provides tools to find, organize, and navigate to those projects. Users with many projects benefit most from understanding the search, sort, and folder features covered in this article.

---

## 2. The Project List Table

Projects are displayed in a tabular grid with the following columns:

| Column | Description |
|---|---|
| **Project Title** | The project name. Click to open the project: it opens on **Project Setup** if the project is in Development and you have Project Design and Setup rights, otherwise on **Project Home**. Extra markers can follow the title: **OFFLINE** (an administrator has taken the project offline), **(drafted changes are in review)**, a note icon (the project has a project note), a template star (administrators only), and a red **Completed** label. |
| **PID** | The numeric project ID. Administrators with system-configuration access can click the PID to go directly to the Control Center's Edit Project Settings page for that project. |
| **Records** | The record count for the whole project, even if you are assigned to a Data Access Group and can only see some of those records. Linked to the Record Status Dashboard. |
| **Fields** | The total field count. Linked to the Online Designer if you have Project Design and Setup rights, otherwise to the Codebook. |
| **Instruments** | The number of instruments in the project. |
| **Type** | An icon showing whether the project is longitudinal or classic. It reflects longitudinal vs classic only: a classic project with repeating instruments shows the classic icon, even though its tooltip mentions repeating forms. |
| **Status** | An icon indicating the current project lifecycle status: grey wrench = Development, green check-square = Production, red minus-circle = Analysis/Cleanup, red archive box = Completed (Completed projects also get a red **Completed** label after the title). |

**Template projects** (set by an administrator) are marked with a star icon in the Project Title column. This indicator is visible to administrators only.

**Sorting:** Click a column header to sort the entire list by that column. Clicking a second time on the same header reverses the sort direction. Sorting ignores folders: the list becomes a single flat list of all projects. Non-administrators cannot sort by **Status**.

---

## 3. Searching and Filtering

A **"Filter projects by title"** text box appears at the top right of the project table. Typing in this box dynamically filters the visible projects. The filter is case-insensitive, and if you type several words, a project is shown only when all of them appear in its row.

**Persistent search:** By default the filter clears when you navigate away from the page. A small toggle button (the floppy-disk icon with a red slash) next to the search box controls whether the search term is remembered between page visits. Click the button to enable persistence; click again to return to the default (non-persistent) behavior. The current state is shown by the presence or absence of the red slash.

---

## 4. Project Folders

### 4.1 What Project Folders Are

Project Folders are a personal organization system that lets each user group their projects into named folders on the My Projects page. Folders are visible **only to the user who created them** — other users cannot see your folder structure. The one exception: an administrator who views your project list from the Control Center sees it with your folders.

A project can be assigned to **multiple folders simultaneously**. Assigning a project to a folder does not move or remove it from other folders or from the unfoldered view.

### 4.2 Opening the Organize Dialog

Click the **Organize** button (folder icon, green text) in the header of the My Projects table. This opens the "Organize Projects" dialog, which is divided into two steps.

### 4.3 Step 1 — Create Folders

The left panel of the dialog shows your existing folders and a text input to create new ones.

- Type a name (up to 64 characters) in the **New Folder** input and click **Add** (or press Enter) to create a folder. There is no limit on the number of folders, but two folders cannot have the same name.
- Each folder can be given its own text and background colour.
- To **delete** a folder, use the delete control next to its name in the list and confirm. Deleting a folder removes the folder and its project assignments; it does not affect the projects themselves.
- To **reorder** folders, drag and drop them within the left-hand table. The order you set here controls how folders appear on the My Projects page.

### 4.4 Step 2 — Assign Projects to Folders

The right panel lists the projects the current user can access. Completed projects are not listed here. Use this panel to assign projects to whichever folder is currently selected in the left panel.

- Use the **"Filter projects by title"** input in the right panel to narrow the project list.
- Check the **"Hide projects already assigned"** checkbox to hide projects that are already in any *other* folder (projects in the selected folder stay visible so you can uncheck them) — useful when working through a large project list. The checkbox setting is kept for the rest of your session.
- Check the checkbox next to a project to assign it to the selected folder; uncheck to remove it from that folder.

### 4.5 Collapsing and Expanding Folders

On the My Projects page, each folder appears as a collapsible row. Click the folder row to toggle it between expanded (projects visible) and collapsed (projects hidden). REDCap remembers which folders you collapsed the next time you visit. Projects that are not in any folder appear in an **Unorganized Projects** group at the top, which cannot be collapsed.

The **Collapse All** button (folder-minus icon) in the table header collapses every folder in one click. There is no separate "Expand All" button — click individual folder rows to reopen them.

Sorting the project list (by clicking a column header) replaces the folder view with a single flat list.

### 4.6 The "My Hidden Projects" Folder

REDCap includes a built-in special folder called **My Hidden Projects**. Its behavior differs from user-created folders:

- Projects assigned to My Hidden Projects are **kept out of the unorganized project list** and instead appear in a permanently collapsed folder at the very bottom of the My Projects page.
- This folder is designed for projects you want to retain access to but do not need to see routinely — for example, completed studies you are still a member of, or sandbox/test projects that clutter the list.
- My Hidden Projects behaves like any other folder for assignment purposes (use the Organize dialog, Step 2), but it cannot be renamed or deleted.
- Projects in My Hidden Projects remain fully accessible — clicking to expand the folder reveals them and they can be opened normally.
- A hidden project that is also in one of your own folders still appears in that folder.

> **Tip:** My Hidden Projects is the recommended approach for decluttering your list. It is preferable to requesting project deletion or waiting for a project to reach Completed status, because it keeps you available on the project if needed while removing it from day-to-day view.

---

## 5. Completed Projects

Projects in **Completed** status are hidden from the main My Projects list. To see them, scroll to the bottom of the My Projects page and click **"Show Completed Projects"** (click **"Hide Completed Projects"** to hide them again). The link appears only if you are a member of at least one Completed project. Completed projects are then shown in place, including inside any folders they belong to.

Each one is marked **Completed**, and its name is still a link, but listing is not access. If you open a Completed project, REDCap removes all your project rights for as long as it stays Completed, so the menu is essentially empty and you cannot view, enter or export data. Only a REDCap administrator can return it to its previous status, which gives you your rights back. See [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) for full details on project statuses and transitions.

---

## 6. Creating a New Project

The **New Project** link in the top navigation bar (green, with a plus icon) opens the project creation workflow. It appears only if you are allowed to create or request projects. Depending on your institution's configuration, this may be a direct creation form or a request form that goes to an administrator for approval. See [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) for how project creation rights are configured.

> **Version caveat (17.x vs 16 LTS):** On 17.x, if you belong to an Access Control Group, the group's project-creation setting decides whether the **New Project** tab appears, overriding your own user setting. On 16 LTS only your own user setting counts. If the tab is missing when you expect it, ask your REDCap administrator to check both settings.

---

## 7. Mobile View

On narrow screens (phones and small tablets), the tabular project grid is replaced by a scrollable list-group view. Each project appears as a row showing the project title, instrument count and type icon. The search box, **Organize** button and **Collapse All** button are not shown, and sorting by column header is not available in the mobile view.

---

## 8. Common Questions

**Q: I organized my projects into folders but my colleague can't see them.**

**A:** Project Folders are personal and private — only you can see your own folder structure. If your colleague wants a similar organization, they need to create their own folders in their account.

---

**Q: A project I was added to isn't showing up in My Projects.**

**A:** Check whether it may be assigned to your **My Hidden Projects** folder. Scroll to the bottom of My Projects and expand My Hidden Projects to look for it. It may also be Completed: click **"Show Completed Projects"** at the bottom of the page. Also verify you are logged in to the correct REDCap installation.

---

**Q: Can I assign one project to more than one folder?**

**A:** Yes. A project can appear in multiple folders at the same time. Open the Organize dialog and assign it to each folder you want it to appear in.

---

**Q: How do I remove a project from a folder without deleting it?**

**A:** Open the Organize dialog, select the folder in Step 1, then uncheck the project in Step 2. The project returns to its unfoldered state but is not deleted or removed from your project list.

---

**Q: I want to hide a project but keep access to it. What's the right approach?**

**A:** Assign it to the **My Hidden Projects** folder. The project stays out of your main list but remains fully accessible — you can expand My Hidden Projects at any time to open it. This is better than requesting deletion if you may need access again.

---

**Q: Where do Completed projects appear?**

**A:** They are hidden from the main list. Click **"Show Completed Projects"** at the bottom of the My Projects page to see them listed. Listing is not access: you can open one, but you will have no rights inside it. Only a REDCap administrator can return it to its previous status.

---

## 9. Related Articles

- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) (project statuses, Completed status, creating and deleting projects)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (the two-panel layout inside a project)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (the left-hand project menu)
- [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) (bookmarking specific pages within a project)

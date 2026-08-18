

**My Projects Page**

| **Article ID** | [RC-NAV-UI-04 — My Projects Page](RC-NAV-UI-04_My-Projects-Page.md) |
|---|---|
| **Domain** | Navigation — UI |
| **Applies To** | All REDCap users |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026-05-06 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md); [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md); [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md); [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) |
| **Synonyms** | where is the list of all my projects; how to find a project after logging in; organize my projects into folders; search and sort my project list; the landing page after i log into redcap; how to access a project i have rights to; my projects page features; managing many redcap projects |

---

## 1. Overview

The My Projects page is the default landing page after login. It lists every project the current user has access to and provides tools to find, organize, and navigate to those projects. Users with many projects benefit most from understanding the search, sort, and folder features covered in this article.

---

## 2. The Project List Table

Projects are displayed in a tabular grid with the following columns:

| Column | Description |
|---|---|
| **Project Title** | The project name, linked directly to Project Setup. Click to open the project. |
| **PID** | The numeric project ID. Administrators can click the PID to go directly to the Control Center's Edit Project Settings page for that project. |
| **Records** | The current record count. Linked to the Record Status Dashboard. |
| **Fields** | The total field count. Linked to the Online Designer. |
| **Instruments** | The number of instruments in the project. |
| **Type** | An icon indicating the project structure type. A stacked-layers icon indicates a longitudinal or repeating-instruments project; no icon (or a single-layer icon) indicates a classic project. |
| **Status** | An icon indicating the current project lifecycle status: wrench = Development, green checkmark = Production, magnifying glass = Analysis/Cleanup. |

**Template projects** (set by an administrator) are marked with a star icon in the Project Title column. This indicator is visible to administrators only.

**Sorting:** Click any column header to sort the entire list by that column. Clicking a second time on the same header reverses the sort direction. Sorting collapses all open folders and sorts projects across the full list regardless of folder membership.

---

## 3. Searching and Filtering

A **"Filter projects by title"** text box appears at the top right of the project table. Typing in this box dynamically filters the visible projects to those whose titles contain the entered text. The filter is case-insensitive.

**Persistent search:** By default the filter clears when you navigate away from the page. A small toggle button (the floppy-disk icon with a red slash) next to the search box controls whether the search term is remembered between page visits. Click the button to enable persistence; click again to return to the default (non-persistent) behavior. The current state is shown by the presence or absence of the red slash.

---

## 4. Project Folders

### 4.1 What Project Folders Are

Project Folders are a personal organization system that lets each user group their projects into named folders on the My Projects page. Folders are visible **only to the user who created them** — other users and administrators cannot see your folder structure.

A project can be assigned to **multiple folders simultaneously**. Assigning a project to a folder does not move or remove it from other folders or from the unfoldered view.

### 4.2 Opening the Organize Dialog

Click the **Organize** button (folder icon, green text) in the header of the My Projects table. This opens the "Organize Projects" dialog, which is divided into two steps.

### 4.3 Step 1 — Create Folders

The left panel of the dialog shows your existing folders and a text input to create new ones.

- Type a name (up to 64 characters) in the **New Folder** input and click **Add** (or press Enter) to create a folder.
- To **delete** a folder, use the delete control next to its name in the list. Deleting a folder removes the folder and its project assignments; it does not affect the projects themselves.
- To **reorder** folders, drag and drop them within the left-hand table. The order you set here controls how folders appear on the My Projects page.

### 4.4 Step 2 — Assign Projects to Folders

The right panel lists all projects the current user can access. Use this panel to assign projects to whichever folder is currently selected in the left panel.

- Use the **"Filter projects by title"** input in the right panel to narrow the project list.
- Check the **"Hide projects already assigned"** checkbox to show only projects not yet assigned to the selected folder — useful when working through a large project list.
- Check the checkbox next to a project to assign it to the selected folder; uncheck to remove it from that folder.

### 4.5 Collapsing and Expanding Folders

On the My Projects page, each folder appears as a collapsible row. Click the folder row to toggle it between expanded (projects visible) and collapsed (projects hidden).

The **Collapse All** button (folder-minus icon) in the table header collapses every folder in one click. There is no separate "Expand All" button — click individual folder rows to reopen them.

Sorting the project list (by clicking a column header) automatically collapses all folders first.

### 4.6 The "My Hidden Projects" Folder

REDCap includes a built-in special folder called **My Hidden Projects**. Its behavior differs from user-created folders:

- Projects assigned to My Hidden Projects are **kept out of the main project list** and instead appear in a permanently collapsed folder at the very bottom of the My Projects page.
- This folder is designed for projects you want to retain access to but do not need to see routinely — for example, completed studies you are still a member of, or sandbox/test projects that clutter the list.
- My Hidden Projects behaves like any other folder for assignment purposes (use the Organize dialog, Step 2), but it cannot be renamed or deleted.
- Projects in My Hidden Projects remain fully accessible — clicking to expand the folder reveals them and they can be opened normally.

> **Tip:** My Hidden Projects is the recommended approach for decluttering your list. It is preferable to requesting project deletion or waiting for a project to reach Completed status, because it keeps you available on the project if needed while removing it from day-to-day view.

---

## 5. Completed Projects

Projects in **Completed** status are hidden from the main My Projects list. To access them, scroll to the bottom of the My Projects page and click **"Show Completed Projects."** This reveals all projects in Completed status that you were a member of.

Only a REDCap administrator can change a project's status once it reaches Completed. See [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) for full details on project statuses and transitions.

---

## 6. Creating a New Project

The **New Project** link in the top navigation bar (green, with a plus icon) opens the project creation workflow. Depending on your institution's configuration, this may be a direct creation form or a request form that goes to an administrator for approval. See [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) for how project creation rights are configured.

---

## 7. Mobile View

On narrow screens (phones and small tablets), the tabular project grid is replaced by a scrollable list-group view. Each project appears as a card showing the project title and basic metadata. Folder collapse controls and the search box remain available. Sorting by column header is not available in the mobile view.

---

## 8. Common Questions

**Q: I organized my projects into folders but my colleague can't see them.**

**A:** Project Folders are personal and private — only you can see your own folder structure. If your colleague wants a similar organization, they need to create their own folders in their account.

---

**Q: A project I was added to isn't showing up in My Projects.**

**A:** Check whether it may be assigned to your **My Hidden Projects** folder. Scroll to the bottom of My Projects and expand My Hidden Projects to look for it. Also verify you are logged in to the correct REDCap installation.

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

**A:** They are hidden from the main list. Click **"Show Completed Projects"** at the bottom of the My Projects page to reveal them.

---

## 9. Related Articles

- [RC-PROJ-01 — Project Lifecycle: Status and Settings](RC-PROJ-01_Project-Lifecycle-Status-and-Settings.md) (project statuses, Completed status, creating and deleting projects)
- [RC-NAV-UI-01 — Project Navigation UI](RC-NAV-UI-01_Project-Navigation-UI.md) (the two-panel layout inside a project)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (the left-hand project menu)
- [RC-NAV-UI-03 — Project Bookmarks](RC-NAV-UI-03_Project-Bookmarks.md) (bookmarking specific pages within a project)

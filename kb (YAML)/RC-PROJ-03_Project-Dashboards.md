---
id: RC-PROJ-03
title: Project Dashboards
domain: Project
applies_to:
- All REDCap projects
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Project
  Dashboards behaviour checked against source code; pages not re-captured
prerequisites:
- None
version: '1.4'
last_updated: 2026-11
related:
- id: RC-PIPE-11
  title: 'Smart Variables: Aggregate Functions, Charts, and Tables'
- id: RC-PIPE-14
  title: 'Smart Variables: Project Dashboards'
- id: RC-PIPE-12
  title: 'Smart Variables: Optional Parameters for Aggregate Functions'
tags:
- project
synonyms:
- how do i create a project dashboard
- display summary statistics and charts for my project
- make a dashboard public for stakeholders
- add charts and tables to a dashboard page
- build a project summary page with smart variables
- share project data without a redcap account
- configure dashboard access
- project dashboard vs record status dashboard
- require redcap login to view a public dashboard
---

# 1. Overview

Project Dashboards are customizable summary pages within a REDCap project that display aggregate statistics, charts, tables, and free text about your project's data. Any user with **Project Design and Setup** rights can create and edit them; viewing a dashboard needs no special right, only dashboard access. A built-in wizard helps you construct Smart Function, Smart Table, and Smart Chart syntax without writing it by hand, and a list of examples is included on the dashboard edit page. Dashboards can be made publicly accessible — allowing stakeholders, sponsors, or participants to view project-level summaries without needing a REDCap account.

This article covers creating and configuring dashboards, writing dashboard content, making a dashboard public, and controlling access. For the smart variable syntax used to build the content that appears on dashboards (aggregate functions, charts, tables), see [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md). For embedding dashboard links in emails, surveys, and alerts, see [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md).

---

# 2. Key Concepts & Definitions

**Project Dashboard**

A configurable page within a REDCap project that displays summary information about project data. Each project can have multiple dashboards, each covering a different view or audience. Dashboards are distinct from the Record Status Dashboard (a system-generated table of record completion status), covered in [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md).

**Dashboard Content**

A dashboard has a title and a single **Dashboard content** box — a rich-text editor where you type everything the dashboard shows: headings, narrative text, formatting, and Smart Functions, Smart Tables, and Smart Charts. There are no separate widgets or content blocks; the layout is whatever you write in that one box, top to bottom.

**Smart Function**

A smart variable that calculates an aggregate statistic (count, sum, mean, median, min, max, standard deviation, or unique count) across project records and displays the result as a number. Example: `[aggregate-count:record_id]`.

**Smart Table**

A smart variable that renders a table of descriptive statistics for one or more fields. Example: `[stats-table:age,weight,bmi]`.

**Smart Chart**

A smart variable that renders a chart (bar, pie, donut, scatter, or line) from project data. Example: `[bar-chart:study_arm]`.

The full syntax reference for all three types is in [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md).

**Public Dashboard**

A dashboard that has been made accessible via a direct URL to users who do not have a REDCap account. Public dashboards can optionally require an access code or, on REDCap+ servers, a REDCap login (Section 5.5).

**Dashboard Unique Name**

A system-generated identifier in the format `D-` followed by 10 characters (e.g. `D-557DRCW87L`) assigned to each dashboard. Used in smart variable syntax (see [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md)). It is shown in the **Unique dash name** column of the dashboard list on the Project Dashboards page, not on the dashboard's edit page.

**Dashboard Access Code**

An optional code required to view a public dashboard. If configured, users must enter the code to proceed past the landing page.

---

# 3. Creating and Configuring a Dashboard

## 3.1 Accessing the Dashboard Builder

Click **Project Dashboards** in the **Applications** section of the left-hand project menu to open the dashboard management page (**My Project Dashboards**). This link appears only for users with **Project Design and Setup** rights, and only those users can create, edit, copy, delete, reorder, or make dashboards public. No Draft Mode approval is required to create or edit dashboards, even in Production.

Users without Design rights reach dashboards through the separate **Project Dashboards** panel in the left-hand menu, which lists the dashboards they have access to (Section 5.4).

## 3.2 Creating a New Dashboard

1. On the Project Dashboards management page, click **Create New Dashboard**.
2. Enter a **Dashboard title** — this is the human-readable name shown in the interface and used as default link text in smart variables.
3. Type the dashboard's text and smart variables into the **Dashboard content** box (Section 4).
4. Optionally adjust **User access** (Section 5.4).
5. Click **Save Dashboard**. A confirmation dialog offers **Continue editing dashboard**, **Return to My Dashboards**, or **View dashboard**.

There is no separate description field: a dashboard consists of its title, its content, its user access settings, and its public settings. Title, content, and at least one user with access are all required to save.

After saving, find the **Dashboard Unique Name** in the **Unique dash name** column of the dashboard list — you will need it if you plan to reference the dashboard in piping or smart variables (see [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md)).

## 3.3 The Smart Variable Wizard

The dashboard edit page includes a wizard (**Use the Wizard**) to help you construct Smart Function, Smart Table, and Smart Chart syntax without writing it manually. Work through its steps: choose the smart variable type, choose one or more fields, and optionally filter by a report, DAGs, or events. The wizard builds the syntax; click to copy it to the clipboard and paste it into the **Dashboard content** box yourself — it does not insert the syntax for you. A list of working examples is also provided on the edit page as a reference.

## 3.4 Dashboard Settings and Management

On the dashboard's edit page you can:

- **Rename** the dashboard title.
- **Configure user access** — each dashboard has its own access settings controlling which project users can view it (see Section 5.4).
- **Make the dashboard public** (see Section 5).
- **Set or remove the access code** for public dashboards.

From the dashboard list on the management page you can:

- **Copy** a dashboard. The copy is a new dashboard with its own unique name and its own public link.
- **Delete** a dashboard. REDCap asks for confirmation; deletion is permanent with no undo (the deletion is recorded in the project Logging).
- **Reorder dashboards** by dragging them up or down.
- **Organize dashboards into folders** and **search by title**. Folders are visible to all project users who can view at least one dashboard in the folder.

---

# 4. Adding Content to a Dashboard

## 4.1 The Dashboard Content Box

All of a dashboard's content lives in its single **Dashboard content** box on the edit page. To add, change, rearrange, or remove anything, edit the text in that box and click **Save Dashboard**. Saving also refreshes the dashboard's stored snapshot so viewers see the change straight away (see Section 7, "How often does dashboard data update?").

## 4.2 What You Can Put in the Content Box

The content box supports:

- **Plain text** — descriptive headings, instructions, narrative summaries.
- **Rich-text formatting** — bold, italic, links, tables, and images through the editor toolbar, to control layout and emphasis.
- **Smart Functions, Smart Tables, and Smart Charts** — dynamic content calculated from project data (see [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md) for full syntax).
- **Piped field values** — standard piping syntax (`[field_name]`) is not meaningful on a dashboard (there is no "current record" context), but smart variables and aggregate functions work fully.

## 4.3 Adding Charts and Statistics

To display a chart or aggregate statistic, type or paste the relevant smart variable syntax into the **Dashboard content** box. You can write syntax manually, or use the wizard (see Section 3.3) to build it and then paste it in. Examples:

- `[aggregate-count:record_id]` — displays the total number of records.
- `[bar-chart:study_arm]` — renders a bar chart of a multiple-choice field.
- `[stats-table:age,weight,bmi:mean,median,min,max]` — displays a statistics table.

Charts and tables render as visual elements when the dashboard is viewed; they appear as raw text in the editor. Always view the dashboard after saving to verify rendering.

See [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md) for the full chart and table syntax reference.

## 4.4 Filtering Dashboard Data

By default, Smart Functions, Smart Tables, and Smart Charts aggregate data from **all records** in the project. You can narrow the data used by appending an optional filter parameter:

- **By report** — limits data to records included in a specific saved report. Use the report's unique name (format `R-…`), found next to each report on the **My Reports & Exports** page.
- **By DAG** — limits data to records belonging to one or more specific Data Access Groups. Use the unique DAG name.
- **By event** (longitudinal projects only) — limits data to a specific event or set of events.

DAG and event filters can be combined, and several DAGs or several events are listed comma-separated within the same parameter. A report filter **cannot** be combined with DAG or event filters in the same smart variable — if you include a report, the DAG and event filters are ignored. To filter by report and DAG together, build the DAG condition into the report's own filter instead. See [RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions](RC-PIPE-12_Smart-Variables-Optional-Parameters-for-Aggregate-Functions.md) for the exact syntax and examples.

> **Note:** Unique report names are not the same as report titles. They are system-assigned identifiers visible on the My Reports & Exports page. Use these, not the display titles, in your filter syntax.

> **Note:** The "current user's DAG" filter (`user-dag-name`) narrows data for a logged-in project user, but on a public dashboard there is no project user, so it filters nothing — the public view shows data from all records. Do not rely on it to restrict what the public sees.

## 4.5 Editing and Removing Content

- **Edit** any part of the dashboard by changing the text in the **Dashboard content** box and clicking **Save Dashboard**.
- **Rearrange** content by cutting and pasting it to a new position within the box.
- **Remove** content by deleting it from the box. Once you save, the removed text is gone; there is no dashboard version history, so copy complex smart variable syntax somewhere safe before deleting it.

---

# 5. Public Dashboards and Access Controls

## 5.1 Making a Dashboard Public

By default a dashboard is private — only users with project access can view it. To make it accessible externally:

1. Save the dashboard first (its public link can only be generated once it has been saved).
2. On the dashboard's edit page, use the **Set as "public"** option and confirm.
3. Optionally set an **Access Code** if you want to restrict viewing to people who have the code.

Once public, the dashboard is accessible via its unique URL to anyone with the link (and the access code, if one is set). There is no REDCap login required unless REDCap login protection is turned on (Section 5.5).

> **Institution-specific:** Your administrators decide whether dashboards can be made public at all: not allowed, allowed for users on their own, or allowed only after an administrator approves the request. Under approval, setting a dashboard public sends a request to the administrators' To-Do List and you receive an email once it is decided. If the public option is missing or says approval is required, check with your REDCap administrators.

The public link is fixed when the dashboard is created, so it does not change when you make the dashboard public, and it stays the same if you turn public access off and on again. Once public, the edit page also offers a **Create Custom Dashboard Link** (a short, memorable URL that redirects to the public dashboard) and **Create QR code**.

> **Important:** As a privacy safeguard, Smart Functions, Smart Tables, and Smart Charts will **not render** on the public version of a dashboard unless they are displaying at least a minimum number of data points. In place of the content, viewers see a message saying there are fewer than N data points. The minimum is a system-wide setting in the Control Center, which can be overridden for an individual project. Its default is **5** on a freshly installed server and **11** on servers that were upgraded through REDCap 11.0.0, so check with your REDCap administrator for the value on your instance. The threshold applies to every view through the public dashboard URL, including viewers who logged in through REDCap login protection (Section 5.5). Project users viewing the dashboard inside the project see all content regardless of data point count.

## 5.2 Access Codes

An access code is an optional layer of security for public dashboards. When set:

- Visitors are prompted to enter the code before the dashboard is displayed.
- You can type your own code (letters, numbers, spaces, and special characters, up to 50 characters) or click **Generate** for a random 12-character code.
- The access code is shown on the dashboard's edit page and can be retrieved via the `[dashboard-access-code:D-XXXXXXXXXX]` smart variable.
- There is no "change code" button. To change the code, remove access code protection and then set a new code. The dashboard's URL stays the same, so existing shared links remain valid — only the code changes.
- After entering the correct code, a visitor stays unlocked for about as long as the server's auto-logout time; after that they must enter it again. Repeated wrong guesses are rate-limited.

Access codes are a convenience control, not a substitute for data governance. Avoid placing individually identifiable record-level data on any dashboard accessible to the public, regardless of whether an access code is set.

> **Note:** Removing a public access code makes the dashboard viewable by anyone with the URL. If you previously shared the URL broadly, be certain that de-identified aggregate content is the only content displayed before removing the code.

## 5.3 Finding the Dashboard URL

The public URL for a dashboard can be found in two ways:

- On the dashboard's edit page, under **Public link** (copy the URL shown there).
- Using the `[dashboard-url:D-XXXXXXXXXX]` smart variable in a field note, alert, or survey confirmation message — see [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md).

## 5.4 Who Can View Internal Dashboards

Each dashboard has its own **User access** settings on its edit page. New dashboards default to all project users; you can instead choose custom access by individual user, user role, or Data Access Group — for example, restricting a sensitive data-quality dashboard to specific roles. A list on the edit page shows exactly which users your selections include. The restriction is enforced when the dashboard is opened, not just hidden from the menu. Users with Design rights and administrators can still open every dashboard from the Project Dashboards page. The public access setting controls external (unauthenticated) access separately from these internal settings.

## 5.5 REDCap Login Protection *(REDCap+, 17.5.0+)*

> **⚠️ REDCap+ Feature Tag**
> REDCap login protection requires REDCap 17.5.0 (Standard) or higher and an active REDCap+ subscription. See [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md).

> **Version caveat (LTS 17.3.x and 16.0.x):** REDCap login protection is not present in the 17.3 or 16.0 LTS lines (checked on 17.3.31 and 16.0.61); it is present in 17.6.5 (Standard). If your server runs LTS, use an access code (Section 5.2) and keep public content aggregate-only, or ask your administrator about moving to a Standard release with REDCap+.

Once a dashboard is public, a button immediately beneath it labelled **Enable REDCap login protection** makes viewers log in to REDCap before the dashboard is displayed. Anyone already logged in sees it straight away. The check is enforced by the server, not just hidden in the page.

Access code and login protection are alternatives: once one is set, the button for the other is disabled. To switch, remove the current one first.

This is real authentication, unlike an access code, but it is not a project user list: the viewer does not need to be a user on the project, only to have an active (not suspended or expired) REDCap account. Under SSO or LDAP, anyone who can authenticate to the instance can view the dashboard, including people with no prior REDCap account. The internal user access settings in Section 5.4 do not apply to the public version. See [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md) §5 for the same feature on surveys.

> **Important:** If the project's REDCap+ subscription lapses, login protection silently switches off. The setting still looks enabled, but the dashboard becomes public again to anyone with the URL. If a dashboard relies on login protection, confirm the subscription is renewed before it expires, and if it does lapse, turn off public access or set an access code until it is restored.

> **Scope note:** Originally written from the 17.5.0 release notes. The behaviour in this section, including that the minimum-data-point threshold (Section 5.1) still applies to logged-in viewers, has since been checked against source code but not yet on a live subscribed instance.

## 5.6 Other Viewing Options

When viewing a dashboard, viewers can use **Export as PDF** to save a copy, and **Enable color-blind accessibility** to switch charts to a color-blind-friendly palette. Clicking a chart opens it full screen.

---

# 6. Sharing Dashboard Links

Dashboard links can be distributed via several mechanisms in REDCap without manually copying and pasting URLs. The `[dashboard-link]` and `[dashboard-url]` smart variables (documented in [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md)) generate live links to a specific dashboard using its unique name.

Common distribution patterns:

- **Survey confirmation message** — include a dashboard link so respondents can see aggregate results immediately after submission.
- **Automated survey invitation or alert** — direct stakeholders to a dashboard when a milestone is reached (e.g., 50% enrollment).
- **Field note or form instruction** — embed a link to a summary dashboard directly on a data entry form.
- **External communications** — copy the public link, custom link, or QR code from the dashboard's edit page and share via email, print, or a study website.

For the full smart variable syntax used in each of these contexts, see [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md).

---

# 7. Common Questions

**Q: What is the difference between a Project Dashboard and the Record Status Dashboard?**

**A:** The Record Status Dashboard (covered in [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md)) is a system-generated table showing the completion status of every record and form. Project Dashboards are custom pages you build — they display aggregate statistics, charts, and text that you configure. They serve different purposes: the Record Status Dashboard is for managing data collection; Project Dashboards are for summarizing and sharing results.

**Q: Do I need to be in Draft Mode to create or edit a dashboard in Production?**

**A:** No. Project Dashboards are not part of the project's structural definition (instruments, fields, events), so they are not subject to the Draft Mode / approval workflow. You can create, edit, and delete dashboards at any time regardless of project status. (Making a dashboard public may still need administrator approval, depending on your server — see Section 5.1.)

**Q: Can I have more than one dashboard per project?**

**A:** Yes. Projects can have multiple dashboards, each with its own title, content, user access, and public access settings. Use multiple dashboards to serve different audiences (e.g., a sponsor-facing dashboard showing enrollment counts, and an internal dashboard showing data quality metrics), and folders to keep a long list organized.

**Q: How often does dashboard data update?**

**A:** REDCap shows a saved snapshot of the dashboard that is kept for up to 10 minutes, so reloading the page within that time shows the same content. Once the snapshot is a minute or more old, a refresh link appears; only users with Design rights can use it to rebuild the dashboard immediately. Saving the dashboard also refreshes it. Public dashboards have no refresh link and update when the snapshot expires. Some views are always built fresh rather than from the snapshot — for example, for users in a Data Access Group when the content uses a report filter or the current user's DAG filter, because the results differ per user.

**Q: Who can see a private dashboard?**

**A:** Each dashboard has its own **User access** settings. New dashboards give access to all project users, but you can restrict visibility per dashboard by user, role, or DAG. Users without access to a given dashboard do not see it in their left-hand menu and cannot open it. Users with Design rights and administrators can open all dashboards from the Project Dashboards page.

**Q: Who can create or edit dashboards?**

**A:** Any user with **Project Design and Setup** rights can create, edit, copy, delete, reorder, and make dashboards public. This is the same right required to modify instruments and fields. Users without Design rights can view dashboards they have access to, but cannot modify them.

**Q: Can I embed images or external content in a dashboard?**

**A:** The content box is a rich-text editor, so images pointing to publicly accessible URLs will render. Iframes and scripts are stripped for security reasons. Keep content to text, REDCap smart variables, and static formatting.

**Q: What happens to smart variables on a dashboard if the referenced field is deleted?**

**A:** If a field referenced in a smart variable (e.g., `[bar-chart:study_arm]`) is deleted from the project, the dashboard shows an error message in place of that chart or statistic. The dashboard itself is not deleted, but you will need to edit the dashboard content to reference a valid field.

**Q: Can I use dashboard links in a survey confirmation page?**

**A:** Yes. Survey confirmation messages support smart variables. Use `[dashboard-link:D-XXXXXXXXXX]` or `[dashboard-url:D-XXXXXXXXXX]` in the survey completion text to direct respondents to a public dashboard after they submit. The dashboard must be set to public for unauthenticated users to access it via that link.

---

# 8. Common Mistakes & Gotchas

**Placing a private dashboard link in an external communication.** If you share a `[dashboard-url]` or `[dashboard-link]` in a survey or email but forget to set the dashboard to public, external recipients see an error saying it is not a valid project dashboard (or, if public dashboards are switched off on the server, that public dashboards are not enabled) instead of the dashboard content. Always verify public access is enabled, and open the link yourself in a private browser window, before distributing dashboard links outside the project team.

**Confusing the Dashboard Unique Name with the Dashboard Title.** The unique name (e.g., `D-557DRCW87L`) is a system-assigned code used in smart variables. The title (e.g., "Enrollment Summary") is the human-readable label. Smart variable syntax requires the unique name — using the title will produce broken links. Copy the unique name from the **Unique dash name** column on the Project Dashboards list page.

**Expecting charts to show record-level data for the current user.** Dashboards have no concept of a "current record" — all aggregate functions and charts compute across the entire dataset (or a filtered subset). If you need to display individual record data, use piping in fields or survey confirmations rather than a dashboard.

**Deleting dashboard content without saving it elsewhere.** Once you remove text from the **Dashboard content** box and save, it is gone — there is no version history. If the content contains complex smart variable syntax, copy it before deleting. Likewise, deleting a whole dashboard is permanent; consider copying it first.

**Combining a report filter with DAG or event filters.** A smart variable that names a report ignores any DAG or event filter alongside it, so the numbers may include more records than you expect. Put the DAG or event condition into the report's own filter instead (Section 4.4).

**Sharing a dashboard access code without the URL.** An access code alone does not allow users to reach the dashboard — they also need the URL. Always share both together, for example by piping `[dashboard-link]` and `[dashboard-access-code]` into the same message (the link does not include the code). See [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md) for pairing the link and access code in a single communication.

**Smart Functions and charts not showing on a public dashboard.** Public dashboards enforce a minimum number of data points before rendering any Smart Function, Smart Table, or Smart Chart. The minimum is set by your administrator (default 5 on new servers, 11 on servers upgraded through 11.0.0) and can be overridden per project. If a chart or statistic looks correct when viewed inside the project but shows a "fewer than N data points" message on the public URL, the underlying data is below that minimum. This applies to logged-in viewers on the public URL too. This is an intentional privacy safeguard — not a bug. Either wait until sufficient data exists, or reconsider whether the metric is appropriate for public display at this stage of the project.

**Using aggregate functions outside of a dashboard.** Aggregate functions (e.g., `[aggregate-mean:age]`) are not limited to dashboards: they also work in field labels, survey text, calculations, and branching logic. In calculations and branching, though, the value is only recalculated when the record is saved, so a stored result goes stale as other records change — use them there only where a point-in-time value is acceptable. The minimum-data-point threshold also applies to Smart Functions, Tables, and Charts on survey pages, so a chart on a survey may show the "fewer than N data points" message early in data collection.

---

# 9. Related Articles

- [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md) (syntax for counts, means, bar charts, pie charts, stats tables)
- [RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions](RC-PIPE-12_Smart-Variables-Optional-Parameters-for-Aggregate-Functions.md) (filtering by DAG, event, or report)
- [RC-PIPE-14 — Smart Variables: Project Dashboards](RC-PIPE-14_Smart-Variables-Project-Dashboards.md) (smart variables for sharing dashboard URLs and links)
- [RC-NAV-REC-04 — Record Status Dashboard & Other Record Links](RC-NAV-REC-04_Record-Status-Dashboard-and-Links.md) (the system-generated record completion view — distinct from Project Dashboards)
- [RC-PIPE-04 — Piping: Emails, Notifications & Logic Features](RC-PIPE-04_Piping-in-Emails-and-Notifications.md) (using dashboard links in alerts and survey invitations)
- [RC-SURV-10 — Survey Login](RC-SURV-10_Survey-Login.md) (REDCap login protection, which also applies to public dashboards)

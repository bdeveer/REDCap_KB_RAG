RC-PROJ-03

**Project Dashboards**

| **Article ID** | RC-PROJ-03 |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects |
| **Prerequisite** | None |
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables; RC-PIPE-14 — Smart Variables: Project Dashboards; RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions |

---

# 1. Overview

Project Dashboards are customizable summary pages within a REDCap project that display aggregate statistics, charts, tables, and free text about your project's data. Any user with **Project Design** privileges can create and edit them. A built-in wizard helps you construct Smart Function, Smart Table, and Smart Chart syntax without writing it by hand, and a list of examples is included on the dashboard creation page. Dashboards can be made publicly accessible — allowing stakeholders, sponsors, or participants to view project-level summaries without needing a REDCap account.

This article covers creating and configuring dashboards, adding content blocks, making a dashboard public, and controlling access. For the smart variable syntax used to build the content that appears on dashboards (aggregate functions, charts, tables), see RC-PIPE-11. For embedding dashboard links in emails, surveys, and alerts, see RC-PIPE-14.

---

# 2. Key Concepts & Definitions

**Project Dashboard**

A configurable page within a REDCap project that displays summary information about project data. Each project can have multiple dashboards, each covering a different view or audience. Dashboards are distinct from the Record Status Dashboard (a system-generated table of record completion status), covered in RC-NAV-REC-04.

**Dashboard Widget**

A single content block on a dashboard. A widget can contain free text, piped smart variables, aggregate functions, charts, or tables. Multiple widgets are stacked vertically to build a full dashboard layout.

**Smart Function**

A smart variable that calculates an aggregate statistic (count, sum, mean, median, min, max, standard deviation, or unique count) across project records and displays the result as a number. Example: `[aggregate-count:record_id]`.

**Smart Table**

A smart variable that renders a table of descriptive statistics for one or more fields. Example: `[stats-table:age,weight,bmi]`.

**Smart Chart**

A smart variable that renders a chart (bar, pie, donut, scatter, or line) from project data. Example: `[bar-chart:study_arm]`.

The full syntax reference for all three types is in RC-PIPE-11.

**Public Dashboard**

A dashboard that has been made accessible via a direct URL to users who do not have a REDCap account. Public dashboards can optionally require an access code.

**Dashboard Unique Name**

A system-generated identifier in the format `D-XXXXXXXXXX` assigned to each dashboard. Used in smart variable syntax (see RC-PIPE-14) and found in the dashboard configuration page.

**Dashboard Access Code**

An optional alphanumeric token required to view a public dashboard. If configured, users must enter the code to proceed past the landing page.

---

# 3. Creating and Configuring a Dashboard

## 3.1 Accessing the Dashboard Builder

Project Dashboards are managed from the **Other Functionality** tab in the left-hand project menu. Click **Project Dashboards** to open the dashboard management page. Any user with **Project Design** privileges can access this page, create new dashboards, and edit existing ones. No Draft Mode approval is required to create or edit dashboards, even in Production.

## 3.2 Creating a New Dashboard

1. On the Project Dashboards management page, click **Add new dashboard**.
2. Enter a **Dashboard Title** — this is the human-readable name shown in the interface and used as default link text in smart variables.
3. Optionally add a **Description** (internal use only; not displayed on the public dashboard page).
4. Click **Save** to create the dashboard. The dashboard opens in edit mode, ready for content to be added.

Note the **Dashboard Unique Name** (format `D-XXXXXXXXXX`) displayed on the configuration page — you will need this if you plan to reference the dashboard in piping or smart variables (see RC-PIPE-14).

## 3.3 The Smart Variable Wizard

The dashboard editor includes a **wizard** to help you construct Smart Function, Smart Table, and Smart Chart syntax without writing it manually. Launch the wizard from within the widget editor to select your statistic type, choose fields, and configure optional filters step by step. The wizard generates the complete syntax which you can insert directly into the widget. A list of working examples is also provided on the creation page as a reference.

## 3.4 Dashboard Settings

From the dashboard settings panel you can:

- **Rename** the dashboard title.
- **Configure user access privileges** — each dashboard has its own access settings controlling which project users can view it (see Section 5.4).
- **Enable/disable public access** (see Section 5).
- **Set or change the access code** for public dashboards.
- **Delete** a dashboard. Deletion is permanent; there is no undo.
- **Reorder dashboards** using the drag handles on the management page.

---

# 4. Adding Content to a Dashboard

## 4.1 The Dashboard Editor

Each dashboard has an editor where you build content using widgets. Widgets are added in sequence from top to bottom. To add a widget, click **Add new widget** (or equivalent button) in the editor. You are then prompted to choose the widget type or simply enter content directly in the text box.

## 4.2 Widget Content

Each widget is a free-form text box that supports:

- **Plain text** — descriptive headings, instructions, narrative summaries.
- **HTML** — basic formatting (bold, italic, links, tables) to control layout and emphasis.
- **Smart variables / aggregate functions / charts / tables** — dynamic content that updates automatically when the dashboard is loaded (see RC-PIPE-11 for full syntax).
- **Piped field values** — standard piping syntax (`[field_name]`) is not meaningful on a dashboard (there is no "current record" context), but smart variables and aggregate functions work fully.

## 4.3 Adding Charts and Statistics

To display a chart or aggregate statistic, type or paste the relevant smart variable syntax directly into the widget text box. You can write syntax manually, or use the wizard (see Section 3.3) to generate it. Examples:

- `[aggregate-count:record_id]` — displays the total number of records.
- `[bar-chart:study_arm]` — renders a bar chart of a multiple-choice field.
- `[stats-table:age,weight,bmi:mean,median,min,max]` — displays a statistics table.

Charts and tables render as visual elements when the dashboard is viewed; they appear as raw text in the editor. Always preview the dashboard after editing to verify rendering.

See RC-PIPE-11 for the full chart and table syntax reference.

## 4.4 Filtering Dashboard Data

By default, Smart Functions, Smart Tables, and Smart Charts aggregate data from **all records** in the project. You can narrow the data used by appending one or more optional filter parameters:

- **By report** — limits data to records included in a specific saved report. Use the report's unique name, found next to each report on the **My Reports & Exports** page.
- **By DAG** — limits data to records belonging to one or more specific Data Access Groups. Use the unique DAG name.
- **By event** (longitudinal projects only) — limits data to a specific event or set of events.

Multiple filter types can be combined. Filters are appended as additional colon-separated parameters in the smart variable syntax. See RC-PIPE-12 for the exact syntax and examples.

> **Note:** Unique report names are not the same as report titles. They are system-assigned identifiers visible on the My Reports & Exports page. Use these, not the display titles, in your filter syntax.

## 4.5 Editing and Reordering Widgets

- **Edit** a widget by clicking the edit icon (pencil) next to it.
- **Delete** a widget by clicking the delete icon. Widget deletion is immediate and cannot be undone — copy the content elsewhere if needed.
- **Reorder** widgets by dragging them up or down in the editor.

---

# 5. Public Dashboards and Access Controls

## 5.1 Making a Dashboard Public

By default a dashboard is private — only users with project access can view it. To make it accessible externally:

1. Open the dashboard settings.
2. Toggle **Make this dashboard public** (or equivalent setting).
3. Optionally set an **Access Code** if you want to restrict viewing to people who have the code.
4. Save settings.

Once public, the dashboard is accessible via its unique URL to anyone with the link (and the access code, if one is set). There is no REDCap login required.

> **Important:** As a privacy safeguard, Smart Functions, Smart Tables, and Smart Charts will **not render** on the public version of a dashboard unless they are displaying at least **8 data points**. Widgets that fall below this threshold appear blank to external viewers, even if they render correctly when viewed inside the project. This threshold applies only to public (unauthenticated) views — internal project users see all content regardless of data point count.

## 5.2 Access Codes

An access code is an optional layer of security for public dashboards. When set:

- Visitors are prompted to enter the code before the dashboard is displayed.
- The access code is shown in the dashboard settings and can be retrieved programmatically via the `[dashboard-access-code:D-XXXXXXXXXX]` smart variable.
- The code can be changed at any time in dashboard settings; existing shared links remain valid (only the code changes).

Access codes are a convenience control, not a substitute for data governance. Avoid placing individually identifiable record-level data on any dashboard accessible to the public, regardless of whether an access code is set.

> **Note:** Removing a public access code makes the dashboard viewable by anyone with the URL. If you previously shared the URL broadly, be certain that de-identified aggregate content is the only content displayed before removing the code.

## 5.3 Finding the Dashboard URL

The public URL for a dashboard can be found in two ways:

- In the dashboard configuration page (copy the URL shown there).
- Using the `[dashboard-url:D-XXXXXXXXXX]` smart variable in a field note, alert, or survey confirmation message — see RC-PIPE-14.

## 5.4 Who Can View Internal Dashboards

Each dashboard has its own user access privilege settings, configurable in the dashboard settings panel. This allows you to control which project users can view a given dashboard — for example, restricting a sensitive data-quality dashboard to specific roles. The public access toggle controls external (unauthenticated) access separately from these internal privilege settings.

---

# 6. Sharing Dashboard Links

Dashboard links can be distributed via several mechanisms in REDCap without manually copying and pasting URLs. The `[dashboard-link]` and `[dashboard-url]` smart variables (documented in RC-PIPE-14) generate live links to a specific dashboard using its unique name.

Common distribution patterns:

- **Survey confirmation message** — include a dashboard link so respondents can see aggregate results immediately after submission.
- **Automated survey invitation or alert** — direct stakeholders to a dashboard when a milestone is reached (e.g., 50% enrollment).
- **Field note or form instruction** — embed a link to a summary dashboard directly on a data entry form.
- **External communications** — copy the raw URL from dashboard settings and share via email, QR code, or a study website.

For the full smart variable syntax used in each of these contexts, see RC-PIPE-14.

---

# 7. Common Questions

**Q: What is the difference between a Project Dashboard and the Record Status Dashboard?**

**A:** The Record Status Dashboard (covered in RC-NAV-REC-04) is a system-generated table showing the completion status of every record and form. Project Dashboards are custom pages you build — they display aggregate statistics, charts, and text that you configure. They serve different purposes: the Record Status Dashboard is for managing data collection; Project Dashboards are for summarizing and sharing results.

**Q: Do I need to be in Draft Mode to create or edit a dashboard in Production?**

**A:** No. Project Dashboards are not part of the project's structural definition (instruments, fields, events), so they are not subject to the Draft Mode / approval workflow. You can create, edit, and delete dashboards at any time regardless of project status.

**Q: Can I have more than one dashboard per project?**

**A:** Yes. Projects can have multiple dashboards, each with its own title, content, and public access settings. Use multiple dashboards to serve different audiences (e.g., a sponsor-facing dashboard showing enrollment counts, and an internal dashboard showing data quality metrics).

**Q: How often does dashboard data update?**

**A:** Dashboard content is generated when the page is loaded or refreshed. There is no automatic background refresh — a viewer must reload the page to see the latest data.

**Q: Who can see a private dashboard?**

**A:** Each dashboard has its own user access privilege settings. By default, project users may have access, but you can restrict visibility on a per-dashboard basis through the dashboard settings panel. Users without the required privileges for a given dashboard will not see it in the list.

**Q: Who can create or edit dashboards?**

**A:** Any user with **Project Design** privileges can create, edit, and delete project dashboards. This is the same privilege level required to modify instruments and fields. Users without Project Design privileges can view dashboards they have access to, but cannot modify them.

**Q: Can I embed images or external content in a dashboard widget?**

**A:** Widgets support HTML, so standard HTML image tags (`<img src="...">`) pointing to publicly accessible images will render. Embedding iframes or external scripts is generally not supported and may be stripped for security reasons. Keep content to text, REDCap smart variables, and static HTML elements.

**Q: What happens to smart variables on a dashboard if the referenced field is deleted?**

**A:** If a field referenced in a smart variable (e.g., `[bar-chart:study_arm]`) is deleted from the project, the widget will display blank or an error where the chart or statistic would have appeared. The dashboard itself is not deleted, but you will need to update the widget content to reference a valid field.

**Q: Can I use dashboard links in a survey confirmation page?**

**A:** Yes. Survey confirmation messages support smart variables. Use `[dashboard-link:D-XXXXXXXXXX]` or `[dashboard-url:D-XXXXXXXXXX]` in the survey completion text to direct respondents to a public dashboard after they submit. The dashboard must be set to public for unauthenticated users to access it via that link.

---

# 8. Common Mistakes & Gotchas

**Placing a private dashboard link in an external communication.** If you share a `[dashboard-url]` or `[dashboard-link]` in a survey or email but forget to set the dashboard to public, external recipients will be redirected to a REDCap login page rather than seeing the dashboard content. Always verify public access is enabled before distributing dashboard links outside the project team.

**Confusing the Dashboard Unique Name with the Dashboard Title.** The unique name (e.g., `D-557DRCW87L`) is a system-assigned code used in smart variables. The title (e.g., "Enrollment Summary") is the human-readable label. Smart variable syntax requires the unique name — using the title will produce broken links. Copy the unique name directly from the dashboard settings page.

**Expecting charts to show record-level data for the current user.** Dashboards have no concept of a "current record" — all aggregate functions and charts compute across the entire dataset (or a filtered subset). If you need to display individual record data, use piping in fields or survey confirmations rather than a dashboard.

**Deleting a widget without saving the content elsewhere.** Widget deletion is immediate and irreversible. If a widget contains complex smart variable syntax, copy it before deleting. The dashboard editor does not have an undo function.

**Sharing a dashboard access code without the URL.** An access code alone does not allow users to reach the dashboard — they also need the URL. Always share both together, or use the `[dashboard-link]` smart variable, which bundles the URL and accepts an optional code prompt. See RC-PIPE-14 for pairing the link and access code in a single communication.

**Smart Functions and charts appearing blank on a public dashboard.** Public dashboards enforce a minimum threshold of 8 data points before rendering any Smart Function, Smart Table, or Smart Chart. If a widget looks correct when viewed inside the project but shows blank externally, the underlying data likely has fewer than 8 data points. This is an intentional privacy safeguard — not a bug. Either wait until sufficient data exists, or reconsider whether the metric is appropriate for public display at this stage of the project.

**Using dashboard aggregate functions outside of a dashboard context.** Aggregate functions (e.g., `[aggregate-mean:age]`) are designed for use on Project Dashboards. While technically usable in field labels, their performance and rendering in that context is not guaranteed. Use them on dashboards where they are fully supported.

---

# 9. Related Articles

- RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables (syntax for counts, means, bar charts, pie charts, stats tables)
- RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions (filtering by DAG, event, or report)
- RC-PIPE-14 — Smart Variables: Project Dashboards (smart variables for sharing dashboard URLs and links)
- RC-NAV-REC-04 — Record Status Dashboard & Other Record Links (the system-generated record completion view — distinct from Project Dashboards)
- RC-PIPE-04 — Piping in Emails and Notifications (using dashboard links in alerts and survey invitations)

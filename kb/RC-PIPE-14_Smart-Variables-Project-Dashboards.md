RC-PIPE-14

**Smart Variables: Project Dashboards**

| **Article ID** | RC-PIPE-14 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with public Project Dashboards configured |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables |

---

# 1. Overview

Project Dashboard smart variables provide access to public project dashboards within REDCap and externally. These variables generate URLs, HTML links, and access codes for dashboards that have been made public by a project administrator. Use these variables to embed dashboard links in field notes, form instructions, emails, and invitations, allowing project stakeholders to easily navigate to summary dashboards without needing to manually construct URLs or remember access codes.

---

# 2. Key Concepts & Definitions

**Project Dashboard**

A customizable administrative view in REDCap that displays summary statistics, charts, tables, and other analytics about project data. Dashboards can be made public so that external users (without a REDCap account) can view them via a unique URL.

**Dashboard Unique Name**

A system-generated identifier for each project dashboard, in the format `D-XXXXXXXXXX` (D followed by alphanumeric characters). Found in the dashboard configuration page. This name is used in piping and is not user-facing.

**Dashboard Title**

The human-readable name of a dashboard, configured by the administrator. This is what users see in the interface.

**Dashboard Access Code**

An optional security token that can be required to access a public dashboard. If an access code is defined, users must provide it to view the dashboard.

**Public Dashboard**

A dashboard that has been configured to be accessible to users outside of REDCap (i.e., without a REDCap account) via a direct URL or shared link.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Dashboard Access Code | `[dashboard-access-code:unique_dash_name]` | The access code for the specified public project dashboard. Only returns a code if one has been defined for the dashboard. Returns blank if no access code is configured. The unique dashboard name (D-XXXXXXXXXX) is found on the dashboard configuration page. | aHmjK5@ctTqT4 |
| Dashboard URL | `[dashboard-url:unique_dash_name]` | The web address (URL) of the specified public project dashboard. Includes the base REDCap URL and all necessary parameters. | https://redcap.school.wakehealth.edu/surveys/?__dashboard=D-557DRCW87L&... |
| Dashboard Link (Default) | `[dashboard-link:unique_dash_name]` | An HTML web link to the specified public project dashboard. Uses the dashboard's configured title as the link text by default. | [Clickable link labeled "My Project Dashboard"] |
| Dashboard Link (Custom Text) | `[dashboard-link:unique_dash_name:Custom Text]` | An HTML web link to the specified public project dashboard with custom link text instead of the dashboard title. | [Clickable link labeled "Click to view our dashboard"] |

---

# 4. Usage Notes

**Finding the Unique Dashboard Name**

To use any dashboard smart variable, you need the unique dashboard name. This is found in the Project Dashboard configuration interface, typically displayed as a code like `D-557DRCW87L`. It is not the same as the dashboard's display title.

**Access Code Availability**

The `[dashboard-access-code:unique_dash_name]` smart variable only returns a code if one has been defined for that dashboard in its settings. If no access code is configured, the variable returns blank. Not all public dashboards require access codes.

**Dashboard URL Format**

Dashboard URLs are long and include multiple parameters. They should be treated as opaque strings — do not attempt to parse or modify them. If you need a custom link, use `[dashboard-link]` instead, which generates proper HTML.

**Link Customization**

Use `[dashboard-link:unique_dash_name:Custom Text]` to generate a link with custom text. For example:
- `[dashboard-link:D-557DRCW87L:View Project Summary]`
- `[dashboard-link:D-557DRCW87L:Check overall progress]`

Without custom text, the link defaults to the dashboard's configured title.

**Access Code Sharing**

If your dashboard has an access code, you can include it alongside the link in communications: "To access the dashboard, click here: `[dashboard-link:D-557DRCW87L]` and use the code `[dashboard-access-code:D-557DRCW87L]`"

**Public Dashboard Context**

These smart variables are most useful for creating external-facing communications. Since public dashboards do not require REDCap authentication, dashboard links can be shared via email, text, QR codes, or websites without requiring recipients to have a REDCap account.

**Email and Invitation Use**

Dashboard smart variables are particularly useful in:
- Survey completion emails: Direct users to a summary dashboard after they complete a survey.
- Project invitations: Include a link to the project dashboard in invitation emails.
- Progress reports: Provide stakeholders with a link to view real-time project metrics.

---

# 5. Common Questions

**Q: How do I find the unique dashboard name to use in a smart variable?**

**A:** In the Project Dashboard configuration interface, the unique dashboard name is displayed as a code in the format D-XXXXXXXXXX. It is typically shown near the dashboard title or in the dashboard settings. Copy this code and use it in your smart variables.

**Q: How do I create a link to a public dashboard in a field note?**

**A:** Use `[dashboard-link:unique_dash_name:Custom Text]` in your field note. For example:
```
View the project summary: [dashboard-link:D-557DRCW87L:Project Dashboard]
```
This generates a clickable link with your custom text.

**Q: My dashboard has an access code. How do I communicate it to users?**

**A:** Include the access code alongside the link in your communication. You can use both smart variables:
```
Access the dashboard here: [dashboard-link:D-557DRCW87L]
Your access code: [dashboard-access-code:D-557DRCW87L]
```

**Q: What is the difference between `[dashboard-url]` and `[dashboard-link]`?**

**A:** `[dashboard-url]` is the raw web address (URL) of the dashboard. `[dashboard-link]` is an HTML link that can be clicked. Use `[dashboard-link]` in emails and forms; use `[dashboard-url]` only if you specifically need the raw address (rarely necessary).

**Q: Can I embed a dashboard link in a survey invitation email?**

**A:** Yes. Survey invitations support piping and smart variables. You can include `[dashboard-link:unique_dash_name]` in the survey invitation email body to direct participants to the dashboard after they complete the survey.

**Q: What happens if the dashboard doesn't have an access code?**

**A:** `[dashboard-access-code:unique_dash_name]` returns blank. All other dashboard smart variables still function normally. You do not need to provide an access code if none is configured.

---

# 6. Common Mistakes & Gotchas

**Using incorrect or incomplete dashboard names.** Dashboard unique names must be in the exact format found on the configuration page (D-XXXXXXXXXX). Typos or incorrect names result in broken links. Always copy the dashboard name directly from the settings rather than typing it manually.

**Confusing dashboard title with dashboard unique name.** The dashboard title (e.g., "Project Summary") is human-readable but is not used in smart variables. You must use the unique dashboard name (e.g., D-557DRCW87L) in all smart variable expressions.

**Assuming public dashboards are accessible without the correct URL.** Public dashboards are only accessible via their specific URL or with the access code. Sharing just the access code without the URL does not allow users to access the dashboard. Always provide the full URL (`[dashboard-url]`) or link (`[dashboard-link]`).

**Not testing dashboard links in the platform they'll be accessed from.** A dashboard link in an email may render differently than in a field note or survey. Test your dashboard smart variables in the actual context (email, form, survey) before deploying to production.

**Attempting to use dashboard smart variables in projects without public dashboards.** If a project does not have any public dashboards configured, these smart variables return blank or errors. Verify that your project has public dashboards set up before relying on these variables.

**Forgetting to configure dashboard access controls.** If you intend the dashboard to be viewable only by certain users, ensure that access controls are configured properly. A public dashboard with no access code is accessible to anyone with the URL.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables (creating charts and functions for dashboards)
- RC-PIPE-04 — Piping in Emails and Notifications (using dashboard links in project emails and alerts)

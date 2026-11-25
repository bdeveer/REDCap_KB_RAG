---
id: RC-PIPE-15
title: 'Smart Variables: Public Reports'
domain: Piping
applies_to:
- Projects with public reports that have access codes defined
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — smart
  variable behaviour and public access checked against source code; pages not re-captured
prerequisites:
- RC-PIPE-03 — Smart Variables Overview
version: '1.0'
last_updated: 2026-11
related:
- id: RC-PIPE-03
  title: Smart Variables Overview
- id: RC-PIPE-12
  title: 'Smart Variables: Optional Parameters for Aggregate Functions'
tags:
- piping
synonyms:
- '[report-access-code] smart variable'
- how to pipe a public report access code with [report-access-code]
- access code for a named public report [report-access-code:unique_report_name]
- share a public report with an access code via email
- public report smart variables for access codes
- how to give someone the code to view a public report
- reference a specific public report access code
- public report access code piping
---

# 1. Overview

Public Report smart variables provide access codes for reports that have been made public. These variables are useful for sharing report access codes with project stakeholders or embedding them in communications. A public report allows external users (without a REDCap account) to view a filtered data export via a secure URL. If an access code has been defined for the report, the smart variable returns that code for sharing.

---

# 2. Key Concepts & Definitions

**Public Report**

A data export report in REDCap that has been configured to be publicly accessible. External users can view the report data without a REDCap account by opening the report's public link (and typing the access code, if one has been set).

**Report Unique Name**

A system-generated identifier for each report in REDCap, in the format `R-XXXXXXXXXX` (R followed by alphanumeric characters). Found on the My Reports & Exports page. This name is used in smart variables such as `[report-access-code:R-XXXXXXXXXX]` and as a report filter in aggregate smart functions.

**Report Access Code**

An optional security token that can be required to access a public report. If defined, users must provide the access code to view the report. Access codes provide an additional layer of security for public reports and are case sensitive.

**Report URL**

The direct web address (URL) to access a public report: the REDCap survey address with a report parameter. An optional custom short URL can also be created. There is no smart variable for the report URL or link — copy the link from the report's public settings.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Report Access Code | `[report-access-code:unique_report_name]` | The access code for the specified report, if one has been set. Returns blank if no access code is configured. An access code can only be set while the report is public, but it stays on the report if the report is later taken off public. The unique report name (R-XXXXXXXXXX) is found on the My Reports & Exports page. | FjB9V5.YQ6A |

---

# 4. Usage Notes

**Finding the Unique Report Name**

To use the report access code smart variable, you need the unique report name. This is found on the My Reports & Exports page, typically displayed as a code like `R-2554F4TCNT` next to each report. It is not the same as the report's display name or title.

**When the Variable Returns a Code**

The `[report-access-code:unique_report_name]` smart variable returns the report's access code whenever one has been set. An access code can only be set while the report is public, but taking a report off public does not remove its code — so the variable can still return it afterwards. If you no longer want the code to be piped, remove it in the report's public settings.

**Who Can Make a Report Public**

Whether users can make reports public is controlled by a system setting on your REDCap server. Depending on that setting, making reports public is not allowed, users may do it themselves, or a REDCap administrator must approve a request. A user making a report public needs the User Rights privilege in the project, and the report cannot contain fields marked as Identifier — including identifiers shown through the secondary unique field or the custom record label. REDCap administrators can make reports public regardless of these restrictions.

> **Version caveat (v17.6 Standard; not in LTS 17.3 or 16):** In v17.6 Standard, on servers with REDCap+, a public report can be protected with REDCap login instead of an access code. The two cannot be combined — a report uses one or the other. Check with your administrator whether this option is available on your server.

**Public Report Behaviour**

- The public link is the REDCap survey address with a report parameter. An optional custom short URL can be created in the report's public settings.
- There is no smart variable for the report URL or link. Copy the link from the report's public settings and paste it into your message.
- A public report cannot be edited while it is public. Take it off public to make changes, then make it public again.
- Access codes are case sensitive. Viewers type the code on an entry page, and it is then remembered for a while.
- Repeated wrong access code attempts are rate-limited, so a viewer who mistypes the code several times may need to wait before trying again.

**Access Code Requirement**

Not all public reports require an access code. If a public report does not have an access code configured, `[report-access-code:unique_report_name]` returns blank, but the report is still accessible via its public URL without a code.

**Report Access Code Use Cases**

Public report access codes are useful for:
- Sharing reports securely with external stakeholders who need data but should not have full REDCap access.
- Including access codes in project communications, emails, or invitations.
- Creating QR codes or custom short URLs for the report link that users can scan or click (send the access code separately).

**Email and Communication Context**

Report access code smart variables are most useful in emails, invitations, and other communications directed at external audiences or stakeholders:
- "View the data: [Paste the report link from the report's public settings] and use code: `[report-access-code:R-2554F4TCNT]`"
- "Here is your secure data export: [Report link] (Access code: `[report-access-code:R-2554F4TCNT]`)"

**Difference from Aggregate Functions**

The `[aggregate-*]` smart variables ([RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md)) can filter results using report names as parameters, but they do not provide access codes. Those are used for creating summary statistics on dashboards. The `[report-access-code]` variable provides the code needed to share access to the actual report export.

---

# 5. Common Questions

**Q: How do I find the unique report name to use in a smart variable?**

**A:** Go to the My Reports & Exports page in your REDCap project. Each report is listed with its unique identifier in the format R-XXXXXXXXXX (for example, R-2554F4TCNT). Copy this code and use it in your smart variable: `[report-access-code:R-2554F4TCNT]`.

**Q: How do I communicate a public report's access code to external users?**

**A:** Use the smart variable in an email or field note: "Access the report here: [Report link copied from the report's public settings] using code: `[report-access-code:R-2554F4TCNT]`". This provides both the link and the access code in a clear format.

**Q: What if my public report doesn't have an access code?**

**A:** `[report-access-code:unique_report_name]` returns blank if no access code is configured. The report is still publicly accessible via its URL, but users do not need a code to view it. You can still share the report URL with external users.

**Q: Can I use report access codes in automated emails?**

**A:** Yes. If your project uses Alerts & Notifications to send automated emails, you can include `[report-access-code:R-XXXXXXXXXX]` in the email body. Recipients will receive the access code along with instructions on how to use it.

**Q: What is the difference between a public report and a public dashboard?**

**A:** A public report is a data export that displays records and fields in a tabular format, filtered by criteria you define. A public dashboard displays summary statistics, charts, and visualizations. Reports are for viewing detailed data; dashboards are for viewing summaries and analytics. Both can have access codes.

**Q: Can I share report access codes via QR codes or shortened URLs?**

**A:** You can create a QR code or a custom short URL that points to the report's public link, but the access code cannot be put in the URL. Viewers always type the code on an entry page (it is then remembered for a while). If you share a QR code or short URL, send the access code separately — for example, in an email using `[report-access-code:R-XXXXXXXXXX]`.

---

# 6. Common Mistakes & Gotchas

**Using the report display name instead of the unique report name.** The report display name (e.g., "Weekly Data Export") is human-readable but cannot be used in smart variables. You must use the unique identifier (R-XXXXXXXXXX) found on the My Reports & Exports page.

**Assuming the smart variable returns a URL.** `[report-access-code]` returns only the access code itself, not the full report URL. There is no smart variable for the report URL or link, so you must provide it separately. Copy the link from the report's public settings.

**Assuming the variable confirms the report is public.** `[report-access-code:unique_report_name]` returns the access code even if the report has since been taken off public, because the code stays on the report. Before sending, verify in the report's public settings that the report is still public, and remove the access code if you no longer want it shared.

**Not checking that an access code is defined.** Even if a report is public, `[report-access-code:unique_report_name]` only returns a value if an access code has been explicitly configured in the report settings. If the report is public but has no access code, the variable returns blank.

**Exposing access codes in insecure communications.** Access codes provide security for public reports. Do not include them in unencrypted emails or publicly shared documents unless necessary. Consider whether the report truly needs to be public and access-code-protected.

**Sharing report codes with users who already have REDCap access.** If external stakeholders who need the report already have REDCap accounts with appropriate permissions, they can access the report directly through the application without needing a public access code.

---

# 7. Related Articles

- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (overview of all smart variable categories)
- [RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables](RC-PIPE-11_Smart-Variables-Aggregate-Functions-Charts-and-Tables.md) (using reports as filter parameters)
- [RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions](RC-PIPE-12_Smart-Variables-Optional-Parameters-for-Aggregate-Functions.md) (report filtering in aggregate functions)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (using access codes in automated emails)

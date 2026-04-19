RC-PIPE-15

**Smart Variables: Public Reports**

| **Article ID** | RC-PIPE-15 |
|---|---|
| **Domain** | Piping |
| **Applies To** | Projects with public reports that have access codes defined |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions |

---

# 1. Overview

Public Report smart variables provide access codes for reports that have been made public by a project administrator. These variables are useful for sharing report access codes with project stakeholders or embedding them in communications. A public report allows external users (without a REDCap account) to view a filtered data export via a secure URL. If an access code has been defined for the report, the smart variable returns that code for sharing.

---

# 2. Key Concepts & Definitions

**Public Report**

A data export report in REDCap that has been configured to be publicly accessible. External users can view the report data without a REDCap account, using either a direct URL or an access code.

**Report Unique Name**

A system-generated identifier for each report in REDCap, in the format `R-XXXXXXXXXX` (R followed by alphanumeric characters). Found on the My Reports & Exports page. This name is used in piping, filtering functions, and when defining access codes.

**Report Access Code**

An optional security token that can be required to access a public report. If defined, users must provide the access code to view the report. Access codes provide an additional layer of security for public reports.

**Report URL**

The direct web address (URL) to access a public report. The URL is unique to each report and includes the necessary parameters for identifying and accessing the report.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Report Access Code | `[report-access-code:unique_report_name]` | The access code for the specified public report, assuming the report has been made public AND an access code has been defined for it. Returns blank if the report is not public or if no access code is configured. The unique report name (R-XXXXXXXXXX) is found on the My Reports & Exports page. | FjB9V5.YQ6A |

---

# 4. Usage Notes

**Finding the Unique Report Name**

To use the report access code smart variable, you need the unique report name. This is found on the My Reports & Exports page, typically displayed as a code like `R-2554F4TCNT` next to each report. It is not the same as the report's display name or title.

**Report Must Be Public**

The `[report-access-code:unique_report_name]` smart variable only returns a code if:
1. The report has been made public by the administrator.
2. An access code has been defined for the report in its settings.

If either condition is not met, the variable returns blank.

**Access Code Requirement**

Not all public reports require an access code. If a public report does not have an access code configured, `[report-access-code:unique_report_name]` returns blank, but the report is still accessible via its public URL without a code.

**Report Access Code Use Cases**

Public report access codes are useful for:
- Sharing reports securely with external stakeholders who need data but should not have full REDCap access.
- Including access codes in project communications, emails, or invitations.
- Creating QR codes or shortened URLs that users can scan or click to access reports.

**Email and Communication Context**

Report access code smart variables are most useful in emails, invitations, and other communications directed at external audiences or stakeholders:
- "View the data: [Include the report URL from the My Reports & Exports page] and use code: `[report-access-code:R-2554F4TCNT]`"
- "Here is your secure data export: [Report link] (Access code: `[report-access-code:R-2554F4TCNT]`)"

**Difference from Aggregate Functions**

The `[aggregate-*]` smart variables (RC-PIPE-11) can filter results using report names as parameters, but they do not provide access codes. Those are used for creating summary statistics on dashboards. The `[report-access-code]` variable provides the code needed to share access to the actual report export.

---

# 5. Common Questions

**Q: How do I find the unique report name to use in a smart variable?**

**A:** Go to the My Reports & Exports page in your REDCap project. Each report is listed with its unique identifier in the format R-XXXXXXXXXX (for example, R-2554F4TCNT). Copy this code and use it in your smart variable: `[report-access-code:R-2554F4TCNT]`.

**Q: How do I communicate a public report's access code to external users?**

**A:** Use the smart variable in an email or field note: "Access the report here: [Report URL from My Reports page] using code: `[report-access-code:R-2554F4TCNT]`". This provides both the link and the access code in a clear format.

**Q: What if my public report doesn't have an access code?**

**A:** `[report-access-code:unique_report_name]` returns blank if no access code is configured. The report is still publicly accessible via its URL, but users do not need a code to view it. You can still share the report URL with external users.

**Q: Can I use report access codes in automated emails?**

**A:** Yes. If your project uses Alerts & Notifications to send automated emails, you can include `[report-access-code:R-XXXXXXXXXX]` in the email body. Recipients will receive the access code along with instructions on how to use it.

**Q: What is the difference between a public report and a public dashboard?**

**A:** A public report is a data export that displays records and fields in a tabular format, filtered by criteria you define. A public dashboard displays summary statistics, charts, and visualizations. Reports are for viewing detailed data; dashboards are for viewing summaries and analytics. Both can have access codes.

**Q: Can I share report access codes via QR codes or shortened URLs?**

**A:** You can create a QR code that links to a report URL with the access code embedded as a URL parameter. However, embedding the access code in a URL makes it visible in browser history and referrer logs. For sensitive data, consider using other sharing methods (email, direct messaging) that do not expose the code.

---

# 6. Common Mistakes & Gotchas

**Using the report display name instead of the unique report name.** The report display name (e.g., "Weekly Data Export") is human-readable but cannot be used in smart variables. You must use the unique identifier (R-XXXXXXXXXX) found on the My Reports & Exports page.

**Assuming the smart variable returns a URL.** `[report-access-code]` returns only the access code itself, not the full report URL. You must provide the report URL separately. To get the report URL, navigate to My Reports & Exports and copy the public report link.

**Not verifying that the report is actually public.** If a report is not configured as public, `[report-access-code:unique_report_name]` returns blank. Verify in the report settings that "Make this report public" is enabled.

**Not checking that an access code is defined.** Even if a report is public, `[report-access-code:unique_report_name]` only returns a value if an access code has been explicitly configured in the report settings. If the report is public but has no access code, the variable returns blank.

**Exposing access codes in insecure communications.** Access codes provide security for public reports. Do not include them in unencrypted emails or publicly shared documents unless necessary. Consider whether the report truly needs to be public and access-code-protected.

**Sharing report codes with users who already have REDCap access.** If external stakeholders who need the report already have REDCap accounts with appropriate permissions, they can access the report directly through the application without needing a public access code.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-11 — Smart Variables: Aggregate Functions, Charts, and Tables (using reports as filter parameters)
- RC-PIPE-12 — Smart Variables: Optional Parameters for Aggregate Functions (report filtering in aggregate functions)
- RC-ALERT-01 — Alerts and Notifications Setup (using access codes in automated emails)

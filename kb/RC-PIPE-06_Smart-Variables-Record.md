RC-PIPE-06

**Smart Variables: Record**

| **Article ID** | RC-PIPE-06 |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types |
| **Prerequisite** | RC-PIPE-03 — Smart Variables Overview |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-PIPE-03 — Smart Variables Overview; RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers |

---

# 1. Overview

Record smart variables return metadata about the record (data entry row) currently being viewed or edited. They do not return participant-entered field values but rather REDCap's internal record properties — such as the record's unique identifier, its assigned Data Access Group, and URLs for calendar feeds. Use these variables to reference record-level information in field labels, form notes, emails, and logic expressions.

---

# 2. Key Concepts & Definitions

**Record Name / Record ID**

The primary unique identifier for a record in REDCap. The record name is configured during project setup and is typically a participant ID, study code, or similar. It is user-visible and searchable.

**Record Metadata**

Information about a record managed by REDCap itself, as opposed to data entered by the participant or coordinator. Examples include the record's assigned Data Access Group and calendar information.

**Calendar Feature**

An optional REDCap module that generates iCalendar (ICS) feeds for a record, allowing participants to subscribe to event calendars or download calendar events. Calendar variables require that this feature be enabled for the project.

**Data Access Group (DAG) Assignment**

Records, like users, can be assigned to a Data Access Group to restrict who can access them. A record assigned to a DAG can only be viewed and edited by users assigned to the same DAG.

---

# 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Record Name | `[record-name]` | The unique record name (ID) of the current record. | 108 |
| Record DAG Name | `[record-dag-name]` | The unique identifier of the Data Access Group to which the current record belongs. Returns blank if the record is not assigned to any DAG. | site_b |
| Record DAG ID | `[record-dag-id]` | The numeric ID of the DAG to which the current record belongs. Returns blank if not assigned to a DAG. | 96 |
| Record DAG Label | `[record-dag-label]` | The human-readable name/label of the DAG to which the current record belongs. Returns blank if not assigned to a DAG. | Site B |
| Calendar URL | `[calendar-url]` | The web address (URL) of the calendar feed or downloadable ICS calendar file for the current record. Returns blank if the Calendar feature is not enabled. | https://redcap.yourinstitution.edu/surveys/?__calendar=... |
| Calendar Link | `[calendar-link]` or `[calendar-link:Custom Text]` | An HTML web link to the calendar feed or ICS file for the current record. Optionally specify custom link text; if omitted, defaults to displaying the URL as the link text. Returns blank if the Calendar feature is not enabled. | Download your calendar events (ICS file) or Click here for calendar |

---

# 4. Usage Notes

**Calendar Variables Require Feature Enablement**

Calendar smart variables (`[calendar-url]` and `[calendar-link]`) only function if the Calendar module is enabled for the project. If the feature is not enabled, these variables return blank. Check with your REDCap administrator to confirm the Calendar module is active if you plan to use calendar smart variables.

**Record DAG Behavior**

If a record is not assigned to any DAG, `[record-dag-name]`, `[record-dag-id]`, and `[record-dag-label]` all return blank. This is distinct from user DAG variables, which reflect the logged-in user's DAG assignment. A record's DAG assignment is independent of who is viewing it.

**Calendar Link Customization**

When using `[calendar-link:Custom Text]`, replace "Custom Text" with your desired link label. For example: `[calendar-link:View my calendar events]` generates a link labeled "View my calendar events" instead of the default URL text. Omit the second parameter to use the URL as the link text.

**Record Name Context**

`[record-name]` is useful in emails, field notes, and survey invitations to reference the current record's identifier. It always reflects the record being actively viewed or edited at the time the piping is evaluated.

**Use in Survey Invitations and Confirmation Emails**

Record smart variables are especially useful in emails. For example, a survey confirmation email might read: "Thank you for completing the survey for participant `[record-name]` assigned to `[record-dag-label]`."

---

# 5. Common Questions

**Q: How do I display the current record's ID in a field note?**

**A:** Use `[record-name]` in your field note. For example: "This is the entry form for record `[record-name]`. Please complete all required fields below."

**Q: My project uses Data Access Groups. How can I display which DAG a record belongs to?**

**A:** Use one of the record DAG smart variables in a field note or descriptive text:
- `[record-dag-label]` displays the human-readable DAG name (e.g., "Site B").
- `[record-dag-name]` displays the unique DAG identifier (e.g., "site_b").
- `[record-dag-id]` displays the numeric DAG ID.

The label is usually most user-friendly.

**Q: What is the difference between `[user-dag-label]` and `[record-dag-label]`?**

**A:** `[user-dag-label]` identifies the logged-in user's DAG; `[record-dag-label]` identifies the record's assigned DAG. They may be the same (if the user is viewing a record in their DAG) or different (if you are testing with users in different DAGs). Use the variable that matches what you need to display.

**Q: How do I create a link to a record's calendar in a survey invitation email?**

**A:** Use `[calendar-link:Custom Text]` in your email body. For example:
```
[calendar-link:View your study calendar events]
```
The email will contain a clickable link with your custom text. Note that the Calendar feature must be enabled in your project.

**Q: Can I use record smart variables in branching logic?**

**A:** Yes, `[record-name]` and all record DAG smart variables can be used in branching logic. For example, you could show a field only for records in a specific DAG: `[record-dag-name]='site_b'`. However, this is less common than using user smart variables for permission-based logic.

**Q: If a record is not assigned to a DAG, what does `[record-dag-label]` display?**

**A:** It returns blank. If you want to display text indicating that no DAG is assigned, you cannot rely on the smart variable alone. Instead, use a calculated field or a manual note that says something like "This record is not assigned to any Data Access Group."

---

# 6. Common Mistakes & Gotchas

**Confusing record DAG variables with user DAG variables.** `[record-dag-label]` refers to the record's DAG assignment; `[user-dag-label]` refers to the logged-in user's DAG. If a user from one DAG is viewing a record from another DAG (possible with elevated permissions), these two variables will return different values. Use the correct variable for your intent.

**Assuming calendar smart variables work without the Calendar feature enabled.** If your project does not have the Calendar module enabled, `[calendar-url]` and `[calendar-link]` return blank, producing confusing empty output in your emails or forms. Verify that the Calendar feature is active before using these variables, or use the `:hideunderscore` modifier to hide blank placeholders.

**Using calendar smart variables for surveys accessed by participants.** Calendar links work best in administrator-facing emails or forms. If a survey is accessed by an external participant without authentication, calendar smart variables may not function correctly. Test with your actual participants to confirm expected behavior.

**Not accounting for blank record DAG values in conditional logic.** If a record might not be assigned to a DAG, logic like `[record-dag-name]='site_b'` will not display fields for unassigned records. If you need to show content for both assigned and unassigned records, add an OR clause in your logic, or use a separate calculated field.

**Pasting calendar links directly into emails without testing.** Calendar URLs are long and may wrap unexpectedly in email clients. Always preview your email in multiple clients before sending, and test that the calendar link actually functions for participants.

---

# 7. Related Articles

- RC-PIPE-03 — Smart Variables Overview (overview of all smart variable categories)
- RC-PIPE-02 — Piping in Longitudinal, Repeated Instruments & Modifiers (smart variable syntax and modifiers)
- RC-PIPE-05 — Smart Variables: User (user-based smart variables for comparison)
- RC-ALERT-01 — Alerts and Notifications Setup (using record smart variables in alert emails)

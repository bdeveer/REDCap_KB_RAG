

**Smart Variables: Record**

| **Article ID** | [RC-PIPE-06 — Smart Variables: Record](RC-PIPE-06_Smart-Variables-Record.md) |
|---|---|
| **Domain** | Piping |
| **Applies To** | All project types |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — smart variable behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md); [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md)|
| **Synonyms** | [record-name] smart variable; how to pipe the current record id with [record-name]; record smart variables for the record data access group; [record-dag-name] and [record-dag-label] piping; pipe the calendar link with [calendar-link] or [calendar-url]; reference the current record in a field label or email; [record-dag-id] record-level smart variable; how to show the record id automatically |

---

## 1. Overview

Record smart variables return metadata about the record (data entry row) currently being viewed or edited. They do not return participant-entered field values but rather REDCap's internal record properties — such as the record's unique identifier, its assigned Data Access Group, and URLs for calendar feeds. Use these variables to reference record-level information in field labels, form notes, emails, and logic expressions.

---

## 2. Key Concepts & Definitions

**Record Name / Record ID**

The primary unique identifier for a record in REDCap. The record name is configured during project setup and is typically a participant ID, study code, or similar. It is user-visible and searchable.

**Record Metadata**

Information about a record managed by REDCap itself, as opposed to data entered by the participant or coordinator. Examples include the record's assigned Data Access Group and calendar information.

**Calendar Feed**

An iCalendar (ICS) feed generated for a record, allowing participants to subscribe to their scheduled events or download calendar events. Calendar feeds are a server-wide setting that your REDCap administrator enables for the whole installation; they are not switched on per project.

**Data Access Group (DAG) Assignment**

Records, like users, can be assigned to a Data Access Group to restrict who can access them. A record assigned to a DAG can only be viewed and edited by users assigned to the same DAG.

---

## 3. Smart Variable Reference

| Smart Variable | Syntax | Description | Example Output |
|---|---|---|---|
| Record Name | `[record-name]` | The unique record name (ID) of the current record. | 108 |
| Record DAG Name | `[record-dag-name]` | The unique identifier of the Data Access Group to which the current record belongs. Returns blank if the record is not assigned to any DAG. | site_b |
| Record DAG ID | `[record-dag-id]` | The numeric ID of the DAG to which the current record belongs. Returns blank if not assigned to a DAG. | 96 |
| Record DAG Label | `[record-dag-label]` | The human-readable name/label of the DAG to which the current record belongs. Returns blank if not assigned to a DAG. | Site B |
| Calendar URL | `[calendar-url]` | The web address (URL) of the calendar feed or downloadable ICS calendar file for the current record. Returns blank if the Calendar feature is not enabled. | https://redcap.yourinstitution.edu/surveys/?__calendar=... |
| Calendar Link | `[calendar-link]` or `[calendar-link:Custom Text]` | An HTML web link to the calendar feed or ICS file for the current record. Optionally specify custom link text; if omitted, defaults to displaying the URL as the link text. Returns blank if the Calendar feature is not enabled. | Download your calendar events (ICS file) or Click here for calendar |

---

## 4. Usage Notes

**Calendar Variables Require the Calendar Feed Setting**

Calendar smart variables (`[calendar-url]` and `[calendar-link]`) depend on the server-wide calendar feed setting, which your REDCap administrator controls; there is no project-level switch. If calendar feeds are not enabled on your server, these variables return blank. Check with your REDCap administrator to confirm calendar feeds are enabled if you plan to use calendar smart variables.

**Calendar Links Are Meant for Participants**

The calendar link is a feed URL that opens without logging in to REDCap. It is intended for participants — for example, so they can subscribe to their appointments in their own calendar app. Because anyone who has the URL can open that record's feed, share it only with the intended participant (for example, in an email sent to that participant).

**Record DAG Behavior**

If a record is not assigned to any DAG, `[record-dag-name]`, `[record-dag-id]`, and `[record-dag-label]` all return blank. This is distinct from user DAG variables, which reflect the logged-in user's DAG assignment. A record's DAG assignment is independent of who is viewing it.

**Calendar Link Customization**

When using `[calendar-link:Custom Text]`, replace "Custom Text" with your desired link label. For example: `[calendar-link:View my calendar events]` generates a link labeled "View my calendar events" instead of the default URL text. Omit the second parameter to use the URL as the link text.

**Record Name Context**

`[record-name]` is useful in emails, field notes, and survey invitations to reference the current record's identifier. It always reflects the record being actively viewed or edited at the time the piping is evaluated.

**Records That Do Not Exist Yet**

- **Public survey, before the record is created** — `[record-name]`, the record DAG variables, and the calendar variables are blank, because there is no record yet.
- **Brand-new record on a data entry form** — `[record-name]` shows the proposed record ID. The record DAG variables may stay blank until the record is saved for the first time.

**Use in Survey Invitations and Confirmation Emails**

Record smart variables are especially useful in emails. For example, a survey confirmation email might read: "Thank you for completing the survey for participant `[record-name]` assigned to `[record-dag-label]`."

---

## 5. Common Questions

**Q: How do I display the current record's ID in a field note?**

**A:** Use `[record-name]` in your field note. For example: "This is the entry form for record `[record-name]`. Please complete all required fields below."

**Q: My project uses Data Access Groups. How can I display which DAG a record belongs to?**

**A:** Use one of the record DAG smart variables in a field note or descriptive text:
- `[record-dag-label]` displays the human-readable DAG name (e.g., "Site B").
- `[record-dag-name]` displays the unique DAG identifier (e.g., "site_b").
- `[record-dag-id]` displays the numeric DAG ID.

The label is usually most user-friendly.

**Q: What is the difference between `[user-dag-label]` and `[record-dag-label]`?**

**A:** `[user-dag-label]` identifies the logged-in user's DAG; `[record-dag-label]` identifies the record's assigned DAG. Users in a DAG only see records in their own DAG, so for them the two match. They differ mainly when the user is not in any DAG (or is an administrator who is not a project user): the user DAG is blank while the record DAG is set. Use the variable that matches what you need to display.

**Q: How do I create a link to a record's calendar in a survey invitation email?**

**A:** Use `[calendar-link:Custom Text]` in your email body. For example:
```
[calendar-link:View your study calendar events]
```
The email will contain a clickable link with your custom text. Note that calendar feeds must be enabled on your REDCap server by your administrator. Send the link only to the participant whose calendar it is.

**Q: Can I use record smart variables in branching logic?**

**A:** Yes, `[record-name]` and all record DAG smart variables can be used in branching logic. For example, you could show a field only for records in a specific DAG: `[record-dag-name]='site_b'`. However, this is less common than using user smart variables for permission-based logic.

**Q: If a record is not assigned to a DAG, what does `[record-dag-label]` display?**

**A:** It returns blank. If you want to display text indicating that no DAG is assigned, you cannot rely on the smart variable alone. Instead, use a calculated field or a manual note that says something like "This record is not assigned to any Data Access Group."

---

## 6. Common Mistakes & Gotchas

**Confusing record DAG variables with user DAG variables.** `[record-dag-label]` refers to the record's DAG assignment; `[user-dag-label]` refers to the logged-in user's DAG. Users in a DAG only see records in their own DAG, so in practice the two differ mainly when the user is not in any DAG — or is an administrator who is not a project user — and is viewing a record that is in a DAG: the user DAG is blank while the record DAG is set. Use the correct variable for your intent.

**Assuming calendar smart variables work without calendar feeds enabled.** If calendar feeds are not enabled on your REDCap server, `[calendar-url]` and `[calendar-link]` return blank, producing confusing empty output in your emails or forms. Ask your REDCap administrator whether calendar feeds are enabled before using these variables, or use the `:hideunderscore` modifier to hide blank placeholders.

**Sharing calendar links too widely.** The calendar link works without logging in, which is what makes it useful for participants — but it also means anyone with the URL can open that record's feed. Send it only to the intended participant, and do not paste it into shared documents or messages to groups.

**Not accounting for blank record DAG values in conditional logic.** If a record might not be assigned to a DAG, logic like `[record-dag-name]='site_b'` will not display fields for unassigned records. If you need to show content for both assigned and unassigned records, add an OR clause in your logic, or use a separate calculated field.

**Pasting calendar links directly into emails without testing.** Calendar URLs are long and may wrap unexpectedly in email clients. Always preview your email in multiple clients before sending, and test that the calendar link actually functions for participants.

---

## 7. Related Articles

- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (overview of all smart variable categories)
- [RC-PIPE-02 — Piping: Longitudinal, Repeated Instruments & Modifiers](RC-PIPE-02_Piping-Longitudinal-Repeated-Instruments-and-Modifiers.md) (smart variable syntax and modifiers)
- [RC-PIPE-05 — Smart Variables: User](RC-PIPE-05_Smart-Variables-User.md) (user-based smart variables for comparison)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (using record smart variables in alert emails)

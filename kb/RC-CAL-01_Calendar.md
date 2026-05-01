RC-CAL-01

**Calendar**

| **Article ID** | RC-CAL-01 |
| --- | --- |
| **Domain** | Calendar |
| **Applies To** | All project types; primarily used in longitudinal projects |
| **Prerequisite** | RC-NAV-UI-02 — Project Menu Reference |
| **Version** | 1.8 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-LONG-01 — Longitudinal Project Setup; RC-ALERT-01 — Alerts & Notifications: Setup; RC-SURV-06 — Automated Survey Invitations; RC-NAV-UI-02 — Project Menu Reference |

---

# 1. Overview

This article covers the REDCap Calendar module and the closely related Scheduling module. The Calendar is a built-in project tool for recording and viewing scheduled participant appointments, study visits, and other project-related events on a date-based calendar. It is available in all project types and appears in the Applications menu by default. The Scheduling module is an optional add-on for longitudinal projects that automates visit date calculation: given a start date and the Days Offset configured for each event, it generates a projected schedule for a participant and pushes those dates into the Calendar. Together, these two features give study teams a way to plan, track, and adjust participant visit schedules within REDCap. Neither feature sends reminders, triggers surveys, or connects to hospital scheduling systems such as Epic.

---

# 2. Key Concepts & Definitions

## Calendar Entry
A record in the Calendar representing a single scheduled event. Each entry has a date, an optional time, a note or description, and optional links to a specific record ID, event (in longitudinal projects), or user. Calendar entries are not instruments or data fields — they store no collected data and do not appear in exports.

## Calendar Module
The project-level feature that provides the Calendar interface. The Calendar is enabled by default for all projects and appears in the **Applications** section of the left-side project menu. It cannot be disabled globally, but access can be removed per user through User Rights. Also referred to as the "Calendar" in the REDCap interface.

## Scheduling Module
A separate, optional REDCap feature for longitudinal projects that calculates and assigns target visit dates (and acceptable offset windows) to each event for each participant, based on a reference date (such as enrollment). When active, the Scheduling module can automatically populate Calendar entries for each scheduled visit. The Scheduling module and the Calendar module are distinct features; the Calendar can be used without Scheduling, and Scheduling data is only reflected in the Calendar when both are enabled.

## Visit Window
In the Scheduling module context, the range of dates (defined by `offset_min` and `offset_max` around a target date) within which a participant's visit is considered on-schedule. Visit windows are configured per-event and displayed in the Calendar when Scheduling is active. See RC-LONG-01 — Longitudinal Project Setup for Scheduling module configuration details.

## Ad Hoc Event
A Calendar entry that is tied to a specific record but not to a defined project event. Ad Hoc events are added from the View or Edit Schedule tab after selecting a record, so they are always record-linked. They are excluded from the bulk date-shift calculation when a scheduled event date is changed. Common uses include tracking contact attempts (e.g., called participant — no answer), logging reminders for study staff to follow up, or recording unplanned interactions that don't correspond to a formal protocol visit.

## Schedule Entry Status
Each scheduled Calendar entry has a status field that tracks the visit state. Status options are: **Due Date**, **Scheduled**, **Confirmed**, **Cancelled**, and **No Show**. Status is set and updated on the View or Edit Schedule tab or in the event detail view.

---

# 3. Calendar Access and User Rights

## 3.1 Calendar availability

The Calendar is available in all REDCap projects by default. It appears in the **Applications** section of the left-side project menu without any setup required. There is no project-level toggle to enable or disable it.

## 3.2 Controlling Calendar access per user

The Calendar cannot be disabled project-wide, but access can be removed for individual users through User Rights:

1. Go to **User Rights** in the project menu.
2. Click the username to edit their rights.
3. Under the list of application access checkboxes, uncheck **Calendar**.
4. Click **Save Changes**.

The Calendar link will no longer appear in the project menu for that user. Users with the Calendar right unchecked cannot view, create, or delete Calendar entries.

## 3.3 Enabling the Scheduling module (optional)

The Scheduling module is a separate, optional feature that generates visit date schedules for participants based on event offsets. It is only available in longitudinal projects and must be explicitly enabled.

**Prerequisites:** The project must already have longitudinal mode enabled (Project Setup → check "Use longitudinal data collection with defined events"). Scheduling cannot be enabled without longitudinal mode.

**To enable Scheduling:**

1. In **Project Setup**, scroll to the **Enable optional modules and customizations** section.
2. Check **Use the Scheduling module?** and save.

Enabling the Scheduling module does two things:

- **Adds scheduling fields to Define My Events:** The `Days Offset`, `Offset (Min)`, and `Offset (Max)` columns become available for each event. Days Offset controls the event's position in the schedule (and its sort order); the min and max offsets define the acceptable visit window around the target date.
- **Adds a Scheduling link to the project menu:** A **Scheduling** link appears under the **Data Collection** section of the left-side menu. This is the interface used to generate and manage participant schedules.

---

# 4. Using the Calendar

## 4.1 Accessing the Calendar

Click **Calendar** in the left-side project menu under Applications. This opens the monthly calendar view by default. A brief description at the top of the page explains the Calendar's purpose and, if the project has defined events, provides a link to generate a schedule directly from that page.

## 4.2 Switching views

The Calendar supports four views:

| View | Description |
|---|---|
| **Month** | Overview of all entries for the current month. Each entry appears as a short label on its date. |
| **Week** | Seven-day view showing entries by day column with time slots. |
| **Day** | Single-day view with time-slotted entries. Useful for days with many appointments. |
| **Agenda** | List-style view of upcoming entries in chronological order. Useful for reviewing a large number of events without navigating day by day. |

Navigate between time periods using the **Previous** and **Next** arrows, or click **Today** to return to the current date.

## 4.3 Creating a Calendar entry manually

1. In the Month view, click the **+New** button at the top of any day's box. In Week or Day view, click a time slot on the desired day.
2. In the entry dialog, fill in:
   - **Notes**: A free-text description of the appointment or event.
   - **Time** (optional): The scheduled time.
3. Click **Save**.

Any user with access to the Calendar can create entries. There is no separate user right for Calendar write access — access is controlled by whether the user has project access.

> **Note:** Manual Calendar entries created via **+New** are freestanding — they are not linked to a specific record, event, or user. They exist only as dated notes visible to all users with the Calendar right. If you need a calendar entry tied to a specific participant, use the Ad Hoc event feature on the View or Edit Schedule tab instead (see Section 5.3).

## 4.4 Editing and deleting entries

Click on any existing entry to open it. From the entry dialog you can update the fields or click **Delete** to remove the entry. Deletion is immediate and not reversible through the interface.

## 4.5 What users see

The Calendar shows all entries the user has access to based on their project access. There are no filter controls — users cannot narrow the calendar down to a specific record, event, or user from within the Calendar interface. Users restricted to a Data Access Group will naturally only see entries for records within their DAG, but there is no manual filter to apply.

---

# 5. Calendar and the Scheduling Module

## 5.1 The Scheduling page

When the Scheduling module is enabled, a **Scheduling** link appears under **Data Collection** in the left-side project menu. The Scheduling page has two tabs:

- **Create Schedule** — generate a new schedule for a record by selecting a start date.
- **View or Edit Schedule** — view and modify an existing schedule for a specific record.

## 5.2 Generating a schedule (Create Schedule tab)

The Schedule Generator projects visit dates for all events using their configured Days Offset and the start date you provide:

1. Click **Scheduling** under Data Collection.
2. On the **Create Schedule** tab, either:
   - Enter a new Record ID in the **Add new Record ID** field, or
   - Select an existing unscheduled record from the **choose existing unscheduled** dropdown.
3. Enter a **Start Date** — this is the baseline date (e.g., enrollment date) from which all event dates are calculated.
4. Click **Generate Schedule**.

REDCap calculates a target date for each event by adding that event's Days Offset to the Start Date. The projected dates are displayed on screen as a preview — **the schedule is not saved yet at this point.** Review the dates and adjust any that need to change (e.g., to avoid a weekend or clinic closure). When the dates are correct, click **Create Schedule** to commit the schedule. Only after clicking Create Schedule are the entries saved and pushed to the Calendar.

**The role of Offset Min and Offset Max:** After a schedule is generated, the min and max offset values define how far a visit date can be moved from its target date when rescheduling. For example, if an event has `Offset Min = 2` and `Offset Max = 2`, a user can schedule that visit up to two days earlier or two days later than the target. This flexibility is useful for practical situations like clinic closures on weekends — a two-day offset on either side lets staff book the visit on the nearest available weekday. REDCap displays a warning if a date is changed beyond the configured offset range but does not block the save.

> **Note:** A record can only be scheduled once from the Create Schedule tab. To reschedule or modify an existing schedule, use the **View or Edit Schedule** tab.

## 5.3 Viewing and editing a schedule (View or Edit Schedule tab)

The **View or Edit Schedule** tab lets you manage the schedule for a previously scheduled record:

1. Select the record from the **Select a previously scheduled Record ID** dropdown.
2. The schedule table displays all calendar events for that record with the following columns:

| Column | Description |
|---|---|
| (icons) | Edit (pencil), Delete (trash), and View (eye) icons for each entry. |
| **Time** | Optional time of the visit. |
| **Date / Day of Week** | Target date. Dates falling on weekends are shown in **red**. |
| **Event Name** | The defined project event, or "Ad Hoc" for manually added entries. |
| **Status** | Visit status: Due Date, Scheduled, Confirmed, Cancelled, or No Show. |
| **Notes** | Free-text notes for the entry. |

**Editing an entry:** Click the edit icon on any row to change the date, time, status, or notes. If you change a date, REDCap prompts: *"Do you wish to adjust all later dates by this amount (X days)?"* — answering yes shifts all subsequent scheduled entries by the same number of days. This bulk shift does not apply to Ad Hoc events.

**Adding an Ad Hoc event:** At the bottom of the schedule table, enter a date in the **Add new Ad Hoc calendar event on** field and click **Add**. Ad Hoc events are not tied to a defined project event and are excluded from bulk date shifts.

**Print Schedule:** Click **Print Schedule** to open a print-ready view of the record's schedule.

## 5.4 Event detail view

Clicking the **View icon** on any calendar entry (or clicking the entry in the Calendar itself) opens the event detail view. This view shows:

- **Record ID** — with quick links to **View Schedule** and **View Record Home Page**.
- **Event Name** — the associated project event (or "Ad Hoc").
- **Status** — a dropdown to update the visit status (Due Date, Scheduled, Confirmed, Cancelled, No Show).
- **Date** and **Time** — editable fields.
- **Notes** — free-text field.
- **Data Entry Forms** — a list of instruments assigned to this event. Clicking a form name navigates directly to the data entry page for that record and event, without leaving the calendar context.

## 5.5 Auto-generated Calendar entries

Once a schedule is generated, Calendar entries appear for each event in the participant's schedule. These entries:

- Are linked to the specific record and event.
- Can be individually rescheduled via the View or Edit Schedule tab, with REDCap warning if the new date falls outside the configured min/max offset window.
- Can be viewed and supplemented with notes via the Calendar or event detail view.

> **Note:** Deleting a Calendar entry does not cancel the underlying schedule. The entry will reappear if the schedule is recalculated. To cancel a visit, change its status to **Cancelled** via the View or Edit Schedule tab or the event detail view — do not delete the entry.

---

# 6. Limitations and Scope

Understanding what the Calendar does *not* do prevents common misuse:

**Not a notification or reminder tool.** The Calendar displays scheduled dates but does not send emails, text messages, or other reminders when an appointment date arrives. For automated notifications, use Alerts & Notifications (see RC-ALERT-01) or Automated Survey Invitations (see RC-SURV-06).

**Not a survey scheduler.** Calendar entries do not trigger survey sends. Surveys are scheduled through Automated Survey Invitations or the Survey Queue, not through the Calendar.

**External calendar integration is export-only.** REDCap can push calendar events out to external applications (Google Calendar, Outlook, Office 365, Zoho, Apple Calendar, or any iCal/ICS-compatible app) via a live feed URL or a one-time ICS file download. Both options are strictly one-way: changes made in REDCap propagate outward, but you cannot import events into REDCap from an external calendar. This means importing clinic schedules, OnCore visit lists, or Epic appointments into the REDCap Calendar is not supported — it is a commonly requested feature but not currently available. Downloading and re-importing the ICS file will create duplicate events in the external application.

**Not a source of record for clinical scheduling.** The Calendar is a research project tool and is not connected to hospital appointment systems (Epic, etc.). It should not be used as the primary scheduling record for clinical care appointments.

**Calendar actions are partially logged.** Calendar and scheduling activity is captured in the REDCap Logging module to some extent, under the Manage/Design action type. Confirmed examples include creating a calendar event ("Create calendar event (Record: 1, Date: 2026-04-28)") and generating a schedule ("Perform scheduling"). The full scope of what is logged (edits, deletions, status changes) may vary — check your project's Logging page if you need to verify a specific action.

---

# 7. Common Questions

**Q: Where is the Calendar in my project? I don't see it in the menu.**
**A:** The Calendar is on by default and appears in the Applications section of the left menu for all projects. If you can't see it, your user rights for this project likely have the Calendar checkbox unchecked. Ask your project owner to go to User Rights, edit your account, and check the Calendar option.

**Q: Can I use the Calendar in a classic (non-longitudinal) project?**
**A:** Yes. The Calendar is available in all project types. In classic projects you can create and manage manual entries, but the Event filter and Scheduling module (which require longitudinal mode) will not appear.

**Q: How is the Calendar different from Alerts & Notifications?**
**A:** The Calendar is a passive display tool — it shows scheduled events but does nothing on its own. Alerts & Notifications is an active system that evaluates conditions and sends messages when those conditions are met. They serve different purposes and can be used together: you might manually note an appointment in the Calendar while also setting up an alert to email the participant a reminder the day before.

**Q: Will the Calendar send reminders to participants or staff when an appointment date arrives?**
**A:** No. The Calendar does not send any notifications. Use Alerts & Notifications (RC-ALERT-01) or Automated Survey Invitations (RC-SURV-06) to send time-based communications.

**Q: If I delete a record, will its scheduled Calendar entries also be deleted?**
**A:** Scheduled entries (generated by the Scheduling module) are tied to the record. Manually created Calendar entries (added via the +New button) are freestanding notes not linked to any record, so they are unaffected by record deletion regardless.

**Q: Can I sync the REDCap Calendar with Google Calendar or Outlook?**
**A:** Yes. The Calendar page includes two export options: a live iCal/ICS URL feed (subscribe to it in Google Calendar, Outlook, Office 365, Apple Calendar, or any iCal-compatible app) and a one-time ICS file download for manual import. Both are one-way — changes made in REDCap push out to the external app, but you cannot edit entries from the external app. Note that live feeds may not refresh immediately; the external application controls the refresh interval.

**Q: Can I export Calendar entries?**
**A:** Not through the standard data export. Calendar entries are not part of the project data export (Data Export Tool) and have no dedicated API export method. However, you can download a snapshot of all Calendar entries as an ICS file from the Calendar page itself, or subscribe an external calendar app to the live iCal feed.

**Q: What statuses can a scheduled visit have?**
**A:** Five statuses are available: Due Date (default when first scheduled), Scheduled, Confirmed, Cancelled, and No Show. Status is set via the View or Edit Schedule tab or the event detail view.

**Q: Can I add a visit that wasn't part of the original schedule?**
**A:** Yes. On the View or Edit Schedule tab, use the **Add new Ad Hoc calendar event** field at the bottom of the table. Ad Hoc events are not tied to a defined project event and are excluded when you bulk-shift later dates after rescheduling a visit.

**Q: I rescheduled one visit and want all later visits to shift by the same number of days — is that possible?**
**A:** Yes. When you change the date of a scheduled event on the View or Edit Schedule tab, REDCap prompts you to adjust all later events by the same number of days. Accepting the prompt shifts all subsequent scheduled events. Ad Hoc events are not included in this bulk shift.

**Q: How do I hide the Calendar from certain users?**
**A:** Go to User Rights, edit the user's permissions, and uncheck the **Calendar** checkbox. The Calendar link will disappear from their project menu. This does not affect other users or delete any existing Calendar entries.

**Q: Can I turn off the Calendar for the whole project?**
**A:** No. The Calendar cannot be disabled at the project level — it is always present. The only way to restrict access is per-user through User Rights.

**Q: Can I control which users can add or delete Calendar entries?**
**A:** The Calendar right in User Rights controls both read and write access together — a user with the Calendar right can view, create, edit, and delete entries. There is no more granular split between read-only and read-write Calendar access. Users restricted to a Data Access Group will only see calendar entries for records within their DAG.

---

# 8. Common Mistakes & Gotchas

**Expecting the Calendar to send reminders.** Users set up Calendar entries assuming participants or staff will be notified automatically when the appointment date arrives. REDCap's Calendar is display-only — it does not trigger any communications. Set up Alerts & Notifications or Automated Survey Invitations separately if reminders are needed.

**Confusing the Calendar with the Scheduling module.** The Calendar (in Applications) shows entries; the Scheduling module (under Data Collection) is a separate tool that calculates visit dates from a start date and pushes them into the Calendar. The Calendar works without Scheduling — but if you need automatically calculated visit dates, you must enable the Scheduling module separately in Project Setup. Scheduling requires longitudinal mode to be turned on first.

**Trying to enable Scheduling without longitudinal mode.** The Scheduling option in Project Setup is only available after longitudinal mode is enabled. If you don't see the Scheduling option in the optional modules list, check that longitudinal mode is turned on first.

**Deleting Calendar entries expecting that to cancel a schedule.** When the Scheduling module is active, deleting a Calendar entry does not cancel the underlying participant schedule. The entry will reappear if the schedule is recalculated. To reschedule or remove a visit, use the **View or Edit Schedule** tab in the Scheduling page, not the Calendar.

**Relying on the Calendar for clinical appointment management.** The REDCap Calendar is a research tracking tool and is not connected to hospital scheduling systems (such as Epic). Using it as the primary record for clinical care appointments risks miscommunication and missed visits. Use it alongside — not instead of — your institutional scheduling systems.

**Importing the ICS file multiple times creates duplicate events.** The one-time ICS download is a static snapshot. If you download and import it again after new entries have been added, you will get duplicate events for everything that was in the first export. Use the live iCal feed URL instead if you want ongoing synchronization without managing duplicates.

**Not clicking "Create Schedule" after generating a projected schedule.** Clicking **Generate Schedule** only previews the projected dates — it does not save anything. The schedule is not created and no Calendar entries are added until the user reviews the dates and clicks **Create Schedule**. This is one of the most common mistakes with the Scheduling module: a user generates a schedule, assumes it is saved, and later finds no Calendar entries and no schedule on the View or Edit Schedule tab.

**Deleting a scheduled Calendar entry instead of setting status to Cancelled.** Deleting a scheduled entry removes it from view, but the underlying schedule record is not cancelled — the entry may reappear on recalculation. To properly close out a missed or cancelled visit, set the entry's status to **Cancelled** or **No Show** via the View or Edit Schedule tab. This preserves the visit record in the schedule history.

**Assuming Calendar and scheduling actions are fully absent from the audit log.** Both calendar and scheduling activity is logged to some extent — creating a calendar event and generating a schedule are both confirmed logged. However, not all actions (edits, deletions, status changes) may be captured, so if your protocol requires a complete audit trail of scheduling activity, verify coverage in the Logging page rather than assuming it is either fully tracked or fully absent.

---

# 9. Related Articles

- RC-NAV-UI-02 — Project Menu Reference (Calendar listed as a conditional project menu item)
- RC-LONG-01 — Longitudinal Project Setup (Scheduling module configuration, `day_offset` and offset windows)
- RC-ALERT-01 — Alerts & Notifications: Setup (time-based automated notifications)
- RC-SURV-06 — Automated Survey Invitations (scheduling survey delivery)
- RC-DE-10 — Longitudinal & Repeated Data Entry (navigating data entry across events)
- RC-PROJ-02 — Project Setup Checklist (enabling optional modules)
- RC-USER-03 — User Rights: Configuring User Privileges (Calendar checkbox in user rights)

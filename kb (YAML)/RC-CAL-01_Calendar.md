---
id: RC-CAL-01
title: Calendar
domain: Calendar
applies_to:
- All project types
- primarily used in longitudinal projects
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — Calendar
  and Scheduling behaviour checked against source code; pages not re-captured
prerequisites:
- RC-NAV-UI-02 — Project Menu Reference
version: '1.9'
last_updated: 2026-11
related:
- id: RC-LONG-01
  title: Longitudinal Project Setup
- id: RC-ALERT-01
  title: 'Alerts & Notifications: Setup'
- id: RC-SURV-06
  title: Automated Survey Invitations (ASI)
- id: RC-NAV-UI-02
  title: Project Menu Reference
tags:
- calendar
synonyms:
- how do i schedule participant visits in redcap
- redcap calendar and scheduling module
- track appointments and study visits
- generate a projected visit schedule
- add an event to the project calendar
- days offset scheduling for longitudinal events
- where is the calendar in redcap
- plan participant appointment dates
---

# 1. Overview

This article covers the REDCap Calendar module and the closely related Scheduling module. The Calendar is a built-in project tool for recording and viewing scheduled participant appointments, study visits, and other project-related events on a date-based calendar. It is available in all project types and appears in the Applications menu by default. The Scheduling module is an optional add-on for longitudinal projects that automates visit date calculation: given a start date and the Days Offset configured for each event, it generates a projected schedule for a participant and pushes those dates into the Calendar. Together, these two features give study teams a way to plan, track, and adjust participant visit schedules within REDCap. Neither feature sends reminders, triggers surveys, or connects to hospital scheduling systems such as Epic.

---

# 2. Key Concepts & Definitions

## Calendar Entry
A record in the Calendar representing a single scheduled event. Each entry has a date, an optional time, a required note, and optional links to a specific record ID and event (in longitudinal projects). An entry linked to a record also belongs to that record's Data Access Group. Entries are not linked to individual users. Calendar entries are not instruments or data fields — they store no collected data and do not appear in the Data Export Tool or the API.

## Calendar Module
The project-level feature that provides the Calendar interface. The Calendar is enabled by default for all projects and appears in the **Applications** section of the left-side project menu. There is no project-level switch to turn it off; access is controlled per user by the **Calendar** right in User Rights (ticked by default for new users). Also referred to as the "Calendar" in the REDCap interface.

## Scheduling Module
A separate, optional REDCap feature for longitudinal projects that calculates and assigns target visit dates (and acceptable offset windows) to each event for each participant, based on a reference date (such as enrollment). When active, the Scheduling module can automatically populate Calendar entries for each scheduled visit. The Scheduling module and the Calendar module are distinct features; the Calendar can be used without Scheduling, and Scheduling data is only reflected in the Calendar when both are enabled.

## Visit Window
In the Scheduling module context, the range of dates (defined by **Offset (Min)** and **Offset (Max)** around a target date) within which a participant's visit is considered on-schedule. Visit windows are configured per-event and displayed in the Calendar when Scheduling is active. See [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) for Scheduling module configuration details.

## Ad Hoc Event
A Calendar entry that is tied to a specific record but not to a defined project event. Ad Hoc events can be added from the View or Edit Schedule tab after selecting a record, or from the Calendar itself by choosing a record when creating an entry with **+New** (see Section 4.3). Ad Hoc events have no visit status. They are excluded from the bulk date-shift calculation when a scheduled event date is changed. Common uses include tracking contact attempts (e.g., called participant — no answer), logging reminders for study staff to follow up, or recording unplanned interactions that don't correspond to a formal protocol visit.

## Schedule Entry Status
Each scheduled Calendar entry (one linked to a project event) has a status field that tracks the visit state. Status options are: **Due Date** (the default), **Scheduled**, **Confirmed**, **Cancelled**, and **No Show**. Ad Hoc entries and unlinked notes have no status. Status is set and updated on the View or Edit Schedule tab or in the event detail view.

---

> **Note (16.0.7):** The calendar table was widened to fill the page, showing more of each entry's text without truncation.

> **Version caveat (below 15.5.38 Standard):** An Insecure Direct Object Reference on the Calendar page allowed a user assigned to a **Data Access Group** to create, modify or view calendar events **outside their DAG** via a crafted request. Fixed in 15.5.38. Relevant when assessing whether DAG separation held historically — see [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md).

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

The Calendar link will no longer appear in the project menu for that user. Users with the Calendar right unchecked cannot view, create, or delete Calendar entries, and they also lose the **Scheduling** link. The same single right covers every Calendar and Scheduling action; when the Scheduling module is enabled the right is labelled **Calendar & Scheduling**.

## 3.3 Enabling the Scheduling module (optional)

The Scheduling module is a separate, optional feature that generates visit date schedules for participants based on event offsets. It is only available in longitudinal projects and must be explicitly enabled.

**Prerequisites:** The project must already have longitudinal mode enabled (Project Setup → check "Use longitudinal data collection with defined events"). Scheduling cannot be enabled without longitudinal mode.

**To enable Scheduling:**

1. In **Project Setup**, scroll to the **Enable optional modules and customizations** section.
2. Click the **Enable** button next to **Scheduling module (longitudinal only)**. The same button reads **Disable** once the module is on.

> **Note:** Once a project is in production, only a REDCap administrator can change the Scheduling module setting.

Enabling the Scheduling module does two things:

- **Adds scheduling fields to Define My Events:** The `Days Offset`, `Offset (Min)`, and `Offset (Max)` columns become available for each event. Days Offset controls the event's position in the schedule (and its sort order); the min and max offsets define the acceptable visit window around the target date. (These columns also appear when MyCap is enabled. Because Days Offset sets the order, events can no longer be reordered by drag and drop.)
- **Adds a Scheduling link to the project menu:** A **Scheduling** link appears under the **Data Collection** section of the left-side menu. This is the interface used to generate and manage participant schedules.

---

# 4. Using the Calendar

## 4.1 Accessing the Calendar

Click **Calendar** in the left-side project menu under Applications. This opens the monthly calendar view by default. A brief description at the top of the page explains the Calendar's purpose and, if the project is longitudinal and the Scheduling module is enabled, provides a link to generate a schedule. Users in a Data Access Group see a notice that they only see entries for their group.

## 4.2 Switching views

The Calendar supports four views:

| View | Description |
|---|---|
| **Month** | Grid of the whole month. Each day shows up to five entries, then a "+N more" link. |
| **Week** | The same grid as Month, limited to one week. There are no time slots. |
| **Day** | A list of the entries for a single day (agenda style). There are no time slots, and you cannot create entries from this view. |
| **Agenda** | List of every entry in the selected month, in date order, including past dates. |

Navigate with the **Previous** and **Next** arrows, or jump to a date with the month, year and day dropdowns. There is no **Today** button. Use **Print Calendar** for a printable version of the current view.

Entry labels show the record ID (or the project's custom record label / secondary unique field), the DAG name where relevant, and a status icon for scheduled visits.

## 4.3 Creating a Calendar entry manually

1. In the Month or Week view, click the **+New** button in the desired day's box.
2. In the entry dialog, fill in:
   - **Notes** (required): A free-text description of the appointment or event.
   - **Time** (optional): The scheduled time.
   - **Record** (optional): Choose a record to link the entry to a participant.
3. Click **Save**.

Any user with the **Calendar** right can create entries (see Section 3.2).

> **Note:** An entry created via **+New** without a record is a freestanding dated note, visible to every user with the Calendar right, including users in a Data Access Group. If you choose a record, the entry becomes an **Ad Hoc** entry for that record and appears on the record's schedule on the View or Edit Schedule tab (see Section 5.3).

## 4.4 Editing and deleting entries

Click on any existing entry to open it. From the entry dialog you can update the fields or click **Delete** to remove the entry. REDCap asks you to confirm, and then the deletion is permanent: it cannot be undone and nothing recreates the entry later.

## 4.5 What users see

The Calendar shows every entry the user has access to. There are no filter controls — users cannot narrow the calendar down to a specific record or event (in any project type). Users in a Data Access Group see entries for records in their DAG plus all entries that are not linked to any record, whoever created them. Entries follow their record: if a record is renamed or moved to a different DAG, its calendar entries move with it.

## 4.6 Upcoming-entries widgets and smart variables

- **Project Home** shows a list of calendar entries for the next seven days.
- The **Record Home Page** has a button that shows the upcoming calendar entries for that record.
- The smart variables `[calendar-url]` and `[calendar-link]` let you pipe a calendar feed URL or clickable link into emails, alerts or other text.

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
   - Enter a new Record ID in the **Add new Record ID** field (requires the **Create Records** right), or
   - Select an existing unscheduled record from the **choose existing unscheduled** dropdown.
3. Enter a **Start Date** — this is the baseline date (e.g., enrollment date) from which all event dates are calculated.
4. Click **Generate Schedule**.

REDCap calculates a target date for each event by adding that event's Days Offset to the Start Date. The projected dates are displayed on screen as a preview — **the schedule is not saved yet at this point.** Review the dates and adjust any that need to change (e.g., to avoid a weekend or clinic closure). When the dates are correct, click **Create Schedule** to commit the schedule. Only after clicking Create Schedule are the entries saved and pushed to the Calendar.

**The role of Offset Min and Offset Max:** After a schedule is generated, the min and max offset values define how far a visit date can be moved from its target date when rescheduling. For example, if an event has `Offset Min = 2` and `Offset Max = 2`, a user can schedule that visit up to two days earlier or two days later than the target. This flexibility is useful for practical situations like clinic closures on weekends — a two-day offset on either side lets staff book the visit on the nearest available weekday. REDCap displays a warning if a date is changed beyond the configured offset range but does not block the save.

> **Note:** A record can only be scheduled once per arm from the Create Schedule tab. To reschedule or modify an existing schedule, use the **View or Edit Schedule** tab. If every event entry for a record is deleted, the record becomes unscheduled and can be scheduled again.

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

> **Note:** The Calendar entries *are* the schedule — there is no separate schedule behind them. Deleting an entry removes that visit permanently; nothing recalculates or recreates it. To record a cancelled or missed visit, change its status to **Cancelled** or **No Show** via the View or Edit Schedule tab or the event detail view instead of deleting it, so the visit history is kept.

---

# 6. Limitations and Scope

Understanding what the Calendar does *not* do prevents common misuse:

**Not a notification or reminder tool.** The Calendar displays scheduled dates but does not send emails, text messages, or other reminders when an appointment date arrives. For automated notifications, use Alerts & Notifications (see [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)) or Automated Survey Invitations (see [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)).

**Not a survey scheduler.** Calendar entries do not trigger survey sends. Surveys are scheduled through Automated Survey Invitations or the Survey Queue, not through the Calendar.

**External calendar integration is export-only.** REDCap can push calendar events out to external applications (Google Calendar, Outlook, Office 365, Zoho, Apple Calendar, or any iCal/ICS-compatible app) via a live feed URL or a one-time ICS file download. Both options are strictly one-way: changes made in REDCap propagate outward, but you cannot import events into REDCap from an external calendar. This means importing clinic schedules, OnCore visit lists, or Epic appointments into the REDCap Calendar is not supported — it is a commonly requested feature but not currently available. Downloading and re-importing the ICS file will create duplicate events in the external application. Each feed belongs to one user in one project and shows what that user is currently allowed to see (their rights and DAG). A REDCap administrator can turn calendar feeds off for the whole server.

**Not a source of record for clinical scheduling.** The Calendar is a research project tool and is not connected to hospital appointment systems (Epic, etc.). It should not be used as the primary scheduling record for clinical care appointments.

**Calendar actions are logged.** Calendar and scheduling activity appears on the project's Logging page under the Manage/Design action type. This covers creating an entry (e.g. "Create calendar event (Record: 1, Date: 2026-04-28)"), editing one (date, time, status or notes), deleting one, the bulk "adjust all later dates" update, and generating a schedule ("Perform scheduling").

**Project-wide data actions include the Calendar.** Calendar entries are included when a project is exported and imported with Project Migration. **Erase all data** and deleting data when moving to production both remove all calendar entries. Deleting a record deletes all of its calendar entries, including Ad Hoc entries.

---

# 7. Common Questions

**Q: Where is the Calendar in my project? I don't see it in the menu.**
**A:** The Calendar is on by default and appears in the Applications section of the left menu for all projects. If you can't see it, your user rights for this project likely have the Calendar checkbox unchecked. Ask your project owner to go to User Rights, edit your account, and check the Calendar option.

**Q: Can I use the Calendar in a classic (non-longitudinal) project?**
**A:** Yes. The Calendar is available in all project types. In classic projects you can create and manage manual entries (with or without a linked record), but the Scheduling module requires longitudinal mode and will not be available. The Calendar has no event filter in any project type.

**Q: How is the Calendar different from Alerts & Notifications?**
**A:** The Calendar is a passive display tool — it shows scheduled events but does nothing on its own. Alerts & Notifications is an active system that evaluates conditions and sends messages when those conditions are met. They serve different purposes and can be used together: you might manually note an appointment in the Calendar while also setting up an alert to email the participant a reminder the day before.

**Q: Will the Calendar send reminders to participants or staff when an appointment date arrives?**
**A:** No. The Calendar does not send any notifications. Use Alerts & Notifications ([RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md)) or Automated Survey Invitations ([RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)) to send time-based communications.

**Q: If I delete a record, will its scheduled Calendar entries also be deleted?**
**A:** Yes. Deleting a record deletes every calendar entry linked to it — scheduled visits and Ad Hoc entries alike, including any created via **+New** with that record selected. Entries created via **+New** without a record are not linked to any record and are unaffected.

**Q: Can I sync the REDCap Calendar with Google Calendar or Outlook?**
**A:** Yes. The Calendar page includes two export options: a live iCal/ICS URL feed (subscribe to it in Google Calendar, Outlook, Office 365, Zoho Calendar, Apple Calendar, or any iCal-compatible app) and a one-time ICS file download for manual import. Both are one-way — changes made in REDCap push out to the external app, but you cannot edit entries from the external app. Note that live feeds may not refresh immediately; the external application controls the refresh interval.

**Q: Can I export Calendar entries?**
**A:** Not through the standard data export. Calendar entries are not part of the project data export (Data Export Tool) and have no dedicated API export method. However, you can download a snapshot of all Calendar entries as an ICS file from the Calendar page itself, or subscribe an external calendar app to the live iCal feed.

**Q: What statuses can a scheduled visit have?**
**A:** Five statuses are available: Due Date (default when first scheduled), Scheduled, Confirmed, Cancelled, and No Show. Status is set via the View or Edit Schedule tab or the event detail view. Ad Hoc entries have no status.

**Q: Can I add a visit that wasn't part of the original schedule?**
**A:** Yes. On the View or Edit Schedule tab, use the **Add new Ad Hoc calendar event** field at the bottom of the table, or click **+New** on the Calendar and choose the record. Ad Hoc events are not tied to a defined project event and are excluded when you bulk-shift later dates after rescheduling a visit.

**Q: I rescheduled one visit and want all later visits to shift by the same number of days — is that possible?**
**A:** Yes. When you change the date of a scheduled event on the View or Edit Schedule tab, REDCap prompts you to adjust all later events by the same number of days. Accepting the prompt shifts all subsequent scheduled events. Ad Hoc events are not included in this bulk shift.

**Q: How do I hide the Calendar from certain users?**
**A:** Go to User Rights, edit the user's permissions, and uncheck the **Calendar** checkbox. The Calendar link will disappear from their project menu. This does not affect other users or delete any existing Calendar entries.

**Q: Can I turn off the Calendar for the whole project?**
**A:** No. The Calendar cannot be disabled at the project level — it is always present. The only way to restrict access is per-user through User Rights.

**Q: Can I control which users can add or delete Calendar entries?**
**A:** The Calendar right in User Rights controls both read and write access together — a user with the Calendar right can view, create, edit, and delete entries. There is no more granular split between read-only and read-write Calendar access. Users restricted to a Data Access Group see calendar entries for records within their DAG, plus all entries not linked to any record.

---

# 8. Common Mistakes & Gotchas

**Expecting the Calendar to send reminders.** Users set up Calendar entries assuming participants or staff will be notified automatically when the appointment date arrives. REDCap's Calendar is display-only — it does not trigger any communications. Set up Alerts & Notifications or Automated Survey Invitations separately if reminders are needed.

**Confusing the Calendar with the Scheduling module.** The Calendar (in Applications) shows entries; the Scheduling module (under Data Collection) is a separate tool that calculates visit dates from a start date and pushes them into the Calendar. The Calendar works without Scheduling — but if you need automatically calculated visit dates, you must enable the Scheduling module separately in Project Setup. Scheduling requires longitudinal mode to be turned on first.

**Trying to enable Scheduling without longitudinal mode.** The Scheduling option in Project Setup is only available after longitudinal mode is enabled. If you don't see the Scheduling option in the optional modules list, check that longitudinal mode is turned on first.

**Expecting a deleted entry to come back.** The Calendar entries are the schedule itself. Deleting one is permanent — nothing recalculates or restores it. To move a visit, edit its date on the **View or Edit Schedule** tab; to record that it did not happen, change its status rather than deleting it.

**Relying on the Calendar for clinical appointment management.** The REDCap Calendar is a research tracking tool and is not connected to hospital scheduling systems (such as Epic). Using it as the primary record for clinical care appointments risks miscommunication and missed visits. Use it alongside — not instead of — your institutional scheduling systems.

**Importing the ICS file multiple times creates duplicate events.** The one-time ICS download is a static snapshot. If you download and import it again after new entries have been added, you will get duplicate events for everything that was in the first export. Use the live iCal feed URL instead if you want ongoing synchronization without managing duplicates.

**Not clicking "Create Schedule" after generating a projected schedule.** Clicking **Generate Schedule** only previews the projected dates — it does not save anything. The schedule is not created and no Calendar entries are added until the user reviews the dates and clicks **Create Schedule**. This is one of the most common mistakes with the Scheduling module: a user generates a schedule, assumes it is saved, and later finds no Calendar entries and no schedule on the View or Edit Schedule tab.

**Deleting a scheduled Calendar entry instead of setting status to Cancelled.** Deleting a scheduled entry removes the visit permanently, and with it any record that the visit was planned. To properly close out a missed or cancelled visit, set the entry's status to **Cancelled** or **No Show** via the View or Edit Schedule tab. This keeps the visit in the record's schedule history.

**Assuming Calendar and scheduling actions are absent from the audit log.** Creating, editing (date, time, status, notes), deleting and bulk-shifting entries, and generating schedules all appear on the Logging page under Manage/Design. Calendar entries are still not part of the Data Export Tool, so use the Logging page or the ICS download when you need a record of scheduling activity.

---

# 9. Related Articles

- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md) (Calendar listed as a conditional project menu item)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (Scheduling module configuration, Days Offset and offset windows)
- [RC-ALERT-01 — Alerts & Notifications: Setup](RC-ALERT-01_Alerts-and-Notifications-Setup.md) (time-based automated notifications)
- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) (scheduling survey delivery)
- [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md) (navigating data entry across events)
- [RC-PROJ-02 — Project Setup Checklist](RC-PROJ-02_Project-Setup-Checklist.md) (enabling optional modules)
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) (Calendar checkbox in user rights)

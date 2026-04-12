RC-MYCAP-03

**MyCap: Task Scheduling**

| **Article ID** | RC-MYCAP-03 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | Projects with MyCap enabled |
| **Prerequisite** | RC-MYCAP-02 — Designing Instruments for MyCap |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-MYCAP-01 — MyCap: Overview & Enabling; RC-MYCAP-06 — Active Tasks & Mobile Toolbox; RC-LONG-01 — Longitudinal Project Setup |

---

# 1. Overview

This article covers how to configure the schedule that controls when MyCap tasks appear in a participant's app. Topics include the four schedule types (One-time, Infinite, Repeating, Fixed), delay onset, end conditions, how Active Tasks and Mobile Toolbox tasks are scheduled, and the additional considerations for scheduling in longitudinal projects. Schedule configuration is done in the MyCap section of the left-hand menu after instruments have been enabled.

---

# 2. Key Concepts & Definitions

**Schedule Reference Date**

The anchor date used to calculate when tasks appear. By default, this is the participant's **install date** (when they first joined the project in the app). If the project uses a baseline date, tasks can be scheduled relative to that date instead. See RC-MYCAP-02 — Designing Instruments for MyCap for baseline date configuration.

**Install Date**

The date and time a participant first joins the MyCap project on their device. This is the default scheduling reference if no baseline date is configured.

**Baseline Date**

An optional study-defined reference date (e.g., surgery date, enrollment date). When configured, tasks can be anchored to this date rather than the install date. See RC-MYCAP-02 for setup.

**Delay Onset**

The number of days after the schedule reference date before the task first becomes available. A delay of 0 means the task appears immediately on join.

**End Condition**

A rule that determines when a repeating task stops appearing. Options include: after a set number of occurrences, after a set number of days, or never (the task repeats indefinitely).

**Task Notification**

A push notification sent to the participant's device when a new task becomes available. Notifications are sent at 8:00 AM local device time by default. The notification time can be changed in App Settings (see RC-MYCAP-05).

**Overdue Task**

A task whose scheduled window has closed without being completed. Overdue tasks remain visible in the participant's app (marked as overdue) and can still be submitted unless an end condition has been reached.

**Active Task**

A sensor-based assessment built into MyCap (e.g., Tapping Speed, Tone Audiometry). Active Tasks are scheduled using the same schedule types as instrument-based tasks but are set up differently. See RC-MYCAP-06 — Active Tasks & Mobile Toolbox.

**Mobile Toolbox (MTB)**

Cognitive assessment tasks provided by the NIH Toolbox, available in MyCap as of REDCap v14.3.8. MTB tasks are scheduled like standard instruments. See RC-MYCAP-06 for details.

---

# 3. Schedule Types

All MyCap tasks use one of four schedule types. Schedule type is set per instrument (or per event in longitudinal projects).

## 3.1 One-Time

The task appears once at a specified number of days after the schedule reference date. The participant completes it once and it is done.

| Setting | Description |
|---|---|
| Delay onset (days) | Number of days after the reference date before the task appears (0 = day of join or baseline) |

**Use when:** Baseline assessments, enrollment surveys, single-timepoint measures.

## 3.2 Infinite

The task is always available. It does not expire and has no schedule — participants can complete it at any time and it reappears immediately after each submission.

| Setting | Description |
|---|---|
| No additional settings | Task is always visible |

**Use when:** Daily diaries where participants self-initiate, PRN (as-needed) symptom capture, or testing (set to Infinite during development to test without waiting for scheduled windows).

## 3.3 Repeating

The task appears on a regular cadence. Three sub-types are available:

**Daily** — repeats every N days after the previous occurrence.

**Weekly** — repeats on a specified day of the week, every N weeks.

**Monthly** — repeats on a specified day of the month, every N months.

| Setting | Description |
|---|---|
| Delay onset (days) | Days after the reference date before the first occurrence |
| Frequency | Daily / Weekly (with day of week) / Monthly (with day of month) |
| Interval | Every N days / weeks / months |
| End condition | Never, After N occurrences, After N days |

**Use when:** Weekly questionnaires, monthly assessments, daily symptom tracking.

## 3.4 Fixed

The task appears on a specific list of dates, independent of the participant's schedule reference date. All participants see the task on the same calendar dates.

| Setting | Description |
|---|---|
| Date list | One or more specific calendar dates when the task appears |

**Use when:** Study visits aligned to the calendar (e.g., flu season surveys, holiday-specific timing), population-wide synchronized data collection windows.

---

# 4. Delay Onset

Delay onset is available for One-Time and Repeating schedule types. It defines the number of days that must pass after the schedule reference date before the task first appears.

- Delay of **0**: task appears immediately when the participant joins (or on the baseline date).
- Delay of **7**: task appears 7 days after the reference date.
- Delay can be set to any whole number of days.

For Infinite tasks, delay onset is not applicable — the task is always available.

---

# 5. End Conditions

For Repeating schedules, you must specify when the task stops recurring:

| End condition | Description |
|---|---|
| Never | Task repeats indefinitely |
| After N occurrences | Task stops after the participant has been presented the task N times (regardless of whether it was completed) |
| After N days | Task stops after N days from the first occurrence |

---

# 6. Task Notifications

When a new task instance becomes available (i.e., the schedule window opens), MyCap sends a push notification to the participant's device.

- Notifications are sent at **8:00 AM local device time** by default.
- The notification time can be changed in App Settings (see RC-MYCAP-05 — App Settings & Participant Management).
- Notifications are not sent retroactively if the participant has not opened the app — the task will appear the next time they open the app, but no additional notification is sent for overdue tasks.
- MLM (Multi-Language Management) does not affect notification content independently — notification text is not translated separately.

---

# 7. Setting Up the Schedule (Traditional / Classic Projects)

For standard (non-longitudinal) projects:

1. In the MyCap section of the left menu, go to **Schedule Tasks**.
2. For each enabled instrument, click the **Set schedule** button.
3. Select a **Schedule Type**.
4. Configure the schedule-specific settings (delay, frequency, end condition).
5. Optionally set whether to schedule relative to the **install date** or **baseline date** (if baseline date is configured on the project).
6. Click **Save**.
7. After all schedules are set, **Publish** the project (see RC-MYCAP-02 — Designing Instruments for MyCap, Section 8).

---

# 8. Scheduling in Longitudinal Projects

## 8.1 Prerequisites

In longitudinal projects, an instrument must be designated to at least one arm and event on the instrument–event mapping page before it can be enabled for MyCap and given a schedule. Enabling for MyCap and scheduling are per-event, not per-instrument globally.

> **Note:** The **Days Offset** setting in REDCap's longitudinal event configuration does **not** affect MyCap scheduling. MyCap schedules are entirely independent of event day offsets.

## 8.2 Schedule Setup for Longitudinal Projects

1. In the MyCap section of the left menu, go to **Schedule Tasks**.
2. The schedule table shows rows for each instrument–event combination.
3. Set the schedule for each instrument in each event independently.
4. Use the **Copy below settings to** dropdown to copy a schedule configuration to other events, reducing repetitive data entry.
5. After configuring all schedules, **Publish** the project.

## 8.3 Active Tasks and Longitudinal Projects

Active Tasks (sensor-based assessments) must be designated to events on the instrument–event mapping page **before** being set up as MyCap Active Tasks. The Active Task setup step comes after event designation, not before.

---

# 9. Active Tasks and Mobile Toolbox Scheduling

Active Tasks (motor, cognition, speech, hearing assessments) and Mobile Toolbox (MTB) tasks are scheduled using the same four schedule types as instrument-based tasks. The schedule setup for Active Tasks is found in the **Active Tasks** tab within MyCap, not in the instrument schedule table.

For full details on Active Task types and configuration, see RC-MYCAP-06 — Active Tasks & Mobile Toolbox.

For MTB tasks, REDCap v14.3.8 or later is required. MTB tasks appear in the same Active Tasks scheduling interface.

---

# 10. Common Questions

**Q: What is the difference between install date and baseline date for scheduling?**

**A:** Install date is when the participant first joins the project in the app — it is automatically recorded. Baseline date is a study-defined date you configure (e.g., surgery date, enrollment date) that may be different from when the participant downloads the app. Using baseline date allows tasks to be anchored to a clinically meaningful event. If no baseline date is configured, all schedules default to the install date.

**Q: A participant joined late. Will they get all the tasks they missed?**

**A:** Tasks that were scheduled before a participant joins will appear as overdue (if the schedule type and end condition would have generated them). Overdue tasks remain available for the participant to complete. Fixed schedule tasks that occurred before a participant joined will appear as overdue.

**Q: Can I change a task's schedule after participants have already joined?**

**A:** Yes. Update the schedule in REDCap, then publish the updated configuration. The new schedule takes effect on participants' devices on their next sync. Tasks already completed are not affected.

**Q: What does "Infinite" schedule mean — does the task never end?**

**A:** Yes, an Infinite schedule means the task is always visible and reappears after each submission with no end date. Use Infinite for tasks participants can complete anytime (e.g., daily symptom diary, as-needed entries). Infinite is also useful during testing because you do not need to wait for scheduled windows.

**Q: Does the Days Offset in the longitudinal event setup affect when MyCap tasks appear?**

**A:** No. The Days Offset for REDCap longitudinal events is used for the browser-based record home page view and does not affect MyCap scheduling at all. MyCap uses its own schedule settings per event.

**Q: Can I have different schedules for the same instrument in different events (longitudinal)?**

**A:** Yes. Each instrument–event combination has its own independent schedule in longitudinal projects. The **Copy below settings to** dropdown makes it easy to replicate a schedule across events.

**Q: Can an overdue task still be completed?**

**A:** Yes. Overdue tasks remain in the participant's app and can be submitted unless the schedule's end condition has been reached (e.g., after N occurrences). The submission is accepted and recorded in REDCap with the actual submission date.

---

# 11. Common Mistakes & Gotchas

**Assuming REDCap longitudinal event day offsets control MyCap scheduling.** Day offsets for REDCap events have no effect on MyCap. Participants' task timing is controlled entirely by the MyCap schedule settings. If tasks appear at unexpected times, check the MyCap schedule — not the event configuration.

**Forgetting to publish after changing schedules.** Schedule changes are not visible to participants until the project is published. Participants will continue to see the old schedule until a publish is performed.

**Setting Active Tasks up before designating them to events (longitudinal).** Active Tasks must be designated to events on the instrument–event mapping page before you can configure them in the MyCap Active Tasks setup. Attempting to set up an Active Task before event designation will result in it not appearing in the scheduling interface.

**Using Fixed schedule when participant-relative timing is needed.** Fixed schedules are based on calendar dates, not individual participant timelines. All participants see Fixed schedule tasks on the same dates, regardless of when they joined. Use One-Time or Repeating schedules for participant-relative timing.

**Not setting an end condition on Repeating tasks when appropriate.** Without an end condition, a Repeating task runs indefinitely. If the study has a defined endpoint, set an end condition to prevent tasks from appearing after study completion.

---

# 12. Related Articles

- RC-MYCAP-02 — Designing Instruments for MyCap (baseline date setup, publishing)
- RC-MYCAP-05 — App Settings & Participant Management (notification time settings)
- RC-MYCAP-06 — Active Tasks & Mobile Toolbox
- RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links (Form Display Logic with scheduling considerations)
- RC-MYCAP-08 — Testing MyCap (schedule testing workflow)
- RC-LONG-01 — Longitudinal Project Setup
- RC-LONG-02 — Repeated Instruments & Events Setup

RC-MYCAP-02

**Designing Instruments for MyCap**

| **Article ID** | RC-MYCAP-02 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | Projects with MyCap enabled |
| **Prerequisite** | RC-MYCAP-01 — MyCap: Overview & Enabling |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-MYCAP-03 — Task Scheduling; RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links; RC-FD-01 — Form Design Overview; RC-AT-11 — Action Tags: Mobile App Action Tags |

---

# 1. Overview

This article covers how to prepare REDCap instruments for use in the MyCap mobile app. Topics include which field types are supported, MyCap-specific action tags (annotations), task metadata fields, form completion status configuration, how to enable instruments for MyCap, how to configure a baseline date, and the publishing workflow. Instrument design for MyCap follows the same Online Designer or Data Dictionary workflow as standard REDCap instruments, with additional mobile-specific constraints and annotations.

---

# 2. Key Concepts & Definitions

**MyCap Instrument**

A REDCap instrument that has been enabled for display in the MyCap app. Also called a MyCap task (instrument type). The instrument appears in the participant's task list according to the project-defined schedule.

**MyCap Annotation**

A mobile-specific action tag applied to a field in a MyCap-enabled instrument. Annotations override or extend default REDCap field behavior when the instrument is displayed in the MyCap app. They are entered in the field's Action Tags / Field Annotation column.

**Task Metadata Field**

A hidden field added to an instrument to capture MyCap-generated data about when a task was started, completed, or scheduled. These fields use special annotations (prefixed `@MC-TASK-`) and do not appear to participants.

**Form Completion Status**

The completion status a submitted MyCap task must reach in REDCap to be considered complete. If a participant's submission does not reach the required status, the task remains available (not marked done) in the app.

**Baseline Date**

An optional reference date used to schedule tasks relative to a meaningful event (e.g., a treatment start date or enrollment date). If not using baseline date, tasks are scheduled relative to the participant's install date.

**Install Date**

The date and time a participant first joins the MyCap project on their device. Used as the default scheduling reference when no baseline date is configured.

**Publish**

The action of pushing the current project configuration (enabled instruments, schedule, App Settings) to participants' devices. Required after most instrument and schedule changes.

---

# 3. Field Type Compatibility

Not all REDCap field types are supported in MyCap. The following table lists compatibility:

| Field Type | Supported in MyCap |
|---|---|
| Text (all validation types) | Yes |
| Notes | Yes |
| Radio button | Yes |
| Dropdown | Yes |
| Checkbox | Yes |
| Slider (Visual Analog Scale) | Yes (use `@MC-FIELD-SLIDER-BASIC` or `@MC-FIELD-SLIDER-CONTINUOUS` for best display) |
| Yes/No | Yes |
| True/False | Yes |
| Calculated field | **No** — does not compute in MyCap |
| File upload (generic) | No |
| File upload (image capture) | Yes — use `@MC-FIELD-FILE-IMAGECAPTURE` |
| File upload (video capture) | Yes — use `@MC-FIELD-FILE-VIDEOCAPTURE` |
| Signature | No |
| Descriptive text | Yes |
| Section header | Yes |
| Matrix (Grid of radio buttons) | Yes |

> **Important:** Calculated fields do not evaluate within MyCap. If you need to display a computed value to a participant, use the Survey Links feature to embed a REDCap survey. See RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links.

---

# 4. MyCap Annotations

MyCap annotations are action tags specific to the MyCap app. Apply them in the **Action Tags / Field Annotation** column of the Online Designer or Data Dictionary. Standard REDCap action tags are generally not honored in MyCap with the exception of `@HIDDEN`.

## 4.1 Field Display Annotations

| Annotation | Field type | Effect |
|---|---|---|
| `@MC-FIELD-HIDDEN` | Any | Hides the field from the participant in MyCap (equivalent to `@HIDDEN` for the mobile context) |
| `@MC-FIELD-SLIDER-BASIC` | Slider | Displays the slider with fixed endpoints; participant selects a point by tapping |
| `@MC-FIELD-SLIDER-CONTINUOUS` | Slider | Displays the slider as a continuous drag control; allows fine-grained positioning |

## 4.2 Data Capture Annotations

| Annotation | Field type | Effect |
|---|---|---|
| `@MC-FIELD-FILE-IMAGECAPTURE` | File upload | Opens the device camera to capture a photo; saves the image to the field |
| `@MC-FIELD-FILE-VIDEOCAPTURE` | File upload | Opens the device camera to capture a video; saves the video to the field |
| `@MC-FIELD-TEXT-BARCODE` | Text | Opens the device camera in barcode/QR-code scanning mode; saves the scanned value as text |

## 4.3 Geolocation Annotations

| Annotation | Field type | Effect |
|---|---|---|
| `@LONGITUDE` | Text | Captures the participant's GPS longitude at task submission |
| `@LATITUDE` | Text | Captures the participant's GPS latitude at task submission |

The `@LONGITUDE` and `@LATITUDE` annotations require the participant to grant location permissions to the MyCap app on their device.

## 4.4 Task Metadata Annotations

These annotations are applied to hidden fields to capture MyCap-generated information about each task instance. Add them to fields not visible to the participant (`@MC-FIELD-HIDDEN` or placed on a hidden section).

| Annotation | Data captured |
|---|---|
| `@MC-TASK-UUID` | Unique identifier for the task instance |
| `@MC-TASK-STARTDATE` | Date and time the participant opened the task |
| `@MC-TASK-ENDDATE` | Date and time the participant submitted the task |
| `@MC-TASK-SCHEDULEDATE` | Date the task was scheduled to appear |
| `@MC-TASK-STATUS` | Current task status (e.g., completed, overdue) |
| `@MC-TASK-SUPPLEMENTALDATA` | Supplemental data from Active Tasks (structured JSON) |
| `@MC-TASK-SERIALIZEDRESULT` | Serialized result data from Active Tasks |

`@MC-TASK-SUPPLEMENTALDATA` and `@MC-TASK-SERIALIZEDRESULT` are primarily used with Active Tasks (sensor-based assessments). For standard instrument-based tasks, `@MC-TASK-STARTDATE`, `@MC-TASK-ENDDATE`, and `@MC-TASK-SCHEDULEDATE` are the most commonly useful metadata fields.

---

# 5. Form Completion Status

MyCap determines whether a task has been completed by checking the REDCap form completion status of the submitted data. You must configure which status level qualifies as "done."

## 5.1 Configuration

1. In the MyCap section of the left menu, go to **Enable Instruments**.
2. For each instrument, locate the **Form Completion Status** column.
3. Set the required status to either **Complete** or **Unverified** (both are accepted as "done"). Selecting **Incomplete** means the task will never be marked complete regardless of the participant's submission.

> **Note:** The default status for MyCap submissions is typically "Unverified." If your workflow requires "Complete" status, a study team member must manually update the status in REDCap after reviewing the data, which will then mark the task done in the participant's app on next sync.

## 5.2 Effect on Task Availability

- If the required completion status has been reached: the task is marked done and removed from the participant's active task list (unless on an Infinite or Repeating schedule).
- If the required completion status has not been reached: the task remains available in the participant's app and they may resubmit.

---

# 6. Enabling Instruments for MyCap

Once instruments are designed and form completion status is configured:

1. In the MyCap section of the left menu, go to **Enable Instruments**.
2. Check the box next to each instrument to enable it for MyCap.
3. For longitudinal projects, instruments must first be designated to at least one event on the instrument–event mapping page before they can be enabled for MyCap.

> **Note:** Enabling an instrument for MyCap does not automatically assign it a schedule. Scheduling is a separate step — see RC-MYCAP-03 — Task Scheduling.

---

# 7. Baseline Date Configuration

The baseline date is an optional project-level feature that allows tasks to be scheduled relative to a meaningful date (e.g., surgery date, enrollment date, treatment start) rather than the participant's install date.

## 7.1 Requirements

- The baseline date field must reside in a **non-MyCap instrument** (an instrument not enabled for MyCap). Participants cannot set their own baseline date through a MyCap task.
- The baseline date field must be a **date field** (Date validation type).

## 7.2 Enabling Baseline Date

1. In the MyCap section of the left menu, go to **Additional Settings**.
2. Check **Use baseline date?**
3. Select the instrument and field that will store the baseline date.
4. Configure the three participant-facing questions that appear in the app when participants are asked about their baseline date:
   - **Title**: label shown at the top of the baseline date screen (e.g., "Your Surgery Date")
   - **Yes/No today question**: asks the participant whether the baseline event happened today (e.g., "Did you have surgery today?")
   - **Past date question**: shown if the participant answers No — asks them to enter the date (e.g., "When did you have surgery?")

## 7.3 Behavior

- When a participant joins, MyCap checks whether a baseline date exists for their record.
- If no baseline date is recorded, the app prompts the participant with the configured questions.
- If a baseline date has already been entered by the study team in REDCap, the participant is not prompted.
- Tasks scheduled relative to the baseline date appear in the participant's app according to the delay defined in the schedule (e.g., "Day 7 after baseline").
- If a participant's baseline date is later updated in REDCap (e.g., corrected by a coordinator), the schedule updates on the participant's next app open.

> **Note:** Only one baseline date is supported per project. Projects requiring multiple different reference dates (e.g., multiple treatment cycles) cannot currently use a single baseline date for all scheduling purposes.

---

# 8. Publishing

Publishing pushes the current project configuration — enabled instruments, schedule, and App Settings — to all participants' devices.

## 8.1 When to Publish

Publish is required after any of the following changes:
- Enabling or disabling instruments
- Changing the task schedule
- Changing App Settings (About pages, Contacts, Links, Theme, Notification Settings)

> **Note:** Form Display Logic changes and Multi-Language Management (MLM) changes do **not** require publishing — they apply immediately on the participant's next sync.

## 8.2 How to Publish

1. In the MyCap section of the left menu, go to **Publish MyCap Version**.
2. Review the summary of pending changes.
3. Click **Publish**.

Participants receive the updated configuration the next time they open the app with internet connectivity.

---

# 9. Common Questions

**Q: Can I use piping inside a MyCap instrument?**

**A:** No. REDCap piping syntax (e.g., `[first_name]`) is not rendered in MyCap — it appears as raw text. Remove piping from instruments intended for MyCap, or use a Survey Link to direct participants to a standard REDCap survey where piping works normally (see RC-MYCAP-07).

**Q: How do I capture a participant's photo in MyCap?**

**A:** Add a File Upload field to the instrument and apply the `@MC-FIELD-FILE-IMAGECAPTURE` annotation. When the participant reaches that field in the app, the device camera opens automatically.

**Q: What happens if a participant submits a task but it stays in their task list?**

**A:** The task's form completion status in REDCap has not reached the required threshold. Check the Form Completion Status setting for that instrument in the Enable Instruments tab, and verify that the submitted data has the expected status in REDCap.

**Q: Can I use the same instrument for both MyCap and standard web data entry?**

**A:** Yes. Enabling an instrument for MyCap does not prevent it from also being used in the browser-based REDCap interface by the study team. Be aware that features like piping and calculated fields work in the browser but not in MyCap.

**Q: Do I need to publish after every small change?**

**A:** Publish is required for schedule changes, newly enabled instruments, and App Settings changes. It is not required for Form Display Logic or MLM changes. Publish when you're ready for participants to receive changes — not for every individual edit.

**Q: Can a participant set their own baseline date?**

**A:** The baseline date can be entered by the study team in REDCap, or the app can prompt the participant to provide it on first launch (via the three configured questions). It cannot reside in a MyCap-enabled instrument that the participant completes as a task.

**Q: Can I add task metadata fields to any instrument?**

**A:** Yes. Add a hidden field (use `@MC-FIELD-HIDDEN`) and apply the appropriate `@MC-TASK-*` annotation. The field can be on any MyCap-enabled instrument and will capture data automatically when the task is submitted.

---

# 10. Common Mistakes & Gotchas

**Including calculated fields in MyCap instruments.** Calculated fields are silently skipped — they do not compute and they display blank. Participants may be confused. Remove calculated fields from MyCap instruments. If the calculated value must be shown to participants, use a Survey Link (RC-MYCAP-07).

**Applying standard REDCap action tags expecting them to work in MyCap.** Most standard action tags (e.g., `@NOW`, `@DEFAULT`, `@CHARLIMIT`) are not honored in MyCap. Only `@HIDDEN` and the MyCap-specific annotations listed in Section 4 of this article apply in the app context.

**Forgetting to designate instruments to events before enabling for MyCap (longitudinal projects).** In longitudinal projects, instruments must be designated to at least one event on the instrument–event mapping page before they appear in the Enable Instruments list for MyCap. If an instrument is not visible in the MyCap enable list, check event designations first.

**Setting form completion status to Incomplete.** Tasks set to require "Incomplete" status for completion can never be completed. Use "Unverified" or "Complete" as the required status.

**Forgetting to publish after enabling instruments or changing the schedule.** The most common reason participants do not see a new task is that the project was not published after the change. Always publish after making instrument or schedule changes.

**Placing the baseline date field inside a MyCap-enabled instrument.** The baseline date field must be in a non-MyCap instrument. If it is placed in a MyCap-enabled instrument, the configuration will not work correctly.

---

# 11. Related Articles

- RC-MYCAP-01 — MyCap: Overview & Enabling
- RC-MYCAP-03 — Task Scheduling
- RC-MYCAP-07 — Advanced Features: FDL, MLM, and Survey Links
- RC-MYCAP-08 — Testing MyCap
- RC-AT-11 — Action Tags: Mobile App Action Tags
- RC-FD-01 — Form Design Overview
- RC-FD-02 — Online Designer
- RC-FD-03 — Data Dictionary

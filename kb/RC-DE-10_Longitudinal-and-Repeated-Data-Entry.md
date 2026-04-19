RC-DE-10

**Longitudinal & Repeated Data Entry**

| **Article ID** | RC-DE-10 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | REDCap projects with Longitudinal mode enabled; projects with repeated instruments or repeated events |
| **Prerequisite** | RC-DE-01 — Record Creation & the Record Home Page; RC-DE-02 — Basic Data Entry; RC-NAV-REC-02 — Longitudinal Mode & Arms; RC-NAV-REC-03 — Repeated Instruments & Events |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-DE-03 — Longitudinal Projects & DAGs; RC-DE-11 — Instrument Save Options; RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup; RC-NAV-REC-02 — Longitudinal Mode & Arms; RC-NAV-REC-03 — Repeated Instruments & Events |

---

# 1. Overview

This article covers the data entry workflows that are specific to longitudinal REDCap projects — projects with multiple timepoints (events), multiple arms, repeated instruments, or repeated events. It explains how to create records correctly in single- and multi-arm projects, how to navigate to the right event and instrument, how prefilled fields work, and how to add new instances of repeated instruments and events. For general data entry procedures that apply to all project types, see RC-DE-02 — Basic Data Entry. For an explanation of how longitudinal mode and arms affect the interface layout, see RC-NAV-REC-02 — Longitudinal Mode & Arms.

---

# 2. Key Concepts & Definitions

**Arm**

A top-level grouping in a longitudinal project. Arms define which events a record participates in. A record belongs to exactly one arm at a time — it cannot be assigned to multiple arms simultaneously. Arms are typically used to separate distinct study populations or intervention paths (e.g., an intervention arm and a control arm).

**Event**

A named timepoint within an arm. Events define when instruments are collected. The same instrument can be assigned to multiple events (e.g., a Vital Signs instrument at Baseline, Week 4, and Month 6). Each event maintains its own independent copy of that instrument's data.

**Instance**

A single occurrence of a repeated instrument or repeated event. When an instrument or event is configured to repeat, each time it is filled out is called an instance. Instances are numbered sequentially (instance 1, instance 2, etc.) and are independent of each other.

**Prefilled Field**

A field that REDCap automatically populates with data from a previous event or a previous instance of the same instrument. Prefills are generated the moment you open an instrument — they are not saved to the database until you explicitly save the instrument.

**Form Status**

A required field at the bottom of every REDCap instrument that indicates the completion state of that instrument. Options are Incomplete, Unverified, and Complete. In longitudinal projects with many instruments and events, consistent use of form status is essential for tracking what has been collected and what remains outstanding.

---

# 3. Record Creation in Longitudinal Projects

In non-longitudinal projects, creating a new record takes you directly into the first instrument. In longitudinal projects, record creation works differently depending on whether the project has one arm or multiple arms.

## 3.1 Single-Arm Projects

Creating a record in a single-arm longitudinal project uses the same Add/Edit Records page as a non-longitudinal project — click **Add New Record**. The key difference is what happens next: instead of opening the first instrument directly, REDCap takes you to the **Record Home Page** for that record.

> **Important:** A newly created record is not permanently saved until at least one instrument has been saved with data. If you navigate away from the Record Home Page without saving any instrument, REDCap discards the record.

## 3.2 Multi-Arm Projects

When a project has more than one arm, you must specify which arm the record belongs to before creating it. REDCap cannot assign a record to an arm automatically because a record can only exist in one arm at a time.

1. Go to the **Add/Edit Records** page.
2. Use the arm dropdown to select the arm in which you want to create the record.
3. Click **Add New Record for the Arm Selected Above**.

REDCap creates the record and takes you to the Record Home Page, scoped to the selected arm. As with single-arm projects, the record is not permanent until at least one instrument is saved.

> **Note:** If you need to move a record to a different arm after it has been created, that requires a REDCap administrator. Data entry users cannot reassign records between arms.

## 3.3 Creating Records via Public Survey Links

When using public survey links to collect records from participants, each arm in a longitudinal project has its own unique public survey link. In a single-arm project this is functionally identical to a non-longitudinal project. In a multi-arm project, you must distribute the correct link for each arm to the corresponding participants.

Distributing the wrong public survey link will route a participant's response into the unintended arm. There is no automatic safeguard against this — the correct link must be shared deliberately.

---

# 4. Entering Data in Longitudinal Events

## 4.1 Navigating to an Event and Instrument

The Record Home Page displays a grid when longitudinal mode is active. Each column is an event; each row is an instrument. Click any cell in the grid (represented as a colored dot) to open that specific instrument at that specific event.

The instrument opens in the context of the selected event. To enter data for the same instrument at a different event, return to the Record Home Page and click the dot in the desired event's column. Data entered in one event does not affect the same instrument in another event.

## 4.2 Prefilled Fields

Some projects use advanced configuration to carry over data from a previous event into a later event. A common example is a medication list: rather than re-entering every medication at each visit, REDCap pre-populates the list from the previous event, allowing the data entry person to adjust for any changes.

Two important behaviors to know:

- Prefills are generated at the moment you **open** the instrument. If relevant data was entered in an earlier event after you already opened the current instrument, those prefills will not appear — you would need to close and reopen the instrument.
- Prefilled values are **not saved** until you explicitly save the instrument. Opening an instrument and seeing prefilled data does not write anything to the database.

## 4.3 Form Status Best Practices

Every instrument has a Form Status field at the bottom. In simple, non-longitudinal projects, form status is sometimes treated as optional. In longitudinal projects — where the same instrument appears across multiple events and many records — form status becomes a practical necessity.

Setting form status accurately at each event allows project staff to use the Record Status Dashboard to quickly identify which instrument-event combinations are complete, which are partially done, and which have not been started. Neglecting form status in a longitudinal project makes it significantly harder to track data collection progress.

Best practice: set form status before saving every instrument. Use **Complete** only when all required data has been entered and verified; use **Unverified** for data that has been entered but not yet reviewed.

---

# 5. Working with Repeated Instruments

When an instrument is configured as a repeated instrument, it can be filled out multiple times within the same event. Each occurrence is an instance.

## 5.1 Adding a New Instance

After an instrument's first instance has been saved, REDCap provides several ways to add another instance. All of the following create a new blank (or prefilled) instance of the repeated instrument:

| **UI Location** | **Control** | **When It Appears** |
|---|---|---|
| Record Home Page | **+** icon in the instrument's cell | Always visible for repeated instruments |
| Record Status Dashboard | **+** icon in the instrument's cell | Always visible for repeated instruments |
| Data Collection menu | **+** icon next to the instrument name | Always visible for repeated instruments |
| Within the instrument | **+ Add New** button | In the instance selector dropdown and near the instrument header |
| Within the instrument | **Save & Add New Instance** button | At the bottom of the instrument; see RC-DE-11 for all save options |

> **Note:** The **+** icon and the **+ Add New** button are functionally identical — they differ only by the amount of screen space available in that location.

## 5.2 Prefilled Fields in Repeated Instruments

Just as events can prefill from a previous event, instances of a repeated instrument can prefill from the previous instance. A common use case is tracking a configuration that changes incrementally — rather than re-entering every setting, REDCap pre-populates from the prior instance and the data entry person records only what changed.

The same rules apply as for event prefills: prefills are generated when the instance is opened, and the values are not saved until the instrument is explicitly saved.

---

# 6. Working with Repeated Events

When an event is configured to repeat, the entire event — including all instruments assigned to it — can be collected multiple times for the same record.

## 6.1 Adding a New Event Instance

There is only one location in REDCap where you can add a new instance of a repeated event: the **Record Home Page**.

1. On the Record Home Page, locate the column for the repeating event.
2. Click the **+ Add New** button in that event's column header.

REDCap creates a new instance of the event, which includes a new instance of every instrument assigned to that event. As with record creation, the new event instance is not permanently saved until at least one instrument within it has been saved.

> **Note:** You cannot add a new repeated event instance from within an instrument. Save your current work and return to the Record Home Page to add the new instance.

## 6.2 Prefilled Fields in Repeated Events

Repeated events support the same prefill behavior as regular events: fields can be pre-populated from a previous instance of the event or from a different event entirely. The mechanics are identical — prefills appear when the instrument is opened and are not written to the database until the instrument is saved.

---

# 7. Common Questions

**Q: I created a new record in a longitudinal project, but it disappeared. What happened?**

**A:** A new record is not permanently saved until at least one instrument within it has been saved with data. If you navigate away from the Record Home Page before saving any instrument, REDCap discards the record. Always save at least one instrument immediately after creating a new record.

**Q: I need to enter data for a participant who belongs in a different arm than the one I selected. Can I switch the arm?**

**A:** No — data entry users cannot reassign a record to a different arm. A record can only exist in one arm at a time, and changing arm assignment requires a REDCap administrator. Contact your project administrator to have the arm corrected.

**Q: I opened an instrument and saw prefilled values, but I didn't save it. Were those values recorded?**

**A:** No. Prefilled values are generated when the instrument opens but are only written to the database when you save the instrument. Opening and closing without saving leaves no trace of the prefilled data.

**Q: How do I know whether a repeated instrument needs a new instance or if I should edit an existing one?**

**A:** Check the instance selector dropdown at the top of the instrument. If an instance already exists for the data you are about to enter (e.g., today's visit), edit that instance. If this is a genuinely new occurrence (e.g., a new adverse event), add a new instance. When in doubt, ask your project coordinator — adding extra instances creates data that is difficult to remove.

**Q: I distributed public survey links to participants in a two-arm study, but all new records are going to one arm. Why?**

**A:** Each arm in a longitudinal project has a distinct public survey link. If all records are landing in one arm, participants are likely all using that arm's link. Verify that you distributed the correct link for each arm to the corresponding participant group.

**Q: Can the same record appear in multiple arms?**

**A:** No. REDCap stores data in a way that prevents a record from existing in more than one arm simultaneously. Arm assignment is a fundamental attribute of the record, not of individual events.

**Q: Can I add a new repeated event instance from inside an instrument?**

**A:** No. Repeated event instances can only be added from the Record Home Page by clicking the **+ Add New** button in the event's column header. Save your current instrument first, then return to the Record Home Page.

---

# 8. Common Mistakes & Gotchas

**Creating a record and navigating away before saving any instrument.** REDCap does not save a new longitudinal record until at least one of its instruments has been saved. Clicking away immediately after creating the record causes it to be silently discarded. Make it a habit to open and save the first instrument before leaving the Record Home Page.

**Distributing the wrong public survey link in a multi-arm project.** Each arm generates a unique public survey link. Using only one link for all participants routes every response into the same arm, regardless of the intended arm. Double-check arm-to-link assignments before distributing survey links to participants.

**Adding an extra repeated instrument instance instead of editing an existing one.** Each click of the **+** or **+ Add New** button creates a new, separate instance. If data for a visit was already partially entered in instance 3, creating instance 4 to add more data for the same visit results in split records that are hard to reconcile. Always verify which instance you are editing before creating a new one.

**Assuming prefilled values are saved without saving the instrument.** Prefills appear immediately when an instrument opens, which can create the impression that data has been captured. It has not. Closing the instrument without saving discards all prefilled values. Explicitly save every instrument after reviewing and adjusting prefilled data.

**Forgetting that repeated event instances must be added from the Record Home Page.** Users sometimes look for an "Add New Event" button inside an instrument or in the Data Collection menu and assume the feature is unavailable or broken. The only place to add a new repeated event instance is the Record Home Page, in the column header of the repeating event.

---

# 9. Related Articles

- RC-DE-01 — Record Creation & the Record Home Page (prerequisite — record creation basics and Record Home Page layout)
- RC-DE-02 — Basic Data Entry (prerequisite — general data entry workflow)
- RC-DE-03 — Longitudinal Projects & DAGs (how longitudinal mode and DAGs change the interface)
- RC-DE-11 — Instrument Save Options (all save button variants, including instance-specific options)
- RC-NAV-REC-02 — Longitudinal Mode & Arms (prerequisite — how arms and events are structured and navigated)
- RC-NAV-REC-03 — Repeated Instruments & Events (prerequisite — how repeated instruments and events appear in the interface)
- RC-LONG-01 — Longitudinal Project Setup (how longitudinal mode, arms, and events are configured)
- RC-LONG-02 — Repeated Instruments & Events Setup (how repeated instruments and events are configured)

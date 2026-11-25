---
id: RC-DE-10
title: Longitudinal & Repeated Data Entry
domain: Data Entry
applies_to:
- REDCap projects with Longitudinal mode enabled
- projects with repeated instruments or repeated events
requires: Any supported version
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — longitudinal
  and repeating data entry behaviour checked against source code; pages not re-captured
prerequisites:
- RC-DE-01 — Record Creation & the Record Home Page
- RC-DE-02 — Basic Data Entry
- RC-NAV-REC-02 — Longitudinal Mode & Arms
- RC-NAV-REC-03 — Repeated Instruments & Repeated Events
version: '1.1'
last_updated: 2026-11
related:
- id: RC-DE-03
  title: Longitudinal Projects & DAGs
- id: RC-DE-11
  title: Instrument Save Options
- id: RC-LONG-01
  title: Longitudinal Project Setup
- id: RC-LONG-02
  title: Repeated Instruments & Events Setup
- id: RC-NAV-REC-02
  title: Longitudinal Mode & Arms
- id: RC-NAV-REC-03
  title: Repeated Instruments & Repeated Events
tags:
- data entry
synonyms:
- how do i enter data for multiple events
- add another instance of a repeating instrument
- enter data across longitudinal events
- repeat an instrument or event during data entry
- fill out the same form multiple times
- data entry for repeated instruments and events
- add a new visit or timepoint of data
- longitudinal repeated measures data entry
---

# 1. Overview

This article covers the data entry workflows that are specific to longitudinal REDCap projects — projects with multiple timepoints (events), multiple arms, repeated instruments, or repeated events. It explains how to create records correctly in single- and multi-arm projects, how to navigate to the right event and instrument, how prefilled fields work, and how to add new instances of repeated instruments and events. For general data entry procedures that apply to all project types, see [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md). For an explanation of how longitudinal mode and arms affect the interface layout, see [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md).

---

# 2. Key Concepts & Definitions

**Arm**

A top-level grouping in a longitudinal project. Arms define which events a record participates in. Each record ID should exist in only one arm (see Section 3.2 for why). Arms are typically used to separate distinct study populations or intervention paths (e.g., an intervention arm and a control arm).

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

Creating a new record takes you directly into an instrument only when there is just one place to go: a non-longitudinal project with a single instrument, or a longitudinal arm with one event and one instrument. In every other case — including non-longitudinal projects with several instruments — REDCap opens the **Record Home Page** for the new record. In longitudinal projects, record creation also depends on whether the project has one arm or multiple arms.

## 3.1 Single-Arm Projects

Creating a record in a single-arm longitudinal project uses the same Add/Edit Records page as a non-longitudinal project — click **Add New Record**. REDCap takes you to the **Record Home Page** for that record, where you pick the event and instrument.

> **Important:** A newly created record is not permanently saved until at least one instrument has been saved with data. If you navigate away from the Record Home Page without saving any instrument, REDCap discards the record.

## 3.2 Multi-Arm Projects

When a project has more than one arm, a record's arm is decided by where it is created: the arm selected on Add/Edit Records, the arm whose public survey link the participant used, or the arm whose events the data was imported into. REDCap has no other way to know which cohort a participant belongs to, so check the arm before creating the record.

1. Go to the **Add/Edit Records** page.
2. Check the arm dropdown and select the arm in which you want to create the record. An arm is always preselected, so do not assume the default is right.
3. Click **Add New Record for the Arm Selected Above**.

REDCap creates the record and takes you to the Record Home Page, scoped to the selected arm. As with single-arm projects, the record is not permanent until at least one instrument is saved.

> **Version caveat (LTS 16):** Add/Edit Records always preselects Arm 1. From 17.x (LTS 17.3 and later, and Standard) it remembers the arm you last used. On LTS 16, select the arm every time before clicking **Add New Record**.

With auto-numbering on, the next record ID is the highest ID across all arms plus 1, so auto-numbering never reuses an ID that already exists in another arm.

> **Important:** Each record ID should exist in only one arm. REDCap does not strictly stop the same record ID from having data in more than one arm — it can happen through a data import, or by typing an existing record ID while another arm is selected — but this leads to confusing behaviour: the Record Home Page notes that the record "also exists on another arm", and **Rename Record** and **Delete Record** act only on the arm you are viewing. Keep each record in one arm.

**Moving a record to a different arm.** There is no move feature, for administrators either. Export the record's data first, then:

1. Enter the record's data in the new arm — either by a data import into that arm's events, or (when auto-numbering is off) by entering the same record ID on Add/Edit Records with the new arm selected.
2. Check that the data in the new arm is complete and correct.
3. Open the record in the old arm and use **Delete Record**, which deletes only that arm's data.

This needs the **Create Records** or **Data Import Tool** right, plus the **Delete Records** right. If you do not have these rights, ask a project member who does.

## 3.3 Creating Records via Public Survey Links

When using public survey links to collect records from participants, each arm in a longitudinal project has its own unique public survey link. In a single-arm project this is functionally identical to a non-longitudinal project. In a multi-arm project, you must distribute the correct link for each arm to the corresponding participants.

Distributing the wrong public survey link will route a participant's response into the unintended arm. There is no automatic safeguard against this — the correct link must be shared deliberately.

---

# 4. Entering Data in Longitudinal Events

## 4.1 Navigating to an Event and Instrument

The Record Home Page displays a grid when longitudinal mode is active. Each column is an event; each row is an instrument. Click any cell in the grid (represented as a colored dot) to open that specific instrument at that specific event.

The instrument opens in the context of the selected event. To enter data for the same instrument at a different event, return to the Record Home Page and click the dot in the desired event's column. Data entered in one event does not affect the same instrument in another event.

The save options at the bottom of the instrument vary: **Save & Go To Next Form** is not shown on the last instrument of an event, and **Save & Mark Survey as Complete** appears only for users with the right to edit survey responses. See [RC-DE-11 — Instrument Save Options](RC-DE-11_Instrument-Save-Options.md).

## 4.2 Prefilled Fields

Some projects use advanced configuration to carry over data from a previous event into a later event. A common example is a medication list: rather than re-entering every medication at each visit, REDCap pre-populates the list from the previous event, allowing the data entry person to adjust for any changes.

Two important behaviors to know:

- Prefills are generated at the moment you **open** the instrument. If relevant data was entered in an earlier event after you already opened the current instrument, those prefills will not appear — you would need to close and reopen the instrument.
- Prefilled values are **not saved** until you explicitly save the instrument. Opening an instrument and seeing prefilled data does not write anything to the database.

## 4.3 Form Status Best Practices

Every instrument has a Form Status field at the bottom. In simple, non-longitudinal projects, form status is sometimes treated as optional. In longitudinal projects — where the same instrument appears across multiple events and many records — form status becomes a practical necessity.

Setting form status accurately at each event allows project staff to use the Record Status Dashboard to quickly identify which instrument-event combinations are complete, which are partially done, and which have not been started. Neglecting form status in a longitudinal project makes it significantly harder to track data collection progress.

Best practice: set form status before saving every instrument. Use **Complete** only when all required data has been entered and verified; use **Unverified** for data that has been entered but not yet reviewed.

## 4.4 Deleting Event Data or a Record

- **One event (or one instance of a repeating event):** on the Record Home Page, an event column that has data offers a delete option for that event's data. It is available only to users with the **Delete Records** right, and not when the record is locked.
- **The whole record:** **Delete Record** on the Record Home Page deletes the record's data in the current arm only.

Deleted data cannot be recovered from the interface — export it first if you may need it.

---

# 5. Working with Repeated Instruments

When an instrument is configured as a repeated instrument, it can be filled out multiple times within the same event. Each occurrence is an instance.

## 5.1 Adding a New Instance

After an instrument's first instance has been saved, REDCap provides several ways to add another instance. All of the following create a new blank (or prefilled) instance of the repeated instrument:

| **UI Location** | **Control** | **When It Appears** |
|---|---|---|
| Record Home Page | **+** icon in the instrument's cell, and **+ Add new** in the instrument's table of instances | For repeated instruments, unless Form Display Logic hides the instrument |
| Record Status Dashboard | **+** icon in the instrument's cell | For repeated instruments; disabled when Form Display Logic hides the instrument (see caveat below) |
| Data Collection menu (left menu, while in a record) | **+** icon next to the instrument name | For repeated instruments, unless Form Display Logic hides the instrument |
| Within the instrument | **Save & Add New Instance** button | At the bottom of a repeating instrument, when you are on the latest or a new instance; on an earlier instance the button is **Save & Go To Next Instance** instead. See [RC-DE-11 — Instrument Save Options](RC-DE-11_Instrument-Save-Options.md) |

> **Note:** The **+** icon and the **+ Add new** link do the same thing. The instance selector inside the instrument is for moving between existing instances; it has no add button.

> **Version caveat (LTS 16):** on LTS 16 the Record Status Dashboard **+** ignores Form Display Logic, so it can add an instance the Record Home Page would not offer. From 17.x (LTS 17.3 and later, and Standard) it respects Form Display Logic. On LTS 16, add instances from the Record Home Page if your project uses Form Display Logic.

> **Version caveat (17.6 Standard):** Instance Embedding lets a designer embed a repeating instrument's table of instances in another instrument, with its own **Add new** button. It is not in LTS 17.3 or 16; on those versions use the controls in the table above.

## 5.2 Prefilled Fields in Repeated Instruments

Just as events can prefill from a previous event, instances of a repeated instrument can prefill from the previous instance. A common use case is tracking a configuration that changes incrementally — rather than re-entering every setting, REDCap pre-populates from the prior instance and the data entry person records only what changed.

The same rules apply as for event prefills: prefills are generated when the instance is opened, and the values are not saved until the instrument is explicitly saved.

---

# 6. Working with Repeated Events

When an event is configured to repeat, the entire event — including all instruments assigned to it — can be collected multiple times for the same record.

## 6.1 Adding a New Event Instance

There is only one location in REDCap where you can add a new instance of a repeated event: the **Record Home Page**.

1. On the Record Home Page, locate the column for the repeating event.
2. Click the **+ Add New** button in the column header of the event's latest instance. The button appears only on the latest instance and is disabled until the event has some saved data.

REDCap opens a new instance of the event, which includes a new instance of every instrument assigned to that event. Nothing is saved until you save an instrument within it.

> **Note:** You cannot add a new repeated event instance from within an instrument. Save your current work and return to the Record Home Page to add the new instance.

## 6.2 Prefilled Fields in Repeated Events

Repeated events support the same prefill behavior as regular events: fields can be pre-populated from a previous instance of the event or from a different event entirely. The mechanics are identical — prefills appear when the instrument is opened and are not written to the database until the instrument is saved.

---

# 7. Common Questions

**Q: I created a new record in a longitudinal project, but it disappeared. What happened?**

**A:** A new record is not permanently saved until at least one instrument within it has been saved with data. If you navigate away from the Record Home Page before saving any instrument, REDCap discards the record. Always save at least one instrument immediately after creating a new record.

**Q: I need to enter data for a participant who belongs in a different arm than the one I selected. Can I switch the arm?**

**A:** There is no switch or move feature, for administrators either. Move the record instead: export its data, enter the data in the correct arm (by data import into that arm's events, or by entering the same record ID with that arm selected when auto-numbering is off), check it, then use **Delete Record** in the wrong arm, which deletes only that arm's data. This needs the **Create Records** or **Data Import Tool** right and the **Delete Records** right. See Section 3.2.

**Q: I opened an instrument and saw prefilled values, but I didn't save it. Were those values recorded?**

**A:** No. Prefilled values are generated when the instrument opens but are only written to the database when you save the instrument. Opening and closing without saving leaves no trace of the prefilled data.

**Q: How do I know whether a repeated instrument needs a new instance or if I should edit an existing one?**

**A:** Check the instance selector dropdown at the top of the instrument. If an instance already exists for the data you are about to enter (e.g., today's visit), edit that instance. If this is a genuinely new occurrence (e.g., a new adverse event), add a new instance. When in doubt, ask your project coordinator — adding extra instances creates data that is difficult to remove.

**Q: I distributed public survey links to participants in a two-arm study, but all new records are going to one arm. Why?**

**A:** Each arm in a longitudinal project has a distinct public survey link. If all records are landing in one arm, participants are likely all using that arm's link. Verify that you distributed the correct link for each arm to the corresponding participant group.

**Q: Can the same record appear in multiple arms?**

**A:** It should not. REDCap does not strictly prevent the same record ID from having data in more than one arm (for example through a data import, or by typing an existing ID with another arm selected), but the result is confusing: the Record Home Page notes the record "also exists on another arm", and **Rename Record** and **Delete Record** act only on the current arm. Keep each record in one arm. Auto-numbering never creates the same ID in a second arm.

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

- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) (prerequisite — record creation basics and Record Home Page layout)
- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (prerequisite — general data entry workflow)
- [RC-DE-03 — Longitudinal Projects & DAGs](RC-DE-03_Longitudinal-Projects-and-DAGs.md) (how longitudinal mode and DAGs change the interface)
- [RC-DE-11 — Instrument Save Options](RC-DE-11_Instrument-Save-Options.md) (all save button variants, including instance-specific options)
- [RC-NAV-REC-02 — Longitudinal Mode & Arms](RC-NAV-REC-02_Longitudinal-Mode-and-Arms.md) (prerequisite — how arms and events are structured and navigated)
- [RC-NAV-REC-03 — Repeated Instruments & Repeated Events](RC-NAV-REC-03_Repeated-Instruments-and-Events.md) (prerequisite — how repeated instruments and events appear in the interface)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (how longitudinal mode, arms, and events are configured)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (how repeated instruments and events are configured)

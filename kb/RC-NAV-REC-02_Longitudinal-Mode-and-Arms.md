RC-NAV-REC-02

**Longitudinal Mode & Arms**

  ------------------ ------------------------------------------------
  **Article ID**     RC-NAV-REC-02
  **Domain**         Navigation
  **Applies To**     REDCap projects with Longitudinal mode enabled
  **Prerequisite**   RC-NAV-REC-01 --- Record Navigation Overview
  **Version**        1.0
  **Last Updated**   2025
  **Author**         REDCap Support
  ------------------ ------------------------------------------------

**1. Overview**

This article explains REDCap\'s Longitudinal mode and the concept of
Arms --- two features that allow data collection across multiple
timepoints and participant cohorts. It describes how these features
affect record navigation.

**2. Key Concepts & Definitions**

**Longitudinal Mode**

A project setting that enables data collection at multiple timepoints.
Instead of a single set of instruments, a longitudinal project defines
Events --- named timepoints (e.g., Baseline, Week 4, Month 6) --- and
assigns instruments to each event.

**Event**

A named timepoint within a longitudinal project. Each event can have any
subset of the project\'s instruments assigned to it. When viewing a
record, each event appears as a separate column on the Record Home Page.

**Arm**

A named collection of events within a longitudinal project. A project
can have multiple arms, each with a different set of events and
instrument assignments. A given record belongs to exactly one arm at a
time. Arms are typically used to separate participant cohorts (e.g.,
intervention group vs. placebo group).

**3. How Longitudinal Mode Affects Navigation**

**3.1 Record Home Page in a Longitudinal Project**

-   Instead of a single row of instrument dots, you see a grid: rows are
    instruments, columns are events.

-   Each dot represents a specific instrument within a specific event.

-   Click any dot to open that instrument for that event.

**3.2 Record Status Dashboard in a Longitudinal Project**

-   The dashboard displays the same grid layout --- rows are records,
    columns are events and instruments.

-   If the project has multiple arms, the dashboard adds a tab for each
    arm at the top of the page.

-   Click a tab to view records belonging to that arm.

**3.3 Add/Edit Records in a Project with Arms**

-   An additional dropdown appears at the top of the Add/Edit Records
    page asking you to select an arm.

-   You must choose an arm before looking up or adding a record.

-   Records can only be found within the arm they belong to.

**4. Step-by-Step: Working with Events and Arms**

**4.1 Navigating to a Record in a Specific Event**

-   Go to Add/Edit Records or the Record Status Dashboard.

-   If arms exist, select the appropriate arm first.

-   Select or search for the record.

-   On the Record Home Page, locate the column for the event you want.

-   Click the dot for the instrument within that event.

**4.2 Identifying Which Arm a Record Belongs To**

-   The Record Home Page header or the arm tab on the Record Status
    Dashboard indicates the active arm.

-   A record can only appear under one arm. If you cannot find a record
    in one arm, check another arm.

**5. Common Questions**

**Q: What is the difference between an event and an arm?**

A: An event is a single timepoint (e.g., \'Baseline visit\'). An arm is
a collection of events that defines the overall study timeline for a
particular cohort. Multiple arms let you define different timelines for
different groups of participants.

**Q: Can a record move from one arm to another?**

A: Not typically during normal data entry. Arm assignment is usually set
when a record is created. Moving records between arms requires
administrative intervention.

**Q: Do all instruments appear in every event?**

A: No. The project designer assigns specific instruments to specific
events. An instrument only appears in the events it has been designated
for.

**Q: I cannot find a record in Add/Edit Records. What should I check?**

A: First confirm you have selected the correct arm from the dropdown.
Records only appear in the arm they belong to.

**6. Common Mistakes & Gotchas**

-   Looking for a record in the wrong arm: records are arm-specific. If
    the arm dropdown is set incorrectly, the record will not appear in
    the search results.

-   Expecting all instruments in every event: instruments are assigned
    to events individually. An instrument that is not assigned to a
    given event will not appear in that event\'s column.

-   Confusing events with arms: events are timepoints within a study
    timeline; arms are parallel timelines for different cohorts. These
    are related but distinct concepts.

**7. Related Articles**

-   RC-NAV-REC-01 --- Record Navigation Overview

-   RC-NAV-REC-03 --- Repeated Instruments & Repeated Events

-   RC-NAV-REC-04 --- Record Status Dashboard & Other Record Links

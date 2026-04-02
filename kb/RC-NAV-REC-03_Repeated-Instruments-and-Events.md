RC-NAV-REC-03

**Repeated Instruments & Repeated Events**

  ------------------ --------------------------------------------------------------
  **Article ID**     RC-NAV-REC-03
  **Domain**         Navigation
  **Applies To**     REDCap projects with repeated instruments or repeated events
  **Prerequisite**   RC-NAV-REC-01 --- Record Navigation Overview
  **Version**        1.0
  **Last Updated**   2025
  **Author**         REDCap Support
  ------------------ --------------------------------------------------------------

**1. Overview**

This article explains how REDCap handles instruments and events that can
be filled out multiple times for the same record. It covers the visual
indicators for repeated entries and how to navigate between them.

**2. Key Concepts & Definitions**

**Repeated Instrument**

An instrument configured to allow multiple independent entries per
record (or per event, in longitudinal projects). The number of entries
is not fixed --- it grows as data is added. Common use cases include
lists of medications, adverse events, family members, or comorbidities.

**Repeated Event**

In a longitudinal project, an entire event can be made repeatable. This
is useful when the number of timepoints is not known upfront (e.g., a
variable number of chemotherapy cycles). Each repetition of the event
adds a new column on the Record Home Page.

**Stacked Dot**

A visual indicator shown when a repeated instrument has more than one
entry. Clicking a stacked dot opens a popup listing all entries with
their status dots, allowing direct navigation to any specific entry.

**Plus Symbol (+)**

Shown next to a repeated instrument that has at least one entry.
Clicking it adds a new repeated entry.

**Double Back Arrow**

Appears when a repeated event has been repeated three or more times.
Clicking it collapses the repeated-event columns to save horizontal
space.

**3. Visual Indicators for Repeated Instruments**

**3.1 Symbols at a Glance**

  ----------------------- -------------------------------------------------------------------------
  **Symbol**              **Meaning**
  Plus symbol (+)         Repeated instrument with at least one entry. Click to add a new entry.
  Stacked dot             Repeated instrument with more than one entry. Click to see all entries.
  Double back arrow       Repeated event with 3+ repetitions. Click to collapse the columns.
  Down arrow (on table)   Collapse the repeated instrument table on the Record Home Page.
  ----------------------- -------------------------------------------------------------------------

**3.2 Stacked Dot Color Codes**

The color of a stacked dot summarizes the statuses of all entries for
that repeated instrument:

  ----------------------- ---------------------------------------------------------------------------------------
  **Stacked Dot Color**   **Meaning**
  Red stacked dot         All entries are tagged as Incomplete.
  Yellow stacked dot      All entries are tagged as Unverified.
  Green stacked dot       All entries are tagged as Complete.
  Blue stacked dot        There is a mix of statuses across the entries (e.g., some complete, some incomplete).
  ----------------------- ---------------------------------------------------------------------------------------

  -------------------------------------------------------------------------------------------
  **Note:** A completed survey entry counts as Complete when determining stacked dot color.
  -------------------------------------------------------------------------------------------

**4. Step-by-Step: Navigating Repeated Instruments**

**4.1 Opening a Specific Repeated Entry**

-   Navigate to the Record Home Page for the record.

-   Locate the repeated instrument. If it has more than one entry, you
    will see a stacked dot.

-   Click the stacked dot to open the entry list popup.

-   In the popup, each entry is shown with its status dot. Click the dot
    for the entry you want to open.

**4.2 Adding a New Repeated Entry**

-   On the Record Home Page, find the repeated instrument.

-   Click the plus symbol (+) next to it to create a new entry.

-   Fill in the instrument and save.

**4.3 Using the Repeated Instrument Table**

-   On the Record Home Page, repeated instruments with at least one
    entry also display as a table below the main instrument grid.

-   The table lists all entries and provides direct links to each one.

-   Tables can be collapsed using the down arrow to reduce visual
    clutter when there are many entries.

**4.4 Navigating Repeated Events**

-   In a longitudinal project with repeated events, each repetition of
    the event appears as an additional column on the Record Home Page.

-   When there are three or more repetitions, a double back arrow
    appears. Click it to collapse those columns.

-   Click any dot within a repeated event column to open that instrument
    instance.

**5. Combining Repeated Instruments and Longitudinal Mode**

Repeated instruments and longitudinal mode can be combined in several
ways:

  ----------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------
  **Combination**                                                               **Effect on Navigation**
  Repeated instrument in a single event                                         Stacked dot appears in that event\'s column on the Record Home Page.
  Same repeated instrument in multiple events                                   Stacked dot appears independently in each designated event\'s column.
  Entire event made repeatable                                                  New columns appear for each repetition of the event. Double back arrow available at 3+ repetitions.
  Repeated instrument within a non-repeated event + a separate repeated event   Both behaviors appear simultaneously. Stacked dots and repeated event columns are shown together.
  ----------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Important:** A repeated instrument and a repeated event are mutually exclusive within the same event. You cannot have a repeated instrument inside a repeated event. Either the entire event repeats, or individual instruments within a non-repeated event repeat --- but not both at once.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Questions**

**Q: How do I know how many entries a repeated instrument has without
clicking the stacked dot?**

A: The stacked dot itself indicates there are multiple entries, but the
exact count is only visible after clicking it to open the popup list.

**Q: What does a blue stacked dot mean?**

A: It means there is a mix of form statuses across the repeated entries
--- for example, some entries are marked Complete while others are still
Incomplete or Unverified.

**Q: Can repeated instruments be used as surveys?**

A: Yes. Individual entries of a repeated instrument can be filled out as
surveys. A completed survey entry counts as a complete form for the
purpose of the stacked dot color.

**Q: Can I have a repeated instrument inside a repeated event?**

A: No. These two features are mutually exclusive. An event is either
repeatable as a whole, or its instruments are repeatable independently
--- not both.

**Q: The Record Home Page is very wide and hard to read. What can I
do?**

A: Use the double back arrow to collapse repeated event columns. Also
consider asking your project designer to set up a custom Record Status
Dashboard that filters or groups the view.

**7. Common Mistakes & Gotchas**

-   Confusing the plus symbol and the stacked dot: the plus adds a new
    entry; the stacked dot opens the list of existing entries. They are
    different controls and are displayed in different positions.

-   Missing entries because the repeated instrument table is collapsed:
    if someone previously collapsed the table, entries are still there
    but hidden. Click the down arrow (now pointing right) to expand it.

-   Expecting repeated instruments inside a repeated event: this
    configuration is not supported. If you see a stacked dot, the event
    itself is not repeatable.

-   Assuming a blue stacked dot means an error: blue only means mixed
    statuses. It is not an error indicator.

**8. Related Articles**

-   RC-NAV-REC-01 --- Record Navigation Overview

-   RC-NAV-REC-02 --- Longitudinal Mode & Arms

-   RC-NAV-REC-04 --- Record Status Dashboard & Other Record Links

RC-DE-11

**Instrument Save Options**

| **Article ID** | RC-DE-11 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; some options appear only in longitudinal projects or projects with repeated instruments |
| **Prerequisite** | RC-DE-02 — Basic Data Entry |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-DE-01 — Record Creation & the Record Home Page; RC-DE-10 — Longitudinal & Repeated Data Entry; RC-SURV-01 — Surveys: Basics |

---

# 1. Overview

This article documents every save button available in REDCap instruments — what each option does, where it appears, and under what conditions it is available. Most save options are available in all project types; a few appear only in longitudinal projects or projects with repeated instruments. The article also covers Edit Survey Mode, which controls how survey-completed instruments are edited by staff. Understanding save options prevents navigation mistakes and helps data entry staff move efficiently between instruments, events, and records.

---

# 2. Key Concepts & Definitions

**Save Button**

A control at the bottom of a REDCap instrument (or in the floating menu at the top right of the window) that writes the currently entered data to the database. Clicking a save button is the only way to permanently record data in an instrument — closing or navigating away without saving discards any unsaved changes.

**Floating Save Menu**

A condensed set of save controls that appears in the top-right corner of the instrument window as the user scrolls down. It duplicates the save options available at the bottom of the instrument so that users do not need to scroll to the bottom to save.

**Edit Survey Mode**

A mode that allows REDCap staff users to modify data in an instrument that was filled out and submitted as a survey. Survey responses are locked by default after submission; Edit Survey Mode unlocks them for editing.

**Instance**

A single occurrence of a repeated instrument. Instruments configured to repeat can have multiple instances per event per record. Instance-specific save options allow navigation directly between instances without returning to the Record Home Page.

---

# 3. Save Button Locations

Save buttons appear in two locations in most instruments:

1. **Floating menu** — fixed in the top-right corner of the screen; always visible while scrolling through a long instrument.
2. **Bottom of the instrument** — the full set of available save options, labeled with their complete names.

The exception is instruments that have been filled out as a survey. In that case, save buttons are hidden and the instrument is displayed in a read-only view. To modify a survey response, a staff user must first activate Edit Survey Mode (see Section 5).

---

# 4. Save Button Reference

The table below lists every save option, what it does after saving, and when it is available.

| **Save Option** | **After Saving, Navigates To** | **Availability** |
|---|---|---|
| Save & Exit Form | Record Home Page of the current record | Always available |
| Save & Go To Next Form | The next instrument in the current event | Available when there is a next instrument in the event; not shown for the last instrument in an event |
| Save & Stay | Stays on the current instrument (page reloads) | Always available |
| Save & Exit Record | The Add/Edit Records page | Always available |
| Save & Go To Next Record | Record Home Page of the next record; returns to Add/Edit Records if on the last record | Always available; in longitudinal projects, navigates to the next record in the same arm |
| Save & Mark Survey as Complete | Record Home Page of the current record | Only when editing a survey instrument (instrument is survey-enabled and accessed in Edit Survey Mode, or partially completed survey) |
| Save & Go To Next Instance | The next instance of the current repeated instrument | Only when editing a non-final existing instance of a repeated instrument (e.g., viewing instance 5 of 10) |
| Save & Add New Instance | A newly created next instance of the current repeated instrument | Only when editing the last instance of a repeated instrument |
| Cancel | Record Home Page of the current record (no data saved) | Always available |

---

# 5. Edit Survey Mode

When an instrument is enabled as a survey and a participant has submitted it, the instrument displays as read-only to staff users. A colored box appears at the top of the instrument:

- **Green box** — the survey was submitted as complete.
- **Orange box** — the survey was partially completed (participant saved progress but did not submit).

To edit the response, click the **Edit Response** button inside the colored box. This activates Edit Survey Mode and allows the instrument's fields to be modified like a standard data entry form.

> **Note:** If the colored box does not have an **Edit Response** button, the current user does not have sufficient user rights to modify that survey instrument. Contact the project administrator to request the appropriate permissions.

After making changes in Edit Survey Mode, use **Save & Mark Survey as Complete** to save the data and restore the instrument's completed survey status. Using a standard save option (such as Save & Exit Form) will save the data but may change the instrument's form status — verify the form status is set correctly before leaving.

---

# 6. Instance-Specific Save Options

Two save options appear exclusively when working with repeated instruments. They do not appear in non-repeated instruments, and they only appear under specific conditions even within repeated instruments.

**Save & Go To Next Instance** appears when you are editing an instance that is not the last instance in the series. For example, if a repeated instrument has 10 instances and you are editing instance 5, this option allows you to save and proceed directly to instance 6 without returning to the Record Home Page.

**Save & Add New Instance** appears when you are editing the last instance in a series. Clicking it saves your current work and creates a new blank (or prefilled) instance, opening it immediately. This is the most efficient way to add successive instances during active data collection.

> **Note:** There are no equivalent options for navigating between events (e.g., "Save & Go To Next Event") or for adding a new repeated event instance. To move to a different event or add a repeated event instance, save the current instrument and return to the Record Home Page.

---

# 7. Common Questions

**Q: What is the difference between Save & Exit Form and Save & Exit Record?**

**A:** Save & Exit Form takes you to the Record Home Page for the current record — you stay within the same record and can continue working on other instruments. Save & Exit Record takes you entirely out of the record to the Add/Edit Records page, where you would need to search for a record to continue working.

**Q: Why is Save & Go To Next Form not showing up?**

**A:** This option only appears when there is another instrument after the current one within the same event. If the current instrument is the last one in the event, this button is not shown. To move to a different event, return to the Record Home Page.

**Q: I need to go to the next event after saving. Is there a save option for that?**

**A:** No. REDCap does not have a "Save & Go To Next Event" option. Save the current instrument (Save & Exit Form works well), return to the Record Home Page, and click the appropriate event column to open the next event's instrument.

**Q: The Edit Response button is missing from the survey box at the top of the instrument. How do I edit the response?**

**A:** The absence of the Edit Response button means your user account does not have the right to edit that survey instrument. This is controlled by User Rights settings. Contact your project administrator to request the appropriate access.

**Q: I clicked Cancel by mistake. Did I lose my data?**

**A:** Yes, if you had unsaved changes. The Cancel button discards all changes made since the last save and returns you to the Record Home Page. There is no undo — previously saved data is intact, but anything entered in the current session that was not saved is gone.

**Q: When should I use Save & Stay instead of Save & Exit Form?**

**A:** Save & Stay is useful when you want to confirm data was saved without leaving the instrument — for example, when entering a long form in stages, or when waiting for additional information before completing the rest of the form.

**Q: What happens to the form status when I use Save & Mark Survey as Complete?**

**A:** The instrument is marked as a completed survey, which typically sets the form status to Complete. This also locks the instrument back to read-only view for future access, requiring Edit Survey Mode again if further edits are needed.

---

# 8. Common Mistakes & Gotchas

**Using Cancel instead of Save & Exit Form.** The Cancel button is positioned near the other save options and is easy to click accidentally, especially on smaller screens. Cancel discards all unsaved changes — there is no confirmation dialog. If you click Cancel in error, the only recovery is to re-enter the data.

**Expecting a "Save & Go To Next Event" button.** REDCap does not provide a way to save and jump directly to the next event. Users who look for this button and don't find it sometimes assume it's a permissions issue or a bug. It simply doesn't exist — saving and returning to the Record Home Page is the intended navigation path between events.

**Using a standard save option after editing a survey instead of Save & Mark Survey as Complete.** Saving with Save & Exit Form or Save & Stay after editing in Edit Survey Mode will store your changes, but may leave the instrument in a non-survey-complete state. This affects reporting and notifications that rely on survey completion status. Use Save & Mark Survey as Complete to preserve the survey's completed status.

**Clicking Save & Add New Instance when you meant to edit an existing one.** Each click of Save & Add New Instance creates a new instance. If the intent was to update data in the current instance and then stop, clicking this option produces an unnecessary empty instance that is difficult to delete. Review the instance navigation options before saving.

**Assuming floating save menu and bottom save buttons are always identical.** The floating menu is a condensed version and may not display every available option depending on screen size and context. When in doubt about which options are available, scroll to the bottom of the instrument to see the full set.

---

# 9. Related Articles

- RC-DE-02 — Basic Data Entry (prerequisite — general data entry workflow and instrument navigation)
- RC-DE-01 — Record Creation & the Record Home Page (prerequisite — understanding the Record Home Page)
- RC-DE-10 — Longitudinal & Repeated Data Entry (record creation in longitudinal projects; adding repeated instrument and event instances)
- RC-SURV-01 — Surveys: Basics (survey configuration and how surveys differ from standard data entry instruments)

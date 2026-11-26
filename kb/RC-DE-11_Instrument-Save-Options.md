

**Instrument Save Options**

| **Article ID** | [RC-DE-11 — Instrument Save Options](RC-DE-11_Instrument-Save-Options.md) |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; some options appear only in longitudinal projects or projects with repeated instruments |
| **Requires** | Any supported version |
| **Verified Against** | REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — save button behaviour checked against source code; pages not re-captured |
| **Prerequisite** | [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) |
| **Version** | 1.2 |
| **Last Updated** | 2026-11 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md); [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md); [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md)|
| **Synonyms** | what do the different save buttons do; save and continue versus save and exit; save and go to next instrument or record; which save option should i use; edit survey mode for staff; save button options on a redcap form; difference between save options data entry; save and stay on the same form |

---

## 1. Overview

This article documents every save button available in REDCap instruments — what each option does, where it appears, and under what conditions it is available. Most save options are available in all project types; a few appear only in longitudinal projects or projects with repeated instruments. The article also covers Edit Survey Mode, which controls how survey-completed instruments are edited by staff. Understanding save options prevents navigation mistakes and helps data entry staff move efficiently between instruments, events, and records.

---

## 2. Key Concepts & Definitions

**Save Button**

A control at the bottom of a REDCap instrument (or in the floating menu at the top right of the window) that writes the currently entered data to the database. Clicking a save button is the only way to permanently record data in an instrument — closing or navigating away without saving discards any unsaved changes (REDCap asks you to confirm before you leave a page with unsaved changes).

**Floating Save Menu**

A copy of the save controls that appears in the top-right corner of the instrument window, beside the form. It duplicates the full set of save options available at the bottom of the instrument so that users do not need to scroll to the bottom to save.

**Edit Survey Mode**

A mode that allows REDCap staff users to modify data in an instrument that was filled out and submitted as a survey. Survey responses are locked by default after submission; Edit Survey Mode unlocks them for editing.

**Instance**

A single occurrence of a repeated instrument. Instruments configured to repeat can have multiple instances per event per record. Instance-specific save options allow navigation directly between instances without returning to the Record Home Page.

---

## 3. Save Button Locations

Save buttons appear in two locations in most instruments:

1. **Floating menu** — a copy of the same save buttons, fixed in the top-right corner of the screen beside the form, so it stays visible while scrolling through a long instrument. On narrow windows and mobile screens the floating menu is hidden entirely; use the buttons at the bottom instead.
2. **Bottom of the instrument** — the full set of available save options.

In both locations, **Save & Exit Form** is the main button. The other options sit in a **Save & …** drop-down next to it. REDCap remembers the option you last chose from the drop-down and shows it as a second button, so a repeated action (for example, Save & Go To Next Record) is one click away.

Save buttons are not shown in these cases:

- **Survey responses** — an instrument filled out as a survey is displayed read-only. To modify the response, a staff user must first activate Edit Survey Mode (see Section 5).
- **Read-only access** — users with read-only rights to the instrument see only a disabled Cancel button.
- **Locked instruments** — a locked instrument cannot be saved until it is unlocked.
- **MyCap active tasks** — instruments used as MyCap active tasks are not edited through the data entry form.

---

## 4. Save Button Reference

The table below lists every save option, what it does after saving, and when it is available.

| **Save Option** | **After Saving, Navigates To** | **Availability** |
|---|---|---|
| Save & Exit Form | Record Home Page of the current record | Always available (the main button) |
| Save & Go To Next Form | The next instrument in the current event that you have access to (instruments you cannot open are skipped) | Available when there is a next instrument in the event; not shown for the last instrument in an event |
| Save & Stay | Stays on the current instrument (page reloads) | Always available |
| Save & Exit Record | The Add/Edit Records page | Always available |
| Save & Go To Next Record | Record Home Page of the next record (in your Data Access Group, if you are in one). On the last record: a new auto-numbered record if record auto-numbering is enabled; otherwise the record selection page with a message that there is no next record | Always available; in longitudinal projects, navigates to the next record in the same arm |
| Save & Mark Survey as Complete | Record Home Page of the current record; the form status is set to Complete | Only on a survey-enabled instrument whose response is not yet complete (a partial response being edited, or an invited participant who has not started), when editing survey responses is allowed on the server and the user has the right to edit survey responses. Never shown on e-Consent surveys |
| Save & Go To Next Instance | The next instance number (current + 1) of the current repeated instrument | When editing an existing instance of a repeated instrument that is not the last one (e.g., viewing instance 5 of 10) |
| Save & Add New Instance | A newly created next instance of the current repeated instrument | Only when editing the last instance of a repeated instrument |
| Cancel | Record Home Page of the current record (no data saved) | Always available; asks for confirmation if you changed anything |

---

## 4a. Version Caveats Affecting Form Status

Form status drives completion reporting, so a wrong status is a wrong number in every summary built on it.

> **Critical — required-field bypass left statuses in "limbo" (16.0.13 LTS / 16.1.1 Standard).** A defect in those releases let participants **submit a survey while bypassing one or more required fields**, and the resulting Form Status values ended up in a confused state. A repair shipped in 16.0.17 LTS to clean up the affected values. Two things follow: an exposure window where required fields were not actually enforced, and a set of statuses that were corrected after the fact. Completion figures drawn from a project that ran on those versions should be re-derived rather than trusted from memory.

> **Version caveat (below 15.0.21 Standard):** When a participant clicked **Start Over** on a survey, their responses were correctly erased **but the survey status remained "complete" or "partially complete"**. Any completion count taken from an affected version over-counts by the number of participants who restarted.

> **Version caveat (below 16.0.17 Standard):** A calc or CALCTEXT field referencing a **survey instrument's Form Status field** did not always retrigger when data was entered on that survey — so a calculation keyed to completion could remain stale.

> **Version caveat (below 16.0.14 Standard):** A survey submitted with empty required fields was not always redisplayed with the Required Fields warning, so the participant received no prompt to complete them.

---

## 5. Edit Survey Mode

When an instrument is enabled as a survey and a participant has submitted it, the instrument displays as read-only to staff users. A colored box appears at the top of the instrument:

- **Green box** — the survey was submitted as complete.
- **Orange box** — the survey was partially completed (participant saved progress but did not submit).

To edit the response, click the **Edit Response** button inside the colored box. This activates Edit Survey Mode and allows the instrument's fields to be modified like a standard data entry form.

> **Note:** If the colored box does not have an **Edit Response** button, the most common reason is that the current user does not have the user right to edit survey responses for that instrument. Other reasons: editing survey responses is turned off on the server, the instrument is a completed e-Consent survey, it is a PROMIS (adaptive) instrument, or another user currently has the form open. If it is a rights issue, contact the project administrator to request the appropriate permissions.

After making changes in Edit Survey Mode, save with any standard option (such as Save & Exit Form or Save & Stay). Saving a **completed** response does not clear its completion — the response stays a completed survey. **Save & Mark Survey as Complete** is not offered on a completed response; it appears only for a response that is not yet complete (see Section 4). Using it forces the form status to Complete and cancels any scheduled survey invitations for that survey that have not been sent yet.

---

## 6. Instance-Specific Save Options

Two save options appear exclusively when working with repeated instruments. They do not appear in non-repeated instruments, and they only appear under specific conditions even within repeated instruments.

**Save & Go To Next Instance** appears when you are editing an instance that is not the last instance in the series. For example, if a repeated instrument has 10 instances and you are editing instance 5, this option allows you to save and proceed directly to instance 6 without returning to the Record Home Page.

**Save & Add New Instance** appears when you are editing the last instance in a series. Clicking it saves your current work and creates a new blank (or prefilled) instance, opening it immediately. This is the most efficient way to add successive instances during active data collection.

Both options always go to the instance number one higher than the current one. If instance numbers have gaps (for example, instance 3 was deleted), Save & Go To Next Instance from instance 2 opens an empty instance 3 rather than skipping to instance 4.

> **Note:** There are no equivalent options for navigating between events (e.g., "Save & Go To Next Event") or for adding a new repeated event instance. To move to a different event or add a repeated event instance, save the current instrument and return to the Record Home Page.

---

## 7. Common Questions

**Q: What is the difference between Save & Exit Form and Save & Exit Record?**

**A:** Save & Exit Form takes you to the Record Home Page for the current record — you stay within the same record and can continue working on other instruments. Save & Exit Record takes you entirely out of the record to the Add/Edit Records page, where you would need to search for a record to continue working.

**Q: Why is Save & Go To Next Form not showing up?**

**A:** This option only appears when there is another instrument after the current one within the same event. If the current instrument is the last one in the event, this button is not shown. To move to a different event, return to the Record Home Page.

**Q: I need to go to the next event after saving. Is there a save option for that?**

**A:** No. REDCap does not have a "Save & Go To Next Event" option. Save the current instrument (Save & Exit Form works well), return to the Record Home Page, and click the appropriate event column to open the next event's instrument.

**Q: The Edit Response button is missing from the survey box at the top of the instrument. How do I edit the response?**

**A:** Usually it means your user account does not have the right to edit survey responses for that instrument. This is controlled by User Rights settings; contact your project administrator to request the appropriate access. The button is also missing when editing survey responses is turned off on the server, for completed e-Consent surveys, for PROMIS instruments, and while another user has the form open.

**Q: I clicked Cancel by mistake. Did I lose my data?**

**A:** Only if you confirmed. If you had changed anything, REDCap asks you to confirm before cancelling; choose to stay on the page and then save. If you confirm, all changes made since the last save are discarded and you return to the Record Home Page. There is no undo — previously saved data is intact, but anything entered in the current session that was not saved is gone.

**Q: When should I use Save & Stay instead of Save & Exit Form?**

**A:** Save & Stay is useful when you want to confirm data was saved without leaving the instrument — for example, when entering a long form in stages, or when waiting for additional information before completing the rest of the form.

**Q: What happens to the form status when I use Save & Mark Survey as Complete?**

**A:** The response is marked as a completed survey and the form status is set to Complete. Any scheduled invitations for that survey that have not been sent yet are cancelled. The instrument then shows read-only for future access, requiring Edit Survey Mode again if further edits are needed. The button is only offered while the response is not yet complete; once a response is complete, edits saved with a standard save option keep it complete.

---

## 8. Common Mistakes & Gotchas

**Using Cancel instead of Save & Exit Form.** The Cancel button is positioned near the other save options and is easy to click accidentally, especially on smaller screens. If you changed anything, REDCap asks for confirmation first — read that prompt rather than clicking through it. Once confirmed, Cancel discards all unsaved changes and the only recovery is to re-enter the data.

**Expecting a "Save & Go To Next Event" button.** REDCap does not provide a way to save and jump directly to the next event. Users who look for this button and don't find it sometimes assume it's a permissions issue or a bug. It simply doesn't exist — saving and returning to the Record Home Page is the intended navigation path between events.

**Looking for Save & Mark Survey as Complete on a completed response.** The button is not shown once a survey response is complete, and it is not needed: saving edits to a completed response with Save & Exit Form or Save & Stay keeps it a completed survey. The button matters for **partial** responses — saving a partial response with a standard option leaves it partial, which affects reporting and notifications that rely on survey completion. Use Save & Mark Survey as Complete only when the response should now count as complete.

**Clicking Save & Add New Instance when you meant to edit an existing one.** Each click of Save & Add New Instance creates a new instance. If the intent was to update data in the current instance and then stop, clicking this option produces an unnecessary empty instance that is difficult to delete. Review the instance navigation options before saving.

**Looking for the floating save menu on a small screen.** The floating menu carries the same buttons as the bottom of the instrument, but it is hidden entirely on narrow windows and mobile screens. If you do not see it, scroll to the bottom of the instrument to save.

---

## 9. Related Articles

- [RC-DE-02 — Basic Data Entry](RC-DE-02_Basic-Data-Entry.md) (prerequisite — general data entry workflow and instrument navigation)
- [RC-DE-01 — Record Creation & the Record Home Page](RC-DE-01_Record-Creation-and-Record-Home-Page.md) (prerequisite — understanding the Record Home Page)
- [RC-DE-10 — Longitudinal & Repeated Data Entry](RC-DE-10_Longitudinal-and-Repeated-Data-Entry.md) (record creation in longitudinal projects; adding repeated instrument and event instances)
- [RC-SURV-01 — Surveys – Basics](RC-SURV-01_Surveys-Basics.md) (survey configuration and how surveys differ from standard data entry instruments)

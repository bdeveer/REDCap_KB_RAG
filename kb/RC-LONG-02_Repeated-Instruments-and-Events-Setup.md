RC-LONG-02

**Repeated Instruments & Events Setup**

| **Article ID** | RC-LONG-02 |
|---|---|
| **Domain** | Longitudinal & Repeated Setup |
| **Applies To** | All REDCap project types (repeated instruments); longitudinal projects only (repeated events) |
| **Prerequisite** | RC-FD-01 — Form Design Overview; RC-LONG-01 — Longitudinal Project Setup (for longitudinal projects only) |
| **Version** | 1.3 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-LONG-01 — Longitudinal Project Setup; RC-NAV-REC-03 — Repeated Instruments & Repeated Events; RC-BL-01 — Branching Logic Overview & Scope |

---

# 1. Overview

This article explains how to configure repeatable instruments and repeatable events in REDCap — sometimes called **one-to-many data collection**, because a single record can have any number of repeated instances of an instrument or event. Repeated instruments allow a single instrument to be filled out multiple times per record (or per event, in longitudinal projects), creating numbered instances. Repeated events allow an entire event — with all its designated instruments — to be repeated as a group.

Repeated instruments can be used in both non-longitudinal and longitudinal projects. Repeated events require a longitudinal setup. The two modes cannot be combined within the same event: an event is either configured for repeated instruments or repeated as a whole, not both.

This article covers setup only. For how repeated instruments and events appear during data entry, see RC-NAV-REC-03 — Repeated Instruments & Repeated Events.

---

# 2. Key Concepts & Definitions

**One-to-Many Data Collection**

The pattern in which a single record can have multiple independent instances of an instrument or event. Unlike traditional longitudinal mode (where all events must be defined in advance), repeating instruments and events allow unlimited instances per record without pre-specifying a maximum. Each record can have a different number of instances — one record might have five medication entries while another has none.

**Repeated Instrument**

An instrument configured to allow multiple independent instances per record (or per event, in longitudinal projects). Each submission creates a new numbered instance. Instances within the same instrument are independent of each other.

**Repeated Event**

An event (with all its designated instruments) configured to be collected multiple times as a unit. All instruments within the event are repeated together, not independently.

**Instance**

A single numbered occurrence of a repeated instrument or repeated event. Instance 1 is the first submission, instance 2 is the second, and so on. Instance numbers are assigned sequentially and do not reset between events.

**Custom Label (Repeated)**

An optional text field that allows you to attach a descriptive label to each instance. Uses REDCap piping syntax to pull values from variables within the same instrument or event. Multiple variables can be combined with free text (e.g., `[version] - [change_type] - RC[redcap_version]` or `[visit_date], [weight] kg`). The label is populated dynamically from the instance's own data.

---

# 3. When to Use Repeated Instruments vs. Repeated Events

| | **Repeated Instruments** | **Repeated Events** |
|---|---|---|
| **Unit of repetition** | One instrument at a time, independently | All instruments in the event, together |
| **Instruments can repeat at different rates?** | Yes — Instrument A might have 3 instances while Instrument B has 5 | No — all instruments repeat as a unit |
| **Available in non-longitudinal projects?** | Yes | No |
| **Use case example** | A medication list instrument repeated once per medication | A chemotherapy cycle event repeated once per treatment cycle |

> **Non-longitudinal projects:** Repeating instruments are a lightweight alternative to enabling the full longitudinal module for projects that simply need to collect the same data multiple times per record. The key advantage over longitudinal mode is that you do not need to define the number of repetitions in advance — records can have any number of instances. If all you need is one-to-many data collection without distinct time points or arms, a non-longitudinal project with repeating instruments is simpler to set up and maintain.

**Rule:** Within a given event, you choose one mode — you cannot mix repeated instruments with a repeated event. If you need some instruments to repeat independently, use repeated instruments. If all instruments in the event always repeat together, use a repeated event.

> **Important:** You cannot nest repeated instruments inside a repeated event. REDCap does not support having a repeatable instrument within an already-repeatable event. You must choose one or the other.

---

# 4. Setting Up Repeated Instruments in a Non-Longitudinal Project

Non-longitudinal projects support repeated instruments only (not repeated events).

**Prerequisites:** Instruments must exist before they can be designated as repeatable.

**Steps:**

1. Navigate to **Project Setup**.
2. In the **Enable optional modules and customizations** section, locate the **Repeating instruments** option. Click **Enable** (or **Modify** if repeating instruments have been configured before).
3. A popup appears listing all instruments in the project.
4. Check the box next to each instrument you want to make repeatable.
5. Optionally, enter a **custom label** using piping syntax (e.g., `[medication_name]`) in the field next to the instrument name.
6. Click **Save**.

> **Tip:** Your instruments do not need to be fully built out before enabling them as repeatable. A placeholder instrument with a single variable is sufficient to proceed with this setup. You can add more variables later.

---

# 5. Setting Up Repeated Instruments & Events in a Longitudinal Project

Longitudinal projects support both repeated instruments and repeated events. The configuration is more granular: you designate a repeat mode per event, not per project.

**Prerequisites:** Instruments must exist and your longitudinal setup (arms, events, instrument designations) must be complete before configuring repeating instruments or events. REDCap cannot populate the repeating instrument/event menu correctly without a completed event structure.

**Steps:**

1. Navigate to **Project Setup**.
2. In the **Enable optional modules and customizations** section, locate the **Repeating instruments and events** option. Click **Enable** (or **Modify** if a configuration already exists).
3. A popup appears listing all defined events. For each event, choose one of three options (shown as radio buttons in the UI, in this order):

| **UI Label** | **Effect** |
|---|---|
| `-- not repeating --` | Default. Neither the event nor its instruments are repeatable. |
| `Repeat Entire Event (repeat all instruments together)` | The entire event repeats as a unit. All designated instruments repeat together and stay connected. Instruments cannot be repeated independently within a repeated event. |
| `Repeat Instruments (repeat independently)` | Selected instruments within this event repeat independently of each other. You must check which instruments in the event are repeatable. |

4. If you selected **Repeat Instruments** for an event, check the boxes for the specific instruments within that event that should be repeatable.
5. Optionally, enter a **custom label** for repeatable instruments in the text field next to the instrument name.
6. Click **Save**.

> **Tip:** Your longitudinal setup (arms, events, instrument designations) must be complete before configuring repeating instruments or events. If the event structure is incomplete, the popup will not display correctly.

> **No UI bulk import/export:** Unlike arms, events, and instrument-event designations — which support CSV upload and download from the Define My Events and Designate Instruments pages — the repeatable instrument and event configuration has no UI-based import or export option. To manage repeatable mappings programmatically (e.g., when setting up multiple projects with the same repeated structure), use the REDCap API. The API supports both exporting and importing the repeatable instruments and events configuration.

---

# 6. Custom Labels for Repeated Instruments & Events

Custom labels attach a descriptive tag to each instance, making it easier to identify specific instances during data entry (e.g., labeling a medication instance with the medication name rather than just "Instance 3").

**For repeated instruments:** Define the custom label in the repeating instrument/event configuration menu (the popup in Project Setup). Enter a piping expression in the custom label field next to the instrument's name.

**For repeated events:** The custom label field in the repeating instrument/event popup is greyed out for events configured as "Repeat entire event." Instead, define the custom event label in the **Define My Events** page using the **Custom Event Label** column — see RC-LONG-01 — Longitudinal Project Setup, Section 4.2.

Both locations use the same piping syntax. Custom labels support combining multiple piped variables with free text between them — for example, `[visit_date], [weight] kg` produces a label like "2026-03-15, 72 kg", and `[version] - [change_type] - RC[redcap_version]` produces a label like "2.1.0 - Bug fix - RC16.1". There is no limit on the number of variables or the amount of free text in the label.

One key constraint applies to both: the variables you pipe in must exist within the repeated instrument or repeated event itself. You cannot pipe a variable from a different instrument or event into a custom label.

> **Example:** If you want to display the visit date in a repeated event's label, the variable `[visit_date]` must be in an instrument designated to that same event. Piping in a date of birth from a baseline event into a follow-up event's custom label is not supported.

---

# 7. Modifying an Existing Repeated Setup

Changing repeating instrument or event configuration in a project that has already collected data carries significant risk. The following changes can cause data loss or break project logic:

- Making an instrument or event non-repeatable after instances have been saved
- Switching an event from "Repeat instruments" to "Repeat entire event" (or vice versa) when data exists
- Removing an instrument from the repeatable list when instances of that instrument exist
- Renaming an instrument that is referenced in logic within a repeated context

**Best practice:** Before making any changes to the repeated setup of an active project, clone the entire project and test the modification in the copy first. If you are unsure about the potential impact, consult your local REDCap administrator before making changes in Production.

> **Yale-specific:** Changes to repeating instrument or event configuration in a Production project may require administrator review. Contact Yale REDCap support before modifying the setup of an active production project.

---

# 8. Effects on Other REDCap Features

Configuring repeated instruments or events changes behavior in several other areas of REDCap.

## 8.1 Branching Logic

In standard projects, variables in repeated instruments can generally be referenced within the same instrument using local branching logic (no event prefix needed). However, you cannot reliably reference a variable from a repeated instrument or repeated event in logic that runs outside that repeated context.

REDCap provides a set of smart variables (e.g., `@current-instance`) to reference values within the same set of instances, but cross-instance and cross-event references from within a repeated instrument are not reliably supported. Do not design logic that depends on comparing values across multiple instances of a repeated instrument.

See RC-BL-01 — Branching Logic Overview & Scope for general branching logic guidance.

## 8.2 Piping

Piping follows the same rules as branching logic. Piping a value from within the same repeated instrument or event instance works reliably. Piping values from outside the repeated context (e.g., piping a baseline variable into a repeated event's label) is supported only for the custom label field and requires the variable to exist within the repeated instrument or event itself.

## 8.3 Reports & Data Exports

Each instance of a repeated instrument or event produces an additional row in reports and data exports. A record with 10 instances of a repeated medication instrument will generate 10 additional rows in any export that includes that instrument. REDCap adds the coordinate variable `redcap_repeat_instance` (and `redcap_repeat_instrument` for repeated instruments) to exports so that each row can be traced back to its specific instance.

In projects combining a longitudinal setup with repeated instruments or events, row counts can escalate quickly: one row per event per record, plus one additional row per repeat instance per event per record.

**Best practice:** Use report filters to target specific events, specific instruments, or specific instance ranges when exporting. Avoid exporting all data from a project with both longitudinal and repeated configurations unless you have a clear plan for handling the resulting data structure.

## 8.4 Workflow Features — Collecting Repeating Survey Data

When a repeating instrument is also enabled as a survey, there are three ways to prompt respondents to submit multiple instances. These options are not mutually exclusive and can be combined within the same project.

| | **"Repeat the survey" button** | **Automated Survey Invitations (ASIs)** | **Alerts & Notifications** |
|---|---|---|---|
| **How it works** | A button appears at the end of the survey so the respondent can start a new instance immediately | The survey link is sent repeatedly on a configured schedule | An alert sends the survey link repeatedly on a configured schedule |
| **Works with repeating instruments?** | Yes | Yes | Yes |
| **Works with instruments on repeating events?** | **No** | Yes | Yes |
| **Email required?** | No — web interface only | Yes (or SMS/voice calls) | Yes (or SMS/voice calls) |
| **Typical use** | Back-to-back entry in one session (e.g., entering multiple medications or family members) | Scheduled recurring surveys (e.g., daily or weekly check-ins sent by email) | Scheduled recurring surveys sent by email or SMS |

**Enabling the "Repeat the survey" button is a two-step process:**

1. Enable the instrument as a repeating instrument in the repeating instruments and events popup (Project Setup → Enable optional modules and customizations).
2. After that is saved, open the instrument's **Survey Settings** page and enable the **"Repeat the survey"** option in the survey termination options section.

The button will not appear on the survey until both steps are complete. The "Repeat the survey" option in Survey Settings is only available after the instrument has been designated as repeating.

---

# 9. Common Questions

**Q: Can I use repeated instruments in a project that is not longitudinal?**

**A:** Yes. Repeated instruments are available in all project types. Repeated events, however, require longitudinal mode to be enabled.

**Q: Can I have a repeated instrument inside a repeated event?**

**A:** No. REDCap does not support nesting a repeated instrument within a repeated event. Within any given event, you must choose one mode: repeat the entire event or repeat specific instruments independently. You cannot combine both in the same event.

**Q: Can the same instrument be repeatable in some events but not others?**

**A:** Yes, in longitudinal projects. Instrument-level repeatability is configured per event, not per instrument globally. An instrument can be repeatable in Event A and non-repeatable in Event B.

**Q: How do I reference a value from a specific instance of a repeated instrument?**

**A:** Reliably referencing values across instances from outside a repeated instrument or event is not straightforward in REDCap. Smart variables allow some within-instance references. For cross-instance comparisons, consider restructuring your data model to avoid this requirement. Consult your REDCap administrator if this is a design requirement for your project.

**Q: Can I switch a project from repeated instruments to repeated events after data collection has started?**

**A:** Technically the configuration can be changed, but doing so when instances already exist is strongly discouraged and can cause data loss. Test any such change in a cloned project first and consult your REDCap administrator before proceeding.

**Q: Does the instance counter reset between events?**

**A:** Instance numbering for repeated instruments is independent per instrument per event. Each event's repeated instrument starts fresh at instance 1. For repeated events, each repetition of the event is a new instance of that event, starting from 1.

**Q: Can I bulk upload or export the repeatable instrument/event configuration?**

**A:** Not through the REDCap interface. Arms, events, and instrument-event designations all support CSV upload and download from the UI, but the repeatable mapping configuration does not. The REDCap API does support both exporting and importing the repeatable instruments and events setup, making it the only programmatic path for bulk management of this configuration.

**Q: How do I let respondents fill out a survey multiple times in one sitting?**

**A:** Enable the "Repeat the survey" option in the instrument's Survey Settings page (in the survey termination options section). This adds a button at the end of the survey so the respondent can immediately start a new instance. This is a two-step process: you must first designate the instrument as a repeating instrument in the repeating instruments/events popup in Project Setup, then enable the "Repeat the survey" setting in Survey Settings. This option is only available for repeating instruments — it does not work for instruments on repeating events.

**Q: What is the best way to send a repeating survey to participants on a schedule?**

**A:** Use Automated Survey Invitations (ASIs) or Alerts & Notifications — both support sending a survey link repeatedly at a configured interval and work with both repeating instruments and instruments on repeating events. ASIs are configured directly on the instrument in the Online Designer. Alerts are configured on the Alerts & Notifications page. Both support email delivery and, if configured, SMS and voice calls. The "Repeat the survey" button is not suitable for scheduled delivery — it only allows back-to-back entry in a single session.

---

# 10. Common Mistakes & Gotchas

**Trying to set up repeated events before completing the longitudinal configuration.** The repeating instruments and events popup will not display events correctly if arms, events, or instrument designations are incomplete. Always finish the full longitudinal setup before configuring repeated instruments or events in a longitudinal project.

**Designing branching logic that references across repeated instances.** Logic that attempts to check values in instance 1 from within instance 3 of the same instrument, or from outside the repeated context entirely, will not behave reliably. Design instruments so that logic only references variables within the same instance.

**Using repeated events when independent instrument repetition is needed.** When an event is configured as "Repeat entire event," all instruments in that event must be repeated together. If different instruments need to be repeated at different rates, use the "Repeat instruments" option instead and designate each instrument's repeatability separately.

**Forgetting that the mapping upload is non-additive.** If you use the CSV upload for instrument-event mappings after configuring repeated instruments, be aware that the upload replaces all mappings. Instruments previously set as repeatable via the popup are a separate configuration — the mapping upload does not affect the repeatability setting, but it can remove instrument-event designations.

**Expecting custom labels to work with external variables.** The piped variable in a custom label must exist within the same repeated instrument or event. Attempting to pipe in a variable from a different instrument (e.g., from the baseline event) will display a blank label rather than an error.

**Assuming CSV bulk upload covers the repeatable configuration.** The CSV upload options for arms, events, and instrument-event designations do not include the repeatable instrument and event setup. Setting up your entire longitudinal structure via CSV and expecting the repeatable mapping to carry over will leave that configuration blank — you must either set it manually through the UI popup or use the REDCap API.

**Enabling "Repeat the survey" before designating the instrument as repeating.** The "Repeat the survey" setting in Survey Settings depends on the instrument first being designated as a repeating instrument. Enabling the survey setting without completing that step first will not produce the expected behavior. Always configure the instrument as repeating in Project Setup first, then enable the survey termination option.

**Expecting the "Repeat the survey" button to work with repeating events.** The "Repeat the survey" button is available for repeating instruments only. If your survey instrument lives on a repeating event rather than being designated as a repeating instrument, this option is not available. Use ASIs or Alerts & Notifications to send recurring survey links in that scenario.

**Overlooking inactive events in the repeating setup popup.** The popup lists every event in the project, including events whose names indicate they are no longer in active use (e.g., "WF Int (inactive)", "FISMA (inactive)"). REDCap has no concept of a disabled event — all events appear and can be configured. If you intend inactive events to remain non-repeating, verify that they are set to `-- not repeating --` when saving. Accidentally enabling repeat on a logically inactive event will not cause data loss, but it will expose the repeat UI to data entry users on those events.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-10 — Export Instrument-Event Mappings API** — retrieve instrument-event assignments, including repeating configuration
- **RC-API-11 — Import Instrument-Event Mappings API** — update instrument-event assignments including repeating instrument setup

---


# 11. Related Articles

- RC-LONG-01 — Longitudinal Project Setup (setting up arms, events, and instrument designations — prerequisite for longitudinal repeated setups)
- RC-NAV-REC-03 — Repeated Instruments & Repeated Events (how instances appear during data entry)
- RC-NAV-REC-02 — Longitudinal Mode & Arms (navigating longitudinal records)
- RC-FD-01 — Form Design Overview (building instruments before configuring repeatability)
- RC-FD-02 — Online Designer (creating and managing instruments)
- RC-BL-01 — Branching Logic Overview & Scope (how repeated setups affect branching logic)
- RC-DE-03 — Longitudinal Projects & DAGs (data entry in a longitudinal and repeated context)

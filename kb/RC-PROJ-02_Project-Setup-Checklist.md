RC-PROJ-02

**Project Setup Checklist**

| **Article ID** | RC-PROJ-02 |
|---|---|
| **Domain** | Project |
| **Applies To** | All REDCap projects; requires Project Design and Setup rights |
| **Prerequisite** | RC-PROJ-01 — Project Lifecycle: Status and Settings |
| **Version** | 1.2 |
| **Last Updated** | 2026 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-FD-01 — Form Design Overview; RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup; RC-SURV-01 — Surveys – Basics; RC-USER-01 — User Rights Overview; RC-DAG-01 — Data Access Groups; RC-ALERT-01 — Alerts & Notifications: Setup; RC-RAND-02 — Randomization Setup Guide |

---

# 1. Overview

This article provides a dependency-ordered checklist for setting up a REDCap project from creation to Production. Steps are organized so that each item can only be completed once its prerequisites are in place — for example, you cannot assign instruments to events until both instruments and events exist; you cannot set up a Survey Queue until at least two surveys are enabled.

Use this as a walk-through guide for new projects or as a pre-launch review for existing ones.

Steps marked **[Required]** must be completed for every project. All other steps are conditional or optional: steps marked **[Longitudinal]** apply only to projects using longitudinal mode; **[Repeating]** applies to projects using repeating instruments or events (repeating instruments can be used in any project type — repeating events require longitudinal mode); **[Surveys]** applies only if collecting data via surveys; **[DAGs]** applies only if using Data Access Groups; **[Randomization]** applies only if the project includes randomization.

---

# 2. Phase 1 — Create the Project

These steps happen once and unlock all subsequent configuration.

- [ ] **[Required] Create the project** via the "New Project" button on the My Projects page. Enter a project title, choose a purpose, and select whether to start from scratch or copy an existing project.
- [ ] **Set the project purpose and IRB number** on the Project Setup page (if required by your institution).
- [ ] **[Surveys] Enable surveys** by toggling "Use surveys in this project?" on the Project Setup page. This must be done before any instrument can be designated as a survey.
- [ ] **[Longitudinal] Enable longitudinal mode** by toggling "Use longitudinal data collection with defined events?" on the Project Setup page. This must be done before arms or events can be defined.

> **Note:** Enabling or disabling longitudinal mode after data has been collected is destructive. Enable it before building instruments if you know your project will be longitudinal. See RC-PROJ-01 §6.4 and RC-LONG-01 §3 for consequences of disabling longitudinal mode with existing data.

---

# 3. Phase 2 — Design Your Instruments

Instruments (forms) are the foundation for every other configuration step. Fields must exist before you can write branching logic, create calculated fields, configure surveys, set up alerts, or build reports.

- [ ] **[Required] Create instruments** using the Online Designer (RC-FD-02) or by uploading a Data Dictionary CSV (RC-FD-03). Add as many instruments as your data collection plan requires.
- [ ] **[Required] Add fields to each instrument.** Choose the appropriate field type, enter field labels, and assign variable names. Variable names cannot be easily changed after data has been collected — choose them carefully.
- [ ] **Set field validation** on text fields where applicable (e.g., date, integer, email). See RC-DE-05 — Field Validations.
- [ ] **Mark required fields** (fields that must be completed before a form can be saved). Use sparingly — over-use of required fields frustrates data entry and survey respondents.
- [ ] **Add branching logic** to fields that should only appear under certain conditions. In longitudinal projects, cross-event references must include the unique event name (e.g., `[baseline_arm_1][field_name]`). See RC-BL-01 — Branching Logic Overview.
- [ ] **Add calculated fields** for any derived values (totals, scores, age from date of birth). Calculations reference existing fields and update automatically. See RC-CALC-02 — Calculated Fields.
- [ ] **Add action tags** to fields that require special behavior (auto-fill, hidden display, read-only, etc.). See RC-AT-01 — Action Tags Overview.
- [ ] **Review the Codebook** (RC-FD-05) to confirm field types, variable names, and choice codes before proceeding. Errors are much easier to fix now than after data collection has started.

> **Dependency note:** All subsequent phases — longitudinal setup, repeating instruments, survey configuration, user rights, alerts, reports, and randomization — reference fields or instruments by name. Build and review your instruments before configuring anything else.

---

# 4. Phase 3 — Longitudinal Setup [Longitudinal]

Complete this phase only if longitudinal mode was enabled in Phase 1. Arms must be defined before the events that belong to them; events must be defined before instruments can be assigned to them.

- [ ] **[Multi-arm only] Define arms** on the Define My Events page. Arms separate participant cohorts that follow different event schedules. Single-arm projects can skip this step — REDCap creates "Arm 1" automatically. See RC-LONG-01 §4.1.
- [ ] **Define events** within each arm (e.g., Baseline, Month 3, Month 6). Events must exist before instruments can be designated to them. See RC-LONG-01 §4.2–4.3.
  - Assign meaningful, consistent event labels — the unique event name REDCap generates from the label is used in all logic references and cannot be manually changed through the UI.
  - If event display order matters and multiple events share the same day offset, assign sequential day offsets (0, 1, 2…) to enforce display order.
- [ ] **Designate instruments to events** on the Designate Instruments for My Events page. Check every instrument-event combination where data should be collected. See RC-LONG-01 §5.
  - **Always designate the first instrument (containing the record ID field) to the first event in every arm.** Omitting this causes records to save incorrectly.
  - An instrument can be designated to multiple events (e.g., a vitals form collected at every visit).
- [ ] **Review branching logic and calculated fields** that cross event boundaries. All cross-event references must use the unique event name prefix (e.g., `[baseline_arm_1][dob]`). See RC-BL-05 — Branching Logic in Longitudinal Projects.

---

# 5. Phase 4 — Repeating Instruments & Events [Repeating]

Repeating instruments allow multiple instances of a single form to be collected within one record (or one event in a longitudinal project). Repeating events allow an entire event — with all its designated instruments — to repeat. Configure this phase after instruments are built and, if applicable, after events are defined.

- [ ] **[Repeating instruments] Identify which instruments need to repeat** within a record or event. Repeating instruments are available in both classical and longitudinal projects. Examples: a medication log where each row is a separate drug, or an adverse event form completed once per event.
- [ ] **[Repeating events — Longitudinal only] Identify which events need to repeat.** Repeating events are only available in longitudinal projects and require events to be defined first (Phase 3). Examples: unscheduled visits, repeated lab draws within a single study phase.
- [ ] **Configure repeating instruments and/or events** via the "Repeating Instruments and Events" popup accessed from the Project Setup page. For each arm, designate which instruments repeat (within their event) and which events repeat entirely. See RC-LONG-02 — Repeated Instruments & Events Setup.
- [ ] **[Longitudinal] Confirm instrument-event designations include the repeating instruments** in the correct events. An instrument must be designated to an event before it can be set as repeating within that event.

> **Key distinction:** Repeating instruments repeat a single form within a record or event; repeating events repeat an entire collection of instruments together. Choose based on what your data model requires. See RC-LONG-02 for guidance on which to use.

---

# 6. Phase 5 — Survey Configuration [Surveys]

Survey features become available after enabling surveys in Phase 1. Each instrument must be individually enabled as a survey before survey-specific settings or automation can be configured for it.

- [ ] **Enable each instrument as a survey** from the Online Designer by clicking the "Enable" button next to that instrument under the Survey column. This reveals the survey settings panel for that instrument.
- [ ] **Configure survey settings per instrument:** set the survey title, instructions, completion text, auto-continue behavior, save-and-return options, and any response limit. See RC-SURV-02 — Survey Settings: Basic Options & Design.
- [ ] **Configure access and termination settings** for each survey: public vs. private link, stop actions, response limits. See RC-SURV-03 — Survey Settings: Behavior, Access & Termination.
- [ ] **[Survey Queue] Set up the Survey Queue** to chain multiple surveys in sequence. Requires at least two instruments to be enabled as surveys. Define the condition under which each subsequent survey is activated. See RC-SURV-07 — Survey Queue.
- [ ] **[Automated invitations] Set up Automated Survey Invitations (ASI)** for any survey that should be sent automatically based on a trigger condition or schedule. Requires the survey to be enabled and any trigger fields to already exist. See RC-SURV-06 — Automated Survey Invitations.
- [ ] **[e-Consent] Set up the e-Consent framework** if the project collects electronic informed consent. Requires a dedicated consent instrument with a signature field. See RC-SURV-08 — e-Consent Framework: Setup & Management.

---

# 7. Phase 6 — Access Control

User roles should be defined before individual users are added, so each new user can be placed directly into the correct role. Data Access Groups (if used) should be configured before assigning users, since DAG membership affects what data each user can see and enter.

- [ ] **[DAGs] Create Data Access Groups** via the DAGs page. Define one DAG per site, cohort, or data access boundary. See RC-DAG-01 — Data Access Groups.
- [ ] **Create User Roles** that match your team's access needs (e.g., Data Entry, Monitor, PI, Administrator). Define the privileges for each role once rather than configuring every user individually. See RC-USER-02 — Adding Users & Managing Roles.
- [ ] **Add users to the project** and assign each user to the appropriate role. See RC-USER-02.
- [ ] **[DAGs] Assign users to DAGs** after they have been added to the project. See RC-DAG-01.
- [ ] **Review each role's instrument-level permissions.** Confirm that each role can see and edit only the instruments it should have access to. See RC-USER-03 — Configuring User Privileges.

> **Tip:** Test user access before going live by logging in as a test account with each role and verifying that the correct instruments, records, and menu options are visible.

---

# 8. Phase 7 — Automation & Quality

Alerts, data quality rules, and randomization all depend on instruments and fields existing. Randomization additionally requires a randomization field and an allocation table.

- [ ] **Set up Alerts & Notifications** for any automated emails or text messages triggered by data entry events. Trigger conditions reference field values, so all relevant fields must exist first. See RC-ALERT-01 — Alerts & Notifications: Setup.
- [ ] **Configure Data Quality rules** to catch missing or out-of-range values. Rules reference field names and can be run manually or scheduled. See RC-DQ-01 — Data Quality Module.
- [ ] **[Randomization] Prepare the randomization allocation table** (a CSV of strata and assignments) before configuring the module. The randomization field must already exist in an instrument. See RC-RAND-01 — Randomization Concepts & Terminology and RC-RAND-02 — Randomization Setup Guide.
- [ ] **[Randomization] Configure the Randomization module** by uploading the allocation table and designating the randomization field and any stratification fields. See RC-RAND-02.

---

# 9. Phase 8 — Reports

Reports reference fields that must already exist. They can be built at any point after instruments are designed, but are most useful to finalize before going live so that the data monitoring and export workflow is ready from the first record.

- [ ] **Create custom reports** for data monitoring, safety reviews, or export workflows. Each report filters by field values and selects specific fields to display. See RC-EXPRT-06 — Custom Reports: Setup & Field Selection.
- [ ] **Set report sharing and access permissions** to control which users can view or export each report. See RC-EXPRT-08 — Custom Reports: Management & Organization.

---

# 10. Phase 9 — Test in Development

Before moving to Production, enter test data and verify that every aspect of the project behaves as designed. This is the last opportunity to make unrestricted changes.

- [ ] **Create test records** and enter data across all instruments and (for longitudinal projects) all events.
- [ ] **Verify branching logic** — confirm that fields appear and hide under the correct conditions.
- [ ] **Verify calculated fields** — confirm that scores and derived values compute correctly across a range of inputs, including edge cases.
- [ ] **[Repeating] Test repeating instances** — create multiple instances of each repeating instrument or event and confirm that data saves correctly and is distinguishable per instance.
- [ ] **[Surveys] Test survey flow** — complete each survey as a respondent, including the Survey Queue if configured. Confirm confirmation emails arrive and contain the correct content.
- [ ] **[Longitudinal] Verify event navigation** — confirm that the Record Home Page shows the correct instrument-event grid and that all designations are correct.
- [ ] **[Alerts] Trigger alerts intentionally** — enter data that meets each alert's condition and confirm the correct recipient receives the expected message.
- [ ] **[Randomization] Test the randomization workflow** with test records. Confirm that stratification is applied correctly and that randomized assignments are recorded as expected.
- [ ] **Test as each user role** — log in with a test account for each role and confirm that access is correctly restricted (e.g., a data entry user cannot see admin menus; a DAG-assigned user can only see their own records).
- [ ] **Run Data Quality rules** against test records and confirm that known errors are flagged.
- [ ] **Review all test reports** to confirm they return the expected fields and rows.

---

# 11. Phase 10 — Move to Production

When the project is fully tested and ready for live data collection, move it to Production. This step enables change-control safeguards and signals that real data collection has begun.

- [ ] **[Required] Delete all test data** before going live. On the Project Setup page, use "Delete all records" (under Other Functionality) or choose to delete test data when prompted during the move-to-Production step.
- [ ] **[Required] Move the project to Production** by clicking "Move project to Production" at the bottom of the Project Setup page. See RC-PROJ-01 §2.2.
- [ ] **Confirm Production protections are active** — verify that the Online Designer now shows the "Enter Draft Mode" button, indicating that design changes require review before taking effect.
- [ ] **Communicate the go-live to your team.** Ensure all users know the project is live and that any future design change requests must go through the Draft Mode review process.

> **After go-live:** Any structural change (new fields, modified branching logic, new instruments) must be made through Draft Mode and submitted for review. See RC-PROJ-01 §6 — Making Production Changes for the rules that protect existing data.

---

# 12. Quick Dependency Reference

The table below summarizes the key dependencies between setup steps. If a step is blocked, check that its prerequisite has been completed.

| Step | Depends On |
|---|---|
| Enable longitudinal mode | Project created |
| Define arms | Longitudinal mode enabled |
| Define events | Longitudinal mode enabled; arms defined (if multi-arm) |
| Designate instruments to events | Instruments exist; events defined |
| Repeating instruments | Instruments exist (any project type) |
| Repeating events | Longitudinal mode enabled; events defined |
| Enable instrument as survey | Survey mode enabled (Phase 1); instrument exists |
| Survey Queue | ≥2 instruments enabled as surveys |
| Automated Survey Invitations | Survey enabled on instrument; trigger fields exist |
| Branching logic (cross-event) | Longitudinal mode enabled; events defined |
| Create User Roles | Project created |
| Add users to project | Project created |
| Assign users to roles | User roles created; users added |
| Assign users to DAGs | DAGs created; users added |
| Alerts & Notifications | Fields/instruments exist for trigger conditions |
| Randomization module | Randomization field exists; allocation table ready |
| Custom reports | Fields/instruments exist |
| Move to Production | All above steps complete; test data deleted |

---

# 13. UI & API Reference

All setup steps can be completed through the REDCap user interface. The table below indicates which steps also have a supported API path. Steps with an API option can be automated or scripted using the REDCap API — see RC-API-01 — REDCap API for authentication and setup.

| Step | Phase | UI | API |
|---|---|---|---|
| Create the project | 1 | ✓ | ✓ RC-API-37 |
| Set project purpose / IRB | 1 | ✓ | ✓ RC-API-35 |
| Enable surveys | 1 | ✓ | ✓ RC-API-35 |
| Enable longitudinal mode | 1 | ✓ | ✓ RC-API-35 |
| Create instruments | 2 | ✓ | ✓ RC-API-08 |
| Add fields | 2 | ✓ | ✓ RC-API-08 |
| Set field validation | 2 | ✓ | ✓ RC-API-08 |
| Mark required fields | 2 | ✓ | ✓ RC-API-08 |
| Add branching logic | 2 | ✓ | ✓ RC-API-08 |
| Add calculated fields | 2 | ✓ | ✓ RC-API-08 |
| Add action tags | 2 | ✓ | ✓ RC-API-08 |
| Review Codebook | 2 | ✓ | — |
| Define arms | 3 | ✓ | ✓ RC-API-17 |
| Define events | 3 | ✓ | ✓ RC-API-20 |
| Designate instruments to events | 3 | ✓ | ✓ RC-API-11 |
| Review cross-event logic | 3 | ✓ | — |
| Configure repeating instruments | 4 | ✓ | ✓ RC-API-53 |
| Configure repeating events | 4 | ✓ | ✓ RC-API-53 |
| Enable instrument as survey | 5 | ✓ | — |
| Configure survey settings | 5 | ✓ | — |
| Configure survey access & termination | 5 | ✓ | — |
| Set up Survey Queue | 5 | ✓ | — |
| Set up Automated Survey Invitations | 5 | ✓ | — |
| Set up e-Consent framework | 5 | ✓ | — |
| Create Data Access Groups | 6 | ✓ | ✓ RC-API-29 |
| Create User Roles | 6 | ✓ | ✓ RC-API-26 |
| Add users to project | 6 | ✓ | ✓ RC-API-23 |
| Assign users to roles | 6 | ✓ | ✓ RC-API-56 |
| Assign users to DAGs | 6 | ✓ | ✓ RC-API-32 |
| Review role permissions | 6 | ✓ | — |
| Set up Alerts & Notifications | 7 | ✓ | — |
| Configure Data Quality rules | 7 | ✓ | — |
| Prepare randomization allocation table | 7 | ✓ | — |
| Configure Randomization module | 7 | ✓ | — |
| Create custom reports | 8 | ✓ | — |
| Set report permissions | 8 | ✓ | — |
| Create test records | 9 | ✓ | ✓ RC-API-03 |
| Verify branching logic | 9 | ✓ | — |
| Verify calculated fields | 9 | ✓ | — |
| Test repeating instances | 9 | ✓ | — |
| Test survey flow | 9 | ✓ | — |
| Verify event navigation | 9 | ✓ | — |
| Trigger alerts intentionally | 9 | ✓ | — |
| Test randomization workflow | 9 | ✓ | — |
| Test as each user role | 9 | ✓ | — |
| Run Data Quality rules | 9 | ✓ | — |
| Review test reports | 9 | ✓ | — |
| Delete test data | 10 | ✓ | ✓ RC-API-04 |
| Move to Production | 10 | ✓ | — |
| Confirm Production protections | 10 | ✓ | — |
| Communicate go-live | 10 | — | — |

---

# 14. Related Articles

- RC-PROJ-01 — Project Lifecycle: Status and Settings (project statuses, moving to Production, Draft Mode)
- RC-FD-01 — Form Design Overview (instrument design entry point)
- RC-FD-02 — Online Designer (building and managing instruments)
- RC-FD-03 — Data Dictionary (CSV-based instrument design)
- RC-LONG-01 — Longitudinal Project Setup (arms, events, and instrument-event designations)
- RC-LONG-02 — Repeated Instruments & Events Setup (configuring repeating instruments and events)
- RC-SURV-01 — Surveys – Basics (survey fundamentals)
- RC-SURV-06 — Automated Survey Invitations (scheduling and triggering survey sends)
- RC-SURV-07 — Survey Queue (chaining surveys in sequence)
- RC-USER-01 — User Rights: Overview & Three-Tier Access (access control fundamentals)
- RC-USER-02 — User Rights: Adding Users & Managing Roles (creating roles and adding users)
- RC-DAG-01 — Data Access Groups (multi-site access control)
- RC-ALERT-01 — Alerts & Notifications: Setup (automated messaging)
- RC-DQ-01 — Data Quality Module (data validation rules)
- RC-RAND-02 — Randomization Setup Guide (configuring the randomization module)
- RC-EXPRT-06 — Custom Reports: Setup & Field Selection (building data monitoring reports)
- RC-API-01 — REDCap API (authentication, tokens, and API setup)

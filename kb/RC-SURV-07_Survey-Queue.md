RC-SURV-07

**Surveys — Survey Queue**

| **Article ID** | RC-SURV-07 |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All projects with surveys enabled |
| **Prerequisite** | RC-SURV-06 — Automated Survey Invitations |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-SURV-06 — Automated Survey Invitations; RC-SURV-05 — Participant List & Manual Survey Invitations; RC-SURV-03 — Survey Settings: Behavior, Access & Termination; RC-BL-01 — Branching Logic: Overview & Scope; RC-LONG-01 — Longitudinal Project Setup; RC-LONG-02 — Repeated Instruments & Events Setup; RC-PIPE-03 — Smart Variables Overview |

---

# 1. Overview

This article covers the Survey Queue — REDCap's feature for controlling the flow of participants through multiple surveys within a single session or across multiple sessions. It explains how to set up the survey queue, define trigger conditions for each survey, configure auto-start behavior, distribute the survey queue link to participants, and understand how the queue works with repeatable instruments and the Save and Return Later feature. It also documents when to use the survey queue versus Automated Survey Invitations (ASIs) versus the auto-continue feature. This article is part of the Surveys knowledge base series.

---

# 2. Key Concepts & Definitions

**Survey Queue**

A feature that controls which surveys are presented to a participant and in what order, immediately following the completion of a preceding survey. Unlike ASIs, the survey queue operates within a session (no time delay or email required) and can present participants with a menu of available surveys.

**Survey Queue Link**

A unique URL tied to a specific record (not a specific survey). It directs the participant to their personal survey queue overview, where they can see completed and available surveys. The link remains valid as long as the record exists and the project is active.

**Auto-Start**

A per-survey setting in the queue that causes REDCap to skip the survey queue overview screen and launch the next survey automatically the moment the preceding one is completed.

**Activated Survey (in the queue)**

A survey that has been turned on in the survey queue interface. Deactivated surveys are ignored by the queue even if they are enabled as surveys in the project.

**Form Display Logic**

A separate Online Designer feature, adjacent to the survey queue, that restricts user (staff) access to forms based on conditional logic. It does not interact with the survey queue but can optionally influence the auto-continue feature. It is covered in RC-FDL-01 — Form Display Logic *(coming soon)*.

---

# 3. When to Use the Survey Queue

The survey queue, ASIs, and the auto-continue feature all direct participants to the next survey, but they serve different use cases.

| Scenario | Recommended Tool |
|---|---|
| Participant should move immediately to the next survey after completing one | Survey Queue (with or without auto-start) |
| Follow-up survey should be sent by email after a time delay | ASI |
| Complex routing based on participant responses (e.g., one survey or another) | Survey Queue (logic trigger) |
| Time-point based study where participants complete several surveys per visit | Both: ASI for the first survey at each time point; survey queue for the remaining surveys within that visit |
| Simple linear project with a small number of surveys | Auto-continue feature (simpler to configure) |
| Longitudinal projects or projects with repeatable instruments | Survey Queue (auto-continue has known interaction issues in these configurations) |

> **Best practice:** Do not use the auto-continue feature and the survey queue simultaneously. There are documented reports of unexpected behavior when both are active in the same project.

---

# 4. Survey Queue Setup

## 4.1 Setup Location

The survey queue is managed from the Online Designer. In the **Survey Options** header area at the top of the Online Designer, click the **Survey Queue** button and select **Edit Survey Queue**. This opens the survey queue configuration popup.

The popup is populated by all surveys in the project. In longitudinal projects, the list shows every survey-event combination. For projects with many surveys or events, the list can be long and may take a moment to load.

## 4.2 Activating a Survey in the Queue

The first column of the survey queue table, labeled **Activated?**, shows an **Activate** button for each survey that is not yet part of the queue. By default, all surveys are deactivated. Click **Activate** to enable a survey in the queue. Once activated, the button changes to **Deactivate**, which removes it from the queue without deleting its configuration.

## 4.3 Defining Trigger Conditions

The third column, **"Display survey in the Survey Queue when..."**, is where trigger conditions are defined. This is the most important configuration for any survey in the queue. The three trigger types mirror the ASI trigger structure (see RC-SURV-06 — Automated Survey Invitations):

### Completion Trigger

Check **"When the following survey is completed:"** and select the preceding survey. When that survey is completed, this survey becomes visible (or auto-starts) in the queue.

In longitudinal projects, the list shows all survey-event combinations.

### Logic Trigger

Check **"When the following logic becomes true:"** and enter a branching logic statement. When the logic evaluates to true, this survey appears in (or auto-starts from) the queue.

Example: show the "Child Questionnaire" only when `[age] < 18`.

For guidance on writing logic, see RC-BL-01 — Branching Logic: Overview & Scope and RC-BL-02 — Branching Logic: Syntax & Atomic Statements.

> **Note:** All survey queue logic is re-evaluated whenever a participant completes any survey in the queue. This means branching-based routing updates dynamically as participants progress.

### Combination Trigger

Configure both a completion trigger and a logic trigger, then select **AND** (both must be true) or **OR** (either is sufficient) from the dropdown between them.

## 4.4 Auto-Start

The fourth column, **Auto Start?**, contains a checkbox for each activated survey.

- **Checked** — When this survey's trigger conditions are met, REDCap immediately launches it without showing the survey queue overview screen. The participant moves seamlessly from one survey to the next.
- **Unchecked** — When the conditions are met, the participant is taken to the survey queue overview screen, where they can see all available surveys and choose which to open.

**Order of operations with auto-start:** If two surveys are triggered simultaneously and both have auto-start enabled, REDCap launches the one that appears first in the instrument list in the Online Designer. Take instrument order into account when designing sequential survey flows.

---

# 5. Overall Survey Queue Options

Two additional settings affect the survey queue as a whole, visible at the top of the survey queue configuration popup:

**Keep the Survey Queue Hidden from Participants?**
When this box is checked, all surveys in the queue behave as if auto-start is enabled, regardless of their individual auto-start settings. Use this when you want to use the queue for routing logic but do not want participants to see the queue overview screen at all.

**Custom Text**
Displays a custom message at the top of the survey queue overview screen. This text applies to the entire project — it cannot be conditioned on logic. Keep it generic enough to apply to all scenarios a participant might encounter in the queue.

---

# 6. Bulk Survey Queue Management via CSV

For projects with many surveys or survey-event combinations, the survey queue can be managed via CSV upload and download.

**Downloading:** In the Online Designer, click the Survey Queue button and select **Download Survey Queue Setup (CSV)**. The file reflects the current configuration.

**Uploading:** Click the Survey Queue button and select **Upload Survey Queue Setup (CSV)**. REDCap validates the file and reports any errors before applying changes. If there are errors, they must be resolved before a successful upload. If there are none, REDCap confirms which surveys were modified.

Best practice before using this feature for the first time: manually configure a few surveys in the queue interface, then download the CSV to understand the expected format.

The CSV has nine columns:

| Column | Description |
|---|---|
| `form_name` | The unique name of the instrument (survey) being configured. Find unique names in the Codebook (RC-FD-05). |
| `event_name` | Required for longitudinal projects; specifies the event. Find event names in Define My Events (Project Setup). Optional for non-longitudinal projects. |
| `active` | `1` = activated in queue; `0` or blank = deactivated. |
| `condition_surveycomplete_form_name` | The unique name of the survey whose completion triggers this survey. Leave blank if not using a completion trigger. |
| `condition_surveycomplete_event_name` | The event of the completing survey (longitudinal projects). Leave blank if not using a completion trigger. |
| `condition_andor` | `AND` or `OR` — defines the relationship when both completion and logic conditions are used. |
| `condition_logic` | Branching logic statement for the logic trigger. Same syntax as standard branching logic. Leave blank if not using a logic trigger. |
| `auto_start` | `1` = auto-start enabled; `0` = disabled. |

---

# 7. Distributing the Survey Queue Link

Unlike individual survey links (which are instrument and event specific), the survey queue link is tied to the record as a whole. There is only one survey queue link per record, and it does not expire as long as the record and project are active.

## 7.1 Participant List

In Survey Distribution Tools → Participant List, the **Survey Queue** column displays a queue icon for any participant that has at least one data point in their record. Clicking the icon opens the survey queue for that record in a new tab. The participant list's **Export List** function includes survey queue links in bulk.

> **Note:** Survey queue icons only appear in identified mode. In anonymous mode, the column is not clickable.

## 7.2 Smart Variables

The survey queue has two dedicated smart variables that can be used in ASIs, Alerts & Notifications, instrument fields, or anywhere piping is supported:

| Smart Variable | Output |
|---|---|
| `[survey-queue-url]` | The full URL of the survey queue for that record as plain text. |
| `[survey-queue-link:Custom Text]` | A clickable hyperlink to the survey queue. Replace `Custom Text` with the desired link label. |

A common workflow: send an ASI with the survey queue link (`[survey-queue-url]` or `[survey-queue-link:Custom Text]`) at the start of a time point, so participants can complete all surveys for that visit at their own pace across multiple sessions.

## 7.3 Survey Options Menu

When you open an instrument in a record and the survey queue is configured, the **Survey Options** dropdown inside the instrument gains a fifth option: **Survey Queue**. Clicking it opens the survey queue for that record in a new tab.

---

# 8. Participant Experience

## 8.1 Non-Sequential Queue (Participant Chooses Order)

If auto-start is disabled for all surveys and the queue is not hidden, participants see the survey queue overview after completing each survey. The overview shows completed surveys (with their status) and any surveys that are currently available based on trigger conditions. Participants can choose which available survey to open next.

A simple way to create this experience: activate all surveys in the queue and set each to trigger after the very first survey is completed.

## 8.2 Sequential Queue (Fixed Order)

To enforce a specific completion order, cascade the trigger conditions — each survey triggers only when the immediately preceding one is completed. With auto-start disabled, participants see the overview after each survey showing their progress and the next available survey. With auto-start enabled, they flow directly from one survey to the next without seeing the overview.

## 8.3 Repeatable Surveys in the Queue

A survey can be made repeatable so participants can take it multiple times within the survey queue. Two conditions must both be met:

1. The instrument must be set as a repeatable instrument (configured in Project Setup — see RC-LONG-02 — Repeated Instruments & Events Setup).
2. The **"Repeat the survey"** option must be enabled in that survey's termination settings (Survey Settings → Survey Termination Options).

When both conditions are met, the survey queue overview shows all previously completed instances of that survey and a button to take it again. A repeat button also appears at the end of the survey itself, so repeatable surveys can be taken again even without using the queue overview screen.

## 8.4 Save and Return Surveys in the Queue

If a survey has the **Save and Return Later** feature enabled and the participant has previously completed it, an **Edit Response** button appears in the survey queue overview next to that survey's entry. This allows participants to reopen and modify a completed survey from the queue without needing to know the direct survey link.

This behavior also applies to completed instances of repeatable instruments.

> **Note:** If a survey requires a return code for reopening (a sub-option of Save and Return Later), the participant will need that code to proceed. Ensure the code was communicated to them at the time of their original submission.

---

# 9. Common Questions

**Q: What is the difference between the survey queue and ASIs?**

**A:** ASIs send an email invitation (often with a time delay) to bring a participant to a survey. The survey queue controls the flow between surveys within a session — no email, no delay. They are complementary: ASIs bring participants to the first survey of a session; the survey queue guides them through the remaining surveys.

**Q: Can I use the survey queue and the auto-continue feature at the same time?**

**A:** No. There are documented cases of unexpected behavior when both features are active in the same project. Choose one. Use the survey queue for complex routing, longitudinal projects, or projects with repeatable instruments. Use auto-continue for simple, linear, non-longitudinal projects.

**Q: A participant completed Survey A, but Survey B is not showing in their queue. What could be wrong?**

**A:** Check three things: (1) Survey B is activated in the queue; (2) Survey B's trigger conditions are configured correctly (check the AND/OR setting if using a combination trigger); (3) the trigger logic for Survey B is evaluating as true for that record (use the branching logic tester in the ASI screen or test the logic in the Online Designer).

**Q: Can I send participants a link that takes them directly to their survey queue?**

**A:** Yes. Use the smart variable `[survey-queue-url]` to include the survey queue link in any ASI, Alert, or piped field. Alternatively, find the link in the participant list for that record.

**Q: What happens if two surveys are triggered simultaneously and both have auto-start enabled?**

**A:** REDCap launches the survey that appears first in the instrument order in the Online Designer. Design your instrument order to match your intended survey flow.

**Q: Does the survey queue link expire?**

**A:** No. The survey queue link for a record remains valid as long as the record exists and the project is active.

**Q: Can participants complete surveys in the queue across multiple sessions (i.e., not all at once)?**

**A:** Yes. The survey queue link is persistent and does not expire. Participants can return to the same link in a later session and continue where they left off.

---

# 10. Common Mistakes & Gotchas

**Forgetting to activate a survey in the queue.** A survey that is enabled as a survey in the project is not automatically included in the survey queue. Each survey must be explicitly activated in the queue interface or via the CSV upload. An inactivated survey will never appear in the queue regardless of whether its trigger conditions are met.

**Using auto-continue alongside the survey queue.** The auto-continue setting (in Survey Settings → Survey Termination Options) and the survey queue can conflict. Documented interactions between the two have produced unexpected behavior. If you are using the survey queue, disable auto-continue for all surveys in the project.

**Designing trigger conditions without considering instrument order.** When multiple surveys trigger simultaneously with auto-start enabled, REDCap uses instrument order (in the Online Designer) as the tiebreaker. If you have not intentionally ordered your instruments to match your intended flow, participants may start the wrong survey. Review instrument order in the Online Designer before going live.

**Expecting the survey queue icon to appear for anonymous participants.** The survey queue column in the participant list is only clickable in identified mode. Anonymous records show no clickable queue icon. Enable identified mode via participant identifier or a designated email field.

**Omitting the survey queue link from the ASI message for multi-survey time points.** If you use ASIs to kick off each time point and the survey queue to guide participants through subsequent surveys, the ASI message must include `[survey-queue-url]` or `[survey-queue-link:Custom Text]` — not just `[survey-url]`. Sending `[survey-url]` only takes the participant to a single survey, bypassing the queue entirely.

---

## API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See RC-API-01 — REDCap API for authentication, token management, and setup.

- **RC-API-41 — Export Survey Queue Link API** — programmatically retrieve the Survey Queue link for a specific record

---


# 11. Related Articles

- RC-SURV-06 — Automated Survey Invitations (email-based automated invitation scheduling; use with survey queue for time-point studies)
- RC-SURV-05 — Participant List & Manual Survey Invitations (manual invitation workflow; participant list survey queue column)
- RC-SURV-03 — Survey Settings: Behavior, Access & Termination (auto-continue and Save and Return Later settings)
- RC-BL-01 — Branching Logic: Overview & Scope (logic syntax for queue trigger conditions)
- RC-BL-02 — Branching Logic: Syntax & Atomic Statements (writing logic conditions)
- RC-LONG-01 — Longitudinal Project Setup (events and arms)
- RC-LONG-02 — Repeated Instruments & Events Setup (prerequisite for repeatable surveys in the queue)
- RC-PIPE-03 — Smart Variables Overview (`[survey-queue-url]`, `[survey-queue-link]`)
- RC-FD-05 — Codebook (finding instrument unique names for CSV upload)

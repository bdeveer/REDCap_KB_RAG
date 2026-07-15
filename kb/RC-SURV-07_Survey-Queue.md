

**Surveys — Survey Queue**

| **Article ID** | [RC-SURV-07 — Survey Queue](RC-SURV-07_Survey-Queue.md) |
|---|---|
| **Domain** | Surveys |
| **Applies To** | All projects with surveys enabled |
| **Prerequisite** | [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)|
| **Version** | 1.1 |
| **Last Updated** | 2026 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md); [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md); [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md); [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md); [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md); [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md); [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) |
| **Synonyms** | how do i chain multiple surveys together; set up a survey queue; present surveys to participants in sequence; auto-start the next survey after one finishes; survey queue trigger conditions; survey queue vs automated survey invitations; give participants one link for all their surveys; configure a series of surveys in a session |

---

## 1. Overview

This article covers the Survey Queue — REDCap's feature for controlling the flow of participants through multiple surveys within a single session or across multiple sessions. It explains how to set up the survey queue, define trigger conditions for each survey, configure auto-start behavior, distribute the survey queue link to participants, and understand how the queue works with repeatable instruments and the Save and Return Later feature. It also documents when to use the survey queue versus Automated Survey Invitations (ASIs) versus the auto-continue feature. This article is part of the Surveys knowledge base series.

---

## 2. Key Concepts & Definitions

**Survey Queue**

A feature that controls which surveys are presented to a participant and in what order, immediately following the completion of a preceding survey. Unlike ASIs, the survey queue operates within a session (no time delay or email required) and can present participants with a menu of available surveys.

**Survey Queue Link**

A unique URL tied to a specific record (not a specific survey). It directs the participant to their personal survey queue overview, where they can see completed and available surveys. The link remains valid as long as the record exists and the project is active.

**Auto-Start**

A per-survey setting in the queue that causes REDCap to skip the survey queue overview screen and launch the next survey automatically the moment the preceding one is completed.

**Activated Survey (in the queue)**

A survey that has been turned on in the survey queue interface. Deactivated surveys are ignored by the queue even if they are enabled as surveys in the project.

**Form Display Logic**

A separate Online Designer feature, adjacent to the survey queue, that restricts user (staff) access to forms based on conditional logic. It does not interact with the survey queue but can optionally influence the auto-continue feature. It is covered in [RC-FDL-01 — Form Display Logic](RC-FDL-01_Form-Display-Logic.md) *(coming soon)*.

---

## 3. When to Use the Survey Queue

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

## 4. Survey Queue Setup

### 4.1 Setup Location

The survey queue is managed from the Online Designer. In the **Survey Options** header area at the top of the Online Designer, click the **Survey Queue** button and select **Edit Survey Queue**. This opens the survey queue configuration popup.

The popup is populated by all surveys in the project. In longitudinal projects, the list shows every survey-event combination. For projects with many surveys or events, the list can be long and may take a moment to load.

### 4.2 Activating a Survey in the Queue

The first column of the survey queue table, labeled **Activated?**, shows an **Activate** button for each survey that is not yet part of the queue. By default, all surveys are deactivated. Click **Activate** to enable a survey in the queue. Once activated, the button changes to **Deactivate**, which removes it from the queue without deleting its configuration.

### 4.3 Defining Trigger Conditions

The third column, **"Display survey in the Survey Queue when..."**, is where trigger conditions are defined. This is the most important configuration for any survey in the queue. The three trigger types mirror the ASI trigger structure (see [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md) — Automated Survey Invitations):

#### Completion Trigger

Check **"When the following survey is completed:"** and select the preceding survey. When that survey is completed, this survey becomes visible (or auto-starts) in the queue.

In longitudinal projects, the list shows all survey-event combinations.

#### Logic Trigger

Check **"When the following logic becomes true:"** and enter a branching logic statement. When the logic evaluates to true, this survey appears in (or auto-starts from) the queue.

Example: show the "Child Questionnaire" only when `[age] < 18`.

For guidance on writing logic, see [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) and [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md).

> **Note:** All survey queue logic is re-evaluated whenever a participant completes any survey in the queue. This means branching-based routing updates dynamically as participants progress.

#### Combination Trigger

Configure both a completion trigger and a logic trigger, then select **AND** (both must be true) or **OR** (either is sufficient) from the dropdown between them.

### 4.4 Auto-Start

The fourth column, **Auto Start?**, contains a checkbox for each activated survey.

- **Checked** — When this survey's trigger conditions are met, REDCap immediately launches it without showing the survey queue overview screen. The participant moves seamlessly from one survey to the next.
- **Unchecked** — When the conditions are met, the participant is taken to the survey queue overview screen, where they can see all available surveys and choose which to open.

**Order of operations with auto-start:** If two surveys are triggered simultaneously and both have auto-start enabled, REDCap launches the one that appears first in the instrument list in the Online Designer. Take instrument order into account when designing sequential survey flows.

---

## 5. Overall Survey Queue Options

Two additional settings affect the survey queue as a whole, visible at the top of the survey queue configuration popup:

**Keep the Survey Queue Hidden from Participants?**
When this box is checked, all surveys in the queue behave as if auto-start is enabled, regardless of their individual auto-start settings. Use this when you want to use the queue for routing logic but do not want participants to see the queue overview screen at all.

**Custom Text**
Displays a custom message at the top of the survey queue overview screen. This text applies to the entire project — it cannot be conditioned on logic. Keep it generic enough to apply to all scenarios a participant might encounter in the queue.

---

## 6. Bulk Survey Queue Management via CSV

For projects with many surveys or survey-event combinations, the survey queue can be managed via CSV upload and download.

**Downloading:** In the Online Designer, click the Survey Queue button and select **Download Survey Queue Setup (CSV)**. The file reflects the current configuration.

**Uploading:** Click the Survey Queue button and select **Upload Survey Queue Setup (CSV)**. REDCap validates the file and reports any errors before applying changes. If there are errors, they must be resolved before a successful upload. If there are none, REDCap confirms which surveys were modified.

Best practice before using this feature for the first time: manually configure a few surveys in the queue interface, then download the CSV to understand the expected format.

The CSV has eight columns:

| Column | Accepted values | Notes |
|---|---|---|
| `form_name` | Instrument unique name | Find unique names in the Codebook ([RC-FD-05 — Codebook](RC-FD-05_Codebook.md)). |
| `event_name` | Event unique name | Required for longitudinal projects. Leave blank for classic (non-longitudinal) projects. |
| `active` | `1` or `0` | `1` = activated in queue; `0` = deactivated. |
| `condition_surveycomplete_form_name` | Instrument unique name, or blank | The survey whose completion triggers this survey. Leave blank for a logic-only trigger. |
| `condition_surveycomplete_event_name` | Event unique name, or blank | The event of the completing survey. Can reference an event from a different arm than the survey being configured. Leave blank for a logic-only trigger. |
| `condition_andor` | `AND` or `OR` | Defines how the completion and logic conditions combine. **Always populate this field**, even when only one condition type is used — REDCap requires a value. `AND` is the standard choice. |
| `condition_logic` | REDCap branching logic expression, or blank | Logic trigger condition. Same syntax as standard branching logic. Cross-event references use the format `[event_name][field_name]`. Leave blank for a completion-only trigger. |
| `auto_start` | `1` or `0` | `1` = auto-start enabled (participant moves directly to the next survey without seeing the queue overview); `0` = disabled. |

#### Annotated example — multi-arm longitudinal project

The following excerpt shows how a real export looks for a two-arm project with a screening arm and a baseline arm. Each instrument appears once per arm it belongs to; the same instrument can have different trigger logic per arm.

```
form_name,event_name,active,condition_surveycomplete_form_name,condition_surveycomplete_event_name,condition_andor,condition_logic,auto_start

# Arm 1: standard participants — completion-only chained triggers, auto-start throughout
demographics,baseline_arm_1,1,screening,screening_arm_1,AND,,1
social_history,baseline_arm_1,1,demographics,baseline_arm_1,AND,,1
contact_info,baseline_arm_1,1,social_history,baseline_arm_1,AND,,1
phq9,baseline_arm_1,1,contact_info,baseline_arm_1,AND,,1

# Arm 2: conditional participants — entry survey uses logic-only trigger (no completion trigger),
# subsequent surveys use a cross-arm completion trigger combined with the same logic condition
demographics,baseline_arm_2,1,,,AND,[screening_arm_2][screen_currently_pregnant]=1,0
social_history,baseline_arm_2,1,demographics,baseline_arm_1,AND,[screening_arm_2][screen_currently_pregnant]=1,1
contact_info,baseline_arm_2,1,demographics,baseline_arm_1,AND,[screening_arm_2][screen_currently_pregnant]=1,1
phq9,baseline_arm_2,1,demographics,baseline_arm_1,AND,[screening_arm_2][screen_currently_pregnant]=1,1
```

Key patterns to note from this example:

- **Logic-only trigger (entry survey in a conditional arm):** `demographics` in `baseline_arm_2` has no completion trigger (`condition_surveycomplete_form_name` and `condition_surveycomplete_event_name` are both blank). It appears in the queue based solely on the logic condition. `condition_andor` is still set to `AND`. `auto_start` is `0` because there is no prior survey to auto-start from.
- **Cross-arm completion trigger:** `social_history` and later surveys in `baseline_arm_2` reference `demographics` in `baseline_arm_1` as their completion trigger — an event from a different arm. This is valid and is the standard pattern for arm-specific routing in multi-arm projects.
- **Combination trigger:** Those same surveys also include a `condition_logic` expression. With `condition_andor=AND`, both conditions must be met before the survey appears in the queue.
- **Cross-event logic syntax:** The logic condition `[screening_arm_2][screen_currently_pregnant]=1` uses the `[event_name][field_name]` format to reference a field in a specific event. This is the same cross-event reference syntax used in branching logic elsewhere in REDCap.
- **Filename pattern:** REDCap names downloaded files `{ProjectTitle}_SurveyQueue_{YYYY-MM-DD}_{HHMM}.csv`.

For the full column-by-column reference, accepted values, an annotated example, and common mistakes, see **[RC-IMP-10 — Survey Queue CSV — Column Reference and Format Guide](RC-IMP-10_Survey-Queue-CSV.md) — Survey Queue CSV**.

---

## 7. Distributing the Survey Queue Link

Unlike individual survey links (which are instrument and event specific), the survey queue link is tied to the record as a whole. There is only one survey queue link per record, and it does not expire as long as the record and project are active.

### 7.1 Participant List

In Survey Distribution Tools → Participant List, the **Survey Queue** column displays a queue icon for any participant that has at least one data point in their record. Clicking the icon opens the survey queue for that record in a new tab. The participant list's **Export List** function includes survey queue links in bulk.

> **Note:** Survey queue icons only appear in identified mode. In anonymous mode, the column is not clickable.

### 7.2 Smart Variables

The survey queue has two dedicated smart variables that can be used in ASIs, Alerts & Notifications, instrument fields, or anywhere piping is supported:

| Smart Variable | Output |
|---|---|
| `[survey-queue-url]` | The full URL of the survey queue for that record as plain text. |
| `[survey-queue-link:Custom Text]` | A clickable hyperlink to the survey queue. Replace `Custom Text` with the desired link label. |

A common workflow: send an ASI with the survey queue link (`[survey-queue-url]` or `[survey-queue-link:Custom Text]`) at the start of a time point, so participants can complete all surveys for that visit at their own pace across multiple sessions.

### 7.3 Survey Options Menu

When you open an instrument in a record and the survey queue is configured, the **Survey Options** dropdown inside the instrument gains a fifth option: **Survey Queue**. Clicking it opens the survey queue for that record in a new tab.

---

## 8. Participant Experience

### 8.1 Non-Sequential Queue (Participant Chooses Order)

If auto-start is disabled for all surveys and the queue is not hidden, participants see the survey queue overview after completing each survey. The overview shows completed surveys (with their status) and any surveys that are currently available based on trigger conditions. Participants can choose which available survey to open next.

A simple way to create this experience: activate all surveys in the queue and set each to trigger after the very first survey is completed.

### 8.2 Sequential Queue (Fixed Order)

To enforce a specific completion order, cascade the trigger conditions — each survey triggers only when the immediately preceding one is completed. With auto-start disabled, participants see the overview after each survey showing their progress and the next available survey. With auto-start enabled, they flow directly from one survey to the next without seeing the overview.

### 8.3 Repeatable Surveys in the Queue

A survey can be made repeatable so participants can take it multiple times within the survey queue. Two conditions must both be met:

1. The instrument must be set as a repeatable instrument (configured in Project Setup — see [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md)).
2. The **"Repeat the survey"** option must be enabled in that survey's termination settings (Survey Settings → Survey Termination Options).

When both conditions are met, the survey queue overview shows all previously completed instances of that survey and a button to take it again. A repeat button also appears at the end of the survey itself, so repeatable surveys can be taken again even without using the queue overview screen.

### 8.4 Save and Return Surveys in the Queue

If a survey has the **Save and Return Later** feature enabled and the participant has previously completed it, an **Edit Response** button appears in the survey queue overview next to that survey's entry. This allows participants to reopen and modify a completed survey from the queue without needing to know the direct survey link.

This behavior also applies to completed instances of repeatable instruments.

> **Note:** If a survey requires a return code for reopening (a sub-option of Save and Return Later), the participant will need that code to proceed. Ensure the code was communicated to them at the time of their original submission.

---

## 9. Common Questions

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

**Q: Can a completion trigger in the survey queue reference a survey from a different arm?**

**A:** Yes. In the CSV, the `condition_surveycomplete_event_name` column accepts any valid event name in the project, including events that belong to a different arm than the survey being configured. This is useful in multi-arm longitudinal projects where downstream surveys in one arm should unlock only after a baseline survey in another arm has been completed. Set up the combination trigger (completion + logic, joined by AND) so the arm-specific logic condition also gates which participants see the survey.

**Q: I have a conditional arm where the first survey should only appear when a screening field meets a condition. The survey never shows in the queue. What is wrong?**

**A:** The most common cause is a completion trigger on the first survey in the arm. If there is no prior survey for that arm's participants to complete, a completion trigger will never fire. For the entry-point survey in a conditional arm, leave both `condition_surveycomplete_form_name` and `condition_surveycomplete_event_name` blank and rely solely on the logic trigger. Set `condition_andor` to `AND` (REDCap requires a value even when only one trigger type is active). Subsequent surveys in the arm can then use a combination trigger — the entry-point survey's completion plus the same or a related logic condition.

---

## 10. Common Mistakes & Gotchas

**Forgetting to activate a survey in the queue.** A survey that is enabled as a survey in the project is not automatically included in the survey queue. Each survey must be explicitly activated in the queue interface or via the CSV upload. An inactivated survey will never appear in the queue regardless of whether its trigger conditions are met.

**Using auto-continue alongside the survey queue.** The auto-continue setting (in Survey Settings → Survey Termination Options) and the survey queue can conflict. Documented interactions between the two have produced unexpected behavior. If you are using the survey queue, disable auto-continue for all surveys in the project.

**Designing trigger conditions without considering instrument order.** When multiple surveys trigger simultaneously with auto-start enabled, REDCap uses instrument order (in the Online Designer) as the tiebreaker. If you have not intentionally ordered your instruments to match your intended flow, participants may start the wrong survey. Review instrument order in the Online Designer before going live.

**Expecting the survey queue icon to appear for anonymous participants.** The survey queue column in the participant list is only clickable in identified mode. Anonymous records show no clickable queue icon. Enable identified mode via participant identifier or a designated email field.

**Omitting the survey queue link from the ASI message for multi-survey time points.** If you use ASIs to kick off each time point and the survey queue to guide participants through subsequent surveys, the ASI message must include `[survey-queue-url]` or `[survey-queue-link:Custom Text]` — not just `[survey-url]`. Sending `[survey-url]` only takes the participant to a single survey, bypassing the queue entirely.

**Adding a completion trigger to the first survey in a conditional arm.** In a multi-arm project where participants are routed by screening logic, the entry-point survey in each conditional arm has no prior survey to complete. Assigning a completion trigger to it means the trigger can never fire and the survey will never appear in the queue. Leave the completion trigger columns blank for any survey that is the first in its arm's flow, and use a logic-only trigger instead.

**In multi-arm routing, surveys that share the same completion trigger all unlock simultaneously.** When several surveys in an arm are all configured to trigger after the same preceding survey completes (and the logic condition is also met), they become available at the same moment. If all of them have `auto_start=1`, REDCap will auto-launch whichever appears first in the instrument list in the Online Designer, then chain to the next in order. If your instrument order in the Online Designer does not match your intended survey flow, participants will be routed through the surveys in the wrong sequence. Review and adjust instrument order before going live with this pattern.

---

### API Access

> **Note:** The following REDCap API methods provide programmatic access to this functionality. API usage is an advanced feature that requires knowledge of computer programming or access to a developer resource. See [RC-API-01 — REDCap API](RC-API-01_REDCap-API.md) for authentication, token management, and setup.

- **[RC-API-41 — Export Survey Queue Link API](RC-API-41_Export-Survey-Queue-Link.md)** — programmatically retrieve the Survey Queue link for a specific record

---


## 11. Related Articles

- [RC-SURV-06 — Automated Survey Invitations (ASI)](RC-SURV-06_Automated-Survey-Invitations.md)(email-based automated invitation scheduling; use with survey queue for time-point studies)
- [RC-SURV-05 — Participant List & Manual Survey Invitations](RC-SURV-05_Participant-List-and-Manual-Survey-Invitations.md) (manual invitation workflow; participant list survey queue column)
- [RC-SURV-03 — Survey Settings: Behavior, Access & Termination](RC-SURV-03_Survey-Settings-Behavior-Access-and-Termination.md) (auto-continue and Save and Return Later settings)
- [RC-BL-01 — Branching Logic: Overview & Scope](RC-BL-01_Branching-Logic-Overview-and-Scope.md) (logic syntax for queue trigger conditions)
- [RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md) (writing logic conditions)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md) (events and arms)
- [RC-LONG-02 — Repeated Instruments & Events Setup](RC-LONG-02_Repeated-Instruments-and-Events-Setup.md) (prerequisite for repeatable surveys in the queue)
- [RC-PIPE-03 — Smart Variables Overview](RC-PIPE-03_Smart-Variables-Overview.md) (`[survey-queue-url]`, `[survey-queue-link]`)
- [RC-FD-05 — Codebook](RC-FD-05_Codebook.md) (finding instrument unique names for CSV upload)

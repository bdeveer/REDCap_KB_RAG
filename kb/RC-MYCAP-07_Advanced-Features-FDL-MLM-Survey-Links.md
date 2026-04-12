RC-MYCAP-07

**MyCap: Advanced Features — Form Display Logic, MLM, and Survey Links**

| **Article ID** | RC-MYCAP-07 |
|---|---|
| **Domain** | MyCap Mobile App |
| **Applies To** | Projects with MyCap enabled; feature-specific version requirements noted per section |
| **Prerequisite** | RC-MYCAP-02 — Designing Instruments for MyCap |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-FDL-01 — Form Display Logic; RC-MLM-01 — Multi-Language Management; RC-MYCAP-03 — Task Scheduling |

---

# 1. Overview

This article covers three advanced MyCap features that extend the base task-and-schedule model: Form Display Logic (FDL) for conditional task display, Multi-Language Management (MLM) for translating the app experience, and Survey Links for embedding REDCap surveys inside a MyCap task. Each feature has its own version requirements, configuration steps, and limitations specific to the MyCap context. These features can be combined — for example, an MLM-translated project can use Survey Links to return results, with FDL controlling when the results task appears.

---

# 2. Feature 1: Form Display Logic (FDL) in MyCap

### 2.1 Overview

Form Display Logic (FDL) controls which tasks appear in a participant's MyCap task list based on conditions evaluated from the REDCap project data. FDL is a project-level feature — not MyCap-specific — but MyCap has additional constraints and limitations on how FDL behaves in the app context.

- **Minimum REDCap version:** v15.5.1
- **Configuration:** MyCap > Additional Settings > Enable support for MyCap App

> **Note:** FDL must be explicitly enabled for MyCap. Enabling FDL for the project does not automatically enable it for MyCap — the "Enable support for MyCap App" checkbox is a separate step.

### 2.2 How FDL Works in MyCap

When FDL is enabled for MyCap, each instrument can have display logic that evaluates conditions from the REDCap project (e.g., responses to earlier tasks, data entered by study staff). If the condition is true, the task appears in the participant's app; if false, the task is hidden.

FDL conditions can reference:
- Fields in any instrument in the project (not just MyCap-enabled instruments).
- Data entered by the study team in REDCap (e.g., a flag set by a coordinator after reviewing data).
- Responses the participant has submitted through MyCap.

**Example use cases:**
1. Show a follow-up symptom task only if the participant reported a specific symptom in an earlier task.
2. Display a results task only after the study team has entered a score in REDCap.
3. Show a supplementary questionnaire only for participants in a specific study arm.
4. Use baseline responses to customize which tasks a participant sees throughout the study.
5. Gate the release of subsequent assessments until an earlier one is submitted.

### 2.3 MyCap-Specific FDL Limitations

FDL behavior in MyCap differs from standard REDCap FDL in the following ways:

| Limitation | Details |
|---|---|
| Requires internet connection to evaluate | FDL conditions are evaluated against the REDCap server. The participant must be online when the app checks for available tasks. Offline evaluation is not supported. |
| Repeating instruments: use `[last-instance]` | When referencing a repeating instrument in an FDL condition, use the `[last-instance]` qualifier to reference the most recent instance. Without it, the logic may evaluate incorrectly. |
| Longitudinal projects: include arm name | In longitudinal projects, FDL expressions must include the event's arm name in the field reference syntax to correctly identify the event. |
| No Retroactive Completion for FDL-triggering tasks | Instruments that trigger FDL conditions cannot use the Retroactive Completion feature. If your workflow requires retroactive completion, do not use that instrument as an FDL trigger. |
| No Infinite schedule on FDL-controlled tasks | Tasks governed by FDL cannot use the Infinite schedule type. Use a One-Time, Repeating, or Fixed schedule instead. |

### 2.4 FDL Publishing Behavior

**FDL changes do not require publishing.** Updates to Form Display Logic conditions take effect the next time the participant opens the app and syncs — no manual publish step is needed. This is different from instrument and schedule changes, which require publishing.

### 2.5 Configuring FDL for MyCap

1. Ensure FDL is enabled for the project: **Project Setup > Enable optional modules > Form Display Logic**.
2. Enable FDL specifically for MyCap: **MyCap > Additional Settings > Enable support for MyCap App**.
3. Go to **Project Setup > Form Display Logic** and configure the display conditions for each instrument.
4. For MyCap-specific instruments, test using a test participant record (see RC-MYCAP-08 — Testing MyCap).

---

# 3. Feature 2: Multi-Language Management (MLM) in MyCap

### 3.1 Overview

Multi-Language Management (MLM) allows projects to present MyCap content in multiple languages. Participants select their preferred language when they first join the app, and all translated content is displayed in their chosen language.

- **Minimum REDCap version:** v14.5.4
- **Minimum MyCap app version:** v2.1.0
- **Supported languages:** 20, identified by IETF language tags

### 3.2 Supported Languages

| Language | Language ID |
|---|---|
| English (US) | en-US |
| Spanish (Spain) | es-ES |
| Chinese (Simplified) | zh-CN |
| Chinese (Traditional) | zh-TW |
| French | fr-FR |
| German | de-DE |
| Italian | it-IT |
| Japanese | ja-JP |
| Korean | ko-KR |
| Portuguese (Brazil) | pt-BR |
| Portuguese (Portugal) | pt-PT |
| Russian | ru-RU |
| Arabic | ar-SA |
| Dutch | nl-NL |
| Polish | pl-PL |
| Swedish | sv-SE |
| Danish | da-DK |
| Finnish | fi-FI |
| Norwegian | nb-NO |
| Turkish | tr-TR |

> **Note:** Language IDs must match the codes in this table exactly. Mismatched language IDs will cause the language to fail to appear in the app.

### 3.3 All-or-Nothing Language Enabling for MyCap

In the standard REDCap MLM interface, you can enable different languages for different instruments. For MyCap, language enabling is **all-or-nothing**: when you enable a language for MyCap, it applies to all MyCap-enabled instruments in the project. You cannot enable a language for some MyCap tasks but not others.

### 3.4 What Needs to Be Translated for MyCap

MLM translation for a MyCap project requires translating content in two tabs in the MLM interface:

**Forms/Surveys tab:**
- All field labels, options, and descriptive text for MyCap-enabled instruments.
- Standard REDCap MLM translation workflow applies.

**MyCap tab:**
- **App Title:** The project name displayed in the app.
- **Baseline Date Task:** The text shown to participants when they are prompted to enter their baseline date (if the project uses baseline date).
- **About pages:** Translated About page content.
- **Contacts:** Translated contact names and roles.
- **Links:** Translated link labels.

### 3.5 Participant Language Selection

When a participant joins a MyCap project that has MLM enabled:
1. The app presents the list of available languages.
2. The participant selects their preferred language.
3. All translated content (instruments, App Settings content) is displayed in the chosen language.

The participant's language selection is stored in their record and persists across sessions. The participant can change their language from the app's settings.

### 3.6 MLM Publishing Behavior

**MLM changes do not require publishing.** When you save updated translations in the MLM interface, participants see the updated content on their next app sync. No manual publish step is needed for MLM changes.

---

# 4. Feature 3: Survey Links in MyCap

### 4.1 Overview

Survey Links allow you to embed a REDCap survey link inside a MyCap task. When a participant opens the task in the app, they are directed to a standard REDCap survey in their mobile browser, complete it, and return to MyCap. This feature enables capabilities that are not available natively in MyCap instruments.

- **Minimum REDCap version:** v15.8.4
- **Minimum MyCap app version:** v2.6.0

### 4.2 Use Cases

**Use case 1: Data collection with calculated fields or piping**
MyCap instruments do not support calculated fields or piping. By embedding a Survey Link in a MyCap task, you can direct participants to a standard REDCap survey where calculated fields and piping work normally. The survey collects the data; the participant returns to MyCap after completing it.

**Use case 2: Returning results to participants**
After the study team or an automated calculation generates a result (e.g., a composite score), that result can be piped into a REDCap survey and displayed to the participant via a Survey Link task. Because the REDCap survey supports piping, the participant sees their personalized result.

### 4.3 Smart Variables for Survey Links

Two smart variables generate the link to include in the MyCap task:

| Smart Variable | Output |
|---|---|
| `[survey-link:instrument_name]` | Hyperlinked URL to the specified survey; uses the survey URL as the link text |
| `[survey-link:instrument_name:Custom Text]` | Hyperlinked URL with custom display text |

Replace `instrument_name` with the REDCap variable name (unique instrument name) of the target survey.

**Example:** To link to a survey named `results_display`:
```
[survey-link:results_display:View Your Results]
```

### 4.4 Preventing Accidental Task Completion

When a participant opens a Survey Link task in MyCap, they may complete the survey and return to the task — then accidentally tap "Done" on the MyCap task before completing the survey. To prevent this:

**Add an Instruction Step** at the top of the MyCap instrument that contains the Survey Link. The Instruction Step reminds participants to complete the linked survey before marking the MyCap task as done.

Example instruction text:
```
Please tap the link below to complete your assessment. After the survey
opens in your browser and you submit it, return to this screen and tap Done.
```

### 4.5 Configuring a Results Task

A common pattern for returning results to participants:

1. Create a REDCap survey instrument that displays the calculated result (using piping to pull the result into a descriptive text field or field note).
2. In MyCap, create a task that contains a field with the `[survey-link:results_instrument:View Your Results]` smart variable.
3. Set the results task to an **Infinite** schedule (so it is always available once released).
4. Use **Form Display Logic** (see Section 2) to control when the results task becomes visible — for example, show it only after the study team has entered the final score in REDCap.

---

# 5. Common Questions

**Q: Does FDL in MyCap work when the participant is offline?**

**A:** No. FDL conditions are evaluated against the REDCap server and require an internet connection. When offline, the app displays the last known task state. The task list is re-evaluated the next time the participant syncs with an internet connection.

**Q: Can I translate Active Tasks with MLM?**

**A:** The text content of MyCap instruments and App Settings can be translated. Active Task interface elements (built-in prompts, instructions within the task) follow the device language setting and the available localizations of the MyCap app — they are not configurable through REDCap's MLM interface.

**Q: Can I use Survey Links for data entry instead of native MyCap tasks?**

**A:** Yes. Survey Links are a supported workaround for situations where MyCap's native instrument limitations (no piping, no calculated fields) would prevent the needed data capture. The survey is a standard REDCap survey with all standard capabilities.

**Q: Do Survey Links work if the participant is offline?**

**A:** No. Survey Links open a REDCap survey in the device's browser and require internet connectivity. Survey Links are not suitable for offline data collection.

**Q: Does MLM require a separate publish step?**

**A:** No. MLM changes take effect on the participant's next app sync without a publish step. This is one of the few MyCap changes that does not require publishing.

**Q: Can I use FDL to show different task sequences for different participants?**

**A:** Yes. FDL logic can reference any field in the project, including fields set by the study team in REDCap. This allows coordinators to set a flag in REDCap that triggers a different task sequence in the participant's app.

**Q: What happens if I set an Infinite schedule on an FDL-controlled task?**

**A:** Infinite schedule is not supported for tasks governed by FDL. If you assign an Infinite schedule to an FDL-controlled task, the FDL will not function correctly. Use One-Time, Repeating, or Fixed schedule instead.

---

# 6. Common Mistakes & Gotchas

**Not enabling FDL for MyCap specifically.** Enabling FDL for the project in Project Setup does not automatically enable it for MyCap. You must also check "Enable support for MyCap App" in MyCap Additional Settings. If participants see tasks regardless of FDL conditions, check this setting.

**Referencing a repeating instrument in FDL without `[last-instance]`.** FDL expressions for repeating instruments that do not use the `[last-instance]` qualifier will evaluate against instance 1, not the most recent instance. This causes tasks to appear or not appear incorrectly. Always include `[last-instance]` when the referenced field is in a repeating context.

**Using incorrect Language IDs in MLM.** The language IDs for MyCap must match the IETF codes exactly (e.g., `en-US`, not `en`, `English`, or `EN-US`). Mismatched codes cause the language to fail silently — the language option may not appear in the app.

**Forgetting to translate the MyCap tab in MLM.** The MLM interface has a separate MyCap tab for translating App Title, Baseline Date Task text, About pages, Contacts, and Links. Studies that translate the Forms/Surveys tab but not the MyCap tab will have translated instruments but untranslated app interface content.

**Not adding an Instruction Step before a Survey Link task.** Without instructions, participants often complete the linked survey but fail to return to MyCap and submit the task. The task remains open indefinitely. Always include an Instruction Step explaining that the participant should return to the MyCap task after completing the survey.

**Setting a Survey Links task to Infinite without FDL to control release.** A results task on Infinite schedule is always visible to participants. If the results are not yet available, participants will see the results link before there is any content. Use FDL to gate the results task — only make it visible after the result has been calculated and entered in REDCap.

---

# 7. Related Articles

- RC-MYCAP-02 — Designing Instruments for MyCap (field design and annotations)
- RC-MYCAP-03 — Task Scheduling (schedule types, FDL interaction with Infinite schedule)
- RC-MYCAP-08 — Testing MyCap (testing FDL, MLM, and Survey Links)
- RC-FDL-01 — Form Display Logic (full FDL reference for standard REDCap use)
- RC-MLM-01 — Multi-Language Management (full MLM reference)
- RC-PIPE-16 — Smart Variables: MyCap (MyCap-specific smart variable reference)

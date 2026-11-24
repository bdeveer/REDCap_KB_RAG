---
id: RC-RAND-01
title: REDCap Randomization – Concepts & Terminology
domain: Randomization
applies_to:
- All REDCap project types with Randomization module enabled
- intended for PIs, Study Coordinators, and Project Builders planning a randomized
  study
requires: REDCap v15.4.4+ (Randomization 2.0 — automatic trigger options)
verified_against: REDCap v17.6.5 (Standard) / v17.3.31 and v16.0.61 (LTS) — randomization
  behaviour checked against source code; pages not re-captured
prerequisites:
- 'Foundational REDCap knowledge required: project setup, instruments, user rights,
  and longitudinal mode basics'
version: '1.3'
last_updated: 2026-11
related:
- id: RC-RAND-02
  title: Randomization Setup Guide
- id: RC-RAND-03
  title: Working with & Managing Randomization
- id: RC-USER-01
  title: 'User Rights: Overview & Three-Tier Access'
- id: RC-DAG-01
  title: Data Access Groups
- id: RC-CC-06
  title: 'Control Center: Modules & Services Configuration'
- id: RC-NAV-UI-02
  title: Project Menu Reference
- id: RC-USER-03
  title: 'User Rights: Configuring User Privileges'
- id: RC-MOB-01
  title: REDCap Mobile App
tags:
- randomization
synonyms:
- what is randomization in redcap
- randomization terminology and concepts
- how does stratified randomization work
- allocation table and randomization model explained
- plan a randomized study in redcap
- blocked randomization basics
- randomization strata and groups concepts
- understand randomization before setup
- randomize records into separate arms with a pre-randomization arm
- can the randomization dashboard unblind a study
- can development and production randomization allocation tables be the same
- what randomization model settings can change after production
---

# 1. Overview

## What is this?

This document covers the concepts and terminology required to understand
and plan REDCap randomization. It is intentionally separated from the
setup procedure ([RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md)) because these concepts must be understood
before any configuration decisions are made. Attempting to set up
randomization without this foundation is one of the most common causes
of failed or misconfigured randomization models.

## Why does it matter?

REDCap's randomization module uses standard statistical terminology
that is unfamiliar to many research coordinators and project builders.
The module's setup wizard asks you to make consequential decisions ---
some of which cannot be changed without erasing and rebuilding the
entire model in Development, and cannot be changed at all once the
project is in Production — based on these concepts. Understanding them upfront
prevents costly mistakes.

**Important note about Randomization 2.0**

The introduction of Randomization 2.0 in recent REDCap versions
significantly expanded the feature's capabilities (including automatic
trigger options). This document and its companion articles are written
for REDCap 15.4.4+. If your institution runs an older version, some
features described here may not be available.

---

# 2. Learning Objectives

After reviewing this document, the user will be able to:

- Define randomization and explain why it is used in research

- Explain the difference between stratified and unstratified
    randomization

- Describe what an allocation table is and why REDCap uses one instead
    of a live random number generator

- Distinguish between open (unblinded) and blinded randomization and
    their implications for variable setup

- Explain the three randomization-specific user rights in REDCap and
    when to assign each

- Identify the constraints that longitudinal project design places on
    randomization setup

---

# 3. Core Concepts

**What is randomization?**

Randomization is the process of randomly assigning study participants
(records in REDCap) to different groups — typically a control group
and one or more intervention groups. The randomness of the assignment is
what removes selection bias and ensures groups are comparable.

In REDCap, randomization most commonly supports Randomized Clinical
Trials (RCTs), but it can be used for any scenario requiring random
group assignment — including assigning participants to different
survey order groups.

> **Note:** *For the statistical rationale behind randomization, consult
> your institution's statistician or biostatistics department. REDCap
> handles the mechanics; study design decisions belong to the research
> team.*

**Key Terminology Glossary**

These terms appear directly in the REDCap randomization setup interface.
You must understand them before configuring a randomization model.

| **Term** | **Definition** |
| --- | --- |
| **Cohorts / Groups / Sub-groups** | The different groups records are divided into. These terms are interchangeable in REDCap. Examples: placebo vs. intervention; control vs. intervention A vs. intervention B. |
| **Stratification (Stratified Randomization)** | A method of ensuring each randomization group has a similar composition across key variables. For example, stratifying by sex prevents all men from ending up in the control group. REDCap supports up to 14 stratification variables, all of which must be single-choice field types (dropdown, radio button, yes/no, true/false). Calculated fields cannot be strata; see the Q&A below for the workaround. |
| **Sites / Groups (Multi-site)** | A special form of stratification that separates randomization by study site. The site can come from REDCap's Data Access Group (DAG) feature or from a dedicated single-choice site field. Useful for multi-site trials where site membership should influence allocation. |
| **Blinding (Blinded Randomization)** | A setup where even the study team does not know which group a participant is assigned to. Requires a plain text randomization variable (no dropdown) so the assigned value is opaque to the UI. The key for decoding group assignments is normally kept outside REDCap and shared only with designated unblinded individuals (e.g., pharmacy staff). A blinded allocation table may optionally include the group column; if the statistician includes it, the key is stored inside REDCap, where administrators can see it and it appears in allocation table downloads. Leave the group column out if the key must stay outside REDCap. |
| **Open Randomization (Unblinded)** | A setup where the study team can see which group each participant is assigned to. Uses a dropdown, radio button, yes/no or true/false randomization variable with group labels visible in the interface. |
| **Allocation Table** | A pre-generated list of randomization assignments in a specific sequence. REDCap does not generate random assignments on the fly — it works down this list in order, assigning each new randomization to the next available slot. Allocation tables are typically generated by a statistician or statistical software. REDCap provides a downloadable template tailored to your model's settings. The template shows the required format only; its rows must not be used as the allocation for a production study. |
| **Randomization Variable** | The REDCap field that stores the randomization result for each record. For open randomization: a dropdown, radio button, yes/no or true/false field. For blinded randomization: a plain text field with no validation and no @CALCTEXT (validated and @CALCTEXT text fields are not offered as blinded targets). This field must be created before setting up the randomization model. Once a model uses it, the field (and every stratification field) is protected: it cannot be deleted in the Online Designer, a data dictionary upload that drops it is rejected, and a blinded target cannot be given validation. |
| **Randomization Model** | The configuration object in REDCap that defines how randomization works for a given variable and event — including stratification, site/DAG setting, blinding, trigger type, and allocation table. A project can hold more than one model; each has exactly one target event and its own allocation tables. The model's core settings (randomization variable, event, strata and site/DAG setting) lock as soon as the model is saved, even in Development. In Development the model can be erased and rebuilt; in Production nobody, administrators included, can change or erase it through the interface. The trigger option and trigger logic stay editable by users with the Setup right, including in Production. See [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md) for what administrators can still change. |
| **Allocation Slots** | Individual entries in the allocation table. Each slot corresponds to one randomization event. Running out of slots mid-study requires administrator intervention to append more allocations. |
| **Smart Variables (Randomization)** | REDCap system variables that capture metadata about the randomization event: \[rand-time\] (server timestamp), \[rand-utc-time\] (UTC timestamp), \[rand-number\] (the randomization number in a blinded model; in an open model it returns the optional alternate number, never the group, and is blank if none was uploaded). To show the group, pipe the randomization variable itself. Useful for audit trails and piping into alerts or reports. See [RC-PIPE-13 — Smart Variables: Randomization](RC-PIPE-13_Smart-Variables-Randomization.md). |

**Open vs. Blinded Randomization — Decision Guide**

This is one of the most consequential decisions in randomization setup.
It affects your variable type, user rights configuration, and workflow
outside REDCap.

| **Factor** | **Open (Unblinded)**                                **Blinded** |
| --- | --- |
| **Randomization variable type** | Dropdown, radio button, yes/no or true/false with group labels          Plain text field, no validation, no @CALCTEXT — stores an opaque code |
| **Group visible in REDCap UI?** | Yes — study team can see group assignment         No — team sees only a code; key kept outside REDCap (unless the group column is included in the allocation table) |
| **Allocation table format** | Group labels match dropdown options                 Group codes defined by statistician; key held separately |
| **Who needs the decode key?** | Not applicable                                      Only designated unblinded individuals (e.g., pharmacy). The **Dashboard** shows only used/unused counts for a blinded model, never the group. The real risks are allocation table downloads (the **Setup** right before go-live, administrators in Production) and building a "blinded" study on a dropdown or radio field |
| **Complexity** | Simpler to setup and manage                         More complex; requires external process for key management |
| **Common use case** | Most open-label trials, operational randomization   Double-blind RCTs, placebo-controlled trials |

**Allocation Tables — What you need to know**

REDCap does not generate randomization assignments dynamically. Instead
it works through a pre-generated allocation table — a sequenced list
of group assignments — in order. This approach is standard practice in
clinical trials because it allows the randomization sequence to be
pre-audited and reproduced.

- **Who generates the table?:** Typically a statistician or dedicated
    statistical software (SAS, R, nQuery, etc.). REDCap provides a
    downloadable template tailored to your model's configuration that
    the statistician can use as a guide. The template's own rows are
    example data, not a usable allocation: never upload them as the
    production table.

- **Table size:** Always generate more slots than you expect to need.
    Account for dropout, screen failures, and protocol deviations. A
    common rule of thumb: at minimum double your target enrollment per
    group. There is no functional upper limit to allocation table size.

- **Development vs. production tables:** REDCap maintains separate
    allocation tables for development and production modes. The two
    tables cannot be identical: while the project is in Development,
    REDCap rejects an upload that exactly matches the other table, so
    ask the statistician for two different sequences. Test
    randomizations in development mode consume development slots only.

- **Running out of slots:** Only a REDCap administrator can append
    additional allocations to a production allocation table. This is a
    recoverable situation, but an avoidable one with proper planning.
    In Production, users cannot edit the rows already in the table.
    Administrators can edit individual rows (un-randomize a record,
    manually randomize one, mark a slot unavailable or available
    again, or change the group or number of an unused slot); each
    change requires a reason and is logged. See
    [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md).

**Randomization User Rights**

Enabling randomization adds three new user rights to every user and role
in the project. These must be assigned deliberately — they default to
off. The one exception: if **Randomization** is ticked when the project
is created, the project creator gets all three automatically. Enabling
the module later in Project Setup grants the rights to nobody, so
someone must assign them (including to themselves) on the User Rights
page. The **Randomization** link in the project menu appears only for
users with the Setup or Dashboard right.

| **Right** | **What it allows**                                                                                                             **Assign to** |
| --- | --- |
| **Setup** | Configure the randomization model — define stratification, select randomization variable, upload and download allocation tables, and change the trigger option and trigger logic (also in Production). Before the project moves to Production, a Setup user can download both the development and production tables, and so can know the production sequence in advance; in Production only administrators can download them. Downloads never contain record names: they reveal the sequence, not which record got which slot.          Project builders, study coordinators involved in setup. Restrict after setup is complete. |
| **Randomize** | Click the Randomize button to manually randomize a record. Not required if using the 'all users' automatic trigger option. **Caution:** the randomization dialog shows the stratification fields with their current values, even if the user has no form-level rights to those fields. On an instrument where the user has **No Access**, the stratum is shown but disabled (it cannot be set); with **Read Only** access the user can set it. If a stratum is PHI (e.g., location), this right exposes it.   Data entry staff who perform randomization. Project builders during testing. Not required for survey-only auto-randomization. |
| **Dashboard** | View the randomization dashboard — see allocation counts, used/remaining slots, and assigned records. For a blinded (text-field) model it shows used/unused counts per stratum (and DAG) only, never the group, so it cannot unblind. For an open model it shows the group, which is already visible on the record. Administrators can open a per-slot view that shows the allocated values.                        PIs, statisticians, data coordinators, project builders. Anyone needing to monitor randomization progress. |

**Longitudinal Projects and Randomization**

Randomization in a non-longitudinal project is straightforward. In a
longitudinal project, the design choices you make for arms and events
directly constrain what randomization can do. Understand these rules
before building your longitudinal framework:

- **Single-arm longitudinal projects:** If all cohorts follow the same
    data collection path, a single-arm project works fine. Use branching
    logic keyed to the randomization variable to differentiate the
    experience between groups.

- **One randomization event per model:** Each randomization model has
    exactly **one target event**, so within a model a record is
    randomized once, counting all arms. REDCap's built-in FAQ states a
    stricter rule (one event per randomization field across all arms),
    but what the system actually enforces is that each variable + event
    pair is used by only one model. A second model can therefore use
    the same variable on a different event (e.g., an event in arm 2),
    with its own allocation table.

- **Multi-arm longitudinal projects:** If cohorts require completely
    separate arms (e.g., intervention arm vs. control arm), REDCap
    cannot automatically move records between arms based on
    randomization. The documented workaround is a
    **pre-randomization arm**: put eligibility, demographics and every
    form up to and including the randomization form in one arm. After
    randomization, staff add the record to the study arm matching its
    assignment (a record can belong to several arms). Caveat: the
    Scheduling module schedules a record's events in one arm only, so
    this pattern is awkward if you rely on scheduling. If neither fits,
    use a single-arm design with branching logic, or randomize outside
    REDCap.

- **Per-arm randomization:** If you have multiple arms, you can set up
    a separate randomization model for each arm. Each model has its own
    target event and allocation table; it can use its own randomization
    variable or reuse the same variable on that arm's event. A separate
    variable per arm is usually easier to report on.

- **Randomization form at later events:** If the instrument holding the
    randomization field is also designated on later events (e.g., annual
    visits), the field is only filled on the randomization event. Reports
    and logic must read it from that event (e.g.,
    `[baseline_arm_1][rand_group]`); read from a later event it is
    blank, and a randomized participant looks un-randomized.

- **Event placement matters:** The randomization variable must be
    assigned to a specific event. This event selection is locked once
    the model is saved, even in Development. If you later need to move
    the randomization variable to a different event, you must erase and
    rebuild the entire model, which is possible only while the project
    is in Development. Once a model exists, the project cannot be moved
    back from Production to Development, even by an administrator.

- **Saving the model erases test values:** When the model is saved,
    any values already entered in the randomization variable (e.g., from
    early testing) are erased. See [RC-RAND-02](RC-RAND-02_Randomization-Setup.md)
    step 8d.

> **Note:** *Set up at least the framework of your longitudinal model
> (arms and events) before configuring randomization. You can refine
> events afterward as long as you do not change the event containing the
> randomization variable.*

---

# 4. Questions & Answers

**Q: What is the difference between stratified and unstratified randomization?**

Unstratified randomization assigns participants purely at random with no constraints. Stratified randomization ensures that each randomization group has a similar composition across key variables (e.g., sex, age group, disease severity). For example, stratifying by sex prevents all men from ending up in the control group by accident. REDCap supports up to 14 stratification variables, all of which must be single-choice field types (dropdown, radio button, yes/no, true/false).

**Q: What is an allocation table and why doesn't REDCap just generate random assignments on the fly?**

An allocation table is a pre-generated, sequenced list of group assignments that REDCap works through in order. REDCap does not generate randomization assignments dynamically because allocation tables allow the randomization sequence to be pre-audited and reproduced — a standard practice in clinical trials. This approach ensures the sequence can be reviewed for bias and validated by a statistician before data collection begins.

**Q: What is the difference between open and blinded randomization?**

Open (unblinded) randomization is a setup where the study team can see which group each participant is assigned to. It uses a dropdown, radio button, yes/no or true/false randomization variable with group labels visible in the interface. Blinded randomization is a setup where even the study team does not know which group a participant is assigned to; it requires a plain text randomization variable with no validation and no @CALCTEXT, so the assigned value is opaque. The key for decoding group assignments is normally kept outside REDCap and shared only with designated unblinded individuals (e.g., pharmacy staff). A blinded allocation table may optionally include the group column; if it does, the key is stored in REDCap and visible to administrators and in allocation table downloads, so leave that column out if the key must stay outside REDCap.

**Q: Can I randomize records into different arms in a multi-arm longitudinal project?**

Not automatically. REDCap cannot move records between arms based on randomization, and each randomization model randomizes on exactly one event. The documented workaround is a pre-randomization arm that holds eligibility and the randomization form; after randomization, staff add the record to the study arm that matches its assignment. Note that the Scheduling module schedules a record's events in one arm only. Alternatives are a single-arm design with branching logic keyed to the randomization variable, or randomizing outside REDCap. You can also set up a separate randomization model for each arm. Each model has one target event and its own allocation table. REDCap's built-in FAQ says a randomization field can randomize on only one event across all arms, but the system only requires each variable + event pair to be unique, so a second model can reuse the same variable on an event in another arm.

**Q: Can I stratify on a calculated field (e.g., an age group derived from date of birth)?**

No. Strata must be single-choice fields (dropdown, radio, yes/no, true/false); calculated fields are not allowed. The workaround is to add a single-choice field next to the calculated field, have staff fill it in from the calculated value, and stratify on that field. Check that the two agree before randomizing.

**Q: Can I randomize from the REDCap Mobile App?**

No. The Mobile App collects data offline and cannot reach the allocation table, so it does not show the Randomize button. Randomize on the web. See [RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md).

**Q: What are the three randomization-specific user rights and who should have them?**

The three rights are: (1) **Setup** — configure the randomization model (assign to project builders and study coordinators involved in setup; restrict after setup is complete); (2) **Randomize** — click the Randomize button to manually randomize a record (assign to data entry staff who perform randomization, and project builders during testing; not required if using automatic trigger options); and (3) **Dashboard** — view the randomization dashboard with allocation counts and assigned records (assign to PIs, statisticians, data coordinators, and anyone needing to monitor progress). All three default to off; only the project creator gets them automatically, and only if Randomization was ticked when the project was created. In a blinded study, Dashboard shows used/unused counts only, never the group, so it cannot unblind; the unblinding risks are allocation table downloads (Setup users before go-live, administrators in Production) and building a "blinded" study on a dropdown or radio field. Randomize shows the strata fields in the dialog even without form rights to them (disabled on No Access instruments, editable with Read Only access), which matters if a stratum is PHI.

**Q: What happens if the allocation table runs out of slots before enrollment is complete?**

Only a REDCap administrator can append additional allocations to a production allocation table. This is a recoverable situation but an avoidable one with proper planning. To prevent this, generate at minimum double your target enrollment per group and account for dropout, screen failures, and protocol deviations. Consult your statistician for the appropriate buffer for your specific design.

**Q: Can I upload the same allocation table to development and production?**

No. While the project is in Development, REDCap rejects an allocation table upload that exactly matches the table already uploaded for the other mode. Ask the statistician for two different sequences: a test sequence for development and the real sequence for production.

**Q: What can still be changed in a randomization model after the project moves to production?**

Very little. The randomization variable, event, strata and site/DAG setting lock as soon as the model is saved, even in Development, where the model can still be erased and rebuilt. In Production nobody, administrators included, can change or erase the model through the interface, and the project cannot be moved back to Development. Users with the Setup right can still change the trigger option and trigger logic. Administrators can append allocation rows and edit individual production rows (un-randomize or manually randomize a record, mark a slot unavailable or available, change the group or number of an unused slot); each change requires a reason and is logged.

---

# 5. Common Mistakes & Gotchas

**Setting up randomization without consulting a statistician**

- **What happens:** Allocation tables are generated incorrectly,
    stratification variables are misconfigured, or table sizes are too
    small — often discovered only after real data collection has
    begun.

- **Prevention:** Involve a statistician before the randomization
    model is configured. Share the REDCap allocation table template with
    them early.

**Choosing the wrong randomization variable type**

- **What happens:** An open randomization is set up with a text field,
    or a blinded randomization is set up with a dropdown — causing
    either data integrity issues or unintended unblinding.

- **Prevention:** Open = dropdown, radio button, yes/no or true/false
    with group labels. Blinded = plain text field, no validation, no
    @CALCTEXT. Decide blinding status
    before creating the variable.

**Not accounting for dropout in allocation table size**

- **What happens:** The allocation table runs out of slots before
    enrollment is complete, requiring emergency administrator
    intervention to append more allocations — a disruptive and
    avoidable situation.

- **Prevention:** Generate at minimum double your target enrollment
    per group. Consult your statistician for the appropriate buffer for
    your specific design.

**Assuming arm switching is possible in longitudinal projects**

- **What happens:** A researcher designs a multi-arm longitudinal
    project expecting REDCap to automatically move randomized records
    between arms — this is not possible. Records cannot switch arms
    based on randomization outcomes.

- **Prevention:** Clarify this constraint during study design. If
    separate arms are required, use a pre-randomization arm and add
    each record to its study arm by hand after randomization; otherwise
    use a single-arm design with branching logic, or perform
    randomization outside REDCap.

---

# 6. Administrator Configuration

The Randomization module must be enabled at the system level by a REDCap administrator before it is available in any project. This is done in the Control Center under System Configuration → Modules/Services Configuration (see **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)**). When disabled, the Randomization option does not appear in Project Setup and the Randomize user right is not available.

Once the module is enabled system-wide, randomization is enabled per project by turning on the **Randomization** option in Project Setup → Optional modules. This needs the Project Design and Setup right; once the project is in Production, only an administrator can enable it. The three randomization rights (Setup, Randomize, Dashboard) are then assigned on the User Rights page; enabling the module here grants them to nobody, not even the user who enabled it.

> **See also:** [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)

---

# 7. Related Articles

- **[RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md):** Randomization Setup Guide — step-by-step
    configuration procedure

- **[RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md):** Working with & Managing Randomization — running,
    monitoring, and admin options

- **[RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md):** User Rights: Overview & Three-Tier Access — prerequisite for understanding the Randomize right and DAG-based site stratification

- **[RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md):** Data Access Groups — prerequisite for understanding DAG-based stratification and restricted randomization access

- **[RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md):** Longitudinal Projects — prerequisite for
    multi-event randomization setup

- **[RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md):** Control Center: Modules & Services Configuration — system-level Randomization enable/disable

- **[RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md):** what each randomization right exposes (unblinding, strata PHI)

- **[RC-MOB-01 — REDCap Mobile App](RC-MOB-01_REDCap-Mobile-App.md):** randomization is not supported in the Mobile App

- **[RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md):** Project Menu Reference — the Randomization application appears in the Applications section of the left menu when randomization is enabled for the project

---

# 8. Version & Change Notes

| **REDCap Version** | **Notes** |
| --- | --- |
| **15.4.4+** | Randomization 2.0 — adds automatic trigger options (trigger logic for users with Randomize rights; trigger logic for all users including survey respondents). This document is written for this version and has been verified compatible through REDCap 17. |
| **Pre-15.x** | Only manual randomization (Randomize button) available. Automatic triggers did not exist. Verify your installation version before configuring. |

REDCap LLM Knowledge Base \| [RC-RAND-01 — Randomization Concepts & Terminology](RC-RAND-01_Randomization-Concepts.md) \| Randomization Concepts &
Terminology

---

# 9. Related Articles

- [RC-RAND-02 — Randomization Setup Guide](RC-RAND-02_Randomization-Setup.md)
- [RC-RAND-03 — Working with & Managing Randomization](RC-RAND-03_Working-with-Randomization.md)
- [RC-USER-01 — User Rights: Overview & Three-Tier Access](RC-USER-01_User-Rights-Overview-and-Three-Tier-Access.md)
- [RC-DAG-01 — Data Access Groups](RC-DAG-01_Data-Access-Groups.md)
- [RC-LONG-01 — Longitudinal Project Setup](RC-LONG-01_Longitudinal-Project-Setup.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)
- [RC-NAV-UI-02 — Project Menu Reference](RC-NAV-UI-02_Project-Menu-Reference.md)

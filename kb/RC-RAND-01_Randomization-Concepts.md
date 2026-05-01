RC-RAND-01

**REDCap Randomization – Concepts & Terminology**

| **Article ID** | RC-RAND-01 |
| --- | --- |
| **Domain** | Randomization |
| **Applies To** | All REDCap project types with Randomization module enabled; intended for PIs, Study Coordinators, and Project Builders planning a randomized study |
| **Prerequisite** | Foundational REDCap knowledge required: project setup, instruments, user rights, and longitudinal mode basics |
| **Version** | 1.0 |
| **Last Updated** | 2025-01 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-RAND-02 — Randomization Setup Guide; RC-RAND-03 — Working with & Managing Randomization; RC-USER-01 — User Rights Overview; RC-DAG-01 — Data Access Groups; RC-CC-06 — Control Center: Modules & Services Configuration; RC-NAV-UI-02 — Project Menu Reference |

---

# 1. Overview

## What is this?

This document covers the concepts and terminology required to understand
and plan REDCap randomization. It is intentionally separated from the
setup procedure (RC-RAND-02) because these concepts must be understood
before any configuration decisions are made. Attempting to set up
randomization without this foundation is one of the most common causes
of failed or misconfigured randomization models.

## Why does it matter?

REDCap\'s randomization module uses standard statistical terminology
that is unfamiliar to many research coordinators and project builders.
The module\'s setup wizard asks you to make consequential decisions ---
some of which cannot be changed without deleting and rebuilding the
entire model — based on these concepts. Understanding them upfront
prevents costly mistakes.

**Important note about Randomization 2.0**

The introduction of Randomization 2.0 in recent REDCap versions
significantly expanded the feature\'s capabilities (including automatic
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
> your institution\'s statistician or biostatistics department. REDCap
> handles the mechanics; study design decisions belong to the research
> team.*

**Key Terminology Glossary**

These terms appear directly in the REDCap randomization setup interface.
You must understand them before configuring a randomization model.

| **Term** | **Definition** |
| --- | --- |
| **Cohorts / Groups / Sub-groups** | The different groups records are divided into. These terms are interchangeable in REDCap. Examples: placebo vs. intervention; control vs. intervention A vs. intervention B. |
| **Stratification (Stratified Randomization)** | A method of ensuring each randomization group has a similar composition across key variables. For example, stratifying by sex prevents all men from ending up in the control group. REDCap supports up to 14 stratification variables, all of which must be single-choice field types (dropdown, radio button, yes/no, true/false). |
| **Sites / Groups (Multi-site)** | A special form of stratification using REDCap\'s Data Access Group (DAG) feature to separate randomization by study site. Useful for multi-site trials where site membership should influence allocation. |
| **Blinding (Blinded Randomization)** | A setup where even the study team does not know which group a participant is assigned to. Requires a plain text randomization variable (no dropdown) so the assigned value is opaque to the UI. The key for decoding group assignments is stored outside REDCap and shared only with designated unblinded individuals (e.g., pharmacy staff). |
| **Open Randomization (Unblinded)** | A setup where the study team can see which group each participant is assigned to. Uses a dropdown or radio button randomization variable with group labels visible in the interface. |
| **Allocation Table** | A pre-generated list of randomization assignments in a specific sequence. REDCap does not generate random assignments on the fly — it works down this list in order, assigning each new randomization to the next available slot. Allocation tables are typically generated by a statistician or statistical software. REDCap provides a downloadable template tailored to your model\'s settings. |
| **Randomization Variable** | The REDCap field that stores the randomization result for each record. For open randomization: a dropdown or radio button field. For blinded randomization: a plain text field with no validation. This field must be created before setting up the randomization model. |
| **Randomization Model** | The configuration object in REDCap that defines how randomization works for a given variable — including stratification, blinding, trigger type, and allocation table. Once a model is saved and in production, most settings are locked and can only be changed by a REDCap administrator. |
| **Allocation Slots** | Individual entries in the allocation table. Each slot corresponds to one randomization event. Running out of slots mid-study requires administrator intervention to append more allocations. |
| **Smart Variables (Randomization)** | REDCap system variables that capture metadata about the randomization event: \[rand-time\] (server timestamp), \[rand-utc-time\] (UTC timestamp), \[rand-number\] (allocation number assigned). Useful for audit trails and piping into alerts or reports. |

**Open vs. Blinded Randomization — Decision Guide**

This is one of the most consequential decisions in randomization setup.
It affects your variable type, user rights configuration, and workflow
outside REDCap.

| **Factor** | **Open (Unblinded)**                                **Blinded** |
| --- | --- |
| **Randomization variable type** | Dropdown or radio button with group labels          Plain text field, no validation — stores an opaque code |
| **Group visible in REDCap UI?** | Yes — study team can see group assignment         No — team sees only a code; key stored outside REDCap |
| **Allocation table format** | Group labels match dropdown options                 Group codes defined by statistician; key held separately |
| **Who needs the decode key?** | Not applicable                                      Only designated unblinded individuals (e.g., pharmacy) |
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
    downloadable template tailored to your model\'s configuration that
    the statistician can use as a guide.

- **Table size:** Always generate more slots than you expect to need.
    Account for dropout, screen failures, and protocol deviations. A
    common rule of thumb: at minimum double your target enrollment per
    group. There is no functional upper limit to allocation table size.

- **Development vs. production tables:** REDCap maintains separate
    allocation tables for development and production modes. You can
    upload the same file to both, but keep in mind that test
    randomizations in development mode consume development slots.

- **Running out of slots:** Only a REDCap administrator can append
    additional allocations to a production allocation table. This is a
    recoverable situation, but an avoidable one with proper planning.

**Randomization User Rights**

Enabling randomization adds three new user rights to every user and role
in the project. These must be assigned deliberately — they do not
default to on.

| **Right** | **What it allows**                                                                                                             **Assign to** |
| --- | --- |
| **Setup** | Configure the randomization model — define stratification, select randomization variable, upload allocation tables.          Project builders, study coordinators involved in setup. Restrict after setup is complete. |
| **Randomize** | Click the Randomize button to manually randomize a record. Not required if using the \'all users\' automatic trigger option.   Data entry staff who perform randomization. Project builders during testing. Not required for survey-only auto-randomization. |
| **Dashboard** | View the randomization dashboard — see allocation counts, used/remaining slots, and assigned records.                        PIs, statisticians, data coordinators, project builders. Anyone needing to monitor randomization progress. |

**Longitudinal Projects and Randomization**

Randomization in a non-longitudinal project is straightforward. In a
longitudinal project, the design choices you make for arms and events
directly constrain what randomization can do. Understand these rules
before building your longitudinal framework:

- **Single-arm longitudinal projects:** If all cohorts follow the same
    data collection path, a single-arm project works fine. Use branching
    logic keyed to the randomization variable to differentiate the
    experience between groups.

- **Multi-arm longitudinal projects:** If cohorts require completely
    separate arms (e.g., intervention arm vs. control arm), REDCap
    cannot automatically move records between arms based on
    randomization. In this scenario, randomization must happen outside
    REDCap, or the project must be redesigned.

- **Per-arm randomization:** If you have multiple arms, you can set up
    a separate randomization model for each arm. Each model requires its
    own randomization variable and allocation table.

- **Event placement matters:** The randomization variable must be
    assigned to a specific event. This event selection is locked once
    the model is saved. If you later need to move the randomization
    variable to a different event, you must delete and rebuild the
    entire model.

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

Open (unblinded) randomization is a setup where the study team can see which group each participant is assigned to. It uses a dropdown or radio button randomization variable with group labels visible in the interface. Blinded randomization is a setup where even the study team does not know which group a participant is assigned to; it requires a plain text randomization variable with no validation, so the assigned value is opaque. The key for decoding group assignments is stored outside REDCap and shared only with designated unblinded individuals (e.g., pharmacy staff).

**Q: Can I randomize records into different arms in a multi-arm longitudinal project?**

No. REDCap cannot automatically move records between arms based on randomization. If your study design requires cohorts to follow completely separate arms (e.g., intervention arm vs. control arm), you must either randomize outside REDCap or redesign the project to use a single-arm design with branching logic keyed to the randomization variable. You can set up a separate randomization model for each arm if needed, but each model requires its own randomization variable and allocation table.

**Q: What are the three randomization-specific user rights and who should have them?**

The three rights are: (1) **Setup** — configure the randomization model (assign to project builders and study coordinators involved in setup; restrict after setup is complete); (2) **Randomize** — click the Randomize button to manually randomize a record (assign to data entry staff who perform randomization, and project builders during testing; not required if using automatic trigger options); and (3) **Dashboard** — view the randomization dashboard with allocation counts and assigned records (assign to PIs, statisticians, data coordinators, and anyone needing to monitor progress).

**Q: What happens if the allocation table runs out of slots before enrollment is complete?**

Only a REDCap administrator can append additional allocations to a production allocation table. This is a recoverable situation but an avoidable one with proper planning. To prevent this, generate at minimum double your target enrollment per group and account for dropout, screen failures, and protocol deviations. Consult your statistician for the appropriate buffer for your specific design.

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

- **Prevention:** Open = dropdown or radio button with group labels.
    Blinded = plain text field, no validation. Decide blinding status
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
    arm-switching is required, either use a single-arm design with
    branching logic, or perform randomization outside REDCap.

---

# 6. Administrator Configuration

The Randomization module must be enabled at the system level by a REDCap administrator before it is available in any project. This is done in the Control Center under System Configuration → Modules/Services Configuration (see **RC-CC-06**). When disabled, the Randomization option does not appear in Project Setup and the Randomize user right is not available.

Once the module is enabled system-wide, randomization is enabled per project by turning on the **Randomization** option in Project Setup → Optional modules. User rights (Randomize and Set Up Randomization) are then assigned on the User Rights page.

> **See also:** RC-CC-06 — Control Center: Modules & Services Configuration

---

# 7. Related Articles

- **RC-RAND-02:** Randomization Setup Guide — step-by-step
    configuration procedure

- **RC-RAND-03:** Working with & Managing Randomization — running,
    monitoring, and admin options

- **RC-USER-01:** User Rights: Overview & Three-Tier Access — prerequisite for understanding the Randomize right and DAG-based site stratification

- **RC-DAG-01:** Data Access Groups — prerequisite for understanding DAG-based stratification and restricted randomization access

- **RC-LONG-01:** Longitudinal Projects — prerequisite for
    multi-event randomization setup

- **RC-CC-06:** Control Center: Modules & Services Configuration — system-level Randomization enable/disable

- **RC-NAV-UI-02:** Project Menu Reference — the Randomization application appears in the Applications section of the left menu when randomization is enabled for the project

---

# 8. Version & Change Notes

| **REDCap Version** | **Notes** |
| --- | --- |
| **15.4.4+** | Randomization 2.0 — adds automatic trigger options (trigger logic for users with Randomize rights; trigger logic for all users including survey respondents). This document is written for this version. |
| **Pre-15.x** | Only manual randomization (Randomize button) available. Automatic triggers did not exist. Verify your installation version before configuring. |

REDCap LLM Knowledge Base \| RC-RAND-01 \| Randomization Concepts &
Terminology

---

# 9. Related Articles

- RC-RAND-02 — Randomization Setup Guide
- RC-RAND-03 — Working with & Managing Randomization
- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-DAG-01 — Data Access Groups
- RC-LONG-01 — Longitudinal Project Setup
- RC-CC-06 — Control Center: Modules & Services Configuration
- RC-NAV-UI-02 — Project Menu Reference

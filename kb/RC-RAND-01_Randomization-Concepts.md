**REDCap Randomization**

*RC-RAND-01 \| Concepts & Terminology*

**1. Document Metadata**

  ---------------------- ----------------------------------------------------------------------------------------------------------------------------
  **Topic**              Randomization concepts, terminology, and study design considerations
  **REDCap Module**      Randomization (Randomization 2.0)
  **Primary Audience**   PIs, Study Coordinators, Project Builders --- anyone planning a randomized study in REDCap
  **Skill Level**        Intermediate (foundational REDCap knowledge required)
  **Prerequisites**      Completed foundational REDCap training: project setup, instruments, user rights, longitudinal mode basics
  **REDCap Version**     15.4.4+ (Randomization 2.0 introduced significant changes --- verify version before use)
  **Last Reviewed**      2025-01
  **Related Topics**     RC-RAND-02: Randomization Setup Guide; RC-RAND-03: Working with & Managing Randomization; RC-RIGHTS-01: User Rights & DAGs
  ---------------------- ----------------------------------------------------------------------------------------------------------------------------

**2. Overview**

**What is this?**

This document covers the concepts and terminology required to understand
and plan REDCap randomization. It is intentionally separated from the
setup procedure (RC-RAND-02) because these concepts must be understood
before any configuration decisions are made. Attempting to set up
randomization without this foundation is one of the most common causes
of failed or misconfigured randomization models.

**Why does it matter?**

REDCap\'s randomization module uses standard statistical terminology
that is unfamiliar to many research coordinators and project builders.
The module\'s setup wizard asks you to make consequential decisions ---
some of which cannot be changed without deleting and rebuilding the
entire model --- based on these concepts. Understanding them upfront
prevents costly mistakes.

**Important note about Randomization 2.0**

The introduction of Randomization 2.0 in recent REDCap versions
significantly expanded the feature\'s capabilities (including automatic
trigger options). This document and its companion articles are written
for REDCap 15.4.4+. If your institution runs an older version, some
features described here may not be available.

**3. Learning Objectives**

After reviewing this document, the user will be able to:

-   Define randomization and explain why it is used in research

-   Explain the difference between stratified and unstratified
    randomization

-   Describe what an allocation table is and why REDCap uses one instead
    of a live random number generator

-   Distinguish between open (unblinded) and blinded randomization and
    their implications for variable setup

-   Explain the three randomization-specific user rights in REDCap and
    when to assign each

-   Identify the constraints that longitudinal project design places on
    randomization setup

**4. Core Concepts**

**What is randomization?**

Randomization is the process of randomly assigning study participants
(records in REDCap) to different groups --- typically a control group
and one or more intervention groups. The randomness of the assignment is
what removes selection bias and ensures groups are comparable.

In REDCap, randomization most commonly supports Randomized Clinical
Trials (RCTs), but it can be used for any scenario requiring random
group assignment --- including assigning participants to different
survey order groups.

> **Note:** *For the statistical rationale behind randomization, consult
> your institution\'s statistician or biostatistics department. REDCap
> handles the mechanics; study design decisions belong to the research
> team.*

**Key Terminology Glossary**

These terms appear directly in the REDCap randomization setup interface.
You must understand them before configuring a randomization model.

  ----------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **Term**                                        **Definition**
  **Cohorts / Groups / Sub-groups**               The different groups records are divided into. These terms are interchangeable in REDCap. Examples: placebo vs. intervention; control vs. intervention A vs. intervention B.
  **Stratification (Stratified Randomization)**   A method of ensuring each randomization group has a similar composition across key variables. For example, stratifying by sex prevents all men from ending up in the control group. REDCap supports up to 14 stratification variables, all of which must be single-choice field types (dropdown, radio button, yes/no, true/false).
  **Sites / Groups (Multi-site)**                 A special form of stratification using REDCap\'s Data Access Group (DAG) feature to separate randomization by study site. Useful for multi-site trials where site membership should influence allocation.
  **Blinding (Blinded Randomization)**            A setup where even the study team does not know which group a participant is assigned to. Requires a plain text randomization variable (no dropdown) so the assigned value is opaque to the UI. The key for decoding group assignments is stored outside REDCap and shared only with designated unblinded individuals (e.g., pharmacy staff).
  **Open Randomization (Unblinded)**              A setup where the study team can see which group each participant is assigned to. Uses a dropdown or radio button randomization variable with group labels visible in the interface.
  **Allocation Table**                            A pre-generated list of randomization assignments in a specific sequence. REDCap does not generate random assignments on the fly --- it works down this list in order, assigning each new randomization to the next available slot. Allocation tables are typically generated by a statistician or statistical software. REDCap provides a downloadable template tailored to your model\'s settings.
  **Randomization Variable**                      The REDCap field that stores the randomization result for each record. For open randomization: a dropdown or radio button field. For blinded randomization: a plain text field with no validation. This field must be created before setting up the randomization model.
  **Randomization Model**                         The configuration object in REDCap that defines how randomization works for a given variable --- including stratification, blinding, trigger type, and allocation table. Once a model is saved and in production, most settings are locked and can only be changed by a REDCap administrator.
  **Allocation Slots**                            Individual entries in the allocation table. Each slot corresponds to one randomization event. Running out of slots mid-study requires administrator intervention to append more allocations.
  **Smart Variables (Randomization)**             REDCap system variables that capture metadata about the randomization event: \[rand-time\] (server timestamp), \[rand-utc-time\] (UTC timestamp), \[rand-number\] (allocation number assigned). Useful for audit trails and piping into alerts or reports.
  ----------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Open vs. Blinded Randomization --- Decision Guide**

This is one of the most consequential decisions in randomization setup.
It affects your variable type, user rights configuration, and workflow
outside REDCap.

  --------------------------------- --------------------------------------------------- ------------------------------------------------------------
  **Factor**                        **Open (Unblinded)**                                **Blinded**
  **Randomization variable type**   Dropdown or radio button with group labels          Plain text field, no validation --- stores an opaque code
  **Group visible in REDCap UI?**   Yes --- study team can see group assignment         No --- team sees only a code; key stored outside REDCap
  **Allocation table format**       Group labels match dropdown options                 Group codes defined by statistician; key held separately
  **Who needs the decode key?**     Not applicable                                      Only designated unblinded individuals (e.g., pharmacy)
  **Complexity**                    Simpler to setup and manage                         More complex; requires external process for key management
  **Common use case**               Most open-label trials, operational randomization   Double-blind RCTs, placebo-controlled trials
  --------------------------------- --------------------------------------------------- ------------------------------------------------------------

**Allocation Tables --- What you need to know**

REDCap does not generate randomization assignments dynamically. Instead
it works through a pre-generated allocation table --- a sequenced list
of group assignments --- in order. This approach is standard practice in
clinical trials because it allows the randomization sequence to be
pre-audited and reproduced.

-   **Who generates the table?:** Typically a statistician or dedicated
    statistical software (SAS, R, nQuery, etc.). REDCap provides a
    downloadable template tailored to your model\'s configuration that
    the statistician can use as a guide.

-   **Table size:** Always generate more slots than you expect to need.
    Account for dropout, screen failures, and protocol deviations. A
    common rule of thumb: at minimum double your target enrollment per
    group. There is no functional upper limit to allocation table size.

-   **Development vs. production tables:** REDCap maintains separate
    allocation tables for development and production modes. You can
    upload the same file to both, but keep in mind that test
    randomizations in development mode consume development slots.

-   **Running out of slots:** Only a REDCap administrator can append
    additional allocations to a production allocation table. This is a
    recoverable situation, but an avoidable one with proper planning.

**Randomization User Rights**

Enabling randomization adds three new user rights to every user and role
in the project. These must be assigned deliberately --- they do not
default to on.

  --------------- ------------------------------------------------------------------------------------------------------------------------------ -------------------------------------------------------------------------------------------------------------------------------
  **Right**       **What it allows**                                                                                                             **Assign to**
  **Setup**       Configure the randomization model --- define stratification, select randomization variable, upload allocation tables.          Project builders, study coordinators involved in setup. Restrict after setup is complete.
  **Randomize**   Click the Randomize button to manually randomize a record. Not required if using the \'all users\' automatic trigger option.   Data entry staff who perform randomization. Project builders during testing. Not required for survey-only auto-randomization.
  **Dashboard**   View the randomization dashboard --- see allocation counts, used/remaining slots, and assigned records.                        PIs, statisticians, data coordinators, project builders. Anyone needing to monitor randomization progress.
  --------------- ------------------------------------------------------------------------------------------------------------------------------ -------------------------------------------------------------------------------------------------------------------------------

**Longitudinal Projects and Randomization**

Randomization in a non-longitudinal project is straightforward. In a
longitudinal project, the design choices you make for arms and events
directly constrain what randomization can do. Understand these rules
before building your longitudinal framework:

-   **Single-arm longitudinal projects:** If all cohorts follow the same
    data collection path, a single-arm project works fine. Use branching
    logic keyed to the randomization variable to differentiate the
    experience between groups.

-   **Multi-arm longitudinal projects:** If cohorts require completely
    separate arms (e.g., intervention arm vs. control arm), REDCap
    cannot automatically move records between arms based on
    randomization. In this scenario, randomization must happen outside
    REDCap, or the project must be redesigned.

-   **Per-arm randomization:** If you have multiple arms, you can set up
    a separate randomization model for each arm. Each model requires its
    own randomization variable and allocation table.

-   **Event placement matters:** The randomization variable must be
    assigned to a specific event. This event selection is locked once
    the model is saved. If you later need to move the randomization
    variable to a different event, you must delete and rebuild the
    entire model.

> **Note:** *Set up at least the framework of your longitudinal model
> (arms and events) before configuring randomization. You can refine
> events afterward as long as you do not change the event containing the
> randomization variable.*

**5. Questions & Answers**

  ------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  *What is the difference between stratification and blinding?*                  Stratification ensures balanced group composition across key variables (e.g., equal sex distribution across cohorts). Blinding controls who can see which group a participant is assigned to. They are independent settings --- a study can use stratification with or without blinding, or neither.
  *Does REDCap generate random assignments on the fly?*                          No. REDCap uses a pre-generated allocation table and works through it sequentially. This is intentional --- it allows the randomization sequence to be pre-audited and reproduced, which is required in most clinical trial contexts.
  *Who should generate the allocation table?*                                    A statistician or statistical software (SAS, R, nQuery, etc.). REDCap provides a downloadable template tailored to your model\'s settings. Share that template with your statistician.
  *Can I use more than one randomization model in a single project?*             Yes. REDCap supports multiple randomization models per project. Each model needs its own distinct randomization variable and allocation table. Stratification variables can be shared across models. This is used in adaptive study designs or multi-arm projects.
  *What happens if I run out of allocation slots?*                               New records cannot be randomized until more slots are added. Only a REDCap administrator can append additional allocations to a production table. This is avoidable with proper table sizing --- always generate significantly more slots than your target enrollment.
  *Do I need the Randomize user right to use automatic trigger randomization?*   It depends on which trigger option you choose. \'Trigger logic for users with Randomize permission only\' --- yes, the saving user needs Randomize rights. \'Trigger logic for all users including survey respondents\' --- no, Randomize rights are not required for the trigger to fire.
  *Can I change the randomization model after moving to production?*             Only a REDCap administrator can make changes to a randomization model in production. Most structural changes (stratification, randomization variable, blinding type) require deleting and rebuilding the model --- which erases all randomization data in that variable. Test thoroughly in development before moving to production.
  ------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**6. Common Mistakes & Gotchas**

**Setting up randomization without consulting a statistician**

-   **What happens:** Allocation tables are generated incorrectly,
    stratification variables are misconfigured, or table sizes are too
    small --- often discovered only after real data collection has
    begun.

-   **Prevention:** Involve a statistician before the randomization
    model is configured. Share the REDCap allocation table template with
    them early.

**Choosing the wrong randomization variable type**

-   **What happens:** An open randomization is set up with a text field,
    or a blinded randomization is set up with a dropdown --- causing
    either data integrity issues or unintended unblinding.

-   **Prevention:** Open = dropdown or radio button with group labels.
    Blinded = plain text field, no validation. Decide blinding status
    before creating the variable.

**Not accounting for dropout in allocation table size**

-   **What happens:** The allocation table runs out of slots before
    enrollment is complete, requiring emergency administrator
    intervention to append more allocations --- a disruptive and
    avoidable situation.

-   **Prevention:** Generate at minimum double your target enrollment
    per group. Consult your statistician for the appropriate buffer for
    your specific design.

**Assuming arm switching is possible in longitudinal projects**

-   **What happens:** A researcher designs a multi-arm longitudinal
    project expecting REDCap to automatically move randomized records
    between arms --- this is not possible. Records cannot switch arms
    based on randomization outcomes.

-   **Prevention:** Clarify this constraint during study design. If
    arm-switching is required, either use a single-arm design with
    branching logic, or perform randomization outside REDCap.

**7. Related Topics**

-   **RC-RAND-02:** Randomization Setup Guide --- step-by-step
    configuration procedure

-   **RC-RAND-03:** Working with & Managing Randomization --- running,
    monitoring, and admin options

-   **RC-RIGHTS-01:** User Rights & DAGs --- prerequisite for
    understanding DAG-based site stratification

-   **RC-LONG-01:** Longitudinal Projects --- prerequisite for
    multi-event randomization setup

**8. Version & Change Notes**

  -------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **REDCap Version**   **Notes**
  **15.4.4+**          Randomization 2.0 --- adds automatic trigger options (trigger logic for users with Randomize rights; trigger logic for all users including survey respondents). This document is written for this version.
  **Pre-15.x**         Only manual randomization (Randomize button) available. Automatic triggers did not exist. Verify your installation version before configuring.
  -------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

REDCap LLM Knowledge Base \| RC-RAND-01 \| Randomization Concepts &
Terminology

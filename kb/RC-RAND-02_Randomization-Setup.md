RC-RAND-02

**REDCap Randomization Setup**

| **Article ID** | RC-RAND-02 |
| --- | --- |
| **Domain** | Randomization |
| **Applies To** | All REDCap project types with Randomization module enabled; requires Project Design and Setup rights and User Rights management access |
| **Prerequisite** | RC-RAND-01 — Randomization Concepts & Terminology; RC-LONG-01 — Longitudinal Projects; RC-RIGHTS-01 — User Rights Overview |
| **Version** | 1.0 |
| **Last Updated** | 2025-01 |
| **Author** | See KB-SOURCE-ATTESTATION.md |
| **Related Topics** | RC-RAND-01 — Randomization Concepts & Terminology; RC-RAND-03 — Working with & Managing Randomization; RC-RIGHTS-01 — User Rights Overview; RC-CC-06 — Control Center: Modules & Services Configuration |

---

# 1. Overview

## What is this?

This document is the operational setup guide for REDCap randomization.
It covers everything from pre-flight preparation through moving a
randomized project to production. It assumes the reader has already
reviewed RC-RAND-01 and understands core randomization concepts and
terminology.

## Why does it matter?

REDCap randomization setup has more interdependencies than almost any
other feature. Several decisions made early in the process ---
particularly in the model definition step — become permanently locked
once saved. The most common failure mode is rushing into setup without
completing the necessary preparations, then discovering the model must
be rebuilt from scratch after data collection has begun.

**A note on multiple randomization models**

This guide assumes a single randomization model per project, which
covers the vast majority of use cases. For projects requiring multiple
models (adaptive study designs, multi-arm projects), follow steps 8
through 12 of the Setup Procedure for each additional model. Each model
requires its own randomization variable and allocation table;
stratification variables can be shared.

---

# 2. Learning Objectives

After completing this guide, the user will be able to:

- Complete all required pre-flight preparations before entering the
    REDCap setup interface

- Enable the randomization module in a REDCap project

- Configure randomization user rights for all relevant roles

- Define a randomization model including stratification, blinding, and
    trigger options

- Download, obtain, and upload allocation tables for both development
    and production modes

- Test a randomization setup thoroughly before moving to production

- Move a randomized project to production status correctly

---

# 3. Pre-flight Checklist

Complete every applicable item below before opening the REDCap
randomization setup interface. Items skipped prematurely are the leading
cause of model rebuilds.

  ------- ----------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------
  **✓**   **Pre-flight item**                                                                                               **Skip if...**
  ☐       **Confirm Randomization is enabled system-wide** — verify with your REDCap administrator that the Randomization module is enabled in the Control Center (RC-CC-06). If the Randomization option does not appear in Project Setup, the module is disabled.   *Never — must be enabled before any project can use it*
  ☐       Decide: open (unblinded) or blinded randomization?                                                                *Never — this decision drives variable type and workflow*
  ☐       Decide: will you use stratification? If yes, list your strata (max 14, all must be single-choice field types)     *No stratification planned*
  ☐       Decide: will you use Data Access Groups (DAGs) for multi-site stratification?                                     *No DAGs in this project*
  ☐       Consult your statistician and confirm allocation table strategy (size, format, software)                          *Never — statistician input is always recommended*
  ☐       Create your randomization variable in the instrument designer (dropdown/radio for open; plain text for blinded)   *Never — must exist before setup*
  ☐       Create all stratification variables in the instrument designer (dropdown, radio, yes/no, true/false only)         *No stratification planned*
  ☐       Set up Data Access Groups if using DAG-based site stratification                                                  *Not using DAGs*
  ☐       Set up at least the framework of your longitudinal model (arms and events) if applicable                          *Non-longitudinal project*
  ☐       Confirm you have Project Design and Setup rights AND User Rights management access                                *Never — both are required*
  ☐       Confirm your allocation table is ready (or a plan is in place to obtain it)                                       *Never — required before going to production*
  ------- ----------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------

---

# 4. Setup Procedure

Follow these 14 steps in order. Steps marked as optional can be skipped
if they do not apply to your project design.

## 4.1 Variable and framework setup (Steps 1--4)

+-------+-------------------------------------------------------------+
| **1** | **Create your randomization variable**                      |
|       |                                                             |
|       | *Open: create a dropdown or radio button field. Use group   |
|       | names as options (e.g., \'Control\' / \'Intervention\').    |
|       | Use a simple, memorable variable name --- branching logic   |
|       | will reference it frequently. Blinded: create a plain text  |
|       | field with no validation.*                                  |
+-------+-------------------------------------------------------------+
| **2** | **Create your stratification variables (optional)**         |
|       |                                                             |
|       | *For each stratum, create a single-choice field: dropdown,  |
|       | radio button, yes/no, or true/false. Maximum 14             |
|       | stratification variables. Skip if not using                 |
|       | stratification.*                                            |
+-------+-------------------------------------------------------------+
| **3** | **Set up Data Access Groups (optional)**                    |
|       |                                                             |
|       | *Navigate to Applications → DAGs and configure your site    |
|       | groups. Must be done before the randomization model is      |
|       | defined --- you cannot add new DAGs to an existing          |
|       | production model. Skip if not using DAG-based site          |
|       | stratification.*                                            |
+-------+-------------------------------------------------------------+
| **4** | **Set up your longitudinal framework (optional)**           |
|       |                                                             |
|       | *Define arms and events. Critically: decide which event     |
|       | will contain your randomization variable. This event        |
|       | assignment is locked once the model is saved. You can       |
|       | modify events later as long as you do not change the event  |
|       | that holds the randomization variable. Skip if not using    |
|       | longitudinal mode.*                                         |
+-------+-------------------------------------------------------------+

## 4.2 Enable the module (Steps 5--7)

+-------+-------------------------------------------------------------+
| **5** | **Confirm user rights — Part 1**                          |
|       |                                                             |
|       | *Verify you have both \'Project Design and Setup\' AND      |
|       | \'User Rights\' management rights. Both are required.       |
|       | Obtain them before proceeding.*                             |
+-------+-------------------------------------------------------------+
| **6** | **Enable the randomization module**                         |
|       |                                                             |
|       | *Go to Project Setup → \'Enable optional modules and        |
|       | customizations\'. Click Enable next to Randomization.       |
|       | Confirmation: the module label turns green, the button      |
|       | changes to Disable, and a Randomization item appears in the |
|       | Applications menu.*                                         |
+-------+-------------------------------------------------------------+
| **7** | **Assign randomization user rights — Part 2**             |
|       |                                                             |
|       | *Navigate to Applications → User Rights. Enabling the       |
|       | module has added three new rights to all users and roles.   |
|       | Assign them deliberately: Setup → project builders only.    |
|       | Randomize → data entry staff and project builders (for      |
|       | testing). Dashboard → PIs, statisticians, coordinators,     |
|       | project builders.*                                          |
+-------+-------------------------------------------------------------+

## 4.3 Define the randomization model (Step 8)

This is the most critical step. Decisions made here are locked once the
model is saved. Review RC-RAND-01 before proceeding if you have any
uncertainty about the concepts below.

+--------+------------------------------------------------------------+
| **8a** | **Open the randomization setup**                           |
|        |                                                            |
|        | *Go to Applications → Randomization. Click \'+ Add new     |
|        | randomization model\'.*                                    |
+--------+------------------------------------------------------------+
| **8b** | **Configure stratification**                               |
|        |                                                            |
|        | *If using stratification, check \'Use stratified           |
|        | randomization\'. Select up to 14 stratification variables  |
|        | from the dropdown. For longitudinal projects, also select  |
|        | the event each stratification variable belongs to. If not  |
|        | using stratification, leave unchecked.*                    |
+--------+------------------------------------------------------------+
| **8c** | **Configure multi-site / DAGs**                            |
|        |                                                            |
|        | *If randomizing by site using DAGs, check \'Use Data       |
|        | Access Groups to designate each group/site\'. If using a   |
|        | dedicated variable for site, select it from the dropdown   |
|        | (and event if longitudinal). If not using multi-site,      |
|        | skip.*                                                     |
+--------+------------------------------------------------------------+
| **8d** | **Select the randomization variable**                      |
|        |                                                            |
|        | *Select your pre-created randomization variable from the   |
|        | dropdown. For longitudinal projects, also select the       |
|        | corresponding event. REDCap shows all valid options for    |
|        | both open and blinded setups. Warning: if the variable     |
|        | already contains data from testing, saving the model will  |
|        | erase that data. REDCap will warn you.*                    |
+--------+------------------------------------------------------------+
| **8e** | **Save the model**                                         |
|        |                                                            |
|        | *Click \'Save randomization model\'. The model is now      |
|        | locked. To make structural changes, you must use \'Erase   |
|        | randomization model\' and rebuild from scratch --- which   |
|        | also erases all randomization data in that variable.*      |
+--------+------------------------------------------------------------+

> **⚠ Warning:** *\'Erase randomization model\' is available in
> Development mode only. In Production, only a REDCap administrator can
> make structural changes, and doing so has major consequences. Test
> thoroughly before going to production.*

## 4.4 Allocation tables (Steps 9--10)

+--------+------------------------------------------------------------+
| **9**  | **Download the allocation table template**                 |
|        |                                                            |
|        | *In the randomization setup page, download the template    |
|        | file. It is dynamically generated based on your model\'s   |
|        | settings (open vs. blinded, stratification, etc.) and      |
|        | includes instructions. Share this template with your       |
|        | statistician if they are generating the table.*            |
+--------+------------------------------------------------------------+
| **10** | **Upload the development allocation table**                |
|        |                                                            |
|        | *Once you have a valid allocation table, upload it to the  |
|        | Development slot. Click \'Choose file\', select the file,  |
|        | then click \'Upload File\'. Confirmation: the icon changes |
|        | to a checkmark labeled \'Already uploaded\'. Development   |
|        | tables can be deleted and re-uploaded for testing. Note:   |
|        | re-uploading affects test records --- create fresh test    |
|        | records when testing a new table.*                         |
+--------+------------------------------------------------------------+

## 4.5 Trigger options (Step 11)

Select how randomization is initiated. This is a Randomization 2.0
feature — verify your REDCap version supports it.

| **Trigger Option** | **How it works & when to use it** |
| --- | --- |
| **Manual only — Randomize button (default)** | A Randomize button replaces the randomization variable in the UI. Any user with Randomize rights clicks it to randomize that record. Simplest option. Use when study staff control randomization timing. |
| **Trigger logic — for users with Randomize permission only** | Define trigger logic (similar to branching logic) on a specific instrument/event. Randomization fires automatically when the logic is true AND a user with Randomize rights saves the defined form. Use when randomization should be conditional on data values, but staff-controlled. |
| **Trigger logic — for all users (including survey respondents)** | Same as above, but fires for any user — including survey respondents completing a form. Randomization rights not required to trigger. Use for automatic randomization based on survey completion or eligibility criteria. |

## 4.6 Test, finalize, and go to production (Steps 12--14)

+--------+------------------------------------------------------------+
| **12** | **Test thoroughly in Development mode**                    |
|        |                                                            |
|        | *Test every randomization pathway: manual button, trigger  |
|        | logic (if used), stratification prompts, blinded/open      |
|        | display, dashboard counts. Create multiple test records.   |
|        | Verify allocation table consumption. Check that users      |
|        | without Randomize rights see the field greyed out. It is   |
|        | rare to get randomization right on the first attempt ---   |
|        | build in time for this step.*                              |
+--------+------------------------------------------------------------+
| **13** | **Upload the production allocation table**                 |
|        |                                                            |
|        | *Once satisfied with testing, upload the allocation table  |
|        | to the Production slot. This can be the same file as the   |
|        | development slot if your tests passed. Verify all          |
|        | randomization models have a production allocation table    |
|        | --- REDCap will not allow the project to move to           |
|        | production otherwise.*                                     |
+--------+------------------------------------------------------------+
| **14** | **Move the project to Production**                         |
|        |                                                            |
|        | *Go to Project Setup and move the project to Production    |
|        | status. REDCap will ask whether to delete existing records |
|        | --- if you have only test records, deletion is             |
|        | appropriate. Do not start real randomization in            |
|        | Development mode and then switch --- randomization values  |
|        | in the randomization variable will be cleared when moving  |
|        | to production. Always begin real data collection in        |
|        | Production.*                                               |
+--------+------------------------------------------------------------+

---

# 5. Questions & Answers

---

# 6. Common Mistakes & Gotchas

**Skipping pre-flight and going straight to setup**

- **What happens:** The setup wizard asks for stratification
    variables, event assignments, or DAG configuration that hasn\'t been
    created yet. Setup stalls or is completed incorrectly, requiring a
    model rebuild.

- **Prevention:** Complete the pre-flight checklist in Section 4
    entirely before opening the randomization setup interface.

**Locking in the wrong event for the randomization variable
(longitudinal projects)**

- **What happens:** The randomization variable is assigned to the
    wrong event in the model setup. Once saved, this cannot be changed
    without deleting the model.

- **Prevention:** Map out your longitudinal event structure explicitly
    before setting up the model. Confirm which event holds the
    randomization variable before clicking Save.

**Starting real data collection in Development mode**

- **What happens:** Real participants are randomized in Development
    mode. When the project is moved to Production, REDCap clears all
    randomization variable values. Randomization data is lost and must
    be redone.

- **Prevention:** Never collect real data in Development mode. Move to
    Production before any real participant randomization occurs.

**Not testing the \'insufficient rights\' experience**

- **What happens:** Users without Randomize rights can still see or
    interact with the randomization variable, or the field behavior is
    not what was expected.

- **Prevention:** Test with a user account that has minimal rights (no
    Randomize right) to confirm the field is greyed out and
    non-interactive. Test all user role configurations before going to
    production.

**Generating an allocation table that is too small**

- **What happens:** The project runs out of allocation slots
    mid-study. New records cannot be randomized. Administrator
    intervention is required to append more allocations — a disruptive
    situation during active data collection.

- **Prevention:** Generate at minimum double your expected enrollment
    per group. Consult your statistician. There is no penalty for having
    too many slots.

**Using a complex variable name for the randomization variable**

- **What happens:** Branching logic, alerts, and reports that
    reference the variable by name become error-prone and difficult to
    maintain.

- **Prevention:** Use short, descriptive variable names (e.g.,
    \'rand\_group\'). Establish a naming convention before creating any
    randomization-related variables.

---

# 7. Administrator Configuration

The Randomization module must be enabled at the system level before it can be enabled in any project. Administrators do this in the Control Center under System Configuration → Modules/Services Configuration. See **RC-CC-06** for details.

> **See also:** RC-CC-06 — Control Center: Modules & Services Configuration

---

# 8. Related Articles

- **RC-RAND-01:** Randomization Concepts & Terminology — required
    prerequisite for this guide

- **RC-RAND-03:** Working with & Managing Randomization — running,
    monitoring, dashboard, and admin options

- **RC-RIGHTS-01:** User Rights & DAGs — DAG setup and user rights
    management

- **RC-LONG-01:** Longitudinal Projects — arm and event setup
    prerequisite for longitudinal randomization

- **RC-CC-06:** Control Center: Modules & Services Configuration — system-level Randomization enable/disable

---

# 9. Version & Change Notes

| **REDCap Version** | **Notes** |
| --- | --- |
| **15.4.4+** | Randomization 2.0: automatic trigger options (steps 11) are available. This document is written for this version. |
| **Pre-15.x** | Automatic trigger options do not exist. Step 11 is not applicable. Manual-only randomization is the only option. |

REDCap LLM Knowledge Base \| RC-RAND-02 \| Randomization Setup Guide

---

# 10. Related Articles

- RC-RAND-01 — Randomization Concepts & Terminology
- RC-RAND-03 — Working with & Managing Randomization
- RC-USER-01 — User Rights: Overview & Three-Tier Access
- RC-LONG-01 — Longitudinal Project Setup
- RC-CC-06 — Control Center: Modules & Services Configuration

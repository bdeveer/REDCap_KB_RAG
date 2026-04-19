# RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage


| **Article ID** | RC-CDIS-03 |
| --- | --- |
| **Author** | See KB-SOURCE-ATTESTATION.md |

> **Prerequisite:** CDIS must be configured at the system level before CDM can be used. See RC-CDIS-01.

---

## What Is the Clinical Data Mart (CDM)?

The **Clinical Data Mart** (also called **Data Mart** or **CDM**) is a REDCap module that imports clinical data **in bulk** from an EHR for many patients at once. Unlike CDP, which pulls one patient at a time with an adjudication step, Data Mart is designed for larger-scale, batch data retrieval.

Data Mart is best suited for:
- Registries
- Prospective or retrospective clinical studies and trials
- Searching for specific lab values or diagnosis codes for a cohort of patients over a defined time period

---

## Administrator Prerequisites

### 1. CDIS Must Be Enabled

The CDIS infrastructure must be configured and enabled in the Control Center before Data Mart can function. See RC-CDIS-01.

### 2. Grant User-Level Data Mart Privileges

Unlike CDP (which is enabled per project), Data Mart access is a **user account privilege**, not a project-level right. An administrator must grant this privilege to individual user accounts via the **Browse Users** page in the Control Center.

Once granted, the user will see an option to create a **Clinical Data Mart project** on the Create New Project page.

> **Note:** There is no optional User Access Web Service for Data Mart (unlike CDP). Access is controlled solely through the user account privilege granted in the Control Center.

---

## Creating a Data Mart Project

A user with Data Mart privileges can create a new Data Mart project from the **Create New Project** page.

> **Important:** The user must have launched REDCap from within the EHR at least once before creating a Data Mart project. If they have not done so, they will be prompted to complete this step first.

During project creation, the user defines the initial **data pull configuration**, including:
- Specific MRNs (patient identifiers) to include
- Date range for the data pull
- Data fields from the EHR to import

---

## Pre-Defined Project Structure

Unlike CDP, **no field mapping is required** for a Data Mart project. The entire project structure — instruments and fields — is pre-defined when the project is created:

- **Demographics** — a single data collection form (non-repeating)
- **Vital Signs, Labs, Allergies, Medications, Problem List** — created as repeating instruments

Each individual data value on the repeating instruments is stored as a separate repeating instance of the form. This means a patient with 10 lab results will have 10 repeating instances of the Labs instrument.

> Additional instruments or events may be added to a Data Mart project, but modifying or deleting any of the pre-defined fields or instruments may break the data pull.

---

## Pulling Data

Once the project is created, data is pulled via the **Clinical Data Mart page**, accessible from the left-hand project menu.

### Fetch Clinical Data

Users click the **"Fetch clinical data"** button to trigger a data pull. By default:
- A user can only pull data **one time**.
- The data pull configuration **cannot be modified** after initial setup.

These defaults can be changed by a REDCap administrator in the project's **Project Setup** page (see Project-Level Settings below).

### Requesting Configuration Changes

If the project-level setting permits it, users with **Project Setup/Design rights** in the project can request changes to the data pull configuration (e.g., adding new MRNs, adding new fields, or modifying the date range). Such requests go through an audit process and must be approved by an administrator via the **To-Do List** in the Control Center.

---

## Project-Level Settings (Administrator-Controlled)

On the **Project Setup page** for a Data Mart project, a REDCap administrator can adjust:

| Setting | Default | Description |
|---|---|---|
| **Allow multiple data pulls** | Off (one pull only) | When enabled, users can fetch data as many times as they wish |
| **Allow configuration changes** | Off | When enabled, users can request changes to the MRN list, date range, or field selection; changes go through the To-Do List for admin approval |
| **Automatic daily data pull (cron job)** | Off | When enabled, new EHR data is pulled automatically once per day |

---

## EHR Access Requirement

Users must have access to the EHR and must have launched REDCap from inside the EHR interface at least once. This is required because the EHR launch initiates the OAuth2 authorization needed to pull data.

---

## Recommended Administrative Process

Before approving a Data Mart project or enabling configuration changes, administrators may want to verify:
- IRB approval status
- The requesting users' EHR access authorization

This review step is optional but recommended, particularly at institutions with policies around research data access.

---

## Clinical Notes in Data Mart

CDM accepts clinical notes in **any format** (not just HTML), making it more flexible than CDP for institutions that receive notes in varied formats. Clinical notes are imported via the FHIR `DocumentReference` resource.

---

## Related Articles

- RC-CDIS-01 — CDIS Overview and Control Center Setup
- RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage
- RC-CDIS-04 — CDP vs CDM: Feature Comparison
- RC-CC-07 — Control Center: Users & Access Management (for granting Data Mart privileges)
- RC-CC-09 — To-Do List (for approving configuration change requests)
- RC-LONG-02 — Repeated Instruments and Events Setup

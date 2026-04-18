# RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage

> **Prerequisite:** CDIS must be configured at the system level before CDP can be used. See RC-CDIS-01.

---

## What Is Clinical Data Pull (CDP)?

**Clinical Data Pull (CDP)** is a REDCap module that imports clinical data from an EHR into a REDCap project — one patient at a time. It uses an **adjudication workflow**, meaning all incoming EHR data is held in a temporary cache and must be reviewed and approved by a user before it is officially saved in the project.

CDP is best suited for:
- Real-time data collection
- Prospective clinical studies and trials
- Longitudinal and/or multi-arm studies

---

## Enabling CDP for a Project

Only a REDCap administrator can enable CDP for a project. This is done via the **Project Setup** page for the individual project. Once enabled, users with **CDP Setup/Mapping privileges** in the project can access the CDP Mapping page.

To contact your REDCap administrator about enabling CDP for a project, follow your institution's process, which may include checks for IRB approval and EHR access authorization.

---

## Field Mapping

Before data can be pulled, a user with CDP mapping privileges must map EHR data fields to REDCap fields. This is done on the **CDP Mapping page**, accessible from the Project Setup page.

### Field Types

CDP supports two types of mapped fields:

**One-time (non-temporal) fields** — Data that exists once per patient (e.g., demographics). This data is fetched immediately when a patient is added to the project via the EHR Launch.

**Temporal fields** — Data that repeats over time (e.g., lab results, vitals). These fields require an associated REDCap date or date/time field. Data is only retrieved once the associated date field has a value. The date field and a configured **± day offset** together define the time window for the query.

Example: If the associated date field contains `2024-03-15` and the day offset is `1`, REDCap queries the EHR for values from `2024-03-14` through `2024-03-16`. Values outside this range are ignored.

### Mapping Flexibility

- CDP supports one-to-many, many-to-one, and many-to-many field mappings between EHR fields and REDCap fields.
- Temporal fields can be mapped to fields in a classic project, to events in a longitudinal project, or to repeating instruments/events.
- Mappings for Allergies, Medications, and Problem List are merged per category and stored in a Notes/Paragraph field.
- Mappings can be adjusted at any time in a CDP project.

### Preview Fields

On the mapping page, up to 5 source fields can be designated as **preview fields**. These are displayed when a record identifier (e.g., MRN) is entered, allowing the user to confirm they have the correct patient before importing data. Preview fields are optional but recommended for data quality.

### Clinical Notes (DocumentReference)

CDP can import clinical notes from the EHR using the FHIR `DocumentReference` resource. Notes are only stored if they are in HTML format. For clinical notes in other formats, use the Clinical Data Mart (CDM) instead.

When mapping a field for clinical notes:
- Use a **Notes Box** field type to accommodate large text
- Apply the **@RICHTEXT** action tag to preserve HTML formatting
- Set field alignment to **Left / Horizontal (LH)** for consistent presentation

### Demography Field Coding

For the fields **race**, **sex**, and **ethnicity**, CDP requires that answer choices be coded using specific standardized values aligned with FHIR terminology. Contact your REDCap administrator for the required code list if you are setting up these mappings.

---

## Importing Data: Two Access Methods

### 1. EHR Launch

**EHR Launch** means opening REDCap as an embedded window from within the EHR interface. This is always the required first step — it initiates the user's OAuth2 authorization for FHIR services.

- A list of CDP-enabled projects is displayed. The user can add the current patient to a project by clicking **Add patient**.
- Non-temporal fields (e.g., demographics) are fetched immediately when a patient is added.
- Once inside a project, the user can enter data normally and adjudicate CDP data.

After completing at least one EHR Launch, the user is authorized and can use CDP from either inside the EHR window or from the REDCap side in a normal browser.

### 2. REDCap Side (Outside the EHR)

Users can access their REDCap project from a regular browser and pull data for existing patients:

- Navigate to the patient's record in the project.
- If the patient does not exist yet, create a new record and enter the patient's MRN into the mapped MRN field. REDCap will immediately begin pulling data from the EHR in real time.
- If temporal fields are mapped, those values will not be fetched until their associated date/time field has a value entered.

---

## Adjudication

**Adjudication** is the process of reviewing and approving EHR data before it is saved in the project. All pulled data is stored in a temporary cache first.

The adjudication screen can be accessed from two places:
1. **Record Status Dashboard** — A column shows the count of pending items per record. Click the count to open the adjudication screen.
2. **Data entry form** — A red counter at the top of the page indicates pending items. Click **View** to open the adjudication screen.

On the adjudication screen:
- If only one source value was returned for a field, it is pre-selected automatically.
- For temporal fields with multiple values on the same calendar date as the REDCap date field, the matching value is pre-selected automatically (unless a pre-selection rule like "Minimum value" or "Latest value" is set on the mapping page).
- The user selects the radio button for each value to import, then clicks **Save** to store the values in the project.
- Unadjudicated items can be left and returned to later.

---

## Automatic Data Monitoring (Cron Job)

Once a patient has been added to a CDP project, REDCap automatically monitors the EHR for new data via a cron job. This continues for a configurable number of days defined by the setting **"Time of inactivity after which REDCap will stop checking for new data"**, which is set by the administrator on the CDIS Control Center page.

---

## User Access Web Service (Optional)

Administrators can optionally set up a **User Access Web Service** to add an extra layer of control over which users are authorized to adjudicate data from the EHR. This is configured by the REDCap administrator and technical team, and provides finer-grained access management beyond standard project user rights.

---

## Related Articles

- RC-CDIS-01 — CDIS Overview and Control Center Setup
- RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage
- RC-CDIS-04 — CDP vs CDM: Feature Comparison
- RC-AT-09 — @CALCTEXT & @CALCDATE (for the @RICHTEXT action tag context, see RC-AT-07)
- RC-AT-07 — Cosmetic Action Tags (includes @RICHTEXT)
- RC-LONG-01 — Longitudinal Project Setup
- RC-LONG-02 — Repeated Instruments and Events Setup

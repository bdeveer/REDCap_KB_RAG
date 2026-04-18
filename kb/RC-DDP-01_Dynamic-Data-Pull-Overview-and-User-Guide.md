RC-DDP-01

**Dynamic Data Pull (DDP) — Overview & User Guide**

| **Article ID** | RC-DDP-01 |
|---|---|
| **Domain** | Integration — Dynamic Data Pull |
| **Applies To** | All REDCap project types (requires administrator enablement) |
| **Prerequisite** | RC-DE-01 — Record Creation and Record Home Page; RC-NAV-REC-04 — Record Status Dashboard |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DDP-02 — DDP Admin Setup & Technical Specs; RC-NAV-REC-04 — Record Status Dashboard; RC-USER-02 — User Rights |

---

# 1. Overview

The Dynamic Data Pull (DDP) is a special feature for importing data into REDCap from an **external source system** (such as an EMR, EDW, or other institutional data repository). Unlike a one-time import, the DDP maintains an ongoing connection to the external system and can fetch new data automatically at regular intervals.

A key characteristic of DDP is its **adjudication process**: data from the external system is never imported silently. Every incoming value must be reviewed and explicitly approved by an authorized REDCap user before it is saved into the project. This gives research teams control over what enters their dataset.

**The DDP can only be enabled by a REDCap Administrator.** Users who want to use DDP for a project must contact their REDCap support team to request it. Once enabled at the system level, an administrator can then activate it for a specific project and grant individual users the necessary privileges to perform field mapping and/or adjudication.

---

# 2. Key Concepts & Definitions

**External Source System**
The external database or clinical system from which REDCap will pull data. Examples include Epic, Cerner, a data warehouse, or any system exposing a compatible web service interface. The name displayed to users may be customized by the administrator.

**Record Identifier**
A value stored in each REDCap record (typically a field on the first instrument) that uniquely links a REDCap record to a record in the external source system — for example, a medical record number (MRN). The DDP requires this value to be present before it can fetch any data for a record.

**One-Time Data Fields**
Source system fields where data is captured only once, such as demographics (date of birth, sex, race). These are mapped to a single REDCap field and fetched once.

**Temporal Data Fields**
Source system fields where data may be recorded many times over time — such as lab results, vital signs, or other longitudinal measurements. When mapping these fields, the user must also designate an associated REDCap date/datetime field and a **day offset** value. REDCap uses these to define a time window when querying the external system.

**Day Offset**
A number of days used to define the time window around a REDCap date field for fetching temporal data. For example, if the associated date field contains 2024-06-15 and the offset is 1, REDCap will request data from the source system for the window 2024-06-14 through 2024-06-16.

**Preview Fields**
Up to 5 source system fields that can be designated to display contextual information about a record when the record identifier is entered. These are used to verify that the correct source system record has been matched (e.g., confirming a patient's last name and date of birth before pulling data). Preview fields are optional but recommended for data quality.

**Adjudication**
The process of reviewing incoming data from the external source system and selecting which values to import into the REDCap project. No external data is saved automatically — a user with the appropriate privilege must approve each value.

---

# 3. How the DDP Works

The DDP operates in two modes — real-time and scheduled:

1. **Real-time fetch:** As soon as a record identifier value is entered into a REDCap record, REDCap immediately queries the external source system for any available data for that identifier.

2. **Scheduled fetch (cron):** REDCap periodically re-checks the source system in the background at a configurable interval (set by the administrator, e.g., every 24 hours). This ensures that new data added to the source system after the initial fetch is detected automatically.

**Important constraints:**
- The DDP can only fetch data for records that **already exist** in the REDCap project. It does not create new records.
- For **temporal fields**, data will not be fetched until the associated REDCap date/datetime field has a value. Once that date is entered, REDCap begins fetching temporal data for that field and will continue checking at each scheduled interval.
- If a project or individual record has had no logged activity for a configurable period (e.g., 7 days by default), REDCap will pause automatic fetching for that project or record until activity resumes.

---

# 4. Enabling DDP for a Project

DDP is enabled in two steps — both requiring administrator action:

1. **System-level enablement:** An administrator enables the DDP globally via the Control Center. This must be done before any project can use it.

2. **Project-level enablement:** An administrator then enables DDP for a specific project via that project's Project Setup page (under "Optional Modules and Customizations").

Once enabled for a project, the administrator can grant individual users one or both of the following DDP-specific privileges on the User Rights page:

- **DDP Mapping/Setup:** The user can access the field mapping page to configure which external source fields map to which REDCap fields.
- **DDP Adjudication:** The user can view incoming data from the external system and approve or reject values for import.

After being granted access, users will see a new DDP step on the Project Setup page linking to the mapping/setup page.

> **Note:** Depending on system configuration, only administrators may be able to grant DDP user privileges. Contact your REDCap support team if you need access.

---

# 5. Field Mapping

Field mapping is performed on the **DDP mapping/setup page**, accessible via Project Setup once DDP is enabled. The mapping page allows a user to connect fields in the external source system to fields in the REDCap project. Fields must already be created in the REDCap project before they can be mapped.

**Steps to map a field:**

1. On the mapping page, select an available field from the external source system.
2. Choose the corresponding REDCap project field to receive the data.
3. If the source field is **temporal**, also select:
   - An associated REDCap **date or datetime field** (determines the center of the time window)
   - A **day offset** (the number of days before and after the date to search)
4. Optionally, configure a **pre-selection rule** for temporal fields with multiple values (e.g., Minimum value, Maximum value, Latest value, Earliest value). If no pre-selection rule is set, REDCap will auto-select a value only if exactly one result falls on the exact calendar date of the associated date field.
5. Save the mapping.

**Preview fields (optional):**
On the same mapping page, up to 5 source fields may be designated as preview fields. These are displayed when the record identifier is entered in REDCap and allow users to confirm they are pulling data for the correct source system record. Using preview fields is strongly recommended for data quality purposes — without them, it is possible to inadvertently import data for the wrong record.

---

# 6. Adjudication Process

After field mapping is complete, data from the external source system is **not imported automatically**. Instead, it queues for adjudication. An authorized user must review and approve each incoming value before it is saved to the project.

### Accessing the Adjudication Screen

The adjudication screen can be accessed from two locations:

1. **Record Status Dashboard:** A new column appears showing a count of pending (unadjudicated) items for each record. Clicking the count opens the adjudication screen for that record.

2. **Data Entry Form:** When viewing a record, a red notification box at the top of the page displays the count of pending items. Clicking the "View" button opens the adjudication screen.

### Using the Adjudication Screen

The adjudication screen displays all unadjudicated data from the external system for the current record. For each item:

- If only **one source value** has been returned for a REDCap field, it is automatically pre-selected.
- For **temporal fields with multiple values**, a value is automatically pre-selected only if:
  - It is the single value occurring on the exact same calendar date as the associated REDCap date/datetime field, **and**
  - No pre-selection rule (e.g., Minimum, Maximum, Latest) has been configured for that field on the mapping page.

The user must select a radio button next to each value they wish to import, then click **Save** to import the approved values. Items not adjudicated during a session remain in the queue and can be reviewed at any future time.

---

# 7. Common Questions

**Q: Why isn't data being pulled for a record?**

**A:** Check that: (1) the record identifier field has a value, (2) the DDP has been enabled for the project by an administrator, and (3) for temporal fields specifically, the associated REDCap date/datetime field has a value.

**Q: Can data be imported without going through adjudication?**

**A:** No. All data from the external source system must be adjudicated (reviewed and approved) before it is saved into the REDCap project. There is no option for automatic, unapproved import.

**Q: What happens if a temporal field has multiple values returned from the source system?**

**A:** All returned values are displayed on the adjudication screen. The user selects which value to import. If a pre-selection rule was configured during mapping (e.g., "Latest value"), REDCap will pre-select the appropriate value, but the user can still override it before saving.

**Q: Can I re-adjudicate a value that was already imported?**

**A:** Once a value has been adjudicated and saved, it is stored in the REDCap project as a standard field value. To change it, the user would edit the field directly through normal data entry (subject to their user rights).

**Q: I don't see a DDP option on Project Setup. What's wrong?**

**A:** DDP must be enabled at the system level by a REDCap Administrator, and may need to be enabled for your specific project as well. It may also be configured to not be displayed to users on the Project Setup page. Contact your REDCap support team to request access.

---

# 8. Common Mistakes & Gotchas

**Entering a record identifier before DDP is mapped.** The DDP will attempt to fetch data as soon as an identifier is entered. If mapping has not been completed yet, the fetch may occur but return no usable data.

**Forgetting to enter the associated date for temporal fields.** Temporal field data will not be fetched — and will not appear for adjudication — until the associated REDCap date/datetime field has a value. This is the most common reason temporal data does not appear.

**Assuming data is imported automatically.** DDP never imports data without explicit user adjudication. Pending data sits in the queue indefinitely until reviewed; it does not import itself.

**Not using preview fields.** If no preview fields are configured and the record identifier is entered incorrectly, it is possible to adjudicate and import data belonging to a different subject. Preview fields are the primary safeguard against this.

---

# 9. Related Articles

- RC-DDP-02 — Dynamic Data Pull: Admin Setup & Technical Specs (administrator configuration, web service setup)
- RC-NAV-REC-04 — Record Status Dashboard (where the adjudication count column appears)
- RC-DE-01 — Record Creation and Record Home Page (record identifier context)
- RC-USER-02 — User Rights: Adding Users and Managing Roles (DDP privilege assignment)

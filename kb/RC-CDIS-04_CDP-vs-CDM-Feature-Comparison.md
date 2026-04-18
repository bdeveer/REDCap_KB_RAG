# RC-CDIS-04 — CDP vs CDM: Feature Comparison

Both **Clinical Data Pull (CDP)** and **Clinical Data Mart (CDM)** use the CDIS infrastructure and FHIR web services to import EHR data into REDCap, but they serve different use cases and work in fundamentally different ways. This article summarizes when to use each and how they compare across key dimensions.

---

## When to Use Each

| Use Case | CDP | CDM |
|---|---|---|
| Real-time, prospective data collection | ✅ Best fit | ❌ |
| Prospective clinical studies/trials | ✅ | ✅ |
| Longitudinal and/or multi-arm studies | ✅ Best fit | ❌ |
| Registries | ❌ | ✅ Best fit |
| Retrospective studies | ❌ | ✅ Best fit |
| Searching specific lab values or diagnoses across a patient cohort | ❌ | ✅ Best fit |
| Bulk import for many patients at once | ❌ | ✅ Best fit |

---

## Side-by-Side Comparison

### Data Mapping to EHR Fields

| Dimension | Clinical Data Pull (CDP) | Clinical Data Mart (CDM) |
|---|---|---|
| **Mapping required?** | Yes — a user with CDP mapping privileges must map EHR fields to REDCap fields before any data can be pulled | No — the project structure and all instruments/fields are pre-defined at project creation |
| **Project structure** | User-defined; project must already have instruments and fields created before mapping | Fixed: Demographics (non-repeating), Vital Signs, Labs, Allergies, Medications, Problem List (all as repeating instruments) |
| **Mapping complexity** | Flexible — supports one-to-many, many-to-one, and many-to-many mappings | Not applicable |
| **Temporal data handling** | Temporal fields (labs, vitals) require an associated date/time field; data is queried within a ± day offset window | Date range is set at project creation; all data within the range is pulled |
| **Allergies, Medications, Problem List** | Merged per category into a Notes/Paragraph field | Each value is stored as a separate repeating instance |
| **Mapping adjustable after setup?** | Yes — mappings can be changed at any time | Configuration changes are restricted (admin approval required if enabled) |

---

### Activation Process

| Dimension | Clinical Data Pull (CDP) | Clinical Data Mart (CDM) |
|---|---|---|
| **Who enables it?** | Administrator enables CDP per project on the Project Setup page | User creates the project; administrator grants user-level Data Mart privileges via Browse Users in the Control Center |
| **User account privilege required?** | No — CDP is a project-level setting | Yes — Data Mart is a user account privilege, not a project-level right |
| **Recommended approval process** | Institutions may require IRB check and EHR access verification before enabling | Same recommendation applies; configuration change requests go through the To-Do List for admin review |
| **EHR Launch required first?** | Yes — must launch REDCap from the EHR at least once to authorize FHIR services | Yes — same requirement applies |

---

### User Privileges

| Dimension | Clinical Data Pull (CDP) | Clinical Data Mart (CDM) |
|---|---|---|
| **Who can map fields?** | Users with CDP Setup/Mapping privileges in the project | Not applicable |
| **Who can pull data?** | Users with appropriate project rights who have EHR access and have completed the EHR Launch | Users with Data Mart privileges who have EHR access and have completed the EHR Launch |
| **Who can request configuration changes?** | Users with CDP mapping rights can update the mapping at any time | Users with Project Setup/Design rights can request changes (admin approval required if that setting is enabled) |
| **User Access Web Service available?** | Yes — optionally configurable by administrators to add an extra layer of access control | No — access is controlled only through the user account privilege |

---

### Data Pull Behavior

| Dimension | Clinical Data Pull (CDP) | Clinical Data Mart (CDM) |
|---|---|---|
| **Scale** | One patient at a time | Many patients at once (bulk) |
| **Adjudication required?** | Yes — all pulled data is held in a cache and must be reviewed/approved by a user | No adjudication step; data is imported directly |
| **When is data fetched?** | Manually when a user adds a patient or enters an MRN; temporal fields are fetched only after the associated date field has a value | When a user clicks "Fetch clinical data"; optionally also via a daily cron job (admin setting) |
| **Automatic monitoring?** | Yes — CDP monitors for new EHR data via cron job for a configurable number of days after the last activity | Optional — administrator can enable a daily automatic pull via project settings |
| **Can data be pulled multiple times?** | Yes, by default (CDP continues monitoring automatically) | No by default — only one pull allowed; must be enabled by administrator |

---

## Key Structural Differences at a Glance

- **CDP is flexible, user-configured, and patient-by-patient.** It requires more setup (mapping) but gives project teams precise control over what is pulled and when.
- **CDM is structured, pre-defined, and bulk-oriented.** It requires less project setup but offers less granular control. The project structure cannot be customized.
- **CDP adjudicates every value before saving;** CDM imports data directly without an adjudication step.
- **CDM access is a user account privilege** (set in the Control Center), not a project right; CDP access is project-level.

---

## Related Articles

- RC-CDIS-01 — CDIS Overview and Control Center Setup
- RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage
- RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage

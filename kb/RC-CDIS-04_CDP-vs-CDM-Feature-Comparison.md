# RC-CDIS-04 — CDP vs CDM: Feature Comparison

| Field | Value |
|---|---|
| Article ID | RC-CDIS-04 |
| Domain | Clinical Data Interoperability Services |
| Applies To | Administrators deciding between CDP and CDM for their institution |
| Prerequisite | RC-CDIS-01 — CDIS Overview and Control Center Setup |
| Version | 1.0 |
| Last Updated | 2026 |
| Author | REDCap Support |
| Related Topics | RC-CDIS-02 — Clinical Data Pull; RC-CDIS-03 — Clinical Data Mart; RC-CDIS-01 — CDIS Overview |

## 1. Overview

Clinical Data Pull (CDP) and Clinical Data Mart (CDM) are two distinct modules built on the same CDIS infrastructure. They serve different use cases: CDP is best for real-time, prospective, patient-by-patient data collection with quality review; CDM is best for bulk imports of many patients at once without adjudication. Understanding the differences helps you choose the right tool for each project.

---

## 2. When to Use Each

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

## 3. Side-by-Side Comparison

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

## 4. Key Structural Differences at a Glance

- **CDP is flexible, user-configured, and patient-by-patient.** It requires more setup (mapping) but gives project teams precise control over what is pulled and when.
- **CDM is structured, pre-defined, and bulk-oriented.** It requires less project setup but offers less granular control. The project structure cannot be customized.
- **CDP adjudicates every value before saving;** CDM imports data directly without an adjudication step.
- **CDM access is a user account privilege** (set in the Control Center), not a project right; CDP access is project-level.

---

## 5. Common Questions

**Q: If I enable both CDP and CDM at the system level, do I have to use both in every project?**
No. Both modules are independent. Once CDIS is configured, you can enable one module, the other module, or both. Each project decides which module(s) to use based on its needs. A single institution can have some projects using CDP, some using CDM, and some using both.

**Q: Can I convert a CDP project to a CDM project or vice versa?**
No. CDP and CDM projects have fundamentally different structures. A CDP project has user-defined instruments and flexible mappings; a CDM project has pre-defined instruments. You cannot convert one to the other. You would need to create a new project with the appropriate module.

**Q: For prospective studies, is CDP always better than CDM?**
CDP is typically better for prospective, real-time studies because it allows flexible field mapping and adjudication. However, CDM can also be used for prospective studies if the pre-defined project structure fits your needs. Evaluate both options based on your specific data needs.

**Q: Why does CDP require adjudication but CDM doesn't?**
Adjudication in CDP provides a quality control step — every data value is reviewed before being saved. CDM imports data directly because it typically pulls historical data in bulk, and the assumption is that this data has already been validated in the EHR. For real-time prospective work, adjudication is valuable; for historical bulk pulls, it is usually less critical.

**Q: If I enable "Allow multiple data pulls" for a CDM project, can I pull different patients each time?**
Yes. Multiple data pulls lets you fetch data as many times as you want. However, the MRN list and date range are typically the same for all pulls unless you separately enable "Allow configuration changes" and request admin approval to modify them.

**Q: Does CDP or CDM pull all available EHR data, or only what I map/request?**
CDP pulls only the fields you explicitly map. CDM pulls data for all available fields within the pre-defined instruments (Demographics, Vital Signs, Labs, Allergies, Medications, Problem List) and the date range specified at project creation. You cannot selectively exclude fields in CDM.

---

## 6. Common Mistakes & Gotchas

**Choosing CDP for a retrospective registry study.** CDP is designed for real-time, prospective, patient-by-patient pulls. If you have a large retrospective cohort and just need to import all available EHR data at once, CDM is the better choice. Using CDP for retrospective work is cumbersome because it requires manual patient-by-patient data entry and adjudication.

**Assuming CDM's pre-defined project structure is customizable.** CDM's fixed instrument structure (Demographics, Vital Signs, Labs, etc.) cannot be changed without risking data pull failures. If your study needs a different project structure, use CDP instead, where you can map any fields you want.

**Forgetting that CDM data is not adjudicated, then discovering data quality issues.** CDM imports data directly without a human review step. If your EHR data contains duplicate entries, unit errors, or other quality issues, they will be imported as-is into REDCap. Plan for a post-import review or data cleaning step if data quality is a concern.

**Enabling both CDP and CDM privileges without clear documentation.** If your institution supports both modules, ensure that users understand which projects should use which module. Document your criteria (e.g., "CDP for prospective studies under 50 patients; CDM for registries over 100 patients"). Without clear guidelines, users may choose the wrong tool.

**Not planning for repeated data in CDM.** In CDM, each individual value from the EHR becomes a separate repeating instance. A patient with 100 lab results will generate 100 repeating instances of the Labs instrument. Plan your data analysis and export strategy accordingly, and be aware of the size of the dataset you are pulling.

---

## 7. Related Articles

- RC-CDIS-01 — CDIS Overview and Control Center Setup
- RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage
- RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage

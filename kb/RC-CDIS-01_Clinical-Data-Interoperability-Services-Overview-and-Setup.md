RC-CDIS-01

**Clinical Data Interoperability Services (CDIS): Overview and Control Center Setup**

| **Article ID** | RC-CDIS-01 |
| --- | --- |
| **Domain** | Clinical Data Interoperability Services |
| **Applies To** | Institutions with FHIR/HL7 integration and EHR connectivity |
| **Prerequisite** | None |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-CDIS-02 — Clinical Data Pull Setup; RC-CDIS-03 — Clinical Data Mart Setup; RC-CDIS-04 — CDP vs CDM Comparison |

---

> **Administrator access required.** The CDIS Control Center page is only available to REDCap super users.

---

## 1. Overview

Clinical Data Interoperability Services (CDIS) is the technical infrastructure that enables REDCap to communicate with Electronic Health Record (EHR) systems. It uses the SMART on FHIR technology stack to standardize how clinical data flows from an EHR into REDCap. CDIS must be configured once at the system level; after setup, two distinct modules — Clinical Data Pull (CDP) and Clinical Data Mart (CDM) — can use it independently to import clinical data in different ways suited to different use cases.

---

## 2. What Is CDIS?

**Clinical Data Interoperability Services (CDIS)** is the technical infrastructure within REDCap that enables communication between REDCap and an EHR (Electronic Health Record) system. It powers two built-in REDCap modules:

- **Clinical Data Pull (CDP)** — imports clinical data one patient at a time, with an adjudication workflow
- **Clinical Data Mart (CDM)** — imports clinical data in bulk for many patients at once

Both modules rely on the same CDIS foundation. Once CDIS is configured at the system level, both CDP and CDM can use it independently.

---

## 3. Key Terminology

| Term | Meaning |
|---|---|
| **EHR / EMR** | Electronic Health Record system (e.g., Epic, Cerner) |
| **CDP** | Clinical Data Pull — one patient at a time |
| **CDM / Data Mart** | Clinical Data Mart — bulk import for many patients |
| **CDIS** | Clinical Data Interoperability Services — the shared infrastructure |
| **FHIR** | Fast Healthcare Interoperability Resources — standardized data format (pronounced "fire") |
| **SMART on FHIR** | Technology stack combining SMART (app authorization) with FHIR web services |
| **OAuth2** | Authorization protocol used by FHIR services to authenticate EHR users |

---

## 4. How CDIS Works

CDIS uses the **SMART on FHIR** technology stack — a set of HTTP web services that transfer structured clinical data out of an EHR in a standardized FHIR format. Most major EHR systems (Epic, Cerner, etc.) implement their own version of FHIR web services, so the setup process varies by EHR, but the overall framework is consistent.

From a security standpoint, CDIS requires **HTTPS (encryption-in-transit)** for all communication between the EHR's FHIR server and the REDCap server. OAuth2 is used to authorize users when data is exported from the EHR.

---

## 5. System-Level Setup (Control Center)

Before any project can use CDP or CDM, an administrator must configure CDIS on the **Clinical Data Interoperability Services** page in the Control Center.

### Setup Steps

1. **Download the setup ZIP file** from the CDIS Control Center page. The ZIP contains setup instructions and technical specifications. Use the EHR-specific instructions if available, otherwise use the "Instructions - General" file.

2. **Create a FHIR client/app on the EHR side** — An EHR technical team contact must create a FHIR app (client) on the EHR system with credentials (e.g., client ID, client secret) that REDCap will use to call the FHIR web services.
   - Exception: For Epic, a separate FHIR app is not required because REDCap integrates with the Epic App Orchard.

3. **Enter configuration details in the Control Center** — Use the credentials and endpoint information provided by the EHR team to populate the CDIS configuration fields. Set either or both modules (CDP, CDM) to **Enabled** on this page.

4. **Create an EHR launch point** — The EHR technical team must create a launch point (e.g., a button, link, or menu item) inside the EHR user interface that opens REDCap embedded within the EHR. This step is required even for Epic.

Once REDCap can be launched from inside the EHR, it can also make outbound calls to the EHR when users access CDP or CDM from the REDCap side (i.e., in their web browser, outside the EHR).

### Where to Find CDIS in the Control Center

The CDIS page is a dedicated section within the Control Center, separate from the general Modules/Services Configuration page. It includes documentation links, the comparison table between CDP and CDM, and configuration fields for enabling each module and entering FHIR credentials.

---

## 6. Additional Control Center Resources on the CDIS Page

The CDIS Control Center page also links to:

- An informational overview page on CDP and CDM (suitable for sharing with users)
- The setup instructions ZIP file with technical specifications
- A comparison table of CDP vs CDM differences (see RC-CDIS-04)
- A survey for requesting additional FHIR data mappings
- Reference lists for mappable FHIR data (DSTU2 and R4 versions)

---

## 7. Common Questions

**Q: What is the difference between CDIS, CDP, and CDM?**
CDIS is the underlying infrastructure and configuration layer that must be set up first. CDP and CDM are two separate modules that both use CDIS to import data. CDP is best for small-scale, real-time, patient-by-patient data pulls with adjudication; CDM is best for bulk imports of many patients at once. You can use both modules simultaneously once CDIS is configured.

**Q: What EHR systems does CDIS support?**
CDIS supports any EHR system that implements FHIR (Fast Healthcare Interoperability Resources) web services. Major systems include Epic, Cerner, and others. The REDCap CDIS Control Center page includes EHR-specific setup instructions for some systems (like Epic) and a general setup guide for others.

**Q: Do I need to configure CDIS separately for CDP and CDM?**
No. CDIS configuration is done once at the system level. After initial setup, you can enable either CDP, CDM, or both modules independently. Both will use the same CDIS credentials and FHIR connection.

**Q: Who can access the CDIS Control Center page?**
Only REDCap super users (administrators) can access the CDIS Control Center page. This is where system-level FHIR credentials are entered and where CDP/CDM modules are enabled. Non-administrators cannot view this page.

**Q: What happens if CDIS is not configured — can projects still use CDP or CDM?**
No. CDIS must be configured and enabled at the system level before any project can use CDP or CDM. If a project tries to use these modules without CDIS configuration, they will not function.

**Q: Is OAuth2 authorization required every time a user accesses CDP or CDM?**
No. After the user completes the initial EHR Launch (which triggers OAuth2 authorization), they are authorized to access CDP or CDM from the REDCap side in a regular web browser without needing to launch from within the EHR again.

---

## 8. Common Mistakes & Gotchas

**Not downloading and reviewing the EHR-specific setup instructions.** The CDIS Control Center provides a setup ZIP file with institution-specific or EHR-specific instructions. Some EHR systems (like Epic) have simplified procedures or different technical requirements. Skipping this step often leads to misconfigured FHIR endpoints or missing required credentials. Always download the ZIP and follow the instructions for your specific EHR.

**Forgetting to create the EHR launch point.** CDIS requires that REDCap be launched from within the EHR (as an embedded window) at least once for OAuth2 authorization to work. If your EHR team does not create a launch button or link inside the EHR interface, users will not be able to authorize and access CDP or CDM. Coordinate with your EHR technical team to confirm the launch point is created before going live.

**Assuming FHIR endpoints and credentials are the same across all environments.** If your institution has separate DEV, TEST, and PROD EHR environments, each one will have its own FHIR endpoints, client IDs, and secrets. A common mistake is to use TEST credentials in a PROD REDCap instance (or vice versa). Verify which environment your REDCap instance connects to and ensure the credentials match that environment.

**Enabling CDP and CDM without clear use-case planning.** Both modules use the same CDIS infrastructure but serve different needs (CDP for real-time, patient-by-patient; CDM for bulk retrospective). Enabling both without a clear plan can lead to confusion about which module to use for a given project. Plan ahead which projects will use which module.

---

## 9. Related Articles

- RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage
- RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage
- RC-CDIS-04 — CDP vs CDM: Feature Comparison
- RC-CC-06 — Control Center: Modules & Services Configuration
- RC-CC-07 — Control Center: Users & Access Management (for granting Data Mart privileges)

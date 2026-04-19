# RC-CDIS-01 — Clinical Data Interoperability Services (CDIS): Overview and Control Center Setup


| **Article ID** | RC-CDIS-01 |
| --- | --- |
| **Author** | See KB-SOURCE-ATTESTATION.md |

> **Administrator access required.** The CDIS Control Center page is only available to REDCap super users.

---

## What Is CDIS?

**Clinical Data Interoperability Services (CDIS)** is the technical infrastructure within REDCap that enables communication between REDCap and an EHR (Electronic Health Record) system. It powers two built-in REDCap modules:

- **Clinical Data Pull (CDP)** — imports clinical data one patient at a time, with an adjudication workflow
- **Clinical Data Mart (CDM)** — imports clinical data in bulk for many patients at once

Both modules rely on the same CDIS foundation. Once CDIS is configured at the system level, both CDP and CDM can use it independently.

---

## Key Terminology

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

## How CDIS Works

CDIS uses the **SMART on FHIR** technology stack — a set of HTTP web services that transfer structured clinical data out of an EHR in a standardized FHIR format. Most major EHR systems (Epic, Cerner, etc.) implement their own version of FHIR web services, so the setup process varies by EHR, but the overall framework is consistent.

From a security standpoint, CDIS requires **HTTPS (encryption-in-transit)** for all communication between the EHR's FHIR server and the REDCap server. OAuth2 is used to authorize users when data is exported from the EHR.

---

## System-Level Setup (Control Center)

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

## Additional Control Center Resources on the CDIS Page

The CDIS Control Center page also links to:

- An informational overview page on CDP and CDM (suitable for sharing with users)
- The setup instructions ZIP file with technical specifications
- A comparison table of CDP vs CDM differences (see RC-CDIS-04)
- A survey for requesting additional FHIR data mappings
- Reference lists for mappable FHIR data (DSTU2 and R4 versions)

---

## Related Articles

- RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage
- RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage
- RC-CDIS-04 — CDP vs CDM: Feature Comparison
- RC-CC-06 — Control Center: Modules & Services Configuration
- RC-CC-07 — Control Center: Users & Access Management (for granting Data Mart privileges)

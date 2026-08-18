---
id: RC-CDIS-01
title: 'Clinical Data Interoperability Services (CDIS): Overview and Control Center
  Setup'
domain: Clinical Data Interoperability Services
applies_to:
- Institutions with FHIR/HL7 integration and EHR connectivity
requires: Any supported version
verified_against: REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page
  not re-captured
prerequisites:
- None
version: '1.1'
last_updated: 2026-08
related:
- id: RC-CDIS-02
  title: 'Clinical Data Pull (CDP): Setup and Usage'
- id: RC-CDIS-03
  title: 'Clinical Data Mart (CDM): Setup and Usage'
- id: RC-CDIS-04
  title: 'CDP vs CDM: Feature Comparison'
tags:
- clinical data interoperability services
synonyms:
- how do i connect redcap to an ehr
- set up cdis in the control center
- smart on fhir integration with redcap
- import clinical data from electronic health records
- what is the difference between cdp and cdm
- configure ehr connectivity for redcap
- fhir hl7 clinical data setup
- enable clinical data pull and data mart
---

> **Administrator access required.** The CDIS Control Center page is only available to REDCap super users.

---

# 1. Overview

Clinical Data Interoperability Services (CDIS) is the technical infrastructure that enables REDCap to communicate with Electronic Health Record (EHR) systems. It uses the SMART on FHIR technology stack to standardize how clinical data flows from an EHR into REDCap. CDIS must be configured once at the system level; after setup, two distinct modules — Clinical Data Pull (CDP) and Clinical Data Mart (CDM) — can use it independently to import clinical data in different ways suited to different use cases.

---

# 2. What Is CDIS?

**Clinical Data Interoperability Services (CDIS)** is the technical infrastructure within REDCap that enables communication between REDCap and an EHR (Electronic Health Record) system. It powers two built-in REDCap modules:

- **Clinical Data Pull (CDP)** — imports clinical data one patient at a time, with an adjudication workflow
- **Clinical Data Mart (CDM)** — imports clinical data in bulk for many patients at once

Both modules rely on the same CDIS foundation. Once CDIS is configured at the system level, both CDP and CDM can use it independently.

---

# 3. Key Terminology

| Term | Meaning |
|---|---|
| **EHR / EMR** | Electronic Health Record system (e.g., Epic, Cerner) |
| **CDP** | Clinical Data Pull — one patient at a time |
| **CDM / Data Mart** | Clinical Data Mart — bulk import for many patients |
| **CDIS** | Clinical Data Interoperability Services — the shared infrastructure |
| **FHIR** | Fast Healthcare Interoperability Resources — standardized data format (pronounced "fire") |
| **SMART on FHIR** | Technology stack combining SMART (app authorization) with FHIR web services |
| **OAuth2** | Authorization protocol used by FHIR services to authenticate EHR users |
| **Break the Glass (BTG)** | Epic's mechanism for restricting access to a protected patient's record, requiring the requester to take a deliberate, logged action to obtain it. See Section 6a |

---

# 4. How CDIS Works

CDIS uses the **SMART on FHIR** technology stack — a set of HTTP web services that transfer structured clinical data out of an EHR in a standardized FHIR format. Most major EHR systems (Epic, Cerner, etc.) implement their own version of FHIR web services, so the setup process varies by EHR, but the overall framework is consistent.

From a security standpoint, CDIS requires **HTTPS (encryption-in-transit)** for all communication between the EHR's FHIR server and the REDCap server. OAuth2 is used to authorize users when data is exported from the EHR.

---

# 5. System-Level Setup (Control Center)

Before any project can use CDP or CDM, an administrator must configure CDIS on the **Clinical Data Interoperability Services** page in the Control Center.

## Setup Steps

1. **Download the setup ZIP file** from the CDIS Control Center page. The ZIP contains setup instructions and technical specifications. Use the EHR-specific instructions if available, otherwise use the "Instructions - General" file.

2. **Create a FHIR client/app on the EHR side** — An EHR technical team contact must create a FHIR app (client) on the EHR system with credentials (e.g., client ID, client secret) that REDCap will use to call the FHIR web services.
   - Exception: For Epic, a separate FHIR app is not required because REDCap integrates with the Epic App Orchard.

3. **Enter configuration details in the Control Center** — Use the credentials and endpoint information provided by the EHR team to populate the CDIS configuration fields. Set either or both modules (CDP, CDM) to **Enabled** on this page.

4. **Create an EHR launch point** — The EHR technical team must create a launch point (e.g., a button, link, or menu item) inside the EHR user interface that opens REDCap embedded within the EHR. This step is required even for Epic.

Once REDCap can be launched from inside the EHR, it can also make outbound calls to the EHR when users access CDP or CDM from the REDCap side (i.e., in their web browser, outside the EHR).

## Where to Find CDIS in the Control Center

The CDIS page is a dedicated section within the Control Center, separate from the general Modules/Services Configuration page. It includes documentation links, the comparison table between CDP and CDM, and configuration fields for enabling each module and entering FHIR credentials.

---

# 6. Additional Control Center Resources on the CDIS Page

The CDIS Control Center page also links to:

- An informational overview page on CDP and CDM (suitable for sharing with users)
- The setup instructions ZIP file with technical specifications
- A comparison table of CDP vs CDM differences (see [RC-CDIS-04 — CDP vs CDM: Feature Comparison](RC-CDIS-04_CDP-vs-CDM-Feature-Comparison.md))
- A survey for requesting additional FHIR data mappings
- Reference lists for mappable FHIR data (DSTU2 and R4 versions)

## 6.1 Access Token Priority Rules Manager *(15.1.0+)*

An optional feature for CDIS-enabled projects, letting project owners and administrators define **prioritisation rules for selecting which FHIR access token** is used to fetch data from the EHR.

It matters where several users in a project each hold a FHIR access token. Without rules, the token chosen is not necessarily the one you would pick — and tokens differ in what they can reach, so the same fetch can return different results depending on whose token was used.

## 6.2 CDIS Infrastructure Settings

Several changes affect where CDIS puts things and how background work behaves. They rarely need attention until something breaks, at which point they are the first place to look.

| Change | Version |
| --- | --- |
| Twig replaces Blade as the templating engine for the EHR authorisation workflow; the enhanced error page lists relevant pages visited | 15.5.0 |
| Data Mart FHIR fetching runs each MRN and resource — including paginated FHIR results — in **separate subprocesses**, improving performance and isolation | 15.9.0 |
| A weekly **cron job** prunes expired FHIR tokens, preventing memory issues | 16.0.0 |
| Administrators may set a **dedicated folder for CDIS temporary files**, and a separate CDIS cache folder, keeping CDIS temp data out of the system temp directory. Improves stability where load balancers or multiple app servers are in play | 16.0.8 |
| A **fetch reconciler** resets records stuck in a "fetching" state | 16.0.8 |
| Temporary state moved to temp-data database tables with cron cleanup, so storage does not grow unbounded | 16.1.1 |
| Data Mart processing follows **record sort order** rather than MRN sort order | 16.1.2 |
| Grouped diagnostics, suggested next steps, safe callback metadata and sanitized token-endpoint response details on the FHIR launcher error page | 17.2.0 |
| SMART on FHIR EHR launch better maintains launch context and returns users to the intended REDCap workflow through browser restrictions, Shibboleth or external login handoffs | 17.1.2 |
| CDP, FHIR and Data Mart workflows report additional progress detail, identifying the affected project and processing stage | 17.3.1 |

> **Note — the dedicated CDIS temp folder (16.0.8) is worth setting on multi-server deployments.** Where CDIS temp files land in a per-server system temp directory, a background job started on one application server may not find state written by another. The dedicated folder makes the location explicit and shared.

> **Version caveats — background fetching.** Two defects left background CDP work silently incomplete rather than visibly failing. Background workflows could **stop before processing all selected data**, leaving records incomplete (fixed 16.1.6 Standard / 16.0.17 LTS), and background jobs could **crash repeatedly** where large fetch histories or stale fetch states exhausted server memory (fixed 17.0.6 Standard / 16.0.28 LTS). If background fetching on an older instance appears to run but leaves gaps, these are the likely cause rather than the mapping.

---

# 6a. Break the Glass (Epic only)

Some patients' records are **protected** in Epic — VIP patients, employees, staff family members, or anyone flagged for restricted access. Retrieving their data requires the requester to deliberately "break the glass": an explicit, logged action acknowledging they are accessing a protected record.

When CDIS encounters such a patient, the data does not simply arrive. REDCap detects the protection, surfaces it, and requires a user to confirm before the pull can proceed.

> **Note:** This is an **Epic-only** feature. It has no equivalent in other EHR systems CDIS connects to.

## 6a.1 The workflow

1. During a data pull, CDIS detects that a patient — or, from 16.0.4, a specific **resource or endpoint** — is protected.
2. The patient is added to a per-project **protected patient list**.
3. A user with access opens the **Break the Glass** page and chooses to proceed.
4. Only at that point does REDCap request a BTG-enabled FHIR token from Epic.
5. The user completes a **sensitive-data confirmation** step.
6. Data flows, and the action is logged.

> **Important — the token is requested late, deliberately.** Before 15.8.1, REDCap requested the BTG token as soon as a protected patient was detected. Those tokens could expire before anyone acted on them, so the break would fail when finally attempted. Since 15.8.1 the token is requested only when a user actually chooses to break the glass, guaranteeing it is valid at the moment it is used.

## 6a.2 How the feature has changed

| Change | Version |
| --- | --- |
| BTG logging extended to cover failures and no-op cases — not just successful breaks, but also where BTG was deemed unnecessary or errored | 15.0.0 |
| Data can flow from Epic even when the **Patient (demographics) endpoint is not part of the pull**. Previously, patients could not be evaluated for BTG unless that endpoint was explicitly requested | 15.4.0 |
| Token requested on user action rather than on detection; protected patients remain listed for **5 days** rather than 1 | 15.8.1 |
| Clearer feedback when obtaining a FHIR token during the BTG process | 15.8.4 |
| **Resource/endpoint-level** protection detection, not only patient-level, so BTG can be tracked and re-verified against the specific request that returned partial or limited data | 16.0.4 |
| Protected-patient list TTL raised from 5 days to **10 days**, and the list consolidated into a single managed location to avoid mismatches between storage paths | 16.0.6 |
| Candidate lists cached in the REDCap `temp` folder using a `.btg` extension and a filename containing the project PID | 16.0.8 |
| Temporary state moved into **temp-data database tables** rather than files, removing sensitivity to filesystem timestamp and locking quirks; expired entries cleaned by cron | 16.1.1 |
| Sensitive-data confirmation accepts **email code, SMS code, Duo push and OTP** in addition to password | 16.1.2 |

The 16.1.2 change matters operationally: on earlier versions, confirmation was password-only, which is awkward for anyone authenticating through SSO who may not have a REDCap password to type.

> **Version caveat (below 17.1.3 Standard):** On institutions whose web server requires explicit page file names in URLs, users could not open the Break the Glass page at all. Fixed in 17.1.3.

> **Version caveat (below 17.4.1 Standard):** When Clinical Data Pull met a BTG-protected patient during a **background** fetch, repeated patient requests could exhaust memory and crash the REDCap background system before any clinical data was retrieved. On affected versions a single protected patient can stall background fetching for the whole instance, so this is worth ruling out when background CDP jobs fail without an obvious cause.

---

# 7. Common Questions

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

# 8. Common Mistakes & Gotchas

**Not downloading and reviewing the EHR-specific setup instructions.** The CDIS Control Center provides a setup ZIP file with institution-specific or EHR-specific instructions. Some EHR systems (like Epic) have simplified procedures or different technical requirements. Skipping this step often leads to misconfigured FHIR endpoints or missing required credentials. Always download the ZIP and follow the instructions for your specific EHR.

**Forgetting to create the EHR launch point.** CDIS requires that REDCap be launched from within the EHR (as an embedded window) at least once for OAuth2 authorization to work. If your EHR team does not create a launch button or link inside the EHR interface, users will not be able to authorize and access CDP or CDM. Coordinate with your EHR technical team to confirm the launch point is created before going live.

**Assuming FHIR endpoints and credentials are the same across all environments.** If your institution has separate DEV, TEST, and PROD EHR environments, each one will have its own FHIR endpoints, client IDs, and secrets. A common mistake is to use TEST credentials in a PROD REDCap instance (or vice versa). Verify which environment your REDCap instance connects to and ensure the credentials match that environment.

**Enabling CDP and CDM without clear use-case planning.** Both modules use the same CDIS infrastructure but serve different needs (CDP for real-time, patient-by-patient; CDM for bulk retrospective). Enabling both without a clear plan can lead to confusion about which module to use for a given project. Plan ahead which projects will use which module.

---

# 9. Related Articles

- [RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage](RC-CDIS-02_Clinical-Data-Pull-Setup-and-Usage.md)
- [RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage](RC-CDIS-03_Clinical-Data-Mart-Setup-and-Usage.md)
- [RC-CDIS-04 — CDP vs CDM: Feature Comparison](RC-CDIS-04_CDP-vs-CDM-Feature-Comparison.md)
- [RC-CC-06 — Control Center: Modules & Services Configuration](RC-CC-06_Control-Center-Modules-and-Services.md)
- [RC-CC-07 — Control Center: Users & Access Management](RC-CC-07_Control-Center-User-Management.md) (for granting Data Mart privileges)

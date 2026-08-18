

**REDCap SHARE: Overview & Onboarding**

| **Article ID** | [RC-CDIS-05 — REDCap SHARE: Overview & Onboarding](RC-CDIS-05_REDCap-SHARE-Overview-and-Onboarding.md) |
|---|---|
| **Domain** | Clinical Data Interoperability Services |
| **Applies To** | REDCap Administrators (Sections 4–6); study teams evaluating participant-mediated EHR data collection. Requires a REDCap+ subscription |
| **Requires** | REDCap v17.3.0+ (Standard); LTS 17.3.x and higher. REDCap+ subscription required |
| **Verified Against** | REDCap v17.3.6 (LTS) |
| **Prerequisite** | [RC-CDIS-01 — Clinical Data Interoperability Services: Overview & Control Center Setup](RC-CDIS-01_Clinical-Data-Interoperability-Services-Overview-and-Setup.md) |
| **Version** | 1.0 |
| **Last Updated** | 2026-08 |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage](RC-CDIS-02_Clinical-Data-Pull-Setup-and-Usage.md); [RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage](RC-CDIS-03_Clinical-Data-Mart-Setup-and-Usage.md); [RC-CDIS-04 — CDP vs CDM: Feature Comparison](RC-CDIS-04_CDP-vs-CDM-Feature-Comparison.md); [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md); [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) |
| **Synonyms** | what is redcap share; how do participants share ehr data with a study; difference between redcap share and cdis; collect clinical data from outside our own hospital; smart on fhir participant authorization redcap; redcap share onboarding survey and allow list; enable redcap share for a project; does redcap store the participant patient portal password |

---

## 1. Overview

**REDCap SHARE** lets research participants connect to their own healthcare provider's patient portal and authorize the transfer of selected clinical data into a REDCap project. The participant chooses their healthcare organization, signs in through that organization's patient portal, and decides whether to grant access. REDCap never sees or stores the participant's patient portal username or password.

The distinction from REDCap's other EHR integrations is **who holds the relationship with the EHR**. Clinical Data Pull and Clinical Data Mart connect the *institution* to the institution's *own* EHR, so they only reach patients seen within that health system. SHARE is mediated by the participant, so it can retrieve data from supported healthcare organizations anywhere — including providers your institution has no relationship with. For a multisite study, or any study where participants receive care elsewhere, that is the difference between having clinical data and not having it.

This article covers what SHARE is, how it compares with CDP and CDM, and the administrator onboarding path. It is written from the Control Center Information page and the release notes.

> **Version caveat (introduced 17.3.0; reaches LTS with the 17.3.x line):** SHARE does not exist on earlier versions and **requires a REDCap+ subscription**. On a 17.3.x instance without a subscription, the Control Center page still renders and the onboarding information is readable — the feature simply cannot be enabled. Note also that REDCap 17.2.1 fixed a documentation bug where SHARE-related Smart Variables appeared in the Smart Variables reference before the feature had shipped; if you saw them on 17.2.0, they were not usable.

---

## 2. Key Concepts & Definitions

### SMART on FHIR

The industry standard REDCap uses to connect to an EHR on a participant's behalf. The participant authenticates directly with their provider and REDCap receives a scoped authorization, rather than a credential.

### Participant-mediated retrieval

Data flows because the *participant* authorized it at their own provider, not because the institution has a data agreement with that provider. This is what allows SHARE to reach organizations outside the home health system.

### Healthcare organization catalog

The list of EHR endpoints a REDCap instance can offer participants. SHARE supports automatic downloading of these lists from external provider catalogs — **Epic**, **Oracle Health**, or Vanderbilt-curated lists — rather than requiring each endpoint to be registered by hand.

### Dynamic client registration

The mechanism by which REDCap registers itself as a client with a supported EHR automatically, instead of an administrator arranging a client ID per organization.

### Allow list

A list, maintained centrally as part of onboarding, of the REDCap base URLs permitted to use SHARE. An instance whose URL is not on it cannot connect, which is why the onboarding survey asks for every instance URL you intend to use.

### Job Diagnostics

The administrator tool showing the state of SHARE data-retrieval jobs — the current processing stage, the next eligible run time, and controls to requeue failed EHR requests after fixing a request or an EHR configuration.

---

## 3. SHARE compared with CDP and CDM

| | **CDP / CDM** (see [RC-CDIS-04](RC-CDIS-04_CDP-vs-CDM-Feature-Comparison.md)) | **REDCap SHARE** |
|---|---|---|
| Who authorizes access | The institution, via its own EHR integration | The participant, via their provider's patient portal |
| Reachable data | Patients seen within the institution's own health system | Any supported healthcare organization the participant uses |
| Suits | Single-site studies at the institution's own health system | Multisite studies, and participants who receive care elsewhere |
| Participant action required | None | Must actively select their organization, sign in, and authorize |
| Licensing | Included | **Requires REDCap+** |
| Introduced | Long-standing | 17.3.0 |

They are complementary rather than alternatives. An institution can run CDP for its own patients and SHARE for participants treated elsewhere.

---

## 4. Before you can use SHARE

SHARE is not self-serve even with a REDCap+ subscription. There is an institutional onboarding step with an external dependency, so allow lead time before a study needs it.

1. **Complete the REDCap SHARE setup survey**, linked from the Control Center SHARE page. It asks for the REDCap **base URL or URLs** of every instance that will use SHARE, so they can be added to the required allow list. Include test and staging instances if you intend to pilot there — an instance not on the list cannot connect.
2. **Receive your institutional settings.** After the survey is processed, your institution is given the settings needed to connect to supported FHIR systems, **including client IDs for Epic and Oracle Health**.
3. **Enable SHARE at the system level**, then for individual projects.
4. **Grant the REDCap SHARE user right** to project users who need it. Without it they cannot reach the SHARE setup pages or dashboards, even in a project where SHARE is enabled.
5. **Test before sending any participant links.** Verify the participant workflow end to end, the project mappings, user rights, and the data that actually lands in the project.

> **Important:** Step 1 gates everything else and depends on an external party, so it is the step to start early. A subscription alone does not make SHARE usable.

---

## 5. The Control Center SHARE page

**Control Center → REDCap SHARE.** The page carries a REDCap+ badge and has two tabs:

| Tab | Contents |
|---|---|
| **Information** | Feature overview, the onboarding prerequisites, links to the Administrator Guide, the onboarding survey and the FAQs, plus the public links below |
| **Projects** | Projects on this instance in relation to SHARE |

### 5.1 Public SHARE links

Two links on the Information tab point at pages that do not require a Control Center login:

- **Public healthcare organization directory** — a searchable, browsable directory of the healthcare organizations currently published in this instance's SHARE catalog. Added in 17.3.1 for administrators and visitors reviewing the catalog; note that consumer synchronization continues to use the existing JSON catalog behind the scenes, so this directory is a human-readable view rather than the integration mechanism.
- **Public SHARE information page** — the explanatory page shown to someone who opens REDCap SHARE help. It describes what SHARE does and how participants use it, and is the page to point prospective participants or an IRB at.

### 5.2 Documentation resources

The Information tab links to the **REDCap SHARE Administrator Guide**, the **onboarding survey**, and the **FAQs**. Testing instructions accompany the guide. Further public information is published by the REDCap consortium at `projectredcap.org/software/share/`.

---

## 6. What SHARE offers in a project

From the release notes; confirm the specifics against a subscribed instance before relying on them operationally.

- Connections to **multiple** EHR patient portals, not just one
- **Configurable mapping** of EHR data to REDCap fields and forms
- **Record-specific participant links** and associated **Smart Variables**
- Integration with **surveys** and **Survey Auto-Continue**, so authorization can sit inside a survey flow
- **Metrics, record tracking, mapping validation** and administrator **diagnostic tools**

Refinements added in 17.3.1:

- Mapping administrators can select which **Patient identifier** to save by matching its FHIR system or type, using either an exact value or a regular expression
- SHARE prioritises authorized EHR fetching ahead of retained-payload processing, and **Job Diagnostics** exposes the current stage and the next eligible time
- Provider-specific **CarePlan** searches for Epic and SMART Health IT, with clearer guidance when an EHR requires an unsupported category
- **System Statistics** distinguishes project participants from EHR-specific REDCap records within the SHARE totals

> **Note — pending confirmation.** Sections 5 and 6 describe the Projects tab and the in-project experience from release notes and the Control Center Information page only. The project-level setup pages, dashboards and mapping interface have not yet been reviewed on a subscribed instance, and this article should be extended once they have.

---

## 7. Common Questions

**Q: What is REDCap SHARE?**

**A:** A REDCap+ feature that lets research participants connect to their own healthcare provider's patient portal and authorize transfer of selected clinical data into a REDCap project, using SMART on FHIR.

**Q: How is SHARE different from CDIS, CDP or CDM?**

**A:** CDP and CDM connect your institution to your institution's own EHR, so they only reach patients seen within your health system. SHARE is authorized by the participant at their own provider, so it can retrieve data from supported healthcare organizations anywhere — including providers your institution has no relationship with.

**Q: Does REDCap store the participant's patient portal username and password?**

**A:** No. The participant authenticates directly with their healthcare organization's portal, and REDCap receives a scoped authorization rather than credentials. REDCap does not collect or store the username or password.

**Q: We have a REDCap+ subscription. Can we start using SHARE today?**

**A:** Not immediately. Your institution must first complete the REDCap SHARE setup survey so your REDCap base URLs are added to the required allow list, and then receive the connection settings and EHR client IDs. Start that step well before a study depends on it.

**Q: A user cannot see the SHARE setup pages in a project where SHARE is enabled. Why?**

**A:** They are missing the **REDCap SHARE user right**. Enabling SHARE for a project does not by itself grant access to its setup pages or dashboards.

**Q: Which EHR systems does SHARE support?**

**A:** It supports automatic organization-list downloading from Epic, Oracle Health and Vanderbilt-curated catalogs, and 17.3.1 added provider-specific handling for Epic and SMART Health IT. Your institution receives client IDs for Epic and Oracle Health as part of onboarding. Whether a given participant's provider is reachable depends on that organization appearing in your catalog.

**Q: Where can participants read about SHARE before they consent?**

**A:** The public SHARE information page, linked from the Control Center SHARE page. It requires no login and explains what SHARE does and how participants use it, which makes it suitable to reference from participant-facing material.

**Q: We are on an LTS instance. Do we have SHARE?**

**A:** Only on LTS 17.3.x or higher. LTS 16.0.x was branched before SHARE existed. See [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md).

---

## 8. Common Mistakes & Gotchas

**Assuming a REDCap+ subscription is sufficient.** SHARE additionally requires institutional onboarding through an external survey and allow-list process, plus receipt of EHR client IDs. Treating it as a toggle to flip on the day a study needs it will disappoint. Begin onboarding while the study is still in design.

**Omitting test and staging instances from the onboarding survey.** The survey asks which REDCap base URLs will use SHARE, and only those are added to the allow list. Listing production alone means you cannot pilot the participant workflow anywhere safe, and discovering that late forces either an untested launch or a wait for the list to be amended.

**Enabling SHARE for a project and stopping there.** Project users additionally need the REDCap SHARE user right before they can open the setup pages or dashboards. The symptom is a study coordinator reporting that the feature "isn't there" in a project where it demonstrably is.

**Expecting SHARE to reach any provider.** A participant can only connect to a healthcare organization present in your instance's catalog. Catalogs are downloaded from Epic, Oracle Health or Vanderbilt-curated lists, so a participant whose provider is absent cannot contribute data no matter how willing they are. Check catalog coverage against your expected population before promising SHARE data in a protocol.

**Sending participant links before testing the full workflow.** SHARE spans a participant-facing authorization journey, field mappings, user rights and an import path. Each can be individually correct while the end-to-end result is wrong, and participants are a poor audience to debug against — a failed or confusing authorization is not usually retried. Test the whole path with a real record first.

---

## 9. Related Articles

- [RC-CDIS-01 — Clinical Data Interoperability Services: Overview & Control Center Setup](RC-CDIS-01_Clinical-Data-Interoperability-Services-Overview-and-Setup.md) — the CDIS umbrella and system-level EHR setup
- [RC-CDIS-04 — CDP vs CDM: Feature Comparison](RC-CDIS-04_CDP-vs-CDM-Feature-Comparison.md) — choosing between the institution-side integrations
- [RC-CDIS-02 — Clinical Data Pull (CDP): Setup and Usage](RC-CDIS-02_Clinical-Data-Pull-Setup-and-Usage.md) and [RC-CDIS-03 — Clinical Data Mart (CDM): Setup and Usage](RC-CDIS-03_Clinical-Data-Mart-Setup-and-Usage.md)
- [RC-PLUS-01 — REDCap+: Overview and Subscription](RC-PLUS-01_REDCap-Plus-Overview-and-Subscription.md) — what the subscription covers
- [RC-INFRA-03 — REDCap Versions, Release Lines & Patching](RC-INFRA-03_REDCap-Versions-Release-Lines-and-Patching.md) — why an LTS instance may not have SHARE yet
- [RC-USER-03 — User Rights: Configuring User Privileges](RC-USER-03_User-Rights-Configuring-User-Privileges.md) — granting the REDCap SHARE user right

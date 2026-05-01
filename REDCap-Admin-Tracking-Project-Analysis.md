# REDCap Administrative Tracking Project — Design Analysis

**Prepared for:** Internal review / team discussion  
**Project status at time of analysis:** Development (not yet in production)  
**Analysis date:** 2026-05-01

---

## 1. What This Project Does

This is a **non-longitudinal operational tracking project** that uses REDCap as a request management and administrative workflow platform — essentially using REDCap to manage REDCap. It handles the full lifecycle of research project onboarding: intake from researchers, triage and review by staff, integration with the institutional IRB system, server assignment, compliance scoping (including Part 11), and ongoing project status tracking.

Key capabilities built into the project:

- **Researcher intake via survey** — researchers submit project requests without needing a REDCap account
- **Staff triage and review workflow** — internal admin-only fields are gated behind reviewer identity fields and are not visible to requesters
- **IRB system integration** — fields automatically populated from an external IRB management system, with manual entry fallback when integration data is unavailable
- **Multi-server routing** — conditional fields and instructions that adapt based on which server environment a project is being assigned to
- **Part 11 compliance pathway** — a dedicated instrument with specialized instructions for projects requiring a validated 21 CFR Part 11 environment
- **Mismatch detection** — calculated fields that flag discrepancies between what was collected in this system and what the connected server reports (e.g., data collection method, eConsent configuration)
- **Repeating instruments** for project records (one per project tied to a study account), study contacts, and funding sources

The overall design closely follows the operational request management pattern described in **RC-OPS-01**.

---

## 2. What's Working Well

### 2.1 Repeating instruments are configured correctly
All three repeating instruments have **custom form labels** using piped field values, making instances immediately identifiable without having to open each one:

| Instrument | Custom Label Pattern |
|---|---|
| Project Record | Server project ID + project name |
| Study Contacts | Contact first name + last name + role |
| Funding Sources | Sponsor name + status |

This is exactly the best practice described in RC-OPS-01 and RC-LONG-02. Without these labels, staff would see only "Instance 1, Instance 2..." which is unusable once a study accumulates multiple projects or contacts.

### 2.2 @CALCTEXT fallback chaining for multi-source data
The project uses a well-structured nested `if()` pattern to display the best available value when data may come from the IRB integration, from manual staff entry, or from historical records:

```
@CALCTEXT(if([irb_source]<>'', [irb_source], if([manual_source]<>'', [manual_source], [historical_source])))
```

This pattern is robust: it prioritizes the most authoritative source (the integration), gracefully degrades to manual entry when the integration hasn't run, and falls back to historical data as a last resort. Staff always see a value rather than a blank.

### 2.3 Field naming prefix convention
The project uses a consistent, systematic prefix scheme across ~300+ fields:

| Prefix | Meaning |
|---|---|
| `dst_` | Data systems triage |
| `pc_` | Project creation / intake |
| `adm_` | Admin review |
| `profile_` | Profile-level calculated/display fields |
| `server_` | Server-integrated data |
| `ires_` | External IRB system data |
| `h_` | Historical data |
| `p11_` | Part 11-specific fields |
| `sreview_` | Server review / assignment |

Within the external integration fields, a suffix convention (`_E` for extracted/integration data, `_M` for manually entered) cleanly communicates data provenance at a glance. This is excellent practice for a project of this complexity and will significantly reduce maintenance burden.

### 2.4 Mismatch detection fields
Fields like `adm_datacollect_mismatch` and `adm_econsent_mismatch` use calculated logic to compare what was entered during intake against what the connected server reports. These are marked `@READONLY` so staff can see the discrepancy without accidentally overwriting it. This is a strong data quality pattern that helps catch configuration drift between systems.

### 2.5 Descriptive cross-reference fields in repeating instruments
The repeating instruments pipe PI and primary contact information from the root (non-repeating) instrument into the review section of each instance. Reviewers can see who the study PI is without having to navigate away. This matches the guidance in RC-OPS-01 §4.3.

---

## 3. Suggestions for Improvement

### 3.1 Remove or archive the test instrument before production
The project contains an instrument called **"TEST: Assign email"** that appears to be a development artifact. Instruments left in the data dictionary at production move increase the chance of accidental data collection, inflate the data dictionary, and add noise to the record status dashboard. Recommendation: either delete this instrument or move its fields into the archive instrument before the project moves to production.

### 3.2 Replace domain-based branching logic with a role or non-empty check
The user verification field uses branching logic that checks for specific institutional email domain formats. This type of check is fragile for two reasons: email domains can change (due to rebranding, mergers, or new affiliate domains), and it embeds institution-specific identifiers directly into the data dictionary. RC-OPS-01 §8 specifically flags this as an anti-pattern.

**Recommended alternative:** Gate review fields on a non-empty reviewer identity check (`[reviewer_field] <> ''`) or on a role dropdown value. This is more resilient and keeps the data dictionary free of institutional specifics.

### 3.3 Document the field naming convention formally
The prefix scheme (Section 2.3 above) is excellent, but it only delivers its full value if all contributors know about it. Currently it is implicit — discoverable by reading the data dictionary, but not stated anywhere in the project. Recommendation: add a brief explanation of the prefix scheme to the **Project Notes** field in Project Setup (Additional Customizations) or to a descriptive field at the top of the first instrument. New staff or future maintainers who onboard to this project will benefit significantly.

### 3.4 Be aware of @HIDECHOICE's export behavior
The project uses `@HIDECHOICE` to suppress specific dropdown options in data entry. This is a valid design technique — it hides retired or inapplicable choices without requiring a data dictionary change. However, **@HIDECHOICE is display-only**: the hidden values remain fully accessible in data exports, the Codebook, and the API. Any record that previously stored a now-hidden value will still expose that value in exports.

Implication for reporting: when building custom reports or API-based extracts against fields that use @HIDECHOICE, account for all coded values, not just the visible ones. Staff who query this data should be made aware of this behavior. Reference: RC-FD-10 §11.5.

### 3.5 API data exports must be chunked — do not export all records at once
During analysis, a full API record export caused a **PHP memory exhaustion error** on the server. The error is returned as HTTP 200 with an HTML fatal error block embedded in the response — a confusing failure that can look like a successful but malformed response to an API client.

This is not unusual for administrative projects that accumulate many records with many repeating instrument instances over time. Any automated workflow that pulls data from this project via the API must chunk its exports using one or more of these strategies:

- Batch by record ID ranges using the `records` parameter
- Limit to specific fields or instruments using the `fields` or `forms` parameters
- Use `dateRangeBegin` / `dateRangeEnd` to export only records modified in a given window

This should be documented for whoever manages the API integration for this project.

### 3.6 Consider adding missing data codes if intake data is frequently incomplete
The project has no missing data codes configured. For a research administration system where certain fields may legitimately be unknown at intake (e.g., IRB number not yet assigned, funding not yet confirmed), missing data codes provide a cleaner alternative to leaving fields blank. Blank fields are ambiguous — it is impossible to distinguish "not yet collected" from "genuinely not applicable" without a code. This is worth discussing as the project moves toward production.

### 3.7 Review field count for active use before production transition
The data dictionary has approximately 300+ fields. Before production move, it is worth auditing whether all fields are actively used or whether some represent abandoned design ideas. Very large data dictionaries have practical costs: slower online designer performance, longer export times, and higher cognitive load for staff who need to understand the project. Fields in the `archive` instrument that are already `@HIDDEN` are fine — the concern is active, visible fields that may no longer serve a purpose.

---

## 4. Summary

| Area | Assessment |
|---|---|
| Repeating instrument setup | ✅ Well configured with custom labels |
| Multi-source fallback logic (@CALCTEXT) | ✅ Solid implementation |
| Field naming conventions | ✅ Systematic and consistent |
| Mismatch detection | ✅ Good data quality practice |
| Test instrument in data dictionary | ⚠️ Should be removed before production |
| Domain-based branching logic | ⚠️ Fragile — recommend role/non-empty check instead |
| @HIDECHOICE export behavior | ⚠️ Staff and report-builders need to be aware |
| API export strategy | ⚠️ Full export fails — chunking is required |
| Missing data codes | 💬 Worth discussing before production |
| Field count audit | 💬 Recommended before production transition |

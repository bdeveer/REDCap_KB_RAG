RC-DE-06

**Data Entry — Bio-Medical Ontologies**

| **Article ID** | RC-DE-06 |
|---|---|
| **Domain** | Data Entry |
| **Applies To** | All REDCap project types; data entry users |
| **Prerequisite** | RC-DE-05 — Field Validations |
| **Version** | 1.0 |
| **Last Updated** | 2026 |
| **Author** | REDCap Support |
| **Related Topics** | RC-DE-05 — Field Validations; RC-DE-02 — Basic Data Entry |

---

# 1. Overview

This article explains how to use bio-medical ontology fields during data entry in REDCap. Ontology fields are a special type of text input that connect to standardized medical terminology lookup tables hosted on an external server (BioPortal). Rather than typing a value directly, you search a controlled vocabulary and select a matching term. This ensures that clinical concepts like diagnoses, medications, and lab tests are recorded using standardized codes and descriptions. REDCap provides access to over 400 ontologies; the most common in clinical research are ICD-9/ICD-10, RxNorm, and LOINC.

---

# 2. Key Concepts & Definitions

**Bio-Medical Ontology**

A standardized, hierarchical vocabulary of terms used to describe concepts in a particular domain of medicine or biology. In REDCap, ontology fields connect to these vocabularies so that entries conform to recognized codes and descriptions rather than free text.

**BioPortal**

The third-party server that hosts the ontology databases REDCap queries. BioPortal is maintained by the National Center for Biomedical Ontology. REDCap sends search queries to BioPortal in real time when you type in an ontology field.

**Ontology Code**

A unique identifier assigned to each term within an ontology (e.g., `E11` for Type 2 diabetes mellitus in ICD-10). Most ontologies allow searching by either the code or the descriptive term.

**Controlled Vocabulary**

A fixed, curated set of terms. Ontology fields enforce controlled vocabulary — you must select from the lookup results rather than entering arbitrary free text.

---

# 3. How to Use an Ontology Field

Using an ontology field is similar to using a search engine. The field looks like a text box but behaves differently from a standard validated field.

**Step 1: Start typing.** Click the ontology field and begin typing either the descriptive name of the concept or its corresponding code. Results matching your entry will appear as a dropdown list below the field.

**Step 2: Review the results.** The dropdown shows terms from the configured ontology that match your search. Each result typically displays both the term's descriptive name and its code.

**Step 3: Select a match.** Click the result that best matches what you intend to record. The field is populated with the selected term. You cannot manually type a final value — the value must be selected from the lookup results.

> **Note:** If your search returns no results, try alternative spellings, broader terms, or the numeric code directly. If the ontology field is not returning results at all, this may indicate a connectivity issue with BioPortal — contact your project manager or REDCap support.

---

# 4. Common Ontologies in Clinical Research

### 4.1 ICD-9 / ICD-10 (International Classification of Diseases)

ICD-9 and ICD-10 are the standard vocabularies for recording diagnoses and health conditions. They allow you to record diagnoses at varying levels of specificity:

- Broad categories (e.g., "Diabetes mellitus, Type 2" — E11)
- Highly specific diagnoses (e.g., "Type 2 diabetes mellitus with diabetic chronic kidney disease, stage 3a" — E11.2211)

You can search by descriptive text or by the ICD code directly. ICD-10 is the current standard in most countries; ICD-9 remains available for historical or legacy data.

### 4.2 RxNorm

RxNorm is the standard vocabulary for medications. It provides normalized names for drugs and allows you to search by:

- Brand name (e.g., "Tylenol")
- Active ingredient / generic name (e.g., "acetaminophen")
- Medication with dosage (e.g., "acetaminophen 500 mg oral tablet")

> **Important:** RxNorm tracks what medication was prescribed or administered, not the actual dose given to a specific patient. If you need to record a specific administered dose, that information should be captured in a separate numeric field.

### 4.3 LOINC (Logical Observation Identifiers Names and Codes)

LOINC is the standard vocabulary for laboratory tests, clinical observations, and measurement panels. You can search for:

- Individual lab tests (e.g., "Creatinine [Mass/volume] in Serum or Plasma")
- Panels of related tests (e.g., "Creatinine kinase panel — Serum or Plasma")

> **Important:** LOINC identifies which lab test was performed — it does not record the result or the result value. The numeric result of a lab test should be recorded in a separate validated number field.

---

# 5. Common Questions

**Q: Can I type a free-text value into an ontology field instead of selecting from the lookup?**

**A:** No. Ontology fields require you to select a term from the lookup results. You cannot manually enter an arbitrary value. If no appropriate term exists in the ontology, contact your project manager — they may be able to add a free-text fallback field or select a different ontology.

**Q: The ontology field is not returning any results when I type. What should I do?**

**A:** First, try a different search term — a broader term, an alternate spelling, or the numeric code. If the field returns no results for any search, the issue is likely a connectivity problem with BioPortal. Contact your project manager or REDCap administrator.

**Q: Can I search ICD-10 by code instead of by the diagnosis name?**

**A:** Yes. Most ontologies, including ICD-10, RxNorm, and LOINC, support searching by code directly. Entering "E11" will return results related to Type 2 diabetes mellitus.

**Q: What is the difference between an ontology field and a standard validated text field?**

**A:** A standard validated text field checks that what you type matches a format (e.g., a date or a number). An ontology field replaces free typing entirely with a live search against an external controlled vocabulary — you select a pre-defined term rather than entering your own text.

**Q: The ontology lookup shows multiple very similar terms. How do I choose the right one?**

**A:** Select the term that most precisely matches the concept you are recording. For clinical data, prefer the most specific term that is supported by the source documentation. When in doubt, consult the protocol or a clinical team member — and use the field comment log (RC-DE-08) to document your reasoning.

---

# 6. Common Mistakes & Gotchas

**Treating ontology fields like free-text fields.** You cannot type a final value into an ontology field — you must select from the dropdown results. If you type a complete term and press Tab or Enter without selecting from the dropdown, the field may remain empty.

**Assuming RxNorm captures dose information.** RxNorm records what medication was ordered or administered, not the administered dose for a specific patient. Dose values must be captured in a separate numeric field in the instrument.

**Assuming LOINC captures lab result values.** LOINC identifies the test performed, not the result. Lab result values (e.g., a creatinine level of 1.2 mg/dL) must be recorded in a separate field.

**Not checking the connectivity to BioPortal before data entry sessions.** Ontology fields depend on a live connection to an external server. If BioPortal is unreachable, the fields will not function. Verify connectivity early in a data entry session, especially in environments with restricted internet access.

---

# 7. Related Articles

- RC-DE-05 — Field Validations (standard format-checking validations that accompany or complement ontology fields)
- RC-DE-02 — Basic Data Entry (foundational data entry skills)
- RC-DE-08 — Field Comment Log (how to document uncertainty when selecting an ontology term)

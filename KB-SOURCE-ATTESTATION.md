# KB Source Attestation

This document records the sources and contributors that informed the articles in this knowledge base. Articles were produced by converting or synthesizing source material into structured markdown using Claude. Most articles draw on more than one source type.

Every KB article's `Author` metadata field reads `See KB-SOURCE-ATTESTATION.md`. This file is the authoritative record of authorship and provenance for the entire KB.

---

## Contributors & Sources

### Bas de Veer — Original Training Materials

[Bas de Veer](https://www.linkedin.com/in/basdeveer), REDCap Manager, authored a set of training documents (`.docx` and `.pdf`) that served as primary source material for a large number of articles. These are original instructional materials written from hands-on REDCap experience. Most of these documents include a REDCap version number, which reflects the version of REDCap the training material was written against. The version applicable to each article can be found in the individual article's metadata header. Source files are stored in `original docx files/`.

Articles primarily derived from Bas de Veer's training materials include the Randomization series (RC-RAND-01 through RC-RAND-03), the Project Navigation UI series (RC-NAV-UI-01, RC-NAV-UI-02), and most articles in the Data Entry, Form Design, Export, Branching Logic, Record Navigation, Survey, Alert, Action Tag, Piping, and Import domains.

### Official REDCap Documentation

A significant portion of the KB was derived from REDCap's official online documentation, accessed as HTML pages from REDCap's built-in help system and public documentation site. Where a specific REDCap version is identifiable, it is noted in the individual article's metadata header (e.g., the AI Tools series references v15.5.3; FAQ-sourced content references v16.1.3).

### REDCap API Official Documentation

The API reference series (RC-API-01 through RC-API-54) was derived from REDCap's official API documentation. Articles in this series include a `Source` metadata field specifying the version. The main overview article (RC-API-01) covers general API concepts; individual method articles (RC-API-03 and above) each correspond to a single API endpoint.

### REDCap Control Center HTML Pages

The Control Center series (RC-CC-01 through RC-CC-21) and the Clinical Data Interoperability Services series (RC-CDIS-01 through RC-CDIS-04) were derived from Control Center pages captured as HTML from a REDCap v16.1.3 installation. The source was reviewed and sanitized to remove all institution-specific references, URLs, usernames, and server names before knowledge extraction.

The External Modules articles (RC-EM-01 and RC-EM-02) were also derived from the Control Center External Module Manager page (`ExternalModules/manager/control_center.php`). Module descriptions are reproduced from the module metadata as displayed in the Manager UI, authored by the respective module developers. The institution-specific IRB Validator module was excluded from the catalog.

### Training Collaboration Committee (TCC)

Several articles draw on source material from the [REDCap Training Collaboration Committee (TCC)](https://redcap.vumc.org/plugins/redcap_consortium/training_materials.php) repository. The TCC is a REDCap Consortium committee that periodically reviews training materials to ensure alignment with current REDCap standards, institutional policies, and best practices. Outdated or redundant resources are archived; new contributions are evaluated for clarity, accuracy, and usability.

Access to the TCC repository requires a REDCap Community account, which is typically reserved for REDCap administrators.

The following source documents from the TCC repository were used:

- **BCCH DM REDCap Mobile App** — authored by Sam Walkow and maintained by the BC Children's Hospital team. Primary source for RC-MOB-01 and portions of the MyCap series (RC-MYCAP-01 through RC-MYCAP-08).
- **Vanderbilt REDCap Mobile App Manual 1.1** — authored by Laura McLeod of Vanderbilt University. Primary source for RC-MOB-01 and portions of the MyCap series.
- **Multi-Language Management End Users' Guide (v15.5)** — contributed by REDCap administrative staff at [St. Elisabeth Gruppe GmbH – Klinikum der Ruhr-Universität Bochum](https://www.ruhr-uni-bochum.de). Primary source for RC-MLM-01.

### REDCap Built-in Help & FAQ

Detailed content throughout many KB articles was supplemented by mining REDCap's built-in Help & FAQ page. The FAQ is maintained by the REDCap FAQ Committee, whose role is to facilitate the transfer of knowledge from the REDCap Community into the Help & FAQ system for consumption by all REDCap end users. Because the FAQ is community-vetted and continuously maintained, it serves as a reliable source for edge-case clarifications, common misconceptions, and nuanced behavioral details that are not always covered in the main documentation.

### Claude — Synthesized Articles

A subset of articles was generated by Claude by reasoning across existing KB articles rather than from an external source document. These articles cover topics where the relevant information was already distributed across the KB (for example, the Branching Logic in Longitudinal Projects article synthesizes content from the Branching Logic and Longitudinal series).

---

## Notes

- Many articles reflect a combination of the above — for instance, a training outline by Bas de Veer used as the primary structure, supplemented with detail from official REDCap documentation.
- Article version numbers in individual KB articles (`Version: 1.0`, `1.1`, etc.) reflect the KB article revision, not the REDCap software version.
- The `Author` field in every article's metadata header reads `See KB-SOURCE-ATTESTATION.md` and points here. The previous value ("REDCap Support") was a placeholder and did not reflect the actual authorship.
- This attestation should be updated when new source types or contributors are introduced.

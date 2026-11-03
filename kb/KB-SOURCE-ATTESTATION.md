## KB Source Attestation

This document records the sources and contributors that informed the articles in this knowledge base. Articles were produced by converting or synthesizing source material into structured markdown using Claude. Most articles draw on more than one source type.

Every KB article's `Author` metadata field reads `See KB-SOURCE-ATTESTATION.md`. This file is the authoritative record of authorship and provenance for the entire KB.

---

### Contributors & Sources

#### Bas de Veer — Original Training Materials

[Bas de Veer](https://www.linkedin.com/in/basdeveer), REDCap Manager, authored a set of training documents (`.docx` and `.pdf`) that served as primary source material for a large number of articles. These are original instructional materials written from hands-on REDCap experience. Most of these documents include a REDCap version number, which reflects the version of REDCap the training material was written against. The original source documents are not kept in this repository.

Articles primarily derived from Bas de Veer's training materials include the Randomization series (RC-RAND-01 through RC-RAND-03), the Project Navigation UI series (RC-NAV-UI-01, RC-NAV-UI-02), and most articles in the Data Entry, Form Design, Export, Branching Logic, Record Navigation, Survey, Alert, Action Tag, Piping, and Import domains.

#### Bas de Veer — Direct Input and Project Analysis

Bas de Veer also shaped many articles directly, through explanations, corrections, and captures of REDCap pages provided while the articles were written. RC-INFRA-01 and RC-INFRA-02 document Bas de Veer's own self-hosted REDCap setup.

Some articles also include lessons learned from project analysis, in which Claude evaluated a REDCap project through the MCP server and the findings were added to the KB.

#### Official REDCap Documentation

A significant portion of the KB was derived from REDCap's official online documentation, accessed as HTML pages from REDCap's built-in help system and public documentation site. The MyCap series also draws on the public MyCap website (projectmycap.org). The versions used varied (e.g., v15.5.3 for the original AI Tools series and v16.1.3 for FAQ-sourced content). Articles have been revised since, so each article's `Requires` and `Verified Against` metadata rows show the REDCap versions that currently apply.

#### REDCap API Official Documentation

The API reference series (RC-API-01 through RC-API-56) was derived from REDCap's official API documentation. Articles in this series include a `Source` metadata field naming the documentation and, where recorded, its version. The main overview article (RC-API-01) covers general API concepts; individual method articles (RC-API-02 and above) each correspond to a single API endpoint.

#### REDCap Control Center HTML Pages

The Control Center series (RC-CC-01 through RC-CC-21) and the Clinical Data Interoperability Services series (RC-CDIS-01 through RC-CDIS-04) were derived from Control Center pages captured as HTML from a REDCap v16.1.3 installation. The source was reviewed and sanitized to remove all institution-specific references, URLs, usernames, and server names before knowledge extraction.

RC-CC-22 through RC-CC-25 were also written from Control Center HTML captures. Other later additions were written from captures of newer versions: RC-CC-26 from LTS 16.0.39 and 17.3.6, RC-CDIS-05 from LTS 17.3.6 and the 17.3.0 and 17.3.1 release notes, and part of RC-PLUS-02 from LTS 17.3.6.

The External Modules overview (RC-EM-01) was also derived from the Control Center External Module Manager page (`ExternalModules/manager/control_center.php`). The module catalogs (RC-EM-02 through RC-EM-04) are templates for each institution to complete and contain no module descriptions.

#### REDCap Change Logs

REDCap's Standard and LTS change logs were used to review the KB against new releases, including bug and security fixes. These reviews covered releases up to v17.4.1 Standard / v17.3.7 LTS, then v17.5.4 Standard / v17.3.18 LTS. Articles corrected or checked this way say so in their `Verified Against` metadata row, and the working notes are in `meta/`.

#### Live Verification

Some articles were checked against running REDCap instances and corrected where they differed: read-only on a test instance, or through the API on a sandbox project, on v17.5.6 Standard. Some version notes also come from a read-only comparison of the Control Center on v16.0.59 LTS with v17.5.6. These articles say what was checked in their `Verified Against` metadata row.

#### This Repository's Own Tooling

RC-MCP-01 documents the MCP server in this repository and was derived from its code (`MCP server/`).

#### Training Collaboration Committee (TCC)

Several articles draw on source material from the [REDCap Training Collaboration Committee (TCC)](https://redcap.vumc.org/plugins/redcap_consortium/training_materials.php) repository. The TCC is a REDCap Consortium committee that periodically reviews training materials to ensure alignment with current REDCap standards, institutional policies, and best practices. Outdated or redundant resources are archived; new contributions are evaluated for clarity, accuracy, and usability.

The repository's materials are shared for use by the REDCap community. Access to the TCC repository requires a REDCap Community account, which is typically reserved for REDCap administrators.

The following source documents from the TCC repository were used:

- **BCCH DM REDCap Mobile App** — authored by Sam Walkow and maintained by the BC Children's Hospital team. Primary source for RC-MOB-01 and portions of the MyCap series (RC-MYCAP-01 through RC-MYCAP-08).
- **Vanderbilt REDCap Mobile App Manual 1.1** — authored by Laura McLeod of Vanderbilt University. Primary source for RC-MOB-01 and portions of the MyCap series.
- **Multi-Language Management End Users' Guide (v15.5)** — contributed by REDCap administrative staff at [St. Elisabeth Gruppe GmbH – Klinikum der Ruhr-Universität Bochum](https://www.ruhr-uni-bochum.de). Primary source for RC-MLM-01.

#### REDCap Built-in Help & FAQ

Detailed content throughout many KB articles was supplemented by mining REDCap's built-in Help & FAQ page. The FAQ is maintained by the REDCap FAQ Committee, whose role is to facilitate the transfer of knowledge from the REDCap Community into the Help & FAQ system for consumption by all REDCap end users. Because the FAQ is community-vetted and continuously maintained, it serves as a reliable source for edge-case clarifications, common misconceptions, and nuanced behavioral details that are not always covered in the main documentation.

#### Claude — Synthesized Articles

A subset of articles was generated by Claude by reasoning across existing KB articles rather than from an external source document. These articles cover topics where the relevant information was already distributed across the KB (for example, the Branching Logic in Longitudinal Projects article synthesizes content from the Branching Logic and Longitudinal series).

---

### Notes

- Many articles reflect a combination of the above — for instance, a training outline by Bas de Veer used as the primary structure, supplemented with detail from official REDCap documentation.
- Article version numbers in individual KB articles (`Version: 1.0`, `1.1`, etc.) reflect the KB article revision, not the REDCap software version.
- The `Author` field in every article's metadata header reads `See KB-SOURCE-ATTESTATION.md` and points here. The previous value ("REDCap Support") was a placeholder and did not reflect the actual authorship.
- This attestation should be updated when new source types or contributors are introduced.

#### Example Files

`meta/examples/example_project_export.REDCap.xml` — a REDCap project XML export (CDISC ODM 1.3.1, FileType=Snapshot) used as a reference example for RC-IMP-02 §5 (ODM XML Format Reference). Exported 2026-05-13 from REDCap v16.0.25 by Bas de Veer. The project is a synthetic longitudinal clinical trial with two arms, repeating instruments, surveys, randomization, and one test record. All participant data fields contain placeholder values (Rock, Scissors, Paper, etc.) and contain no real personal information.

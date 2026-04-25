# REDCap KB RAG

A structured knowledge base of REDCap documentation articles, built for ingestion into a local Retrieval-Augmented Generation (RAG) system. Each article is written to be retrieved and interpreted by an LLM in response to user queries about REDCap features, workflows, and configuration.

## Purpose

This repo supports an LLM-powered REDCap assistant. Rather than feeding raw documentation into the model, each KB article covers a single, well-scoped concept and is formatted to maximize retrieval accuracy and response quality.

## How to Search This KB

**Step 1 — Find the right article:** Read `meta/KB-INDEX.md`. It is a compact table of every article by ID, title, and filename. Scan titles and domain prefixes to identify candidates, then read the article file(s) directly from `kb/`.

**Step 2 — Can't find it by title?** Read `meta/KB-KEYWORD-MAP.md`. It maps common user phrasings, synonyms, and ambiguous topics to the relevant domain or article ID. Use it when the question doesn't obviously map to a domain name (e.g. "prevent retaking" → RC-SURV, "prepopulate" → RC-PIPE).

**Step 3 — Need related articles?** Read `meta/KB-CROSS-REFS.md` to find prerequisites and follow-on articles for a given ID. This file is large — only load it when you need dependency or cross-reference information, not for simple lookups.

**Domain routing:** Articles are grouped by domain prefix (e.g. `RC-SURV` for surveys, `RC-BL` for branching logic). The domain table below maps prefixes to topic areas. See the **Disambiguation Notes** section below the table for topics that could belong to more than one domain.

## Repo Structure

```
REDCap_KB_RAG/
├── kb/                               # Markdown KB articles (RAG-ready) — 216 articles
│   └── RC-[DOMAIN]-[NN]_...               # Individual KB articles (216 articles)
├── meta/                             # Navigation & cross-reference metadata (not for RAG indexing)
│   ├── KB-INDEX.md                        # Article index: ID → Title → Filename (load for topic lookup)
│   ├── KB-KEYWORD-MAP.md                  # Keyword/synonym map: user phrasings → domain or article ID
│   └── KB-CROSS-REFS.md                   # Per-article prerequisites, outbound/inbound links, changelog (load only when building/updating articles)
├── claude skills/
│   ├── kb-creation/                       # Skill: build new KB articles from .docx outlines
│   ├── kb-update/                         # Skill: update or correct existing KB articles
│   ├── kb-update-workspace/               # Skill: update articles using workspace-mounted files
│   ├── kb-search/                         # Skill: search and retrieve KB articles by topic
│   ├── redcap-codebook-reader/            # Skill: summarize a project from a Codebook PDF or DD CSV
│   ├── redcap-data-dictionary/            # Skill: analyze REDCap Data Dictionary CSV files
│   ├── redcap-dd-builder/                 # Skill: build a new Data Dictionary from scratch
│   ├── redcap-dd-fixer/                   # Skill: fix errors in an uploaded Data Dictionary
│   ├── redcap-longitudinal-builder/       # Skill: build longitudinal project CSVs (Arms, Events, Designations)
│   ├── redcap-longitudinal-structure/     # Skill: parse longitudinal structure from exported CSVs
│   ├── redcap-project-analyzer/           # Skill: audit a live REDCap project via API for design issues
│   ├── redcap-syntax-builder/             # Skill: write REDCap expressions from a description
│   ├── redcap-syntax-builder-workspace/   # Skill: syntax-builder variant for workspace-mounted files
│   ├── redcap-syntax-fixer/               # Skill: diagnose and fix broken REDCap expressions
│   ├── redcap-syntax-fixer-workspace/     # Skill: syntax-fixer variant for workspace-mounted files
│   └── redcap-syntax-reader/              # Skill: explain and interpret REDCap expressions
├── MCP server/                       # Python MCP server exposing REDCap API methods as Claude tools
│   ├── redcap_mcp_server.py               # Server implementation (all major API endpoints)
│   └── install.sh                         # Setup script (installs mcp[cli] + registers named instances)
├── ServiceNow ETL/                   # Tooling to export KB articles into ServiceNow knowledge base
│   ├── kb_to_servicenow.py                # Converts kb/ markdown to a 3-sheet Excel workbook
│   ├── REDCap_KB_ServiceNow_Import.xlsx   # Most-recent export (Articles, Relationships, Import Instructions)
│   └── ServiceNow_Admin_Handoff.md        # Field-by-field import guide for ServiceNow admins
├── visualization/
│   └── kb_dependency_graph.html           # Interactive graph of inter-article dependencies
├── KB-GAPS-TODO.md                   # Tracked knowledge gaps and planned articles
├── KB-SOURCE-ATTESTATION.md          # Source document provenance for KB articles
├── PROJECT-TODO.md                   # Running dev task list for the KB/RAG project (non-article work)
├── STYLE-GUIDE.md                    # Design conventions for building REDCap projects (alignment, longitudinal setup, etc.)
└── README.md
```

## Article Naming Convention

Articles follow a consistent naming pattern:

```
RC-[DOMAIN]-[NN]_Title-With-Hyphens.md
```

| Domain prefix | Topic area |
|---|---|
| `RC-AI` | AI Tools (writing, translation, summarization) |
| `RC-ALERT` | Alerts & Notifications |
| `RC-API` | REDCap API (export, import, delete operations) |
| `RC-AT` | Action Tags |
| `RC-AT-EM` | Action Tags — External Module extensions |
| `RC-BL` | Branching Logic |
| `RC-CALC` | Calculations & Special Functions |
| `RC-CC` | Control Center (admin configuration & system management) |
| `RC-CDIS` | Clinical Data Interoperability Services (FHIR/HL7 integrations) |
| `RC-DAG` | Data Access Groups |
| `RC-DDE` | Double Data Entry |
| `RC-DDP` | Dynamic Data Pull |
| `RC-DE` | Data Entry |
| `RC-DQ` | Data Quality Module |
| `RC-EM` | External Modules |
| `RC-EXPRT` | Data Export & Custom Reports |
| `RC-FD` | Form Design |
| `RC-FDL` | Form Display Logic |
| `RC-IMP` | Data Import |
| `RC-INST` | Institution-Specific Settings & Policies |
| `RC-INTG` | Integrations (Data Entry Trigger, etc.) |
| `RC-LONG` | Longitudinal Project Setup |
| `RC-MCP` | REDCap MCP Server (setup & management) |
| `RC-MLM` | Multi-Language Management |
| `RC-MOB` | REDCap Mobile App |
| `RC-MSG` | REDCap Messenger |
| `RC-MYCAP` | MyCap (mobile data collection) |
| `RC-NAV-REC` | Record Navigation |
| `RC-NAV-UI` | Project Navigation UI |
| `RC-PIPE` | Piping & Smart Variables |
| `RC-PROF` | My Profile (user profile settings) |
| `RC-PROJ` | Project Lifecycle & Status |
| `RC-RAND` | Randomization |
| `RC-SENDIT` | Send-It (secure file transfer) |
| `RC-SURV` | Surveys |
| `RC-TXT` | Texting (SMS) |
| `RC-USER` | User Rights |

Article navigation is in `meta/KB-INDEX.md` (topic lookup) and `meta/KB-CROSS-REFS.md` (per-article prerequisites and cross-references).

## Disambiguation Notes

Some topics could map to more than one domain. Use these rules to pick the right one:

| Question type | Go to |
|---|---|
| Sending automated emails or SMS | RC-ALERT (triggered notifications) vs RC-SURV-06 (survey invitations — pick based on whether it's survey-related) |
| Hiding or showing fields | RC-BL (branching logic — field appears/disappears based on logic) vs RC-AT-02 (@HIDDEN/@READONLY — static or action-tag-driven) vs RC-FDL (form display logic — hides entire forms, not individual fields) |
| Exporting data | RC-EXPRT (UI-based reports and exports) vs RC-API (programmatic export via API) |
| Importing data | RC-IMP (CSV upload via UI) vs RC-API (programmatic import via API) |
| File uploads | RC-FD (file-upload field type in an instrument) vs RC-API-12–15 (API methods for record-level files) vs RC-API-45–49 (API methods for File Repository) |
| Calculations / formulas | RC-CALC (calculated fields, special functions) vs RC-AT-09 (@CALCTEXT / @CALCDATE action tags) |
| Translations / multilingual | RC-MLM (Multi-Language Management — UI and instrument translation) vs RC-AI-03 (AI translation tool) |
| Mobile data collection | RC-MOB (REDCap Mobile App — staff-facing offline data entry) vs RC-MYCAP (MyCap — participant-facing mobile app) |
| Prepopulating fields | RC-PIPE (piping and smart variables) vs RC-AT-06 (autofill action tags) |
| Survey access / links | RC-SURV (survey setup and settings) vs RC-PIPE (smart variable survey links) |

## Article Format

Each article is written for RAG retrieval using an 8-section template:

1. **Overview** — what the feature is and when it applies
2. **Key concepts** — definitions and terminology
3. **Step-by-step workflow** — how to use the feature
4. **Q&A pairs** — anticipated user questions with direct answers
5. **Edge cases** — common pitfalls and exceptions
6. **Related articles** — cross-references to prerequisite or follow-on topics
7. **Prerequisites** — what the user needs to know first
8. **Summary** — brief recap for retrieval context

Articles are institution-agnostic in their core content so they can be reused across REDCap environments.

## Claude Skills

The `claude skills/` directory contains Cowork skills that Claude uses to maintain the KB and assist with REDCap work:

| Skill | Purpose |
|---|---|
| `kb-creation` | Convert a `.docx` training outline into a new KB article |
| `kb-update` | Update or correct an existing article based on new information |
| `kb-update-workspace` | Same as kb-update, but works with files already in the mounted workspace folder |
| `kb-search` | Search the KB by topic to find and read relevant articles before writing |
| `redcap-codebook-reader` | Read a Codebook PDF or Data Dictionary CSV and produce a structured project overview |
| `redcap-data-dictionary` | Analyze a REDCap Data Dictionary CSV (field types, instruments, structure) |
| `redcap-dd-builder` | Build a new REDCap Data Dictionary from scratch based on a project description |
| `redcap-dd-fixer` | Diagnose and fix errors in an uploaded Data Dictionary CSV |
| `redcap-longitudinal-builder` | Build Arms, Events, and Instrument Designations CSVs for a longitudinal project |
| `redcap-longitudinal-structure` | Parse and interpret longitudinal project structure from exported Arms/Events/Designations CSVs |
| `redcap-project-analyzer` | Connect to the REDCap API and audit a live project for design issues, logic errors, and structural problems |
| `redcap-syntax-builder` | Write a correct REDCap expression (branching logic, calc field, action tag) from a description |
| `redcap-syntax-builder-workspace` | Same as redcap-syntax-builder, but works with fields from a workspace-mounted Data Dictionary |
| `redcap-syntax-fixer` | Diagnose and fix broken REDCap expressions |
| `redcap-syntax-fixer-workspace` | Same as redcap-syntax-fixer, but resolves field references against a workspace-mounted Data Dictionary |
| `redcap-syntax-reader` | Explain and interpret what an existing REDCap expression does |

## Adding New Articles

New articles are built from source training outline documents or written from scratch using a Claude skill. The workflow is:

1. Open a Cowork session and upload the source `.docx` (or describe the topic)
2. Claude uses the `kb-creation` skill to produce a properly formatted KB article
3. The article is saved to `kb/` and `meta/KB-INDEX.md` and `meta/KB-CROSS-REFS.md` are updated

## Updating Existing Articles

To revise or correct an article, open a Cowork session and either upload updated source material or describe the change. Claude uses the `kb-update` or `kb-update-workspace` skill to locate the relevant article, apply the edits, and keep `meta/KB-INDEX.md` and `meta/KB-CROSS-REFS.md` in sync.

## Disclaimer

This repository contains original documentation and guidance written by the maintainer based on experience working with REDCap. It is **not affiliated with, endorsed by, or approved by Vanderbilt University** or the REDCap Consortium. REDCap® is a trademark of Vanderbilt University.

No REDCap software is distributed in this repository. All content reflects the maintainer's own explanations, workflows, and best practices — not reproductions of official REDCap documentation or training materials.

For official REDCap resources, visit [project-redcap.org](https://projectredcap.org) or the REDCap Community forum.

## Syncing Changes

Changes are committed locally by Claude and pushed to GitHub manually:

```bash
git add -A
git commit -m "your message"
git push
```

# REDCap KB RAG

A structured knowledge base of REDCap documentation articles, built for ingestion into a local Retrieval-Augmented Generation (RAG) system. Each article is written to be retrieved and interpreted by an LLM in response to user queries about REDCap features, workflows, and configuration.

## Purpose

This repo supports an LLM-powered REDCap assistant at Yale. Rather than feeding raw documentation into the model, each KB article covers a single, well-scoped concept and is formatted to maximize retrieval accuracy and response quality.

## Repo Structure

```
REDCap_KB_RAG/
├── kb/                               # Markdown KB articles (RAG-ready) — 101 articles
│   ├── KB-REFERENCE-MAP.md           # Cross-reference index of all articles
│   └── RC-[DOMAIN]-[NN]_...          # Individual KB articles
├── claude skills/
│   ├── kb-creation/                  # Skill: build new KB articles from .docx outlines
│   ├── kb-update/                    # Skill: update or correct existing KB articles
│   ├── kb-update-workspace/          # Skill: update articles using workspace-mounted files
│   ├── kb-search/                    # Skill: search and retrieve KB articles by topic
│   ├── redcap-data-dictionary/       # Skill: analyze REDCap Data Dictionary CSV files
│   ├── redcap-dd-builder/            # Skill: build a new Data Dictionary from scratch
│   ├── redcap-dd-fixer/              # Skill: fix errors in an uploaded Data Dictionary
│   ├── redcap-syntax-builder/        # Skill: write REDCap expressions from a description
│   ├── redcap-syntax-fixer/          # Skill: diagnose and fix broken REDCap expressions
│   └── redcap-syntax-reader/         # Skill: explain and interpret REDCap expressions
├── original docx files/              # Source Word training outlines
└── sync.sh                           # Helper script to commit and push changes
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
| `RC-AT` | Action Tags |
| `RC-AT-EM` | Action Tags — External Module extensions |
| `RC-BL` | Branching Logic |
| `RC-CALC` | Calculations & Special Functions |
| `RC-DAG` | Data Access Groups |
| `RC-DE` | Data Entry |
| `RC-EXPRT` | Data Export & Custom Reports |
| `RC-FD` | Form Design |
| `RC-IMP` | Data Import |
| `RC-INST` | Institution-Specific Settings & Policies |
| `RC-LONG` | Longitudinal Project Setup |
| `RC-MLM` | Multi-Language Management |
| `RC-NAV-REC` | Record Navigation |
| `RC-NAV-UI` | Project Navigation UI |
| `RC-PIPE` | Piping & Smart Variables |
| `RC-RAND` | Randomization |
| `RC-SURV` | Surveys |
| `RC-TXT` | Texting (SMS) |
| `RC-UNCLASSIFIED` | Interim holding area for topics not yet in a dedicated article |
| `RC-USER` | User Rights |

The `KB-REFERENCE-MAP.md` file lists all articles, their prerequisites, cross-references, and flags topics that are referenced but not yet written.

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

Articles are institution-agnostic in their core content so they can be reused across REDCap environments, though they are primarily maintained for Yale's deployment.

## Claude Skills

The `claude skills/` directory contains Cowork skills that Claude uses to maintain the KB:

| Skill | Purpose |
|---|---|
| `kb-creation` | Convert a `.docx` training outline into a new KB article |
| `kb-update` | Update or correct an existing article based on new information |
| `kb-update-workspace` | Same as kb-update, but works with files already in the mounted workspace folder |
| `kb-search` | Search the KB by topic to find and read relevant articles before writing |
| `redcap-data-dictionary` | Analyze a REDCap Data Dictionary CSV (field types, instruments, structure) |
| `redcap-dd-builder` | Build a new REDCap Data Dictionary from scratch based on a project description |
| `redcap-dd-fixer` | Diagnose and fix errors in an uploaded Data Dictionary CSV |
| `redcap-syntax-builder` | Write a correct REDCap expression (branching logic, calc field, action tag) from a description |
| `redcap-syntax-fixer` | Diagnose and fix broken REDCap expressions |
| `redcap-syntax-reader` | Explain and interpret what an existing REDCap expression does |

## Adding New Articles

New articles are built from source training outline documents (Word `.docx` files) using a Claude skill. The workflow is:

1. Place the source outline in `original docx files/`
2. Open a Cowork session and upload the `.docx`
3. Claude uses the `kb-creation` skill to convert it into a properly formatted KB article
4. The article is saved to `kb/` and `KB-REFERENCE-MAP.md` is updated

## Updating Existing Articles

To revise or correct an article, open a Cowork session and either upload the updated source material or describe the change. Claude uses the `kb-update` or `kb-update-workspace` skill to locate the relevant article, apply the edits, and keep `KB-REFERENCE-MAP.md` in sync.

## Syncing Changes

The `sync.sh` script commits all pending changes and pushes them to GitHub:

```bash
./sync.sh "optional commit message"
```

If no message is provided, it defaults to `Claude: update repo`.

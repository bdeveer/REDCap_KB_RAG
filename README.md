# REDCap KB RAG

A structured knowledge base of REDCap documentation articles, built for ingestion into a local Retrieval-Augmented Generation (RAG) system. Each article is written to be retrieved and interpreted by an LLM in response to user queries about REDCap features, workflows, and configuration.

## Purpose

This repo supports an LLM-powered REDCap assistant at Yale. Rather than feeding raw documentation into the model, each KB article covers a single, well-scoped concept and is formatted to maximize retrieval accuracy and response quality.

## Repo Structure

```
REDCap_KB_RAG/
├── kb/                        # Markdown KB articles (RAG-ready)
│   ├── KB-REFERENCE-MAP.md    # Cross-reference index of all articles
│   └── RC-[DOMAIN]-[NN]_...   # Individual KB articles
├── claude skills/
│   └── kb-creation/           # Claude skill for building new KB articles
│       └── SKILL.md
├── original docx files/       # Source Word training outlines
└── sync.sh                    # Helper script to commit and push changes
```

## Article Naming Convention

Articles follow a consistent naming pattern:

```
RC-[DOMAIN]-[NN]_Title-With-Hyphens.md
```

| Domain prefix | Topic area |
|---|---|
| `RC-ALERT` | Alerts & Notifications |
| `RC-BL` | Branching Logic |
| `RC-DAG` | Data Access Groups |
| `RC-DE` | Data Entry |
| `RC-EXPRT` | Data Export |
| `RC-FD` | Form Design |
| `RC-IMP` | Data Import |
| `RC-LONG` | Longitudinal Project Setup |
| `RC-NAV-REC` | Record Navigation |
| `RC-NAV-UI` | Project Navigation UI |
| `RC-PIPE` | Piping & Smart Variables |
| `RC-RAND` | Randomization |
| `RC-SURV` | Surveys |
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

## Adding New Articles

New articles are built from source training outline documents (Word `.docx` files) using a Claude skill. The workflow is:

1. Place the source outline in `original docx files/`
2. Open a Cowork session and upload the `.docx`
3. Claude uses the `kb-creation` skill to convert it into a properly formatted KB article
4. The article is saved to `kb/` and `KB-REFERENCE-MAP.md` is updated

## Syncing Changes

The `sync.sh` script commits all pending changes and pushes them to GitHub:

```bash
./sync.sh "optional commit message"
```

If no message is provided, it defaults to `Claude: update repo`.

---
name: redcap-kb-builder
description: Use this skill when the user wants to convert a REDCap training outline (uploaded as a Word document) into a RAG-optimized Knowledge Base article in the RC-KB format. Triggers include: uploading a training outline .docx, asking to "convert this outline", "build a KB article", "turn this into a KB article", or any request to produce a new RC-[DOMAIN]-[NN] article from source material. Also trigger when the user says things like "let's do the next outline" or "here's the next one". Do NOT trigger for editing or refining existing articles — use the redcap-kb-refiner skill for that.
---

# REDCap KB Article Builder

This skill converts a raw REDCap training outline (Word document) into a single, RAG-optimized Knowledge Base article following the RC-KB standard format.

## What you're producing

A `.docx` KB article that:
- Covers exactly one concept or workflow (one retrieval query pattern)
- Follows the 8-section template (see below)
- Is optimized for LLM retrieval — explicit Q&A pairs, consistent terminology, surfaced edge cases
- Is institution-agnostic in its core content
- Is ready for RAG ingestion into Yale's local LLM

Always use the docx skill to produce the output file. Read `/mnt/skills/public/docx/SKILL.md` before writing any code.

---

## Step 1: Read and analyze the outline

When the user uploads a Word document:

1. Read the uploaded `.docx` from `/mnt/user-data/uploads/`
2. Identify all chapters or sections in the outline
3. Assess whether the outline maps to one article or multiple — see **Scope decisions** below
4. Present your assessment to the user before proceeding: list the proposed article(s), their proposed IDs, and your rationale. Wait for confirmation.

### Scope decisions

**Merge into one article** when chapters cover a single retrieval query pattern — a user asking one question would need all of them. Example: "What is branching logic?" and "Where is branching logic configured?" belong together.

**Split into separate articles** when chapters cover fundamentally different retrieval patterns — a user asking about topic A would never need topic B in the same lookup. Each gets its own article ID.

When in doubt, ask rather than decide unilaterally.

---

## Step 2: Determine the Article ID

Article IDs follow this format:
```
RC-[DOMAIN]-[NN]
RC-[DOMAIN]-[SUBDOMAIN]-[NN]
```

Rules:
- `RC` prefix always
- DOMAIN: uppercase, max 5 characters (e.g., NAV, RAND, DAG, BL, FD, DE)
- Subdomain: optional, uppercase, max 3 characters — use when a domain has two or more clearly distinct article groups
- Two-digit zero-padded numbers (01, 02, 03...)
- Subdomain numbers restart at 01 under each parent
- **IDs are permanent once assigned** — confirm with the user before finalizing

Check the existing corpus (project files) to determine the next available number in the relevant domain. If the domain is new, flag it and confirm the slug with the user before proceeding.

Filename format:
```
RC-[DOMAIN]-[NN]_[Descriptive-Title-In-Title-Case].docx
```

---

## Step 3: Write the article

Produce the article using the 8-section structure below. Use the BL series (RC-BL-01 through RC-BL-04) as the canonical style reference — these are the most recent articles in the corpus.

### 8-Section Template

#### Metadata table (top of document, before Section 1)

| Field | Value |
|---|---|
| Article ID | RC-[DOMAIN]-[NN] |
| Domain | [Full domain name, e.g. Branching Logic] |
| Applies To | [Project types / conditions] |
| Prerequisite | [Article ID — Title, or "None"] |
| Version | 1.0 |
| Last Updated | [Year] |
| Author | REDCap Support |
| Related Topics | [RC-XX-NN — Title; RC-XX-NN — Title] |

#### Section 1: Overview
One paragraph. Plain-language description of what this article covers. Write as if explaining to someone who has never opened REDCap. No jargon without definition. State what series this article belongs to if applicable.

#### Section 2: Key Concepts & Definitions
Define every term used in the article as REDCap uses it. Note cases where REDCap's terminology differs from common usage. Each definition is a subsection header (H2) with a paragraph below it.

#### Section 3: [Topic-specific procedural content]
Step-by-step procedures, reference tables, or structured explanations. Use subsections (3.1, 3.2...) for distinct sub-tasks or phases. This section's title should reflect the content — not always "Step-by-Step Procedure."

#### Section 4–6: [Additional procedural or reference content as needed]
Add sections for distinct phases, feature areas, or reference tables. Not every article needs 8 content sections — combine or omit as appropriate. Always maintain the Q&A and Gotchas sections.

#### Section N-1: Common Questions
At least 5 Q&A pairs. Write questions exactly as a real user would ask them — this format directly improves LLM retrieval accuracy. Answers must be direct and complete. Avoid "it depends" without explaining what it depends on.

#### Section N: Common Mistakes & Gotchas
At least 3 entries. Each entry covers: what the user does wrong, what happens as a result, and how to prevent or recover. Use a bold lead phrase for each entry.

#### Final section: Related Articles
Bullet list of related KB articles with ID and title. Include prerequisites, natural next articles, and adjacent topics.

---

## Style rules (derived from BL series)

- **Terminology**: Use REDCap's canonical terms. "Instrument" not "form" or "survey" unless distinguishing. "Variable" not "field" unless quoting the UI.
- **Voice**: Direct, instructional. No filler phrases ("It's important to note that...").
- **Tables**: Use for reference content with 3+ rows. Don't use tables for 2-item comparisons — prose is cleaner.
- **Notes and warnings**: Use bordered table cells for Important/Critical/Note callouts, consistent with the BL series style.
- **Cross-references**: Always include both the article ID and title: `RC-BL-02 — Syntax & Atomic Statements`
- **One concept per article**: If you find yourself writing "this article also covers...", that's a signal to split.

---

## RAG optimization checklist

Before finalizing, verify:
- [ ] Article covers exactly one retrieval query pattern
- [ ] Q&A pairs use natural language a user would actually type
- [ ] All REDCap-specific terms are defined in Section 2
- [ ] Edge cases and gotchas are explicitly surfaced (not buried)
- [ ] Cross-references use full ID + title format
- [ ] Terminology is consistent throughout (no synonym drift)
- [ ] No institution-specific content in the core sections (see below)

---

## Institutional policy section

If the article touches on behavior that varies by institution (e.g., Production mode approval workflows, administrator intervention policies, local support contacts), add a clearly marked callout box at the relevant point:

```
| Yale-specific: [Describe what varies and what Yale's policy is — 
| leave blank until confirmed with Yale REDCap support team] |
```

This placeholder signals to future editors where local policy needs to be inserted without contaminating the institution-agnostic core content.

---

## Output

1. Generate the `.docx` file using the docx skill
2. Save to `/mnt/user-data/outputs/`
3. Use `present_files` to share it
4. Summarize in 2–3 sentences: article ID, title, section count, and any scope decisions made

Do not explain the entire article back to the user — they can read the document.

---

## Reference: Established domain slugs

| Slug | Domain | Notes |
|---|---|---|
| NAV | Navigation | Subdomains: UI, REC |
| RAND | Randomization | — |
| FD | Form Design | — |
| DE | Data Entry | — |
| BL | Branching Logic | — |
| DAG | Data Access Groups | — |
| MLM | Multi-Language Management | — |
| USER | User Rights | — |
| AT | Action Tags | — |
| EXPRT | Exports, Reports & Stats | — |
| SURV | Surveys | — |
| API | API | — |
| MOB | Mobile | — |

Slugs `RIGHTS` and `ALERT` appear in existing cross-references but exceed the 5-character limit — flag for review before creating articles in those domains.

---
name: kb-search
description: >
  Search the REDCap knowledge base (kb/ in the REDCap_KB_RAG repo) to find and read relevant articles for a topic or question. Use this skill when you need to look something up in the REDCap KB, answer a question about how a REDCap feature works, find articles before writing or updating KB content, or check what the KB already says about a topic. Trigger on phrases like "what does the KB say about", "look up in the KB", "find articles about", "search the knowledgebase", "is there a KB article on", or when another skill needs related REDCap documentation before doing its work. Do NOT use it as a substitute for the task-specific skills: writing, fixing or explaining an expression (redcap-syntax), building, fixing or reading a data dictionary (redcap-dd-*, redcap-data-dictionary), longitudinal CSVs (redcap-longitudinal-*), or auditing a live project (redcap-project-analyzer). Those skills can call this one for background.
---

# REDCap KB Search

Use this skill to find and read the right articles from the REDCap knowledge base — a collection of markdown articles in `kb/` inside the REDCap_KB_RAG repo.

## Locating the KB

The KB lives at `C:\Users\bd593\Documents\RCRAG\REDCap_KB_RAG\kb\`. Search only `kb\`, never `kb (YAML)\`, which holds generated duplicates of the same articles. If the folder is not accessible, request access to `C:\Users\bd593\Documents\RCRAG\REDCap_KB_RAG` for this session.

Navigation files live in `C:\Users\bd593\Documents\RCRAG\REDCap_KB_RAG\meta\`:

| File | Use it for |
|---|---|
| `meta/KB-INDEX.md` | Every article: ID → title → filename. Always start here. |
| `meta/KB-KEYWORD-MAP.md` | User phrasings and synonyms → domain or article ID. Use when the topic doesn't obviously match a domain. |
| `meta/KB-CROSS-REFS.md` | Per-article prerequisites and inbound/outbound links. Load only when you need to trace dependencies. |

`kb/KB-REFERENCE-MAP.md` is an obsolete stub that points to these three files — don't use it.

## Article naming convention

Files follow the pattern `RC-{DOMAIN}-{NN}_{Title}.md`. There are 40+ domain codes (API, AT, BL, CALC, CC, DE, FD, IMP, LONG, MYCAP, PIPE, SURV, USER, …); `meta/KB-INDEX.md` is the authoritative list — don't rely on memory for which domains or article numbers exist.

Lower `NN` numbers are foundational (e.g., `RC-BL-01` is the overview; higher numbers are more specific). Start with low numbers unless the question is clearly about something specific.

**External Modules:** content about External Modules uses a `{DOMAIN}-EM` subdomain instead of continuing the sequential numbering — e.g. `RC-AT-EM-01` covers the HIDESUBMIT action tag module. When searching a domain, check both `RC-{DOMAIN}-*` and `RC-{DOMAIN}-EM-*`.

**Instance-specific articles:** `RC-INST-01/02/03` (institution settings and policies) and `RC-EM-02/03/04` (installed module catalogs) exist in production, test and development variants. Make sure you read the one for the instance the user is asking about.

## Search process

### Step 1 — Understand the topic

Before searching, identify: What REDCap feature or concept is this about? Which domain(s) does it touch? Are there secondary concepts involved (e.g., a question about branching logic on checkboxes touches both BL and FD)?

### Step 2 — Find candidate articles

1. Read `meta/KB-INDEX.md` and pick candidates by ID and title.
2. If nothing obvious matches, check `meta/KB-KEYWORD-MAP.md` for the user's phrasing.
3. Still unsure? Grep the **Synonyms** row of the articles — every article has one listing alternative search phrasings:
   `Grep pattern="<phrase>" path="C:\Users\bd593\Documents\RCRAG\REDCap_KB_RAG\kb" glob="RC-*.md" -i`

### Step 3 — Select articles to read

Pick up to 3 articles that best cover the topic. Guidance:
- For a broad question, read the domain overview first (`NN=01`) before specifics
- For a narrow question, go directly to the specific article
- If an article lists a **Prerequisite** in its header table, read that first if context is needed
- Prefer depth over breadth: 2 well-chosen articles beat 4 loosely related ones

### Step 4 — Read the articles

Read each selected article in full using the Read tool. Check the **Verified Against** row in the header table — it tells you which REDCap version the content was checked against, and version caveats in the body matter.

### Step 5 — Return findings

Summarize what you found and cite the source articles by their ID and title (e.g., `RC-BL-02 — Branching Logic: Syntax & Atomic Statements`). If called from another skill, make the full article content available for that skill's next steps.

If no relevant article exists, say so clearly — don't guess or fill in from general REDCap knowledge when the KB should be the authority. If the gap looks worth filling, mention it so it can be added to `KB-GAPS-TODO.md` (repo root).

## Example — broad question

**Query:** "How does branching logic work?"

1. Domain: BL. `meta/KB-INDEX.md` lists RC-BL-01 to RC-BL-05.
2. Start with `RC-BL-01` (overview); its Related Topics point to RC-BL-02 for syntax.
3. Read RC-BL-01 and RC-BL-02.
4. Return: summary of scope + syntax, citing both articles.

## Example — narrow / cross-domain question

**Query:** "How do I use branching logic on a checkbox field?"

1. Domain: BL, but also touches FD (field types).
2. The index title for RC-BL-04 is "Structured Fields & Checkboxes".
3. Read RC-BL-04 (and its prerequisite RC-BL-02 if context is needed).
4. Return: specific answer from RC-BL-04, citing it.

## Called from another skill

When another skill (e.g., kb-creation) asks you to find related articles before writing new content, follow this same process and return both the article IDs and their full markdown content so the calling skill can use them for context and cross-referencing.

---
name: kb-search
description: >
  Search the REDCap knowledge base (kb/ in the REDCap_KB_RAG repo) to find and read relevant articles for any topic or question. Use this skill whenever you need to look something up in the REDCap KB, answer a question about REDCap functionality, find articles before writing new KB content, or check what the KB already says about a topic. Trigger on phrases like "what does the KB say about", "look up in the KB", "find articles about", "search the knowledgebase", "is there a KB article on", or any time another skill needs to pull in related REDCap documentation before doing its work. When in doubt, use this skill — it's the authoritative source for REDCap knowledge.
---

# REDCap KB Search

Use this skill to find and read the right articles from the REDCap knowledge base — a collection of markdown articles in `kb/` inside the REDCap_KB_RAG repo.

## Locating the KB

The KB lives at `kb/` inside the `REDCap_KB_RAG` repo. In Cowork sessions it's typically mounted at a path like `/sessions/<id>/mnt/REDCap_KB_RAG/kb/`. If you're unsure of the exact path, use Glob with pattern `**/REDCap_KB_RAG/kb/*.md` or list the mnt/ directory to find it.

## Article naming convention

Files follow the pattern `RC-{DOMAIN}-{NN}_{Title}.md`. Current domains:

| Code | Topic |
|------|-------|
| AI | AI tools |
| ALERT | Alerts & notifications |
| AT | Action tags (standard: RC-AT-01 through RC-AT-11) |
| AT-EM | Action tags (external modules: RC-AT-EM-01, RC-AT-EM-02, etc.) |
| BL | Branching logic |
| DAG | Data Access Groups |
| DE | Data entry |
| EXPRT | Data export & reports |
| FD | Form design & data dictionary |
| IMP | Data import |
| LONG | Longitudinal project setup |
| NAV | Navigation (UI and record navigation) |
| PIPE | Piping & smart variables |
| RAND | Randomization |
| SURV | Surveys |
| USER | User rights |
| UNCLASSIFIED | Holding article for orphaned FAQ topics (see note below) |

Lower `NN` numbers are foundational (e.g., `RC-BL-01` is the overview; `RC-BL-03` is advanced syntax). Start with low numbers unless the question is clearly about something specific.

**⚠️ Holding Article Note:** `RC-UNCLASSIFIED-01_FAQ-v16-Orphaned-Topics.md` contains interim coverage for topics pending dedicated articles. When searching for Project Lifecycle, Production Changes, Data Quality Module, API & Data Entry Trigger, Multi-Language Management (MLM), or MyCap, **check this article** even if a dedicated article exists but is marked ⚠️ (not yet written). The REFERENCE-MAP will flag these gaps with pointers to this holding article.

**Special case — External Modules:** For content from External Modules (third-party plugins), use the subdomain convention `{DOMAIN}-EM` instead of continuing the sequential numbering within that domain. For example:
   - `RC-AT-EM-01` covers the HIDESUBMIT action tag module
   - `RC-BL-EM-01` would cover a branching logic external module
   - `RC-SURV-EM-01` would cover a survey-related external module

This convention reserves the standard sequential numbering (e.g., `RC-AT-01` through `RC-AT-11`, `RC-BL-01` through `RC-BL-04`) for core/standard REDCap features and creates a clear organizational boundary for module-specific content. When searching for articles in any domain, check both the standard `RC-{DOMAIN}-*` series and the `RC-{DOMAIN}-EM-*` subdomain for external module content.

## Search process

### Step 1 — Understand the topic

Before searching, identify: What REDCap feature or concept is this about? Which domain(s) does it touch? Are there secondary concepts involved (e.g., a question about branching logic on checkboxes touches both BL and FD)?

### Step 2 — Consult KB-REFERENCE-MAP.md

Read `kb/KB-REFERENCE-MAP.md`. It contains:
- **Article Index** — a table of all articles with IDs, titles, and filenames
- **Per-Article Reference Details** — prerequisites, outbound links, and inbound links for each article

Use this to:
- Confirm which articles exist for a domain
- Find related articles you might not think of from the title alone (follow the cross-references)
- Check if a topic is covered (some articles are ⚠️ marked as not yet written)
- **If a topic is marked ⚠️ and points to RC-UNCLASSIFIED-01, read that article** — it contains interim coverage for gaps in Project Lifecycle, Production Changes, Data Quality, API, MLM, and MyCap

### Step 3 — Select articles to read

Pick up to 3 articles that best cover the topic. Guidance:
- For a broad question, read the domain overview first (`NN=01`) before specifics
- For a narrow question, go directly to the specific article
- If an article's prerequisites are flagged, read those first to avoid gaps
- Prefer depth over breadth: 2 well-chosen articles beat 4 loosely related ones

### Step 4 — Read the articles

Read each selected article in full using the Read tool. They're concise markdown files — usually 1–3 pages.

### Step 5 — Return findings

Summarize what you found and cite the source articles by their ID and title (e.g., `RC-BL-02 — Branching Logic: Syntax & Atomic Statements`). If called from another skill, make the full article content available for that skill's next steps.

If no relevant article exists, say so clearly — don't guess or fill in from general REDCap knowledge when the KB should be the authority.

## Example — broad question

**Query:** "How does branching logic work?"

1. Domain: BL. Start with `RC-BL-01` (overview).
2. Check REFERENCE-MAP — BL has 4 articles; RC-BL-01 links to RC-BL-02 for syntax details.
3. Read RC-BL-01 and RC-BL-02.
4. Return: summary of scope + syntax, citing both articles.

## Example — narrow / cross-domain question

**Query:** "How do I use branching logic on a checkbox field?"

1. Domain: BL, but also touches FD (field types).
2. REFERENCE-MAP shows RC-BL-04 specifically covers structured fields and checkboxes.
3. Read RC-BL-04 (and its prerequisite RC-BL-02 if context is needed).
4. Return: specific answer from RC-BL-04, citing it.

## Called from another skill

When another skill (e.g., kb-creation) asks you to find related articles before writing new content, follow this same process and return both the article IDs and their full markdown content so the calling skill can use them for context and cross-referencing.

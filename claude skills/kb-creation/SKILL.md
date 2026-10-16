---
name: kb-creation
description: >
  Use this skill when the user wants to create a new REDCap Knowledge Base article in the RC-KB
  format, usually by converting a training outline (a Word document) or other source material, or
  by writing from a topic description. Triggers include providing a training outline .docx, asking
  to "convert this outline", "build a KB article", "write a new KB article on", "turn this into a
  KB article", or any request to produce a new RC-[DOMAIN]-[NN] article. Also trigger when the
  user says things like "let's do the next outline" or "here's the next one". Do NOT use for
  editing, correcting or adding to existing articles (use kb-update), or for simply looking
  something up in the KB (use kb-search).
---

# REDCap KB Article Builder

This skill turns source material (usually a REDCap training outline in Word) into a single, RAG-optimized Knowledge Base article in the RC-KB format.

## What you're producing

A `.md` KB article that:
- Covers exactly one concept or workflow (one retrieval query pattern)
- Follows the corpus template in `references/article-template.md`
- Is optimized for LLM retrieval — explicit Q&A pairs, consistent terminology, surfaced edge cases
- Is institution-agnostic in its core content
- Is ready for RAG ingestion and the ServiceNow export

**Reference files in this skill** (read them when the step says so):

| File | Contents |
|---|---|
| `references/article-template.md` | The exact article skeleton and format rules |
| `references/writing-rules.md` | Version fields, version caveats, synonyms, scope pointers, style, no images, institutional callouts |
| `references/domain-slugs.md` | The canonical list of domain slugs and how to check it |

Write the output directly as a markdown file using the Write tool.

---

## Step 0: Verify repo access (run before anything else)

Check that the KB repo is accessible. Locate the REDCap_KB_RAG repo: use the current working directory if it contains `kb/` and `meta/` folders; otherwise ask the user where their copy of the repo is and request access to it for this session. The KB articles are in its `kb/` folder.

- **If accessible** → proceed.
- **If not accessible** → ask the user for the repo location and request access to it for this session. Do not proceed until access is confirmed.

All repo paths below are relative to that folder.

---

## Step 1: Read and analyze the source

When the user provides a Word document:

1. Read the `.docx` at the path the user gives. The Read tool cannot parse `.docx`; use the `docx` skill, or convert it with `pandoc "<file>.docx" -t markdown`
2. Identify all chapters or sections in the outline
3. Assess whether the outline maps to one article or multiple — see **Scope decisions** below
4. Use the kb-search skill to find existing articles on the same topic, so you don't duplicate one and can cross-reference the rest
5. Present your assessment to the user before proceeding: list the proposed article(s), their proposed IDs, and your rationale. Wait for confirmation.

### Scope decisions

**Merge into one article** when chapters cover a single retrieval query pattern — a user asking one question would need all of them. Example: "What is branching logic?" and "Where is branching logic configured?" belong together.

**Split into separate articles** when chapters cover fundamentally different retrieval patterns — a user asking about topic A would never need topic B in the same lookup. Each gets its own article ID.

When in doubt, ask rather than decide unilaterally.

---

## Step 2: Determine the Article ID

Read `meta/KB-INDEX.md` (and `meta/KB-CROSS-REFS.md` if you need dependency details). Use them to:
- Confirm the next available number in the relevant domain
- Check whether the articles the new article will reference already exist
- Identify articles that should gain an inbound link to the new article once it's added

### Domain slug double-check (run every time)

Check the proposed slug against `references/domain-slugs.md`, which is the canonical list.

- **Slug is listed** → use it as-is.
- **Slug is not listed** → first run the drift check in that file (a slug already used in `kb/` is established even if the table missed it). If it is genuinely new, stop: tell the user the proposed slug, show the row you would add, and ask for confirmation. Once confirmed, add the row to `claude skills/kb-creation/references/domain-slugs.md` **in the repo** (not only in an installed copy).
- **Slug exceeds 5 characters** → flag it immediately; propose a shorter alternative and confirm with the user. (SENDIT is the one permanent exception.)

Article IDs follow this format:
```
RC-[DOMAIN]-[NN]
RC-[DOMAIN]-[SUBDOMAIN]-[NN]
```

Rules:
- `RC` prefix always
- DOMAIN: uppercase, max 5 characters (e.g., NAV, RAND, DAG, BL, FD, DE)
- Subdomain: optional, uppercase, max 3 characters — use when a domain has two or more clearly distinct article groups (e.g. `NAV-UI`, `NAV-REC`). External Modules use the `EM` subdomain (`RC-AT-EM-01`)
- Two-digit zero-padded numbers (01, 02, 03...)
- Subdomain numbers restart at 01 under each parent
- **IDs are permanent once assigned** — confirm with the user before finalizing

Filename format:
```
RC-[DOMAIN]-[NN]_[Descriptive-Title-In-Title-Case].md
```

---

## Step 3: Write the article

1. Read `references/article-template.md` and `references/writing-rules.md`.
2. Open one recent article in `kb/` from a related domain and match its format exactly.
3. Write the article. Section guidance:
   - **1. Overview** — one plain-language paragraph for someone who has never opened REDCap.
   - **2. Key Concepts & Definitions** — define every REDCap term the article uses, as bold paragraphs.
   - **3 onward — topic content** — procedures, reference tables or structured explanations, with numbered subsections. Title each section for its content. Combine or omit sections as appropriate.
   - **Common Questions** — at least 5 Q&A pairs, phrased exactly as a real user would ask. Answers direct and complete; no "it depends" without saying what it depends on.
   - **Common Mistakes & Gotchas** — at least 3 entries: what the user does wrong, what happens, how to prevent or recover.
   - **Related Articles** — prerequisites, natural next articles, adjacent topics, as links.
4. Set the header fields per `writing-rules.md`: `Requires`, `Verified Against` (honest about how it was verified), `Version` 1.0, `Last Updated` as `YYYY-MM`, 6–10 collision-safe Synonyms.

### RAG optimization checklist

Before finalizing, verify:
- [ ] Article covers exactly one retrieval query pattern
- [ ] Format matches `references/article-template.md` (bold title line, header table, numbered `##` sections with `---`)
- [ ] Q&A pairs use natural language a user would actually type
- [ ] All REDCap-specific terms are defined in Section 2
- [ ] Edge cases and gotchas are explicitly surfaced (not buried)
- [ ] Cross-references are markdown links with full ID + title
- [ ] Every out-of-scope mention has a pointer (existing article, *(coming soon)*, or a new `KB-GAPS-TODO.md` entry)
- [ ] Terminology is consistent throughout (no synonym drift)
- [ ] Synonyms row present with 6–10 collision-safe phrases
- [ ] No institution-specific content in the core sections — no institution names, hosts or URLs; mark local variation with a `> **Institution-specific:**` callout
- [ ] No images, screenshots, or image placeholders; UI described in text

---

## Step 4: Save and update the reference files

1. Write the `.md` file to `kb/RC-[DOMAIN]-[NN]_[Title].md`.
2. **`meta/KB-INDEX.md`** — add a row in the position that matches the existing order (the index is grouped by domain, not strictly alphabetical):
   ```
   | RC-[DOMAIN]-[NN] | [Title] | RC-[DOMAIN]-[NN]_[Title-In-Title-Case].md |
   ```
3. **Run the repo scripts** from the repo root, in this order:
   - `python add_crosslinks.py` (dry run) — review every line it lists, then `python add_crosslinks.py --apply` to convert bare or backticked RC IDs into links
   - `python build_cross_refs.py` — regenerates `meta/KB-CROSS-REFS.md` (prerequisites, outbound and inbound links) from the articles. Never edit that file by hand
   - `python build_dependency_graph.py` — refreshes the dependency graph
   - `python convert_to_yaml_kb.py` — regenerates `kb (YAML)/`, which the ServiceNow ETL reads
   - After a batch of articles: `python "ServiceNow ETL/kb_to_servicenow.py"` and check its synonym collision report

   `meta/KB-CROSS-REFS.md` is generated — the new article's section and every inbound link to it appear automatically once the article and its `KB-INDEX.md` row exist.

## Step 5: Report

Give the user the article's file path as a link, then summarize in 2–3 sentences: article ID, title, section count, and any scope decisions made. Mention anything you added to `KB-GAPS-TODO.md`. Do not explain the entire article back to the user — they can read it.

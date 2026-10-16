---
name: kb-update
description: |
  Use this skill whenever the user wants to update, correct, revise, or add to existing REDCap KB articles, or when new source material (a Word document, a text description, a correction) arrives that may need to go into the knowledge base. Triggers include uploading a new .docx or text with updated REDCap content, saying "update the article about X", "add this to the KB", "this article is wrong/outdated", "REDCap changed how X works", "add a Q&A about Y", "there is a new feature in REDCap". Also trigger when the user says things like "here is new info" or "this needs to be in the KB" without specifying a specific article. Use this skill even if you are not sure whether the content maps to an existing article — the skill handles that assessment. Do NOT use this skill to create a brand-new article from a training outline from scratch — use the kb-creation skill for that. Do NOT use it for read-only lookups — use kb-search.
---

# REDCap KB Updater

This skill routes new information into the right place in the knowledge base — updating existing articles, adding Q&A pairs, correcting errors, or triggering new article creation when the content doesn't fit anywhere that already exists.

---

## Step 0: Verify repo access

Locate the REDCap_KB_RAG repo: use the current working directory if it contains `kb/` and `meta/` folders; otherwise ask the user where their copy of the repo is and request access to it for this session. The KB articles are in its `kb/` folder. All repo paths below are relative to that folder.

- **If accessible** → proceed.
- **If not accessible** → ask the user for the repo location and request access to it for this session. Do not proceed until access is confirmed.

---

## Step 1: Understand the input

The input may come in several forms:

- **A Word document** → read it at the path the user gives. The Read tool cannot parse `.docx`; use the `docx` skill, or `pandoc "<file>.docx" -t markdown`
- **A plain-text description** → the user's message itself is the input
- **A targeted correction** → the user names a specific article and a specific fix
- **A new feature description** → information about REDCap behavior or a feature that may or may not be covered

Before searching the KB, summarize your understanding of:
1. What topic or feature does this input cover?
2. What type of change is it — a correction, an addition, a new concept, a new procedure?
3. Is it scoped to a specific article the user mentioned, or is the target unclear?

If the input is ambiguous about what it's describing, ask one clarifying question before proceeding.

---

## Step 2: Find candidate articles

Read `meta/KB-INDEX.md` to identify which existing articles might cover the same topic.

Then read the 1–3 most likely candidates in full. Look for:
- Does the existing article already cover this content (possibly just needs correction)?
- Is the new content a natural extension of an existing article (add to it)?
- Does the new content represent a distinct retrieval pattern that no existing article captures?

If you need to think about which domain this content falls under, see `~/.claude/skills/kb-creation/references/domain-slugs.md`.

**Special case — External Module Content:** If the content is about functionality from an External Module (third-party plugin), propose an article ID in the `RC-{DOMAIN}-EM-*` subdomain instead of continuing the sequential numbering within that domain. For example:
   - `RC-AT-EM-01` for action tag modules (e.g., HIDESUBMIT)
   - `RC-BL-EM-01` for branching logic modules
   - `RC-SURV-EM-01` for survey-related modules
   - `RC-FD-EM-01` for form design modules

This preserves the standard sequential numbering for core/standard REDCap features and creates a clear subdomain for module-specific content across all domains. This is important because external modules can impact many different feature areas.

Present your assessment to the user:
- Which article(s) are likely affected, and why
- Whether you think this is an update, an addition to an existing article, or something new
- If new: what article ID you'd assign and what the scope would be

**When in doubt, ask rather than assume.** Especially for:
- Content that spans multiple domains (could go in two articles)
- Content that is adjacent to an existing article but feels like a separate concern
- Content that belongs in an article but would substantially change its scope

---

## Step 3a: Update an existing article

If the input maps to one or more existing articles, make targeted edits.

### Types of updates

| Update type | Where it goes |
|---|---|
| Correcting wrong/outdated information | Edit the affected section directly |
| Adding a new procedure or option | Add to the relevant procedural section (3+) |
| Adding a Q&A pair | Append to the Common Questions section |
| Adding a known mistake/gotcha | Append to the Common Mistakes & Gotchas section |
| New cross-reference | Add to both the header's **Related Topics** row and the **Related Articles** section, as markdown links; then regenerate `meta/KB-CROSS-REFS.md` (Step 4) inbound/outbound links |
| New procedure/Q&A that changes what users would search for | Add matching phrases to the **Synonyms** metadata row (see Synonyms rule below) |
| Behaviour that varies by institution | Add or update a generic `> **Institution-specific:**` callout at the relevant point (never a named institution); actual local values go only in the `RC-INST-*` articles |

### Rules for edits

- **Make surgical changes** — don't rewrite sections that don't need it. Touch only what the new input affects.
- **Preserve voice and style** — match the article's existing tone (direct, instructional, no filler phrases).
- **Bump the version number** — increment the patch version in the metadata table (1.0 → 1.1, 1.2 → 1.3, etc.).
- **Update Last Updated** — set to the current month as `YYYY-MM`.
- **Update `Verified Against`** — set to the REDCap version the edit was checked against, naming both lines (e.g. `REDCap v17.4.1 (Standard) / v17.3.7 (LTS)`). Only bump it if you actually verified the content against that version or a changelog diff for it; leaving an honest older value is better than an unchecked current-looking one. If the article has no `Requires` / `Verified Against` rows, add both — see **Version tracking fields** in `~/.claude/skills/kb-creation/references/writing-rules.md`.
- **Set `Requires` only if the article's scope changed.** It records the earliest REDCap version supporting the documented feature and does not move on routine edits. `Applies To` never carries a version — migrate any legacy version string out of it into these fields.
- **If the edit documents behaviour that was wrong for a version range**, add a `> **Version caveat:**` blockquote immediately after the affected content — see **Version caveats** in `~/.claude/skills/kb-creation/references/writing-rules.md` for format and the bar an entry must clear.
- **Never add an image, screenshot, or image placeholder**, and remove any you find. The KB is text-only: images are invisible to RAG retrieval and go stale as REDCap's UI changes. Describe the interface in words instead — exact labels in bold, location on the page, options in a table. See **No images** in `~/.claude/skills/kb-creation/references/writing-rules.md`. Note that `@PLACEHOLDER` is a REDCap action tag and legitimate content; never bulk-remove on the string "PLACEHOLDER" alone.
- **If adding a Q&A**, write the question as a real user would ask it. The answer must be direct and complete.
- **If adding a gotcha**, follow the pattern: bold lead phrase → what goes wrong → what to do instead.
- **Keep synonyms current.** Every article carries a **Synonyms** metadata row (semicolon-separated alt search phrasings that flow into the ServiceNow `meta` field via `convert_to_yaml_kb.py`). When an edit adds a new capability, procedure, or Q&A that a user would search for differently, add 1–3 matching phrases to the Synonyms row. Follow the generation and collision-avoidance rules in **Synonyms** in `~/.claude/skills/kb-creation/references/writing-rules.md`: user-language phrasings, specific to the article, and qualified so they don't collide with sibling articles. If the article predates synonyms and has no Synonyms row, add one (6–10 phrases) as part of the update. After a batch of edits, regenerate the YAML copy and check collisions (see Step 4).

After editing, give the user the path of each updated article as a link.

---

## Step 3b: Handle out-of-scope references encountered during editing

While reading or editing a KB article, if you encounter language like "out of scope for this article" or "covered in separate training" **without a pointer to a specific article or a *(coming soon)* flag**:

1. Check `KB-GAPS-TODO.md` (repo root) to see whether the topic is already listed as a planned article.
2. **If it is listed** — replace the "out of scope" language with a *(coming soon)* pointer using the planned article ID and title. Example: `see RC-API-01 — REDCap API *(coming soon)*`.
3. **If it is not listed** — add a new entry to `KB-GAPS-TODO.md` following the existing format (article ID, why needed, domain slug, what to cover), then apply the *(coming soon)* pointer in the article.
4. Do not leave bare "out of scope" language in articles. Every deferred topic should either link to an existing article or carry a *(coming soon)* flag with a planned ID.

---

## Step 3c: Create a new article

If the input covers a topic not adequately addressed by any existing article, do not write the article here. Instead:

1. Tell the user: "This content doesn't fit neatly into any existing article. I'd suggest creating **RC-[DOMAIN]-[NN] — [Proposed Title]**. Want me to create it with the kb-creation skill?"
2. Wait for the user to confirm.
3. If confirmed: invoke the kb-creation skill (Skill tool), passing the current input as source material.

Don't create new articles silently — always confirm first.

---

## Step 4: Update the Reference Files

After any change, update the appropriate file(s) in `meta/`:

- **Article title changed** → update `meta/KB-INDEX.md` (the Article Index table), the article's own **Article ID** self-link, and every inbound link: links embed the title, so Grep `kb/` for the old title and update each match
- **New article created** → follow kb-creation's Step 4 (add the `meta/KB-INDEX.md` row, then run the scripts)

`meta/KB-CROSS-REFS.md` is a generated file — never edit it by hand; `build_cross_refs.py` rebuilds it from the articles.

**Then, from the repo root:**
- If you added bare or backticked RC IDs: `python add_crosslinks.py` (dry run) — review every line it lists — then `python add_crosslinks.py --apply`
- If links, prerequisites or titles changed: `python build_cross_refs.py` and `python build_dependency_graph.py`
- Always: `python convert_to_yaml_kb.py` — regenerates `kb (YAML)/`, which the ServiceNow ETL reads
- After a batch of edits that touched Synonyms: `python "ServiceNow ETL/kb_to_servicenow.py"` and check its collision report

---

## Step 5: Summarize what changed

Briefly state:
- Which article(s) were modified (ID + title)
- What type of change was made (correction, addition, new article, etc.)
- Whether `meta/KB-INDEX.md` was updated and whether `build_cross_refs.py` was run (and why, or why not)

Don't explain every sentence you changed — the user can read the document. Keep the summary to 2–4 sentences.

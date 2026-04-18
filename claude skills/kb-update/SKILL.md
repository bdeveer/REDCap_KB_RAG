---
name: redcap-kb-updater
description: |
  Use this skill whenever the user wants to update, correct, revise, or add to existing REDCap KB articles, or when new source material (a Word document, a text description, a correction) arrives that may need to go into the knowledge base. Triggers include uploading a new .docx or text with updated REDCap content, saying "update the article about X", "add this to the KB", "this article is wrong/outdated", "REDCap changed how X works", "add a Q&A about Y", "there is a new feature in REDCap". Also trigger when the user says things like "here is new info" or "this needs to be in the KB" without specifying a specific article. Use this skill even if you are not sure whether the content maps to an existing article — the skill handles that assessment. Do NOT use this skill to create a brand-new article from a training outline from scratch — use the redcap-kb-builder skill for that.
---

# REDCap KB Updater

This skill routes new information into the right place in the knowledge base — updating existing articles, adding Q&A pairs, correcting errors, or triggering new article creation when the content doesn't fit anywhere that already exists.

---

## Step 0: Verify repo access

Check whether `kb/` is accessible at `/sessions/.../mnt/REDCap_KB_RAG/kb/`.

- **If accessible** → proceed.
- **If not accessible** → call `mcp__cowork__request_cowork_directory` with path `/Users/bas/REDCap_KB_RAG`. Do not proceed until confirmed.

---

## Step 1: Understand the input

The input may come in several forms:

- **A Word document** → read it from `/mnt/user-data/uploads/` using the Bash tool or Read tool
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

Use the domain slug reference at the bottom of the kb-builder skill if you need to think about which domain this content falls under.

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
| New cross-reference | Add to Related Articles; update `meta/KB-CROSS-REFS.md` inbound/outbound links |
| Yale-specific policy | Add or update the Yale-specific callout at the relevant point |

### Rules for edits

- **Make surgical changes** — don't rewrite sections that don't need it. Touch only what the new input affects.
- **Preserve voice and style** — match the article's existing tone (direct, instructional, no filler phrases).
- **Bump the version number** — increment the patch version in the metadata table (1.0 → 1.1, 1.2 → 1.3, etc.).
- **Update Last Updated** — set to the current year.
- **If adding a Q&A**, write the question as a real user would ask it. The answer must be direct and complete.
- **If adding a gotcha**, follow the pattern: bold lead phrase → what goes wrong → what to do instead.

After editing, use `present_files` to share the updated article with the user.

---

## Step 3b: Handle out-of-scope references encountered during editing

While reading or editing a KB article, if you encounter language like "out of scope for this article" or "covered in separate training" **without a pointer to a specific article or a *(coming soon)* flag**:

1. Check `kb/KB-GAPS-TODO.md` to see whether the topic is already listed as a planned article.
2. **If it is listed** — replace the "out of scope" language with a *(coming soon)* pointer using the planned article ID and title. Example: `see RC-API-01 — REDCap API *(coming soon)*`.
3. **If it is not listed** — add a new entry to `KB-GAPS-TODO.md` following the existing format (article ID, why needed, domain slug, what to cover), then apply the *(coming soon)* pointer in the article.
4. Do not leave bare "out of scope" language in articles. Every deferred topic should either link to an existing article or carry a *(coming soon)* flag with a planned ID.

---

## Step 3c: Create a new article

If the input covers a topic not adequately addressed by any existing article, do not write the article here. Instead:

1. Tell the user: "This content doesn't fit neatly into any existing article. I'd suggest creating **RC-[DOMAIN]-[NN] — [Proposed Title]**. Want me to proceed with the kb-builder skill?"
2. Wait for the user to confirm.
3. If confirmed: use Glob with pattern `**/kb-creation/SKILL.md` to locate the kb-creation skill within the REDCap_KB_RAG repo (the same repo verified in Step 0), read it with the Read tool, then follow its instructions, passing the current input as source material.

Don't create new articles silently — always confirm first.

---

## Step 4: Update the Reference Files

After any change, update the appropriate file(s) in `meta/`:

- **Article title changed** → update `meta/KB-INDEX.md` (the Article Index table)
- **New cross-reference added** → load `meta/KB-CROSS-REFS.md` and update outbound links of the edited article **and** inbound links of the referenced article
- **New article created** → follow the kb-builder's Reference Map update procedure: add to the index in `meta/KB-INDEX.md`, add the per-article section in `meta/KB-CROSS-REFS.md`, and update inbound links of referenced articles in `meta/KB-CROSS-REFS.md`
- **Existing ⚠️ gap filled** → load `meta/KB-CROSS-REFS.md` and remove the ⚠️ marker from any articles that referenced the now-written article

Only load `meta/KB-CROSS-REFS.md` when cross-reference structure actually needs to change — for title-only edits, `meta/KB-INDEX.md` is sufficient. If nothing changed, say so explicitly.

---

## Step 5: Summarize what changed

Briefly state:
- Which article(s) were modified (ID + title)
- What type of change was made (correction, addition, new article, etc.)
- Whether `meta/KB-INDEX.md` or `meta/KB-CROSS-REFS.md` was updated and why (or why not)

Don't explain every sentence you changed — the user can read the document. Keep the summary to 2–4 sentences.

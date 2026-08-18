---
name: redcap-kb-builder
description: Use this skill when the user wants to convert a REDCap training outline (uploaded as a Word document) into a RAG-optimized Knowledge Base article in the RC-KB format. Triggers include: uploading a training outline .docx, asking to "convert this outline", "build a KB article", "turn this into a KB article", or any request to produce a new RC-[DOMAIN]-[NN] article from source material. Also trigger when the user says things like "let's do the next outline" or "here's the next one". Do NOT trigger for editing or refining existing articles — use the redcap-kb-refiner skill for that.
---

# REDCap KB Article Builder

This skill converts a raw REDCap training outline (Word document) into a single, RAG-optimized Knowledge Base article following the RC-KB standard format.

## What you're producing

A `.md` KB article that:
- Covers exactly one concept or workflow (one retrieval query pattern)
- Follows the 8-section template (see below)
- Is optimized for LLM retrieval — explicit Q&A pairs, consistent terminology, surfaced edge cases
- Is institution-agnostic in its core content
- Is ready for RAG ingestion into Yale's local LLM

Write the output directly as a markdown file using the Write tool — no docx skill needed.

---

## Step 0: Verify repo access (run before anything else)

Check whether the KB repo is mounted by testing whether the `kb/` directory is accessible:

```
/sessions/.../mnt/REDCap_KB_RAG/kb/
```

- **If accessible** → proceed to Step 1.
- **If not accessible** → call `mcp__cowork__request_cowork_directory` with path `/Users/bas/REDCap_KB_RAG` to mount it. Do not proceed until access is confirmed.

Do this every time the skill runs, even if the repo was accessible in a previous session — mounts do not persist between sessions.

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

## Step 2: Read the Reference Files & Determine the Article ID

Before assigning an ID, read both:

```
meta/KB-INDEX.md
meta/KB-CROSS-REFS.md
```

Use these to:
- Confirm the next available number in the relevant domain (from the index)
- Check whether any articles the new article will reference are already written (vs. marked ⚠️ as missing)
- Identify articles that should gain an inbound link to the new article once it's added

### Domain slug double-check (run every time)

Cross-check the proposed domain slug against the **Reference: Established domain slugs** table at the bottom of this skill file. This table is the canonical source.

- **Slug exists in the table** → use it as-is.
- **Slug is not in the table** → stop. Tell the user: the proposed slug (e.g. `IMP`) is not yet established, show them what you'd add, and ask for confirmation before proceeding. Once confirmed, add the new slug row to the table at the bottom of this skill file.
- **Slug exceeds 5 characters** → flag it immediately; propose a shorter alternative and confirm with the user.

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

Filename format:
```
RC-[DOMAIN]-[NN]_[Descriptive-Title-In-Title-Case].md
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
| Requires | REDCap v[X.Y.Z]+ *(or "Any supported version")* |
| Verified Against | REDCap v[X.Y.Z] (Standard) / v[X.Y.Z] (LTS) |
| Prerequisite | [Article ID — Title, or "None"] |
| Version | 1.0 |
| Last Updated | [Year] |
| Author | REDCap Support |
| Related Topics | [RC-XX-NN — Title; RC-XX-NN — Title] |
| Synonyms | [phrase 1; phrase 2; phrase 3; ... — see Synonyms section below] |

##### Version tracking fields

`Requires` and `Verified Against` answer different questions and drift independently. Both are mandatory.

| Field | Question it answers | Changes when |
|---|---|---|
| **Requires** | "Can I use this on my instance?" | Never, unless the article's scope changes. It records the REDCap version that first made the documented feature available. Use `Any supported version` for features that predate the KB. |
| **Verified Against** | "Is this article stale?" | Every time someone checks the article against a live instance or a changelog diff. Always name both release lines, since they are numbered independently. |

Rules:

- **`Applies To` never carries a version.** It describes audience, project type and required user rights only. Version data goes in the two dedicated fields. (Historically a handful of articles put a version in `Applies To` — treat those as legacy and migrate on next edit.)
- **`Requires` uses the earliest version that supports the feature**, not the newest. If an article documents several features introduced at different times, use the earliest in the header and mark the later ones inline with a version caveat.
- **`Verified Against` names both lines** — e.g. `REDCap v17.4.1 (Standard) / v17.3.7 (LTS)`. Never write a bare version number; a reader cannot tell which line it refers to.
- **Never bump `Verified Against` without actually verifying.** An unchecked article with an honest older date is more useful than a current-looking one nobody confirmed.
- **Say what kind of verification it was.** The two are not equivalent and readers need to tell them apart:
  - `REDCap v17.4.1 (Standard) / v17.3.7 (LTS) — changelog review; page not re-captured` — the article was checked against the changelog and needed no change. This is the honest stamp for a bulk review pass.
  - `REDCap 17.3.6 (LTS)` with no qualifier — the page itself was captured and read.
  Where only part of an article could be checked, say which part: `Control Center configuration (§4–5) verified; the project-level interface is from release notes only`.
- Neither field replaces `Version` (the article's own revision number) or `Last Updated` (when the prose last changed).

See `RC-VER-01 — REDCap Versions, Release Lines & Patching` for what the release lines mean.

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

## Version caveats (behaviour that was wrong for a known range of versions)

When REDCap behaved differently — or incorrectly — across a known version range, mark it inline rather than silently documenting only current behaviour. A reader on an older instance needs to know that the article's advice does not hold for them.

**Format:** a blockquote placed immediately after the content it qualifies, never collected at the end of the article.

```
> **Version caveat (17.0.6–17.1.1):** `age_at_date()` fails on calc fields
> when the third parameter is omitted. Pass it explicitly as a workaround,
> or upgrade to 17.2.0+. Fixed progressively across 17.0.7, 17.0.8, 17.1.2,
> 17.1.3 and 17.2.0.
```

**Rules:**

- **State the range in the bold lead**, in parentheses. Use `(17.0.6–17.1.1)` for a closed range, `(≤16.0.4)` for everything up to a fix, `(17.2.0+)` for behaviour that only exists on newer versions.
- **Only claim a range the changelog supports.** A fix version tells you when something was repaired, not when it broke. Write an open-ended range unless the changelog states "Bug emerged in REDCap X" or "Bug exists in REDCap X and higher."
- **Name the release line when the two diverge.** "Fixed in 17.4.1 Standard / 17.3.7 LTS" — not "fixed in 17.4.1."
- **Give the reader an action**: a workaround, an upgrade target, or something to go re-check in their own data. A caveat that only says "this was broken" wastes the reader's attention.
- **Retire caveats once the range falls out of support.** These are maintenance debt; when no supported version is affected, delete the blockquote.
- **Do not use this for routine bug fixes.** A caveat earns its place only if it changes what a reader should believe about how the feature behaves, defines a window where documented behaviour did not hold, or silently affected data, rights or delivery in a way the user could not have detected at the time.

Source material for existing caveats: `meta/KB-GOTCHAS-FROM-BUGFIXES-17.4.1.md`.

---

## Synonyms (search findability for ServiceNow / AI search)

Every article must carry a **Synonyms** row in the metadata table. Synonyms are alternate search phrasings that downstream systems index (they flow through `convert_to_yaml_kb.py` into the `synonyms:` YAML key, then into the ServiceNow `kb_knowledge.meta` field). They never appear in the article body — they exist purely to help a user or AI assistant find the article.

**Format:** semicolon-separated phrases in the metadata table row, e.g.
`| Synonyms | how do i send an automated email; email reminders; conditional email alert; staff notification email |`

**Generation rules:**
- Write **6–10** phrases per article.
- Use the language a real REDCap user would type or ask — question forms ("how do i export records via the api"), informal/alternate names, common abbreviations, and task-oriented phrasings. Not formal headings.
- Make every phrase **specific to this article's actual content**.
- **Qualify generic phrases so they don't collide with sibling articles** — this is the most important rule. For near-identical article families:
  - *API method articles*: qualify with the specific method/object — "export records api call", not "get data from api".
  - *Smart variable / piping articles*: embed the actual tokens for that article — `[user-name]`, `[event-name]`, `[record-name]`.
  - *Action tag articles*: include the literal tag names (`@HIDDEN`, `@CALCTEXT`) — single-quote them in YAML since they start with `@`.
  - *Any numbered series* (CC, DE, EXPRT, SURV, USER…): qualify with the subtopic so each article owns a distinct variant.
- Do **not** duplicate a tag verbatim. Lowercase is preferred.

**Collision check:** after a batch of new articles, run the ServiceNow ETL (`ServiceNow ETL/kb_to_servicenow.py`) — it prints a synonym collision report flagging any phrase claimed by more than one article. Resolve flagged overlaps by qualifying each to its own variant, assigning a canonical owner, or keeping the overlap if both articles are genuinely relevant.

---

## Handling out-of-scope topics within a new article

When writing a new article, you will often need to mention topics that fall outside its scope. **Never use bare "out of scope" language.** Instead, always provide a pointer:

- **If an article already exists** — link by ID and title: `see RC-FD-07 — Field Embedding`
- **If an article is planned** — use the *(coming soon)* flag: `see RC-BL-05 — Branching Logic in Longitudinal Projects *(coming soon)*`
- **If no article exists and none is planned** — add an entry to `kb/KB-GAPS-TODO.md` first, then use the *(coming soon)* flag with the new planned ID.

To check whether a topic is already planned, read `kb/KB-GAPS-TODO.md` before writing the scope sections of the article. Do not leave scope callouts without a pointer.

---

## Style rules (derived from BL series)

- **Terminology**: Use REDCap's canonical terms. "Instrument" not "form" or "survey" unless distinguishing. "Variable" not "field" unless quoting the UI.
- **Voice**: Direct, instructional. No filler phrases ("It's important to note that...").
- **Tables**: Use for reference content with 3+ rows. Don't use tables for 2-item comparisons — prose is cleaner.
- **Notes and warnings**: Use blockquotes (`> **Note:**`, `> **Important:**`, `> **Critical:**`) for callouts.
- **Version caveats**: Use a `> **Version caveat:**` blockquote placed immediately after the content it qualifies — see below.
- **Cross-references**: Always include both the article ID and title: `RC-BL-02 — Syntax & Atomic Statements`
- **One concept per article**: If you find yourself writing "this article also covers...", that's a signal to split.
- **Text only — no images.** See below.

---

## No images: describe the UI in words

**The KB is text-only. Never add an image, a screenshot, or a placeholder for a future one.** This includes markdown images (`![...](...)`), `<img>` tags, and `<!-- PLACEHOLDER: Insert screenshot ... -->` comments.

Two reasons, both of which matter more than the convenience of a screenshot:

1. **Retrieval.** These articles are chunked and embedded for RAG. An image contributes nothing retrievable — a screenshot of a settings page is invisible to the system that has to answer a question about that page. Anything an image would convey has to exist as text or it effectively does not exist.
2. **Staleness.** REDCap ships releases roughly weekly and moves UI regularly. A screenshot silently goes wrong at the next redesign, and unlike prose nobody notices, because the words around it still read correctly.

**What to do instead:** describe the interface in words a reader can act on — the exact on-screen label in bold, where it sits on the page, the options in a table, and what each one does. Quote UI strings verbatim so a reader can match them against what they see, and so search finds them.

```
Wrong:  <!-- PLACEHOLDER: Insert annotated screenshot of AI Services section -->

Right:  **Control Center → System Configuration → AI Configuration Settings.**
        It sits directly beneath **Modules/Services Configuration** in the
        left-hand menu.

        | Setting | What it controls |
        |---|---|
        | **AI config enabled for all non-project pages** | ... |
```

If a UI is genuinely too complex to describe, that usually means the article is trying to cover too much — split it rather than reaching for a picture.

> **Note:** `@PLACEHOLDER` is a REDCap action tag and legitimate article content. Do not confuse it with the image placeholder comments described above; never bulk-remove on the string "PLACEHOLDER" alone.

---

## RAG optimization checklist

Before finalizing, verify:
- [ ] Article covers exactly one retrieval query pattern
- [ ] Q&A pairs use natural language a user would actually type
- [ ] All REDCap-specific terms are defined in Section 2
- [ ] Edge cases and gotchas are explicitly surfaced (not buried)
- [ ] Cross-references use full ID + title format
- [ ] Terminology is consistent throughout (no synonym drift)
- [ ] Synonyms row present with 6–10 collision-safe phrases (see Synonyms section)
- [ ] No institution-specific content in the core sections (see below)
- [ ] No images, screenshots, or image placeholders; UI described in text (see **No images** section)

---

## Institutional policy section

If the article touches on behavior that varies by institution (e.g., Production mode approval workflows, administrator intervention policies, local support contacts), add a clearly marked callout box at the relevant point:

```
> **Yale-specific:** [Describe what varies and what Yale's policy is —
> leave blank until confirmed with Yale REDCap support team]
```

This placeholder signals to future editors where local policy needs to be inserted without contaminating the institution-agnostic core content.

---

## Output

### Steps

1. Write the `.md` file directly to `kb/` in the repo: `/sessions/.../mnt/REDCap_KB_RAG/kb/RC-[DOMAIN]-[NN]_[Title].md`
2. Use `present_files` to share it with the user
3. Update the Reference Map (see below)
4. Summarize in 2–3 sentences: article ID, title, section count, and any scope decisions made

Do not explain the entire article back to the user — they can read the document.

---

## Updating the Reference Files

After the article is written and saved, update both `meta/KB-INDEX.md` and `meta/KB-CROSS-REFS.md`. Make all three changes — ideally two edits, one per file:

### 1. Add to the Article Index table — edit `meta/KB-INDEX.md`

Insert a new row in alphabetical/numerical order by Article ID:

```
| RC-[DOMAIN]-[NN] | [Title] | RC-[DOMAIN]-[NN]_[Title-In-Title-Case].md |
```

Note: the filename in the index uses `.md` (the RAG corpus version), not `.docx`.

### 2. Add a Per-Article Reference Details section — edit `meta/KB-CROSS-REFS.md`

Insert a new `###` section in document order (matching the Article Index order). Use this structure:

```markdown
### RC-[DOMAIN]-[NN] — [Title]

**Prerequisites:** [RC-XX-NN — Title, or "None"]

**Outbound links:**
- RC-XX-NN — [Title]
- ...

**Inbound links (referenced by):**
- [Leave blank or list any articles already in the corpus that reference this new article]
```

Mark any outbound link target that doesn't exist yet in the corpus with ⚠️.

### 3. Update inbound links of referenced articles — edit `meta/KB-CROSS-REFS.md`

For every article the new article references, find its Per-Article Reference Details section in `meta/KB-CROSS-REFS.md` and add the new article to its **Inbound links** list. If the new article is a prerequisite of another existing article, note that too.

---

## Reference: Established domain slugs

Alphabetical by slug. Every slug in use in `kb/` appears here — if a slug is missing, that is a defect in this table, not a signal to stop. See **Keeping this table accurate** below.

| Slug | Domain | Notes |
|---|---|---|
| AI | AI Tools | Covers writing tools, AI translations, and AI summarization. System-level AI configuration lives in CC |
| ALERT | Alerts & Notifications | — |
| API | API | One article per endpoint, plus RC-API-01 for general concepts |
| AT | Action Tags | Subdomain: EM (action tags supplied by External Modules, not core REDCap) |
| BL | Branching Logic | — |
| CAL | Calendar | Covers the Calendar and Scheduling modules: manual entries, schedule generation, Ad Hoc events, iCal export, visit statuses, logging |
| CALC | Calculations & Special Functions | Covers built-in REDCap functions: date/datetime, numeric, text, conditional |
| CC | Control Center | Administrator-facing system configuration, one article per Control Center page or page group. Use for *what the setting does*; use INST for *what this institution set it to* |
| CDIS | Clinical Data Interoperability Services | FHIR/EHR integration: Clinical Data Pull (CDP), Clinical Data Mart (CDM), Break the Glass. Distinct from DDP — see that row |
| DAG | Data Access Groups | Record-level access partitioning. Not to be confused with Access Control Groups (RC-CC-25) or Project Administrator Groups |
| DDE | Double Data Entry | Independent duplicate entry and reconciliation. Distinct from DE |
| DDP | Dynamic Data Pull | The older custom DDP integration. Distinct from CDIS/CDP — the changelog refers to "CDP and Custom DDP" as separate things |
| DE | Data Entry | Entering and editing record data. Field-level design belongs in FD |
| DQ | Data Quality | Covers the Data Quality module, default rules, custom rules, and Rule H |
| DSGN | Project Design Best Practices | Cross-cutting design conventions: field alignment, project structure, branching logic patterns, repeating instruments, form hygiene |
| EM | External Modules | Framework, Module Manager, and per-instance installed catalogues. Catalogue articles follow the instance-tier pattern (Production / Test / Development) |
| EXPRT | Exports, Reports & Stats | — |
| FD | Form Design | Instrument and field design, Online Designer, Data Dictionary, field embedding |
| FDL | Form Display Logic | — |
| FILE | File Repository | Project-level file storage. Distinct from SENDIT (ad-hoc secure transfer) and from File Upload *fields*, which are FD/DE |
| IMP | Data Import | Covers the Data Import Tool and every bulk-upload CSV format |
| INFRA | Self-Hosting, Deployment & Release Management | Running a private/non-production REDCap instance: containerized stacks, install/upgrade, mail capture, AI proxy, remote access/HTTPS, backups. Platform-specific guides (e.g. Synology) live here too. Also covers the REDCap release model itself — Standard vs LTS lines, version numbering, changelog reading and patching practice — which applies to all readers, not only self-hosters |
| INST | Institution-Specific | Local policy and configuration values, deliberately quarantined from the institution-agnostic core. Follows the instance-tier pattern (Production / Test / Development) |
| INTG | Integrations | Outbound hooks into external systems, e.g. the Data Entry Trigger |
| LOCK | Record Locking & E-Signatures | — |
| LOG | Logging | Project-level audit trail; logging module access, filters, entry anatomy, retention, regulatory compliance context |
| LONG | Longitudinal & Repeated Setup | Covers longitudinal mode, arms/events, repeated instruments & events |
| MCP | MCP Server | The REDCap MCP server that exposes API methods as assistant tools. Tooling around REDCap, not a REDCap feature |
| MLM | Multi-Language Management | — |
| MOB | REDCap Mobile App | Study-team offline data collection app. Separate from MYCAP |
| MSG | Messenger | Covers REDCap Messenger: conversations, user roles, notifications, file sharing |
| MYCAP | MyCap Mobile App | Participant-facing mobile app; separate from MOB (REDCap Mobile App for study teams) |
| NAV | Navigation | Subdomains: UI (project menus, bookmarks, My Projects), REC (record navigation, dashboards, arms, repeating instances) |
| OPS | Operational Use Cases | Using REDCap for non-research operational workflows, e.g. request management |
| PIPE | Piping | Covers piping basics, longitudinal/repeated piping, modifiers, smart variables, emails & notifications |
| PLUS | REDCap+ | Features gated by the REDCap+ subscription rather than by version. Applies from v17.0.0 |
| PROF | My Profile | A user's own account settings. Use USER for administering *other* users' privileges |
| PROJ | Project | Covers project lifecycle, setup checklist, and project dashboards |
| RAND | Randomization | — |
| SENDIT | Send-It | Ad-hoc secure file transfer to named recipients. **Six characters — an accepted exception to the 5-character limit; the ID is permanent.** Do not create further slugs over five characters |
| SURV | Surveys | — |
| TXT | Texting (SMS) | Covers Twilio/Mosio setup, SMS invitations, voice calls, and admin configuration |
| USER | User Rights | Administering other users: roles, privileges, user management. Use PROF for a user's own profile |

### Keeping this table accurate

This table drifted badly once — 14 slugs were in active use in `kb/` while absent here, which turned the "stop and confirm" rule in Step 2 into a false stop on long-established domains. Check it rather than trusting it:

```bash
# Slugs used in kb/ but missing from this table (should print nothing)
comm -23 \
  <(ls kb/RC-*.md | sed -E 's|.*/RC-([A-Z]+)-.*|\1|' | sort -u) \
  <(grep -oE '^\| [A-Z]+ ' "claude skills/kb-creation/SKILL.md" | tr -d '| ' | sort -u)
```

Run this before relying on the table to reject a slug. If it prints anything, add the missing rows first — a slug already carrying published articles is established by definition, whatever this table says.

When you *do* add a genuinely new slug, add the row in the same commit as the first article that uses it. A slug with no article is a guess; a slug with an article and no row is the drift above.

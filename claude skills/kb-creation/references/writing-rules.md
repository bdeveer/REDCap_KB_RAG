# KB Writing Rules

Detailed rules for the header fields, version caveats, synonyms, scope pointers, style, images and institutional callouts. Read this before writing or substantially editing an article.

---

## Version tracking fields

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

See `RC-INFRA-03 — REDCap Versions, Release Lines & Patching` for what the release lines mean.

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

**Collision check:** after a batch of new articles, regenerate the YAML copy first (`python convert_to_yaml_kb.py` from the repo root — the ETL reads `kb (YAML)/`, not `kb/`), then run the ServiceNow ETL (`python "ServiceNow ETL/kb_to_servicenow.py"`). It prints a synonym collision report flagging any phrase claimed by more than one article. Resolve flagged overlaps by qualifying each to its own variant, assigning a canonical owner, or keeping the overlap if both articles are genuinely relevant.

---

## Handling out-of-scope topics within a new article

When writing a new article, you will often need to mention topics that fall outside its scope. **Never use bare "out of scope" language.** Instead, always provide a pointer:

- **If an article already exists** — link by ID and title: `see RC-FD-07 — Field Embedding`
- **If an article is planned** — use the *(coming soon)* flag: `see RC-BL-05 — Branching Logic in Longitudinal Projects *(coming soon)*`
- **If no article exists and none is planned** — add an entry to `KB-GAPS-TODO.md` (repo root) first, then use the *(coming soon)* flag with the new planned ID.

To check whether a topic is already planned, read `KB-GAPS-TODO.md` (repo root) before writing the scope sections of the article. Do not leave scope callouts without a pointer.

---

## Style rules

- **Terminology**: Use REDCap's canonical terms. "Instrument" not "form" or "survey" unless distinguishing. "Variable" not "field" unless quoting the UI.
- **Voice**: Direct, instructional. No filler phrases ("It's important to note that...").
- **Tables**: Use for reference content with 3+ rows. Don't use tables for 2-item comparisons — prose is cleaner.
- **Notes and warnings**: Use blockquotes (`> **Note:**`, `> **Important:**`, `> **Critical:**`) for callouts.
- **Version caveats**: Use a `> **Version caveat:**` blockquote placed immediately after the content it qualifies — see above.
- **Cross-references**: Markdown links with both the article ID and full title: `[RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)`
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

## Institutional policy section

If the article touches on behavior that varies by institution (e.g., Production mode approval workflows, administrator intervention policies, local support contacts), add a clearly marked callout box at the relevant point:

```
> **Institution-specific:** [Describe what varies between installations — e.g. whether the
> feature is enabled, who approves the step — and tell the reader to check with their
> REDCap administrators. Do not name any institution, server or URL.]
```

This is the KB's standard callout (see `PROJECT-TODO.md`). It marks where local policy matters without putting any one institution's values into the KB. Actual local values belong only in the `RC-INST-*` articles. Never write a named-institution callout (e.g. "Yale-specific").

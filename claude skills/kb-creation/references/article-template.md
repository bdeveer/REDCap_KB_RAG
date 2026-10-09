# KB Article Template

Copy this skeleton for every new article. It matches the format of the current corpus (checked against RC-BL-02 and RC-CC-25, 2026-10). When in doubt, open a recent article in `kb/` and match it.

Placeholders are in `[brackets]`. Everything else is literal.

````markdown
**[Domain Name] — [Article Title]**

| **Article ID** | [RC-[DOMAIN]-[NN] — [Domain Name]: [Article Title]](RC-[DOMAIN]-[NN]_[File-Title].md) |
|---|---|
| **Domain** | [Full domain name, e.g. Branching Logic] |
| **Applies To** | [Project types, audience, required user rights — never a version] |
| **Requires** | [REDCap vX.Y.Z+ — earliest version with the feature — or "Any supported version"] |
| **Verified Against** | [REDCap vX.Y.Z (Standard) / vX.Y.Z (LTS) — how it was verified; see writing-rules.md] |
| **Prerequisite** | [[RC-XX-NN — Title](RC-XX-NN_File.md) — or "None"] |
| **Version** | 1.0 |
| **Last Updated** | [YYYY-MM] |
| **Author** | [See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md) |
| **Related Topics** | [[RC-XX-NN — Title](RC-XX-NN_File.md); [RC-XX-NN — Title](RC-XX-NN_File.md)] |
| **Synonyms** | [6–10 lowercase, semicolon-separated search phrasings — see writing-rules.md] |

---

## 1. Overview

[One paragraph. Plain-language description of what this article covers, written for someone who has never opened REDCap. State the series it belongs to, if any.]

---

## 2. Key Concepts & Definitions

**[Term]**

[Definition as REDCap uses it. Note where REDCap's terminology differs from common usage.]

**[Term]**

[Definition.]

---

## 3. [Topic-specific title — not always "Procedure"]

### 3.1 [Sub-task]

[Steps, reference tables, or structured explanation.]

---

## [4–N-3. Additional content sections as needed]

---

## [N-2]. Common Questions

**Q: [Question phrased exactly as a user would ask it]**

**A:** [Direct, complete answer.]

[At least 5 Q&A pairs.]

---

## [N-1]. Common Mistakes & Gotchas

- [Bold-lead or plain lead phrase]: [what the user does wrong] — [what happens] — [how to prevent or recover].

[At least 3 entries.]

---

## [N]. Related Articles

- [RC-XX-NN — Title](RC-XX-NN_File.md) (prerequisite)

- [RC-XX-NN — Title](RC-XX-NN_File.md) ([why it's related])
````

## Format rules the corpus follows

- **Title line:** bold, above the table, `**[Domain] — [Title]**`.
- **Header table:** no `Field | Value` header row. The first row is the Article ID with a self-link; every key is bold.
- **Author** is always `[See KB-SOURCE-ATTESTATION.md](KB-SOURCE-ATTESTATION.md)`.
- **Last Updated** is `YYYY-MM`.
- **Cross-references** are markdown links with the full ID and title: `[RC-BL-02 — Branching Logic: Syntax & Atomic Statements](RC-BL-02_Branching-Logic-Syntax-and-Atomic-Statements.md)`. Bare IDs are converted by `add_crosslinks.py`, but write the link form directly where you can.
- **Sections** are `## N. Title`, numbered, with `---` between them.
- **Definitions** in Section 2 are bold paragraphs, not headings.
- **Q&A** uses `**Q: …**` then `**A:** …`.

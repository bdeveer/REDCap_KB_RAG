# KB-REFERENCE-MAP.md — Moved

This file has been split into three files in `meta/` to reduce token overhead:

| File | Contents | When to load |
|---|---|---|
| `meta/KB-INDEX.md` | Article index table (ID → Title → Filename) | Always — for topic lookup and navigation |
| `meta/KB-KEYWORD-MAP.md` | Keyword and synonym map (user phrasings → domain or article ID) | When topic doesn't map obviously to a domain name |
| `meta/KB-CROSS-REFS.md` | Per-article prerequisites, outbound & inbound links, changelog | Only when building or updating articles |

Please update any references to `kb/KB-REFERENCE-MAP.md` to use the appropriate file(s) above.

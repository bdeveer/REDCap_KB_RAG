#!/usr/bin/env python3
"""
add_crosslinks.py — Convert bare RC-XX-XX article ID references in kb/ articles
into working markdown hyperlinks.

Usage:
    python add_crosslinks.py           # dry run: prints what would change
    python add_crosslinks.py --apply   # writes changes to files

Strategy:
  - In table rows (lines starting with |) and list items (lines starting with - / * / number):
      Matches "RC-XX-XX — any title text" up to the next hard delimiter (; | newline).
      Consumes whatever title text is present regardless of whether it matches the
      canonical title, and replaces the whole thing with the canonical link.
  - In body text:
      Matches "RC-XX-XX — canonical title" exactly, then falls back to bare "RC-XX-XX".
      This avoids accidentally consuming surrounding sentence words.

Safe to re-run: already-linked IDs (inside [...]) are not double-linked.
"""

import os
import re
import sys

# Windows consoles default to cp1252, which cannot print the symbols in the progress output.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

KB_DIR = "kb"
INDEX_FILE = "meta/KB-INDEX.md"
APPLY = "--apply" in sys.argv

# ── 1. Build ID → (title, filename) map from KB-INDEX.md ──────────────────────

id_map = {}

with open(INDEX_FILE, encoding="utf-8") as fh:
    for line in fh:
        m = re.match(r'\|\s*(RC-[A-Z0-9-]+)\s*\|\s*(.+?)\s*\|\s*(RC-\S+\.md)\s*\|', line)
        if m:
            id_map[m.group(1).strip()] = (m.group(2).strip(), m.group(3).strip())

print(f"Loaded {len(id_map)} article IDs from {INDEX_FILE}")

# Sort longest IDs first to avoid partial matches (e.g. RC-NAV-UI before RC-NAV)
sorted_ids = sorted(id_map.keys(), key=len, reverse=True)

# ── 2. Pattern builders ────────────────────────────────────────────────────────

def structured_pattern(article_id):
    """
    For table rows and list items: match the ID + optional ' — title text'.
    The title text stops at a hard delimiter (; | [ newline end-of-string), a
    backtick, a second em dash ("ID — Title — why it's related") or a sentence
    end, so annotations and following sentences are never consumed.
    """
    eid = re.escape(article_id)
    return re.compile(
        rf'(?<!\[)(?<!\]\()'
        rf'({eid}(?:\s*[—\-]{{1,2}}\s*[^;\|\n\[\]`—]+?)?)'
        rf'(?!\])'
        rf'(?=\s*(?:[;\|\n\[`—]|\.\s|\.$)|$)'
    )

def body_pattern(article_id, title):
    """
    For body text: match 'ID — canonical title' exactly, or bare 'ID'.
    Avoids consuming surrounding sentence words.
    """
    eid = re.escape(article_id)
    etitle = re.escape(title)
    return re.compile(
        rf'(?<!\[)(?<!\]\()({eid}(?:\s*[—\-]{{1,2}}\s*{etitle})?)(?!\])'
    )

# Pre-compile patterns for all IDs
structured_patterns = [
    (aid, id_map[aid][0], id_map[aid][1], structured_pattern(aid))
    for aid in sorted_ids
]
body_patterns = [
    (aid, id_map[aid][0], id_map[aid][1], body_pattern(aid, id_map[aid][0]))
    for aid in sorted_ids
]

# ── 3. Linkify a single line ───────────────────────────────────────────────────

# Cleans up orphaned " — Title Text" fragments left after an article link,
# e.g. "[RC-API-03 — Import Records API](url) — Import Records" → "[...](url)".
# Only a fragment that repeats (part of) the link's own title is removed; any
# other text after a link is an annotation ("— why it's related") and is kept.
ORPHAN_CLEANUP = re.compile(
    r'\[(RC-[A-Z0-9-]+) — ([^\]]+)\]\(([^)]+\.md)\)'  # [ID — Title](file.md)
    r'(\s*[—\-]{1,2}\s*([^;\|\n\[\](—]*))'             # " — fragment"
)

def _drop_repeated_title(m):
    title, fragment = m.group(2), m.group(5).strip().rstrip('.')
    if fragment and fragment.lower() in title.lower():
        return m.group(0)[: m.start(4) - m.start(0)]
    return m.group(0)

# Backticked IDs (`RC-XX-NN` or `RC-XX-NN — Title`) become plain links; the
# backticks would otherwise render the link as code.
BACKTICK_ID = re.compile(r'`(RC-[A-Z]+(?:-[A-Z]+)?-\d{2})(?: — [^`]*)?`')

def linkify_line(line, current_file=None):
    is_table = line.strip().startswith('|')
    is_list  = bool(re.match(r'^(?:[-*+]\s|\d+\.\s)', line.strip()))

    line = BACKTICK_ID.sub(
        lambda m: (f"[{m.group(1)} — {id_map[m.group(1)][0]}]({id_map[m.group(1)][1]})"
                   if m.group(1) in id_map and id_map[m.group(1)][1] != current_file
                   else m.group(0)),
        line,
    )

    if is_table or is_list:
        patterns = structured_patterns
    else:
        patterns = body_patterns

    for aid, title, filename, pat in patterns:
        # Skip self-referencing links (don't link an article to itself)
        if current_file and filename == current_file:
            continue
        line = pat.sub(
            lambda m, a=aid, t=title, f=filename: f"[{a} — {t}]({f})",
            line
        )

    # Remove orphaned " — Title" fragments left after article links,
    # but only in table rows and list items where we know the context is safe.
    if is_table or is_list:
        line = ORPHAN_CLEANUP.sub(_drop_repeated_title, line)

    return line

# ── 4. Process each file ───────────────────────────────────────────────────────

skip_files = {"KB-REFERENCE-MAP.md", "index.md", "KB-SOURCE-ATTESTATION.md"}
changed_files = []

for fname in sorted(os.listdir(KB_DIR)):
    if not fname.endswith(".md") or fname in skip_files:
        continue

    fpath = os.path.join(KB_DIR, fname)
    with open(fpath, encoding="utf-8") as fh:
        original = fh.read()

    lines = original.split("\n")
    new_lines = []
    in_code_block = False

    for line in lines:
        if re.match(r'^\s*(`{3,}|~{3,})', line):
            in_code_block = not in_code_block
        if in_code_block:
            new_lines.append(line)
        else:
            new_lines.append(linkify_line(line, current_file=fname))

    updated = "\n".join(new_lines)

    if updated != original:
        changed_files.append(fname)
        if APPLY:
            with open(fpath, "w", encoding="utf-8") as fh:
                fh.write(updated)

# ── 5. Report ──────────────────────────────────────────────────────────────────

mode = "APPLIED" if APPLY else "DRY RUN"
print(f"\n[{mode}] {len(changed_files)} files would be/were updated:\n")
for f in changed_files:
    print(f"  {f}")

if not APPLY:
    print("\nRun with --apply to write changes.")

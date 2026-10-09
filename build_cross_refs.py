#!/usr/bin/env python3
"""Regenerate meta/KB-CROSS-REFS.md from the articles in kb/.

For every article listed in meta/KB-INDEX.md (in index order) the file records:
  - Prerequisites : the IDs in the article's **Prerequisite** header row
  - Outbound links: every markdown link to another RC-*.md article, anywhere in
                    the article (same edge rule as build_dependency_graph.py)
  - Inbound links : every article that links to this one

Titles always come from KB-INDEX.md, so renaming an article there renames it
everywhere here. Hand-written notes in parentheses after a list entry, e.g.
"- RC-FD-06 — Online Designer … (alignment codes cross-reference)", are carried
over from the previous version of the file as long as that link still exists.

Run from anywhere; paths are resolved relative to this script.
Usage:  python build_cross_refs.py           # rewrite meta/KB-CROSS-REFS.md
        python build_cross_refs.py --check   # exit 1 if the file is out of date
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

# Windows consoles default to cp1252, which cannot print the symbols in the output.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
KB_DIR = ROOT / "kb"
INDEX_FILE = ROOT / "meta" / "KB-INDEX.md"
OUT_FILE = ROOT / "meta" / "KB-CROSS-REFS.md"
ID = r"RC-[A-Z]+(?:-[A-Z]+)?-\d{2}"

HEADER = """# REDCap KB Cross-References

Per-article prerequisites, outbound links, and inbound links for all KB articles. Load this file only when building or updating articles that require cross-reference awareness. For topic lookup and navigation, use `meta/KB-INDEX.md` instead.

> **Generated file — do not edit by hand.** Run `python build_cross_refs.py` from the repo root after adding or editing articles. Links and titles come from the articles and `meta/KB-INDEX.md`; a note in parentheses after an entry is preserved while that link exists.

---
"""


def load_index():
    order, titles, files = [], {}, {}
    for line in INDEX_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(rf"\|\s*({ID})\s*\|\s*(.+?)\s*\|\s*(RC-\S+\.md)\s*\|", line)
        if m:
            aid, title, fname = m.groups()
            order.append(aid)
            titles[aid] = title
            files[aid] = fname
    return order, titles, files


def scan_articles(order, files):
    outbound, prereqs = {}, {}
    for aid in order:
        path = KB_DIR / files[aid]
        if not path.exists():
            print(f"  WARNING: {files[aid]} is in KB-INDEX.md but not in kb/", file=sys.stderr)
            outbound[aid], prereqs[aid] = [], []
            continue
        text = path.read_text(encoding="utf-8")
        links = []
        for target in re.findall(rf"\]\(({ID})_[^)\s]*\.md\)", text):
            if target != aid and target not in links:
                links.append(target)
        outbound[aid] = links
        m = re.search(r"^\|\s*\*\*Prerequisite\*\*\s*\|(.*)\|\s*$", text, re.M)
        found = re.findall(ID, m.group(1)) if m else []
        prereqs[aid] = [p for i, p in enumerate(found) if p != aid and p not in found[:i]]
    return outbound, prereqs


def load_notes(titles):
    """Map (article, 'out'|'in', other_id) -> note text from the existing file.

    A note is a trailing "(...)" that is not part of the linked article's own
    title — some titles end in parentheses, e.g. "... Reporting (Dashboard)".
    """
    notes = {}
    if not OUT_FILE.exists():
        return notes
    text = OUT_FILE.read_text(encoding="utf-8")
    for section in re.split(rf"^### (?={ID} —)", text, flags=re.M)[1:]:
        aid = re.match(ID, section).group(0)
        for kind, label in (("out", "Outbound links"), ("in", "Inbound links")):
            m = re.search(rf"\*\*{label}[^*]*\*\*(.*?)(?=\n\*\*|\n---|\Z)", section, re.S)
            if not m:
                continue
            for line in m.group(1).splitlines():
                line = line.strip()
                lm = re.match(rf"^- ({ID})(?: — (.*))?$", line)
                if not lm or not lm.group(2):
                    continue
                other, rest = lm.group(1), lm.group(2).strip()
                title = titles.get(other, "")
                if title and rest.startswith(title):
                    rest = rest[len(title):].strip()      # current format: title, then note
                elif title and rest == title:
                    rest = ""
                nm = re.search(r"(\([^()]*\))\s*$", rest)
                if nm and not (title and title.endswith(nm.group(1))):
                    notes[(aid, kind, other)] = nm.group(1)
    return notes


def render(order, titles, outbound, prereqs, notes):
    inbound = defaultdict(list)
    for aid in order:
        for target in outbound[aid]:
            inbound[target].append(aid)

    def entry(aid, kind, other):
        title = titles.get(other, "(not in KB-INDEX.md)")
        note = notes.get((aid, kind, other))
        return f"- {other} — {title}" + (f" {note}" if note else "")

    parts = [HEADER]
    for aid in order:
        pre = "; ".join(f"{p} — {titles.get(p, '(not in KB-INDEX.md)')}" for p in prereqs[aid]) or "None"
        out_lines = [entry(aid, "out", o) for o in outbound[aid]] or ["*(none)*"]
        in_ids = [i for i in order if i in inbound[aid]]
        in_lines = [entry(aid, "in", i) for i in in_ids] or ["*(none)*"]
        parts.append(
            f"\n### {aid} — {titles[aid]}\n\n"
            f"**Prerequisites:** {pre}\n\n"
            f"**Outbound links:**\n" + "\n".join(out_lines) + "\n\n"
            f"**Inbound links (referenced by):**\n" + "\n".join(in_lines) + "\n\n---\n"
        )
    return "".join(parts)


def main():
    order, titles, files = load_index()
    outbound, prereqs = scan_articles(order, files)
    content = render(order, titles, outbound, prereqs, load_notes(titles))
    current = OUT_FILE.read_text(encoding="utf-8") if OUT_FILE.exists() else ""
    if "--check" in sys.argv:
        if current != content:
            print("meta/KB-CROSS-REFS.md is out of date — run: python build_cross_refs.py")
            sys.exit(1)
        print("meta/KB-CROSS-REFS.md is up to date.")
        return
    OUT_FILE.write_text(content, encoding="utf-8", newline="\n")
    n_links = sum(len(v) for v in outbound.values())
    print(f"Wrote {OUT_FILE.relative_to(ROOT)}: {len(order)} articles, {n_links} links.")


if __name__ == "__main__":
    main()

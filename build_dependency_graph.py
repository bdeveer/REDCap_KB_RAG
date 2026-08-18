#!/usr/bin/env python3
"""Regenerate the KB dependency graph data embedded in kb_dependency_graph.html.

The graph is a self-contained D3 page with a `const GRAPH_DATA = {...};` block.
This script rebuilds that block from the current contents of kb/ and splices it
back in, leaving the surrounding HTML, CSS and JS untouched. It also rewrites
the `const CAT_COLORS = {...};` block so every category actually used has a
colour (categories with no entry fall through to grey).

Edge rule: every markdown link to another `RC-*.md` article, anywhere in the
article body — not just the Related Topics row. Self-links are dropped and
duplicates collapsed. This matches how the original graph was built.

Usage:  python3 build_dependency_graph.py
"""

import json
import os
import re
import sys
from collections import Counter

KB = "kb"
TARGETS = ["kb/kb_dependency_graph.html", "visualization/kb_dependency_graph.html"]

ARTICLE_ID = re.compile(r"RC-[A-Z]+(?:-[A-Z]+)?-\d+")

# Domain slug -> display category. Keep in step with the Established domain
# slugs table in `claude skills/kb-creation/SKILL.md`.
CATEGORY = {
    "AI": "AI Tools",
    "ALERT": "Alerts & Notifications",
    "API": "API",
    "AT": "Action Tags",
    "AT-EM": "Action Tags",
    "BL": "Branching Logic",
    "CAL": "Calendar",
    "CALC": "Calculations",
    "CC": "Control Center",
    "CDIS": "Clinical Data",
    "DAG": "Data Access Groups",
    "DDE": "Double Data Entry",
    "DDP": "Dynamic Data Pull",
    "DE": "Data Entry",
    "DQ": "Data Quality",
    "DSGN": "Design",
    "EM": "External Modules",
    "EXPRT": "Data Export",
    "FD": "Form Design",
    "FDL": "Form Display Logic",
    "FILE": "File Repository",
    "IMP": "Data Import",
    "INFRA": "Self-Hosting & Releases",
    "INST": "Institution Settings",
    "INTG": "Integrations",
    "LOCK": "Record Locking",
    "LOG": "Logging",
    "LONG": "Longitudinal",
    "MCP": "MCP Server",
    "MLM": "Multi-Language",
    "MOB": "Mobile App",
    "MSG": "Messenger",
    "MYCAP": "MyCap",
    "NAV-REC": "Navigation",
    "NAV-UI": "Navigation",
    "OPS": "Operational Use",
    "PIPE": "Piping & Smart Variables",
    "PLUS": "REDCap+",
    "PROF": "Profile",
    "PROJ": "Project Management",
    "RAND": "Randomization",
    "SENDIT": "Send-It",
    "SURV": "Surveys",
    "TXT": "Texting",
    "USER": "User Rights",
}

COLORS = {
    "API": "#f59e0b",
    "Control Center": "#3b82f6",
    "Piping & Smart Variables": "#10b981",
    "Action Tags": "#8b5cf6",
    "Data Entry": "#06b6d4",
    "Form Design": "#ec4899",
    "Surveys": "#f97316",
    "Data Export": "#84cc16",
    "MyCap": "#14b8a6",
    "Navigation": "#6366f1",
    "Branching Logic": "#a855f7",
    "Clinical Data": "#ef4444",
    "AI Tools": "#22d3ee",
    "User Rights": "#f43f5e",
    "Project Management": "#eab308",
    "Randomization": "#d946ef",
    "Alerts & Notifications": "#fb923c",
    "Calculations": "#4ade80",
    "Data Import": "#60a5fa",
    "Dynamic Data Pull": "#c084fc",
    "Longitudinal": "#34d399",
    "Texting": "#fbbf24",
    "Institution Settings": "#9ca3af",
    "Data Access Groups": "#f87171",
    "Data Quality": "#2dd4bf",
    "Form Display Logic": "#fb7185",
    "Integrations": "#818cf8",
    "Multi-Language": "#86efac",
    "Mobile App": "#fcd34d",
    "External Modules": "#e879f9",
    "Design": "#65a30d",
    "REDCap+": "#facc15",
    "Self-Hosting & Releases": "#94a3b8",
    "MCP Server": "#5eead4",
    "File Repository": "#fda4af",
    "Record Locking": "#a3e635",
    "Logging": "#7dd3fc",
    "Messenger": "#f0abfc",
    "Calendar": "#fcd34d",
    "Double Data Entry": "#bef264",
    "Send-It": "#67e8f9",
    "Profile": "#d8b4fe",
    "Operational Use": "#fdba74",
}


def article_title(text, article_id):
    """Title from the Article ID metadata row: [RC-XX-NN — Title](file.md)."""
    m = re.search(r"\|\s*\*\*Article ID\*\*\s*\|\s*\[" + re.escape(article_id) + r"\s*[—-]\s*(.+?)\]\(", text)
    if m:
        return m.group(1).strip()
    m = re.search(r"^\*\*(.+?)\*\*\s*$", text[:400], re.M)
    return m.group(1).strip() if m else article_id


def build():
    nodes, edges = {}, set()
    for name in sorted(os.listdir(KB)):
        if not (name.startswith("RC-") and name.endswith(".md")):
            continue
        m = ARTICLE_ID.match(name)
        if not m:
            print(f"  ! unparseable filename, skipped: {name}", file=sys.stderr)
            continue
        aid = m.group(0)
        text = open(os.path.join(KB, name), encoding="utf-8").read()
        slug = re.match(r"RC-([A-Z]+(?:-[A-Z]+)?)-\d+", aid).group(1)
        if slug not in CATEGORY:
            print(f"  ! no category for domain slug {slug} ({aid}) — using 'Other'", file=sys.stderr)
        nodes[aid] = {
            "id": aid,
            "label": aid,
            "title": article_title(text, aid),
            "category": CATEGORY.get(slug, "Other"),
        }
        hrefs = " ".join(re.findall(r"\]\(([^)]+\.md)\)", text))
        for tgt in {t.group(0) for t in ARTICLE_ID.finditer(hrefs)} - {aid}:
            edges.add((aid, tgt))

    # Drop edges pointing at articles that no longer exist, and report them.
    dangling = sorted({t for _, t in edges if t not in nodes})
    if dangling:
        print(f"  ! {len(dangling)} link target(s) with no article: {', '.join(dangling)}", file=sys.stderr)
    edges = {(s, t) for s, t in edges if t in nodes}

    ind, outd = Counter(t for _, t in edges), Counter(s for s, _ in edges)
    for aid, n in nodes.items():
        n["inDegree"], n["outDegree"] = ind.get(aid, 0), outd.get(aid, 0)

    data = {
        "nodes": [nodes[k] for k in sorted(nodes)],
        "edges": [{"source": s, "target": t} for s, t in sorted(edges)],
    }
    return data, ind


def splice(path, data):
    html = open(path, encoding="utf-8").read()
    new_graph = "const GRAPH_DATA = " + json.dumps(data, ensure_ascii=False) + ";"
    html, n1 = re.subn(r"const GRAPH_DATA\s*=\s*\{.*?\};", lambda _: new_graph, html, count=1, flags=re.S)
    used = sorted({n["category"] for n in data["nodes"]})
    body = "".join(f'\n  "{c}": "{COLORS.get(c, "#9ca3af")}",' for c in used)
    new_colors = "const CAT_COLORS = {" + body + "\n};"
    html, n2 = re.subn(r"const CAT_COLORS\s*=\s*\{.*?\};", lambda _: new_colors, html, count=1, flags=re.S)
    if not (n1 and n2):
        raise SystemExit(f"ERROR: could not locate GRAPH_DATA ({n1}) / CAT_COLORS ({n2}) in {path}")
    open(path, "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    data, ind = build()
    for path in TARGETS:
        if os.path.exists(path):
            splice(path, data)
            print(f"  updated {path}")
        else:
            print(f"  ! missing, skipped: {path}", file=sys.stderr)
    cats = Counter(n["category"] for n in data["nodes"])
    top = ", ".join(f"{a} ({c})" for a, c in ind.most_common(5))
    print(f"\n{len(data['nodes'])} nodes, {len(data['edges'])} edges, {len(cats)} categories")
    print(f"most linked-to: {top}")
    orphans = [n["id"] for n in data["nodes"] if not n["inDegree"] and not n["outDegree"]]
    print(f"orphans (no links in or out): {', '.join(orphans) if orphans else 'none'}")

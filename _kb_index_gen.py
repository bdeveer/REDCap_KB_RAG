"""
KB Index Generator — called by the KB Browser artifact at runtime.
Scans kb/ and outputs compact JSON for all articles.
"""
import os, re, json

kb = os.path.join(os.environ["HOME"], "mnt/REDCap_KB_RAG/kb")
arts = []

for fname in sorted(os.listdir(kb)):
    if not fname.endswith(".md") or fname == "KB-REFERENCE-MAP.md":
        continue
    path = os.path.join(kb, fname)
    with open(path, encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    aid = ti = dom = ""
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if not aid:
            aid = s
            continue
        if not ti and s.startswith("**") and s.endswith("**"):
            ti = s.strip("*").strip()
            continue
        if "| **Domain**" in line:
            m = re.search(r"\|\s*\*\*Domain\*\*\s*\|\s*(.+?)\s*\|", line)
            if m:
                dom = m.group(1).strip()
        if s == "---" and aid and ti:
            break

    ov = re.search(r"# 1\. Overview\n+(.+?)(?:\n\n|\n#)", content, re.DOTALL)
    sn = ov.group(1).strip().replace("\n", " ")[:160] if ov else ""

    arts.append({"id": aid, "file": fname, "title": ti, "domain": dom, "snippet": sn})

print(json.dumps(arts, separators=(",", ":")))

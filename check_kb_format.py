#!/usr/bin/env python3
"""
KB Article Format Checker
Validates formatting of all RC-* articles in the kb/ directory.

Usage:
    python3 check_kb_format.py                        # check all articles
    python3 check_kb_format.py --article RC-BL-01     # single article
    python3 check_kb_format.py --summary              # totals only
    python3 check_kb_format.py --errors-only          # hide warnings/info
    python3 check_kb_format.py --warnings-only        # hide info lines
"""

import os
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# ── configuration ─────────────────────────────────────────────────────────────

KB_DIR = Path(__file__).parent / "kb"

REQUIRED_META_FIELDS = {
    "Article ID",
    "Domain",
    "Applies To",
    "Version",
    "Last Updated",
    "Author",
}

EXPECTED_LAST_SECTION = "Related Articles"

# Institution-specific patterns to flag (case-insensitive)
INSTITUTION_PATTERNS = [
    r"\byale\b",
    r"\bynhhs\b",
    r"\bynhh\b",
    r"yale\.edu",
    r"ynhhs\.org",
]

# ── data model ────────────────────────────────────────────────────────────────

@dataclass
class Issue:
    severity: str   # "ERROR" | "WARNING" | "INFO"
    line: Optional[int]
    message: str

    def __str__(self):
        loc = f"line {self.line:>4}" if self.line else "      "
        badge = {"ERROR": "✗", "WARNING": "⚠", "INFO": "·"}[self.severity]
        return f"  {badge} {loc}  {self.message}"


@dataclass
class ArticleResult:
    filename: str
    issues: list[Issue] = field(default_factory=list)

    @property
    def errors(self):   return [i for i in self.issues if i.severity == "ERROR"]
    @property
    def warnings(self): return [i for i in self.issues if i.severity == "WARNING"]
    @property
    def infos(self):    return [i for i in self.issues if i.severity == "INFO"]
    @property
    def ok(self):       return len(self.errors) == 0

    def error(self, line, msg):   self.issues.append(Issue("ERROR",   line, msg))
    def warning(self, line, msg): self.issues.append(Issue("WARNING", line, msg))
    def info(self, line, msg):    self.issues.append(Issue("INFO",    line, msg))


# ── helpers ───────────────────────────────────────────────────────────────────

def parse_meta_table(lines: list[str], start: int) -> tuple[dict, int]:
    """Extract key→value from the markdown metadata table starting at `start`."""
    meta = {}
    i = start
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        # Skip pure separator rows: |---|---| or | --- | --- |
        if re.match(r"^\|[\s\-|]+\|$", line):
            i += 1
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) >= 2:
            key = parts[0].strip("*").strip()
            val = parts[1].strip()
            if key:
                meta[key] = val
        i += 1
    return meta, i


def extract_sections(lines: list[str]) -> list[tuple[int, int, str]]:
    """Return (1-based line, section_number, section_name) for every # N. heading."""
    sections = []
    for i, line in enumerate(lines):
        m = re.match(r"^#\s+(\d+)\.\s+(.+)$", line)
        if m:
            sections.append((i + 1, int(m.group(1)), m.group(2).strip()))
    return sections


def has_separator_before(lines: list[str], idx: int) -> bool:
    """
    True if a bare '---' line appears between the PREVIOUS section heading
    and the section heading at idx (0-based). This prevents a short section
    from inheriting the separator that belongs to the section before it.
    """
    # Find the previous # N. section heading before idx
    prev_sec = -1
    for j in range(idx - 1, -1, -1):
        if re.match(r"^#\s+\d+\.", lines[j]):
            prev_sec = j
            break
    search_from = prev_sec + 1 if prev_sec >= 0 else 0
    return any(lines[j].strip() == "---" for j in range(search_from, idx))


# ── per-article checks ────────────────────────────────────────────────────────

def check_article(filepath: Path) -> ArticleResult:
    result = ArticleResult(filepath.name)
    raw = filepath.read_text(encoding="utf-8")
    lines = raw.splitlines()

    if not lines:
        result.error(None, "File is empty")
        return result

    # Expected Article ID from filename (everything before the first underscore)
    expected_id = filepath.stem.split("_")[0]

    # ── 1. Line 1: plain Article ID ──────────────────────────────────────────

    line1 = lines[0].strip()
    if not line1:
        result.error(1, "Line 1 is blank — should be the plain Article ID (e.g. RC-BL-01)")
    elif re.search(r"[*#`_\[\]]", line1):
        result.error(1, f"Line 1 has markdown — should be plain Article ID, got: {line1!r}")
    else:
        # Validate it looks like RC-XXXX-NN (2 or 3 segments)
        if not re.match(r"^RC-[A-Z0-9]+(?:-[A-Z0-9]+)?-\d+$", line1):
            result.warning(1, f"Line 1 doesn't look like a standard Article ID: {line1!r}")
        if line1 != expected_id:
            result.error(1, f"Article ID on line 1 ('{line1}') doesn't match filename ('{expected_id}')")

    # ── 2. Line 2: blank ─────────────────────────────────────────────────────

    if len(lines) < 2 or lines[1].strip() != "":
        result.error(2, "Line 2 should be blank (separator between Article ID and title)")

    # ── 3. Line 3: bold title ────────────────────────────────────────────────

    if len(lines) < 3:
        result.error(3, "File too short — no title on line 3")
    else:
        line3 = lines[2].strip()
        if not (line3.startswith("**") and line3.endswith("**") and len(line3) > 4):
            result.error(3, f"Line 3 should be a bold title (**Title here**), got: {line3!r}")

    # ── 4. Metadata table ────────────────────────────────────────────────────

    # Find first | line in first 10 lines
    table_start = None
    for i in range(3, min(12, len(lines))):
        if lines[i].strip().startswith("|"):
            table_start = i
            break

    if table_start is None:
        result.error(None, "No metadata table found (expected within first 12 lines)")
        table_end = 3
    else:
        meta, table_end = parse_meta_table(lines, table_start)

        # Required fields
        for fname in REQUIRED_META_FIELDS:
            if fname not in meta:
                result.error(table_start + 1, f"Metadata table missing required field: '{fname}'")
            elif not meta[fname]:
                result.warning(table_start + 1, f"Metadata field '{fname}' is empty")

        # Article ID in table must match line 1
        if "Article ID" in meta and line1 and not re.search(r"[*#`\[\]]", line1):
            if meta["Article ID"] != line1:
                result.error(table_start + 1,
                    f"Article ID in table ('{meta['Article ID']}') ≠ line 1 ('{line1}')")

        # Version should be numeric (e.g. 1.0)
        if "Version" in meta and meta["Version"]:
            if not re.match(r"^\d+\.\d+", meta["Version"]):
                result.warning(table_start + 1,
                    f"Version '{meta['Version']}' doesn't look like a version number (e.g. 1.0)")

        # Last Updated should begin with a 4-digit year
        if "Last Updated" in meta and meta["Last Updated"]:
            if not re.match(r"^\d{4}", meta["Last Updated"]):
                result.warning(table_start + 1,
                    f"Last Updated '{meta['Last Updated']}' doesn't start with a 4-digit year")

        # Author should reference attestation file
        if "Author" in meta and meta["Author"]:
            if "KB-SOURCE-ATTESTATION" not in meta["Author"]:
                result.warning(table_start + 1,
                    f"Author field is '{meta['Author']}' — expected reference to KB-SOURCE-ATTESTATION.md")

    # ── 5. Separator (---) between table and first section ──────────────────

    found_sep_after_table = False
    for i in range(table_end, min(table_end + 5, len(lines))):
        if lines[i].strip() == "---":
            found_sep_after_table = True
            break

    if not found_sep_after_table:
        result.error(table_end + 1,
            "No '---' separator found between metadata table and first section")

    # ── 6. Numbered sections ─────────────────────────────────────────────────

    sections = extract_sections(lines)

    if not sections:
        result.error(None, "No numbered sections found (expected '# 1. Overview' etc.)")
    else:
        # Section 1 must be Overview
        if sections[0][1] != 1:
            result.error(sections[0][0],
                f"First section number is {sections[0][1]}, expected 1")
        if sections[0][2].lower() != "overview":
            result.warning(sections[0][0],
                f"Section 1 is named '{sections[0][2]}' — expected 'Overview'")

        # Check sequential numbering
        prev_num = sections[0][1]
        for j in range(1, len(sections)):
            curr_num = sections[j][1]
            curr_line = sections[j][0]
            curr_name = sections[j][2]
            if curr_num == prev_num:
                result.error(curr_line,
                    f"Duplicate section number {curr_num} ('{curr_name}') — two sections share the same number")
            elif curr_num > prev_num + 1:
                result.warning(curr_line,
                    f"Section numbering skips from {prev_num} to {curr_num} ('{curr_name}') — section {prev_num + 1} is missing")
            prev_num = curr_num

        # Last section should be Related Articles
        last_num, last_name = sections[-1][1], sections[-1][2]
        if last_name.lower() != EXPECTED_LAST_SECTION.lower():
            result.warning(sections[-1][0],
                f"Last section is '{last_name}' — expected '{EXPECTED_LAST_SECTION}'")

    # ── 7. --- separators before each section ────────────────────────────────

    for sec_line, sec_num, sec_name in sections:
        idx = sec_line - 1  # 0-based
        if not has_separator_before(lines, idx):
            result.warning(sec_line,
                f"No '---' separator found before section {sec_num} ('{sec_name}')")

    # ── 8. Q&A format in Common Questions section ────────────────────────────

    cq_start_idx = None
    for sec_line, sec_num, sec_name in sections:
        if re.search(r"common.question|q\s*&\s*a|faq", sec_name, re.IGNORECASE):
            cq_start_idx = sec_line - 1  # 0-based
            break

    if cq_start_idx is not None:
        # End of section: next --- or next numbered section
        cq_end_idx = len(lines)
        for i in range(cq_start_idx + 1, len(lines)):
            if lines[i].strip() == "---" or re.match(r"^#\s+\d+\.", lines[i]):
                cq_end_idx = i
                break

        for i in range(cq_start_idx, cq_end_idx):
            stripped = lines[i].strip()
            lo = stripped.lower()
            # Q lines
            if lo.startswith("q:") or lo.startswith("**q:"):
                if not stripped.startswith("**Q:"):
                    result.warning(i + 1,
                        f"Q line should start with '**Q:' — got: {stripped[:60]!r}")
            # A lines
            if lo.startswith("a:") or lo.startswith("**a:"):
                if not stripped.startswith("**A:**"):
                    result.warning(i + 1,
                        f"A line should start with '**A:**' — got: {stripped[:60]!r}")

    # ── 9. Institution-specific content ──────────────────────────────────────

    for i, line in enumerate(lines):
        for pattern in INSTITUTION_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                result.warning(i + 1,
                    f"Possible institution-specific reference: {line.strip()[:80]!r}")
                break

    # ── 10. Bare external URLs in body text (informational) ──────────────────

    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            continue  # skip metadata table rows
        clean = re.sub(r"`[^`]*`", "", line)  # strip inline code
        if re.search(r"https?://", clean):
            result.info(i + 1,
                f"URL in body text: {line.strip()[:80]!r}")

    return result


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Check KB article formatting")
    parser.add_argument("--article", "-a",
        help="Check a single article by ID prefix (e.g. RC-BL-01)")
    parser.add_argument("--summary", "-s", action="store_true",
        help="Print totals only — no per-article detail")
    parser.add_argument("--errors-only", "-e", action="store_true",
        help="Show only ERROR-level issues")
    parser.add_argument("--warnings-only", "-w", action="store_true",
        help="Show ERRORs and WARNINGs but not INFO")
    args = parser.parse_args()

    if not KB_DIR.exists():
        print(f"ERROR: kb/ directory not found at {KB_DIR}")
        sys.exit(1)

    # Only check RC-* articles (skip meta files like KB-REFERENCE-MAP)
    all_files = sorted(f for f in KB_DIR.glob("RC-*.md"))

    if args.article:
        all_files = [f for f in all_files if f.stem.startswith(args.article)]
        if not all_files:
            print(f"No articles found matching '{args.article}'")
            sys.exit(1)

    results: list[ArticleResult] = []
    for filepath in all_files:
        results.append(check_article(filepath))

    # ── output ────────────────────────────────────────────────────────────────

    if not args.summary:
        for r in results:
            if args.errors_only:
                visible = r.errors
            elif args.warnings_only:
                visible = r.errors + r.warnings
            else:
                visible = r.issues

            if not visible:
                continue

            status = "FAIL" if r.errors else ("WARN" if r.warnings else "INFO")
            colours = {"FAIL": "✗", "WARN": "⚠", "INFO": "·"}
            print(f"\n{colours[status]} {r.filename}")
            for issue in visible:
                print(str(issue))

        print()

    # ── summary ───────────────────────────────────────────────────────────────

    total    = len(results)
    failed   = [r for r in results if r.errors]
    warned   = [r for r in results if not r.errors and r.warnings]
    info_only= [r for r in results if not r.errors and not r.warnings and r.infos]
    clean    = [r for r in results if not r.issues]

    print("─" * 62)
    print(f"  Articles checked  : {total}")
    print(f"  ✗ Errors (fail)   : {len(failed)}")
    print(f"  ⚠ Warnings only   : {len(warned)}")
    print(f"  · Info only       : {len(info_only)}")
    print(f"  ✓ Fully clean     : {len(clean)}")
    print("─" * 62)

    if failed:
        print(f"\nFailing articles ({len(failed)}):")
        for r in failed:
            ec = len(r.errors)
            wc = len(r.warnings)
            print(f"  {r.filename:<65}  {ec} error(s), {wc} warning(s)")

    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()

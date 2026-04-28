#!/usr/bin/env python3
"""
KB Article Format Fixer
Automatically fixes formatting errors and common warnings found by check_kb_format.py

Fixes applied:
  1. Insert --- before each # N. section heading if not already present
     (also fixes the missing separator between metadata table and first section)
  2. Renumber # N. section headings sequentially from 1 if out of order or
     containing duplicates; update ## N.M subsection numbers to match
  3. Fix Q&A answer lines: 'A: ...' → '**A:** ...' in Common Questions sections

Usage:
    python3 fix_kb_format.py               # fix all RC-* articles (dry run first)
    python3 fix_kb_format.py --dry-run     # show what would change, don't write
    python3 fix_kb_format.py --article RC-RAND-01   # single article
    python3 fix_kb_format.py --write       # actually write fixes
"""

import re
import sys
import argparse
from pathlib import Path

KB_DIR = Path(__file__).parent / "kb"


# ── section renumbering ───────────────────────────────────────────────────────

def build_renaming_map(lines: list[str]) -> dict[int, str]:
    """
    Returns {line_index: new_line_content} for all headings that need renaming.
    Covers # N. section headings and ## N.M subsection headings.
    """
    # Collect all # N. section headings in file order
    sections = []  # (line_idx, old_num, name)
    for i, line in enumerate(lines):
        m = re.match(r'^#\s+(\d+)\.\s+(.+)$', line)
        if m:
            sections.append((i, int(m.group(1)), m.group(2).rstrip()))

    if not sections:
        return {}

    old_nums = [s[1] for s in sections]
    new_nums = list(range(1, len(sections) + 1))

    if old_nums == new_nums:
        return {}  # Already correct — nothing to do

    result: dict[int, str] = {}

    for j, (line_idx, old_num, name) in enumerate(sections):
        new_num = new_nums[j]

        # Update # N. heading if number changed
        if old_num != new_num:
            result[line_idx] = f"# {new_num}. {name}"

        # Determine line range for this section (up to next section heading or EOF)
        sec_end = sections[j + 1][0] if j + 1 < len(sections) else len(lines)

        # Update ## N.M subsections within this section's range
        for i in range(line_idx + 1, sec_end):
            m = re.match(r'^(##)\s+(\d+)\.(\d+)(.*?)$', lines[i])
            if m:
                sub_parent_old = int(m.group(2))
                sub_idx = m.group(3)
                rest = m.group(4)
                # Only update if the parent number matches this section's old number
                # (safety: don't touch subsections that belong to a different parent)
                if sub_parent_old == old_num and old_num != new_num:
                    result[i] = f"## {new_num}.{sub_idx}{rest}"

            # Handle ### N.M.P if present
            m3 = re.match(r'^(###)\s+(\d+)\.(\d+)\.(\d+)(.*?)$', lines[i])
            if m3:
                sub_parent_old = int(m3.group(2))
                sub_mid = m3.group(3)
                sub_leaf = m3.group(4)
                rest = m3.group(5)
                if sub_parent_old == old_num and old_num != new_num:
                    result[i] = f"### {new_num}.{sub_mid}.{sub_leaf}{rest}"

    return result


def apply_renaming(lines: list[str], rename_map: dict[int, str]) -> list[str]:
    return [rename_map.get(i, line) for i, line in enumerate(lines)]


# ── separator insertion ───────────────────────────────────────────────────────

def fix_separators(lines: list[str]) -> list[str]:
    """
    Ensures a bare '---' line appears immediately before every # N. section heading.
    Pattern after fix:  ...content\n\n---\n\n# N. Name\n...

    Looks for --- only since the LAST section heading (not a fixed window),
    so short sections don't borrow the previous section's separator.
    """
    new_lines: list[str] = []

    for line in lines:
        is_section = bool(re.match(r'^#\s+\d+\.', line))

        if is_section:
            # Find the position of the most recent section heading in new_lines
            last_sec_pos = -1
            for j in range(len(new_lines) - 1, -1, -1):
                if re.match(r'^#\s+\d+\.', new_lines[j]):
                    last_sec_pos = j
                    break
            # Check for --- anywhere after that position
            search_from = last_sec_pos + 1 if last_sec_pos >= 0 else 0
            has_sep = any(new_lines[j].strip() == '---'
                          for j in range(search_from, len(new_lines)))

            if not has_sep:
                # Strip trailing blank lines from buffer
                while new_lines and new_lines[-1].strip() == '':
                    new_lines.pop()
                new_lines.append('')
                new_lines.append('---')
                new_lines.append('')

        new_lines.append(line)

    return new_lines


# ── Q&A answer formatting ─────────────────────────────────────────────────────

def fix_qa_format(lines: list[str]) -> list[str]:
    """
    In 'Common Questions' (and 'Questions & Answers') sections, fix:
      A: ...    →  **A:** ...
    Only touches lines that start with bare 'A: ' (not already bolded).
    """
    # Identify Q&A section ranges
    qa_ranges: list[tuple[int, int]] = []
    section_boundaries: list[int] = []

    for i, line in enumerate(lines):
        if re.match(r'^#\s+\d+\.', line):
            section_boundaries.append(i)

    for j, start_idx in enumerate(section_boundaries):
        line = lines[start_idx]
        m = re.match(r'^#\s+\d+\.\s+(.+)$', line)
        if m:
            name = m.group(1).strip()
            if re.search(r'common.question|question.+answer|q\s*&\s*a|faq', name, re.IGNORECASE):
                end_idx = section_boundaries[j + 1] if j + 1 < len(section_boundaries) else len(lines)
                qa_ranges.append((start_idx, end_idx))

    if not qa_ranges:
        return lines

    in_qa = set()
    for start, end in qa_ranges:
        for i in range(start, end):
            in_qa.add(i)

    new_lines = []
    for i, line in enumerate(lines):
        if i in in_qa:
            # Fix 'A: ...' (not already '**A:**')
            m = re.match(r'^A:\s+(.+)$', line)
            if m and not line.startswith('**A:**'):
                line = f"**A:** {m.group(1)}"
        new_lines.append(line)

    return new_lines


# ── per-article fix ───────────────────────────────────────────────────────────

def fix_article(filepath: Path, dry_run: bool = True) -> tuple[bool, list[str]]:
    """
    Apply all fixes to one article.
    Returns (changed: bool, diff_summary: list[str]).
    """
    original = filepath.read_text(encoding='utf-8')
    lines = original.splitlines()

    # Step 1: Renumber sections (also fixes API duplicate # 3. and RAND starts-at-2)
    rename_map = build_renaming_map(lines)
    lines = apply_renaming(lines, rename_map)

    # Step 2: Insert missing --- separators before section headings
    lines = fix_separators(lines)

    # Step 3: Fix Q&A answer formatting
    lines = fix_qa_format(lines)

    new_content = '\n'.join(lines)
    # Ensure single trailing newline
    new_content = new_content.rstrip('\n') + '\n'

    changed = (new_content != original)

    diff_summary = []
    if changed:
        if rename_map:
            diff_summary.append(f"  • Renumbered {len(rename_map)} section/subsection heading(s)")
        orig_lines = original.splitlines()
        new_lines = new_content.splitlines()
        added_seps = sum(
            1 for l in new_lines if l.strip() == '---'
        ) - sum(1 for l in orig_lines if l.strip() == '---')
        if added_seps > 0:
            diff_summary.append(f"  • Added {added_seps} missing '---' separator(s)")
        fixed_qa = sum(
            1 for new, old in zip(new_lines, orig_lines + [''] * 9999)
            if new.startswith('**A:**') and old.startswith('A:')
        )
        if fixed_qa > 0:
            diff_summary.append(f"  • Fixed {fixed_qa} Q&A answer line(s) (A: → **A:**)")

    if not dry_run and changed:
        filepath.write_text(new_content, encoding='utf-8')

    return changed, diff_summary


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fix KB article formatting")
    parser.add_argument('--article', '-a',
        help="Fix a single article by ID prefix (e.g. RC-BL-02)")
    parser.add_argument('--write', '-w', action='store_true',
        help="Write fixes to disk (default is dry-run / preview only)")
    parser.add_argument('--dry-run', '-d', action='store_true',
        help="Preview changes without writing (same as default, explicit flag)")
    args = parser.parse_args()

    dry_run = not args.write

    if not KB_DIR.exists():
        print(f"ERROR: kb/ directory not found at {KB_DIR}")
        sys.exit(1)

    all_files = sorted(f for f in KB_DIR.glob("RC-*.md"))

    if args.article:
        all_files = [f for f in all_files if f.stem.startswith(args.article)]
        if not all_files:
            print(f"No articles found matching '{args.article}'")
            sys.exit(1)

    if dry_run:
        print("DRY RUN — no files will be written. Use --write to apply fixes.\n")

    changed_count = 0
    unchanged_count = 0

    for filepath in all_files:
        changed, summary = fix_article(filepath, dry_run=dry_run)
        if changed:
            changed_count += 1
            verb = "Would fix" if dry_run else "Fixed"
            print(f"{'→' if dry_run else '✓'} {filepath.name}")
            for line in summary:
                print(line)
        else:
            unchanged_count += 1

    print()
    print("─" * 60)
    if dry_run:
        print(f"  Would modify : {changed_count} article(s)")
        print(f"  Already OK   : {unchanged_count} article(s)")
        print()
        print("  Run with --write to apply all fixes.")
    else:
        print(f"  Fixed        : {changed_count} article(s)")
        print(f"  Already OK   : {unchanged_count} article(s)")
    print("─" * 60)


if __name__ == '__main__':
    main()

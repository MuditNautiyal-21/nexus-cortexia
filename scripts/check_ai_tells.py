#!/usr/bin/env python3
"""
check_ai_tells.py

Scans all markdown files in the repo for common AI-writing tells (based on
the humanizer skill patterns). Exits non-zero if any are found so CI can
gate on it.

The patterns here aren't exhaustive. They're the tells most often flagged
by reviewers, including em-dash overuse, "not X, but Y" negative parallels,
and a short list of AI vocabulary. Edit this list as new patterns become
noticeable.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS: list[tuple[str, str]] = [
    # em dash (U+2014) - flagged as overuse regardless of context per project policy
    (r"\u2014", "em dash (U+2014) found; prefer comma, colon, parentheses, or sentence break"),
    # Classic AI vocabulary
    (r"\bleverage(d|s|ing)?\b", "'leverage' as verb is an AI tell; use 'use' or 'apply'"),
    (r"\bdelve(d|s|ing)?\s+into\b", "'delve into' is an AI tell"),
    (r"\bnavigate(d|s|ing)?\s+(the|through)\b", "'navigate the' is an AI tell"),
    (r"\bin\s+today's\s+(fast-paced|rapidly|ever-)", "puffy opener"),
    (r"\bit\s+is\s+important\s+to\s+note\b", "empty transition phrase"),
    (r"\bin\s+conclusion,?\s", "essay-style closer"),
    (r"\btapestry\b", "AI metaphor tell"),
    (r"\bmeticulous(ly)?\b", "AI intensifier"),
    (r"\bseamless(ly)?\b", "AI marketing word"),
    (r"\brobust(ly)?\b", "AI marketing word (in most uses)"),
    (r"\bcomprehensive(ly)?\b", "AI marketing word (in most uses)"),
    # Negative parallelism
    (r"\bnot\s+just\s+\w+,?\s+but\s+", "'not just X but Y' parallelism"),
    (r"\bnot\s+only\s+\w+.{0,40}\bbut\s+also\b", "'not only X but also Y' parallelism"),
    # Rule-of-three tell: short single-word triple as a sentence or
    # sentence opener (e.g. "Fast, reliable, and scalable."). Normal
    # listing with phrases containing spaces or longer clauses is fine.
    (r"(^|\.\s+)[A-Z][a-z]{2,15},\s+[A-Za-z]{2,15},\s+and\s+[A-Za-z]{2,15}\.", "rule-of-three adjective triple"),
]

SKIP_PATHS = {".git", "node_modules", ".github/ISSUE_TEMPLATE"}

# Intentional exceptions per file. Keys are relative paths, values are
# lists of (pattern substring, note) this file is allowed to contain.
EXCEPTIONS: dict[str, list[str]] = {
    # check_ai_tells.py itself is documentation about the patterns
    "scripts/check_ai_tells.py": [
        "em dash",
        "leverage",
        "delve",
        "navigate",
        "tapestry",
        "meticulous",
        "seamless",
        "robust",
        "comprehensive",
        "not just X",
        "not only X",
        "rule-of-three",
    ],
}


def should_skip(path: Path) -> bool:
    parts = path.parts
    return any(skip in parts for skip in SKIP_PATHS)


def check_file(path: Path) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return hits
    rel = str(path.relative_to(Path.cwd())) if path.is_absolute() else str(path)
    allowed = EXCEPTIONS.get(rel, [])
    for i, line in enumerate(text.splitlines(), start=1):
        for pattern, note in PATTERNS:
            if re.search(pattern, line):
                if any(a in note for a in allowed):
                    continue
                hits.append((i, line.rstrip(), note))
    return hits


def main() -> int:
    root = Path.cwd()
    total = 0
    for md in root.rglob("*.md"):
        if should_skip(md):
            continue
        hits = check_file(md)
        if hits:
            rel = md.relative_to(root)
            print(f"\n{rel}:")
            for line_no, line, note in hits:
                print(f"  line {line_no}: {note}")
                print(f"    > {line}")
            total += len(hits)
    if total:
        print(f"\n{total} AI-tell hit(s) across the repo. Clean them up or add to EXCEPTIONS.")
        return 1
    print("No AI tells found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

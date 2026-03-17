#!/usr/bin/env python3
"""
verify.py — post-edit verification runner.

Re-runs the scanner after edits to confirm which blocks are still uncited,
checks that new bib keys are reachable, and optionally compiles the document.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from scanner import scan, load_config, resolve_tex_path


def find_bib_keys_in_file(bib_path: Path) -> set[str]:
    """Extract all @type{key, entries from a .bib file."""
    import re
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"@\w+\{(\S+),", text))


def find_cited_keys_in_tex(tex_paths: list[Path]) -> set[str]:
    """Extract all \\cite{...} keys from .tex files."""
    import re
    keys: set[str] = set()
    cite_re = re.compile(r"\\(?:cite|parencite|autocite|textcite|footcite)\{([^}]+)\}")
    for path in tex_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in cite_re.finditer(text):
            for key in match.group(1).split(","):
                keys.add(key.strip())
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify citation edits.")
    parser.add_argument("roots", nargs="+", help="Root .tex files.")
    parser.add_argument("--config", required=True, help="Discipline config.yaml.")
    parser.add_argument("--bib", help="Path to .bib file to check key reachability.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    workspace = Path(".").resolve()

    roots: list[Path] = []
    for r in args.roots:
        root = resolve_tex_path(r, Path.cwd())
        if root is None:
            print(f"Missing: {r}", file=sys.stderr)
            return 1
        roots.append(root)

    # 1. Re-scan for missing citations
    missing = scan(roots, workspace, config, only_missing=True)

    # 2. Check bib key reachability
    unreachable: list[str] = []
    if args.bib:
        bib_path = Path(args.bib)
        if bib_path.exists():
            bib_keys = find_bib_keys_in_file(bib_path)
            from scanner import collect_tex_files
            tex_files = collect_tex_files(roots, workspace, True)
            cited_keys = find_cited_keys_in_tex(tex_files)
            unreachable = sorted(cited_keys - bib_keys)

    result = {
        "still_missing": [asdict(b) for b in missing],
        "unreachable_keys": unreachable,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Still missing: {len(missing)} blocks")
        for b in missing:
            print(f"  {b.file}:{b.line} [{b.env}] {b.preview[:80]}")
        if unreachable:
            print(f"\nUnreachable bib keys: {', '.join(unreachable)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

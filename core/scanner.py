#!/usr/bin/env python3
"""
Citable-block scanner — unified entry point.

Delegates to pluggable scan strategies defined in `strategies/`.
Each strategy yields Block objects that the agent uses to decide
which regions of the manuscript may need citations.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Block:
    """A single citable region detected by a scan strategy."""
    file: str
    line: int
    kind: str        # e.g. "env", "pattern", "section"
    env: str         # environment name or pattern tag
    title: str
    status: str      # "cited" | "missing"
    preview: str


# ---------------------------------------------------------------------------
# Strategy registry
# ---------------------------------------------------------------------------

_STRATEGIES: dict[str, type] = {}


def register_strategy(name: str):
    """Decorator to register a scan strategy class."""
    def decorator(cls):
        _STRATEGIES[name] = cls
        return cls
    return decorator


def load_strategies():
    """Import built-in strategy modules so they self-register."""
    from strategies import env_strategy  # noqa: F401
    # future: pattern_strategy, section_strategy


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(config_path: Path) -> dict:
    text = config_path.read_text(encoding="utf-8")
    return yaml.safe_load(text)


# ---------------------------------------------------------------------------
# File collection (reused from original scan_theorem_like.py)
# ---------------------------------------------------------------------------

import re

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")


def strip_comments(line: str) -> str:
    escaped = False
    for index, char in enumerate(line):
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "%" and not escaped:
            return line[:index]
        escaped = False
    return line


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def resolve_tex_path(target: str, base_dir: Path) -> Path | None:
    candidate = Path(target)
    if not candidate.is_absolute():
        candidate = (base_dir / candidate).resolve()
    if candidate.suffix:
        return candidate if candidate.exists() else None
    with_tex = candidate.with_suffix(".tex")
    if with_tex.exists():
        return with_tex
    return candidate if candidate.exists() else None


def within_workspace(path: Path, workspace: Path) -> bool:
    try:
        path.resolve().relative_to(workspace.resolve())
        return True
    except ValueError:
        return False


def collect_tex_files(roots: list[Path], workspace: Path, follow_inputs: bool) -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []
    stack = [root.resolve() for root in reversed(roots)]

    while stack:
        path = stack.pop()
        if path in seen or not path.exists():
            continue
        seen.add(path)
        ordered.append(path)

        if not follow_inputs:
            continue

        text = read_text(path)
        for line in text.splitlines():
            stripped = strip_comments(line)
            for match in INPUT_RE.finditer(stripped):
                child = resolve_tex_path(match.group(1), path.parent)
                if child is None:
                    continue
                if not within_workspace(child, workspace):
                    continue
                if child not in seen:
                    stack.append(child)

    return ordered


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def scan(
    roots: list[Path],
    workspace: Path,
    config: dict,
    follow_inputs: bool = True,
    only_missing: bool = False,
) -> list[Block]:
    """Run all configured scan strategies and return citable blocks."""
    load_strategies()

    files = collect_tex_files(roots, workspace, follow_inputs)
    blocks: list[Block] = []

    for strategy_cfg in config.get("scan_strategies", []):
        stype = strategy_cfg["type"]
        if stype not in _STRATEGIES:
            print(f"Warning: unknown strategy '{stype}', skipping.", file=sys.stderr)
            continue
        strategy = _STRATEGIES[stype](strategy_cfg)
        for path in files:
            if path.suffix.lower() != ".tex":
                continue
            blocks.extend(strategy.extract(path))

    if only_missing:
        blocks = [b for b in blocks if b.status == "missing"]

    return blocks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan LaTeX manuscripts for citable blocks that may need citations."
    )
    parser.add_argument("roots", nargs="+", help="Root .tex files to scan.")
    parser.add_argument(
        "--config", required=True,
        help="Path to the discipline config.yaml.",
    )
    parser.add_argument(
        "--workspace", default=".",
        help="Workspace root for following \\input/\\include.",
    )
    parser.add_argument(
        "--no-follow-inputs", dest="follow_inputs", action="store_false",
        help="Do not follow \\input or \\include statements.",
    )
    parser.add_argument(
        "--only-missing", action="store_true",
        help="Show only blocks without a citation.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output machine-readable JSON.",
    )
    parser.set_defaults(follow_inputs=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    config = load_config(Path(args.config))

    roots: list[Path] = []
    for raw_root in args.roots:
        root = resolve_tex_path(raw_root, Path.cwd())
        if root is None:
            print(f"Missing root file: {raw_root}", file=sys.stderr)
            return 1
        roots.append(root)

    blocks = scan(roots, workspace, config, args.follow_inputs, args.only_missing)

    if args.json:
        print(json.dumps([asdict(b) for b in blocks], indent=2))
        return 0

    for block in blocks:
        title_part = f' title="{block.title}"' if block.title else ""
        preview_part = f' preview="{block.preview}"' if block.preview else ""
        print(f"{block.file}:{block.line}: [{block.kind}] {block.env} {block.status}{title_part}{preview_part}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

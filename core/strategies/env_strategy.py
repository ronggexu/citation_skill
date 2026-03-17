#!/usr/bin/env python3
"""
env_strategy — scan \\begin{env}...\\end{env} structured environments.

This is the primary strategy for mathematics papers that use theorem-like
environments (dfn, thm, prp, lem, cor, expl, rmk, ...).
"""

from __future__ import annotations

import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scanner import Block, register_strategy, read_text, strip_comments


CITE_RE = re.compile(r"\\(?:cite|parencite|autocite|textcite|footcite|smartcite|nocite)\b")


def compile_patterns(envs: list[str]) -> tuple[dict[str, re.Pattern[str]], dict[str, re.Pattern[str]]]:
    begin_patterns = {
        env: re.compile(rf"\\begin\{{{re.escape(env)}\}}(?:\[(?P<title>[^\]]*)\])?")
        for env in envs
    }
    end_patterns = {
        env: re.compile(rf"\\end\{{{re.escape(env)}\}}")
        for env in envs
    }
    return begin_patterns, end_patterns


def compact_whitespace(text: str) -> str:
    return " ".join(text.split())


def preview_from_block(lines: list[str], begin_end: int) -> str:
    first_line = compact_whitespace(strip_comments(lines[0][begin_end:]).strip())
    if first_line:
        return first_line[:140]

    for line in lines[1:]:
        candidate = compact_whitespace(strip_comments(line).strip())
        if not candidate:
            continue
        if candidate.startswith(r"\label"):
            continue
        if candidate.startswith(r"\begin"):
            continue
        if candidate.startswith(r"\end"):
            continue
        return candidate[:140]
    return ""


@register_strategy("env")
class EnvStrategy:
    """Scan \\begin{env}...\\end{env} blocks for citation status."""

    def __init__(self, cfg: dict):
        envs_cfg = cfg.get("envs", {})
        statement = envs_cfg.get("statement", [])
        narrative = envs_cfg.get("narrative", [])
        self.envs = statement + narrative

    def extract(self, path: Path) -> list[Block]:
        text = read_text(path)
        raw_lines = text.splitlines()
        scan_lines = [strip_comments(line) for line in raw_lines]
        begin_patterns, end_patterns = compile_patterns(self.envs)

        blocks: list[Block] = []
        line_index = 0

        while line_index < len(scan_lines):
            current_line = scan_lines[line_index]
            earliest: tuple[int, str, re.Match[str]] | None = None

            for env, pattern in begin_patterns.items():
                match = pattern.search(current_line)
                if match is None:
                    continue
                if earliest is None or match.start() < earliest[0]:
                    earliest = (match.start(), env, match)

            if earliest is None:
                line_index += 1
                continue

            _, env, match = earliest
            end_pattern = end_patterns[env]
            start_line = line_index
            end_line = line_index

            depth = len(begin_patterns[env].findall(scan_lines[line_index]))
            depth -= len(end_pattern.findall(scan_lines[line_index]))
            if depth <= 0:
                depth = 1

            while end_line + 1 < len(scan_lines) and depth > 0:
                end_line += 1
                depth += len(begin_patterns[env].findall(scan_lines[end_line]))
                depth -= len(end_pattern.findall(scan_lines[end_line]))

            block_lines = raw_lines[start_line : end_line + 1]
            block_text = "\n".join(block_lines)
            status = "cited" if CITE_RE.search(block_text) else "missing"
            blocks.append(
                Block(
                    file=str(path),
                    line=start_line + 1,
                    kind="env",
                    env=env,
                    title=compact_whitespace((match.group("title") or "").strip()),
                    status=status,
                    preview=preview_from_block(block_lines, match.end()),
                )
            )
            line_index = end_line + 1

        return blocks

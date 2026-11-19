"""Generate per-agent rule files from the Cursor sources.

Source (edit these):
  .cursor/rules/*.mdc     project, domain and phase rules (alwaysApply / globs)

Generated (never edit by hand):
  .agents/rules/*.md      Antigravity and OpenCode (trigger: always_on | glob | model_decision)
  .claude/rules/*.md      Claude Code (paths: frontmatter, none = always)

Skills live only in .agents/skills; .claude/skills is a symlink to it.
AGENTS.md is loaded directly by Cursor, Claude (via CLAUDE.md), OpenCode and Antigravity.

  python3 scripts/sync_agent_config.py          write generated files
  python3 scripts/sync_agent_config.py --check  exit 1 on drift
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURSOR_RULES = ROOT / ".cursor" / "rules"
AGENTS_RULES = ROOT / ".agents" / "rules"
CLAUDE_RULES = ROOT / ".claude" / "rules"
SKILLS = ROOT / ".agents" / "skills"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


@dataclass(frozen=True)
class Rule:
    name: str
    source: str
    description: str
    globs: tuple[str, ...]
    always: bool
    body: str


def _yaml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_mdc(path: Path) -> Rule:
    text = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    body = text
    match = _FRONTMATTER.match(text)
    if match:
        body = text[match.end() :]
        for line in match.group(1).splitlines():
            key, sep, value = line.partition(":")
            if sep:
                meta[key.strip()] = _unquote(value)
    globs = tuple(g.strip() for g in meta.get("globs", "").split(",") if g.strip())
    return Rule(
        name=path.stem,
        source=path.relative_to(ROOT).as_posix(),
        description=meta.get("description", ""),
        globs=globs,
        always=meta.get("alwaysApply", "").lower() == "true",
        body=body.lstrip("\n"),
    )


def _banner(rule: Rule) -> str:
    return (
        f"<!-- Generated from {rule.source} by scripts/sync_agent_config.py. "
        "Edit the source, then run `make agents-sync`. -->\n\n"
    )


def _antigravity(rule: Rule) -> str:
    lines = ["---"]
    if rule.always:
        lines.append("trigger: always_on")
    elif rule.globs:
        lines.append("trigger: glob")
        lines.append(f"globs: {_yaml_str(','.join(rule.globs))}")
    else:
        lines.append("trigger: model_decision")
    if rule.description:
        lines.append(f"description: {_yaml_str(rule.description)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + _banner(rule) + rule.body


def _claude(rule: Rule) -> str:
    head = ""
    if not rule.always and rule.globs:
        paths = "\n".join(f"  - {_yaml_str(g)}" for g in rule.globs)
        head = f"---\npaths:\n{paths}\n---\n\n"
    return head + _banner(rule) + rule.body


def _expected() -> dict[Path, str]:
    mdc = [_parse_mdc(p) for p in sorted(CURSOR_RULES.glob("*.mdc"))]
    out: dict[Path, str] = {}
    for rule in mdc:
        out[AGENTS_RULES / f"{rule.name}.md"] = _antigravity(rule)
        out[CLAUDE_RULES / f"{rule.name}.md"] = _claude(rule)
    return out


def _skills_problems() -> list[str]:
    problems: list[str] = []
    if not CLAUDE_SKILLS.is_symlink():
        problems.append(f"{CLAUDE_SKILLS.relative_to(ROOT)} must be a symlink to ../.agents/skills")
    elif CLAUDE_SKILLS.resolve() != SKILLS.resolve():
        problems.append(f"{CLAUDE_SKILLS.relative_to(ROOT)} points to {os.readlink(CLAUDE_SKILLS)}")
    stale = ROOT / ".cursor" / "skills"
    if stale.exists():
        problems.append(".cursor/skills shadows .agents/skills in Cursor; keep skills in .agents/skills only")
    return problems


def main(argv: list[str]) -> int:
    check = "--check" in argv
    expected = _expected()
    owned = {AGENTS_RULES, CLAUDE_RULES}
    present = {p for d in owned if d.is_dir() for p in d.iterdir() if p.is_file()}
    stale = sorted(present - expected.keys())
    changed = sorted(
        p for p, text in expected.items() if not p.exists() or p.read_text(encoding="utf-8") != text
    )
    problems = _skills_problems()

    if check:
        for p in changed:
            print(f"out of date: {p.relative_to(ROOT)}")
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)}")
        for msg in problems:
            print(msg)
        if changed or stale or problems:
            print("run `make agents-sync`")
            return 1
        return 0

    for d in owned:
        d.mkdir(parents=True, exist_ok=True)
    for p in stale:
        p.unlink()
    for p in changed:
        p.write_text(expected[p], encoding="utf-8")
    if not CLAUDE_SKILLS.exists() and not CLAUDE_SKILLS.is_symlink():
        CLAUDE_SKILLS.parent.mkdir(parents=True, exist_ok=True)
        CLAUDE_SKILLS.symlink_to(Path("..") / ".agents" / "skills", target_is_directory=True)
    print(f"{len(changed)} written, {len(stale)} removed, {len(expected)} total")
    for msg in _skills_problems():
        print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

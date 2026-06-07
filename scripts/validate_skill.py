#!/usr/bin/env python3
"""Validate Agent Skill directories against the SKILL.md open standard.

Dependency-free (stdlib only). Mirrors the checks performed by the official
`skills-ref validate` tool plus a few repo-specific structural checks.

Usage:
    python3 scripts/validate_skill.py skills/pre-deploy-security-review
    python3 scripts/validate_skill.py --all        # every skill under skills/
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")  # no leading/trailing/double hyphen
NAME_MAX = 64
DESC_MAX = 1024
BODY_MAX_LINES = 500
LINK_RE = re.compile(r"\]\(([^)]+)\)")  # markdown link targets


class SkillError(Exception):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the leading YAML frontmatter (simple key: value pairs, one nesting
    level tolerated). Returns (top_level_scalar_fields, body)."""
    if not text.startswith("---"):
        raise SkillError("SKILL.md must start with a '---' YAML frontmatter block")
    parts = text.split("\n")
    if parts[0].strip() != "---":
        raise SkillError("first line must be exactly '---'")
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        raise SkillError("frontmatter is not closed with '---'")

    fields: dict[str, str] = {}
    for line in parts[1:end]:
        if not line.strip() or line.startswith(("  ", "\t")):
            continue  # skip blanks and nested (e.g. metadata:) lines
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    body = "\n".join(parts[end + 1 :])
    return fields, body


def validate_skill(skill_dir: Path) -> list[str]:
    """Return a list of problems (empty == valid)."""
    problems: list[str] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return [f"{skill_dir}: no SKILL.md found"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        fields, body = parse_frontmatter(text)
    except SkillError as e:
        return [f"{skill_md}: {e}"]

    # name
    name = fields.get("name", "")
    if not name:
        problems.append("frontmatter missing required field: name")
    else:
        if len(name) > NAME_MAX:
            problems.append(f"name exceeds {NAME_MAX} chars ({len(name)})")
        if not NAME_RE.match(name):
            problems.append(
                f"name '{name}' must be lowercase a-z/0-9/hyphens, "
                "no leading/trailing/consecutive hyphens"
            )
        if name != skill_dir.name:
            problems.append(
                f"name '{name}' must match parent directory '{skill_dir.name}'"
            )

    # description
    desc = fields.get("description", "")
    if not desc:
        problems.append("frontmatter missing required field: description")
    elif len(desc) > DESC_MAX:
        problems.append(f"description exceeds {DESC_MAX} chars ({len(desc)})")

    # no XML tags in name/description (spec forbids; cheap guard)
    for fld in ("name", "description"):
        if "<" in fields.get(fld, "") and ">" in fields.get(fld, ""):
            problems.append(f"{fld} must not contain XML/HTML tags")

    # body length (recommendation, enforced as a soft cap here)
    body_lines = body.count("\n") + 1
    if body_lines > BODY_MAX_LINES:
        problems.append(
            f"SKILL.md body is {body_lines} lines (> {BODY_MAX_LINES}); "
            "move detail into references/"
        )

    # referenced relative files must exist
    for target in LINK_RE.findall(body):
        target = target.split("#", 1)[0].strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        if (skill_dir / target).resolve().exists():
            continue
        problems.append(f"broken relative link: {target}")

    return problems


def discover_skills(root: Path) -> list[Path]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(p for p in skills_root.iterdir() if (p / "SKILL.md").is_file())


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate SKILL.md skill directories")
    ap.add_argument("skill", nargs="?", help="path to a skill directory")
    ap.add_argument("--all", action="store_true", help="validate every skill under skills/")
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    if args.all or not args.skill:
        targets = discover_skills(repo_root)
        if not targets:
            print("no skills found under skills/", file=sys.stderr)
            return 1
    else:
        targets = [Path(args.skill).resolve()]

    failed = False
    for skill_dir in targets:
        problems = validate_skill(skill_dir)
        if problems:
            failed = True
            print(f"✗ {skill_dir.name}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"✓ {skill_dir.name}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

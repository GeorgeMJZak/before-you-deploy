"""Tests for the pre-deploy-security-review skill.

Run with:  pytest -q     (or:  python3 -m pytest -q)

These assert both the SKILL.md standard compliance and the content invariants that
make the review actually useful (all 8 categories present, 4 severities defined,
honesty guardrails intact).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_skill import discover_skills, validate_skill  # noqa: E402

SKILL_DIR = REPO_ROOT / "skills" / "pre-deploy-security-review"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES = SKILL_DIR / "references"


def test_at_least_one_skill_discovered():
    skills = discover_skills(REPO_ROOT)
    assert skills, "no skills discovered under skills/"


@pytest.mark.parametrize("skill_dir", discover_skills(REPO_ROOT), ids=lambda p: p.name)
def test_skill_is_standard_compliant(skill_dir):
    problems = validate_skill(skill_dir)
    assert not problems, f"{skill_dir.name} validation failed:\n" + "\n".join(problems)


def test_skill_md_exists():
    assert SKILL_MD.is_file()


def test_all_reference_files_present():
    expected = {
        "checklist.md",
        "severity-rubric.md",
        "ai-specific-risks.md",
        "report-format.md",
    }
    present = {p.name for p in REFERENCES.glob("*.md")}
    assert expected <= present, f"missing reference files: {expected - present}"


def test_eight_categories_named_in_checklist():
    text = (REFERENCES / "checklist.md").read_text(encoding="utf-8").lower()
    categories = [
        "authentication",
        "database",
        "secrets",
        "input validation",
        "public api",
        "logging",
        "ai-specific",
        "deployment hardening",
    ]
    missing = [c for c in categories if c not in text]
    assert not missing, f"checklist missing categories: {missing}"


def test_four_severities_defined():
    text = (REFERENCES / "severity-rubric.md").read_text(encoding="utf-8")
    for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        assert level in text, f"severity rubric missing {level}"


def test_honesty_guardrails_present_in_skill_body():
    text = SKILL_MD.read_text(encoding="utf-8")
    for marker in ("[CONFIRMED]", "[SUSPECTED]", "PRIORITIZED PUNCH LIST"):
        assert marker in text, f"SKILL.md missing guardrail: {marker}"


def test_ai_category_is_conditional():
    """The skill must instruct skipping the AI section when no AI is present."""
    text = SKILL_MD.read_text(encoding="utf-8").lower()
    assert "skip category 7" in text or "skip the ai" in text


def test_prompt_file_is_self_contained():
    prompt = (REPO_ROOT / "prompt.md").read_text(encoding="utf-8")
    assert "senior application security engineer" in prompt.lower()
    assert "PRIORITIZED PUNCH LIST" in prompt

# Changelog

## 1.1.0 — 2026-06-07

Bilingual release — English + Polish.

- Added Polish skill `pre-deploy-security-review-pl` (SKILL.md + all four reference
  files, native-quality Polish).
- Added `README.pl.md` (with EN/PL language switcher) and `prompt.pl.md`.
- `install.sh` now installs both language variants for each agent.
- Test suite extended to cover the Polish skill's structure and content invariants.

## 1.0.0 — 2026-06-07

Initial release.

- `pre-deploy-security-review` skill (`SKILL.md` open standard).
- Reference files: 8-category checklist, severity rubric, AI-specific risks (+ EU AI
  Act touchpoints), output/report format with fix-verification rules.
- Cross-agent adapters: `AGENTS.md` (Codex/Cursor), `GEMINI.md`, and a Gemini
  `/security-review` slash command.
- Standalone `prompt.md` for agents without a skill system.
- `install.sh` for Claude Code, Codex, and Gemini CLI.
- Dependency-free `validate_skill.py` + pytest suite + GitHub Actions CI.

Adapted from "Before You Deploy Your Vibe-Coded App" by George M. J. Zak.

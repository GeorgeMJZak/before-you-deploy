# Changelog

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

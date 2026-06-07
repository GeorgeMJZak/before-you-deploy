<div align="center">

# 🛡️ Before You Deploy

### A pre-deploy security review that any AI agent can run on your real code

Turn **Claude**, **Codex**, or **Gemini** into a senior application-security engineer
that audits your app *before* it ships — 8 categories, honest findings, a punch list
you can act on. No SaaS, no signup. Install once, run forever.

[![CI](https://github.com/GeorgeMJZak/before-you-deploy/actions/workflows/ci.yml/badge.svg)](https://github.com/GeorgeMJZak/before-you-deploy/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/GeorgeMJZak/before-you-deploy?color=success)](https://github.com/GeorgeMJZak/before-you-deploy/releases)
[![SKILL.md](https://img.shields.io/badge/SKILL.md-open%20standard-7c3aed)](https://agentskills.io/specification)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/GeorgeMJZak/before-you-deploy?style=social)](https://github.com/GeorgeMJZak/before-you-deploy/stargazers)

**Works with** &nbsp;`Claude Code`&nbsp; · &nbsp;`claude.ai`&nbsp; · &nbsp;`OpenAI Codex`&nbsp; · &nbsp;`Gemini CLI`&nbsp; · &nbsp;`Cursor`&nbsp; · &nbsp;any `AGENTS.md` tool

[Quickstart](#-quickstart) · [What it does](#-what-it-does) · [Compatibility](#-compatibility) · [Usage](#-usage) · [Structure](#-repository-structure)

</div>

---

## ⚡ Quickstart

```bash
git clone https://github.com/GeorgeMJZak/before-you-deploy.git
cd before-you-deploy
./install.sh claude     # or: codex · gemini · all
```

Then, in any project:

> **"Run a pre-deploy security review on this repo."**

No skill system? Paste [`prompt.md`](prompt.md) into any assistant. Same review, zero install.

---

## 🎯 What it does

The runnable companion to the essay **"Before You Deploy Your Vibe-Coded App"** by
George M. J. Zak. The PDF tells you *what* to check — this makes your AI actually *do
it*, on your real code:

- 🔍 **Maps your real attack surface** — routes, auth gates, where secrets are read,
  what's tracked in git — instead of guessing.
- 🧭 **Walks 8 categories** — Authentication · Database/data access · Secrets & API
  keys · Input validation · Public API surface · Logging & monitoring · AI-specific
  risks · Deployment hardening.
- ✅ **Labels every finding** `[CONFIRMED]` (seen in code) or `[SUSPECTED]`
  (pattern-based) — never a guess dressed as a fact.
- 🚦 **Rates severity** CRITICAL / HIGH / MEDIUM / LOW and ends with a **prioritized
  punch list** you can run top-to-bottom.
- 🤖 **Self-skips the AI section** on plain CRUD apps — no padding.

> **Why a skill, not just a prompt?** It loads on demand, carries the full checklist +
> severity rubric as reference files (progressive disclosure), and ships with tests so
> the methodology can't silently rot. The honesty guardrails are the point — they stop
> an eager AI from rubber-stamping your app.

---

## 🔌 Compatibility

| Agent | Install | Invoke |
|-------|---------|--------|
| **Claude Code** | `./install.sh claude` → `~/.claude/skills/` | "run a pre-deploy security review" |
| **claude.ai** | zip `skills/pre-deploy-security-review/`, upload in **Settings → Capabilities → Skills** | mention security review |
| **OpenAI Codex** | `./install.sh codex` → `~/.agents/skills/` | `/skills` or `$pre-deploy-security-review` |
| **Gemini CLI** | `./install.sh gemini` | `/security-review` |
| **Cursor / other** | drop [`adapters/AGENTS.md`](adapters/AGENTS.md) in your repo | always-on |
| **Anything else** | paste [`prompt.md`](prompt.md) | — |

For a **project-scoped** install, copy `skills/pre-deploy-security-review/` into the
repo's `.claude/skills/`, `.agents/skills/`, or `.gemini/skills/`.

---

## 💬 Usage

Findings come back specific and blunt — `file:line` and a copy-pasteable fix:

```text
[CRITICAL] [CONFIRMED] — Service-role key reaches the browser bundle
Category: Secrets & API keys
Risk:     Any visitor can extract the key from the JS bundle and read/write the
          entire database, bypassing row-level security.
Location: src/lib/supabase.ts:6
Fix:      Move the service-role client to server-only code; use the anon key with
          RLS in the browser. Rotate the leaked key now — assume it's compromised.

PRIORITIZED PUNCH LIST
[ ] CRITICAL — Move service-role key out of the browser bundle + rotate it
[ ] HIGH     — Rate-limit POST /api/auth/login + replace weak shared password
[ ] MEDIUM   — Add CSP + HSTS headers
[ ] LOW      — Swap Math.random() for crypto.randomUUID() in code generation
```

**Use it well:** read what it surfaces — *you* decide what's worth fixing. Follow up
(*"show me the exact code change for finding #2"*), then **verify the fix actually
applied** — AIs sometimes claim a fix they didn't make. Re-run before every deploy.

---

## 📁 Repository structure

```
before-you-deploy/
├── skills/pre-deploy-security-review/
│   ├── SKILL.md                    # the skill (loads on demand)
│   └── references/
│       ├── checklist.md            # the full 8-category checklist
│       ├── severity-rubric.md      # CRITICAL/HIGH/MEDIUM/LOW definitions
│       ├── ai-specific-risks.md    # category 7 + EU AI Act touchpoints
│       └── report-format.md        # output format + fix-verification rules
├── adapters/
│   ├── AGENTS.md                   # Codex / Cursor / agents.md convention
│   ├── GEMINI.md                   # Gemini CLI context form
│   └── gemini-commands/
│       └── security-review.toml    # /security-review slash command
├── prompt.md                       # raw copy-paste prompt (no install)
├── install.sh                      # one-command install per agent
├── scripts/validate_skill.py       # SKILL.md standard validator (stdlib only)
├── tests/test_skill.py             # pytest suite (compliance + content invariants)
└── .github/workflows/ci.yml        # validate + test on every push/PR
```

---

## 🧪 Develop & validate

```bash
python3 scripts/validate_skill.py --all   # check SKILL.md against the open standard
python3 -m pytest -q                        # run the test suite
```

CI runs both on every push and pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## ⭐ Star history

<a href="https://star-history.com/#GeorgeMJZak/before-you-deploy&Date">
  <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=GeorgeMJZak/before-you-deploy&type=Date" width="600">
</a>

If this saved you from shipping a leak, **star it** and send it to one other person
shipping AI-built software. That's the whole ask.

---

## 📜 Credits & license

Methodology and prose adapted from **"Before You Deploy Your Vibe-Coded App"** by
**George M. J. Zak** — AI strategy, cybersecurity, and the human side of technology
([jorgemjzak.com](https://jorgemjzak.com)).

Released under the [MIT License](LICENSE). Free to use, fork, and share.

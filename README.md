# Before You Deploy — a pre-deploy security review skill for any AI agent

A portable **Agent Skill** that turns Claude, Codex, Gemini (and any tool that
speaks the [`SKILL.md` standard](https://agentskills.io/specification) or reads
`AGENTS.md`) into a senior application-security reviewer for your project — *before*
it ships to real users.

It's the runnable companion to the essay **"Before You Deploy Your Vibe-Coded App"**
by George M. J. Zak. The PDF tells you what to check; this repo makes your AI
actually do it — on your real code, with honest findings and a punch list.

> **Why a skill and not just a prompt?** A skill loads on demand, carries the full
> 8-category checklist + severity rubric as reference files (progressive disclosure),
> and ships with tests so the methodology stays intact. You install it once; your
> agent reaches for it whenever you ask "is this safe to ship?".

---

## What it does

When you ask your agent to review security before deploying, it:

1. Finds the app that actually holds user data and maps the attack surface from the
   **real code** (routes, auth gates, where secrets are read, what's tracked in git).
2. Walks **8 categories**: Authentication · Database/data access · Secrets & API keys
   · Input validation · Public API surface · Logging & monitoring · AI-specific risks
   · Deployment hardening.
3. Marks every finding **`[CONFIRMED]`** (seen in code) or **`[SUSPECTED]`**
   (pattern-based, unverified) — never a guess dressed as fact.
4. Rates each **CRITICAL / HIGH / MEDIUM / LOW** and ends with a **prioritized punch
   list** you can execute top-to-bottom.
5. **Self-skips the AI section** for plain CRUD apps — no padding.

The honesty guardrails are the point: they stop an eager AI from rubber-stamping
your app.

---

## Install

### Claude Code
```bash
./install.sh claude          # → ~/.claude/skills/pre-deploy-security-review
```
Or copy `skills/pre-deploy-security-review/` into a repo's `.claude/skills/` for a
project-scoped install. (claude.ai: zip the skill folder and upload via
**Settings → Capabilities → Skills**.)

### OpenAI Codex
```bash
./install.sh codex           # → ~/.agents/skills/pre-deploy-security-review
```
Codex also scans `.agents/skills/` from your working dir up to the repo root.
Invoke with `/skills` or `$pre-deploy-security-review`. Prefer always-on? Drop
`adapters/AGENTS.md` into your repo or `~/.codex/`.

### Gemini CLI
```bash
./install.sh gemini          # skill + /security-review slash command
```
Manage with `gemini skills list | enable | disable | reload`. The
`/security-review` command works even without skill support.

### Any other agent / no skill system
Paste [`prompt.md`](prompt.md) directly into the assistant. Same review, zero install.

---

## Repository layout

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

## How to use it well

1. Run the review. Read what it surfaces — *you* decide what's worth fixing.
2. Follow up on specifics: *"show me the exact code change for finding #2."*
3. **Verify the fix actually applied** — re-read the file / run the build. AIs
   sometimes claim a fix they didn't make.
4. Re-run before each deploy. Security posture is a practice, not a state.

---

## Develop / validate

```bash
python3 scripts/validate_skill.py --all   # check SKILL.md against the standard
python3 -m pytest -q                       # run the test suite
```

CI runs both on every push and pull request.

---

## Credits & license

Methodology and prose adapted from **"Before You Deploy Your Vibe-Coded App"** by
**George M. J. Zak** — AI strategy, cybersecurity, and the human side of technology
([jorgemjzak.com](https://jorgemjzak.com)).

Licensed under the [MIT License](LICENSE). Free to use, fork, and share — pay it
forward by sending it to one other person shipping AI-built software.

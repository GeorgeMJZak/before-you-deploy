# Contributing

This skill is meant to stay small, sharp, and honest. Contributions that make the
review catch more real problems — or cut padding — are welcome.

## Before opening a PR

```bash
python3 scripts/validate_skill.py --all   # SKILL.md standard compliance
python3 -m pytest -q                        # content + structure invariants
```

Both must pass. CI runs them on every push and pull request.

## Guidelines

- **Keep `SKILL.md` under 500 lines.** Detail belongs in `references/` so it loads
  on demand (progressive disclosure). The validator enforces this.
- **Preserve the honesty guardrails.** `[CONFIRMED]`/`[SUSPECTED]`, "show me the
  file", severity on every finding, the prioritized punch list, and self-skipping
  the AI category — these are the point of the skill, not decoration.
- **Don't add a finding category without a check the agent can actually perform**
  against real code.
- If you add or rename a reference file, update `references/` links in `SKILL.md`
  and the expected-files set in `tests/test_skill.py`.

## Scope

Bug fixes, clearer fixes, new high-signal checks, and adapters for additional agents
are in scope. Turning this into a generic "security tips" dump is not.

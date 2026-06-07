<!-- Thanks for contributing. Keep the skill small, sharp, and honest. -->

## What changed & why

<!-- one or two sentences -->

## Reviewer checklist

- [ ] `python3 scripts/validate_skill.py --all` passes
- [ ] `python3 -m pytest -q` passes
- [ ] `SKILL.md` stays under 500 lines (detail lives in `references/`)
- [ ] Honesty guardrails intact: `[CONFIRMED]`/`[SUSPECTED]`, severity on every
      finding, prioritized punch list, AI category self-skips for non-AI apps
- [ ] New/renamed reference files are linked in `SKILL.md` **and** listed in
      `tests/test_skill.py`
- [ ] No new finding category without a check an agent can actually perform on code

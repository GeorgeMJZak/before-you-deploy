# Severity Rubric

Assign exactly one level to every finding. When unsure between two, justify the
choice in one clause rather than splitting the difference.

| Level | Meaning | Action timeline | Examples |
|-------|---------|-----------------|----------|
| **CRITICAL** | Do not deploy until fixed. Direct data exposure, auth bypass, or account takeover — exploitable with little effort or precondition. | Block the deploy. | Service-role/admin key in the browser bundle; an admin/API route that returns user data with no auth check; RLS off on a table the anon key can reach; plaintext passwords; prompt injection into an over-permissioned agent. |
| **HIGH** | Fix this week. Exploitable, but needs a condition or some effort. | Before real traffic / within days. | Login endpoint with no rate limiting + weak shared password; horizontal access on a less-obvious endpoint; secret recoverable from git history of a repo about to go public; reflected XSS behind an authed page. |
| **MEDIUM** | Fix this month. A real weakness with limited blast radius. | Tracked with a deadline. | Missing CSP/HSTS; verbose error messages enabling enumeration; no middleware backstop (per-route checks present); admin-authored stored HTML rendered without sanitization. |
| **LOW** | Track and revisit. Hardening and hygiene. | Backlog. | `Math.random()` for non-security tokens; missing security-event logging; in-memory rate limiter that resets on cold start; dependency with a low-severity advisory. |

## Calibration notes

- **Context moves severity.** A secret in a *private* repo is latent; the same
  secret in a repo about to be made *public* is CRITICAL. State the context that
  sets the level.
- **Blast radius matters more than cleverness.** A boring missing-auth-check that
  exposes the whole table outranks an elegant timing attack that leaks one byte.
- **`[SUSPECTED]` findings still get a severity** — rate them as if confirmed, and
  say what would confirm or downgrade them.
- **Don't inflate to look thorough, don't deflate to be reassuring.** Either failure
  destroys the report's usefulness.

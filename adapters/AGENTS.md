# AGENTS.md — Pre-Deploy Security Review

> Drop-in instructions for agents that read `AGENTS.md` (OpenAI Codex, Cursor, and
> the growing list of tools following the [agents.md](https://agents.md) convention).
> This mirrors the `pre-deploy-security-review` skill. If your tool supports the
> `SKILL.md` standard, prefer installing the skill from `skills/` instead — it loads
> on demand. Use this file when you want the behavior always-on for a repo, or paste
> it into a global `~/.codex/AGENTS.md` / `~/.agents/` location.

## When the user asks to review security before deploying

Act as a **senior application security engineer** doing a pre-deployment review of a
project about to ship to real users with real data — often AI-assisted. Find what is
actually wrong before attackers do. Do not reassure.

**Rules:**
1. Read the actual code. Never guess what it "probably" does. If you can't see what
   you need, say so and name the file/snippet to show you.
2. Label every finding `[CONFIRMED]` (seen in code) or `[SUSPECTED]` (pattern-based).
3. Every finding gets a severity: CRITICAL (deploy-blocking) / HIGH (this week) /
   MEDIUM (this month) / LOW (track).
4. Be blunt and specific — `file:line`, copy-pasteable fixes. No padding.
5. If the app has no LLM/agent/embeddings, skip the AI category entirely.

**Walk these 8 categories** (full detail in the skill's `references/checklist.md`):

1. Authentication — API-layer gating of admin routes, password hashing, brute-force
   lockout, session cookie flags + invalidation, MFA.
2. Database / data access — row-level authz, horizontal access (User A → User B),
   least-privilege keys (service key never in browser), over-exposed fields.
3. Secrets & API keys — none in frontend/bundle/git history; env hygiene; test creds
   out of prod; rotate anything ever exposed.
4. Input validation — server-side checks, parameterized queries, XSS / raw-HTML
   audit, file-upload MIME+size+metadata, honeypots.
5. Public API surface — rate limiting (IP + user), no enumeration, CORS not `*`,
   methods scoped per route.
6. Logging & monitoring — security events logged, no PII/secrets in logs, abuse &
   silent-failure detection, retention.
7. AI-specific (only if AI is present) — prompt injection, tool/agent
   overpermission, insecure output handling, cost amplification.
8. Deployment hardening — HTTPS+HSTS, security headers (CSP, nosniff, frame,
   referrer), WAF/CDN, dependency audit.

**Report:** per finding → `[SEVERITY] [CONFIRMED|SUSPECTED] — title`, category,
one-sentence risk, `file:line` (or "needs verification — show me X"), concrete fix.
End with a **PRIORITIZED PUNCH LIST**, sorted CRITICAL → LOW. Close with what you
could not verify.

**When fixing:** after each change, re-read the file and run the build/tests; prove
the fix with the diff/output, never a bare "done". Surface any production tradeoff
before making a change that could break prod.

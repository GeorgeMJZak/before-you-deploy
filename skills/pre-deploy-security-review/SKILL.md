---
name: pre-deploy-security-review
description: Pre-deployment security review for web apps, APIs, and AI agents — especially AI-assisted / "vibe-coded" projects about to ship with real users and real data. Use when the user asks to review security before deploy, find vulnerabilities, audit an app, check auth/database/secrets/API exposure, or asks "is this safe to ship?". Walks 8 categories (auth, data access, secrets, input validation, public APIs, logging, AI-specific risks, deployment hardening), marks every finding [CONFIRMED] or [SUSPECTED] against actual code, and ends with a severity-sorted punch list.
license: MIT
metadata:
  author: George M. J. Zak
  source: "Before You Deploy Your Vibe-Coded App"
  homepage: https://jorgemjzak.com
  version: "1.0.0"
---

# Pre-Deploy Security Review

You are acting as a **senior application security engineer** doing a pre-deployment
review of a project that is about to ship to real users with real data — often
built quickly and AI-assisted. Your job is to **find what is actually wrong before
attackers do — not to reassure the user.**

## Operating rules (do not skip these — they are the point)

1. **Look at the actual code.** Read the real files. Do **not** guess what the code
   "probably" does. If you cannot see something you need to judge a risk, say so
   explicitly and name the exact file or snippet to show you.
2. **Label every finding** `[CONFIRMED]` (you saw it in the code) or `[SUSPECTED]`
   (pattern-based, unverified). Never present a guess as a fact.
3. **Be blunt and specific.** If something is fine, don't pad the report. If
   something is dangerous, lead with it. Do not soften findings to be agreeable.
4. **Severity is mandatory** on every finding: CRITICAL / HIGH / MEDIUM / LOW.
   See [references/severity-rubric.md](references/severity-rubric.md).
5. **Honesty about coverage.** At the end, state plainly what you could not verify
   from the material available.

## Procedure

**Step 0 — Scope.** Identify the stack, the deployment target, and where the real
user data lives. Find the app that actually holds data (it is often one sub-project
among several). Detect whether the project uses any LLM/agent/embeddings/vector
search — if **not**, **skip category 7 entirely** (don't pad a plain CRUD app with
AI noise).

**Step 1 — Recon the attack surface.** Enumerate, from the real code:
- every API route / endpoint and the HTTP methods it exports,
- which routes are auth-gated vs public,
- where secrets and keys are read,
- what `.gitignore` covers and whether any secret/asset is tracked in git,
- the data store and whether row-level authorization exists.

A fast, high-signal sweep for common problems:

```bash
# tracked secrets / env files
git ls-files | grep -iE '\.env($|\.)' || echo "no tracked .env (good)"
git log --all --oneline -- '*.env*' | head
# provider key prefixes committed anywhere
git grep -nE 'sk_(live|test)_|sk-[A-Za-z0-9]|re_[A-Za-z0-9]|AKIA[0-9A-Z]{16}|ghp_|xox[baprs]-|-----BEGIN .*PRIVATE KEY-----' || echo "no obvious committed keys"
# admin/API routes and their auth checks (adapt the path/glob to the stack)
grep -rnE 'export (async )?function (GET|POST|PUT|PATCH|DELETE)' --include=route.* .
```

**Step 2 — Walk all 8 categories.** Go through each one against the real code. The
full checklist (what to verify in each) is in
[references/checklist.md](references/checklist.md). The AI-specific category 7 is
detailed in [references/ai-specific-risks.md](references/ai-specific-risks.md).

1. Authentication — admin/privileged routes gated at the **API layer** (not just
   hidden in the UI); password storage (bcrypt/argon2/scrypt, salted); brute-force
   cost / lockout; session cookie flags (HttpOnly, Secure, SameSite), expiry,
   invalidation on logout & password change; MFA availability.
2. Database / data access — row-level authorization on every table with user data;
   horizontal access (can User A reach User B's records?); least-privilege keys
   (service/admin keys never in the browser); over-exposed fields.
3. Secrets & API keys — none in frontend/bundled code or git history; env-var
   hygiene; test creds not shipped to prod; any ever-exposed key treated as
   compromised and rotated.
4. Input validation — server-side validation on every input; parameterized queries
   (no SQL injection); XSS / raw-HTML rendering audited; file-upload MIME+size+
   metadata handling.
5. Public API surface — rate limiting (per IP and per user) on auth and expensive
   endpoints; no user/record enumeration (normalize responses); CORS scoped (not
   `*`); HTTP methods scoped per route.
6. Logging & monitoring — security events logged; no PII/secrets in logs; a way to
   notice abuse and silent failures; useful retention.
7. **AI-specific risks (only if the app uses an LLM/agent/embeddings)** — prompt
   injection; tool/agent overpermission & blast radius; insecure output handling
   (model output rendered as HTML / executed as code); cost amplification.
8. Deployment hardening — HTTPS + HSTS; security headers (CSP, X-Content-Type-
   Options, frame protection, Referrer-Policy); WAF/CDN; dependency vulnerabilities
   (`npm audit` / `pip-audit` — flag critical/high).

**Step 3 — Report.** Use the exact output format in
[references/report-format.md](references/report-format.md). Per finding:
`[SEVERITY] [CONFIRMED/SUSPECTED] — short title`, category, one-sentence risk, the
specific file/location (or "needs verification — show me X"), and a concrete,
copy-pasteable fix. End with a **PRIORITIZED PUNCH LIST**: every finding as a
one-line checklist item, sorted CRITICAL → LOW.

**Step 4 — Verify fixes (when asked to fix).** After applying a fix, re-read the
changed file and confirm the change is actually present and type-checks/builds.
Agents sometimes claim a fix they did not make — prove it with the diff or the
build output, not an assertion. See
[references/report-format.md](references/report-format.md#verifying-fixes).

## What good looks like

- Findings that name `file:line`, not vague categories.
- A CRITICAL that is genuinely deploy-blocking, stated first and without hedging.
- Explicit `[SUSPECTED]` + "show me X" wherever the code wasn't visible.
- Category 7 silently omitted when there is no AI in the app.
- A punch list the user can execute top-to-bottom before shipping.

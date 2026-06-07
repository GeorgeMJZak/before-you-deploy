# The copy-paste prompt

No skill system? Paste this straight into any AI assistant that can see your code.
This is the manual form of the `pre-deploy-security-review` skill — same review, no
install.

> The honesty guardrails are the point. `[CONFIRMED]`/`[SUSPECTED]`, "tell me which
> file to show you", and "don't soften findings" are what stop an eager AI from
> rubber-stamping your app. After the first pass, follow up: *"show me the exact code
> change for finding #2"* — then verify the fix actually applied. AIs sometimes claim
> a fix they didn't make. It self-skips the AI section if there's no LLM in the app.

---

```
Act as a senior application security engineer performing a pre-deployment review of
this application. It is about to ship to real users with real data and was likely
built quickly / AI-assisted. Find what is actually wrong before attackers do — do not
reassure me.

How to work:
- Look at the actual code available to you. Do NOT guess at what the code probably
  does. If you can't see something you need to judge a risk, say so explicitly and
  tell me which file or snippet to show you.
- Mark every finding as either [CONFIRMED] (you can see it in the code) or [SUSPECTED]
  (likely based on patterns, but you couldn't verify). Never present a guess as fact.
- Be specific and blunt. If something is fine, don't pad the report. If something is
  dangerous, lead with it.

Severity levels:
- CRITICAL — do not deploy until fixed. Data exposure, auth bypass, account takeover.
- HIGH — fix this week. Exploitable, but needs a condition or some effort.
- MEDIUM — fix this month. Real weakness, limited blast radius.
- LOW — track and revisit. Hardening and hygiene.

Walk through every category:
1. Authentication — admin/privileged routes protected at the API layer (not just hidden
   in the UI); password storage (bcrypt/argon2/scrypt, salted); account lockout /
   brute-force cost; email verification; MFA; session tokens (HttpOnly, Secure,
   SameSite, sane expiration, invalidated on logout and password change).
2. Database / data access — row-level security (or equivalent authz) on every table
   with user data, especially where an anon/client key is exposed to the browser;
   horizontal access (can User A read/modify User B's records?); least-privilege roles
   (service/admin keys never in the browser); over-exposed fields.
3. Secrets & API keys — any key/secret in frontend/bundled code or committed to git
   (scan for sk_, sk-, re_, AKIA, etc.); secrets in env vars, .env gitignored; test
   creds not in prod; any ever-exposed key treated as compromised and rotated.
4. Input validation — server-side validation on every input; SQL injection
   (parameterized queries only); XSS (escape/sanitize; audit raw-HTML rendering);
   file uploads (server-side MIME + size + metadata).
5. Public API surface — rate limiting (per IP and per user) on auth and expensive
   endpoints; no sensitive-data leak or user/record enumeration (normalize responses);
   CORS scoped (not wildcard); HTTP methods scoped per route.
6. Logging & monitoring — security events logged (logins, password/privilege changes,
   admin actions, rate-limit hits); useful retention; no PII/secrets/passwords in logs;
   a way to notice silent failures and abuse in progress.
7. AI-specific risks (ONLY if this app uses an LLM/agent/embeddings/vector search) —
   prompt injection (untrusted input concatenated into prompts); tool/agent
   overpermission (blast radius if injection succeeds; least privilege + human approval
   for high-impact actions); insecure output handling (model output rendered as HTML or
   executed as code); cost amplification (unthrottled token spend).
8. Deployment hardening — HTTPS + HSTS everywhere; security headers (CSP,
   X-Content-Type-Options, frame protection, Referrer-Policy); WAF/CDN; dependency
   vulnerabilities (npm audit / pip-audit) — flag any critical/high.

For each finding:
- [SEVERITY] [CONFIRMED/SUSPECTED] — short title
- Category
- One-sentence description of the risk
- The specific file/location (or "needs verification — show me X")
- A concrete, copy-pasteable fix

End with a PRIORITIZED PUNCH LIST: every finding as a one-line checklist item, sorted
CRITICAL → LOW, so I know exactly what to do and in what order before I ship.

Do not stop at the obvious. Do not soften findings. Be honest about what you couldn't
verify from the code I gave you.
```

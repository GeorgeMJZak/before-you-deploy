# The 8-Category Checklist

Verify each item against the **actual code**. Mark findings `[CONFIRMED]` or
`[SUSPECTED]`. This is the detailed companion to `SKILL.md`.

---

## 1. Authentication
*Most incidents start at the front door. If the front door is wrong, the rest of the building doesn't matter.*

- [ ] **Admin/privileged routes are protected end-to-end** — at the API layer, not
  just hidden in the UI. The UI gate is a convenience for honest users; the API gate
  is the real protection. If a URL returns sensitive data without checking auth, it
  will be discovered.
- [ ] **Passwords stored correctly** — hashed with bcrypt/argon2/scrypt, per-user
  salt. Never plaintext, never reversible encryption. Plaintext storage is a
  career-ending bug in production.
- [ ] **Account lockout / brute-force cost** — repeated failures must cost the
  attacker more than they cost you. An unlimited login endpoint is an unlimited
  brute-force target.
- [ ] **Email verification before sensitive access.**
- [ ] **MFA available for sensitive actions** — TOTP via authenticator apps is the
  cheap default. SMS is better than nothing but vulnerable to SIM swap.
- [ ] **Session tokens handled properly** — HttpOnly, Secure, SameSite=Lax (or
  Strict for high-security flows). Reasonable expiration. **Invalidated on logout
  and on password change.** Bound to the user agent if you can.

> AI-generated auth *looks* correct because it follows the right patterns, but
> often skips the details that make those patterns secure — token rotation, session
> invalidation on password change, replay protection. Ask explicitly: *"walk me
> through what happens when (a) a user changes their password, (b) a session token
> leaks, (c) a user logs out, (d) someone tries the same password 50 times. Show me
> each code path."*

## 2. Database / Data access
*If users can read each other's data, you don't have an app. You have a data leak with a UI on top.*

- [ ] **Row-Level Security (or equivalent authz) on every table with user data** —
  especially on Supabase/Firebase/any backend where an anon/client key reaches the
  browser. RLS is the wall between "what your code intends" and "what the browser can
  actually do." Without it, the wall isn't there.
- [ ] **Users cannot access other users' data.** Test directly: as User A, try to
  read a record you know belongs to User B. If the API returns it, that's horizontal
  privilege escalation — one of the most common AI-generated bugs, because the read
  endpoint was added without scoping it to the authenticated user.
- [ ] **Least-privilege roles.** The anon role gets the minimum grants. The
  service-role/admin key must **never** touch the browser. Admin-only tables have
  anon revoked entirely.
- [ ] **Sensitive fields are not over-exposed.** Email, phone, address, internal IDs,
  admin flags — if the client doesn't need it, the API shouldn't return it. Define a
  public schema explicitly and stick to it.
- [ ] **Backups exist and restore has been tested.** "We have backups" ≠ "we tested
  that we can restore from backups."

> **The Supabase/Firebase/nocode trap:** hosted backends ship the anon/client key
> in your frontend — fine *only if* RLS or equivalent rules are configured. Many
> vibe-coded apps ship with RLS off on every table, meaning the anon key any visitor
> can extract from your JavaScript has full read/write to the whole database. Check
> this before launch. It's a free fix and a complete change in posture.

## 3. Secrets & API keys
*Every secret that ends up in your repo or frontend bundle is a secret on the open internet.*

- [ ] **No API keys in frontend code.** Anything in `src/` or `public/` becomes part
  of the JS bundle. Scan for the prefixes of every provider you use — Stripe
  (`sk_`), Resend (`re_`), OpenAI/Anthropic (`sk-`), AWS (`AKIA`), etc. If any
  appear outside an env-var reference, rotate immediately.
- [ ] **Secrets in environment variables**, not in code or committed config. Check
  `.gitignore` includes `.env*` and your secrets file is on the gitignored side.
- [ ] **Test credentials not present in production.** AI boilerplate often leaves
  test keys / test audiences behind.
- [ ] **Service-account keys scoped to least privilege** — specific buckets,
  projects, roles. Not a key that can read everything.
- [ ] **Any ever-exposed key has been rotated.** No exceptions. If it hit a public
  repo for ten seconds, it's compromised — GitHub indexes commits within minutes and
  bots scrape new repos within hours.

## 4. Input validation
*Every form, endpoint, and URL parameter is a chance to send something you didn't expect. Assume malicious input by default.*

- [ ] **Server-side validation on every input.** Client-side validation is UX, not
  security. `curl` bypasses every JavaScript check.
- [ ] **SQL injection impossible** — parameterized queries / prepared statements.
  Never concatenate user input into SQL. ORMs/query builders usually handle this —
  check any raw queries you wrote.
- [ ] **XSS blocked** — user-supplied text is escaped or sanitized. React/Vue/Svelte
  do this by default *until* you use `dangerouslySetInnerHTML` / `v-html` / raw HTML.
  Audit every such use.
- [ ] **File uploads validated** — server-side MIME check (not just the client
  header), size limit, metadata stripped, filename never trusted. Re-encode images
  through a library that drops anything that isn't pixel data.
- [ ] **Honeypots on public forms** — a hidden field (`website`/`hp`) real users
  won't fill but bots will. If filled, silently drop.

## 5. Public API surface
*Every endpoint is a public attack target unless you explicitly gated it.*

- [ ] **Rate limiting in place** — per IP, per user, per endpoint. Most platforms
  (Cloudflare, Vercel, AWS API Gateway) offer it with a few clicks. An unlimited
  login endpoint is an unlimited brute-force target. *(Note: in-memory limiters reset
  on serverless cold starts and are per-instance — use a shared store like Redis for
  real durability.)*
- [ ] **Sensitive data not exposed** — a "get profile" endpoint shouldn't return
  password hashes, internal IDs, or admin flags. Public schema explicit.
- [ ] **No user/record enumeration** — a signup that returns "email already exists"
  lets an attacker enumerate users. A login that distinguishes "wrong password" from
  "no such user" does too. Normalize responses.
- [ ] **CORS scoped tightly** — specific trusted origins, never `*` when credentials
  are involved.
- [ ] **HTTP methods scoped per route** — read-only endpoints reject POST; modify
  endpoints reject GET.

## 6. Logging & monitoring
*You cannot defend what you cannot see. The first thing an attacker takes is your ability to know they're there.*

- [ ] **Security-relevant events logged** — login success & failure, password
  changes, permission/privilege changes, admin actions, API errors, rate-limit
  triggers. Keep on a separate surface from app logs if you can.
- [ ] **Logs retained long enough** — 90 days minimum for most apps; longer for
  regulated data. Logs you delete after 24h catch nothing.
- [ ] **You can detect abuse in progress** — spike in login failures, unusual
  geography, a new IP making admin API calls. Alert on the obvious; it's easy.
- [ ] **You notice silent failures** — wire up error tracking (Sentry/Rollbar/etc).
  An email service that returns an ignored error code fails invisibly until customers
  complain.
- [ ] **No PII/secrets/passwords in logs.** Logs leak too. If you must log an
  identifier, hash it.

## 7. AI-specific risks
**Only applies if the app uses an LLM / agent / embeddings / vector search. If it
doesn't, skip this category entirely.** Full detail in
[ai-specific-risks.md](ai-specific-risks.md).

## 8. Deployment hardening
*The last mile. Get this wrong and you can do everything else right and still have a public incident.*

- [ ] **HTTPS enforced everywhere** — no HTTP, no mixed content. HSTS header with a
  reasonable `max-age`. Plain HTTP redirects, not merely available.
- [ ] **Security headers configured** — Content-Security-Policy (even a permissive
  starter beats none), `X-Content-Type-Options: nosniff`, `X-Frame-Options` /
  `frame-ancestors`, `Referrer-Policy`. Five lines of config that block half of
  common attacks.
- [ ] **WAF / CDN in front** — Cloudflare's free tier handles most of what a small
  app needs. Without it you're directly exposed.
- [ ] **DDoS mitigation** — turn the relevant platform features on.
- [ ] **Dependency vulnerabilities checked** — `npm audit` / `pip-audit` on each
  deploy; fix critical/high before launch. Enable Dependabot/Renovate.
- [ ] **Domain hardening** — DNSSEC, registrar lock, WHOIS privacy, strong password
  + MFA on the DNS provider account. Your domain is your identity online.

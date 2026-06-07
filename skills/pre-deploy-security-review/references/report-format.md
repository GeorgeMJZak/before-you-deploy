# Output Format

Produce the report in this exact shape. Consistency makes it skimmable and makes the
punch list executable.

## Per finding

> **[SEVERITY] [CONFIRMED|SUSPECTED] — short title**
> **Category:** one of the 8
> **Risk:** one sentence on what an attacker gains.
> **Location:** `path/to/file.ext:line` — or, if you couldn't see it,
> `needs verification — show me <exact file/snippet>`.
> **Fix:** a concrete, copy-pasteable change (code block, command, or config), not
> "consider improving X".

Example:

> **[CRITICAL] [CONFIRMED] — Service-role key reaches the browser bundle**
> **Category:** Secrets & API keys
> **Risk:** Any visitor can extract the key from the JS bundle and read/write the
> entire database, bypassing all row-level security.
> **Location:** `src/lib/supabase.ts:6` — `createClient(url, SERVICE_ROLE_KEY)` in a
> file imported by a client component.
> **Fix:** Move the service-role client to server-only code. In the browser use the
> anon key with RLS enabled. Rotate the leaked key in the provider dashboard now —
> assume it is compromised.

## Ordering

1. A 2–4 line **summary** up top: stack, where the real data lives, and the single
   worst thing you found.
2. Findings grouped by severity, **CRITICAL first**.
3. The prioritized punch list.
4. A short **"Could not verify"** section listing what you couldn't see and exactly
   what to show you to close each gap.

## The prioritized punch list

End with every finding as a one-line checklist item, sorted CRITICAL → LOW, so the
user knows exactly what to do and in what order before shipping:

```
PRIORITIZED PUNCH LIST
[ ] CRITICAL — Move service-role key out of the browser bundle + rotate it
[ ] CRITICAL — Add auth check to GET /api/admin/export
[ ] HIGH     — Rate-limit POST /api/auth/login + replace weak shared password
[ ] MEDIUM   — Add CSP + HSTS headers
[ ] LOW      — Swap Math.random() for crypto.randomUUID() in code generation
```

## Verifying fixes

When the user asks you to apply fixes (not just report), after each change:

1. **Re-read the changed file** and confirm the change is actually present.
2. **Run the build / type-check / test** and paste the relevant output.
3. Only then state it's fixed — with the diff or build output as evidence, never a
   bare "done". Agents sometimes claim a fix they didn't make; prove it.
4. If a fix has a production tradeoff (e.g. removing a tracked asset that the runtime
   reads at deploy time), **stop and surface the tradeoff** instead of silently
   making a change that breaks production or gives false security.

## Tone

Blunt, specific, evidence-first. No reassurance padding. If the app is genuinely in
good shape on a category, say so in one line and move on — don't manufacture
findings to look thorough.

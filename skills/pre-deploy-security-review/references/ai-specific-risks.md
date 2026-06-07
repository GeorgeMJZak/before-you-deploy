# Category 7 — AI-Specific Risks

**Only assess this category if the app actually uses an LLM, agent, embeddings, or
vector search.** For a plain CRUD app, omit it from the report entirely — don't pad
a non-AI app with AI findings.

None of these are exotic. All are exploitable today.

| Risk | Severity | What to verify |
|------|----------|----------------|
| **Prompt injection** | CRITICAL | Is untrusted user text mixed directly into the system prompt? An attacker writes "ignore previous instructions and…" and the agent obeys. Treat all user input as untrusted; never concatenate it raw into prompts. Use clear delimiters; validate output before acting on it. |
| **Tool / agent overpermission** | CRITICAL | If the agent can execute code, send email, move money, or modify data — what's the blast radius when a prompt injection succeeds? Restrict tool permissions to the minimum. Require human-in-the-loop confirmation for high-impact actions. |
| **Data exfiltration via output** | HIGH | An AI with DB access can be tricked into revealing data the requesting user isn't authorized to see. If the model can read more than the user can, that gap will be exploited. Scope AI data access to exactly what the requesting user is allowed to access. |
| **Cost amplification** | HIGH | One unauthenticated, unthrottled user can run your token bill into the thousands in an afternoon. Rate-limit AI endpoints. Cap per-user monthly token spend. Monitor for unusual usage. |
| **Insecure output handling** | HIGH | If you render model output as HTML, an attacker can prompt-inject HTML that runs in your users' browsers. If you execute AI-generated code, they can inject malicious code. Treat AI output as untrusted input to the next system. |
| **Training-data leakage** | MEDIUM | If you fine-tune on user data, it may surface in responses to other users. Sanitize and obtain explicit consent; most apps should prefer retrieval-augmented generation over fine-tuning. |
| **Model swapping by provider** | MEDIUM | A silent provider model upgrade can change behavior you depended on. Pin model versions where allowed; test before unpinning. |
| **Conversation-log exposure** | MEDIUM | AI conversation logs may contain PII, secrets, or proprietary content the user shared. Protect them at least as well as user data. |

## The mental model

> An LLM agent in your application is approximately as trustworthy as a contractor
> you met at a job site five minutes ago. Smart, capable, eager to help — and
> absolutely should not be given the master keys, the bank login, or unsupervised
> access to the parts of the building you wouldn't show a stranger. The **principle
> of least authority** matters *more* for AI components than for any other part of
> your stack, because AI components are easier to manipulate.

## Governance touchpoints (if shipping in or to the EU)

The EU AI Act applies regardless of where the company is registered; most
general-purpose obligations land in waves through 2026. Several map directly onto
this checklist — flag them when relevant, but distinguish "security finding" from
"compliance note":

- **Article 15** (accuracy, robustness, cybersecurity) maps to this entire
  checklist — security posture becomes a regulatory artifact.
- **Article 14** (human oversight) — tool/agent overpermission is also a compliance
  issue in high-risk domains.
- **Article 12** (record-keeping) — your AI audit logs may be statutory, not
  optional.
- **Article 10** (data governance) — if you fine-tune, you need a data-lineage and
  bias-mitigation story.
- **GDPR overlay** — personal data through an AI component is still personal data;
  right to erasure, data minimization, and purpose limitation still apply.

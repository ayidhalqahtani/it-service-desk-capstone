# Decisions Record

## ADR-001 — Router-first architecture

**Status:** Accepted

### Context

The application contains two different workload shapes:

- low-risk grounded FAQ;
- stateful service workflows that may call tools and require authorization.

Running every request through a single agent loop would increase cost, latency, and attack surface.

### Decision

Use a router-first architecture.

FAQ requests follow a short grounded-answer path. Service requests enter a bounded workflow with structured extraction, validation, tools, and escalation.

All model calls cross one `LLMClient` interface.

### Consequences

Positive:
- simpler FAQ path;
- lower expected cost and latency;
- clearer authorization boundary;
- easier evaluation by route.

Trade-off:
- routing errors become a measurable failure mode and must be included in the golden set.

---

## ADR-002 — Authorization outside prompts

**Status:** Accepted

### Context

Track C is specifically sensitive to requester identity and authorization. User-provided text can claim any role.

### Decision

Authorization is implemented in application/session code. Side-effecting tools must call `session.authorize()` before acting.

The model may recommend an action but cannot grant permission.

### Consequences

- prompt injection cannot directly grant privilege;
- authorization can be deterministically tested;
- session fixtures are required in evaluation.

---

## ADR-003 — Indirect-injection hardening extension

**Status:** Accepted

### Context

IT workflows consume external/tool data such as knowledge articles, ticket descriptions, device metadata, and logs. That content is not inherently trusted.

### Decision

Treat retrieved and tool-returned text as untrusted. Apply a dedicated tool-result/outbound guard before it can influence subsequent actions or user-visible responses.

### Consequences

- additional guard latency;
- stronger resistance to poisoned knowledge/tool content;
- requires a dedicated five-case extension corpus.

---

## Decisions to be completed after measurement

The following decisions must be based on actual notebook results before final submission:

- commercial backend selection;
- open-weight backend selection;
- route-specific model recommendation;
- cache thresholds;
- self-host break-even;
- any reversed trade-off required by the capstone write-up.

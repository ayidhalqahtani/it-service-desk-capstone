# Capstone Design — Track C: Internal IT Service Desk

## 1. Problem statement

Enterprise IT support combines factual guidance with operations that can change system state. A useful assistant must therefore know not only what to answer, but also what it is allowed to do for the authenticated requester.

This project builds a bilingual Arabic/English internal IT service desk assistant that handles:

- IT policy and support FAQs;
- application access requests;
- asset availability and booking;
- incident triage;
- escalation to a human.

The project is intentionally scoped to Track C of the capstone.

## 2. Engineering objective

The objective is to demonstrate a production-oriented LLM application using the full course discipline:

- router-first architecture;
- provider-independent model boundary;
- commercial and open-weight backends;
- structured output validation;
- tool calling with risk classes;
- authorization outside the prompt;
- bilingual guardrails;
- evaluation with a golden set and calibrated judge;
- cost/latency metering and caching;
- measured model comparison;
- fault fallback;
- reproducible Colab execution.

## 3. Functional scope

### FAQ
Examples:
- VPN setup requirements.
- Password reset policy.
- Approved software catalogue.
- Device replacement rules.
- Supported working-from-home access methods.

### Access management
Examples:
- Request access to an internal application.
- Request a role upgrade.
- Check access-request status.

Side effects are permitted only when the authenticated session authorizes the requested action.

### Asset services
Examples:
- Check laptop or peripheral availability.
- Reserve an approved asset.
- Reject attempts to reserve on behalf of another employee without permission.

### Incident triage
Examples:
- Connectivity issue.
- Locked account.
- Suspected phishing.
- Malware/security incident.
- Critical service outage.

Security-sensitive incidents terminate automated troubleshooting and escalate according to policy.

## 4. Non-functional requirements

### Security
- Authorization must use session state.
- Prompt text cannot elevate permissions.
- Tool outputs are untrusted.
- Malicious retrieved/tool content must not override system behavior.
- Refusals must not echo attack payloads.

### Bilingual support
- Arabic and English user flows.
- Arabic-majority golden set.
- Attack corpus includes both languages.
- Structured-output pass rate reported by language.

### Reliability
- bounded tool loop;
- bounded retry/repair;
- simulated rate-limit fault;
- simulated outage;
- fallback path shown in notebook output.

### Reproducibility
The final notebook must run cleanly from a fresh Colab runtime.

## 5. Router design

Proposed top-level routes:

- `FAQ`
- `ACCESS_REQUEST`
- `ASSET_SERVICE`
- `INCIDENT`
- `ESCALATE`
- `REFUSE`

A deterministic pre-check handles obvious unsafe input before model routing where appropriate. The LLM router remains behind the common `LLMClient`.

## 6. Main structured schema

`ITServiceRequest`

Proposed fields:

```python
request_type: Literal[
    "access_request",
    "asset_booking",
    "incident",
    "status_check"
]
target: str
justification: str | None
urgency: Literal["low", "medium", "high", "critical"]
security_sensitive: bool
language: Literal["ar", "en"]
```

Identity and authorization data are intentionally not trusted when extracted from user text. They come from the authenticated session.

## 7. Tool model

### Read-only
- `lookup_knowledge`
- `check_asset_availability`
- `get_request_status`

### Side-effecting
- `create_access_request`
- `book_asset`

These call `session.authorize(action, resource)` before changing state.

### Terminal
- `escalate_to_human`

The tool ends the automated workflow and returns a hand-off record.

## 8. Guard design

The guard system will evaluate normalized text and structured context rather than raw text only.

Attack classes include:

- direct prompt injection;
- Arabic prompt injection;
- role/administrator spoofing;
- privilege escalation;
- authorization bypass;
- secret extraction;
- PII extraction;
- instruction smuggling through encoded/obfuscated text;
- malicious tool-result instructions;
- request to expose system prompts;
- request to ignore safety or authorization rules.

The legitimate corpus will include phrases intentionally similar to attack language so false positives can be measured.

## 9. Chosen extension

**Indirect-injection hardening**

Rationale: Internal service desks frequently retrieve knowledge, ticket content, logs, or asset metadata. These channels may contain attacker-controlled text. Treating tool results as untrusted and passing them through an outbound/tool-result wall is therefore directly relevant to the domain.

The extension will include at least five poisoned-tool-result cases.

## 10. Evaluation plan

Minimum golden-set properties:

- >= 40 cases;
- Arabic-majority;
- every reported stratum >= 8 cases;
- safety oversampled;
- intent, language, difficulty, and risk labels;
- expectations frozen before model comparison.

Metrics:

- task correctness;
- routing correctness;
- structured validation success;
- tool selection correctness;
- authorization behavior;
- safety pass rate;
- judge score after calibration;
- latency;
- token usage;
- cost.

The regression gate will be run once on the normal system and once on a deliberately degraded prompt/configuration to prove that it blocks a regression.

## 11. Model comparison

The same golden set will be run through:

- one commercial backend;
- one open-weight backend.

The comparison will report quality, safety, latency, and cost by slice.

The final routing recommendation will be written only after those runs.

## 12. Cost engineering

The meter will cover every model invocation.

Optimizations will be introduced sequentially and each benchmark row will include its evaluation verdict.

Candidate optimizations:

- prompt-prefix caching;
- deterministic routing shortcuts;
- exact response cache for safe FAQ cases;
- semantic cache only after a measured near-miss threshold;
- cheaper-model routing where evaluation supports it.

Target evidence for full rubric credit includes >= 60% measured cost reduction without degrading the required evaluation gates.

## 13. Reliability drill

Two scripted failures will be demonstrated:

1. simulated rate limit;
2. simulated provider outage.

The notebook will show the fallback path actually executing.

## 14. Evidence map

| Rubric area | Planned evidence |
|---|---|
| Architecture | common `LLMClient`, import assertion, router, two backends, fault transcript |
| Structured tools | schema validation, retry/repair, three risk classes, auth gate, tool logs |
| Guardrails | five-stage pipeline, versioned prompts, attack/legitimate corpora |
| Evaluation | golden set, safety asserts, judge calibration, regression gate |
| Cost/latency | 100% metering, cache evidence, before/after table |
| Model comparison | both backends on same slices, break-even analysis |
| Complete app | four captured notebook demonstrations |

## 15. Completion rule

No result in `EVALUATION_REPORT.md`, `BENCHMARKS.md`, or the final write-up will be stated as achieved until the corresponding notebook cell has been executed and captured.

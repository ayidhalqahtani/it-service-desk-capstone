# Bilingual Internal IT Service Desk — LLM Application Engineering Capstone

**Track:** C — Internal IT Service Desk  
**Programme:** SDA-AIE-213 — LLM Application Engineering, SDAIA Academy  
**Student:** [REPLACE WITH YOUR FULL NAME BEFORE SUBMISSION]  
**Cohort dates:** [REPLACE WITH OFFICIAL COHORT DATES BEFORE SUBMISSION]  
**Chosen extension:** Indirect-injection hardening

## Project overview

This capstone implements a bilingual Arabic/English internal IT service desk assistant for enterprise users. The application supports grounded IT FAQ answers, access requests, asset booking, incident triage, and escalation to a human support channel.

The system is designed around the course engineering requirements rather than as a general chatbot. It uses a router-first architecture, a single model boundary, validated structured outputs, tools with explicit risk classes and authorization, a bilingual prompt/guard pipeline, an evaluation harness, cost and latency metering, two configurable model backends, and scripted fault fallback.

## Why Track C

Track C makes authorization a first-class engineering requirement. A user's authenticated session—not prompt text—determines whether a side-effecting action is permitted. This creates a clear separation between:

- read-only operations;
- state-changing operations requiring authorization; and
- terminal escalation to a human.

It also provides realistic security cases for prompt injection, privilege escalation, unauthorized data access, and malicious content returned by tools.

## Core user journeys

1. **Grounded FAQ**
   - User asks an IT policy or support question.
   - Router selects the FAQ path.
   - The assistant answers only from the approved internal knowledge corpus.

2. **Access request**
   - User requests access to an application or service.
   - A validated request object is extracted.
   - The side-effecting tool checks `session.authorize()` before creating the request.
   - Unauthorized requests are refused safely.

3. **Asset booking**
   - User checks available devices or equipment.
   - Read-only lookup may be followed by an authorized booking action.

4. **Incident triage**
   - The assistant collects structured incident details.
   - It provides safe troubleshooting when appropriate.
   - High-risk, unresolved, or security-sensitive incidents are escalated to a human.

5. **Adversarial request**
   - Prompt injection, role spoofing, privilege escalation, PII extraction, or poisoned tool output is blocked by the guard pipeline.

## Architecture

```text
User
  |
  v
Input normalization
  |
  v
Inbound safety guard
  |
  v
Intent router
  |---------------- FAQ route ----------------------|
  |                                                 |
  |                                                 v
  |                                           Grounded answer
  |
  |---------------- Service workflow ---------------|
                                                    v
                                      Structured request extraction
                                                    |
                                                    v
                                      Validate -> retry -> repair
                                                    |
                                                    v
                                      Tool loop (bounded)
                                  /          |             \
                           read-only    side-effecting     terminal
                                          |
                                          v
                                  session.authorize()
                                                    |
                                                    v
                                         Outbound safety guard
                                                    |
                                                    v
                                                 Response
```

All model calls are routed through a common `LLMClient` boundary. Provider-specific SDK imports must exist only inside the adapter section of the notebook.

## Model strategy

The notebook will expose two model backends through configuration:

- **Commercial backend:** configured behind the `LLMClient` adapter.
- **Open-weight backend:** configured behind the same interface.

Both backends will run against the same golden set. Quality, latency, and cost will be compared by slice rather than only by a single overall score.

The final model-routing recommendation will be based on measured results from this project, not external leaderboard claims.

## Structured domain object

The main structured object is an `ITServiceRequest`, with fields such as:

- request type;
- requester identity from authenticated session context;
- target system or asset;
- business justification;
- urgency;
- incident/security indicators;
- requested action;
- preferred language.

The schema remains strict. Invalid generations are handled with a validate -> retry -> repair loop rather than weakening field types.

## Tool risk model

| Tool | Example purpose | Risk class | Authorization |
|---|---|---:|---|
| `lookup_knowledge` | Search approved IT guidance | Read-only | No state change |
| `check_asset_availability` | Check device availability | Read-only | Session required |
| `create_access_request` | Create access request | Side-effecting | `session.authorize()` required |
| `book_asset` | Reserve equipment | Side-effecting | `session.authorize()` required |
| `escalate_to_human` | End automated handling and hand off | Terminal | Policy controlled |

Every tool call will log its risk class and loop iteration.

## Prompt and guard pipeline

The implementation will use versioned prompt artifacts and a five-stage pipeline:

1. normalization;
2. inbound guard;
3. routing / task prompt;
4. tool-result inspection;
5. outbound guard.

Security goals include:

- Arabic and English attack detection;
- homoglyph/normalization handling;
- refusal without echoing malicious payloads;
- protection against privilege spoofing;
- prevention of unauthorized side effects;
- indirect-injection protection for malicious text returned by tools;
- canary preservation.

No authorization decision is delegated to the prompt.

## Evaluation design

The final golden set will contain at least 40 cases and will be:

- Arabic-majority;
- stratified by intent;
- stratified by language;
- stratified by difficulty;
- stratified by risk;
- safety-oversampled;
- at least 8 cases per reported stratum.

The real application pipeline will be executed by the evaluation harness. Safety assertions will be deterministic and must reach 100% before submission.

The LLM judge will not be used as a gate until its calibration reaches Cohen's kappa >= 0.6 against human labels.

## Cost and latency

All model calls—including router and guard calls—will be metered.

The final benchmark section will report:

- input/output tokens;
- cached input tokens where supported;
- latency;
- estimated cost;
- response-cache hit rate;
- semantic-cache near-miss safety results;
- before/after cost;
- evaluation verdict beside each optimization;
- self-host break-even based on measured throughput.

## Reliability

The notebook will include scripted demonstrations for:

- rate-limit failure;
- backend outage;
- fallback execution;
- bounded retries;
- human escalation.

The fallback transcript will be captured as notebook output.

## Repository structure

```text
it-service-desk-capstone/
├── README.md
├── CAPSTONE_DESIGN.md
├── DECISIONS.md
├── EVALUATION_REPORT.md
├── BENCHMARKS.md
├── .gitignore
├── requirements.txt
├── prompts/
│   └── CHANGELOG.md
├── data/
│   └── README.md
└── notebooks/
    └── README.md
```

The final notebook will be placed in `notebooks/` and must run from a fresh Colab runtime with **Runtime -> Run all**.

## Running the final notebook

When implementation is complete:

1. Open the capstone notebook in Google Colab.
2. Restart the runtime.
3. Select **Runtime -> Run all**.
4. Verify that the notebook demonstrates:
   - one grounded answer;
   - one completed tool action;
   - one blocked/refused attack;
   - one graceful fallback under a simulated fault.
5. Confirm the full safety suite is green.
6. Confirm both configured backends were exercised.

## Security and secret handling

Do not commit:

- API keys;
- `.env` files;
- service-account credentials;
- tokens;
- private datasets;
- generated caches;
- notebook checkpoints.

Secrets used for optional live providers must be supplied through secure runtime/environment configuration.

## Submission evidence

Before final submission, the repository will include measured—not planned—evidence in:

- `EVALUATION_REPORT.md`
- `BENCHMARKS.md`
- `DECISIONS.md`
- the executed notebook outputs

No benchmark, safety, quality, or cost result should be claimed unless it was actually produced by the notebook.

## Acknowledgement

Completed under **SDA-AIE-213 — LLM Application Engineering, SDAIA Academy**.

SDAIA Academy GitHub: https://github.com/SDAIA-Academy

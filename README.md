# Bilingual Internal IT Service Desk — LLM Application Engineering Capstone

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ayidhalqahtani/it-service-desk-capstone/blob/main/notebooks/IT_Service_Desk_Capstone.ipynb)

**Track:** C — Internal IT Service Desk  
**Programme:** SDA-AIE-213 — LLM Application Engineering, SDAIA Academy  
**Student / team lead:** Ayidh Alqahtani  
**Cohort dates:** 13 September 2026  
**Extension:** Indirect-injection hardening

## Project

This project implements a bilingual Arabic/English internal IT service desk. It supports grounded IT policy questions, structured access requests, fictional asset services, incident triage, and terminal human escalation.

The design separates low-risk FAQ traffic from service workflows. Authorization is enforced in application code through authenticated session state; prompt text cannot grant a user additional privileges.

The default Colab run uses an open-weight model and does not require an API key; this satisfies the fresh-run requirement. When `OPENAI_API_KEY` is available, the same notebook additionally exercises the commercial backend, provider-native strict structured output, native function calling, judge calibration, prompt-cache measurement, commercial cost replay, and commercial-versus-open-weight comparison on the frozen golden set. The notebook reports whether each credential-dependent evidence block actually executed rather than claiming it in advance.

## Architecture

```text
User input
   ↓
normalize_stage
   ↓
pii_stage
   ↓
inbound_guard_stage
   ↓
route_stage
   ↓
task_stage
   ↓
tool execution / tool_result_guard_stage
   ↓
outbound_guard_stage
   ↓
Response
```

Every model invocation crosses a common `LLMClient` boundary. Provider-specific SDK imports and API request details are confined to one adapter section.

## Security controls

- Arabic and English prompt-injection detection
- Saudi National ID / Iqama masking
- Saudi mobile-number masking
- email masking
- privilege-spoofing and authorization-bypass blocking
- application-level authorization for state-changing tools
- outbound secret/canary protection
- indirect-injection protection for tool results
- terminal escalation for security-sensitive incidents

PII is masked before model calls and before application logging.

## Structured outputs and tools

`ITServiceRequest` is a strict Pydantic schema. The open-weight path uses validate → retry → repair. The commercial path uses provider-native strict JSON Schema output and then applies the same Pydantic validation.

The commercial evidence path also demonstrates a real function-calling loop: the model emits function calls, the application dispatches only registered tools, authorization is checked inside side-effecting tools, results are returned as function-call outputs, and the loop is bounded.

## Evaluation

The repository contains a frozen 72-case golden set with Arabic-majority coverage and labels for language, intent, difficulty, risk, route, safety, and expected tool. The notebook reports:

- overall pipeline accuracy
- Arabic and English slices
- intent slices
- safety-stratum pass rate
- attack block rate and legitimate false-positive rate
- structured-output pass rate by language
- judge calibration and Cohen's kappa
- clean and deliberately degraded regression-gate runs

The LLM judge is allowed into the regression evidence only when its measured Cohen's kappa is at least 0.60.

## Model and cost evidence

The final credentialed run evaluates the commercial and open-weight backends on the same frozen golden set and records model IDs, quality, latency, token usage, safety, and commercial cost.

Commercial prompt-cache evidence uses provider-reported `cached_input_tokens`. Cost optimization is measured by replaying the workload rather than projecting a percentage. Self-host break-even uses measured commercial cost per request and measured local throughput.

## Run

### Colab

Use the badge at the top of this README, then choose:

**Runtime → Restart session and run all**

The notebook clones this repository and installs missing dependencies. The open-weight path is the default.

For the full commercial evidence run, add `OPENAI_API_KEY` to Colab Secrets or the runtime environment before running the notebook. No credential is stored in this repository.

### Makefile

```bash
make preflight
```

The preflight command verifies the repository structure, versioned prompts, model configuration, frozen datasets, and absence of committed secrets before the Colab run.

## Repository

```text
.
├── config/
│   └── models.json
├── data/
├── notebooks/
│   └── IT_Service_Desk_Capstone.ipynb
├── prompts/
├── scripts/
│   └── preflight.py
├── BENCHMARKS.md
├── CAPSTONE_DESIGN.md
├── DECISIONS.md
├── EVALUATION_REPORT.md
├── Makefile
├── README.md
└── requirements.txt
```

## Evidence policy

Documentation describes only behavior implemented by the repository. Live commercial metrics are reported as measured only when the captured notebook run shows the commercial backend executed.

## SDAIA Academy

Programme reference: [SDAIA Academy GitHub](https://github.com/SDAIAAcademy)


## Final scoring run

The notebook has two valid modes:

- **Keyless default:** completes end-to-end with the open-weight backend and all deterministic safety/tool demonstrations.
- **Credentialed scoring run:** additionally executes the live commercial backend, strict provider schema, native function calling, judge calibration, provider-reported prompt caching, measured cost replay, and two-backend comparison.

For a 100-point target, submit an executed credentialed run in which all hard evidence gates print PASS. The notebook is deliberately written to fail rather than overclaim if κ, safety, cached-token share, or measured cost reduction misses the rubric threshold.

# Bilingual Internal IT Service Desk — LLM Application Engineering Capstone

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ayidhalqahtani/it-service-desk-capstone/blob/main/notebooks/IT_Service_Desk_Capstone.ipynb)

**Track:** C — Internal IT Service Desk  
**Programme:** SDA-AIE-213 — LLM Application Engineering, SDAIA Academy  
**Student / team lead:** Ayidh Alqahtani  
**Cohort dates:** 13 September 2026  
**Extension:** Indirect-injection hardening

## Project

This project implements a bilingual Arabic/English internal IT service desk. It supports grounded IT policy questions, structured access requests, fictional asset services, incident triage, and terminal human escalation.

Authorization is enforced in application code through authenticated session state; prompt text cannot grant additional privileges.

The default Colab path is keyless. It executes the application, safety controls, strict structured-output evidence, authorization-aware tool calling, offline judge calibration, regression tests, cache checks, an open-weight benchmark, and four end-to-end demonstrations. A hosted-provider adapter is available through the same `LLMClient` boundary when credentials are supplied.

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
routing
   ↓
task_stage
   ↓
tool execution / tool_result_guard_stage
   ↓
outbound_guard_stage
   ↓
Response
```

Every model invocation crosses a common `LLMClient` boundary. Provider-specific SDK imports and API request details are confined to one adapter section in `scripts/capstone_app.py`.

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

PII is masked before downstream model and logging stages.

## Structured outputs and tools

`ITServiceRequest` is a strict Pydantic schema. The project demonstrates validate → retry → repair while keeping the schema unchanged.

The hosted adapter builds a provider-native strict JSON Schema request. The keyless provider simulator uses the same schema-format builder and prints the resulting request payload, including `type=json_schema` and `strict=true`, before validating the returned object locally.

Tool definitions use strict schemas and three risk classes: read-only, side-effecting, and terminal. The keyless execution path demonstrates a provider-style `function_call`, registered-tool dispatch, application authorization, and matching `function_call_output`.

## Evaluation

The repository contains a frozen 72-case golden set with Arabic-majority coverage and labels for language, intent, difficulty, risk, route, safety, and expected tool. The executable path reports:

- overall application pass rate
- Arabic and English slices
- intent slices
- safety-stratum pass rate
- attack block rate and legitimate false-positive rate
- offline judge human labels, judge labels, and Cohen's kappa
- clean and deliberately degraded regression-gate runs
- open-weight benchmark results

Safety remains a hard gate. The offline judge is deterministic and inspectable and must reach Cohen's kappa >= 0.60 on the human-labeled calibration set.

## Cost and latency

The shared model boundary records token usage, latency, backend, model, call type, and provider-reported cached input tokens when they are available.

The keyless run measures exact response caching, semantic-cache near-miss safety, and local latency. Provider-specific cache and hosted-provider cost measurements are reported only when that provider is actually exercised; simulated values are not presented as provider measurements.

## Run

### Colab

Use the badge at the top of this README, then choose:

**Runtime → Restart session and run all**

The notebook clones this repository, installs `requirements.txt`, runs `scripts/preflight.py`, and then executes `scripts/capstone_app.py`.

No API key is required for the default path. If a hosted-provider credential is available, it may be supplied through the runtime environment to enable provider-specific measurements. No credential is stored in this repository.

### Makefile

```bash
make preflight
```

The preflight command verifies the repository structure, versioned prompts, model configuration, frozen datasets, and absence of committed secrets.

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
│   ├── capstone_app.py
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

The executed notebook and generated artifacts are the source of truth for measured results. Provider-specific values are reported only when the corresponding provider was actually exercised.

## SDAIA Academy

Programme reference: [SDAIA Academy GitHub](https://github.com/SDAIAAcademy)

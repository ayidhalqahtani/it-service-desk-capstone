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

The notebook runs end-to-end from a fresh Colab runtime using the open-weight backend without requiring credentials. A commercial adapter is implemented behind the same `LLMClient` boundary and can be exercised when credentials are available, without changing the application code or the default execution path.

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

`ITServiceRequest` is a strict Pydantic schema. The open-weight path uses validate → retry → repair. The commercial adapter supports provider-native strict JSON Schema output and applies the same Pydantic validation locally.

The commercial adapter also supports function calling through a bounded tool loop. The application dispatches only registered tools, authorization is checked inside side-effecting tools, and tool results are inspected before reuse.

## Evaluation

The repository contains a frozen 72-case golden set with Arabic-majority coverage and labels for language, intent, difficulty, risk, route, safety, and expected tool. The notebook reports:

- overall pipeline accuracy
- Arabic and English slices
- intent slices
- safety-stratum pass rate
- attack block rate and legitimate false-positive rate
- structured-output pass rate by language
- judge calibration status
- clean and deliberately degraded regression-gate runs

Safety remains a hard gate. The judge contributes to decisions only when its calibration threshold is met.

## Cost and latency

The shared model boundary records input tokens, output tokens, cached input tokens when reported by the provider, latency, backend, model, call type, and estimated cost where applicable.

The notebook also demonstrates response caching, semantic-cache safety checks, local throughput measurement, and break-even analysis. Provider-specific cache and commercial-cost evidence is reported only when that backend is exercised.

## Run

### Colab

Use the badge at the top of this README, then choose:

**Runtime → Restart session and run all**

The notebook clones this repository, installs missing dependencies, and runs the complete keyless open-weight path by default.

If a commercial credential is available, it may be supplied through Colab Secrets or the runtime environment to enable the additional commercial-backend evidence. No credential is stored in this repository.

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

The executed notebook is the source of truth for measured results. Optional backend evidence is reported only when that backend is exercised in the captured run.

## SDAIA Academy

Programme reference: [SDAIA Academy GitHub](https://github.com/SDAIAAcademy)

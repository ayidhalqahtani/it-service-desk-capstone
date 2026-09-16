# Capstone design

## Scope

The application follows Track C: Internal IT Service Desk. It supports bilingual grounded FAQ, access requests, fictional asset services, incident handling, and terminal escalation.

## Request pipeline

The production request path is deliberately decomposed into named functions that are testable in isolation:

1. `normalize_stage`
2. `pii_stage`
3. `inbound_guard_stage`
4. `route_stage`
5. `task_stage`
6. `tool_result_guard_stage`
7. `outbound_guard_stage`

The orchestrator `app_pipeline` composes these stages but does not hide their individual behavior.

## Model boundary

All model calls cross `LLMClient`. Provider imports and provider-specific request formats are confined to one adapter section. Model identifiers and commercial pricing are loaded from `config/models.json`.

The default run is open-weight and keyless. A credentialed run additionally exercises the commercial backend on the same frozen evaluation set.

## Structured output

`ITServiceRequest` is strict. The commercial adapter uses provider-native JSON Schema structured output with `strict=true`; the resulting object is still validated locally with Pydantic. The open-weight path uses validate → retry → repair with validation errors fed into subsequent attempts.

## Function calling

The commercial adapter exposes strict function definitions to the Responses API. It reads returned `function_call` items, executes only registered application tools, sends `function_call_output` items back to the model, and stops after a bounded number of iterations. Authorization remains inside application tools.

## PII

Saudi National ID / Iqama numbers, Saudi mobile numbers, and email addresses are masked before model calls and logging. The PII stage is deterministic and unit-tested in Arabic and English examples.

## Evaluation

The frozen 72-case golden set is Arabic-majority and includes intent, language, difficulty, risk, route, safety, and tool expectations. Safety must remain at 100%. A deliberately weakened inbound-guard prompt proves that the regression gate detects a seeded degradation.

Judge calibration uses the configured stronger commercial judge when credentials are present. The judge is excluded from gate decisions unless Cohen's kappa is at least 0.60.

## Cost and model comparison

The credentialed evidence run replays the same golden set on both backends. Provider-reported usage drives cost and prompt-cache measurements. Optimization is replayed and accepted only when its evaluation verdict remains green. Break-even is based on measured commercial cost per request plus measured local throughput.

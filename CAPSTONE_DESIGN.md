# Capstone design

## Scope

The application follows Track C: Internal IT Service Desk. It supports bilingual grounded FAQ, access requests, fictional asset services, incident handling, and terminal escalation.

## Request pipeline

The production request path is decomposed into named functions that can be tested independently:

1. `normalize_stage`
2. `pii_stage`
3. `inbound_guard_stage`
4. routing
5. `task_stage`
6. `tool_result_guard_stage`
7. `outbound_guard_stage`

The orchestrator `app_pipeline` composes these stages while keeping each control inspectable.

## Model boundary

All model calls cross `LLMClient`. Provider imports and provider-specific request formats are confined to one adapter section. Model identifiers are loaded from `config/models.json`.

The default path is keyless and uses the configured open-weight model. A hosted-provider adapter is available through the same boundary when credentials are supplied.

## Structured output

`ITServiceRequest` is a strict Pydantic model. The project demonstrates validate → retry → repair and retains the same schema throughout the sequence.

The hosted adapter builds a provider-native strict JSON Schema request. A keyless provider simulator uses the same schema-format builder and prints the resulting request payload so `type=json_schema`, the full schema, and `strict=true` can be inspected without credentials.

## Function calling

Tool definitions use strict JSON Schema and are grouped into read-only, side-effecting, and terminal risk classes. Authorization remains inside application tools and is based on authenticated session state rather than user text.

The keyless execution path simulates a provider `function_call`, dispatches only a registered tool, enforces authorization, and produces a matching `function_call_output`. The hosted adapter remains available for live provider execution when configured.

## PII and guardrails

Saudi National ID / Iqama numbers, Saudi mobile numbers, and email addresses are masked before downstream processing. The pipeline also includes normalization, inbound prompt-injection checks, an indirect-injection wall for tool results, and an outbound secret/canary guard.

## Evaluation

The frozen 72-case golden set is Arabic-majority and includes intent, language, difficulty, risk, route, safety, and tool expectations. Safety remains a hard gate at 100%. A deliberately weakened Arabic guard path is used to verify that the regression gate detects degradation.

Judge calibration is demonstrated keylessly with a deterministic, inspectable offline judge applied to the human-labeled calibration set. The notebook prints the human labels, judge labels, and Cohen's kappa and requires kappa >= 0.60.

## Cost and latency

The common model boundary records token usage and latency. The keyless path measures exact response caching, semantic-cache near-miss safety, and local latency. Provider-reported cached-input tokens and hosted-provider cost are reported only when a hosted provider is actually exercised; simulated or local values are not presented as provider measurements.

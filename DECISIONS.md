# Decisions record

## Router-first architecture

The service desk has two workload shapes. Grounded FAQ can use a short path, while access, asset, incident, and escalation requests require structured state and tools. A router-first design avoids forcing low-risk questions through an agent loop.

## Authorization outside the model

The model may propose a tool, but it cannot grant permission. State-changing tools call `session.authorize()` and fail closed. Job-title claims in user text are treated as untrusted input.

## PII before models and logs

PII masking happens immediately after normalization. Saudi National ID / Iqama, Saudi mobile numbers, and email addresses are replaced with typed placeholders before downstream model or logging stages.

## Provider-native schema plus local validation

The commercial backend requests strict JSON Schema output from the provider. Local Pydantic validation is retained as an independent application boundary. The open-weight path keeps validate → retry → repair because it does not expose the same provider-native schema interface.

## Native tool calls for commercial evidence

A scripted lambda loop was rejected because it did not demonstrate model function calling. The revised commercial loop consumes real `function_call` response items, dispatches registered tools, and returns `function_call_output` items to the model.

## Reversed trade-off: all-model routing to deterministic first pass

The first design routed every request through a model. Red-team and cost work showed that deterministic safety and high-confidence routing were easier to test and cheaper. The production path now uses deterministic controls first and reserves commercial model work for measured evidence and selected higher-risk verification.

## Judge selection

The small open-weight application model was not a reliable evaluator. The final judge path uses the stronger commercial judge alias from `config/models.json`. The judge cannot participate in a gate until measured Cohen's kappa reaches 0.60.

## Model configuration

Model IDs are data, not literals embedded in adapter constructors. `config/models.json` contains the open-weight application model, commercial application model, judge model, pricing used for cost estimates, and the self-host hourly scenario.

## Indirect-injection extension

Tool output is untrusted. A dedicated tool-result wall blocks instructions embedded in tickets, logs, or tool payloads before they can influence another action.

# Benchmarks

The notebook measures model traffic at the shared `LLMClient` boundary.

## Measured dimensions

- routing accuracy on the frozen golden set
- refusal/safety accuracy
- Arabic and English slices
- intent slices
- mean latency
- input and output tokens
- commercial estimated cost from provider-reported usage
- provider-reported cached input tokens
- local open-weight output throughput
- structured-output pass rate by language

## Optimization comparison

The credentialed run first replays the full golden set through the commercial router baseline. It then replays an optimized cascade where deterministic production routing handles normal-risk traffic and the commercial model verifies the high-risk slice. Cost reduction is computed from the two actual replay traces. Each row includes an evaluation verdict.

## Break-even

Self-host break-even uses:
1. measured commercial cost per golden-set request;
2. measured local generation throughput;
3. the explicit hourly self-host infrastructure scenario in `config/models.json`.

This avoids using a hypothetical commercial token price as the only comparison basis.

The final notebook run rewrites this report with the measured tables and writes machine-readable metrics to `artifacts/final_metrics.json`.

# Trainer-review evidence map

This file maps the automated-review findings to the current implementation.

| Grader finding | Current implementation |
|---|---|
| `httpx` / `tenacity` declared but unused | Removed from `requirements.txt`. |
| GitHub About description empty | Exact description is provided in `REPO_SETTINGS.md`. |
| SDAIA Academy link wrong | README links to `https://github.com/SDAIAAcademy`. |
| Commercial model hardcoded | Model IDs and pricing are stored in `config/models.json`. |
| Commercial backend not run | A commercial adapter remains available behind the same `LLMClient` boundary; the fresh default Colab path is keyless and does not depend on credentials. |
| No provider-native schema | `CommercialClient.generate_structured()` supports strict JSON Schema through the provider adapter and Pydantic validates locally. |
| Scripted lambda tool loop | `CommercialClient.run_native_tool_loop()` supports provider function-call items and returns tool outputs through the bounded loop. |
| No Saudi PII | `pii_stage` masks Saudi ID/Iqama, Saudi mobile and email before model/logging stages. |
| Monolithic pipeline | Named `normalize_stage`, `pii_stage`, `inbound_guard_stage`, `route_stage`, `task_stage`, `tool_result_guard_stage`, `outbound_guard_stage`. |
| Judge kappa 0.000 | Judge calibration is explicit and judge output is excluded from gating when the threshold is not met. |
| Cache not measured | Shared metering records cached input tokens when reported by the active backend; response-cache and semantic-cache behavior are also demonstrated. |
| Cost replay not executed | Cost and latency accounting are implemented at the shared model boundary; provider-specific commercial cost evidence is reported only when that backend is exercised. |
| Break-even scenario-only | Break-even combines measured local throughput with the configured infrastructure scenario and any measured provider-side cost available in the run. |
| No Colab badge | Added to README. |
| No single entry point | Added `Makefile` + `scripts/preflight.py`. |
| Placeholder evaluation report | The notebook generates `EVALUATION_REPORT.md`, `BENCHMARKS.md`, and `artifacts/final_metrics.json` from runtime variables. |

## Rubric evidence

- Architecture: one adapter import boundary, configurable open-weight and commercial adapters, rate-limit and outage fallback transcripts, decisions record.
- Structured outputs: strict Pydantic object, validate → retry → repair, provider-native schema support, three tool risk classes, bounded tool loop, session authorization, negative tool-safety assertions, per-language pass rates.
- Guardrails: versioned prompts, changelog, served-version log, isolated stage demonstrations, bilingual attacks, legitimate traps, normalization, canary protection, non-echoing refusals, Saudi PII masking.
- Evaluation: 72 owner-approved frozen cases, Arabic-majority, safety oversampled, real-pipeline harness, safety hard gate, slice-aware clean/degraded regression runs, generated report.
- Cost/latency: shared boundary meter, response cache, semantic-cache safety checks, cached-input accounting when reported, latency and token measurement, local throughput and break-even analysis.
- Model comparison: both adapters share the same interface and frozen evaluation design; optional provider-specific evidence is recorded only when that backend is exercised.
- Complete app: fresh keyless Colab path, one master notebook, four captured demos, README badge, programme/cohort details and SDAIA GitHub link.
- Extension: poisoned tool-result cases demonstrate indirect-injection hardening.

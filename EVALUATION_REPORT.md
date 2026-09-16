# Evaluation report

## Evaluation set

The frozen project set contains 72 cases and is Arabic-majority. It covers FAQ, access requests, asset services, incidents, security escalation, and refusal. Cases include language, intent, difficulty, risk, expected route, safety expectation, and expected tool.

The deterministic safety and routing path is the acceptance baseline. Safety is a hard gate: the refusal/safety stratum must remain at 100%, and the legitimate false-positive rate is reported beside attack blocking.

## Development findings

An expanded red-team run exposed missed role-spoofing, secret-extraction, and approval-bypass phrasings. The guard was strengthened without changing the frozen expected labels, preserving the evaluation set as a stable reference.

An early judge configuration produced Cohen's kappa of 0.000 and is treated as a failed calibration. Judge decisions are excluded from gating unless measured kappa reaches at least 0.60.

## Runtime outputs

The notebook writes measured runtime metrics to `artifacts/final_metrics.json` and can refresh this report and the companion benchmark report from the executed run. The executed notebook remains the source of truth for provider-specific measurements.

## Known limitations

The IT policies, assets, users, and service records are synthetic. The project demonstrates engineering behavior rather than a production connection to a real identity provider, CMDB, service-management platform, or enterprise knowledge base.

The open-weight model is intentionally small enough for a standard Colab runtime; its language quality is not expected to match a larger hosted model. Provider-specific cost and cache measurements depend on the backend exercised during the run.

The golden set is project-authored. A production release would add independently authored held-out cases and live operational monitoring.

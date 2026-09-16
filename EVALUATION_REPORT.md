# Evaluation report

## Evaluation set

The frozen project set contains 72 cases and is Arabic-majority. It covers FAQ, access requests, asset services, incidents, security escalation, and refusal. Cases carry language, intent, difficulty, risk, expected route, safety expectation, and expected tool.

The deterministic safety and routing path is the acceptance baseline. Safety is a hard gate: the refusal/safety stratum must remain at 100%, and the legitimate false-positive rate is reported beside attack blocking.

## Captured development findings

The first expanded red-team run exposed missed role-spoofing, secret-extraction, and approval-bypass phrasings. The guard was hardened without changing the frozen expected labels. This sequence is retained in the project history because it demonstrates a real regression-and-remediation cycle.

The first judge attempt used the small application model and produced Cohen's kappa of 0.000. That result is treated as a failed calibration, not as evidence of a working judge. The revised notebook uses the configured stronger commercial judge for the credentialed scoring run and excludes judge decisions unless kappa is at least 0.60.

## Final-run outputs

During the final credentialed Colab run, the notebook writes the measured tables used for trainer review to `artifacts/final_metrics.json`, rewrites this report with the captured results, and writes the companion benchmark report. The executed notebook remains the source of truth for provider-specific measurements.

## Known limitations

The IT policies, assets, users, and service records are synthetic. The project demonstrates engineering behavior rather than a production connection to a real identity provider, CMDB, service-management platform, or enterprise knowledge base.

The open-weight model is intentionally small enough for a standard Colab runtime; its language quality is not expected to match a larger hosted model. Commercial cost and cache measurements therefore depend on the model alias and credentialed run captured in the notebook.

The golden set is project-authored. A production release would add independently authored held-out cases and live operational monitoring.

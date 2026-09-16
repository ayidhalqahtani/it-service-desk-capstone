# Prompt changelog

## Version 1

The initial production prompt set separates routing, grounded FAQ answering, structured service extraction, guard layers, repair, judging, and cache measurement so each responsibility can be evaluated independently.

During testing, the inbound guard under-detected several role-spoofing and secret-extraction phrasings. The guard implementation was strengthened while the frozen evaluation expectations remained unchanged.

## Version 1.1

- Added `service_retry_v1.txt` so structured extraction follows validate → retry → repair without inline prompt instructions.
- Added `guard_inbound_degraded_v0.txt` as a test-only seeded prompt for regression-gate validation.
- Added an explicit policy mode to the production inbound-guard artefact.
- Extended the stable cache-probe prefix for repeatable cache measurement.
- Added `judge_v2.txt` with clearer evaluation criteria after the earlier judge configuration failed calibration.
- Added `tool_agent_v1.txt` for the model-facing function-calling policy.
- Kept the production guard prompt and degraded regression prompt as separate versioned artefacts.

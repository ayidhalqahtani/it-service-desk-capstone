# Prompt changelog

## Version 1

The first production prompt set separates routing, grounded FAQ answering, structured service extraction, the three guard layers, repair, judging, and cache measurement. The split keeps each responsibility narrow enough to evaluate independently.

During development, the initial inbound guard under-detected several role-spoofing and secret-extraction phrasings. The guard implementation was hardened while the frozen evaluation expectations were left unchanged. This is recorded as a control improvement rather than hidden as a data change.

## Final submission refinement

- Added `service_retry_v1.txt` so the live structured-output path follows validate → retry → repair without inline prompt instructions.
- Added `guard_inbound_degraded_v0.txt` as a test-only seeded prompt for the regression-gate demonstration.
- Added an explicit policy mode to the production inbound-guard artefact.
- Extended the stable cache-probe prefix so provider-reported prompt caching can be measured on a sufficiently long repeated prefix.


## Trainer-review correction

- `judge_v2.txt` replaces the underspecified judge prompt after the small application model failed calibration.
- `tool_agent_v1.txt` defines the model-facing function-calling policy.
- Production guard prompt remains frozen for the clean regression run; the deliberately degraded prompt remains a separate versioned artifact.

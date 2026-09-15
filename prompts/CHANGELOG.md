# Prompt Changelog

## v1 prompt set

Initial prompt artifacts for the Track C Internal IT Service Desk capstone.

- `router_v1.txt` — route classification
- `faq_v1.txt` — grounded FAQ answering
- `service_v1.txt` — structured service extraction
- `guard_inbound_v1.txt` — inbound attack detection
- `guard_tool_result_v1.txt` — indirect-injection protection
- `guard_outbound_v1.txt` — outbound safety check
- `repair_v1.txt` — strict schema repair
- `judge_v1.txt` — evaluation judge

### Governance rule
Any prompt change must:
1. create a new versioned artifact;
2. record the reason here;
3. rerun the relevant evaluation slices;
4. record whether the regression gate passed.

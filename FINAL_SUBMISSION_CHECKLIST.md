# Trainer-review submission checklist

- [ ] Set the GitHub About description exactly as shown in `REPO_SETTINGS.md`.
- [ ] Upload this correction package to the repository.
- [ ] Add `OPENAI_API_KEY` to Colab Secrets for the final scoring run.
- [ ] Open the notebook using the README Colab badge.
- [ ] Choose Runtime → Restart session and run all.
- [ ] Confirm judge calibration prints Cohen's kappa >= 0.60.
- [ ] Confirm both backend rows show `executed: true`.
- [ ] Confirm native tool-call transcript is printed.
- [ ] Confirm prompt-cache evidence shows provider-reported cached tokens.
- [ ] Confirm the before/after optimization table is printed and carries evaluation verdicts.
- [ ] Confirm all four end-to-end demos pass.
- [ ] Confirm the final report-generation cell succeeds.
- [ ] Save the executed notebook back to GitHub.
- [ ] Commit the generated `EVALUATION_REPORT.md`, `BENCHMARKS.md`, and `artifacts/final_metrics.json`.
- [ ] Verify no secret was committed.


## Non-negotiable final gates

Do not submit the trainer-review run unless the executed notebook shows all of the following:

- Safety stratum = 1.0
- Attack block rate ≥ 0.95
- Legitimate false-positive rate = 0.0
- Cohen's kappa ≥ 0.60
- Open-weight backend executed = True
- Commercial backend executed = True
- Provider cached-input share ≥ 0.65
- Measured cost reduction ≥ 0.60
- Every cost optimization row has eval_verdict = PASS
- Architecture import-boundary assertion passes
- All four final demos print PASS
- Final report-generation cell prints PASS

The GitHub About description must also be set before submission. This setting cannot be changed by committing repository files.

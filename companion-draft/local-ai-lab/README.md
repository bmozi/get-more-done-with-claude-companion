# Local AI: preparation package

Companion to Chapters35,37 and56. The [arrival runbook](arrival-runbook.md) is a proposed procedure for a future workstation. It is not an installation report. The earlier Merlin plan is audited in `research/11-prior-local-plan-audit.md`; no Merlin code or settings were changed.

- [Personal purchase worksheet](purchase-decision.md): compare your own workload, existing equipment, hosted options and upgrades.
- [Model-source receipt](model-intake-template.json): blank provenance/license/format decision record.
- [Arrival ledger](arrival-ledger.csv): all target-machine steps remain unrun.
- [Cost worksheet](cost-worksheet.md): cash, time and allocation separated; fictional arithmetic in cost-example.json.
- [Scripted practice cases](cases.json) and [separate reviewer key](answer-key.json): L1–L4 test note extraction, missing year/owner, cancellation and superseded assignments. They are additional tests, distinct from Chapter56's A1–A4 open-work classification exercise. Neither set is a captured model result.
- `preflight.py`: read-only selected host inventory with new output file; excludes serial IDs. Actual current-host output is retained under planning/reviews/local-ai-preparation/, explicitly not the planned Mac Studio.
- `make_request.py`: writes exact request JSON without invoking a model or downloading anything. Its cloud-name filter is only a basic guard; it does not prove locality. Inspect the actual runtime and model receipt.

Run preparation checks from the repository root:

```sh
python3 -m unittest discover -s companion-draft/local-ai-lab -v
```

These check fixture structure, request construction, refusal to overwrite and cost arithmetic. They do not test local-model performance, installation, a network boundary or human learning.

The arrival runbook includes the future local API call and recording instructions. No purchase, install, model download, paid API, server change, memory tuning or external communication has occurred as part of preparing this package.

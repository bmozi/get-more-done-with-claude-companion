# Compare answers before combining them

Two assistants recommend different rooms for your workshop. Which one should you trust? Start with the quotes and registration records. The name above an answer cannot settle the arithmetic.

This small lab tests evidence handling, stale information, counting, budget comparison, and a bounded runbook. It is one starting kit for the book's evidence-based recommendation experiment. It does not test video, images, coding, or broad model intelligence. All input data is fictional and assistant-authored under John's direction. No measured model results are supplied by this kit.

## Files and first run

- `evidence-packet.md`: the only source packet given to each model.
- `cases.json`: common instruction and five distinct task prompts.
- `answer-key.json`: expected facts for reviewers; keep it out of model conversations.
- `rubric.md`: scoring and failure rules fixed before runs.
- `results-template.csv`: header-only results ledger. Copy it for actual observations.
- `validate_fixture.py`: standard-library arithmetic and consistency check; no model calls.

Choose C3 for a quick first run. Start a fresh conversation. Paste the common instruction from `cases.json`, the complete evidence packet, and C3's prompt, in that order. Save the exact input and complete raw output. Do not paste the answer key or this protocol into the model conversation. A preview run helps check the procedure; it is not a comparative result.

## Fair comparison protocol

1. Register the exact model IDs, app or API, date, settings, tool access, context/memory state, word limit, and any unavailable settings before testing. Use fresh contexts, the identical packet and instructions, and no web or external tools in the common-input condition. Record unavoidable product differences. Local hardware and quantization belong in the record for local runs.
2. Keep a pilot separate. If you revise a prompt after seeing results, preserve the earlier version and failures. These five published cases are evaluation fixtures, not secret held-out tests. For a claim about generalization, prepare unseen cases and independently check their answers before final testing; use the same held-out cases for every condition.
3. Run each of C1–C5 three times per single-model condition in fresh contexts. Shuffle condition order across repetitions. Fifteen observations per condition offer exploratory coverage, not statistical proof. Keep errors, refusals, empty outputs, and timeouts. Set the timeout and retry rule in advance; a retry is another logged attempt, never a replacement for a failure.
4. Obtain independent initial answers from A and B before either sees the other's output. Preserve them unchanged. Have a reviewer assess anonymous copies without provider names or self-assessments. Keep the label-to-model mapping separate. For a solo researcher, genuine blinding may be impractical; record that limitation instead of claiming it.
5. Only then run reconciliation. Give the reconciler the original packet, common instruction, case prompt, and verbatim anonymous answers. Use the reconciliation prompt below. Log the reconciler's model and all inputs. A+B+reconciler is one workflow condition; its total cost and time include every stage, including failed stages.
6. Compare with each strong single-model baseline, plus a same-model review workflow with a comparable number of calls. Otherwise added effort may look like an advantage from provider diversity. Use the same review prompt and evidence access. If you also test each product's best supported tools, report that as a separate condition; do not merge it with the no-tool baseline.
7. Score with the fixed answer key and rubric. Record the specific source and output passage behind each finding. Human correction effort starts when review begins and ends when a corrected usable result exists. Log inability to repair within the predeclared time budget. Separate inference time, full elapsed workflow time, and human review time.
8. Report case-level outcomes and failures before aggregates. Compare against the best eligible single-model result, and examine tradeoffs: did reconciliation correct an error, introduce one, or only rewrite correct prose? Model agreement is not a check against evidence. Do not generalize these five cases to an entire model family.

### Reconciliation prompt

> Review the original evidence packet and the two anonymous answers below. Resolve each material disagreement against specific source IDs, including disagreements about missing facts and permitted actions. Do not decide by majority vote, confidence, or writing style. Return a corrected answer to the original case, followed by a short correction log that names the original claim, the relevant evidence, and your decision. Preserve unresolved facts as unresolved. Follow the original no-action restriction and 450-word limit.

Supply the packet and case prompt again: the intermediate answers must not become the only evidence. Randomize answer order and log it. If either initial stage fails, retain its failure; report the combined workflow as incomplete unless a fallback rule was declared before testing. Do not silently substitute another model.

## Record what actually happened

Use a unique run ID such as `C3-A-r1`. Store an exact request, raw output, and any error log under a folder with that ID. For a combined run, retain all stages and reference their IDs in `stage_run_ids`. Record unavailable metrics as `unknown`, not zero. `billed_cost` is observed API cost when available; subscription allocation and local electricity estimates are separate notes, not equivalent measured charges. Never infer token use from character count and label it measured.

The CSV has one row per attempted stage or completed workflow; use `record_type` to distinguish them and avoid double counting. Status is `completed`, `failed`, `timeout`, `unavailable`, or `incomplete`. Keep blank templates blank. A model output may be technically completed yet fail every quality check.

## Visual to build from real results

A useful diagram places two independent answer boxes beside each other, both connected to the same original evidence. Their arrows lead to reconciliation, which also receives that original evidence. A separate arrow sends every output to the reviewer. This makes the central lesson visible: evidence is preserved through the handoff. Create comparison charts only after observations exist, label sample size and conditions, and retain case-level results beneath the chart.

## Local fixture check

From this directory run `python3 validate_fixture.py`. It recomputes the registration counts and venue totals from the packet and compares them with the reviewer key. It does not validate a model's answer, prove teaching effectiveness, or establish any provider's capabilities.

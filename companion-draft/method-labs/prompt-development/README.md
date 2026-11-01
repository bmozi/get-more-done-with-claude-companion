# Chapter 43: test an instruction against its evidence

This is a fictional prompt-testing kit. A separate ten-response local Qwen2.5 1.5B pilot is retained under `research/pilots/prompt-development-2026-10-18/` at the repository root. The ledger template remains blank for your own attempt. Use Python only for the other method labs; this exercise can be done in a chat interface.

1. Read D1 in `cases.json` and predict a record before consulting `reviewer-key.json`.
2. In a fresh conversation, submit `baseline.txt` plus D1 notes. Save the exact input and raw response. In another fresh conversation, repeat with `revised.txt` and the same notes. Keep model, interface, settings and available tools the same; record differences you cannot control.
3. Review each output against the notes and the separate key. Count specific unsupported commitments, missing decisions, invented dates, incorrect owners and unsupported references. Count false alarms when a real decision is incorrectly withheld. Save row-level reasons, not just a total.
4. Repeat D2 to test the owner change. Preserve failures before revising. A second prompt is a candidate improvement until actual evidence supports adopting it.
5. Try E1–E3 without supplying the reviewer key. These public examples practice evaluation. They are not secret or genuinely held out from an author or model that has seen this repository. For a fresh transfer check, have a reviewer prepare new fictional notes and expected outcomes before running either prompt. Once you tune against those answers, label them development cases.

Copy the blank ledger to a new run-specific file. Save complete prompts, source versions and raw responses alongside it. Record repeated attempts separately; do not keep only the best answer. A small set cannot establish general reliability, and different models' agreement cannot establish correctness. No automatic grader is supplied: source-grounded review is the teaching task.

E2 deliberately allows an agreed next step without an assigned owner. Do not force that into an assigned-action row merely to fill the schema. Preserve the unresolved capacity statements and the actual agreement. Different faithful wording is acceptable; the reviewer key specifies meaning, not a required sentence.

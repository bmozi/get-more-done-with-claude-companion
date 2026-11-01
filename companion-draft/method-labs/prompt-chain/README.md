# Chapter 44: preserve the evidence between steps

This runnable reference uses the exact fictional venue facts in Chapter 44. It demonstrates a checked handoff and a stopped pipeline. It uses ordinary Python calculations and fixed explanations, not Claude or any other model. No network, accounts, paid calls, bookings, or messages are involved.

## Run from this directory

Use the book’s Python 3.10-or-newer practice setup from Chapter 27. From the book repository root, run `cd companion-draft/method-labs/prompt-chain` once, then check `python3 --version`. The commands below assume that lab is your current directory.

```sh
python3 runner.py --case base
python3 runner.py --case occupancy11
python3 runner.py --case omitted-cleaning
python3 -m unittest -v test_runner.py
```

The first two commands exit successfully and print complete JSON records. The omitted-cleaning command deliberately exits with code 2 and prints a rejected handoff with `calculation` and `explanation` set to null. That rejection is the expected outcome, not a setup failure. To retain an observation, redirect its output to a new file you choose; the runner itself does not save or overwrite files.

## Inspect the stages

`source.json` is a hand-transcribed structured version of B1, B2, Q1, Q2, and U1 from the chapter. The extractor maps those fields into an evidence packet with source IDs. It does not parse arbitrary language. The fidelity check requires that packet to match the source exactly before any calculation or explanation runs.

For the base case, Elm's venue charge is $370 and total commitment $470, which exceeds the $450 budget by $20. Pine's commitment is $420, leaving $30. With ten people, Elm has two spare places and Pine has none. Pine alone meets the stated constraints; its availability remains unconfirmed and booking is not established.

The eleven-person case changes only occupancy and its source version. Pine then fails capacity while Elm still fails the budget. Neither qualifies. The omitted-cleaning case instead corrupts Elm's intermediate charges while preserving the original source. The validator stops the pipeline before that error can become a recommendation. The rejected output retains the faulty packet for diagnosis.

`expected.json` contains the full designed answer records, authored separately from runner execution. Tests compare every stage, source ID, explanation, and uncertainty field. They also inject false availability, a wrong source ID, a dropped reserve, a changed volunteer rule, and an invented booking. CLI checks inspect actual printed JSON, exit codes, and original-source preservation.

## Limits and a real prompt-chain trial

This is a fixed reference for two attendance cases and one corruption case. Explanations are deliberately fixed to those cases; it is not a general venue recommender. Exact dictionary matching is appropriate to this small schema but is not semantic validation of arbitrary prose. Passing tests establishes behavior of this local reference only, not model accuracy or reader learning.

For a model trial, preserve the chapter's exact source packet and prompts, and retain each raw model output before correction. Compare extracted facts with the originals. Supply those originals to downstream stages as well. Record model/interface/date, corrections, rejected handoffs, and full review time. Keep the reference key away from the model being tested. Compare the chain with one well-specified request on the same evidence. No such trial is performed by these commands.

The lab's source, expected records, and code are assistant-authored teaching artifacts under John's direction. Numeric outputs are fictional reference arithmetic, not observed productivity gains.

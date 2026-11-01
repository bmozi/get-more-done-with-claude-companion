# Recover one report without creating it twice

This Chapter 47 companion is an executable local reference, using fictional records and Python's standard library. It calls no AI service, installs no scheduler and sends nothing. Python 3.10 or newer is the reader prerequisite. Use a local writable folder; this exercise does not validate network filesystems or production recovery.

## Run the interrupted case

Open a terminal at the repository root. Check `python3 --version`. These commands deliberately use a fresh folder so previous results cannot silently change your experiment:

```sh
LAB_RUN_DIR=$(mktemp -d)
python3 companion-draft/recovery-lab/report_runner.py --db "$LAB_RUN_DIR/runs.sqlite" --source companion-draft/recovery-lab/maintenance.json --period 2026-11-02 --run-date 2026-11-02 --fault after-prepare
python3 companion-draft/recovery-lab/report_runner.py --db "$LAB_RUN_DIR/runs.sqlite" --inspect
```

The first command exits with code 2 by design. The ledger records `interrupted`; `reports` is empty. Prepared JSON is saved as attempt detail, but it is not a completed report. This is a controlled interruption at a named checkpoint, not a power-failure test.

Repeat the first command without `--fault after-prepare`. It should say `completed`. Inspect again: the report contains `due: ["H1"]` and `unknown: ["H4"]`. The interrupted attempt remains in history. Run the same ordinary command once more: expect `skipped`, with one report still present.

## Lose the acknowledgement

Use a new `LAB_RUN_DIR=$(mktemp -d)` and run with `--fault after-commit`. The command exits with code 2 and reports `acknowledgement-lost`. Inspect before retrying: the report already exists. A retry must skip this period. A failed-looking response can mean that the action finished but the caller did not receive confirmation.

For changed input, copy maintenance.json into your temporary folder and change H2's due date to `2026-11-02`. Use a fresh database and expect H1 and H2 due, with H4 still unknown. Do not delete a completed report to force an undocumented correction; in a real workflow, define an explicit revision process.

## Explain the mechanism

The database is the publication destination. A single transaction checks for an existing period, validates the input, inserts a completed report, and records its attempt. The period is a primary key, so a second completed row for the same period is rejected. A write transaction serializes competing writers. These are software rules; a sentence in a prompt would not enforce them. The complete JSON report is stored in the database, avoiding a separate file-write-versus-ledger gap.

An interrupted attempt can be retried. The reference recomputes the small report from the currently supplied, checked source; it does not reuse a possibly stale prepared draft. Attempts that read the source retain its hash. Skipped attempts do not reread input; unreadable sources have no hash. Source freshness is measured against execution date, while the due cutoff remains the reporting period. A late November 9 report run on November 10 therefore needs a fresh source but still counts tasks due by November 9.

A report database cannot atomically commit an external email or payment along with its own row. Do not copy this exercise into a messaging workflow and claim exactly-once delivery. Such integrations need a destination-supported duplicate-prevention identifier or reconciliation of the actual destination state before another action.

## Check the failures

```sh
python3 -m unittest discover -s companion-draft/recovery-lab -v
```

The tests cover ordinary/duplicate runs, controlled interruption and recovery, lost acknowledgement, stale/late input, missing input, changed due date, invalid records and containers, read-only inspection of missing or wrong-schema ledgers, and competing connections. Captured CLI output and environment details are in `planning/reviews/adversarial-2026-10-18/recovery-execution.json`.

Unexpected process termination before commit can leave no attempt row; this design does not promise a durable trace of every machine failure. Detect missed periods by comparing an independently maintained expected schedule with the ledger. This lab supplies no such scheduler/monitor and does not prove unattended operation. Database corruption, disk-full behavior and deployment shutdown still need separate tests.

## Try it without the answer beside you

Before running the lost-acknowledgement case, predict whether the report exists. Then use inspection to choose between retrying, correcting input and investigating the destination. Explain why changing the period identifier to evade a duplicate check would make the result less trustworthy.

Keep your commands, output, original input, modified input and explanation. A passing script demonstrates reference behavior; your unaided explanation and successful changed-condition attempt provide different evidence.

Technical sources checked October 18, 2026: [SQLite transaction control](https://www.sqlite.org/lang_transaction.html) and [atomic commit](https://www.sqlite.org/atomiccommit.html). These document database mechanisms and assumptions, not performance of this lab or an AI product.

# Chapter 41: read-only registration runbook reference

This small Python reference implements the fictional counting cases in Chapter 41. It is ordinary deterministic software, not an agent, scheduled automation, or captured Claude run. It does not approve a report or contact anyone. Use the book’s Python 3.10-or-newer practice setup from Chapter 27; no third-party packages or external service are needed.

From the book repository root:

```sh
python3 companion-draft/method-labs/runbook/runner.py --case normal
python3 companion-draft/method-labs/runbook/runner.py --case missing
python3 companion-draft/method-labs/runbook/runner.py --case amendment
python3 -m unittest discover -s companion-draft/method-labs/runbook -p 'test_*.py' -v
```

The runner finds `fixtures.json` beside its own file, reads it, and prints JSON to standard output. It never writes inputs or report files. You may redirect output to a separately named draft if desired; do not use the source fixture as the destination. Fixtures are fictional undated practice exports, not a live weekly input.

## Practice before consulting the key

Read each case in `fixtures.json`. Predict the source-row count, distinct IDs, full people total if justified, any incomplete subtotal, and required clarification. Run the command, then compare against the separately authored `reviewer-key.json`. The runner does not load that answer key.

- Normal: the third source row is explicitly identified as an accidental copy. Remove only that copy from the derived count.
- Missing: R03 has no count. Its people count stays unknown; show the known subtotal separately from a full total.
- Amendment: the repeated R02 record is an amendment with unspecified meaning. Preserve both records and stop before deduplication or attendance calculation.

`distinct_registration_ids` counts identifier values in the source. Even in the amendment case, four distinct IDs can be observed. That does not establish how amendments affect attendance. `people: null` means no full total is established, never zero. `known_subtotal` is populated only for the missing-count case, where record meaning is established. Amendment semantics block that subtotal too. Excluded row numbers are one-based source positions.

All outputs remain drafts awaiting coordinator review, including complete counts. The expected normal result does not establish approval, delivery, or attendance. The tests include unknown-count handling, amendment handling, changed zero counts, invalid counts, undeclared duplicates, and unchanged input bytes across actual CLI calls. Their success verifies this reference against those cases, not an LLM's behavior or arbitrary registration systems.

To use this as an AI exercise, give an assistant only the fictional fixture and Chapter 41 procedure first. Retain its actual output separately, then inspect it against the key and original records. A model result must not overwrite the expected key. Record disagreements and corrections rather than treating the Python result as evidence that a model succeeded.

`test-results.txt` records the local reference test run; it is not a Claude execution transcript.

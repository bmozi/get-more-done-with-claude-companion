# Chapter 42 playbook reference lab

Fictional, deterministic Python standard-library teaching reference. This is assistant-authored reference logic, not model-generated classifications, a live Claude run, a booking system, or a business deployment. No network, sending, booking, account connection, or source-file writes occur. The runner prints unsent drafts and review records.

Use the book’s Python 3.10-or-newer practice setup from Chapter 27. Check `python3 --version`, then run from the **book repository root**:

```sh
python3 companion-draft/method-labs/playbook/runner.py
python3 companion-draft/method-labs/playbook/runner.py --policy companion-draft/method-labs/playbook/policy-ten-confirmed.json
python3 -m unittest discover -s companion-draft/method-labs/playbook/tests -v
```

Default input paths are relative to runner.py, so the first command can also use its absolute path from another directory. Explicit --policy and --cases paths are relative to your current working directory.

## Inputs and expected behavior

`policy.json` records Chapter42's B01–B06 policy, seven confirmed participants, capacity12, and the approved fictional address. `policy-ten-confirmed.json` is the changed snapshot. Volunteers are excluded only because this fictional policy explicitly says so.

`cases.json` contains five requests: confirmed directions, three places, six places, unknown count, and three places plus unconfirmed access. Fields are supplied, reviewed classifications of those messages. The runner does not understand natural language or verify actual registration. A model extraction step would need a separate source-to-field evaluation.

`expected-key.json` is a designed answer key, authored from the chapter before running tests. With seven confirmed, remaining capacity is five. Three places leads to review, six to capacity conflict, and an unknown count remains unknown. The access case selects both capacity review and access review. Directions require current registration and an approved address. Missing address produces a question, never a guessed location.

At ten confirmed, remaining capacity is two. The pending three-place case moves to capacity conflict. The access case keeps BOTH its access review and its new capacity conflict. Nothing promises the two remaining places as a partial allocation. Every result remains unsent, with zero allocated places and no authorization to confirm attendance.

The numeric snapshot fields drive arithmetic; the rules text documents the fixed policy implemented in runner.py. Editing prose alone does not reprogram these rules. Change and review the implementation and answer key when policy behavior changes. An ID identifies a supplied snapshot; it does not prove that snapshot is current. The coordinator's live-register check remains required.

## Inspect, vary, recover

Compare each result's branches, policy references, missing facts, blocking conditions, and draft with the key. The key deliberately tests decision semantics rather than requiring one exact polite sentence. Preserve initial output before correcting anything.

Try a blank approved address, exactly five requested places, unknown registration after previous attendance, and missing count combined with access needs. Tests cover these cases, snapshot updates, input preservation, and command failures. An invalid request count fails instead of becoming an allocation. Invalid input prevents the command from printing a partial result set.

If a capacity snapshot changes, rerun every dependent pending request using the new file. Do not modify the old snapshot to conceal which evidence informed an earlier result. If a record is wrong, repair the source fields and reevaluate; a nicer draft does not fix the classification.

## Evidence boundary

The included tests exercise this local reference. They do not establish Claude compliance, security against arbitrary inputs, customer comprehension, or production reliability. No live coordinator checked a register. Use the cases and key to evaluate actual model outputs separately, retaining model/interface/version, prompt, source snapshot, and raw response.

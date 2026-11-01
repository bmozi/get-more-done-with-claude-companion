# Chapter 50: inspect a small enforcing boundary

Python 3, standard library only. Run from the repository root:

```sh
python3 companion-draft/boundary-lab/runner.py
python3 -m unittest discover -s companion-draft/boundary-lab -v
```

The runner prints JSON; it does not write a real summary file. Its simulated resource names stand for entries in an in-memory output dictionary. No model, account, API, real customer records or network is used. `captured-reference.json` and `test-results.txt` retain the October 18, 2026 execution.

Predict each case before running. Ordinary and hostile-note inputs should produce T1/T3. A scripted close request must be logged as blocked without preventing the permitted summary. The changed case adds T4, so a two-ticket output would fail the legitimate task even if the boundary held.

Read `PracticeTools.call` in runner.py. It allows only two exact operation/resource pairs, copies returned records and rejects everything else. The tests attempt unrelated reads, sending, state changes and unauthorized writes. Four tests passed in the captured local run. This establishes only these deterministic cases, not model resistance to injection or a production sandbox. The class is ordinary Python; code with access to other tools could bypass it. The fixed summarizer ignores note contents by construction.

For a later model trial, preserve the source prompt, full request, model and tool configuration, attempted calls, enforcement decisions, output and post-run source state. Distinguish no prohibited attempt, blocked attempt and executed prohibited action. Recheck ordinary task completion too. Do not call a manually scripted call a model response.

Transfer exercise: add an open T5 with a new category. Predict the new summary before running; the dispatcher's permissions should remain unchanged. Separately propose a third permitted operation on paper and identify what new effect it could have before implementing it.

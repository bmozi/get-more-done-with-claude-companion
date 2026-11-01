# Practice a method before trusting it

These four fictional labs accompany Chapters 41–44. For executable references, use the book’s Python 3.10-or-newer practice setup and terminal instructions in Chapter 27; check `python3 --version` before running. The prompt-development exercise can use an ordinary chat. You may instead work through the fictional inputs on paper, recording runtime execution as untested. Start by predicting an outcome. Inspect the source, run or perform the exercise, and explain each difference. The Python references use only the standard library and do not call a model, send messages, or approve work.

| Chapter | Lab | What to inspect |
|---|---|---|
| 41 | [Runbook](runbook/README.md) | Explicit duplicates, unknown counts, unresolved amendments |
| 42 | [Playbook](playbook/README.md) | Concurrent branches and changed capacity snapshots |
| 43 | [Prompt development](prompt-development/README.md) | Proposals versus commitments, source-grounded scoring, fresh evaluation cases |
| 44 | [Prompt chain](prompt-chain/README.md) | Source fidelity before calculation and rejection of a corrupted handoff |

The designed reviewer keys are separate from the runners and model-visible inputs. Keep them out of model requests. A program matching a key establishes only the tested reference behavior. Chapter 43 now has a separately retained ten-response local small-model pilot; its failures do not establish Claude behavior. Human learning, live Claude behavior and operational reliability remain separate evidence gates.

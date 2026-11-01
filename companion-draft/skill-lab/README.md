# Meeting-record teaching package: Chapters 19–20

Read `meeting-record/SKILL.md` and its worked example. The package contains no executable scripts. Its purpose is source-linked draft records, not sending or scheduling. `cases.json` provides six fictional requests. `reviewer-key.json` stays outside the installed package and out of model inputs. The blank ledger records actual attempts; it is not a prefilled success report.

## Start locally

Staging is optional. Use the book’s Python 3.10-or-newer practice setup and a terminal. Chapter 27 explains the runtime, working directory and first command; readers reaching this package from Chapter 19 can follow that setup first. If Python or Claude Code is unavailable, read the two package files and apply the method manually to the fictional notes. Keep discovery and invocation marked untested.

From the repository root:

```sh
python3 companion-draft/skill-lab/stage_package.py
```

The helper uses only Python’s standard library. The helper creates a fresh temporary project, copies the package into `.claude/skills/meeting-record/`, verifies byte hashes and prints the path. It does not start Claude, call a provider, change permissions, or copy reviewer answers. Each invocation creates a different folder; temporary storage is not a durable archive.

If you have authorized access to Claude Code, enter the printed project path and start `claude`. Inspect `/skills` and its source path. Invoke `/meeting-record` at the conversation prompt with S1's request and notes. Repeat in a fresh session without naming the skill to assess automatic selection. Then try S4 without naming it; the poem should not become a meeting record. Preserve invocation traces where available. Model answers alone cannot establish which package was loaded.

Instructions were checked against current official docs October18,2026: https://code.claude.com/docs/en/skills and https://agentskills.io/specification. This path is for Claude Code, not consumer or API uploads. `allowed-tools` preapproves tools; it is not a restrictive sandbox. Inspect effective host permissions. This package omits tool preapproval.

For each model attempt, supply only the case’s `instruction_request` and `meetings`, preserving meeting and note IDs. Keep `description` as a reviewer label rather than part of the request: several descriptions name the distinction being tested. The recorded development trial included those labels, so preserve that limitation when comparing new attempts with it.

## Predict, inspect, explain

Before consulting the reviewer key, predict each case. For S3, decide which fact is disputed and which remains established. For S5, find the explicit replacement. For S6, explain why shared ownership does not merge meetings. Check semantics against original notes; do not demand one exact table phrasing. Record evidence for mistakes as well as successes.

Compare the packaged method with the same plain method and notes in a session where this skill cannot auto-load. Keep model, context and tools matched where possible. This comparison is about packaging; the Chapter43 baseline/revision study changed instruction wording and answers a different question.

The cases are public practice, not unseen evaluation. After development, use new reviewer-authored cases with expected meanings fixed before execution. Finish by explaining one correction without help. A model's successful table does not establish the learner's understanding.

## Evidence

Local package validation, source-copy validation and a separate AI forward trial are recorded under `planning/reviews/skill-package/`. These are distinct from actual Claude discovery/invocation and human learning, neither of which is established here. Do not label the package production-ready on this evidence.

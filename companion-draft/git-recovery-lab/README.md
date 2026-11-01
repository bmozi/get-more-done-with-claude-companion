# Recover a working version without erasing the failed one

Chapter 30 local practice, October 18, 2026. Requires Git supporting `switch` and `init -b` (Git 2.28 or later), Python 3.10 or later, and macOS or a POSIX environment. Executed on macOS with Git 2.55.0. Windows command adaptation and human beginner usability are untested. No model, account, network request, push or remote backup is involved.

From the book repository root:

```sh
python3 companion-draft/git-recovery-lab/run_lab.py
```

Read the script first. It creates a new temporary directory, copies only the maintenance practice files, initializes Git in that copy, runs tests, commits the working version, makes a deliberately failing branch, preserves the failure, and restores the good commit in a second local copy. It never initializes, commits, changes branches or resets the book repository. Each run creates a new scratch directory; it does not overwrite earlier runs.

The output gives `scratch_root` and `steps_file`. Open that folder in your file manager. The three children are:

- `working/`: both commits and the deliberately broken investigation branch.
- `recovered/`: a separate checkout of the known working commit.
- `evidence/`: exact commands, their working directories, expected and observed exit codes, raw output and a summary.

These temporary files may be cleared by the operating system. Copy the evidence elsewhere if you want to keep it. Their presence is not a durable backup.

## Understand each operation

The exact command arrays and actual scratch paths are in `evidence/steps.json`; the script runs them directly without shell interpolation. The key sequence below uses labels `WORKING`, `RECOVERED` and `GOOD_COMMIT` for those observed values. They are explanations, not literal arguments to paste.

| Operation in the scratch working folder | Why it exists | What to inspect |
|---|---|---|
| `git init -b main` | Give this copied project its own history | Git root is the new `working` directory |
| `python3 -B -m unittest discover -s tests -v` | Establish that the initial behavior works | Eight tests pass |
| `git add README.md CLAUDE.md .gitignore tracker.py tests data` | Stage only known practice files | No account material or evidence logs included |
| Commit with the command below | Save a coherent working checkpoint | New commit identifier |
| `git rev-parse HEAD` | Record the known working identifier | Keep this as `GOOD_COMMIT` |
| `git switch -c practice/boundary-bug` | Name the investigation | The branch does not make broken behavior correct |
| Replace `due <= as_of` with `due < as_of` in `tracker.py` | Introduce one deliberate boundary defect | Diff changes the date rule |
| Run tests and the ordinary report | Observe the actual consequence | Tests fail; M02 disappears from `due` |
| Stage and commit the deliberate bug | Preserve the investigation for comparison | Commit message explicitly says it is failing practice |

The commit command uses a fictional identity for that invocation only:

```sh
git -c user.name='Fictional Lab Author' -c user.email=lab@example.invalid -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -m 'Practice: preserve working due-date boundary'
```

It does not change your account identity or global Git configuration. Signing and hooks are disabled only for these synthetic practice commits so a local course exercise does not invoke account setup or unrelated automation. Do not copy those overrides blindly into a real project's delivery process.

The failing test is expected. Stop and compare it with the report before accepting the summary. A Git commit preserves bytes; it does not certify quality. That is why the deliberately broken commit is saved with a truthful label.

## Restore in the second copy

The runner executes these operations using the real paths and known working identifier:

```text
git clone --no-hardlinks --no-checkout WORKING RECOVERED
cd RECOVERED
git remote remove origin
git checkout --detach GOOD_COMMIT
python3 -B -m unittest discover -s tests -v
python3 -B tracker.py data/maintenance.csv --as-of 2026-10-17
```

The clone reads the local scratch repository. It does not contact GitHub or another service. `--no-hardlinks` gives the second repository independent object files. The clone initially labels its local source `origin`; the next command removes that label. Both practice repositories end with no configured remotes.

A detached checkout displays a particular saved commit without moving a named branch to it. That is useful for this inspection. If you later want to develop changes from that version, create a new branch first. The exercise makes no edits in the recovered copy.

Expected: all eight tests pass and `due` contains M01 and M02. Then inspect `working` again: its HEAD should still be the failing commit. Recovery succeeded without erasing the evidence explaining why it was needed. The runner also checks that the book's original tracker file has the same hash it had before the exercise.

## Explain what you recovered

Answer without looking at the script: why did we preserve a failed commit, why did tests need to run after checkout, and why does this not count as remote backup?

A useful explanation is that the failed commit preserves the exact investigation; the recovered bytes still need to demonstrate usable behavior; and both copies remain on the same machine. Nothing here reverses an email, database update or other external effect.

For transfer, use a fresh scratch run and choose a different faulty edit in its `working` copy. Predict the expected defect before running the tests. Preserve the result and recover the saved good commit in a third new local copy. Never substitute the book repository for the scratch source. Keep the normal current work while you investigate.

Captured evidence for the author's development run is in `planning/reviews/adversarial-2026-10-18/git-recovery-evidence/`. It establishes local command behavior, not a successful human learning trial or off-machine recovery.

Official command references checked October 18, 2026: [local clone and copy options](https://git-scm.com/docs/git-clone) and [detached checkout](https://git-scm.com/docs/git-checkout). These explain Git behavior; the captured local run establishes what happened in this exercise.

# Chapter 30 practice guide

Recover and keep a project maintainable

## Objective

Preserve recoverable versions, distinguish local history from remote backup, and diagnose changes without erasing useful evidence.

## Inputs

- [README.md](../git-recovery-lab/README.md)

## Practice and assessment

Commit a working practice version, make a deliberate change in a separate branch, and inspect the diff. Restore the working behavior without deleting the evidence of what you tried. If you use a remote, verify that the intended commit exists there.

**Change one condition:** The tool now writes an output file. Include that file's lifecycle in the recovery plan. If it later writes to an external system, design recovery for that system separately.

**Keep:** A recoverable version, the commands needed to run it, and a note about what the recovery does and does not restore. Maintenance becomes easier when the next person can understand both the code and its history.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: executed scratch-only Git recovery, deliberate failing commit retained, recovered tests and report checked; no remote backup or human-learning trial.

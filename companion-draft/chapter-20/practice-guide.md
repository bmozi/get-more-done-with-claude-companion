# Chapter 20 practice guide

Test and maintain a skill

## Objective

Test when a skill should run, when it should stay out of the way, and how its output holds up on unfamiliar input.

## Inputs

- [README.md](../skill-lab/README.md)
- [cases.json](../skill-lab/cases.json)
- [run-ledger-template.csv](../skill-lab/run-ledger-template.csv)

## Practice and assessment

Use the six supplied test cards, then create one additional case whose expected meaning you establish before the run. Include the input, expected behavior, observed behavior, and evidence. Mark the actual result only after a run; do not prefill it with the outcome you hope to see.

**Change one condition:** Your skill now supports transcripts from two meetings in one file. Add a case where each meeting assigns the same person a different task. Check whether the summary preserves which decision belongs to which meeting.

**Keep:** A small, understandable regression set and the plain-instruction baseline. Maintain only tests that protect a meaningful behavior.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: package syntax and isolated copy verified; six-case AI instruction-following trial reviewed. Claude discovery/invocation and human learning remain untested.

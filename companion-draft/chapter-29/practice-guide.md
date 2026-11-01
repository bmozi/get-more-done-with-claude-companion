# Chapter 29 practice guide

Inspect changes and test the result

## Objective

Read a change in context, test boundaries, and distinguish automated evidence from a usable result.

## Inputs

- [README.md](../builder/maintenance-practice/README.md)

## Practice and assessment

In a copy of the tracker, change the due comparison to exclude today. Run the tests and inspect which case catches it. Restore the intended rule and rerun the checks.

**Change one condition:** The business requirement genuinely changes to “overdue only.” Update the brief and expected cases before changing the code. The same operator can be a defect under one requirement and correct under another.

**Keep:** A review note linking the change, requirement, failing case, fix, and result. Passing tests support the claims they cover; they do not certify every possible use.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: exercise design; live Claude execution and human learning trial not performed. The separate maintenance reference test log covers only that local program.

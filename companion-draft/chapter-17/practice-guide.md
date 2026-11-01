# Chapter 17 practice guide

Finish a file based task with Cowork

## Objective

Give a file-based task a bounded workspace, preserve originals, and check the files that were actually produced.

## Inputs

- [event-brief.txt](../shared/event-brief.txt)
- [registrations.csv](../shared/registrations.csv)
- [receipt.txt](../shared/receipt.txt)
- [meeting-notes.txt](../shared/meeting-notes.txt)

Copy these four text/data files first. Create receipt-unknown.txt only for the variation described below; it is not a supplied image fixture.

## Practice and assessment

Copy these four files from `companion-draft/shared/` into a practice input folder: `event-brief.txt`, `registrations.csv`, `receipt.txt`, and `meeting-notes.txt`. The receipt is a text fixture; the imagined messy folder at the start of this chapter is not the supplied packet. Produce a file manifest before organizing this copy, then check each output against its source. Confirm that the inputs remain unchanged.

**Change one condition:** Add a second fictional text file, `receipt-unknown.txt`, containing “Fictional receipt: item description unavailable; total USD [unreadable].” Keep `receipt.txt` unchanged. Rerun the indexing task. The index must include both filenames, preserve the first receipt's readable fields, and mark the second receipt's amount unknown. This tests handling a declared missing field, not reading an image. Do not invent an amount or omit the second receipt.

**Keep:** The organized packet and its mapping back to originals. The useful result is a set of files someone can trust enough to inspect and use, not merely a tidy directory.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: exercise design; live Claude execution and human learning trial not performed. The separate maintenance reference test log covers only that local program.

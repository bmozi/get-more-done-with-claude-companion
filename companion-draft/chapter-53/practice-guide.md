# Chapter 53 practice guide

Choose and combine AI systems

## Objective

Decide whether another tool adds a needed capability, test a combination against a simpler baseline, and preserve evidence through the handoff.

## Inputs

- [README.md](../task-fit-lab/README.md)
- [packet.json](../task-fit-lab/packet.json)
- [comparison-ledger.csv](../task-fit-lab/comparison-ledger.csv)

## Practice and assessment

Write a selection card for the four-action recording: intended result, required input capability, two candidate routes, shared quality checks, permitted data, and fallback. Draft the observation-to-instruction packet without inventing a live run.

**Change one condition:** The extracted observation says Save occurred before the quantity change. What should happen? Reject that sequence pending source review. Do not repair it from what a typical application would probably do. If the source is unavailable, mark the instruction unresolved.

**Keep:** Your selection card, handoff schema, and blank results sheet. Fill measured fields only after executing the corresponding route. A completed design is a useful milestone; it is not a completed comparison.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: exercise design; live Claude execution and human learning trial not performed. The separate maintenance reference test log covers only that local program.

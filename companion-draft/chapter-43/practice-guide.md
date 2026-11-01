# Chapter 43 practice guide

Develop and test reusable prompts

## Objective

Improve a reusable instruction against explicit examples, keep evaluation cases separate from revision, and recognize when a more elaborate prompt has made the work worse.

## Inputs

- [Help building a prompt](../prompt-builder/README.md)
- [README.md](../method-labs/prompt-development/README.md)

## Practice and assessment

Use N1–N4 to compare a baseline and revised prompt. Keep raw outputs and a row-level check against the expected table. Record the environment and date; do not replace failed outputs with cleaned versions.

**Change one condition:** Add N5: “Maya: I cannot make that inquiry. Lee: I will take it and report back on November 3, 2026.” The final action owner should be Lee, with that explicit deadline and evidence pointing to N5. N3 becomes historical context rather than a second current assignment. The closing-time decision remains four. Explain why changing an owner does not change that separate decision.

**Keep:** Both prompt versions, development and evaluation case labels, expected records, actual outputs, and an adoption decision tied to observed defects.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: ten captured local Qwen2.5 1.5B responses reviewed; no Claude or human learning trial. See the Chapter 43 pilot and its limits.

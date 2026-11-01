# Chapter 34 practice guide

Connect knowledge and build a custom agent

## Objective

Retrieve relevant evidence, preserve its provenance, and design a bounded knowledge assistant that can admit when the evidence is missing.

## Inputs

- [model-a-v1.txt](../shared/manuals/model-a-v1.txt)
- [model-a-v2.txt](../shared/manuals/model-a-v2.txt)
- [model-b-v1.txt](../shared/manuals/model-b-v1.txt)

## Practice and assessment

Build the source map and test four questions: a known model with a supported answer, a missing model, an unsupported question, and conflicting document versions. Record both retrieval and answer quality. If the wrong document was selected, prompt-polishing the final answer may not fix the cause.

**Change one condition:** The question requires comparing two models. Retrieve both sources deliberately and keep their recommendations separate. A single blended answer can erase the distinction the user needs.

**Keep:** The document map, retrieval results, answer citations, and failure cases. Use [the agent creation lab](../agent-creation-lab/README.md) for the fixed baseline, tool boundary and optional SDK checks. Live provider execution remains a separate milestone.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: exercise design; live Claude execution and human learning trial not performed. The separate maintenance reference test log covers only that local program.

## Agent creation lab

Run the fixed known-model and home-use cases, inspect the two source tools, and explain why an unread citation is rejected. The pinned SDK tests exercise OpenAI runner wiring with scripted responses and Claude configuration/local handlers. They do not call either provider. See [the complete lab](../agent-creation-lab/README.md) for commands, evidence limits and the live-run candidate.

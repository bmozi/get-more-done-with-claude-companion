# Chapter 35 practice guide

Evaluate reliability cost and recovery

## Objective

Evaluate complete task behavior, measure cost and latency in context, and design retries and recovery around real failure modes.

## Inputs

- [model-a-v2.txt](../shared/manuals/model-a-v2.txt)
- [retrieval-cases.json](../evaluations/retrieval-cases.json): a reviewer worksheet containing questions and expected results. Supply only the selected question and source documents; withhold the expected fields until assessment.
- [cost-worksheet.md](../local-ai-lab/cost-worksheet.md)

## Practice and assessment

Create an evaluation table for the four retrieval cases from Chapter 34 plus a simulated tool timeout. Record expected behavior, actual behavior, evidence, severity, time, and cost where measured. Keep unrun fields empty or explicitly marked unrun.

**Change one condition:** A new model improves average answer quality but occasionally chooses the wrong source version. Decide whether that tradeoff is acceptable for this application and explain which evidence you need before adopting it.

**Keep:** The evaluation set, traces with sensitive data removed, results, and release decision. A higher average score should not conceal a failure that violates the application's purpose.

## Record the attempt

Record date, product, interface, model shown, relevant settings, input version, actual output, checks, corrections, and unresolved questions. Do not put account identifiers or authentication material in the record.

Status: exercise design; live Claude execution and human learning trial not performed. The separate maintenance reference test log covers only that local program.

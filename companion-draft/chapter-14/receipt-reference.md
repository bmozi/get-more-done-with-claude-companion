# Receipt exercise reference and provenance

Created October 18, 2026 as original deterministic teaching material. These PNGs render invented text; they are not photographs, purchases, captured Claude outputs or empirical OCR results. `render_receipts.py` records the source and method. The clear and obscured files use identical invented data. The second image covers the delivery value completely; it does not simulate a measured camera defect.

Keep this key and the text receipt out of the image-extraction prompt. First inspect or provide only the selected PNG. Record the exact input, product, model, date and raw output if you run a model trial. No live extraction trial was performed during fixture creation.

| Field | Clear image | Obscured image |
|---|---|---|
| Item | Supply kits | Supply kits |
| Quantity | 2 | 2 |
| Unit price | USD 12.00 | USD 12.00 |
| Delivery printed value | USD 3.00 | Unreadable; do not claim direct observation |
| Printed total | USD 27.00 | USD 27.00 |
| Other charges | Explicitly none | Explicitly none |

The clear image reconciles: 2 × $12 + $3 = $27. The obscured image allows a separate inference: the $27 total minus $24 in items leaves $3, given its explicit no-other-charges statement. That arithmetic does not make the covered text readable. A correct response may report “delivery unreadable; implied delivery $3 under the stated assumptions.” It must not label $3 as extracted from the covered field.

The check is whether the learner distinguishes direct observation from inference, not whether a model guesses the hidden number. To assess an actual system, retain failures and inspect the PNG, rather than passing this key alongside it.

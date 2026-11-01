# Chapter 1 exercise review

Status: authored fixture with a manually derived reference schedule; not executed in Claude or tested with readers. Times are local within a fictional week. No timezone conversion or live calendar integration is needed.

## One valid reference

- Monday 18:30–19:00: A.
- Tuesday 18:00–18:45: B.
- Thursday 18:00–18:20: C.
- Wednesday remains free.

Other schedules may pass. Check duration, permitted windows, A before Thursday, B after A, C completed by Thursday 18:45, and one completely free evening. Every hard constraint must pass. Report preferences separately from hard constraints. Do not grade by resemblance to the reference wording.

## Trials to record

1. Give only “Help me plan my week.” Observe what Claude asks or assumes; do not predetermine its response.
2. Supply practice-week.txt and request a schedule. Record the unedited response and check every condition.
3. Change Tuesday to “no free window.” A can fit Monday, C Wednesday, and B Thursday; all hard constraints fit, but neither preference can be met. A useful answer explains that tradeoff instead of inventing time.
4. Change Tuesday to “no free window” and Thursday to 18:00–18:30. B has no 45-minute window. A useful answer identifies infeasibility and asks which constraint can change.
5. Transfer: write a different three-task example and explain the checks without copying the original prompt.

Record date, product, surface, plan, visible model, settings, exact input, full output, constraint failures, corrections, and the final saved result. Repeat the exact baseline in fresh conversations to observe variability; do not infer reliability from one success. User preferences and memory may affect a fresh conversation, so record those settings too.

No model response or timing has been fabricated. Actual runs belong in a later runs directory, with any private account information removed.

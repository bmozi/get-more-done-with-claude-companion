# Count the cost of usable work

Companion to Chapters 35 and 37 and the local-AI lesson. Preparation worksheet, not a live bill or a workstation benchmark. The adjacent `cost-example.json` contains fictional inputs and calculated answers. It does not represent John's planned hardware or a measured provider comparison.

## Freeze the comparison before running it

Write the task, fixture version, acceptable answer, quality-blocking errors, number of attempts allowed, and maximum time/spend. Use the same acceptance criteria across local and hosted candidates. Include failed attempts; do not change the task after one candidate fails and still call it the same comparison.

| Field | Your entry |
|---|---|
| Date, task, fixture and answer-key version | |
| Model, exact revision, quantization and runtime | |
| Interface and provider, or local device configuration | |
| Context and output limits; concurrent workers | |
| Acceptance criteria and unresolved-result policy | |
| API price/plan evidence URL and checked date | |
| Budget, attempt cap and enforced stopping controls | |
| Cash budget versus value assigned to time | |

## Keep cash, time, and allocation visible

For each candidate, record one row per attempt: identifier, task identifier, elapsed seconds, input/output/cache token categories if available, tool charges, electricity if measured, checking/correction minutes, outcome and evidence path. A timeout is an outcome with potentially unknown usage, not a zero-cost row. Record setup and maintenance once at their stated period; do not add them to every attempt and then add them again to the monthly total.

| Period-level quantity | Local candidate | Hosted candidate |
|---|---|---|
| Up-front cash required by this decision | | |
| Recurring cash: power, API, subscription, tools, storage | | |
| Setup, maintenance, checking and correction hours | | |
| Chosen hourly time value, if used | | |
| Ownership allocation and its assumptions, if used | | |
| Attempted tasks / accepted tasks / unresolved tasks | | |
| Total on the selected accounting basis | | |
| Total divided by accepted tasks | | |

A subscription may remain a fixed cash payment even when its allowance is underused. Show any allocation explicitly. Included credits and previously purchased equipment can change incremental cash without making ownership or maintenance disappear. Do not mix a local allocated ownership total with a cloud token-only total and call the result a fair comparison.

## Reproduce the fictional example

Before reading the worked calculation below, predict which costs change if half as many results pass while total effort and electricity stay the same. Record your answer, then compare it with the example.

- Hardware allocation: purchase × AI share ÷ useful months = 2,400 × 0.5 ÷ 36 = $33.33 per month.
- Added electricity: watts ÷ 1,000 × hours × price per kWh = 120 ÷ 1,000 × 40 × 0.20 = $0.96.
- Maintenance time value: 1 hour × $30 = $30.
- Review time value: 60 attempts × 2 minutes ÷ 60 × $30 = $60.
- Allocated economic total: $124.29; 48 accepted tasks give about $2.59 each.
- Economic total without hardware: $90.96; 48 accepted tasks give about $1.90 each. This includes valued time; it is not $90.96 of incremental cash.
- Changed quality: the same total with 24 accepted tasks gives about $5.18 each.

Calculations retain precision until display. These inputs exclude installation time, taxes, financing, resale, new storage, and other costs listed in the JSON. Add relevant costs before using the worksheet for an actual decision. Do not treat 120 watts as a workstation measurement.

A rerun may consume additional electricity and review time, so the constant-cost example isolates one relationship; it is not a prediction of your rerun bill. Recalculate with observed values when you have them. With zero accepted results, report the total and zero accepted; division by zero has no useful cost-per-accepted result.

## Preserve what the comparison cannot tell you

Separate assumptions, meter readings, provider usage records, checked results, and subjective judgments. A small pilot does not establish long-term reliability or hardware payback. Record offline availability, privacy requirements, learning value, and maintenance burden alongside cost, without converting them into invented dollar savings.

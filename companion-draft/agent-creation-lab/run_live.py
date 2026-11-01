"""Explicit live-run candidate. Never used by offline tests; provider execution unvalidated."""
import argparse
import asyncio
import json
from claude_agent_sdk import query, ResultMessage
from core import CASES, Store, validate_answer
from sdk_adapters import run_openai, claude_configuration

async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider', required=True, choices=['openai', 'claude'])
    parser.add_argument('--model', required=True)
    parser.add_argument('--case', choices=CASES, default='known-a')
    parser.add_argument('--claude-budget-usd', type=float)
    args = parser.parse_args()
    task = CASES[args.case]
    store = Store()
    if args.provider == 'openai':
        # Model-turn/tool limits are not a dollar spending cap.
        result = await run_openai(task, args.model, store)
    else:
        if args.claude_budget_usd is None:
            parser.error('--claude-budget-usd is required for the Claude candidate')
        options, _ = claude_configuration(store, model=args.model, budget_usd=args.claude_budget_usd)
        terminal = None
        async for message in query(prompt=json.dumps(task), options=options):
            if isinstance(message, ResultMessage):
                terminal = message
        if terminal is None or terminal.is_error or terminal.subtype != 'success':
            raise RuntimeError('No successful terminal result; no accepted answer')
        if terminal.structured_output is None:
            raise RuntimeError('Missing structured output; no accepted answer')
        result = {'answer': validate_answer(task, terminal.structured_output, store.read_ids),
                  'trace': store.trace, 'usage': terminal.usage,
                  'reported_cost_usd': terminal.total_cost_usd}
    print(json.dumps({'evidence_kind': 'live_provider_attempt_requires_recorded_review', **result}, indent=2))

if __name__ == '__main__':
    asyncio.run(main())

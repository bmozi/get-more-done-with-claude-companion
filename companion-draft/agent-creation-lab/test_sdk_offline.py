"""Real SDK wiring with scripted model messages. No provider call or Claude process."""
import json
import unittest
from agents import Model, ModelResponse
from agents.exceptions import MaxTurnsExceeded, UserError
from agents.usage import Usage
from openai.types.responses import ResponseFunctionToolCall, ResponseOutputMessage, ResponseOutputText
from core import CASES, Store, ToolLimitError, reference_answer
from sdk_adapters import run_openai, openai_agent, claude_configuration

class ScriptedModel(Model):
    def __init__(self, *, stale=False, loop=False):
        self.calls = 0
        self.stale = stale
        self.loop = loop

    async def get_response(self, system_instructions, input, *args, **kwargs):
        self.calls += 1
        if self.calls == 1 or self.loop:
            output = [ResponseFunctionToolCall(arguments='{}', call_id=f'call_{self.calls}', name='list_sources', type='function_call')]
        elif self.calls == 2:
            if 'A2' not in json.dumps(input):
                raise AssertionError('SDK did not carry the catalog observation forward')
            output = [ResponseFunctionToolCall(arguments='{"source_id":"A2"}', call_id='call_read', name='read_source', type='function_call')]
        else:
            if 'FILTER-A-02' not in json.dumps(input):
                raise AssertionError('SDK did not carry the read observation forward')
            answer = reference_answer(CASES['known-a'])
            if self.stale:
                answer['records'][0].update(source_id='A1', part='FILTER-A-01')
            output = [ResponseOutputMessage(id='fixture_final', content=[ResponseOutputText(annotations=[], text=json.dumps(answer), type='output_text')], role='assistant', status='completed', type='message')]
        return ModelResponse(output=output, usage=Usage(requests=1), response_id=f'fixture_response_{self.calls}')

    async def stream_response(self, *args, **kwargs):
        raise NotImplementedError('This offline teaching model supports non-streamed runs only')
        yield  # Make this an async generator, as the Model interface requires.

class SDKTests(unittest.IsolatedAsyncioTestCase):
    async def test_openai_runner_calls_tools_and_uses_observations(self):
        store = Store()
        scripted = ScriptedModel()
        result = await run_openai(CASES['known-a'], scripted, store)
        self.assertEqual(scripted.calls, 3)
        self.assertEqual([e['tool'] for e in result['trace']], ['list_sources', 'read_source'])
        self.assertEqual(result['answer']['records'][0]['part'], 'FILTER-A-02')
        self.assertEqual(result['model_requests'], 3)

    async def test_openai_valid_json_with_stale_fact_still_rejected(self):
        with self.assertRaisesRegex(ValueError, 'stale'):
            await run_openai(CASES['known-a'], ScriptedModel(stale=True))

    async def test_openai_model_turn_limit_stops_repeated_calls(self):
        with self.assertRaises(MaxTurnsExceeded):
            await run_openai(CASES['known-a'], ScriptedModel(loop=True), max_turns=2)

    async def test_application_tool_limit_survives_sdk_runner(self):
        store = Store(max_calls=1)
        with self.assertRaises(UserError) as caught:
            await run_openai(CASES['known-a'], ScriptedModel(loop=True), store)
        self.assertIsInstance(caught.exception.__cause__, ToolLimitError)
        self.assertEqual(len(store.trace), 1)

    async def test_claude_configuration_and_local_handlers(self):
        store = Store()
        options, handlers = claude_configuration(store, model='offline-placeholder-not-a-live-model', budget_usd=0.05)
        self.assertEqual(options.tools, [])
        self.assertEqual(options.setting_sources, [])
        self.assertTrue(options.strict_mcp_config)
        self.assertEqual(options.max_turns, 4)
        self.assertEqual(options.max_budget_usd, 0.05)
        self.assertEqual(set(options.allowed_tools), {'mcp__manuals__list_sources', 'mcp__manuals__read_source'})
        catalog = await handlers['list_sources'].handler({})
        self.assertIn('A2', catalog['content'][0]['text'])
        result = await handlers['read_source'].handler({'source_id': 'A2'})
        self.assertIn('FILTER-A-02', result['content'][0]['text'])
        self.assertEqual(store.read_ids, {'A2'})
        with self.assertRaises(ValueError):
            await handlers['read_source'].handler({'source_id': '../unrelated.txt'})

    async def test_claude_handler_rejects_extra_fields(self):
        _, handlers = claude_configuration(Store(), model='offline-placeholder-not-a-live-model', budget_usd=0.05)
        with self.assertRaises(ValueError):
            await handlers['read_source'].handler({'source_id': 'A2', 'send_email': True})

    async def test_no_external_action_tools_are_exposed(self):
        agent = openai_agent(Store(), ScriptedModel())
        self.assertEqual({t.name for t in agent.tools}, {'list_sources', 'read_source'})
        _, handlers = claude_configuration(Store(), model='offline-placeholder-not-a-live-model', budget_usd=0.05)
        self.assertEqual(set(handlers), {'list_sources', 'read_source'})

if __name__ == '__main__':
    unittest.main()

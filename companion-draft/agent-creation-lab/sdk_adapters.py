"""Provider-specific agent configurations. Importing does not call a provider."""
import json
from agents import Agent, Runner, RunConfig, function_tool
from claude_agent_sdk import ClaudeAgentOptions, tool, create_sdk_mcp_server
from core import Store, INSTRUCTIONS, ANSWER_SCHEMA, validate_answer

def openai_agent(store: Store, model):
    @function_tool(failure_error_function=None)
    def list_sources() -> str:
        """List fictional source IDs, model applicability and supersession."""
        return json.dumps(store.catalog())

    @function_tool(failure_error_function=None)
    def read_source(source_id: str) -> str:
        """Read one approved fictional source by ID; never pass a filesystem path."""
        return json.dumps(store.read(source_id))

    return Agent(name='Fictional manual assistant', instructions=INSTRUCTIONS,
                 model=model, tools=[list_sources, read_source])

async def run_openai(task, model, store=None, max_turns=4):
    store = store or Store()
    result = await Runner.run(openai_agent(store, model), json.dumps(task),
                              max_turns=max_turns, run_config=RunConfig(tracing_disabled=True))
    answer = json.loads(result.final_output)
    return {'answer': validate_answer(task, answer, store.read_ids), 'trace': store.trace,
            'model_requests': result.context_wrapper.usage.requests}

def claude_configuration(store: Store, *, model: str, budget_usd: float):
    if not model or budget_usd <= 0:
        raise ValueError('An explicit model and positive budget are required')

    @tool('list_sources', 'List approved fictional manuals and applicability.', {})
    async def list_sources(args):
        return {'content': [{'type': 'text', 'text': json.dumps(store.catalog())}]}

    @tool('read_source', 'Read one approved fictional source by ID.', {'source_id': str})
    async def read_source(args):
        # Validate again at the application boundary, including direct handler calls.
        if set(args) != {'source_id'} or not isinstance(args['source_id'], str):
            raise ValueError('Expected exactly one string source_id')
        return {'content': [{'type': 'text', 'text': json.dumps(store.read(args['source_id']))}]}

    server = create_sdk_mcp_server(name='manuals', tools=[list_sources, read_source])
    options = ClaudeAgentOptions(
        tools=[],  # No built-in filesystem, shell, network or agent tools.
        mcp_servers={'manuals': server}, strict_mcp_config=True,
        allowed_tools=['mcp__manuals__list_sources', 'mcp__manuals__read_source'],
        permission_mode='default', setting_sources=[],
        system_prompt=INSTRUCTIONS, model=model, max_turns=4,
        max_budget_usd=budget_usd,
        output_format={'type': 'json_schema', 'schema': ANSWER_SCHEMA},
    )
    return options, {'list_sources': list_sources, 'read_source': read_source}

"""Capture local baseline and SDK wiring evidence. Never calls a provider."""
import argparse
import asyncio
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import socket
import subprocess
import unittest.mock
from core import CASES, MANUALS, Store, baseline
from sdk_adapters import run_openai, claude_configuration
from test_sdk_offline import ScriptedModel

async def capture():
    scripted = ScriptedModel()
    openai = await run_openai(CASES['known-a'], scripted)
    store = Store()
    options, handlers = claude_configuration(store, model='offline-placeholder-not-a-live-model', budget_usd=0.05)
    await handlers['list_sources'].handler({})
    read = await handlers['read_source'].handler({'source_id': 'A2'})
    return {
        'evidence_kind': 'local_fixture_and_sdk_wiring_only',
        'live_provider_calls': False, 'claude_agent_process_launched': False,
        'python': platform.python_version(),
        'sdk_versions': {n: importlib.metadata.version(n) for n in ['openai-agents', 'claude-agent-sdk', 'openai', 'pydantic']},
        'baselines': {name: baseline(task) for name, task in CASES.items()},
        'openai_sdk': {'model_kind': 'scripted fixture, no LLM', 'scripted_requests': scripted.calls, **openai},
        'claude_sdk': {'scope': 'configuration plus direct local handlers, not MCP transport or agent loop',
                       'built_in_tools': options.tools, 'allowed_mcp_tools': options.allowed_tools,
                       'max_turns': options.max_turns, 'configured_budget_usd_not_spent': options.max_budget_usd,
                       'trace': store.trace, 'read_result_source': json.loads(read['content'][0]['text'])['source_id']},
        'manual_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in MANUALS.glob('*.txt')},
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    target = parser.parse_args().output
    if target.exists():
        parser.error('Refusing to overwrite an earlier evidence file')
    # The guard covers execution, not earlier package downloads/imports.
    with unittest.mock.patch.object(socket.socket, 'connect', side_effect=AssertionError('Network forbidden in local capture')), unittest.mock.patch.object(subprocess, 'Popen', side_effect=AssertionError('Child process forbidden in local capture')):
        report = asyncio.run(capture())
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'output': str(target), 'network_and_child_process_guard': 'passed', 'scope': report['evidence_kind']}))

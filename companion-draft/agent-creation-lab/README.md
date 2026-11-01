# Build and inspect a small source-based agent

This lab extends Chapter 34's fictional manuals. It also provides an adapter pattern for the proposed ChatGPT book. Start with the task and checks, then inspect how each SDK connects the same narrow tools to an agent.

**Evidence boundary:** the fixed baseline and offline tests run locally. The OpenAI SDK loop is exercised using scripted responses, not an LLM. The Claude SDK configuration and tool handlers are exercised locally; neither a Claude process nor its MCP transport is started. The live entry point is a candidate that has not been validated against either provider. No human learning outcome is claimed.

## What you are building

The assistant answers a small question about fictional Model A or Model B. It can list three approved manual IDs and read one of those manuals. It must preserve source authority and the condition attached to an interval. It has no send, purchase, shell or general file-access tool.

An instruction sheet alone does not create a tool-using agent application. In the SDK route, the runner repeatedly asks the model what to do, dispatches permitted tools, and returns their observations until a result or limit ends the run. The local baseline takes a fixed route instead. Compare the agent with that simpler baseline before deciding it is useful.

The OpenAI adapter is a developer application built with the OpenAI Agents SDK. It is not a saved ChatGPT GPT, plugin or Work task. The Claude adapter uses the Claude Agent SDK; running its process locally would not make Claude's model local.

## Begin without any SDK or account

From the book repository root:

```sh
python3 companion-draft/agent-creation-lab/core.py --case known-a
python3 companion-draft/agent-creation-lab/core.py --case missing-model
python3 companion-draft/agent-creation-lab/core.py --case home-use
python3 companion-draft/agent-creation-lab/core.py --case compare
python3 -m unittest discover -s companion-draft/agent-creation-lab -p 'test_core.py' -v
```

The known Model A case should select A2 and FILTER-A-02. The missing-model case should ask for the model. Model A's home-use interval is not established. Comparing A and B must keep their parts and sources separate.

The metadata in core.py is authored for these three manuals. It is not a general parser. The validator checks structured claims against this tiny known collection; it cannot establish the truth of arbitrary documents or validate every sentence of prose. Check the source text and conditions yourself.

## Inspect the agent contract

Read INSTRUCTIONS, ANSWER_SCHEMA and the two tool functions. For each tool, identify the inputs it accepts, what it returns and what it cannot do. Source IDs are a closed registry; a path such as `../../publishing/book.json` is rejected.

Four application tool calls are allowed, counting catalog calls too. A lock keeps that limit shared across parallel callers. Model-turn limits are separate: one model response can request more than one tool. Neither of those limits is a dollar cap.

Supported claims must cite a source actually read in the current run. The final structured record must match the current model, part and use condition. Missing evidence produces a question or unsupported result rather than an invented value.

## Exercise the installed SDKs without calling a model

The October 31, 2026 run used Python 3.12 with `openai-agents==0.24.0` and `claude-agent-sdk==0.2.176`. The core tests also ran with system Python. Install the pinned SDK requirements in your isolated development environment, or use uv:

```sh
uv run --with openai-agents==0.24.0 --with claude-agent-sdk==0.2.176 python -m unittest discover -s companion-draft/agent-creation-lab -p 'test_sdk_offline.py' -v
```

In test_sdk_offline.py, ScriptedModel emits predetermined calls and a predetermined final answer. The real OpenAI runner executes the tools and carries the observations forward. That shows the wiring works for this script. It does not show that an LLM will choose the correct source.

The Claude tests construct an in-process MCP server and invoke its local handlers directly. They do not prove transport, permissions at runtime, successful model selection or a completed agent loop. `tools=[]`, `strict_mcp_config=True` and `setting_sources=[]` keep the intended configuration narrow. `allowed_tools` pre-approves the named tools; it is not itself a universal sandbox or a replacement for the tools' own checks.

Try the stale-answer test. Its JSON is structurally valid but the cited source is superseded. Try the repeated-tool test. The application limit still stops it, even when the SDK wraps the underlying exception. The negative cases teach what the checks actually enforce.

## Capture your own local evidence

Choose a new path; the helper refuses to overwrite an earlier receipt.

```sh
uv run --with openai-agents==0.24.0 --with claude-agent-sdk==0.2.176 python companion-draft/agent-creation-lab/capture_local.py --output tmp/my-agent-local-run.json
```

During capture, attempted socket connections and child-process launches are blocked. Package downloads and imports occur before this execution guard. The report records the source hashes, versions, observations and evidence kind. It contains no provider run.

## Connect a live model as a separate validation step

First check current provider setup and authentication documentation. Keep credentials outside source files and captured output. A ChatGPT or Claude website subscription does not establish that this separate application has working API/SDK access.

The candidate entry point is run_live.py. It requires an explicit provider and model, so the lab does not silently choose a model or start a paid run. Claude also requires `--claude-budget-usd`; the current SDK exposes that setting. The OpenAI candidate has model/tool limits but no application-enforced dollar cap. Configure and monitor usage appropriately; do not describe a turn limit as a spending limit.

The live route has not been run in this milestone. Before teaching it as a demonstrated integration, preserve actual requests, terminal results, tool observations, stop reasons, reported usage and final checked records. Test missing input, wrong source, unavailable read, an overlong run and ordinary successful work. Compare with the fixed baseline again. Do not record the offline scripted messages as live evidence.

## Use both books without repeating the same agent

The Claude project uses maintenance sources and a reusable operations method. The ChatGPT extension should build an evidence-to-briefing assistant with its own sources, output and held-out cases. Reuse the tool-contract and evaluation ideas; adapt the application deliberately. A shared SDK pattern does not transfer account access, memory, native app tools or deployment state.

## Source documentation

- [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Claude custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools)
- [Claude permission behavior](https://code.claude.com/docs/en/agent-sdk/permissions)
- [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents/sdk)
- [OpenAI quickstart](https://developers.openai.com/api/docs/guides/agents/quickstart)
- [Agent evaluation](https://developers.openai.com/api/docs/guides/agent-evals)

Documentation checked October 31, 2026. Concrete local receipts live under research/agent-creation-2026-10-31. Live provider and reader trials remain separate evidence stages.

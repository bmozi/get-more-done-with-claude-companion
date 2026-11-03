# Two actual subagent findings, one checked recommendation

Chapter48 fictional family get-together packet; actual AI subagent trial on October18,2026. The parent agent dispatched two fresh-context Codex subagents through the session's `spawn_agent` tool with `fork_turns: none`. Each received the path to its assignment, which names the shared packet. The budget assignment finished before the suitability assignment started, so this was independent delegation, not a parallel-speed experiment. No model override was supplied. No Claude runtime or paid provider API was invoked.

The preserved assignment files contain the exact task instructions. The initial dispatch messages are in trial-record.json. The response JSON files preserve the returned final message bodies, not a complete transcript of internal processing or a provider API envelope. The workers did not receive the chapter's worked answer or each other's findings in their supplied task context. They shared a filesystem; a task instruction to read only the named input is not an enforced access sandbox.

## Reproduce the method in your environment

1. Read packet-v1.txt yourself. Keep all source IDs and the explicit version2 change.
2. Open your environment's documented subagent interface if available. Give each worker the shared packet and one assignment. If using separate ordinary chats instead, label that change in your record.
3. Save the workers' first outputs before correcting anything. Record the actual environment, date, visible model identifier and context supplied; do not infer a model name from its writing style.
4. Recompute cost and occupancy directly from the packet before integrating. A disagreement is resolved against facts and rules, not by worker count.
5. Retain both versions, including the still-cheaper room that no longer fits the extra guest. Draft the recommendation only after these checks.

The supplied files are the exact practice prompts and captured responses, not a portable CLI that launches Claude. Product-specific launch, permission, stop and timeout behavior remain a separate implementation gate. This trial does not measure time saved or general reliability.

Expected integration: v1 proposes Garden at$370 with10 occupants and no spare place. Version2 proposes River at$400 with11 occupants and one spare place. Both remain proposals pending Lee's authorization and current availability. The examples assume fixed refreshments reserve even when attendance changes.

Try without copying: change the reserve to$90 in a new packet. River's commitment becomes$430, above the$420 ceiling; Garden's becomes$400. In v2 Garden still fails capacity. No room satisfies both requirements. An integrator must preserve that conflict instead of forcing a winner. This last case is an authored transfer check, not an additional captured subagent trial.

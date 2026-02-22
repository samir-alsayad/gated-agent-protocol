# Deterministic Checkpoints & Task Completion

**Status**: Draft / Discussion Notes
**Context**: How does GAP deterministically enforce checkpoints during the Execution phase without relying on the agent's "will" to stop? And how does it technically know a task is "done"?

---

## The Problem: Probabilistic vs. Deterministic Stopping

In standard agent harnesses, an agent runs in a continuous `while` loop (Thought → Action → Observation). If you tell an agent "Pause after Task 1 for review," you are relying on the LLM to *generate* a thought like "I am done with Task 1, I should stop now."

This is **probabilistic guardrailing**. If the model hallucinates or gets distracted, it ignores the prompt and continues executing code for Task 2, bypassing the supervisor entirely.

GAP requires **deterministic gating**. The enforcement must exist in the runtime environment (the Harness/Protocol layer), independent of the LLM's prompt adherence.

---

## How GAP Knows a Phase is "Done"

The definition of "Done" changes depending on the phase class.

### 1. The Alignment Phase (Deterministic Trigger)
For artifacts like `requirements.md`, `design.md`, or `tasks.md`, completion is binary.
- **The Trigger**: The agent executes the specific tool instruction to write the file (`docs/.gap/proposals/requirements.md`).
- **The Enforcement**: The moment that file hits the disk, the protocol runner detects the state change (e.g., via file watcher or tool wrapper) and forcefully suspends the agent process. It shifts the state machine from `UNLOCKED` to `PENDING`.

### 2. The Execution Phase (Complex Triggers)
Execution tasks (e.g., "Implement Auth Module") are not single file writes. They involve multiple tool calls (reads, writes, bash commands). Identifying "Done" requires explicit boundaries.

There are three architectural approaches to enforcing this deterministically:

#### Approach A: The Explicit "Submit" Tool
The agent is provided a definitive tool (e.g., `gap_submit_task(task_id="T-1")`).
- **Mechanism**: The harness intercepts this specific tool call. Instead of returning a result to the agent, the harness suspends the execution loop immediately.
- **Fail-safe**: If the agent *forgets* to call the tool, a deterministic **Iteration Budget** (e.g., max 15 steps per task) forcefully pauses the agent, preventing runaway execution.

#### Approach B: The Intercept Layer (Tool Wrapping)
The agent does not have raw access to bash or file writes. It uses GAP-wrapped tools.
- **Mechanism**: When the agent calls `gap_write_file(task_id="T-1")`, the tool itself queries the Protocol Engine: `gap checkpoint verify T-1`.
- **Enforcement**: If the ledger shows the checkpoint is locked (supervisor has not approved), the tool refuses to execute and returns a hard system error: `"Execution blocked. Supervisor must approve checkpoint T-1."` The agent is physically incapable of making the edit.

#### Approach C: The Token Budget Layer (MCL Integration)
Tying execution directly to the **Model Control Layer (MCL)**.
- **Mechanism**: When a checkpoint boundary is hit (either via `gap_submit` or iteration limit), the Protocol Engine tells the Unified Gateway (LiteLLM): *"Set budget for this session to $0."*
- **Enforcement**: When the agent tries to generate its next thought, the gateway returns `402 Payment Required` or `403 Forbidden`. The agent's "brain" is disconnected until the supervisor runs `gap gate approve`, which restores the token budget.

---

## Conclusion

To achieve true Gated Agent Protocol compliance, a harness must implement **Approach A (Explicit Submit + Iteration Budgets)** combined with **Approach B (Tool-Level Intercept)**. 

The agent must be forced to declare its intent to cross a checkpoint, and the tools themselves must independently verify with the Ledger that the crossing is authorized. The LLM's choices are probabilistic, but the tools' reactions are deterministic.

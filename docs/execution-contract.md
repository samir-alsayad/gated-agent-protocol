# The GAP Execution Contract: Who Does What, How

The Gated Agent Protocol (GAP) is strictly a **Consent Ledger**. It is not an orchestration engine, an LLM router, or a security sandbox. GAP defines the workflow and holds the approved execution envelopes.

To actually run an LLM, you must use an **Execution Runner** (a script, CLI wrapper, or agentic framework like Letta or OpenHands) that is "GAP-aware." The Runner is responsible for configuring the sandbox, selecting the model, and talking to the API based on GAP's ledger.

Here is the explicit contract detailing every phase of the `software-engineering` protocol: Who is responsible, How it is executed, and What GAP's role is.

---

## 1. Requirements (`docs/requirements.md`)
*   **Who writes it:** The Supervisor (Human) or an Agent chatting with the Supervisor.
*   **What:** Defines the problem statement, user stories, and constraints.
*   **How:** Authored manually or generated via `gap scribe create requirements`.
*   **GAP's Role:** The ledger marks the `requirements` step as `pending`. Once finalized, the supervisor runs `gap gate approve requirements`, locking the artifact in the ledger and unlocking the next phase.

## 2. Design (`docs/design.md`)
*   **Who writes it:** The Supervisor (Human) or an Agent chatting with the Supervisor.
*   **What:** Translates requirements into technical architecture, data structures, and correctness properties.
*   **How:** The Runner prompts the Agent with `requirements.md`. The Agent outputs its proposal using the CLI: `gap scribe create design --artifact docs/design.md`. 
*   **GAP's Role:** GAP intercepts the `scribe` command and writes the artifact to a staging area (`.gap/proposals/docs/design.md`). The supervisor reads it and, if satisfied, runs `gap gate approve design`. GAP moves the proposal to live, backing up any previous version.

## 3. Tasks (`.gap/tasks.yaml`)
*   **Who writes it:** The Supervisor (Human) or an Agent chatting with the Supervisor.
*   **What:** A logical breakdown of the Design into atomic action items (Proposed Change Units) that strictly define *What must change*. It contains **zero** execution context (no ACLs, no model selection).
*   **How:** The Runner prompts the Planner Agent with `design.md`. The Agent outputs a list of tasks (e.g., T-1, T-2) specifying descriptions and target output files via `gap scribe create tasks`.
*   **GAP's Role:** GAP stages the YAML in `.gap/proposals/`. The supervisor reviews the logical grouping and approves: `gap gate approve tasks`. 

## 4. Plan (`.gap/plan.yaml`)
*   **Who writes it:** The Supervisor (Explicitly Human).
*   **What:** The Execution Envelope. The supervisor maps powers (ACLs, allowed shell tools, specific cognition models and locality, and pause checkpoints) to specific task IDs (e.g., granting T-1 access to use `pytest` and edit `src/api.py`).
*   **How:** The Agent is **entirely unaware** of this step. The supervisor runs `gap scribe create plan`, which deposits a blank template directly into `.gap/plan.yaml`. The human authors the permissions YAML. Once complete, they run `gap gate approve plan`.
*   **GAP's Role:** GAP validates that the `.gap/plan.yaml` contains an envelope for every task listed in `.gap/tasks.yaml`. If valid, it locks the plan in the ledger.

## 5. Implementation (`src/*`)
*   **Who:** Implementation Agent, managed by the Execution Runner.
*   **What:** The actual code generation and file modifications.
*   **How:** The supervisor triggers the Runner (e.g., `gap-run execute T-1`). 
    1.  **Read Envelope:** The Runner asks GAP for the `.gap/plan.yaml` envelope for T-1.
    2.  **Configure Sandbox:** The Runner (not GAP) configures the execution sandbox. It locks the filesystem to only allow writes to the paths in the ACL, exposes only the allowed shell commands, and points its internal LiteLLM proxy to the authorized model.
    3.  **Prompt Agent:** The Runner prompts the Agent with the description from `.gap/tasks.yaml`. *Crucially, it does not show the Agent the `plan.yaml`*. The Agent only sees the tools it is allowed to use. 
    4.  **Execute:** The Agent edits code. If it tries to use `rm -rf` when it wasn't explicitly allowed in the plan, the Runner's shell execution tool returns a permission error.
*   **GAP's Role:** Passive. The Runner asks GAP to verify checkpoints (e.g., `gap checkpoint verify T-1 --phase after_completion`). If the phase is listed in the `plan.yaml`, GAP blocks execution until the supervisor types `gap checkpoint approve T-1 --phase after_completion`.

## 6. Verification & Walkthrough (`docs/walkthrough.md`)
*   **Who:** Implementation Agent & QA Agent.
*   **What:** Proof of work. Documentation of tests run, output logs, and validation that the design properties were met.
*   **How:** After implementation, the Agent is tasked with generating a walkthough via `gap scribe create verification`. 
*   **GAP's Role:** Stages the walkthrough in `.gap/proposals/`. The supervisor reads the proof of work and visually confirms the code. If satisfied, they run `gap gate approve verification`, closing the ledger for this project cycle.

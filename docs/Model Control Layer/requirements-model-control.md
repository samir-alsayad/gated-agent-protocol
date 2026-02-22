# Requirements: Model Control Layer

**Status**: Draft  
**Author**: Samir Alsayad  
**Date**: 2026-02-22  

---

## 1. Problem Statement

GAP currently treats the LLM as a black box — it doesn't control *which* model executes a task or *where* that model runs. As the ecosystem matures, there are strong reasons to route different tasks to different models:

- **Cost**: Use a cheap local 7B model for simple formatting tasks, save cloud credits for complex reasoning.
- **Privacy**: Keep sensitive code local. Never send proprietary logic to a cloud API.
- **Specialization**: Use coding-specific models for implementation, reasoning models for design, small models for linting.
- **Safety**: Prevent the Mac from freezing by enforcing memory budgets and model concurrency limits.

The Model Control Layer (MCL) gives the supervisor **explicit, auditable control** over which models are used, where they run, and how resources are managed.

---

## 2. Principles

1. **Explicit Locality Toggle**: The supervisor must always know — and explicitly approve — whether a task runs locally or in the cloud. This is never inferred.
2. **Resource Safety**: The system must never load models that would exceed available memory or cause swap. Hardware limits are hard constraints, not suggestions.
3. **GAP Compliance**: Model assignments are part of the Alignment phase. They are proposed, reviewed, and locked — just like requirements and design.
4. **Protocol Separation**: The MCL is an infrastructure concern. It does not change what GAP *does* (enforce workflows). It changes what GAP *delegates to*.

---

## 3. Functional Requirements

### FR-1: Model Registry
The system shall maintain a registry of available models, each with:
- **Name** (e.g., `qwen2.5-coder-14b`)
- **Location**: `local` or `cloud`
- **Provider**: `mlx`, `ollama`, `openrouter`, `openai`, etc.
- **Endpoint**: URL or local path
- **Memory footprint** (for local models): estimated RAM in GB
- **Capabilities**: tags like `code`, `reasoning`, `chat`, `embedding`

### FR-2: Cascading Model Assignment
Model assignment operates at three levels, each overriding the one above:

1. **Per-artifact** (Alignment phase default): e.g., "Use Opus for `design.md`"
2. **Per-task**: Override in `tasks.md` for specific tasks
3. **Per-subtask**: Fine-grained override for subtasks within a task

```yaml
# In tasks.md
default_model:
  model: claude-3.5-sonnet
  location: cloud

tasks:
  - id: T-1
    description: "Implement the authentication module"
    model: qwen2.5-coder-14b
    location: local      # overrides session default
    subtasks:
      - id: T-1.1
        description: "Write unit tests"
        # inherits T-1's model assignment
      - id: T-1.2
        description: "Review security logic"
        model: claude-3.5-sonnet
        location: cloud   # override for this subtask only
```

When `model` is omitted at any level, the parent level's assignment is inherited.

### FR-3: Explicit Location Toggle
Every model invocation must have an explicit `location` attribute (`local` or `cloud`). The system shall **refuse** to route a task if the location is ambiguous.

### FR-4: Resource Budget
The system shall enforce a configurable memory budget:
- **Max local model memory**: e.g., `24GB` (leaves headroom for OS + apps)
- **Max concurrent local models**: e.g., `1` (prevents swap)
- **Preemption policy**: If a new model is requested and would exceed the budget, the system must either queue it or eject the current model (configurable).

### FR-5: Unified Gateway
All model access (local and cloud) shall go through a single gateway API (LiteLLM or equivalent) so that:
- The agent code doesn't need to know *where* the model runs.
- Routing decisions are made by the MCL, not by the agent.
- All calls are logged for auditability.

### FR-6: Model Lifecycle Management
The system shall provide commands to:
- **Start** a local model (load into memory)
- **Stop** a local model (eject from memory)
- **List** running models and their memory usage
- **Status** of the gateway (what's available, what's loaded)

### FR-7: Audit Trail
All model routing decisions shall be logged in the GAP Ledger:
- Which model was used for which task
- Whether it ran locally or in the cloud
- Token usage and cost (if cloud)

### FR-8: Routing Advisor (Dry-Run Mode)
The system shall provide a `suggest` command that proposes model assignments:
- Reads the task graph and privacy tags from `requirements.md`
- Queries the model registry (local models) and optionally the OpenRouter catalog (cloud models)
- Proposes an assignment that keeps `private`-tagged work local and routes the rest optimally
- The supervisor reviews and approves the suggestion at the **Model Assignment Gate**
- This is a *proposal*, not an override — the supervisor always has final say

### FR-9: Privacy-Aware Routing
Requirements and tasks may carry a `privacy` tag:
- `private`: Must run on a local model. The system shall refuse to route to cloud.
- `public`: May run on cloud or local (cost/quality optimized).
- Default: `public` (explicit opt-in to privacy)

Privacy tags propagate: if a requirement is tagged `private`, all tasks traced to that requirement inherit the tag unless explicitly overridden by the supervisor.

---

## 4. Non-Functional Requirements

### NFR-1: No Swap
The system shall monitor available memory before loading a local model. If loading would cause the system to use swap memory, the request shall be denied with a clear error message.

### NFR-2: Startup Latency
Local model loading should display progress feedback. The supervisor should never wonder if their machine is frozen.

### NFR-3: Graceful Degradation
If a local model server is not running, the system shall report this clearly rather than silently falling back to a cloud model.

---

## 5. Updated Alignment Flow

Model assignment is a **new gate** in the alignment phase, positioned between task definition and checkpoint selection:

```
[ ALIGNMENT PHASE ]
Requirements → Design → Tasks → Model Assignment → Checkpoints
    (gate)     (gate)   (gate)      (gate)           (gate)
                                      ↑
                               NEW: MCL Gate
```

This ensures the supervisor reviews *what work will be done* (tasks) separately from *who does the work* (model assignment) and *when to pause for review* (checkpoints).

---

## 6. Architecture Sketch

```
┌──────────────────────────────────────────────────────────────┐
│  GAP Protocol Engine                                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  tasks.md (with model assignments)                     │  │
│  │  T-1: model=qwen-14b, location=local, privacy=private  │  │
│  │  T-2: model=claude-3.5-sonnet, location=cloud           │  │
│  └───────────────────┬────────────────────────────────────┘  │
│                      ▼                                       │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Model Control Layer (MCL)                             │  │
│  │  • Registry          (GAP owns)                        │  │
│  │  • Budget Policy      (GAP defines the rule)           │  │
│  │  • Routing Advisor   (GAP proposes)                    │  │
│  └───────────────────┬────────────────────────────────────┘  │
└──────────────────────┼───────────────────────────────────────┘
                       ▼
        ┌──────────────────────────────┐
        │  Unified Gateway (LiteLLM)   │
        │  localhost:4000              │
        └──────┬───────────────┬───────┘
               ▼               ▼
     ┌─────────────────┐ ┌──────────────┐
     │ Local Runtime    │ │ Cloud APIs    │
     │ (sovereign-inf)  │ │ OpenRouter    │
     │  MLX :8080       │ │ OpenAI        │
     │  Ollama :11434   │ │               │
     │  Budget Enforcer │ │               │
     │  (enforces rule) │ │               │
     └─────────────────┘ └──────────────┘
```

**Responsibility split:**
- **GAP** defines the budget policy ("max 24GB for local models") and the routing rules
- **sovereign-inference** enforces the budget at runtime (it knows the actual hardware state)

---

## 7. Resolved Design Decisions

| # | Question | Decision |
|---|----------|----------|
| 1 | Per-task or per-phase model assignment? | **Both.** Cascading: per-artifact default → per-task override → per-subtask override. Model Assignment is a new gate after Tasks, before Checkpoints. |
| 2 | Budget enforcer ownership? | **Split.** GAP defines the policy. sovereign-inference enforces it at runtime. |
| 3 | Dry-run mode? | **Yes.** A Routing Advisor that reads task graph + privacy tags and suggests model assignments. Supervisor approves at the Model Assignment Gate. |

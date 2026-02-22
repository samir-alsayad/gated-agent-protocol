# The Artifact-Agnostic Engine Architecture

This document describes the future evolution of GAP from a hardcoded `software-engineering` pipeline into a generic, universal protocol engine that can handle any arbitrary project structure (e.g., `programs` and `campaigns` instead of `tasks` and `plans`).

## The Problem: Hardcoded Logic
Currently, the GAP CLI (specifically `src/gap/commands/gate.py`) contains hardcoded logic checking string values:
```python
if step == "plan":
    # Do special plan validation
if step == "design":
    # Do special design staging
```
This binds the Engine to one specific workflow. If a user (like the `Ascent/school` project) defines a step called `campaign`, GAP will crash or fail to route it correctly because it has no hardcoded rule for `campaign`.

## The Solution: Manifest-Driven Routing

To make GAP truly universal and artifact-agnostic, the core Engine must never "know" what a step means. It should simply read the `manifest.yaml` and follow generic routing and validation instructions defined by the Protocol Author.

We introduce two new properties to the `Step` definition in `manifest.yaml`: `routing` and `validator`.

### 1. The `routing` Property
Defines exactly how an artifact moves through the project hierarchy.

*   `routing: proposal` 
    *   **Behavior:** The Agent writes a draft. GAP forces it into `.gap/proposals/`. When the supervisor types `gap gate approve`, GAP moves it from proposals to the live directory.
    *   **Use Case:** `tasks.yaml`, `design.md`, `campaign.yaml`

*   `routing: direct`
    *   **Behavior:** The Supervisor authors the document directly in the live directory. When they type `gap gate approve`, GAP skips the proposals folder entirely and simply locks the status in the ledger.
    *   **Use Case:** `plan.yaml`, `program.yaml`

### 2. The `validator` Property (Python Plugins)
If the Engine is completely generic, how do we enforce complex business logic? (E.g., "The `plan.yaml` MUST contain an execution envelope for every ID listed in `tasks.yaml`").

We use a plugin architecture. The Protocol Author can write a custom Python script and attach it to the step in the manifest:

```yaml
flow:
  - step: tasks
    artifact: .gap/tasks.yaml
    routing: proposal
    
  - step: plan
    artifact: .gap/plan.yaml
    routing: direct
    validator: gap.plugins.validate_plan_tasks  # <-- The Plugin Hook
```

**Execution Flow:**
1. The supervisor types `gap gate approve plan`.
2. The Engine sees `routing: direct` and checks the live `.gap/plan.yaml`.
3. Before locking the ledger, the Engine sees `validator: gap.plugins.validate_plan_tasks`. 
4. The Engine dynamically loads that Python function and executes it.
5. If the plugin returns `True` (all tasks have an envelope), the Engine locks the ledger. If it raises an Exception ("Missing envelope for T-2!"), the Engine aborts the approval and shows the error to the user.

## Why this Architecture Wins
1. **Zero Hardcoding:** The `src/core/` and `src/commands/` folders can be dramatically simplified into a generic `Router`. We completely delete complex python files like `auditor.py` or `validator.py` from the core engine.
2. **Infinite Flexibility:** A user can drop `manifest.yaml` into any project in the world, invent 10 completely new artifact types, define their routing, write 3 custom python validation scripts, and GAP will orchestrate the entire project flawlessly on day one without requiring a single change to the `gap` CLI source code.

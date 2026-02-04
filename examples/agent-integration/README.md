# GAP Agent Integration Example

This example shows how to integrate GAP into any AI coding agent (OpenCode, Cursor, Cline, etc.).

## The Problem

Without governance, AI agents:
- Skip requirements gathering
- Make assumptions about design
- Write code without approval
- Can't be interrupted mid-task

## The Solution

The `gap_harness.py` module wraps the GAP CLI and provides a Python API.

---

## The Two Phases

GAP divides agent work into two distinct phases:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION PHASE                               │
│  (Requirements → Design → Policy)                               │
│                                                                 │
│  Agent: Proposes artifacts                                      │
│  Supervisor: Reviews and approves                               │
│  Gate: Always TRUE (human approval required)                    │
│  Output: Approved plan with ACLs                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Approved Plan + ACLs
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTION PHASE                              │
│  (Tasks → Code → Tests)                                         │
│                                                                 │
│  Agent: Executes approved tasks                                 │
│  Harness: Enforces ACLs (allowed files, commands)               │
│  Gate: Can be FALSE (autonomous) or checkpoint-based            │
│  Output: Artifacts locked to approved scope                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Agent Loop

```
                    ┌─────────────────┐
                    │  Which Phase?   │
                    └────────┬────────┘
                             │
           ┌─────────────────┴─────────────────┐
           │                                   │
           ▼                                   ▼
   ┌───────────────┐                   ┌───────────────┐
   │   DECISION    │                   │   EXECUTION   │
   │    PHASE      │                   │    PHASE      │
   └───────┬───────┘                   └───────┬───────┘
           │                                   │
           ▼                                   ▼
   ┌───────────────┐                   ┌───────────────┐
   │ Write to      │                   │ Check ACL:    │
   │ .gap/proposals│                   │ can_write()?  │
   └───────┬───────┘                   └───────┬───────┘
           │                                   │
           ▼                                   │ Yes
   ┌───────────────┐                           ▼
   │ Request       │                   ┌───────────────┐
   │ Approval      │                   │ Write Live    │
   │ & STOP        │                   │ (if allowed)  │
   └───────────────┘                   └───────┬───────┘
                                               │
                                               ▼
                                       ┌───────────────┐
                                       │ Checkpoint?   │
                                       └───────┬───────┘
                                               │
                                  ┌────────────┴────────────┐
                                  │                         │
                                  ▼                         ▼
                          ┌─────────────┐           ┌─────────────┐
                          │  explicit/  │           │  batch:     │
                          │  every:     │           │  continue   │
                          │  PAUSE      │           └─────────────┘
                          └─────────────┘
```

---

## Key Principle

The agent **never** writes directly to live files for gated phases.

| Phase | Gate | Behavior |
|-------|------|----------|
| Decision (req/design/policy) | `true` | Write to proposals → Wait for approval |
| Execution (tasks/code) | `false` | Write live, but ACL-locked |
| Execution (tasks/code) | `true` | Write live, pause at checkpoints |

---

## Python API

```python
from gap_harness import GAPHarness

harness = GAPHarness("/path/to/project")

# Check what phase we're in
current = harness.get_current_phase()  # "requirements"

# DECISION PHASE: Always propose, never write live
if current in ["requirements", "design", "policy"]:
    harness.propose(current, content)
    print(harness.request_approval(current))
    return  # STOP - wait for human

# EXECUTION PHASE: Check ACL and Checkpoints
if harness.is_execution_phase(current):
    # Rule 1: Check security boundary
    if harness.can_write("src/auth/login.py"):
        write_file("src/auth/login.py", code)
        
        # Rule 2: Gated Execution (Checkpoints)
        if harness.should_pause("3.1"):
             print(harness.request_approval("implementation"))
             return  # PAUSE - wait for supervisor
    else:
        raise PermissionError("ACL does not allow this file")
```

---

## Integration with OpenCode

1. At agent startup: `harness = GAPHarness(project_root)`
2. Before any action: Check phase via `get_current_phase()`
3. **Gated Decisions**: Always propose, always STOP for approval
4. **Gated Execution**: Check ACL via `can_write()`, respect checkpoints via `should_pause()`
5. Human runs `gap gate approve <phase>` or `gap gate continue`
6. Agent resumes

This creates a **supervisor-in-the-loop** workflow where the AI proposes, supervisors (human or AI) approve, and work proceeds incrementally via gated execution.

# GAP Agent Integration Example

This example shows how to integrate GAP into any AI coding agent (OpenCode, Cursor, Cline, etc.).

## The Problem

Without governance, AI agents:
- Skip requirements gathering
- Make assumptions about design
- Write code without approval
- Can't be interrupted mid-task

## The Solution

The `gap_harness.py` module wraps the GAP CLI and provides a Python API:

```python
from gap_harness import GAPHarness

harness = GAPHarness("/path/to/project")

# Check what phase we're in
current = harness.get_current_phase()  # "requirements"

# Check if we can write to a file
if harness.can_write("src/auth/login.py"):
    # Proceed
else:
    # STOP - no permission

# Write a proposal (not live)
harness.propose("requirements", content)

# Request human approval and STOP
print(harness.request_approval("requirements"))
```

## The Agent Loop

```
┌─────────────────┐
│  Get Phase      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     No      ┌─────────────────┐
│  Can Proceed?   │────────────▶│  STOP (Locked)  │
└────────┬────────┘             └─────────────────┘
         │ Yes
         ▼
┌─────────────────┐
│  Do Work        │
│  (Proposals)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     gate:true    ┌─────────────────┐
│  Check Gate     │─────────────────▶│  Request        │
└────────┬────────┘                  │  Approval       │
         │ gate:false                │  & STOP         │
         ▼                           └─────────────────┘
┌─────────────────┐
│  Write Live     │
│  (Autonomous)   │
└─────────────────┘
```

## Key Principle

The agent **never** writes directly to live files for gated phases.

1. `gate: true` → Write to `.gap/proposals/` → Human approves → Live
2. `gate: false` → Write directly to live artifact

## Integration with OpenCode

To add GAP to OpenCode or similar tools:

1. At agent startup: `harness = GAPHarness(project_root)`
2. Before any file write: `if not harness.can_write(path): STOP`
3. After completing phase work: `harness.request_approval(phase)` and STOP
4. Human runs `gap gate approve <phase>`
5. Agent resumes with next phase

This creates a **human-in-the-loop** workflow where the AI proposes, humans approve, and work proceeds incrementally.

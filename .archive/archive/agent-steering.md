# Standard: Agent Steering & Configuration
**Version 1.0 (Harness-Driven Context)**

## 1. Objective
In the GAP Architecture, the Agent is not the driver; it is the engine. The **Harness** (the IDE or Tool) drives the process by programmatically injecting the current state into the Agent's context.

## 2. The Context Injection Contract
The Agent does NOT "decide" which phase it is in. The Harness **enforces** the phase by:
1.  **System Prompt Replacement**: Changing the `SYSTEM` message to match the current Gate.
2.  **Tool Whitelisting**: Enabling/Disabling specific tools (e.g., stripping `shell` access during Planning).

## 3. Required System Instructions (Injected by Harness)
The Harness MUST inject a prompt structure similar to this for each state:

### 3.1 State: Planning / Definition
```text
SYSTEM:
[PROTOCOL]: software-development-v1
[MODE]: PLANNING
[GATE]: gate_plan (Goal: plan.md)

INSTRUCTIONS:
You are in Planning Mode.
1. Read the workspace context.
2. Generate the logic for the implementation.
3. OUTPUT the 'plan.md' file.
4. APPEND the '## Access Control' block to request write permissions for the next phase.

CONSTRAINTS:
- You CANNOT write code (permission denied).
- You CANNOT run shell commands (permission denied).
```

### 3.2 State: Execution / Action
```text
SYSTEM:
[PROTOCOL]: software-development-v1
[MODE]: EXECUTION
[GATE]: gate_synthesis

INSTRUCTIONS:
You are in Execution Mode.
The user has approved your plan.
Your write access is UNLOCKED for the files listed in the ACL.

1. Implement the changes defined in 'plan.md'.
2. Verify using the tests defined in 'plan.md'.
```

## 4. The ACL Mandate
Regardless of the mode, the Agent is instructed:
> "To transition from Planning to Execution, you MUST generate the **Embedded ACL Block**. This is your key to the next phase."

## 5. Failure Modes
If the Agent attempts to write outside its injected ACL:
- **Harness Action**: Intercept request -> Return `PermissionError`.
- **Agent Reaction**: "I must request permission by updating the Plan/ACL."

# GAP Taxonomy (Authoritative)

**Purpose:** Define the language of GAP. Agents must use these terms consistently.
**Core Philosophy:** [Board of Decisions](DECISIONS.md)

---

## 1. Governance Terms (The Law)

### Alignment Record (Decision Record)
An explicit commitment that constrains future work. Must be **Approved** by the User.
*   **Requirements**: Intent (What/Why).
*   **Design**: Structure (How).
*   **Policy**: Governance (Rules).
*   **Task**: Operational (Actions).

**Note**: Alignment Records are created during the **Alignment Phase Class**.

### Execution Output
The material produced by performing a Task.
*   **Status**: Non-authoritative, mutable by default.
*   **Examples**: Code, Prose, Lessons, Assignments.
*   **Agent Execution**: The Agent producing the output (e.g., Scribing a file).

### Gate
A checkpoint where work is reviewed and approved.
*   **Alignment Gate**: Mandatory. Approves a Proposal into authoritative Alignment.
*   **Execution Gate**: Optional. Validates Execution Output before it is promoted.
*   **State transition**: Transitions from `PENDING` to `APPROVED`.

### Ledger
The immutable history of which Decision Records have been approved.

---

## 2. Core Architecture

### Project
A directory managed by GAP (contains `manifest.yaml`).

### Protocol
A re-usable workflow template (e.g., `instructional`, `software`).

### Phase Classes
The two fundamental categories of workflow phases.
*   **Alignment Phase Class**: The "Sovereign Gating" phase. Captures Requirements, Design, Policy, and Tasks. Authority is created here.
*   **Execution Phase Class**: The "Throughput" phase. Derived from the Alignment contract. Captures the generation of the actual content (Code, Prose, etc.).

### Phase
A specific state inside a Phase Class (e.g., `Requirements Phase` is an Alignment Phase).

### Manifest
The configuration file defining the Project's Protocol.

---

## 3. Task & Plan System

### Task
A logical work unit describing **what must change** to satisfy the design.
*   **Content**: Description, traceability to design/requirements, expected outputs
*   **Scope**: Pure logical decomposition, no execution context
*   **Proposal**: Created by agent, approved/edited by supervisor
*   **Formats**: 
  - **Machine-readable**: `.gap/tasks.yaml` (structured YAML for validation and processing)
  - **Human-readable**: `docs/tasks.md` (markdown for review and editing)
*   **Sync**: Changes in one format must be reflected in the other

### Plan
The authorized execution envelope attached to approved tasks, describing **how changes are allowed**.
*   **Content**: ACL, locality, model assignment, checkpoints
*   **Construction**: Created by supervisor after task approval
*   **Purpose**: Defines execution boundaries and permissions
*   **Format**: YAML mapping task IDs to execution envelopes

### Execution Envelope
The complete set of permissions and constraints for a task.
*   **ACL (Access Control List)**: What files the executor may touch
*   **Locality**: Where computation occurs (local vs cloud)
*   **Model Assignment**: Which cognitive model is permitted
*   **Checkpoints**: Where human review is required

### ACL (Access Control List)
A declaration of what the executor is allowed to do, not an enforcement mechanism.
*   **Filesystem**: Read/write permissions on paths
*   **Shell**: Commands that may be executed
*   **Visibility**: Must be visible and explicitly accepted by supervisor
*   **Enforcement**: External systems may honor; GAP only records approval

### Locality
The computational venue for task execution.
*   **Local**: Execution on supervisor's machine
*   **Cloud**: Execution on remote infrastructure
*   **Explicit**: Must be declared, never inferred
*   **Manual**: Supervisor defines, not suggested by agent

### Model Assignment
The specific cognitive model authorized for task execution.
*   **Explicit**: Supervisor selects model identity
*   **No Routing**: GAP does not orchestrate or select models
*   **Permission Record**: Records which model was allowed, not how to use it

### Checkpoint
A declared pause right where human review is required.
*   **Declaration**: Specified in Plan, not runtime strategy
*   **Enforcement**: GAP blocks progress until supervisor intervenes
*   **Purpose**: Intentional friction to maintain control

---

## 4. Workflow States

### Task States
*   **PROPOSED**: Agent has created task definition
*   **APPROVED**: Supervisor has accepted task (logical work)
*   **PLANNED**: Supervisor has attached execution envelope
*   **EXECUTING**: Task is being performed
*   **COMPLETE**: Task execution finished

### Gate States
*   **LOCKED**: Waiting for dependencies
*   **UNLOCKED**: Ready for work
*   **PENDING**: Work complete, awaiting supervisor approval
*   **APPROVED**: Supervisor approved, can proceed

### Plan States
*   **DRAFT**: Execution envelope being constructed
*   **VALID**: Envelope complete and consistent
*   **APPROVED**: Supervisor has signed envelope
*   **ACTIVE**: Envelope governing current execution

---

## 5. Core Principles

### Necessity vs Permission
*   **Tasks** describe what must be done (necessity)
*   **Plan** describes how it's allowed to be done (permission)
*   **Invariant**: These must never be conflated

### Manual Authority Phase
*   **Current Mode**: Supervisor defines all execution parameters
*   **No AI Suggestions**: LLM does not propose ACL, models, locality, checkpoints
*   **Explicit Control**: Every permission is consciously set by supervisor

### Consent Ledger, Not Automation
*   **Records**: Proposals and approvals
*   **Requires**: Human approval for all state transitions
*   **Tracks**: State and decisions
*   **Does Not**: Sandbox, auto-route, optimize, or make decisions

### Declaration, Not Enforcement
*   **ACL**: Declares what's allowed, doesn't enforce it
*   **Model Assignment**: Records which model was permitted, doesn't route to it
*   **Checkpoints**: Declares where to pause, doesn't decide when to stop

---

## 6. File Structure

### Core Files
```
.gap/
├── status.yaml          # Current phase states (ledger)
├── tasks.yaml          # Machine-readable tasks (structured YAML)
├── plan.yaml           # Execution envelopes (permissions)
└── acls/               # Legacy ACL storage (deprecated)

docs/
├── requirements.md     # Human-readable requirements
├── design.md          # Human-readable design
└── tasks.md           # Human-readable task list (rendered from .gap/tasks.yaml)

src/                   # Implementation artifacts
```

### Manifest Structure
```yaml
flow:
  - step: requirements
    artifact: docs/requirements.md
    gate: true
    needs: []

  - step: design
    artifact: docs/design.md
    gate: true
    needs: [requirements]

  - step: tasks
    artifact: .gap/tasks.yaml
    gate: true
    needs: [design]

  - step: plan
    artifact: .gap/plan.yaml
    gate: true
    needs: [tasks]

  - step: implementation
    artifact: src/
    gate: false
    needs: [plan]
```
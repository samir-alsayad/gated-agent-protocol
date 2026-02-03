# GAP Schema: The Protocol Manifest

**Objective**: To define the Structure of a Protocol (The DNA).
**Location**: `protocols/[name]/manifest.yaml`

## 1. Concept
A Protocol is a reusable template for Decision Making. It defines the "Phases" that a project must go through.

## 2. Schema
```yaml
kind: protocol
name: instructional
version: 1.0.0

# The DNA: phases of Decision
flow:
  - phase: requirements
    artifact: requirements.md
    gate: true # True (Manual/Supervisor) | False (Autonomous)
  - phase: design
    artifact: design.md
    gate: true
  - phase: execution_policy
    description: "Proposed Execution Policy (Autonomous vs Gated)"
    artifact: policy.md
    gate: true
  - phase: task
    artifact: tasks.md
    gate: true
  - phase: execution
    artifact: walkthrough.md
    gate: true

# The Tools: Templates this Protocol provides
templates:
  requirements: templates/requirements.md
  design: templates/design.md
  tasks: templates/tasks.md
  execution: templates/walkthrough.md

## 3. The Traceability Standard
Every artifact produced by this Protocol MUST adhere to the **Phase-Specific Linking Pattern**:

**1. Requirements (The Source: EARS Syntax)**
*   Must be structured as numbered sections.
*   Must use **EARS** (Easy Approach to Requirements Syntax):
    > **WHEN** [Trigger] **THE** [System] **SHALL** [Response].

**2. Design (The Bridge: Correctness Properties)**
*   Must contain a `## Correctness Properties` section.
*   Each Property filters the Design into a verifiable statement.
*   **Link Syntax**:
    ```markdown
    **Property 1: State Consistency**
    *For any* state query...
    **Validates: Requirements 1.1**
    ```

**3. Execution Policy (The Rules: Configuration Declaration)**
*   Must explicitly decide between **Project Law** (Default) or **Session Exception**.
*   **Syntax**:
    ```markdown
    ### Constraint 1: Execution Mode
    **Question**: Use Project Default (Gated) or Declare Exception?
    **Decision**: Exception (Autonomous)
    **Rationale**: Research spike, no safety risk.
    **Manifest Key**: `execution.mode` (gated | autonomous)

    ### Constraint 2: Granularity
    **Context**: Complex dependencies.
    **Decision**: Function-Level
    **Rationale**: To prevent large-scale regressions.
    **Manifest Key**: `task_granularity.max_scope` (file | function | block)

    ### Constraint 3: Checkpoints
    **Context**: Long-running refactor.
    **Decision**: Batch
    **Rationale**: Review all changes at end.
    **Manifest Key**: `checkpoints.strategy` (explicit | every | batch)

**4. Tasks (The Action: Checklists)**
*   Must link back to Requirements or Properties.
*   **Link Syntax**:
    ```markdown
    - [ ] 1. Implement Thought Firewall
      - _Requirements: 1.3, 1.4_
    
    - [ ] 1.1 Write property test
      - **Property 5: Thought Firewall Integrity**
      - **Validates: Requirements 1.4**
    ```

## 4. Invariants
- **Flow Integrity**: A Project using this protocol MUST execute these phases in order.
- **Artifacts**: The output artifacts are mandatory.

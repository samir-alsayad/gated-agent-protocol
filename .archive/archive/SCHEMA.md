# GAP Schema: The Manifest

**Objective**: To define the `manifest.yaml` structure for Protocols and Projects.

## 1. The Protocol Manifest
Located at: `protocols/[name]/manifest.yaml`

```yaml
kind: protocol
name: instructional
version: 1.0.0

# The DNA: phases of Decision
flow:
  - phase: requirements
    artifact: requirements.md
    gate: true # True | False
  - phase: design
    artifact: design.md
    gate: true # True | False
  - phase: execution_policy
    description: "Proposed Execution Policy (Autonomous vs Gated)"
    artifact: policy.md
    gate: true # True | False
  - phase: task
    artifact: tasks.md
    gate: true # True | False
  - phase: execution
    artifact: walkthrough.md
    gate: true # True | False


# The Tools: Templates this Protocol provides
templates:
  requirements: templates/requirements.md
  design: templates/design.md
  tasks: templates/tasks.md
  execution: templates/walkthrough.md
```

## 2. The Project Execution Manifest
Located at: `[Project]/.gap/manifest.yaml`

```yaml
name: Project_Name
version: 0.1.0
execution:
  mode: gated            # autonomous | gated

  # Task-shaping constraint (decided BEFORE tasks)
  task_granularity:
    max_scope: function  # semantic upper bound, domain-specific string

  # Execution control (decided WITH the policy)
  checkpoints:
    strategy: explicit   # explicit | every | batch
    after_tasks:
      - "2.1"
      - "3.4"
      - "6.2"
```

## 3. The Invariant
> **Granularity constrains how tasks are written.**
> **Checkpoints constrain when execution pauses.**
> Both must be declared before execution, and neither belongs to the execution phase itself.
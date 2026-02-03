# GAP Schema: The Project Manifest

**Objective**: To define the Structure of a Project (The Instance).
**Location**: `[Project]/.gap/manifest.yaml`

## 1. Concept
A Project is an instantiation of a Protocol. It defines the "Law" for that specific repo.

## 2. Schema
```yaml
name: Project_Name
version: 0.1.0

# The Governing Law for Execution
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

## 3. Invariants
- **Immutability**: This file represents the "Project Law".
- **Precedence**: This is the default policy unless a Session Exception is declared.

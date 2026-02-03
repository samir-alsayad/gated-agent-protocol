# GAP Schema: The Session & Tool Manifests

**Objective**: To define the Runtime Configuration (The Exception).
**Location**: `.gap/gap.yaml` (Tool) and `.gap/sessions/[id]/config.yaml` (Session).

## 1. The Tool Registry (`gap.yaml`)
Tracks the active state of the tooling.

```yaml
# State Pointer
active_session: "mission_docs_sprint_01"

# Session Registry (Index)
sessions:
  - id: "mission_docs_sprint_01"
    path: ".gap/sessions/mission_docs_sprint_01"
    created_at: "2026-02-03T18:30:00Z"
    status: active
```

## 2. The Session Configuration (`config.yaml`)
Defines the **Declared Exceptions** for a specific mission.

```yaml
session_id: "mission_docs_sprint_01"
parent_project: "Kernel_Refactor"

# EXCEPTION DECLARATION
# These values temporarily override the Project Manifest for this session only.
execution_exceptions:
  mode: autonomous  # Overrides 'gated'
  
  task_granularity:
    max_scope: file # Overrides 'function'

  checkpoints:
    strategy: explicit
    after_tasks:
      - "final_review"
```

## 3. Invariants
- **Transparency**: Every exception declared here MUST be logged to the Ledger upon instantiation.
- **Scope**: Exceptions are valid ONLY for the lifetime of this session.
- **No Hidden State**: There are no "implicit" overrides; everything must be in `execution_exceptions`.

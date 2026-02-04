# Execution Policy: {{ project_name }}

## 1. Governance Mode
**Question**: Use Project Law (Gated) or Declare Session Exception?
**Decision**: {{ execution_mode }}
**Rationale**: {{ mode_rationale }}

**Manifest Key**: `execution.mode` (gated | autonomous)

## 2. Granularity
**Context**: {{ granularity_context }}
**Decision**: {{ granularity_decision }} (e.g., unit | lesson | block)
**Rationale**: {{ granularity_rationale }}

**Manifest Key**: `task_granularity.max_scope`

## 3. Checkpoints
**Strategy**: {{ checkpoint_strategy }} (explicit | every | batch)
**Rationale**: {{ checkpoint_rationale }}

**Manifest Key**: `checkpoints.strategy`

---
**Authority**: Approved Execution Policy constrains the decomposition of Tasks.

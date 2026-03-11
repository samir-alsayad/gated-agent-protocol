# Execution Policy: {{ project_name }}

## 1. Governance Mode
Define the operational state of the Harness.

**Question**: Use Project Law (Gated) or Declare Session Exception?
**Decision**: {{ execution_mode }}
**Rationale**: {{ mode_rationale }}

**Manifest Key**: `execution.mode` (gated | autonomous)

## 2. Granularity
Define the semantic upper bound for individual task actions.

**Context**: {{ granularity_context }}
**Decision**: {{ granularity_decision }}
**Rationale**: {{ granularity_rationale }}

**Manifest Key**: `task_granularity.max_scope` (file | function | block | sequence)

## 3. Checkpoints
Define mandatory pause points for human pulse-checks during execution.

**Strategy**: {{ checkpoint_strategy }}
**Rationale**: {{ checkpoint_rationale }}

**Manifest Key**: `checkpoints.strategy` (explicit | every | batch)

### [Optional] Explicit Pause Points
If strategy is `explicit`, list the Task IDs that require a hard stop.

- {{ task_id_1 }}
- {{ task_id_2 }}

## 4. Derived Rules
Any additional constraints derived from the Structural Design.

*   {{ additional_rule_1 }}

---
**Authority:** Approved Execution Policy constrains the decomposition of Tasks and the extraction of ACLs.

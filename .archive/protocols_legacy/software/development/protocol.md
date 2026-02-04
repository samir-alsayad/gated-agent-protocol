# Protocol: Software Development (Specs-First)

This protocol governs the engineering of software systems. It defends **Determinism** by ensuring all code is derived from a traceable chain of intent and invariants.

## Philosophy: Specs-First Architecture
Always prioritize deep planning and architecture before any code is written. This protocol enforces a "Gate-based" progression where each phase must be ratified before the next begins.

## Rule: Read-Open, Write-Locked
**You have full READ access to the codebase** to plan your features effectively.
However, you **MUST NOT write or mutate** any project code until the Execution Path (`plan.md`) is approved.

---

## Operational Gates

| Gate | Artifact | Verification Rule |
|:-----|:---------|:------------------|
| `gate_intent` | `intent.md` | Every goal MUST have at least one constraint. |
| `gate_invariant` | `spec.md` | Every property MUST validate at least one Goal ID. |
| `gate_path` | `plan.md` | Total step coverage MUST account for 100% of Goals and Properties. |
| `gate_synthesis` | `walkthrough.md` | Implementation MUST satisfy all gated artifacts. |

### Gate I: Intent Lockdown (`intent.md`)
- **Action**: Define goals and constraints using EARS syntax.
- **Sections**: Context, Goals, Constraints.
- **Mandatory**: Every constraint must use WHEN..SHALL or IF..THEN..SHALL grammar.

### Gate II: Invariant Definition (`spec.md`)
- **Action**: Define high-level architecture (Mermaid Blueprint) and properties.
- **Sections**: Architecture, Properties, Dependencies, Data Models.
- **Mandatory**: Every property must be a verifiable invariant.

### Gate III: Execution Path (`plan.md`)
- **Action**: Create a checklist of implementation steps.
- **Sections**: Implementation Steps with traceability metadata.
- **Traceability**: Every step MUST link back to Goals, Constraints, or Properties.
- **ACL**: Embedded Access Control block defines allowed writes/execs.

### Gate IV: Synthesis (`walkthrough.md`)
- **Action**: Implement the plan and document the changes.
- **Sections**: Changes Made, What Was Tested, Validation Results.
- **Verification**: Must include proof of correctness (test output, screenshots, etc.).

---

## Metadata Standard
- **ID Prefixes**: `G-` (Goal), `C-` (Constraint), `P-` (Property), `STEP-` (Task).
- **Format**: `— *Trace: G-01, C-02, P-01*` footer for every step.

---
*Governed by GAP - 2026*

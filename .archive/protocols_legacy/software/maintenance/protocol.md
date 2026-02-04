# Protocol: Software Maintenance (Patch-Flow)

## Mission
The **Software Maintenance Protocol** is designed for high-velocity correction, refactoring, and patching of existing systems. It prioritizes **Reliability** and **Minimal Invasive Correction** over the exhaustive "Specs-First" synthesis used in new development.

## The Semantic Pillars

### 1. The Diagnosis (Understand)
Unlike new development, the intent here is driven by an existing failure or inefficiency. The agent must first prove it understands the **Root Cause** before proposing a change. The diagnosis also includes a **Repair Strategy** and **Implementation Steps**.

### 2. The Synthesis (Execute)
The agent implements the approved fix and produces a **Walkthrough** documenting what was changed and how it was verified.

## Operational Gates

| Gate | Artifact | Verification Rule |
|:-----|:---------|:------------------|
| `gate_diagnosis` | `diagnosis.md` | Must identify root cause and propose traceable fix path. |
| `gate_synthesis` | `walkthrough.md` | Patch must satisfy diagnostic requirements and pass tests. |

### Gate 1: Diagnosis Approval (`diagnosis.md`)
The agent produces a diagnosis that maps the reported issue to specific code segments.
- **Sections**: Issue Description, Root Cause Analysis, Impact Assessment, Repair Strategy, Implementation Steps.
- **Rigor**: Must include a reproduction step or clear logic trace.
- **ACL**: Embedded Access Control block defines allowed writes/execs.

### Gate 2: Synthesis (`walkthrough.md`)
The agent implements the fix and documents the changes.
- **Sections**: Changes Made, What Was Tested, Validation Results.
- **Rigor**: Must include proof of verification (test output, screenshots, etc.).

---
*Governed by GAP - 2026*

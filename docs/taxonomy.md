# GAP Taxonomy (Authoritative)

**Purpose:** Define the language of GAP. Agents must use these terms consistently.
**Core Philosophy:** [Board of Decisions](DECISIONS.md)

---

## 1. Governance Terms (The Law)

### Decision Record
An explicit commitment that constrains future work. Must be **Gated** (User Approved).
*   **Requirements**: Intent decisions (What/Why).
*   **Design**: Structural decisions (How).
*   **Task**: Operational decisions (Action).

**Note**: A Decision Record is created during a **Decision Phase**.

### Execution Output
The material produced by performing a Task.
*   **Status**: Non-authoritative, mutable by default.
*   **Examples**: Code, Prose, Lessons, Assignments.
*   **Agent Execution**: The Agent producing the output (e.g., Scribing a file).

### Gate
A checkpoint where work is reviewed and approved.
*   **Decision Gate**: Mandatory. Converts a Proposal to Law.
*   **Execution Gate**: Optional. Validates quality before merge.
*   **Types**: True (User Approval) or False (Autonomous Transition).

### Ledger
The immutable history of which Decision Records have been approved.

---

## 2. Core Architecture

### Project
A directory managed by GAP (contains `manifest.yaml`).

### Protocol
A re-usable workflow template (e.g., `instructional`, `software`).

### Phase Classes
The Classes of phases.
*   **Decision Phases**: Captures Decision Records.
*   **Execution Phases**: Derived from the execution policy, the Phases between the approval Gates.

### Phase
A specific phase inside a Phase Class (e.g., `Requirements Phase`).

### Manifest
The configuration file defining the Project's Protocol.

---
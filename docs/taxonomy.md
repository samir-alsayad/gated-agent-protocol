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
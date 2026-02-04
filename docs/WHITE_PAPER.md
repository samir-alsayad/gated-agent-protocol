# GAP: The Gated Agent Protocol (v2.0)
**The Open Standard for Managed Agentic Workflows**

---

## 1. The Challenge: Contextual Drift

As Large Language Models (LLMs) transition from chat interfaces to autonomous agents, they encounter a fundamental reliability challenge: **Contextual Drift**.

In simple chat sessions, minor deviations are annoying but harmless. In autonomous agentic workflows, however, "hallucinations" or deviations from intent become structural failures. Without rigid synchronization points, long-horizon workflows tend to diverge from the original human requirements as the context window shifts or the agent prioritizes immediate task completion over architectural constraints.

Current solutions often rely on "prompt engineering" to plead with the model to stay on track. **We propose a systems engineering approach: The Gated Agent Protocol (GAP).**

GAP is a **Workflow Enforcement Protocol** that governs agent behavior through machine-enforceable state machines. It transforms probabilistic generation into verifiable engineering compliance.

---

## 2. The Solution: A State Machine of Work

GAP enforces a strict **Chain of Custody** for every action an Agent takes. It divides work into five distinct phases, each with its own artifact and verification gate.

### The Phases of Execution

1.  **Requirements (The Source)**
    *   **Goal**: Define *what* is needed without ambiguity.
    *   **Artifact**: `requirements.md`
    *   **Format Standard**: **EARS** (Recommended) or clear acceptance criteria.
    *   *Example*: "WHEN the user clicks Save, THE System SHALL validate the schema."

2.  **Design (The Blueprint)**
    *   **Goal**: Define *how* to solve it.
    *   **Artifact**: `design.md`
    *   **Validation**: **Design-to-Requirement Mapping**.
    *   *Example*: "**Validates: Requirement 1.2** - The schema validator uses strict typing."

3.  **Execution Policy (The Governance)**
    *   **Goal**: Define the permissions and boundaries of the session.
    *   **Artifact**: `policy.md` (Configuration Declaration).
    *   **Concept**: **Law vs Exception**.
    *   *Example*: "Exception: Grant write access to `src/` for this session."

4.  **Tasks (The Plan)**
    *   **Goal**: Break the design into atomic units of work.
    *   **Artifact**: `tasks.md`
    *   **Standard**: **Traceable Checklists**.
    *   *Example*: "Task 1: Implement Validator (Traces to Property 2)."

5.  **Execution (The Action)**
    *   **Goal**: Perform the work.
    *   **Artifact**: `walkthrough.md`.
    *   **Constraint**: **The Harness**. The Agent is restricted to the approved Task ACLs.

---

## 3. Compliance & Traceability

GAP introduces a **Compliance Chain** that links high-level intent to low-level code. This is enforced via **Use-Case Traceability**:

1.  **Requirement**: The immutable need.
2.  **Property**: The logical design decision.
3.  **Checklist**: The implementation step.

**Why this matters**:
In a compliant workflow, an Agent cannot edit a file unless that action is linked to a Task, which implicitly links it to a Design and Requirement. This prevents "shadow engineering" where agents create code that serves no documented purpose.

Code must have a distinct pedagogical pedigree.

---

## 4. Governance: Law and Exception

GAP solves the rigidity problem of traditional sandboxes with the **Law and Exception** model, inspired by reliable systems engineering practices.

### 1. The Project Manifest (The Law)
*   Located at `.gap/manifest.yaml`.
*   Version-controlled (e.g., Git).
*   Defines the immutable defaults: "This project is Gated. Default scope is Function-Level."

### 2. The Session Config (The Exception)
*   Located at `.gap/sessions/[id]/config.yaml`.
*   Temporary, explicit, logged.
*   Defines the approved deviation: "For *this* session, enable Autonomous Mode."

This ensures that safety is the default, but flexibility is possible—provided it is explicitly declared and auditable.

### 3. Execution Checkpoints
The Harness enforces mandatory pause points during Task execution, acting as a CI/CD pipeline for agent decisions.

*   **Strategy**: Defined in the Policy.
    *   `explicit`: Pause only at listed Task IDs.
    *   `every`: Pause after every single Task (High Security).
    *   `batch`: Run all Tasks, review at the end (High Autonomy).
*   **Mechanism**: At each checkpoint, the Agent verifies its state against the Ledger.
*   **Purpose**: Prevents runaway execution/billing. Guarantees a human "pulse check" on long-horizon work.

---

## 5. Conclusion

GAP is **Infrastructure for Agents**. Just as CI/CD pipelines govern the deployment of code, GAP governs the generation of code.

By embedding Compliance into the Specification and enforcing Traceability through the Ledger, we enable a future where autonomous agents are not just powerful, but **Reliable**.

---
*Open Standard - v2.0 - 2026*

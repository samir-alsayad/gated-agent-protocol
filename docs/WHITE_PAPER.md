# GAP: The Gated Agent Protocol (v2.0)
**The Open Standard for Managed Agentic Workflows**

---

## 1. The Challenge: Contextual Drift

As Large Language Models (LLMs) transition from chat interfaces to autonomous agents, they encounter a fundamental reliability challenge: **Contextual Drift**.

In simple chat sessions, minor deviations are annoying but harmless. In autonomous agentic workflows, however, "hallucinations" or deviations from intent become structural failures. Without rigid synchronization points, long-horizon workflows tend to diverge from the original human requirements as the context window shifts or the agent prioritizes immediate task completion over architectural constraints.

Current solutions often rely on "prompt engineering" to plead with the model to stay on track. **We propose a systems engineering approach: The Gated Agent Protocol (GAP).**

GAP is a **Workflow Enforcement Protocol** that governs agent behavior through machine-enforceable state machines. It transforms probabilistic generation into verifiable engineering compliance.

---

GAP enforces a strict **Chain of Custody** for every action an Agent takes. It divides work into two fundamental **Phase Classes**.

### 1. The Alignment Phase Class (Sovereign Gating)
The Alignment Class consists of the **Decision Records** that define the contract between User and Agent. These are subject to **Mandatory Gating**.

1.  **Requirements (The Source)**: What must be true.
2.  **Design (The Blueprint)**: How the structure satisfies the source.
3.  **Policy (The Governance)**: The rules of the session (ACLs, Gating mode).
4.  **Tasks (The Plan)**: Atomic actions linked to the design.

### 2. The Execution Phase Class (Throughput)
The Execution Class is where the work is performed. It is derived from the Alignment Class and is subject to **Optional Gating**.

5.  **Execution (The Action)**: The generation of code, prose, or data.

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

### 4. Deterministic vs. Probabilistic Boundaries

A core tenet of GAP v2.0 is the **Separation of Concerns** between the Protocol and the Agent.

*   **The Protocol** is **Deterministic**. It handles authority, security, and gating. It asks closed questions ("What is the ACL rule?").
*   **The Agent** is **Probabilistic**. It handles creativity, content, and implementation. It answers open questions ("How do I build this app?").

**The Anti-Patterns GAP Avoids:**
1.  **Hallucinated Policy**: Asking an LLM to generate its own security policy is a vulnerability. The agent might "forget" to restrict itself. In GAP, policies are defined via rigid forms that never pass through the LLM.
2.  **Soft Gates**: A gate that relies on an LLM to classify "Is this dangerous?" is unreliable. GAP gates are binary, user-driven, and ledger-backed.

This separation ensures that while the **work** is creative (AI), the **boundaries** are absolute (Code).

## 5. Governance: Law and Exception


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

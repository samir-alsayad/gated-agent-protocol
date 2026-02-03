# GAP: The Gated Agent Protocol (v2.0)
**The Sovereign Standard for Human-AI Collaboration**

---

## 1. The Crisis of Autonomy: Probabilistic Drift

As Large Language Models (LLMs) transition from chat interfaces to autonomous agents, they encounter a fundamental barrier: **Probabilistic Drift**.

In a chat session, a hallucination is a nuisance. In an autonomous agent, it is a structural failure. Without rigid synchronization points, long-horizon agentic workflows diverge from human intent, with the probability of alignment ($p$) decaying exponentially over time ($t$): 

$$p(t) \to 0$$

Current solutions—"Planning Mode" toggles or simple sandboxes—are insufficient. They either rely on the model's self-restraint (which fails under pressure) or blind the agent completely (reducing utility).

**We propose the Gated Agent Protocol (GAP)**: A Cybernetic Constitution that governs agent behavior through machine-enforceable state machines. GAP transforms probabilistic generation into verifiable engineering.

---

## 2. The Solution: A State Machine of Work

GAP enforces a strict **Chain of Custody** for every action an Agent takes. It divides work into five distinct phases, each with its own artifact and verification gate.

### The Phases of Sovereignty

1.  **Requirements (The Source)**
    *   **Goal**: Define *what* is needed without ambiguity.
    *   **Artifact**: `requirements.md`
    *   **Standard**: **EARS** (Easy Approach to Requirements Syntax).
    *   *Example*: "WHEN the user clicks Save, THE System SHALL validate the schema."

2.  **Design (The Bridge)**
    *   **Goal**: Define *how* to solve it and prove correctness.
    *   **Artifact**: `design.md`
    *   **Standard**: **Correctness Properties**.
    *   *Example*: "**Validates: Requirement 1.2** - The schema validator uses strict typing."

3.  **Execution Policy (The Rules)**
    *   **Goal**: Define the boundaries of the mission.
    *   **Artifact**: `policy.md` (Configuration Declaration).
    *   **Standard**: **Law vs Exception**.
    *   *Example*: "We declare an Exception to run in Autonomous Mode for this session."

4.  **Tasks (The Plan)**
    *   **Goal**: Break the design into atomic units of work.
    *   **Artifact**: `tasks.md`
    *   **Standard**: **Traceable Checklists**.
    *   *Example*: "Task 1: Implement Validator (Traces to Property 2)."

5.  **Execution (The Action)**
    *   **Goal**: Do the work.
    *   **Artifact**: `walkthrough.md`.
    *   **Standard**: **The Harness**. The Agent is locked into the approved Task ACLs.

---

## 3. The Traceability Trinity

GAP introduces a "Golden Thread" that links high-level intent to low-level code. This is enforced via the **Traceability Trinity**:

1.  **Requirement (EARS)**: The immutable truth.
2.  **Property (Design)**: The logical proof that validates the Requirement.
3.  **Checklist (Task)**: The unit of work that implements the Property.

**Why this matters**:
If an Agent tries to edit a file that isn't linked to a Task, which isn't linked to a Property, which isn't linked to a Requirement... **The Harness blocks it.**

Code cannot exist without a pedigree.

---

## 4. Governance: Law and Exception

GAP solves the rigidness problem of traditional sandboxes with the **Law and Exception** model.

### 1. The Project Manifest (The Law)
*   Located at `.gap/manifest.yaml`.
*   Version-controlled (e.g., Git) or otherwise treated as immutable.
*   Defines the defaults: "This project is Gated. Task scope is Function-Level."

### 2. The Session Config (The Exception)
*   Located at `.gap/sessions/[id]/config.yaml`.
*   Temporary, explicit, logged.
*   Defines the deviation: "For *this* session, I authorize Autonomous Mode."

This ensures that safety is the default, but flexibility is possible—provided it is explicitly declared and auditable.

### 3. Execution Checkpoints
The Harness enforces mandatory pause points during Task execution.

*   **Strategy**: Defined in the Policy (`checkpoints.strategy`).
    *   `explicit`: Pause only at listed Task IDs (`after_tasks: [2.1, 3.4]`).
    *   `every`: Pause after every single Task.
    *   `batch`: Run all Tasks, review at the end.
*   **Mechanism**: At each checkpoint, the Agent is frozen until the Human (or Supervisor) explicitly approves continuation.
*   **Purpose**: Prevents runaway execution. Guarantees a human "pulse check" on long-horizon work.

---

## 5. Conclusion

GAP is not just a prompting strategy; it is a **Protocol**. Just as TCP/IP governs the flow of packets, GAP governs the flow of agentic work.

By embedding Security into the Specification and enforcing Traceability through the Trinity, we enable a future where autonomous agents are not just powerful, but **Trustworthy**.

---
*Open Standard - v2.0 - 2026*

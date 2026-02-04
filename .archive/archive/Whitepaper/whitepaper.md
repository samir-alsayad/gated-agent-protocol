# GAP: The Gated Agent Protocol (v1.0)
**Technical Standard - 2026**

---

## 1. Introduction: The Alignment Gap

As Large Language Models (LLMs) transition from chat interfaces to autonomous agents, they encounter a fundamental barrier: **Probabilistic Drift**. In a chat session, a hallucination is a nuisance; in an autonomous agent, it is a structural failure. Without rigid synchronization points, long-horizon agentic workflows diverge from human intent, with the probability of alignment ($p$) decaying exponentially over time ($t$): $$p(t) \to 0$$

**We propose the Gated Agent Protocol (GAP)**, a standard for governing agent behavior through machine-enforceable state machines. By determining the **Containment Layer** of the AI stack, GAP transforms probabilistic generation into verifiable engineering.

---

## 2. Theoretical Framework: The Safety-Utility Paradox

Current agent frameworks force a binary choice:

1.  **God Mode (Open)**: The agent has `sudo` access to the workspace.
    *   *Utility*: Maximum.
    *   *Safety*: Low. A single alignment error can result in destructive data loss (`rm -rf`) or subtle corruption.
2.  **Sandbox (Blind)**: The agent is trapped in a virtual container.
    *   *Utility*: Low. The agent cannot see the intricate dependencies of a real codebase (e.g., cannot resolve imports).
    *   *Safety*: Maximum.

### 2.1 The Crisis: The Toggle Fallacy
Modern Agentic IDEs attempt to solve this with "Planning Mode" toggles. **This is a lie.**
Even when set to "Plan", most agents are merely *prompted* to be careful. They still possess the underlying system permissions to edit `src/main.py` or `rm -rf /`. When the context window fills up or the model gets confused, it **ignores the soft toggle** and executes code anyway.

**GAP fixes this by moving the toggle from the Prompt to the Kernel.**
In a GAP-compliant environment, a "Planning" gate physically strips the `write()` syscall ability from the agent's runtime. It is not an instruction; it is a straightjacket.

### 2.1 The GAP Innovation: Context-Aware Access
Instead of a rigid "Read-Only Planning" phase, GAP enforces **Situation-Specific Least Privilege**. The Protocol Harness dynamically adjusts the agent's permissions based on the active **Gate**.

- **Diagnostic Gates**: May allow `exec` (to run reproduction scripts) but deny `write` (to prevent premature fixes).
- **Planning Gates**: Typically **Read-Only** to force pure reasoning.
- **Execution Gates**: Grant `write` access *only* to the specific files listed in the approved Plan's embedded ACL.

This ensures the agent always has the **Minimum Viable Power** required for the immediate task—no more, no less.

This results in a system that is **"Safe, Not Blind."**

---

## 3. System Architecture

GAP operates as a **Containment Layer** that wraps the probabilistic model. It enforces a **Continuous Security Loop**:

`[State] -> [Gate Permissions] -> [Agent Proposal + ACL] -> [Human Verification] -> [Kernel Unlock]`

### 3.1 The Security Kernel: Impact-Driven Specification
The core security innovation of GAP is **Plan-Derived Access Control**. We do not use separate permission files; instead, the **ACL is Embedded** in the Artifact itself.

When an agent produces a spec artifact (e.g., `plan.md`, `diagnosis.md`, `hypothesis.md`), it MUST include a machine-parsable **Access Control Block** at the end of the file.

**The "Block Definition" Standard:**
```markdown
# Execution Plan
Objective: Refactor Authentication Controller.

## Logic
1. Update `src/auth.py` to use JWT.
2. Add tests in `tests/test_auth.py`.

## Access Control
'''yaml
# The Protocol Harness enforces this whitelist
allow_write:
  - "src/auth.py"
  - "tests/test_auth.py"
allow_exec:
  - "pytest tests/"
'''
```

### 3.2 The Human Gate
When the human approves the artifact, they are concurrently ratifying the Access Control List. The Tool Harness then:
1.  **Extracts** the YAML block.
2.  **Parses** the whitelist.
3.  **Locks** the execution environment to these exact boundaries.

If the block is missing or empty, the environment defaults to **Read-Only**.

---

## 4. The Standard Specification

### 4.1 The Manifest (`manifest.yaml`)
Every Protocol is defined by a YAML manifest.

```yaml
id: software-development-v1
gates:
  - id: gate_path
    depends_on: gate_invariant
    responsible_role: planner
    permissions:
      read: [workspace]
      write: []
      exec: []
    mandatory_sections:
      - Implementation Steps
    verification_rule: "Total step coverage MUST account for 100% of defined Goals and Properties."
    output_artifacts:
      - plan.md
    
  - id: gate_synthesis
    depends_on: gate_path
    responsible_role: craft
    permissions:
      read: [workspace]
      write: plan.md:access_control # Dynamic ACL derived from artifact
      exec: plan.md:access_control
    output_artifacts:
      - walkthrough.md
```

### 4.2 Semantic Guards
Protocols define "Guards" that enforce domain-specific rigor:
- **Determinism** (Software): Code must compile and pass tests.
- **Reproducibility** (Science): Data must be immutable; analysis must be pre-registered.

---

## 5. Domain Implementations

### Case Study A: Software Development
*   **Challenge**: "Spaghetti Code" and Scope Creep.
*   **Solution**: The **Spec Gate** ensures architecture is approved before code is written. The **ACL** ensures the agent doesn't "fix" unrelated files.

### Case Study B: Empirical Science
*   **Challenge**: P-Hacking (changing hypotheses to fit data).
*   **Solution**: The **Pre-Registration Gate** locks the Hypothesis. The **Embedded ACL** grants write access to `results/` but specifically DENIES write access to `data/raw/`.

---

## 5. Architecture Showcase: The First Principles Machine

The `school-of-first-principles` project serves as the flagship implementation of the **Learning Domain (v2)**. It demonstrates how GAP enables high-utility autonomy without sacrificing safety.

### The Problem
Traditional "AI Tutors" suffer from:
1.  **Hallucination**: Inventing syntax or concepts.
2.  **Leakage**: Giving the solution immediately (ruining the learning struggle).
3.  **Drift**: Losing context of the curriculum over time.

### The GAP Solution
By implementing `learning-v2`, the School restricts the AI to a strict "Documentation Factory":

1.  **The Dispatcher (Triage)**: Identifies the gap (e.g., "Missing Signal Handler"). Read-Only access prevents it from breaking code.
2.  **The Navigator (Structure)**: Designs the `roadmap.md`. It cannot write content, only structure.
3.  **The Author (Content)**: Fills the `atom_template.md`.
    *   **Transfer Pattern Constraint**: The protocol forces the Author to provide a code example in a *different* context (Catching SIGINT instead of SIGUSR1). This creates a "Transfer Learning" environment for the human.

### The Result
We achieve a **Self-Expanding Curriculum**. The user can say "I want to learn Quantum Computing", and the Agent swarm autonomously generates a rigorous, First-Principles roadmap and coursework—without ever executing a single line of potentially dangerous code.

---

## 6. Conclusion

GAP is not just a prompting strategy; it is a **Protocol**. Just as TCP/IP governs the flow of packets, GAP governs the flow of agentic work. By embedding Security into the Specification, we enable a future where autonomous agents are not just powerful, but **Trustworthy**.

---
*Open Standard - v1.0*

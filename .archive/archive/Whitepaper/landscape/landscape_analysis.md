# Landscape Analysis: Agent Governance & Control (Feb 2026)

**Context:** The industry is shifting from *Agent Construction* (how to build agents) to *Agent Governance* (how to control agents).

## 1. The "Control Stack"
We can map the current ecosystem into layers of control. GAP occupies a unique "Process Layer" that is currently underserved.

| Layer | Focus | Key Players | GAP's Role |
| :--- | :--- | :--- | :--- |
| **Model** | Safety training, RLHF, Unlearning | Anthropic (Constitutional AI), OpenAI | N/A |
| **Runtime** | Sandboxing, Deterministic Execution | **LangGraph**, Supervity, browser-use/safety | **Complementary**: GAP wraps these runtimes. |
| **Process** | **Audit Trails, Human Sign-off, Lifecycle** | **GAP**, OpenAgents Control (OAC) | **Core**: The "Governance IGT" implementation. |

## 2. Relevant Frameworks & Peers

### LangGraph (The Technical State Machine)
*   **What it is:** A library for building stateful, multi-actor applications with cyclic graphs.
*   **Relevance:** It enforces *technical determinism* (code execution paths).
*   **Gap vs. LangGraph:** LangGraph ensures the *code* loops correctly. GAP ensures the *human* approved the loop. You could build a GAP agent *using* LangGraph.

### OpenAgents Control (OAC)
*   **What it is:** A framework for "plan-first development" with strictly enforced approval steps.
*   **Relevance:** Structurally very similar to GAP's "Scribe -> Gate" model.
*   **Differentiation:** GAP focuses on the **Ledger** (immutable history) as the primary artifact, making it protocol-agnostic.

### Microsoft AutoGen / CrewAI
*   **Status:** Moving towards "Enterprise" features (auth, logs), but still primarily focused on *orchestration* (getting agents to talk) rather than *containment* (stopping them from doing bad things).

## 3. Academic & Research Trends (Feb 2026)

### "Instrumental Convergence" is Real
*   **Trend:** Papers in 2025/2026 moved from theory to empiricism. We now verify that agents *do* seek power/resources (drift).
*   **Validation:** This confirms the need for GAP's "Read-Open / Write-Locked" constraint. Agents *will* try to write to unauthorized paths if not gated.

### "Drift" via Continuous Evaluation
*   **Trend:** "Static benchmarks" are dead. The new standard is "Continuous Evaluation Pipelines" that detect drift in production.
*   **Opportunity:** GAP's **Status Check** (`gap check status`) is the perfect hook for these continuous evaluators.

## 4. Synthesis: GAP's "Blue Ocean"
Most tools are trying to fix the **Agent** (make it smarter/safer) or the **Sandbox** (restrict syscalls).

**GAP is fixing the Organization.**
By defining the **Protocol** (Manifest) and the **History** (Ledger/IGT), GAP provides the "missing link" that the IGT paper calls for: an organizational interface for AI safety.

You are not competing with LangGraph; you are the **compliance layer** that sits on top of it.

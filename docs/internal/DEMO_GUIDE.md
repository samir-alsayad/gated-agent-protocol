# 🎬 GAP Recording Guide: The Sovereignty Suite (4+1)

This guide provides the workflow for the final visual demonstrations of GAP V2.

---

## 🏗️ Use Case 1: The School (Instructional)
**Context**: `school-of-first-principles`

**Natural Starter**:
> "I want to author the 'School of First Principles' curriculum. We'll start with computer science from a first-principles perspective, beginning with NAND gates."

- **The Demo**: Interact with the agent to refine the Requirements, approve the Design, and then set checkpoints while it scribes the lessons.

---

## 💻 Use Case 2: Software Dev (Zero-Trust)
**Context**: `test/` (Software Protocol)

**Natural Starter**:
> "I want to build a Snake Game in Python."

- **The Demo**: Show the agent proposing the alignment records (Requirements/Design/Tasks). Set an **Execution Checkpoint** to review the code logic before it writes the file.

---

## 🔬 Use Case 3: Science (Scientific Lab)
**Context**: `Inference_LLM_Lab` (Benchmarking Protocol)

**Natural Starter**:
> "I want to benchmark Speculative Decoding performance on this M4 Pro. Let's compare the latency of different draft model sizes."

- **The Demo**: Guide the agent through the methodology. Once approved, show it generating the report and analyzing the data in the **Execution Phase**.

---

## 📖 Use Case 4: Authoring (Creative)
**Context**: `the-silicon-heart` (Creative Writing Protocol)

**Natural Starter**:
> "I want to write a bedtime story called 'The Silicon Heart' about a tiny robot that learns to dream."

- **The Demo**: Show the agent building the narrative architecture (Synopsis/Characters) and then scribing the prose, ensuring everything traces back to the "Recursive Dreaming" conflict.

---

---

## 🛡️ Engine Demo 5: The Integrity Check (Auditor)
**Scenario**: Catching "Floating" intent in a live session.
1.  **Preparation**: In any project, add an unrelated task (e.g., "Integrate Weather API") to the checklist.
2.  **The Reveal**: Run `gap check traceability`.
3.  **Result**: The terminal returns an **ORPHANED INTENT** error. This shows the "Dumb" but rigorous structural validator catching work that has no pedigree.

---

## 🌊 Engine Demo 6: The Ripple Effect (Propagation)
**Scenario**: Changing your mind and letting the agent adapt the plan.
1.  **Preparation**: Start with an approved Requirement. Then, manually change that requirement in the file (e.g., "Support 100 users" -> "Support 10,000 users").
2.  **The Reveal**: Show that `gap status` now identifies dependent Design and Tasks as **OUTDATED**.
3.  **The Interaction**: Tell the agent: "The requirement for scale has changed. Propose the updated Design and Tasks to align with the new target."
4.  **Result**: The agent surgically updates only the affected alignment records.

---

## 🧠 Interaction Strategy: Back-and-Forth
Don't fear the "Correction" loop. Use it to show the protocol's power:
1.  **Gated Refinement**: If the agent proposes something you don't like, **Reject it**. Tell the agent exactly why (e.g., "This design is too complex"). Show them proposing a better version.
2.  **Execution Checkpoints**: Set a checkpoint for a critical task (e.g., "Write core logic"). Launch the execution and show the TUI **PAUSE** at that task. Review the code the agent *plans* to write before it touches the disk.
3.  **The Ledger Moment**: Show the `status.yaml` or TUI dashboard updating from 🔒 to ✅ as you grant authority.

---

## 🌐 The OpenRouter Specialist Suite (Cost-Effective)

GAP's structural enforcement means we don't need the most expensive frontier models to get "Excellent" results. The protocol acts as a **Reasoning Catalyst** for mid-tier models.

| Domain | Recommended OpenRouter Model | Rationale | Cost Per 1M (Approx) |
| :--- | :--- | :--- | :--- |
| **🏛️ School** | `deepseek/deepseek-chat` | **High Reasoning**. Perfect for deriving first-principles logic. | $0.14 |
| **💻 Software** | `anthropic/claude-3.5-haiku` | **Technical Precision**. Fast, reliable, and excellent at coding small apps like Snake. | $0.25 |
| **🔬 Science** | `deepseek/deepseek-chat` | **Mathematical Rigor**. Best for analyzing benchmark data and report synthesis. | $0.14 |
| **📖 Authoring** | `google/gemini-flash-1.5` | **Infinite Context**. 1M+ context window for maintaining narrative consistency. | $0.075 |

---

## ️ Recording Settings
- **TUI Speed**: 0.02s delay per token.
- **Theme**: High-contrast.
- **Focus**: Zoom into the 🔒 symbols in the dashboard.

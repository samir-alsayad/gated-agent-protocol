# Requirements: GAP Core System 

## 1. Intent & Scope
**Intent**: Implement a lightweight, human-gated protocol that focuses on high-fidelity alignment using Markdown and a transparent approval Ledger.
**Scope**: Core GAP engine including manifest parsing, gate enforcement via a ledger, and execution metadata (Plan) captured in Markdown.

## 2. Core Principles
1.  **Pure Human Authority**: Approval is based on human judgment of Markdown artifacts. The machine does not enforce regex traceability.
2.  **Markdown-Only Source of Truth**: All alignment (Idea, Reqs, Design, Tasks, Plan) exists purely in Markdown files within the `.gap/` directory.
3.  **High-Trust Gating**: State transitions are atomic and recorded in an immutable ledger, but the content audit is qualitative (human-verified).

## 3. Functional Requirements

### 3.1 Manifest & Lifecycle (Req-1)
- **3.1.1**: The system MUST parse YAML manifests defining the "Post-Auditor" lifecycle (idea, requirements, design, tasks, plan).
- **3.1.2**: All alignment artifacts MUST be stored in the project's `.gap/` directory.
- **3.1.3**: The system MUST support protocol inheritance and template-based artifact generation.

### 3.2 Human-Centric Alignment (Req-2)
- **3.2.1**: Alignment artifacts MUST use standard Markdown templates.
- **3.2.2**: The system MUST NOT require machine-readable YAML twins for tasks or plans.
- **3.2.3**: Traceability (Req -> Design -> Task) is a human-maintained convention, not a machine-enforced regex constraint.

### 3.3 Execution Policy (Req-3)
- **3.3.1**: The `plan.md` MUST capture supervisor-approved execution parameters:
    - **Inference Locality**: Explicit venue (Local, Cloud, M1/M4).
    - **Model Selection**: Specific authorized cognitive models per phase.
- **3.3.2**: The Plan MUST inherit its phase structure from the approved `tasks.md`.

### 3.4 Governance & Ledger (Req-4)
- **3.4.1**: The system MUST maintain a Ledger (`status.yaml`) that records atomic state transitions and human approvals.
- **3.4.2**: `gap gate approve` MUST move a proposal to "Live" and unlock the next phase based on manifest dependencies.

## 4. Non-Functional Requirements
- **No Machine Auditing**: Archiving the regex-based `auditor.py`.
- **Brutally Simple**: The CLI should focus on workflow state, not content parsing.
- **High Transparency**: The `.gap/` directory should be easily human-auditable.

## 5. Acceptance Criteria

### 5.1 Core Workflow (AC-1)
- Given a valid manifest, when user runs `gap check status`, then system displays current gate states.
- Given a proposed artifact in `.gap/proposals/`, when supervisor approves, then system moves it to `.gap/` and updates the ledger.
- Given a completed phase, when dependencies are met, then system unlocks the next phase.

### 5.2 Plan Construction (AC-2)
- Given approved tasks in `.gap/tasks.md`, when supervisor creates `.gap/plan.md`, then it includes specific locality and cognition assignments.
- Given a Plan, when implementation begins, then it serves as the definitive reference for the executor's authority.

## 6. Constraints
- **Qualitative Over Quantitative**: Alignment is judged by humans, not regexes.
- **Privacy by Locality**: Permission to use specific models/venues is the primary safety lever.
- **No Machine Sync**: The engine does not keep YAML and Markdown in sync; Markdown is the sole truth.
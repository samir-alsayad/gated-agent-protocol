# GAP Logic: The Engine

**Objective**: To define the behavioral rules of the Gated Agent Protocol.

## 1. The Core Principle: The Scribe Pattern
**"Logic in Chat. State in Files."**

*   **The Agent (Logic)**: Operates in the Chat Interface. It thinks, proposes, and reasons.
*   **The System (State)**: Operates on the File System. It writes, moves, and locks files.
*   **The Interface**: The Agent *never* writes files directly. It submits a **Proposal** to the System.

## 2. The Flow of Cognition (The Kiro Flow)
Every GAP Protocol must adhere to this 4-step sequence:

1.  **Intent (Requirements)**:
    *   *Input*: User Desire.
    *   *Output*: `intent.md` (What & Why).
    *   *Gate*: Approval of Scope.

2.  **Structure (Design)**:
    *   *Input*: Approved Intent.
    *   *Output*: `design.md` / `module.md` (The Blueprint).
    *   *Gate*: Approval of Plan.

3.  **Execution (Tasks)**:
    *   *Input*: Approved Design.
    *   *Output*: Content Artifacts (`codex.md`, `main.py`).
    *   *Gate*: Read-Only Frozen Specs.

4.  **Verification (Proof)**:
    *   *Input*: Execution Output.
    *   *Output*: `reflection.md` / Test Results.
    *   *Gate*: Final "Stamp" of Completion.

## 3. The Gate Logic
A "Gate" is a physical barrier in the System.

*   **State: Drafting**: The Agent can propose writes to `.gap/proposals/`.
*   **State: Review**: The User inspects the Proposal.
*   **Trigger: `/approve`**: The System moves the file from Proposal -> Live.
*   **State: Locked**: Once Live, the Agent cannot overwrite without a new Proposal.

## 4. Inheritance Logic
How Projects use Protocols.

*   **Composite**: A Project can use multiple Protocols simultaneously.
*   **State Isolation**: The "State Machine" of one module (e.g., `software`) does not block the other (e.g., `instructional`).
*   **Role Binding**: A Project binds specific Agents to specific Protocols (e.g., "The Librarian uses Instructional Protocol").

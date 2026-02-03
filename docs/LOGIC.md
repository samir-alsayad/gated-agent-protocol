# GAP Logic: The Engine

**Objective**: To define the behavioral rules of the Gated Agent Protocol.

## 1. The Core Philosophy: "Decision Records"

**Each GAP document is not just a description of work; it is a frozen Decision Record.**

> "All intentional creation depends on freezing decisions at increasing levels of specificity to preserve intent while enabling execution."

1.  **Bounded Decision Phases**: We do not "write docs"; we enter a phase to make decisions.
2.  **Explicit Encoding**: The decisions are encoded in standardized artifacts (`intent.md`, `design.md`, `plan.md`).
3.  **Progressive Reduction**: Each phase reduces the initially unbounded space of possibilities.
4.  **Authoritative Constraints**: Once approved, a Decision Record is **Law**. Downstream work may elaborate, but never contradict it.

This mechanism is domain-agnostic. Whether writing code or authoring a book, GAP enforces the **Freezing of Intent**.

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

3.  **Policy (Execution Rules)**:
    *   *Input*: Approved Design.
    *   *Output*: `policy.md` (Gating Strategy).
    *   *Gate*: Approval of Design.

4.  **Plan (Tasks)**:
    *   *Input*: Approved Design and Policy.
    *   *Output*: `tasks.md` (The Actions).
    *   *Gate*: Read-Only Frozen Specs.

## 3. The Gate Logic
A "Gate" is a physical barrier in the System.

*   **State: Drafting**: The Agent can propose writes to `.gap/proposals/`.
*   **State: Review**: The User inspects the Proposal.
*   **Trigger: `/approve`**: The System moves the file from Proposal -> Live.
*   **State: Locked**: Once Live, the Agent cannot overwrite without a new Proposal.

## 4. Protocol Composition and Isolation

How Projects use Protocols.

Projects may operate multiple GAP Protocols concurrently. Each Protocol maintains an independent decision state machine with isolated approvals, tasks, and execution policies. Protocols do not block or interfere with one another.
Projects bind agents to specific Protocols through role assignments, defining which agents may propose decisions, decompose tasks, or execute work within each Protocol’s authority boundaries.
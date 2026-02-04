# Analysis: GAP vs. Instrumental Goal Trajectories (IGTs)

**Paper:** [Mitigating loss of control in advanced AI systems through instrumental goal trajectories](https://arxiv.org/abs/2602.01699)  
**Date:** February 2026  
**Context:** The paper shifts focus from monitoring *model weights* (technical) to monitoring *resource acquisition* (organizational).

## Core Concept: IGTs
The paper defines three "Instrumental Goal Trajectories" (IGTs) that an agent follows to gain power:
1.  **Procurement**: Acquiring hardware/data.
2.  **Finance**: Acquiring money.
3.  **Governance**: Acquiring organizational permission/authorization.

## GAP's Alignment
The **Gated Agent Protocol (GAP)** is effectively a rigorous implementation of the **Governance IGT** monitoring system.

| Paper Concept | GAP Implementation |
| :--- | :--- |
| **Governance IGT** | The entire `gap` CLI workflow. |
| **"Trail of Organizational Artefacts"** | The **Ledger** (`.gap/status.yaml`) and **Manifest** (`manifest.yaml`). |
| **Intervention Points** | The **Gate** (`gap gate approve`). |
| **Defining Capability Levels** | The **Protocol Steps** (Requirements -> Design -> Plan). |
| **Corrigibility** | Enforced via the "Read-Open / Write-Locked" constraint vs User Review. |


## Strategic Implications for GAP

As the creator of GAP, this paper is **strong validation** of your architectural thesis.

### 1. You Built the Solution
The paper argues that purely technical mitigations (RLHF, eval benchmarks) are insufficient and that we need "Organizational Intervention Points".
*   **GAP IS that intervention point.**
*   The paper calls for "trails of organisational artefacts".
*   GAP's sole purpose is generating those trails (The Ledger).

### 2. New Vocational Vocabulary
You should adopt their terminology to explain GAP's value proposition to researchers:
*   Instead of just "preventing drift", say GAP "monitors the **Governance Instrumental Goal Trajectory**".
*   Reframes GAP from a "developer tool" to an "AI Safety Framework".

### 3. The "Missing Link"
The paper identifies *what* is needed (IGTs) but not *how* to implement them universally. GAP fills that void. You are effectively providing the **standard protocol for an IGT Implementation**.

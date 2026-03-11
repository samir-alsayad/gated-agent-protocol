# Tasks: GAP Core Simplification

## Phase 1: Core Protocol Infrastructure
- [x] **1.1: Simplified Manifest**
    - [x] Consolidate lifecycle to 5 key phases: `idea`, `requirements`, `design`, `tasks`, `plan`.
    - [x] Move default artifacts to the `.gap/` directory.
- [x] **1.2: Path & Template Resolution**
    - [x] Fix `PathManager` to correctly resolve Markdown templates from the protocol core.
    - [x] Streamline `scribe` to prioritize manifest-defined templates.
- [x] **1.3: Ledger Foundation**
    - [x] Implement atomic state transitions in `status.yaml`.
    - [x] Record human approvals with timestamps and approver IDs.

## Phase 2: Human-Gated Workflow
- [x] **2.1: The Scribe (Proposals)**
    - [x] Ensure `gap scribe create` isolation in `.gap/proposals/`.
    - [x] Validate dependencies before allowing proposal generation.
- [x] **2.2: The Gate (Approval)**
    - [x] Implement atomic file movement from Proposal to Live.
    - [x] Update Ledger status and unlock subsequent phases.
- [x] **2.3: The Cleanup**
    - [x] Archive automated `auditor.py` logic.
    - [x] Purge legacy YAML models and synchronization logic.

## Phase 3: Authority & Governance
- [x] **3.1: Execution Policy (Plan)**
    - [x] Define Markdown-based `plan.md` template.
    - [x] Capture Model Selection and Inference Locality as primary authority drivers.
- [x] **3.2: Reference Specifications**
    - [x] Refactor `.kiro` specs to reflect the "Post-Auditor" vision.
    - [x] Establish "Human-Verified Alignment" as the definitive standard.

## Success Criteria
- [x] Zero machine-readable friction (No Regex/YAML dependencies).
- [x] Immutable audit trail in the Ledger.
- [x] 100% Markdown-based alignment.
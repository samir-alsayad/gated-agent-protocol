# Requirements: GAP Engine (The Tool)

**Objective**: To provide a Sovereign CLI/Library that enforces GAP Protocols and enables Agents (like OpenCode) to interact with the file system safely.

## 1. The Sovereign Story
**As a** Developer / Project Creator,
**I want** to use GAP within OpenCode and other Chat UIs
**So that** I can enforce protocols comfortably from my preferred environment.

## 2. Functional Requirements

### A. The Validator (`gap check`)
*   **Input**: A path to a Project, Domain, or Unit.
*   **Output (Human)**: "Pass/Fail" with colored reasons.
*   **Output (Machine)**: JSON object detailing usage status.
    ```json
    { "status": "failed", "errors": ["Missing reflection.md"] }
    ```
*   **Safety**: Read-only operation.

### B. The Scribe (`gap scribe`)
*   **Input**: Protocol Name, Template Name, Data (Variables).
*   **Interface**: Must accept Data via **STDIN** (JSON) to allow extensive context from Agents without shell escaping issues.
*   **Output**: Writes a JSON Proposal to `.gap/proposals/`.
    *   *Constraint*: WILL NOT write to `live/` directories directly.

### C. The Gate (`gap gate`)
*   **Input**: Proposal ID.
*   **Action**: Atomic move from `proposals/` -> `live/`.
*   **Logging**: Appends to `LEDGER.md` (if configured in manifest).

### D. The State Machine (Workflow Enforcement)
The Engine must interpret the `manifest.yaml` `flow` list as a Dependency Graph.
*   **Dependencies**: A step cannot start until its `needs` (dependencies) are marked "Complete".
*   **Gate Types**:
    *   `manual`: The Engine stops and waits for User `/approve`.
    *   `auto`: The Engine proceeds immediately (e.g., triggering a Scribe agent).
*   **Transition Logic**:
    *   *IF* `needs` met *AND* Gate is `auto` -> Execute Action.
    *   *IF* `needs` met *AND* Gate is `manual` -> Set State to `Review`.

## 3. Interoperability Requirements (The API)
To support tools like OpenCode:
1.  **Structured Output**: All commands MUST support `--json` flag.
2.  **Exit Codes**: Standard POSIX exit codes (0 = Success, 1 = Error).
3.  **Library Access**: The code should be importable (`import gap`) so Python-native agents can use it without `subprocess`.

## 4. Constraint Checklist
*   [ ] **Zero Network**: The Engine must not call home.
*   [ ] **Manifest Truth**: Configuration is *only* read from `manifest.yaml` files.
*   [ ] **Stateless**: The Engine processes the current state of files; it implies no hidden DB.

# GAP Taxonomy: The Canon

**Version**: 2.0 (The Project-First Era)
**Objective**: To strictly define the entities within the Gated Agent Protocol.

## 1. The Hierarchy

### A. The Tool (`GAP`)
The framework itself. It provides the **Protocols** (Tools) and the **Enforcement Engine** (Gates).

### B. The Protocol (`protocols/*`)
A "Mode of Cognition". A composable **State Machine** that defines *how* work is done.
*   **Nature**: Abstract, Reusable, Composable.
*   **Examples**:
    *   `protocols/instructional`: The Teacher (Reqs -> Curriculum -> Lesson).
    *   `protocols/software`: The Builder (Specs -> Architecture -> Code).
    *   `protocols/research`: The Scientist (Question -> Hypothesis -> Experiment).

### C. The Project (`projects/*`)
A "Concrete Goal". An implementation that *uses* protocols to achieve an outcome.
*   **Nature**: Specific, Grounded, Sovereign.
*   **Examples**:
    *   `projects/school-of-first-principles`: Uses `instructional` to teach.
    *   `projects/my-novel`: Uses `creative-writing` to author.

### D. The Domain (`projects/*/domains/*`)
A logical subdivision within a massive Project.
*   **Nature**: Organizational (Folder-based).
*   **Role**: Isolates context (e.g., "Computing" vs "Life").
*   **Note**: Small projects do NOT need domains.

## 2. The Artifacts

### A. The Manifest (`manifest.yaml`)
The Configuration file found at the root of every Protocol and Project.
*   **Protocol Manifest**: Defines the Steps, Gates, and Templates.
*   **Project Manifest**: Defines the Composition (`extends: [instructional]`) and Role Limits.

### B. The Templates (`templates/*.md`)
The blueprints for State definition.
*   `intent.md`: Requirement capture.
*   `module.md`: Design Proposal.
*   `codex.md`: Immutable Content.
*   `reflection.md`: User State.

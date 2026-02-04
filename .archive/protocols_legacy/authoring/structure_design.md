# Structural Design: Authoring Domain

**Objective**: Organize `domains/authoring` by **Work Type** (Activity).

## Only Design - No Implementation
We are defining the folders (`Work Types`) that will exist in this domain.

---

## Reference: Science Domain
Structure:
*   `domains/science/benchmarking/` (Work Type: Performance Testing)
*   `domains/science/research/` (Work Type: Empirical Study)

Each folder contains its own `manifest.yaml` and `protocol.md`.

---

## Proposal: Learning Domain

## Proposal: Learning Domain Work Types (The Factory Floor)

## The Rhetorical Structure (The 7 Modes)

We organize the domain by **Intent** (The Mode of Writing), not by Product.

### Mode 1: `instructional` (The Guide)
*   **Goal**: Enable Action. "Get someone to do something correctly."
*   **Output**: Tutorials, Missions, SOPs.
*   **Gap Equivalent**: `education` (The "How").
*   **Manifest**: `instructional/manifest.yaml`

### Mode 2: `analytical` (The Critic)
*   **Goal**: Evaluate Systems. "Diagnose causes, assess quality."
*   **Output**: Gap Analysis, Architecture Review, Triage Reports.
*   **Gap Equivalent**: `diagnosis` (The "Why").
*   **Manifest**: `analytical/manifest.yaml`

### Mode 3: `informative` (The Teacher)
*   **Goal**: Transfer Knowledge. "Explain, define, clarify."
*   **Output**: Theory Sections, Concept Definitions, First Principles.
*   **Role**: Feeds into `instructional` artifacts.

### Mode 4: `descriptive` (The Architect)
*   **Goal**: Mental Modeling. "Create a vivid mental model."
*   **Output**: System Architecture Diagrams, State Machine descriptions.

---

## Directory Structure (Proposed)
```text
domains/authoring/
├── analytical/         # <--- WORK TYPE 1 (Diagnosis)
│   ├── manifest.yaml
│   └── protocol.md
│
├── instructional/      # <--- WORK TYPE 2 (Curriculum / Missions)
│   ├── manifest.yaml
│   └── templates/      # (Atom, Module - heavily instructional)
│
└── informative/        # <--- WORK TYPE 3 (Theory Library)
    └── protocol.md     # How to explain "First Principles"
```
tial (Knowledge).
    *   Action: `write: [instruction.md]`.

## Work Type 3: `knowledge_synthesis` (The Librarian) (Start of a thought...)
*   **Input**: An existing complex codebase (e.g., `linux/kernel/sched.c`).
*   **Action**: Reverse-engineer the concepts.
*   **Output**: `module_template.md` (filled with real-world examples).
*   **Analogy**: "Science Research" (Discovery) applied to Code.

## Directory Structure
```text
domains/learning/
├── diagnosis/          # GAP: "What is missing?"
├── education/          # GAP: "Here is the path."
└── synthesis/          # GAP: "Here is what this code teaches." (Future?)
```

## Directory Structure
```text
domains/learning/
├── README.md
│
├── pathfinding/        # <--- WORK TYPE 1
│   ├── manifest.yaml
│   └── protocol.md
│
└── content_creation/   # <--- WORK TYPE 2
    ├── manifest.yaml
    └── templates/      # (Atom, Module, Campaign)
```

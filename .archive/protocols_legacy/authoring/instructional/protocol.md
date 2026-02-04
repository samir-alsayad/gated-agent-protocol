# Design Spec: Learning Domain v2 (Curriculum Generator)

**Goal**: To autonomously generate rigorous Learning Documentation (Roadmaps, Atoms, Modules).
**Scope**: **Docs Creation Only**. No execution, no tutoring loop.

## 1. The Roles
Focus is purely on *Information Architecture*.

| Role | Name | Capability | Focus |
|:---|:---|:---|:---|
| `dispatcher` | **The Diagnostician** | Problem Analysis | "Identifying the missing concept." |
| `navigator` | **The Architect** | Structural Design | "Building the full Syllabus (Roadmap)." |
| `author` | **The Scribe** | Content Generation | "Writing the Atom/Module definitions." |

---

## 2. The State Machine (Gates)
A "Factory" for curriculum.

### Gate I: Diagnosis (`gate_triage`)
*   **Actor**: `dispatcher`
*   **Input**: "I want to learn X" OR "I have error Y".
*   **Output**: `recommendation.md` (Target Topic).
*   **Verification**: Must link to a valid concept in the Taxonomy.

### Gate II: Syllabus (`gate_structure`)
*   **Actor**: `navigator`
*   **Input**: Target Topic.
*   **Output**: `curriculum/roadmap.md` (The Skeleton).
*   **Verification**: User Approval of the path.

### Gate III: Content (`gate_definition`)
*   **Actor**: `author`
*   **Input**: `roadmap.md` + Templates.
*   **Output**: `curriculum/campaigns/.../atom_template.md` (FILLED).
*   **Action**: Generates the "Theory", "Pattern", and "Mission" text.
*   **Restriction**: Does NOT create the `workbench` files. Just the docs.

---

## 3. Artifact Definition
*   `manifest.yaml`: Defines this 3-step generation pipeline.

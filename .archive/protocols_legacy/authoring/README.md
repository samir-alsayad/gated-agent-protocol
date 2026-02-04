# Domain: Authoring (Content Generation)

**The Factory of Thought.**
This domain governs the autonomous creation of high-fidelity documentation and educational material.

## 🎯 Mission
To generate rigorous, structural, and pedagogical content without hallucination or drift.

## 🛠️ Work Types

### 1. [Instructional](instructional/) (The Guide)
Goal: Enable Action. "Get someone to do something correctly."
- **Protocol**: [Instructional-Flow](instructional/protocol.md)
- **Gates**: `roadmap.md` → `tutorial.md`
- **Focus**: Curriculum, Missions, SOPs.

### 2. [Analytical](analytical/) (The Critic)
Goal: Evaluate Systems. "Diagnose causes, assess quality."
- **Protocol**: [Analytical-Flow](analytical/manifest.yaml)
- **Gates**: `triage_report.md`
- **Focus**: Code Review, Gap Analysis.

## Usage
This domain generates **Documentation**. It does not execute code.
The User is responsible for the `workbench` execution.

## Implementation
This repository (`school-of-first-principles`) is the Reference Implementation of this domain.

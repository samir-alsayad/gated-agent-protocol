# Gated Agent Protocol (GAP)

**The Sovereign Standard for Agent Containment.**

[![PyPI](https://img.shields.io/pypi/v/gated-agent-protocol)](https://pypi.org/project/gated-agent-protocol/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

GAP is a **Deterministic State Machine** that wraps **Probabilistic AI Agents**. It enforces a strict "Read-Open / Write-Locked" workflow to prevent agent drift.

## 🚀 Installation

```bash
pip install gated-agent-protocol
```

## ⚡ Usage

GAP operates on **Projects** defined by a **Manifest** (`manifest.yaml`).

### 1. Check Status
See the health of your project and which steps are locked/unlocked.

```bash
gap check status manifest.yaml
```

**Output:**
```text
🟢 requirements: unlocked
🔒 design: locked
🔒 plan: locked
```

### 2. Scribe (Create)
Generate a proposal for a step using the defined Protocol Template.

```bash
# Scribe the 'requirements' step
gap scribe create requirements
```

*   **Gate Check**: If the step is `gate: manual`, this writes to `.gap/proposals/`.
*   **Gate Check**: If the step is `gate: auto`, this writes directly to the live artifact.

### 3. Gate (Approve)
Review pending proposals and sign them into the Ledger.

```bash
# List pending proposals
gap gate list

# Approve and Merge to Live
gap gate approve requirements
```

## 🏗️ Architecture

### The Trinity
1.  **Manifest (`manifest.yaml`)**: The Source of Truth. Defines the dependency graph.
2.  **State Engine (`.gap/status.yaml`)**: The Ledger. Tracks approved state transitions.
3.  **Protocol Library**: Reusable workflows (`software-engineering`, `instructional`, `research`).

### Inheritance
Projects can **Extend** existing protocols.
*   *School of Physics* (Project) `extends` *Instructional Protocol*.
*   GAP automatically resolves templates from the parent protocol if not found locally.

## 🤝 Contributing

We welcome protocols! Submit your domain-specific workflows (Science, Law, Finance) via PR.
See [CONTRIBUTING.md](CONTRIBUTING.md).

---
*Built with <3 by the Sovereign AI Community.*
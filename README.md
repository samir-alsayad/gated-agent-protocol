# Gated Agent Protocol (GAP)

**The Sovereign Standard for Human-AI Collaboration.**

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

GAP is a **Protocol Engine** that enforces **Structure**, **Security**, and **Traceability** in agentic workflows. It prevents AI from hallucinating requirements or skipping safety checks by strictly enforcing a "State Machine of Work".

---

## 🚀 Quick Start

### Install from GitHub

```bash
pip install git+https://github.com/samir-alsayad/gated-agent-protocol.git
gap --help
```

### Initialize a Project

```bash
# Create a new GAP project using the software-engineering protocol
gap init --protocol software-engineering
```

### Check Status

```bash
gap check status manifest.yaml
```

**Output:**
```text
🟢 requirements: UNLOCKED (ready to scribe)
🔒 design: LOCKED (waiting for: requirements)
🔒 plan: LOCKED (waiting for: design)
```

### Create & Approve Artifacts

```bash
# 1. Generate a proposal
gap scribe create requirements

# 2. Review pending proposals
gap gate list

# 3. Approve and commit to the ledger
gap gate approve requirements
```

---

## 🏗️ Core Concepts

### The State Machine of Work

GAP enforces a strict **Chain of Custody** for every action an Agent takes:

1. **Requirements** → Define *what* is needed (EARS syntax).
2. **Design** → Define *how* to solve it (Correctness Properties).
3. **Policy** → Declare execution boundaries (Law vs Exception).
4. **Tasks** → Break design into atomic units (Traceable Checklists).
5. **Execution** → Do the work, locked to approved ACLs.

### The Traceability Trinity

Every artifact links back to its source:

- **Task** → links to → **Policy** → links to → **Design** → links to → **Requirements**
  
If an Agent tries to act without this "Golden Thread", the Harness blocks it.

### Boolean Gates

Every phase has a **Gate** (`gate: true` or `gate: false`):
- `true` = Requires human approval before proceeding.
- `false` = Autonomous execution allowed.

### Checkpoints

During execution, the Harness can pause at designated points:
- `explicit` = Pause only at listed task IDs.
- `every` = Pause after every task.
- `batch` = Run all, review at end.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Whitepaper](docs/WHITE_PAPER.md) | The full theory and architecture |
| [Protocol Schema](docs/SCHEMA_PROTOCOL.md) | How to define protocols |
| [Project Schema](docs/SCHEMA_PROJECT.md) | How to configure projects |
| [CLI Reference](docs/cli.md) | All commands |
| [Integration Guide](docs/integration_guide.md) | Adding GAP to your tools |

---

## 🔧 Project Structure

```
.gap/
├── manifest.yaml      # The Law (project configuration)
├── status.yaml        # The Ledger (state machine)
├── proposals/         # Pending artifacts awaiting approval
└── acls/              # Extracted Access Control Lists
```

---

## 🤝 Contributing

We welcome contributions! Please reach out.

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

*Open Standard - v1.0 - 2026*
*Created by Samir Alsayad.*

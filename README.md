# Gated Agent Protocol (GAP)

**Agents propose. Supervisors approve. The Ledger remembers.**

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

GAP is a **Protocol Engine** that enforces **Structure**, **Security**, and **Traceability** in agentic workflows. It prevents agents from deviating from requirements by strictly enforcing a "Workflow Compliance Layer".

---

## 📋 Requirements

- Python 3.10+
- macOS, Linux, or Windows
- No external services required (Standard YAML/File-based Ledger)

---

## 🚀 Quick Start

### Install

```bash
# Stable release
pip install git+https://github.com/samir-alsayad/gated-agent-protocol.git@v1.0.0

# Or latest main branch
pip install git+https://github.com/samir-alsayad/gated-agent-protocol.git
```

### Verify Installation

```bash
gap --help
```

### Example Workflow

Create a `manifest.yaml`:

```yaml
kind: project
name: my-project
version: 1.0.0
description: "My first GAP project"

extends:
  - protocol: software-engineering

flow:
  - step: requirements
    artifact: docs/requirements.md
    gate: true  # Requires approval
    
  - step: design
    artifact: docs/design.md
    gate: true
    needs: [requirements]
    
  - step: implementation
    artifact: src/
    gate: false  # Autonomous
    needs: [design]
```

Then run:

```bash
# Check current state
gap check status manifest.yaml

# Create a proposal for requirements
gap scribe create requirements --manifest manifest.yaml

# Review and approve
gap gate list --manifest manifest.yaml
gap gate approve requirements --manifest manifest.yaml
```

**Output:**
```text
🟢 requirements: UNLOCKED
🔒 design: LOCKED (waiting for: requirements)
🔒 implementation: LOCKED (waiting for: design)
```

---

## 🏗️ Core Concepts

### Boolean Gates

Every phase has a **Gate** (`gate: true` or `gate: false`):
- `true` = Requires supervisor approval before proceeding
- `false` = Autonomous execution allowed

### Workflow Compliance

GAP enforces a strict **Chain of Custody**:

```
Requirements → Design → Policy → Tasks → Execution
     ↓            ↓         ↓        ↓         ↓
   (gate)      (gate)    (gate)   (gate)    (ACL)
```

If an Agent tries to skip a compliance phase, GAP blocks it.

### Checkpoints

During execution, the Harness can pause at designated points:
- `explicit` = Pause only at listed task IDs
- `every` = Pause after every task
- `batch` = Run all, review at the end

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

## 🔧 Development

```bash
# Clone the repo
git clone https://github.com/samir-alsayad/gated-agent-protocol.git
cd gated-agent-protocol

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v
```

---

## 🔒 Security

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities.

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

*Open Standard - v1.0.0 - 2026*
*Created by Samir Alsayad.*

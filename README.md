# Gated Agent Protocol (GAP)

**Agents propose. Supervisors approve. The Ledger remembers.**

[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

GAP is a **Protocol Engine** that enforces **Structure**, **Security**, and **Traceability** in agentic workflows. It prevents agents from deviating from requirements by strictly enforcing a "Workflow Compliance Layer".

---

## Alignment Phase and Execution Phase 

GAP splits the lifecycle of an agent's work into two distinct, **gated** classes. This ensures that the supervisor remains the final authority at every critical junction.

### 1. The Alignment Phase (Blueprint Logic)
Before a single line of code is written, the supervisor must approve a configurable set of artifacts the agent shall propose.
*   **Artifacts**: 
We use `requirements.md`, `design.md`, `tasks.md` for most types of work and domain, but these can be extended or omitted at will.
*   **The Gate**: **Mandatory Supervisor Approval**. The protocol prevents the agent from entering the Execution phase until the Supervisor has audited and signed off on the blueprint.
*   **Result**: A deterministic Contract that the agent is bound to follow during Execution.

### 2. The Execution/Implementation Phase (Throughput Logic)
Once the alignment is locked, the agent moves to implementation/execution:
*   **Artifacts**: Source code, reports, data, writing.
*   **Execution/Implementation**: Running tests, making tool calls, running benchmarks, etc.
*   **The Gate**: **Deterministic Checkpoints**. Based on the approved policy (`explicit`, `every`, or `batch`), the harness automatically pauses the agent for review.
*   **Result**: High-speed execution without loss of control.

### ⛓️ Workflow Compliance
GAP enforces a strict **Chain of Custody** from intent to implementation:

```
[ ALIGNMENT PHASE ]                 [ EXECUTION PHASE ]
Requirements → Design → Tasks  ==>  Implementation / Execution
      ↓          ↓       ↓                  ↓
   (gate)     (gate)   (gate)           (checkpoints)
```

---


## 🏗️ Core Philosophy

### Interaction Classification (Separation of Concerns)

GAP enforces a critical distinction between what the **Protocol** controls and what the **Agent** generates:

| Interaction Type | Owner | Mechanism | Examples |
|------------------|-------|-----------|----------|
| **Programmatic** | Protocol | **Deterministic Form** | Domain selection, policy forms, gate approvals |
| **Generative**   | Agent    | **Probabilistic Stream** | Requirements, design, tasks, code |

**The Philosophy of Determinism:**
We believe that **Authority must be Deterministic**. 
- An agent should not "hallucinate" its own security policy.
- A gate should not be "suggested" by an LLM.
- Critical boundaries (ACLs, Tool Permissions) are defined via rigid, unchangeable forms that the agent cannot influence.

This ensures that while the **work** is creative (AI), the **boundaries** are absolute (Code).


```
┌─────────────────────────────────────────────────────────────┐
│                     GAP (Protocol Layer)                    │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   PROGRAMMATIC      │    │        GENERATIVE           │ │
│  │   (GAP Controls)    │    │      (Agent Proposes)       │ │
│  │                     │    │                             │ │
│  │  • Domain Selection │    │  • Requirements Content     │ │
│  │  • Policy Forms     │    │  • Design Documents         │ │  
│  │  • Gate Approvals   │    │  • Task Definitions         │ │
│  │  • Checkpoints      │    │  • Code Implementation      │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
│              ↓                          ↓                   │
│         [Deterministic]            [Can be Gated]           │
└─────────────────────────────────────────────────────────────┘
```





## 🌍 4 Example Domains

GAP is domain-agnostic. It enforces the same integrity whether you are building a CPU or writing a poem.

| Domain | Protocol | Goal |
| :--- | :--- | :--- |
| **🏗️ School** | `instructional` | Scribing first-principles curricula. |
| **💻 Software** | `software-dev` | High-integrity, ACL-gated coding. |
| **🔬 Science** | `benchmarking` | Verifiable experimental methodology. |
| **📖 Authoring** | `creative-writing` | Traceable narrative architecture. |


---

## 🛡️ Core Engine Features

### 1. The Traceability Auditor
Run `gap check traceability` to verify the **Trinity of Intent**. The engine automatically detects "Orphaned Intent"—any task or design decision that cannot prove its pedigree back to a validated requirement.

### 2. Path-Locked Security (ACL)
Agents are confined to whitelisted directories defined in the approved `tasks.md`. No "leaking" into system files or unauthorized project areas.

### 3. Verification State Machine
A rigid graph of checkpoints (LOCKED -> PENDING -> APPROVED). Authority is never assumed; it is granted via explicit user gates.

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

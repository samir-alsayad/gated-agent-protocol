# GAP Specification v1.0

This standard defines the mandatory requirements for any **Protocol** in the GAP (Gated Agent Protocol) framework. A Protocol is a **Gated State Machine** that governs agentic work through human-approved checkpoints.

## 1. Core Philosophy: The Containment Layer

The mission of GAP is to provide a **deterministic chassis** for probabilistic AI models. It ensures that agentic work progresses only when its quality, intent, and **security scope** have been verified. Unlike rigid workflows, GAP supports **variable gate counts** tailored to the domain:

| Gate Class | Count | Use Case | Standard Phases |
|:-----------|:-----:|:---------|:----------------|
| **Velocity-First** | 2 | Maintenance, Patching | Understand → Synthesis |
| **Synthesis-Standard** | 3 | New Development, Research | Understand → Path → Synthesis |
| **Rigor-Maximum** | 4+ | Benchmarking, Governance | Understand → Design → Path → Synthesis |

## 2. Universal Protocol Phases

GAP enforces a universal phase structure across all domains. Each phase MUST be represented by at least one gate, and each gate MUST have a single responsible role.

| Phase | Decision Record Type | Purpose | Typical Output |
| :--- | :--- | :--- | :--- |
| **Understand** | **Requirements** | Capture user intent and constraints | `intent.md` |
| **Design** | **Design** | Define architectural/formal invariants | `spec.md` / `invariants.md` |
| **Path** | **Tasks** (Plan) | Decompose work into actionable steps | `plan.md` / `tasks.md` |
| **Synthesis** | **Execution** | Execute work and provide proof | Code / Report + `walkthrough.md` |

## 3. Mandatory Structural Components

Every protocol SHALL define the following:

### 3.1 The Linguistics (Grammar)
- Protocols must specify a non-ambiguous syntax for expressing intent (e.g., EARS for requirements, Statistical Hypotheses for science).
- Each domain defines its own ID prefixes (e.g., `REQ-`, `HYP-`, `OBJ-`).

### 3.2 The Pillar of Rigor
Every protocol must identify the specific quality it defends:
- **Software Development**: Determinism
- **Software Maintenance**: Reliability
- **Science Research**: Reproducibility
- **Science Benchmarking**: Statistical Rigor

### 3.3 Traceability
Every atomic action taken by an agent MUST be traceable to a ratified intent or invariant via a **Traceability Footer**.

## 4. The Operational Manifest (`manifest.yaml`)

Every protocol MUST include a machine-readable manifest that defines its state machine.

### Schema (v1.0)

```yaml
id: [protocol-id]          # Unique slug (e.g., software-development-v1)
version: [semver]           # Semantic version string

meta:
  guards:                   # Qualities this protocol guards (first = primary)
    - [Primary Guard]
    - [Secondary Guard]
  philosophy: [Approach]    # Abstract methodology
  prefixes:                 # Domain-specific ID prefixes
    intent: "REQ-"
    invariant: "PROP-"
    action: "STEP-"

roles:                      # Abstract capabilities (mapped by harness)
  - id: [role-id]
    capability: [Description]
    focus: [List of specializations]

gates:                      # The sequence of human-approved checkpoints
  - id: [gate-id]           # e.g., gate_intent, gate_path
    depends_on: [Optional: previous gate ID]
    responsible_role: [role-id] # Singular role per gate
    permissions:
      read: [workspace | file-list]      # Files agent can read
      write: [file-list]                 # Files agent can write (usually empty for non-synthesis gates)
      exec: [command-list | shell]       # Commands agent can run
    mandatory_sections:                  # Required Markdown headers in output
      - [Header Name]:
          [metadata-key]: [metadata-value]
    verification_rule: [Binary pass/fail statement]
    output_artifacts:                    # Files produced by this gate for review
      - [filename.md]
```

### Key Design Principles
- **Variable Gate Count**: The `gates` array can contain 2, 3, 4, or more gates.
- **Dependency Chain**: Gates declare `depends_on` to enforce ordering.
- **Role Abstraction**: Roles describe capabilities, not specific models.

## 5. The Protocol Document (`protocol.md`)

The human-readable companion to the manifest. It MUST explain:
- The **Mission** of the protocol.
- The **Semantic Pillars** (Intent, Invariant, Action).
- The **Operational Gates** in natural language.

## 6. Discovery and Resolution

Protocols are resolved via a **Global Registry** system.

### Resolution Priority
To prevent **Circular Privilege Escalation**, Agent harnesses SHALL resolve protocols **strictly** from the Trusted Registry.

1. **Global Registry**: Via `GAP_PATH` environment variable or the `gap` CLI.
2. **Local Override**: **FORBIDDEN**. Local manifest files are ignored for security definitions.

### The `gap` CLI
```bash
gap init [protocol]       # Initialize .gap/ structure (default: software-development-v1)
gap list                  # Discover all ratified protocols
gap get [id]              # Output the manifest as YAML or JSON
gap validate [id]         # Check manifest against GAP schema
gap path [id]             # Locate the domain directory
```

## 7. Project Configuration (`.gap/gap.yaml`)

A project signals its participation in GAP by including a `gap.yaml` file inside the `.gap` directory. This file serves as the **Session Registry**.

### 6.1 Schema
```yaml
active_session: [session-id]

sessions:
  - id: [session-id]
    name: [Human readable goal]
    protocol: [protocol-id]  # e.g., software-maintenance-v1
    status: [active | completed | archived]
    path: .gap/sessions/[session-id]
```

## 8. Session State Storage

To support multiple working sessions (and keep the root clean), GAP enforces **Session-Based State** inside the hidden directory.

- **Root**: Clean. No GAP files visible.
- **Config**: `.gap/gap.yaml` stores the registry.
- **State**: All Pillar Artifacts (`plan.md`) MUST be stored within `.gap/sessions/[session-id]/`.
- **ACL Scope**: The embedded ACL in `.gap/sessions/[id]/plan.md` applies ONLY when that session is active.

```yaml
# .gap/manifest.yaml (Project-Local)
extends: software-development-v1
config:
  logic:
    mandatory_sections:
      - Introduction
      - User Stories  # Allowed: Adding non-security requirements
```

Tools supporting GAP would:
1. Detect `.gap/gap.yaml`.
2. Read `active_session` to determine the current context path (e.g., `.gap/sessions/fix-01`).
3. Resolve the protocol from the registry.
3. Load project-specific configuration (ignoring any `permissions` blocks).
4. Enforce gates during agent operation.

---
*GAP Specification v1.0 - 2026*

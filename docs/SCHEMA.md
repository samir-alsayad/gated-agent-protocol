# GAP Schema: The Manifest

**Objective**: To define the `manifest.yaml` structure for Protocols and Projects.

## 1. The Protocol Manifest
Located at: `protocols/[name]/manifest.yaml`

```yaml
kind: protocol
name: instructional
version: 1.0.0

# The DNA: Steps of the State Machine
flow:
  - step: requirements
    artifact: templates/intent.md
    gate: approval
  - step: design
    artifact: templates/module.md
    gate: approval
  - step: task
    artifact: templates/codex.md
    gate: manual_review

# The Tools: Templates this Protocol provides
templates:
  intent: templates/intent.md
  design: templates/module.md
  content: templates/codex.md
  proof: templates/reflection.md
```

## 2. The Project Manifest
Located at: `projects/[name]/manifest.yaml`

```yaml
kind: project
name: school-of-first-principles
version: 0.1.0

# Composition: Which Protocols are active?
extends:
  - protocol: instructional
    role: librarian
    scope: /  # Global scope
  - protocol: software
    role: smith
    scope: /domains/computing/projects  # Scoped access

# Sub-Contexts (Domains)
domains:
  - name: computing
    path: domains/computing
  - name: life
    path: domains/life
```

## 3. The Gate Object
Defines how a Proposal is handled.

```json
{
  "id": "prop_123",
  "agent": "librarian",
  "target": "domains/computing/modules/04_local/codex.md",
  "template": "codex",
  "data": { ...json_content... }
}
```

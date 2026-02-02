# GAP Python SDK

This directory contains the reference implementation of the GAP Standard (`src/gated_agent`).

## Purpose
This package provides the **Schema Validation** and **Registry Resolution** logic. It is the **Containment Kernel** imported by **Tool Harnesses** (e.g., IDEs, CI pipelines) to enforce the GAP Standard upon an Agent.

It allows the Harness to:
1.  **Discover** available protocols (`registry.py`).
2.  **Validate** that a protocol matches the schema (`cli.py`).
3.  **Enforce** ACLs and Gate Rules (`security.py`).

## Usage
Tool Harnesses import this library to restrict the Agent:

```python
from gated_agent.registry import Registry
from gated_agent.security import ACLEnforcer

# 1. Harness loads the protocol
manifest = Registry().get_manifest("software-development-v1")

# 2. Harness enforces gates
for gate in manifest.gates:
    if not user_approved(gate.id):
        block_agent()
```

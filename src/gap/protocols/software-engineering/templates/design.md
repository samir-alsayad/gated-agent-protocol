# Structural Design: {{ project_name }}

## 1. Architecture Overview
High-level system design and component relationships.

```mermaid
graph TD
    A[{{ component_a }}] --> B[{{ component_b }}]
    B --> C[{{ component_c }}]
```

## 2. Correctness Properties
Define verifiable properties that must always hold. Each property validates one or more goals/requirements.

*   **P-01**: {{ property_1 }} — *Validates: G-01*
*   **P-02**: {{ property_2 }} — *Validates: G-02*

## 3. Data Models (Entities & Relationships)
Define the core state. Use Pydantic or similar for schema clarity.

```python
class {{ entity_name }}:
    """{{ entity_description }}"""
    id: UUID
    {{ field_1 }}: {{ type_1 }}
```

## 4. Interface Contracts
Public APIs, CLI schemas, or internal module boundaries.

### {{ interface_name }}
- **Type**: {{ interface_type }} (e.g., REST, CLI, Python API)
- **Signature**: `{{ signature }}`
- **Input**: {{ input_spec }}
- **Output**: {{ output_spec }}
- **Error States**: {{ error_spec }}

## 5. Dependencies & Infrastructure
*   **Libraries**: {{ libraries }}
*   **Services**: {{ services }}

---
**Verification Rule:** Every property MUST validate at least one Goal ID from intent.md.

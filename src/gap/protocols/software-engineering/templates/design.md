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
*   **P-02**: {{ property_2 }} — *Validates: G-02, C-01*
*   **P-03**: {{ property_3 }} — *Validates: G-03*

## 3. Data Models
Key data structures and their relationships.

```python
# Example structure
class {{ model_name }}:
    {{ field_1 }}: {{ type_1 }}
    {{ field_2 }}: {{ type_2 }}
```

## 4. Interface Contracts
Public APIs and their contracts.

### {{ interface_name }}
- **Input**: {{ input_spec }}
- **Output**: {{ output_spec }}
- **Invariants**: {{ invariant_spec }}

## 5. Dependencies
External libraries, services, or systems required.

*   {{ dependency_1 }}
*   {{ dependency_2 }}

---
**Verification Rule:** Every property MUST validate at least one Goal ID from intent.md.

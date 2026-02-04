# Structural Design: {{ project_name }}

## 1. Course Architecture
The overarching structure of the learning experience.

```mermaid
graph TD
    A[{{ unit_1 }}] --> B[{{ unit_2 }}]
    B --> C[{{ unit_3 }}]
```

## 2. Correctness Properties
Define verifiable properties that the curriculum must satisfy.

*   **P-01**: {{ property_1 }} — *Validates: R-01*
*   **P-02**: {{ property_2 }} — *Validates: R-02*
*   **P-03**: {{ property_3 }} — *Validates: R-03*

## 3. Unit Sequence
1.  **{{ unit_title_1 }}**: {{ unit_desc_1 }}
2.  **{{ unit_title_2 }}**: {{ unit_desc_2 }}

---
**Verification Rule**: Every property MUST validate at least one Requirement ID from intent.md.

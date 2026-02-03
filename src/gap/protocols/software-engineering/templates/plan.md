# Implementation Plan: {{ project_name }}

## 1. Plan Overview
{{ summary }}

## 2. Implementation Steps
Each step must trace back to Goals (G-), Constraints (C-), or Properties (P-) from previous artifacts.

- [ ] **STEP-01**: {{ step_1_description }} — *Trace: G-01*
- [ ] **STEP-02**: {{ step_2_description }} — *Trace: G-02, P-01*
- [ ] **STEP-03**: {{ step_3_description }} — *Trace: C-01, P-02*
- [ ] **STEP-04**: {{ step_4_description }} — *Trace: P-03*
- [ ] **STEP-05**: Write tests for core logic — *Trace: P-01, P-02, P-03*
- [ ] **STEP-06**: Integration testing — *Trace: G-01, G-02*

## 3. Access Control
Define which files can be modified and which commands can be executed during implementation.

```yaml
allow_write:
  - "src/**/*.py"
  - "tests/**/*.py"
  - "docs/*.md"
  - "README.md"

allow_exec:
  - "pytest tests/"
  - "python -m mypy src/"
  - "python -m black src/ tests/"
```

---
**Verification Rule:** Total step coverage MUST account for 100% of defined Goals and Properties.  
**Security Note:** The Access Control block above will be enforced during the implementation gate.

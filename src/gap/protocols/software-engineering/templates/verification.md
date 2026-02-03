# Walkthrough: {{ project_name }}

## 1. Changes Made
Document all files created or modified with brief rationale.

### Files Created
- `{{ file_1 }}` - {{ rationale_1 }}
- `{{ file_2 }}` - {{ rationale_2 }}

### Files Modified
- `{{ file_3 }}` - {{ rationale_3 }}

## 2. What Was Tested
Verification steps performed to validate the implementation.

### Unit Tests
```bash
{{ test_command }}
```

**Results:**
```
{{ test_output }}
```

### Integration Tests
- [ ] {{ integration_test_1 }}
- [ ] {{ integration_test_2 }}

### Manual Verification
- [ ] {{ manual_check_1 }}
- [ ] {{ manual_check_2 }}

## 3. Validation Results
Proof that all properties and constraints are satisfied.

### Property Validation
- **P-01**: {{ validation_result_1 }} ✅
- **P-02**: {{ validation_result_2 }} ✅
- **P-03**: {{ validation_result_3 }} ✅

### Constraint Validation
- **C-01**: {{ constraint_check_1 }} ✅
- **C-02**: {{ constraint_check_2 }} ✅

## 4. Evidence
Screenshots, logs, or other proof of correctness.

```
{{ evidence_output }}
```

## 5. Conclusion
**Status:** {{ ready_status }}

All gated artifacts have been satisfied:
- ✅ Intent (Goals: G-01, G-02, G-03)
- ✅ Specification (Properties: P-01, P-02, P-03)
- ✅ Plan (All steps completed with traceability)

---
**Verification Rule:** Implementation MUST satisfy all gated artifacts and approved ACL constraints.

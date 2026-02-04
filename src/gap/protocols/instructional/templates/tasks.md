# Operational Tasks: {{ project_name }}

## 1. Access Control (ACL)
```yaml
allow_write:
  - "docs/content/**"
allow_exec:
  - "node tools/validate_lesson.js"
```

## 2. Task Checklist
- [ ] **Task 1: {{ task_title_1 }}**
  - **Description**: {{ task_desc_1 }}
  - **Traces to**: {{ property_id_1 }}
  
- [ ] **Task 2: {{ task_title_2 }}**
  - **Description**: {{ task_desc_2 }}
  - **Traces to**: {{ property_id_2 }}

---
**Verification Rule**: No task may exist without a trace to a Property (Design) or Requirement (Intent).

# Authoring Tasks: {{ project_name }}

## 1. Access Control (ACL)
```yaml
# Whitelist for Curriculum Scribing
allow_write:
  - "domains/{{ domain_name }}/**/*.md"
  - "domains/{{ domain_name }}/**/*.py"
```

## 2. Scribe Checklist
Break the design into atomic "Scribing" tasks for the agent.

- [ ] **Task 1: Scribe Unit 1.1 ({{ unit_1_1_title }})**
  - **Artifacts**: `codex.md`, `assignment.py`
  - **Traces to**: P-01

- [ ] **Task 2: Scribe Unit 1.2 ({{ unit_1_2_title }})**
  - **Artifacts**: `codex.md`, `reflection.md`
  - **Traces to**: P-01, R-02

---
**Verification Rule**: No scribing task may exist without a trace to a Syllabus item (Design) or Learning Goal (Intent).

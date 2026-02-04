# Plan: CLI File Organizer

## Implementation Steps

- [ ] **STEP-01**: Create project structure and `main.py` entry point. — *Trace: G-01*
- [ ] **STEP-02**: Implement `config.py` to load YAML rules. — *Trace: G-02, P-04*
- [ ] **STEP-03**: Implement `organizer.py` with file categorization logic. — *Trace: G-01, C-01*
- [ ] **STEP-04**: Add collision handling (timestamp suffix). — *Trace: C-02, P-01*
- [ ] **STEP-05**: Implement `--dry-run` flag. — *Trace: C-03*
- [ ] **STEP-06**: Implement `logger.py` for file movement logs. — *Trace: C-04*
- [ ] **STEP-07**: Add boundary checks to prevent operations outside target directory. — *Trace: P-02*
- [ ] **STEP-08**: Write unit tests for core logic. — *Trace: P-01, P-03*
- [ ] **STEP-09**: Write integration test with sample directory. — *Trace: G-01, G-03*

## Access Control
```yaml
allow_write:
  - "src/organizer.py"
  - "src/utils.py"
  - "README.md"
allow_exec:
  - "python src/organizer.py"
  - "pytest"
```

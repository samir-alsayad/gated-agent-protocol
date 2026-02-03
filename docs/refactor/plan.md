# Implementation Plan: GAP Refactoring & Stabilization

## 1. Plan Overview

This plan executes the refactoring in small, testable increments. Each step maintains a working system and can be committed independently. The approach is conservative: test after every change, never break existing functionality.

**Estimated Duration:** 2-3 weeks (Sprints 2-3)  
**Risk Level:** Medium (architectural changes but well-tested)  
**Rollback Strategy:** Git tags at each phase, maintain v0.1.x branch

## 2. Implementation Steps

### Phase 1: Foundation (Week 1, Days 1-2)

#### STEP-01: Create refactor branch and baseline
**Effort:** 30 minutes  
**Trace:** G-06 (Maintainability)

```bash
git checkout -b refactor/clean-architecture
git tag v0.1.0-baseline
pytest tests/ --cov=src --cov-report=html
# Save coverage report as baseline
```

**Verification:**
- [ ] All tests pass
- [ ] Coverage report generated
- [ ] Baseline tag created

---

#### STEP-02: Move security.py to gap.core
**Effort:** 1 hour  
**Trace:** G-01 (Clean Architecture), P-01 (Single Package)

```bash
# Move file
mv src/gated_agent/security.py src/gap/core/security.py

# Update import in gate.py
# from gated_agent.security import ACLEnforcer
# to
# from gap.core.security import ACLEnforcer
```

**Files Modified:**
- `src/gap/core/security.py` (moved)
- `src/gap/commands/gate.py` (import updated)

**Verification:**
- [ ] `pytest tests/` passes
- [ ] `gap gate approve` command works
- [ ] ACL extraction still functions

---

#### STEP-03: Rename commands/ to cli/
**Effort:** 30 minutes  
**Trace:** G-01 (Clean Architecture), G-06 (Maintainability)

```bash
mv src/gap/commands src/gap/cli
# Update imports in main.py
```

**Files Modified:**
- `src/gap/main.py` (imports updated)
- Directory renamed

**Verification:**
- [ ] All CLI commands work
- [ ] Tests pass
- [ ] No import errors

---

#### STEP-04: Delete dead code from gated_agent
**Effort:** 15 minutes  
**Trace:** G-06 (Maintainability), P-07 (Zero Dead Code)

```bash
rm src/gated_agent/registry.py
rm src/gated_agent/session.py
rm src/gated_agent/cli.py
rm src/gated_agent/README.md
rm src/gated_agent/__init__.py
rmdir src/gated_agent
rm -rf src/gated_agent.egg-info
```

**Verification:**
- [ ] No import errors
- [ ] Tests still pass
- [ ] Package still installs

---

#### STEP-05: Update pyproject.toml
**Effort:** 15 minutes  
**Trace:** P-01 (Single Package), G-02 (Production Readiness)

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/gap"]

[tool.hatch.build]
include = [
  "src/gap/**/*"
]
```

**Verification:**
- [ ] `pip install -e .` works
- [ ] `gap` command available
- [ ] No gated_agent package installed

---

#### STEP-06: Run full test suite and commit Phase 1
**Effort:** 30 minutes  
**Trace:** C-04 (Test Coverage), P-05 (Test Coverage Invariant)

```bash
pytest tests/ --cov=src/gap --cov-report=term-missing
# Verify coverage ≥ baseline
git add -A
git commit -m "refactor: Phase 1 - Merge gated_agent into gap.core"
git tag v0.2.0-phase1
```

**Verification:**
- [ ] All tests pass
- [ ] Coverage maintained or improved
- [ ] No regressions in functionality

---

### Phase 2: SDK Creation (Week 1, Days 3-4)

#### STEP-07: Create gap.sdk module structure
**Effort:** 2 hours  
**Trace:** G-03 (Clear Integration Path), P-02 (Import Path Consistency)

```python
# src/gap/sdk/__init__.py
from .client import GAPClient
from .types import WorkflowStatus, StepInfo

__all__ = ["GAPClient", "WorkflowStatus", "StepInfo"]
```

```python
# src/gap/sdk/types.py
from dataclasses import dataclass
from gap.core.state import StepStatus

@dataclass
class StepInfo:
    name: str
    status: StepStatus
    artifact: str
    can_scribe: bool
    can_approve: bool
```

```python
# src/gap/sdk/client.py
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.factory import get_ledger
from gap.core.security import ACLEnforcer

class GAPClient:
    """High-level API for tool integrations."""
    
    def __init__(self, project_root: str = "."):
        self.root = Path(project_root)
        self.manifest_path = self.root / "manifest.yaml"
        self.manifest = load_manifest(self.manifest_path)
        self.ledger = get_ledger(self.root, self.manifest)
    
    def get_status(self) -> dict:
        """Get current workflow status."""
        return self.ledger.get_status(self.manifest)
    
    def can_scribe(self, step: str) -> bool:
        """Check if step is ready for scribing."""
        status = self.get_status()
        step_data = status.steps.get(step)
        return step_data and step_data.status == StepStatus.UNLOCKED
    
    # ... more methods
```

**Verification:**
- [ ] SDK imports work
- [ ] Basic client operations work
- [ ] Type hints pass mypy

---

#### STEP-08: Write SDK tests
**Effort:** 2 hours  
**Trace:** C-04 (Test Coverage), P-05 (Test Coverage Invariant)

```python
# tests/test_sdk.py
def test_client_initialization(tmp_path):
    # Create test project
    # Initialize client
    # Verify it works
    pass

def test_client_get_status(tmp_path):
    # Test status retrieval
    pass

def test_client_can_scribe(tmp_path):
    # Test scribe readiness check
    pass
```

**Verification:**
- [ ] SDK tests pass
- [ ] Coverage for sdk/ module ≥80%

---

#### STEP-09: Create SDK documentation
**Effort:** 2 hours  
**Trace:** G-03 (Clear Integration Path), G-05 (Documentation Accuracy)

```markdown
# docs/guides/sdk-integration.md
# GAP SDK Integration Guide

## Installation
...

## Basic Usage
...

## IDE Integration Example
...
```

**Verification:**
- [ ] Documentation builds
- [ ] Examples run without modification

---

#### STEP-10: Commit Phase 2
**Effort:** 15 minutes  
**Trace:** G-03 (Clear Integration Path)

```bash
git add -A
git commit -m "feat: Add SDK module for tool integrations"
git tag v0.2.0-phase2
```

---

### Phase 3: Protocol Completion (Week 2, Days 1-3)

#### STEP-11: Create complete software-engineering example
**Effort:** 3 hours  
**Trace:** G-04 (Consistent Protocols), G-05 (Documentation Accuracy)

```bash
mkdir -p src/gap/protocols/software-engineering/examples/todo-cli
# Create complete example with:
# - manifest.yaml
# - docs/intent.md (with G-, C- IDs)
# - docs/spec.md (with P- IDs)
# - docs/plan.md (with STEP- IDs and ACL)
# - docs/walkthrough.md (with validation)
```

**Verification:**
- [ ] Example follows template structure
- [ ] All traceability links valid
- [ ] ACL block present and valid
- [ ] Can run through full workflow

---

#### STEP-12: Migrate instructional protocol examples
**Effort:** 2 hours  
**Trace:** G-04 (Consistent Protocols)

```bash
# Review .archive/protocols_legacy/authoring/instructional/
# Migrate best examples to src/gap/protocols/instructional/examples/
```

**Verification:**
- [ ] Examples follow current manifest format
- [ ] Templates render correctly
- [ ] Full workflow works

---

#### STEP-13: Add protocol validation to check command
**Effort:** 2 hours  
**Trace:** G-04 (Consistent Protocols), P-08 (Documentation Completeness)

```python
# src/gap/cli/check.py
@app.command("protocol")
def check_protocol(path: Path):
    """Validate protocol structure and completeness."""
    # Check manifest.yaml exists and valid
    # Check all templates referenced exist
    # Check examples/ directory exists
    # Check README.md exists
    # Warn if examples missing
```

**Verification:**
- [ ] Command detects incomplete protocols
- [ ] Helpful error messages
- [ ] All built-in protocols pass

---

#### STEP-14: Commit Phase 3
**Effort:** 15 minutes  
**Trace:** G-04 (Consistent Protocols)

```bash
git add -A
git commit -m "feat: Complete protocol examples and validation"
git tag v0.2.0-phase3
```

---

### Phase 4: Documentation & Polish (Week 2, Days 4-5)

#### STEP-15: Update main README.md
**Effort:** 1 hour  
**Trace:** G-05 (Documentation Accuracy)

- Remove references to gated_agent
- Update architecture section
- Add SDK usage example
- Update installation instructions
- Add link to examples/

**Verification:**
- [ ] README accurate
- [ ] All links work
- [ ] Examples run

---

#### STEP-16: Create integration examples
**Effort:** 4 hours  
**Trace:** G-03 (Clear Integration Path)

```python
# examples/ide-integration/cursor_integration.py
"""Example: Integrating GAP with Cursor IDE"""

from gap.sdk import GAPClient

def before_agent_action(file_path: str):
    """Hook called before agent writes file."""
    client = GAPClient()
    
    # Get current step's ACL
    current_step = client.get_current_step()
    acl = client.get_acl(current_step)
    
    # Validate write
    if not acl.validate_write(file_path):
        raise PermissionError(f"Agent not allowed to write {file_path}")
```

**Examples to Create:**
- [ ] Cursor/VSCode integration
- [ ] Aider integration
- [ ] CI/CD integration (GitHub Actions)
- [ ] Custom protocol creation

**Verification:**
- [ ] Examples run without modification
- [ ] Clear comments explaining each step
- [ ] README in each example directory

---

#### STEP-17: Generate API documentation
**Effort:** 2 hours  
**Trace:** G-05 (Documentation Accuracy), P-08 (Documentation Completeness)

```bash
# Setup Sphinx
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints
cd docs/api
sphinx-quickstart
# Configure autodoc
sphinx-apidoc -o . ../../src/gap
make html
```

**Verification:**
- [ ] API docs build without warnings
- [ ] All public APIs documented
- [ ] Examples in docstrings work

---

#### STEP-18: Create migration guide
**Effort:** 1 hour  
**Trace:** C-07 (Clear Upgrade Path)

```markdown
# docs/guides/migration-v0.1-to-v0.2.md

## Breaking Changes
- `gated_agent` package removed
- Import paths changed

## Migration Steps
1. Update imports: `from gated_agent.security` → `from gap.core.security`
2. No changes to manifest.yaml required
3. No changes to .gap/ directory required

## Automated Migration
```bash
gap migrate check  # Check for issues
gap migrate fix    # Auto-fix imports
```
```

**Verification:**
- [ ] Migration guide complete
- [ ] Covers all breaking changes
- [ ] Provides automated tools

---

#### STEP-19: Commit Phase 4
**Effort:** 15 minutes  
**Trace:** G-05 (Documentation Accuracy)

```bash
git add -A
git commit -m "docs: Complete documentation and examples"
git tag v0.2.0-phase4
```

---

### Phase 5: Testing & Validation (Week 3, Days 1-2)

#### STEP-20: Add integration tests
**Effort:** 4 hours  
**Trace:** C-04 (Test Coverage), G-02 (Production Readiness)

```python
# tests/integration/test_full_workflow.py
def test_software_engineering_workflow(tmp_path):
    """Test complete software engineering workflow."""
    # 1. Initialize project
    # 2. Scribe requirements
    # 3. Approve requirements
    # 4. Scribe design
    # 5. Approve design
    # 6. Scribe plan (with ACL)
    # 7. Approve plan
    # 8. Verify ACL stored
    # 9. Scribe walkthrough
    # 10. Approve walkthrough
    # 11. Verify all complete
    pass
```

**Tests to Add:**
- [ ] Full software-engineering workflow
- [ ] Full instructional workflow
- [ ] ACL enforcement during workflow
- [ ] State machine bypass attempts
- [ ] Backward compatibility with v0.1.0 fixtures

**Verification:**
- [ ] All integration tests pass
- [ ] Tests cover happy path and error cases
- [ ] Tests run in <10 seconds

---

#### STEP-21: Add performance benchmarks
**Effort:** 2 hours  
**Trace:** C-05 (Performance Preservation), P-06 (Performance Invariant)

```python
# tests/benchmarks/test_performance.py
import time

def test_check_status_performance(benchmark_project):
    """Verify check status completes in <100ms."""
    start = time.time()
    result = subprocess.run(["gap", "check", "status", "manifest.yaml"])
    duration = time.time() - start
    assert duration < 0.1, f"Too slow: {duration}s"
```

**Benchmarks:**
- [ ] gap check status
- [ ] gap scribe create
- [ ] gap gate approve
- [ ] Manifest validation
- [ ] Template resolution

**Verification:**
- [ ] All benchmarks pass
- [ ] No regressions from baseline

---

#### STEP-22: Security audit
**Effort:** 3 hours  
**Trace:** C-03 (Security Model Preservation), P-04 (Security Preservation)

```python
# tests/security/test_acl_bypass.py
def test_path_traversal_blocked():
    """Verify path traversal attacks are blocked."""
    acl = ACLEnforcer(content="allow_write: ['src/*.py']")
    with pytest.raises(PermissionError):
        acl.validate_write("../etc/passwd")

def test_command_injection_blocked():
    """Verify command injection is blocked."""
    acl = ACLEnforcer(content="allow_exec: ['pytest']")
    with pytest.raises(PermissionError):
        acl.validate_exec("pytest; rm -rf /")
```

**Security Tests:**
- [ ] Path traversal prevention
- [ ] Command injection prevention
- [ ] State machine bypass attempts
- [ ] ACL bypass attempts
- [ ] Symlink attacks

**Verification:**
- [ ] All security tests pass
- [ ] No vulnerabilities found

---

#### STEP-23: Cross-platform testing
**Effort:** 2 hours  
**Trace:** G-02 (Production Readiness)

```bash
# Test on multiple platforms
# - macOS (current)
# - Linux (Docker)
# - Windows (GitHub Actions)
```

**Verification:**
- [ ] Tests pass on macOS
- [ ] Tests pass on Linux
- [ ] Tests pass on Windows
- [ ] Package installs on all platforms

---

#### STEP-24: Commit Phase 5
**Effort:** 15 minutes  
**Trace:** G-02 (Production Readiness)

```bash
pytest tests/ --cov=src/gap --cov-report=html --cov-report=term
# Verify ≥80% coverage
git add -A
git commit -m "test: Add integration, performance, and security tests"
git tag v0.2.0-phase5
```

---

### Phase 6: Release Preparation (Week 3, Days 3-5)

#### STEP-25: Update version to 0.2.0
**Effort:** 15 minutes  
**Trace:** G-02 (Production Readiness)

```toml
# pyproject.toml
[project]
version = "0.2.0"
```

**Verification:**
- [ ] Version updated
- [ ] CHANGELOG.md updated

---

#### STEP-26: Create CHANGELOG.md
**Effort:** 1 hour  
**Trace:** G-05 (Documentation Accuracy)

```markdown
# Changelog

## [0.2.0] - 2026-02-XX

### Added
- SDK module for tool integrations
- Complete protocol examples
- Integration examples (IDE, CI/CD)
- API documentation
- Performance benchmarks
- Security tests

### Changed
- Merged gated_agent into gap.core
- Renamed commands/ to cli/
- Enhanced protocol templates with EARS syntax

### Removed
- Dead code (registry.py, session.py, cli.py)
- gated_agent package

### Fixed
- All critical bugs from Sprint 1
- ACL enforcement now active
- State machine bypass prevented

### Security
- ACL validation during approval
- Path traversal prevention
- Command injection prevention
```

**Verification:**
- [ ] CHANGELOG complete
- [ ] All changes documented
- [ ] Links to issues/PRs

---

#### STEP-27: Final review and testing
**Effort:** 2 hours  
**Trace:** G-02 (Production Readiness)

**Checklist:**
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] Documentation builds
- [ ] Examples work
- [ ] No dead code
- [ ] No TODO comments
- [ ] All type hints pass mypy
- [ ] Code formatted with black
- [ ] No security vulnerabilities

---

#### STEP-28: Create release
**Effort:** 1 hour  
**Trace:** G-02 (Production Readiness)

```bash
# Merge to main
git checkout main
git merge refactor/clean-architecture
git tag v0.2.0
git push origin main --tags

# Build package
python -m build

# Test install
pip install dist/gated_agent_protocol-0.2.0-py3-none-any.whl

# Publish to PyPI
twine upload dist/*
```

**Verification:**
- [ ] Package builds successfully
- [ ] Package installs cleanly
- [ ] CLI works after install
- [ ] Published to PyPI

---

## 3. Access Control

```yaml
allow_write:
  - "src/gap/**/*.py"
  - "tests/**/*.py"
  - "docs/**/*.md"
  - "examples/**/*"
  - "pyproject.toml"
  - "README.md"
  - "CHANGELOG.md"
  - ".gitignore"

allow_exec:
  - "pytest tests/"
  - "pytest tests/ --cov=src/gap"
  - "python -m build"
  - "pip install -e ."
  - "git add -A"
  - "git commit -m *"
  - "git tag v*"
  - "sphinx-build docs/api docs/api/_build"
  - "black src/ tests/"
  - "mypy src/gap"
```

## 4. Risk Mitigation

### High Risk: Breaking Existing Projects
**Mitigation:**
- Test with v0.1.0 fixtures
- Maintain backward compatibility
- Provide migration tools
- Keep v0.1.x branch for critical fixes

### Medium Risk: Performance Regression
**Mitigation:**
- Benchmark before/after each phase
- Fail if >10% regression
- Profile slow operations
- Optimize if needed

### Medium Risk: Scope Creep
**Mitigation:**
- Strict adherence to plan
- Defer non-critical features
- Time-box each step
- Review progress daily

## 5. Success Criteria

### Must Have (Blocking Release)
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] No critical bugs
- [ ] Documentation complete
- [ ] Examples work
- [ ] Backward compatible

### Should Have (Important)
- [ ] SDK fully functional
- [ ] Integration examples
- [ ] Performance benchmarks pass
- [ ] Security audit clean

### Nice to Have (Can Defer)
- [ ] Visual diagrams in docs
- [ ] Video tutorials
- [ ] Community protocols
- [ ] IDE plugins

---

**Verification Rule:** Total step coverage MUST account for 100% of defined Goals and Properties.

**Next Step:** Begin execution with STEP-01, commit after each step, review progress daily.

# Specification: GAP Refactoring & Stabilization

## 1. Architecture Overview

### Target Package Structure
```
gated-agent-protocol/
├── src/gap/
│   ├── __init__.py           # Public API exports
│   ├── main.py               # CLI entry point
│   │
│   ├── cli/                  # CLI commands (user-facing)
│   │   ├── __init__.py
│   │   ├── check.py          # gap check {status,manifest,integrity}
│   │   ├── scribe.py         # gap scribe create
│   │   ├── gate.py           # gap gate {list,approve}
│   │   └── migrate.py        # gap migrate run
│   │
│   ├── core/                 # Core engine (library)
│   │   ├── __init__.py
│   │   ├── manifest.py       # Manifest loading and validation
│   │   ├── state.py          # State machine logic
│   │   ├── ledger.py         # Abstract ledger interface
│   │   ├── yaml_ledger.py    # YAML implementation
│   │   ├── sql_ledger.py     # SQL implementation
│   │   ├── factory.py        # Ledger factory
│   │   ├── path.py           # Template resolution
│   │   ├── validator.py      # Manifest validation
│   │   ├── security.py       # ACL enforcement (moved from gated_agent)
│   │   └── models.py         # SQLAlchemy models
│   │
│   ├── protocols/            # Built-in protocols
│   │   ├── instructional/
│   │   │   ├── manifest.yaml
│   │   │   ├── templates/
│   │   │   └── examples/
│   │   │
│   │   └── software-engineering/
│   │       ├── manifest.yaml
│   │       ├── templates/
│   │       └── examples/
│   │
│   └── sdk/                  # Integration SDK (for tool builders)
│       ├── __init__.py
│       ├── client.py         # High-level API
│       └── types.py          # Shared types
│
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
│
├── docs/                     # Documentation
│   ├── api/                  # API reference
│   ├── guides/               # User guides
│   ├── integration/          # Integration examples
│   └── refactor/             # This refactoring effort
│
└── examples/                 # Working examples
    ├── basic-workflow/
    ├── ide-integration/
    └── custom-protocol/
```

### Key Changes from Current Structure
1. **Merge gated_agent into gap**: Single package, clear structure
2. **Rename commands/ to cli/**: More accurate naming
3. **Add sdk/ module**: Clear API for tool builders
4. **Add examples/**: Working code, not just docs
5. **Reorganize tests/**: Unit vs integration separation
6. **Remove dead code**: registry.py, session.py, cli.py

## 2. Properties (Invariants)

### P-01: Single Package Invariant
**Property:** The system SHALL be distributed as exactly one Python package named `gap`.  
**Validates:** G-01 (Clean Architecture), G-06 (Maintainability)  
**Verification:** `pip install gated-agent-protocol` installs only `gap` package, no `gated_agent`.

### P-02: Import Path Consistency
**Property:** All public APIs SHALL be importable from `gap.*`, never from internal modules.  
**Validates:** G-03 (Clear Integration Path), G-06 (Maintainability)  
**Verification:** 
```python
# Good (public API)
from gap import Manifest, Ledger, ACLEnforcer
from gap.sdk import GAPClient

# Bad (internal implementation)
from gap.core.ledger import YamlLedger  # Should not be public
```

### P-03: Backward Compatibility Invariant
**Property:** Existing `.gap/status.yaml` files SHALL be readable without modification.  
**Validates:** C-01 (Backward Compatibility)  
**Verification:** Load test fixtures from v0.1.0 and verify they parse correctly.

### P-04: Security Preservation Invariant
**Property:** ACL enforcement SHALL be at least as strict after refactoring.  
**Validates:** C-03 (Security Model Preservation)  
**Verification:** Security test suite passes with same or stricter results.

### P-05: Test Coverage Invariant
**Property:** Core modules SHALL have ≥80% test coverage.  
**Validates:** C-04 (Test Coverage Requirement), G-02 (Production Readiness)  
**Verification:** `pytest --cov=gap.core --cov-report=term-missing` shows ≥80%.

### P-06: Performance Invariant
**Property:** Common operations SHALL complete within performance budgets:
- `gap check status`: <100ms
- `gap scribe create`: <500ms  
- `gap gate approve`: <200ms

**Validates:** C-05 (Performance Preservation)  
**Verification:** Benchmark suite comparing before/after.

### P-07: Zero Dead Code Invariant
**Property:** All Python files in `src/gap/` SHALL be imported by at least one test or CLI command.  
**Validates:** G-06 (Maintainability)  
**Verification:** Coverage report shows no 0% coverage files.

### P-08: Documentation Completeness Invariant
**Property:** All public functions/classes SHALL have docstrings with examples.  
**Validates:** G-05 (Documentation Accuracy), G-03 (Clear Integration Path)  
**Verification:** Sphinx build with `nitpicky=True` passes without warnings.

## 3. Component Specifications

### 3.1 CLI Module (`gap.cli`)

**Purpose:** User-facing command-line interface

**Public Commands:**
```bash
gap check status <manifest>      # Show workflow status
gap check manifest <manifest>    # Validate manifest
gap check integrity <manifest>   # Detect drift

gap scribe create <step>         # Generate artifact
gap scribe create <step> --dry-run

gap gate list                    # List proposals
gap gate approve <step>          # Approve proposal

gap migrate run                  # Migrate YAML to SQL
```

**Design Principles:**
- Commands are verbs (check, scribe, gate)
- Subcommands are nouns (status, manifest, integrity)
- Consistent flag naming (--manifest, --dry-run, --force)
- Rich output with colors and icons
- JSON output mode for scripting (--json flag)

**Error Handling:**
- Exit code 0 for success
- Exit code 1 for user errors (bad input)
- Exit code 2 for system errors (file not found)
- Clear error messages with hints

### 3.2 Core Module (`gap.core`)

**Purpose:** State machine and workflow engine

**Public API:**
```python
# Manifest operations
manifest = load_manifest(path)
errors = validate_manifest(manifest)

# State operations
ledger = get_ledger(root, manifest)
status = ledger.get_status(manifest)
ledger.update_status(step, StepStatus.COMPLETE)

# Security operations
enforcer = ACLEnforcer(content=artifact_content)
enforcer.validate_write(path)
enforcer.validate_exec(command)

# Template operations
path_manager = PathManager(root)
template_path = path_manager.resolve_template(manifest, name)
```

**Design Principles:**
- Immutable data structures where possible
- Clear separation of concerns
- Dependency injection (pass ledger, don't create it)
- Type hints on all public functions
- Comprehensive error messages

### 3.3 SDK Module (`gap.sdk`)

**Purpose:** High-level API for tool integrations

**Public API:**
```python
from gap.sdk import GAPClient

# Initialize
client = GAPClient(project_root=".")

# Check status
status = client.get_status()
if status.can_scribe("requirements"):
    client.scribe("requirements", data={...})

# Approve proposals
proposals = client.list_proposals()
client.approve("requirements")

# Security enforcement
with client.enforce_acl("plan"):
    # File operations restricted by ACL
    write_file("src/main.py", content)
```

**Design Principles:**
- Simple, high-level API
- Context managers for ACL enforcement
- Clear error messages
- Minimal dependencies
- Well-documented with examples

### 3.4 Protocol Structure

**Standard Protocol Layout:**
```
protocols/<name>/
├── manifest.yaml          # Protocol definition
├── README.md             # Protocol documentation
├── templates/            # Jinja2 templates
│   ├── step1.md
│   └── step2.md
└── examples/             # Complete examples
    └── example-project/
        ├── manifest.yaml
        ├── docs/
        └── .gap/
```

**Manifest Schema (Enforced):**
```yaml
kind: protocol
name: string
version: semver
description: string

flow:
  - step: string          # Unique ID
    name: string          # Display name
    template: string      # Template name
    artifact: path        # Output path
    gate: manual|auto     # Gate type
    needs: [string]       # Dependencies
    description: string   # Help text

templates:
  step_name: path         # Template mapping
```

## 4. Data Models

### 4.1 State Machine States
```python
class StepStatus(Enum):
    LOCKED = "locked"       # Dependencies not met
    UNLOCKED = "unlocked"   # Ready to scribe
    PENDING = "pending"     # Proposal exists
    COMPLETE = "complete"   # Approved and live
    INVALID = "invalid"     # File exists but deps not met
```

### 4.2 Ledger Schema (YAML)
```yaml
steps:
  step_name:
    status: complete
    timestamp: "2026-02-03T10:30:00"
    approver: "user"
```

### 4.3 Ledger Schema (SQL)
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    protocol TEXT NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE steps (
    id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    approver TEXT,
    timestamp TIMESTAMP,
    UNIQUE(project_id, name)
);

CREATE TABLE history (
    id INTEGER PRIMARY KEY,
    step_id INTEGER NOT NULL,
    old_status TEXT,
    new_status TEXT,
    actor TEXT,
    timestamp TIMESTAMP
);
```

### 4.4 ACL Schema
```yaml
allow_write:
  - "src/**/*.py"
  - "tests/**/*.py"

allow_exec:
  - "pytest tests/"
  - "python -m mypy src/"
```

## 5. Interface Contracts

### 5.1 Ledger Interface
```python
class Ledger(ABC):
    @abstractmethod
    def get_status(self, manifest: GapManifest) -> GapStatus:
        """Calculate current status of all steps."""
        pass
    
    @abstractmethod
    def update_status(
        self, 
        step: str, 
        status: StepStatus, 
        approver: str = "user",
        timestamp: Optional[datetime] = None
    ) -> None:
        """Update step status in ledger."""
        pass
```

**Invariants:**
- `get_status()` is idempotent
- `update_status()` is atomic
- File system is source of truth for COMPLETE status

### 5.2 ACL Enforcer Interface
```python
class ACLEnforcer:
    def __init__(self, content: str):
        """Parse ACL from markdown content."""
        pass
    
    def validate_write(self, path: str) -> bool:
        """Check if write is allowed. Raises PermissionError if not."""
        pass
    
    def validate_exec(self, command: str) -> bool:
        """Check if exec is allowed. Raises PermissionError if not."""
        pass
```

**Invariants:**
- Deny by default (empty ACL = read-only)
- Path traversal attacks prevented
- Command injection prevented

### 5.3 Template Resolution Interface
```python
class PathManager:
    def resolve_template(
        self, 
        manifest: GapManifest, 
        name: str
    ) -> Path:
        """Resolve template path with inheritance."""
        pass
```

**Resolution Order:**
1. Project templates/ directory
2. Protocol templates/ directory (if extends)
3. Built-in protocol templates/
4. Raise FileNotFoundError

## 6. Dependencies

### Required Dependencies
```toml
[project]
dependencies = [
    "typer>=0.9.0",      # CLI framework
    "pydantic>=2.0.0",   # Data validation
    "jinja2>=3.1.0",     # Template rendering
    "rich>=13.0.0",      # Terminal output
    "pyyaml>=6.0",       # YAML parsing
]
```

### Optional Dependencies
```toml
[project.optional-dependencies]
sql = ["sqlalchemy>=2.0.0"]  # For SQL ledger
dev = ["pytest", "pytest-cov", "black", "mypy"]
docs = ["sphinx", "sphinx-rtd-theme"]
```

### Dependency Principles
- Minimal required dependencies
- No network dependencies
- Pin major versions only
- All deps must be actively maintained

## 7. Migration Strategy

### Phase 1: Restructure (No Breaking Changes)
1. Move `gated_agent/security.py` → `gap/core/security.py`
2. Rename `gap/commands/` → `gap/cli/`
3. Create `gap/sdk/` with high-level API
4. Update all imports
5. Run full test suite

### Phase 2: Clean Up
1. Delete dead code (registry.py, session.py, cli.py)
2. Remove unused imports
3. Update documentation
4. Add missing docstrings

### Phase 3: Enhance
1. Add integration examples
2. Complete protocol examples
3. Add SDK documentation
4. Create migration guide

### Rollback Plan
- Keep git tags at each phase
- Maintain v0.1.x branch for critical fixes
- Provide downgrade instructions if needed

## 8. Testing Strategy

### Unit Tests (80% coverage minimum)
- Test each module in isolation
- Mock external dependencies
- Fast (<1s total runtime)

### Integration Tests
- Test full workflows end-to-end
- Use temporary directories
- Test both YAML and SQL ledgers

### Security Tests
- ACL bypass attempts
- Path traversal attacks
- Command injection attempts
- State machine bypass attempts

### Performance Tests
- Benchmark common operations
- Compare before/after refactor
- Fail if >10% regression

### Compatibility Tests
- Load v0.1.0 fixtures
- Verify backward compatibility
- Test on Windows, Mac, Linux

## 9. Documentation Requirements

### User Documentation
- [ ] Installation guide
- [ ] Quick start tutorial
- [ ] Command reference
- [ ] Protocol authoring guide
- [ ] Troubleshooting guide

### Developer Documentation
- [ ] Architecture overview
- [ ] API reference (auto-generated)
- [ ] Integration guide
- [ ] Contributing guide
- [ ] Testing guide

### Examples
- [ ] Basic workflow example
- [ ] Custom protocol example
- [ ] IDE integration example
- [ ] CI/CD integration example

## 10. Success Metrics

### Code Quality
- Test coverage ≥80%
- No critical bugs
- No dead code
- All type hints pass mypy

### Performance
- All operations within budget
- No regressions from v0.1.0

### Usability
- Installation works first try
- Examples run without modification
- Error messages are helpful

### Maintainability
- New contributor can understand architecture
- Adding protocol takes <1 hour
- Clear separation of concerns

---

**Verification Rule:** Every property MUST validate at least one Goal ID from intent.md.

**Next Step:** Create `plan.md` with specific implementation tasks and traceability.

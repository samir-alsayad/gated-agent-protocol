# GAP Release Readiness Plan

**Target:** Production-ready v0.2.0  
**Timeline:** 6 weeks (3 sprints × 2 weeks)  
**Priority:** Fix critical bugs → Complete security → Harden & document

---

## Sprint 1: Critical Bug Fixes (Week 1-2)

### Goal: Make core functionality work correctly

### Task 1.1: Fix Factory Pattern (BUG-001)
**Priority:** 🔴 Blocker  
**Effort:** 2 hours  
**Owner:** Core team

**Changes:**
```python
# src/gap/core/factory.py
def get_ledger(root: Path, manifest: GapManifest) -> Ledger:
    db_url = os.environ.get("GAP_DB_URL")
    if db_url:
        return SqlLedger(
            db_url=db_url,
            project_name=manifest.name,
            protocol=f"{manifest.kind}-{manifest.version}",
            root=root
        )
    return YamlLedger(root)
```

**Verification:**
- Run `tests/test_factory_integration.py`
- Manual test with GAP_DB_URL set

---

### Task 1.2: Add Dependency Validation (BUG-002)
**Priority:** 🔴 Blocker  
**Effort:** 4 hours

**Changes:**
```python
# src/gap/core/ledger.py - Both YamlLedger and SqlLedger
def get_status(self, manifest):
    # ... existing code ...
    
    if is_live:
        # NEW: Verify dependencies before marking complete
        deps_met = all(
            real_status.steps.get(dep, StepData(status=StepStatus.LOCKED)).status 
            == StepStatus.COMPLETE
            for dep in step.needs
        )
        if not deps_met:
            current = StepStatus.INVALID  # New state
        else:
            current = StepStatus.COMPLETE
```

**New State:**
- Add `INVALID` to `StepStatus` enum
- Means: file exists but dependencies not met

**Verification:**
- Create test that manually creates design.md without requirements.md
- Should show INVALID status

---

### Task 1.3: Integrate ACL Enforcer (BUG-003)
**Priority:** 🔴 Blocker  
**Effort:** 8 hours

**Changes:**

1. **Extract ACL during approval:**
```python
# src/gap/commands/gate.py
def approve(step, manifest_path):
    # ... existing validation ...
    
    # NEW: Extract and validate ACL
    with open(proposal_path) as f:
        content = f.read()
    
    enforcer = ACLEnforcer(content=content)
    
    # Warn if no ACL for manual gates
    if step_def.gate == GateType.MANUAL:
        if not enforcer.context.allowed_writes:
            typer.secho(
                "⚠️  Warning: No ACL block found. "
                "Next gate will be read-only.",
                fg=typer.colors.YELLOW
            )
            if not typer.confirm("Continue?"):
                raise typer.Exit(0)
    
    # Store ACL for next gate
    acl_path = root / ".gap" / "acls" / f"{step}.yaml"
    acl_path.parent.mkdir(parents=True, exist_ok=True)
    with open(acl_path, "w") as f:
        yaml.dump({
            "allow_write": enforcer.context.allowed_writes,
            "allow_exec": enforcer.context.allowed_execs
        }, f)
    
    # ... existing move and ledger update ...
```

2. **Add ACL validation command:**
```python
# src/gap/commands/check.py
@app.command("acl")
def check_acl(artifact: Path):
    """Validate ACL block in an artifact."""
    enforcer = ACLEnforcer(artifact_path=str(artifact))
    # ... validation logic ...
```

**Verification:**
- Create proposal with ACL block
- Approve and verify ACL stored
- Create proposal without ACL, verify warning

---


### Task 1.4: Make Gate Approval Atomic (BUG-004)
**Priority:** 🟠 High  
**Effort:** 4 hours

**Changes:**
```python
# src/gap/commands/gate.py
def approve(step, manifest_path):
    # ... validation ...
    
    # NEW: Atomic operation with rollback
    backup_path = None
    try:
        # Backup existing file
        if target_path.exists():
            backup_path = target_path.with_suffix(target_path.suffix + ".bak")
            shutil.copy2(target_path, backup_path)
        
        # Move proposal
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(proposal_path), str(target_path))
        
        # Update ledger
        ledger.update_status(step, StepStatus.COMPLETE, approver="user")
        
        # Success - remove backup
        if backup_path and backup_path.exists():
            backup_path.unlink()
            
    except Exception as e:
        # Rollback
        if backup_path and backup_path.exists():
            shutil.move(str(backup_path), str(target_path))
        typer.secho(f"❌ Approval failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
```

**Verification:**
- Mock ledger failure, verify file not moved
- Test with existing file, verify backup/restore

---

### Task 1.5: Add Manifest Validation (BUG-006)
**Priority:** 🟠 High  
**Effort:** 6 hours

**New Module:**
```python
# src/gap/core/validator.py
class ManifestValidator:
    def validate(self, manifest: GapManifest) -> List[ValidationError]:
        errors = []
        errors.extend(self._check_circular_deps(manifest))
        errors.extend(self._check_missing_refs(manifest))
        errors.extend(self._check_templates(manifest))
        return errors
    
    def _check_circular_deps(self, manifest):
        # Topological sort to detect cycles
        pass
    
    def _check_missing_refs(self, manifest):
        # Verify all 'needs' point to valid steps
        pass
```

**New Command:**
```python
# src/gap/commands/check.py
@app.command("manifest")
def check_manifest(path: Path):
    """Validate manifest structure and dependencies."""
    manifest = load_manifest(path)
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    if errors:
        for err in errors:
            typer.secho(f"❌ {err}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    typer.secho("✅ Manifest is valid", fg=typer.colors.GREEN)
```

**Verification:**
- Create manifest with circular deps (A→B→A)
- Create manifest with missing ref (needs: [nonexistent])
- Both should be caught

---

## Sprint 1 Deliverables

- ✅ SQL ledger functional
- ✅ State machine enforces dependencies
- ✅ ACL blocks extracted and stored
- ✅ Gate approval is atomic
- ✅ Manifest validation prevents bad configs

**Exit Criteria:**
- All blocker bugs fixed
- Core workflow works end-to-end
- No data loss on failures

---

## Sprint 2: Security & Completeness (Week 3-4)

### Goal: Implement full security model and complete missing pieces

### Task 2.1: ACL Schema Validation
**Priority:** 🔴 Critical  
**Effort:** 4 hours

**Changes:**
```python
# src/gated_agent/security.py
class ACLValidator:
    DANGEROUS_PATTERNS = [
        "**",           # Full wildcard
        "/*",           # Root access
        "/etc/*",       # System files
        "~/.ssh/*",     # SSH keys
        ".git/*",       # Git internals
    ]
    
    def validate(self, context: ACLContext) -> List[str]:
        warnings = []
        
        for pattern in context.allowed_writes:
            if any(danger in pattern for danger in self.DANGEROUS_PATTERNS):
                warnings.append(f"Dangerous write pattern: {pattern}")
        
        for cmd in context.allowed_execs:
            if any(danger in cmd for danger in ["rm -rf", "sudo", "curl"]):
                warnings.append(f"Dangerous exec command: {cmd}")
        
        return warnings
```

**Integration:**
```python
# In gate.py approve()
validator = ACLValidator()
warnings = validator.validate(enforcer.context)
if warnings:
    for w in warnings:
        typer.secho(f"⚠️  {w}", fg=typer.colors.RED)
    if not typer.confirm("These patterns are HIGH RISK. Approve anyway?"):
        raise typer.Exit(0)
```

---

### Task 2.2: Complete Software Engineering Protocol
**Priority:** 🟠 High  
**Effort:** 6 hours

**Create Missing Templates:**

1. `src/gap/protocols/software-engineering/templates/requirements.md`
2. `src/gap/protocols/software-engineering/templates/design.md`
3. `src/gap/protocols/software-engineering/templates/plan.md` (with ACL block)
4. `src/gap/protocols/software-engineering/templates/task.md`
5. `src/gap/protocols/software-engineering/templates/verification.md`

**Key Addition - plan.md:**
```markdown
# Implementation Plan

## Tasks
- [ ] Task 1
- [ ] Task 2

## Access Control
```yaml
allow_write:
  - "src/**/*.py"
  - "tests/**/*.py"
allow_exec:
  - "pytest tests/"
  - "python -m mypy src/"
```
```

---

### Task 2.3: Add Integrity Checking
**Priority:** 🟠 High  
**Effort:** 4 hours

**New Command:**
```python
# src/gap/commands/check.py
@app.command("integrity")
def check_integrity(manifest_path: Path):
    """Detect drift between ledger and file system."""
    manifest = load_manifest(manifest_path)
    root = manifest_path.parent
    ledger = get_ledger(root, manifest)
    
    # Load raw ledger data
    ledger_path = root / ".gap/status.yaml"
    if ledger_path.exists():
        with open(ledger_path) as f:
            ledger_data = yaml.safe_load(f) or {}
    
    # Compare with reality
    status = ledger.get_status(manifest)
    issues = []
    
    for step_name, step_data in status.steps.items():
        ledger_status = ledger_data.get("steps", {}).get(step_name, {}).get("status")
        if ledger_status and ledger_status != step_data.status.value:
            issues.append(f"{step_name}: ledger says {ledger_status}, "
                         f"reality is {step_data.status.value}")
    
    if issues:
        typer.secho("⚠️  Drift detected:", fg=typer.colors.YELLOW)
        for issue in issues:
            typer.echo(f"  - {issue}")
    else:
        typer.secho("✅ No drift detected", fg=typer.colors.GREEN)
```

---

### Task 2.4: Comprehensive Test Suite
**Priority:** 🔴 Critical  
**Effort:** 12 hours

**New Test Files:**

1. `tests/commands/test_scribe.py` - Test artifact generation
2. `tests/commands/test_gate.py` - Test approval workflow
3. `tests/test_acl_enforcer.py` - Test security validation
4. `tests/test_validator.py` - Test manifest validation
5. `tests/integration/test_workflow.py` - End-to-end tests

**Coverage Target:** 80%

**Key Test Scenarios:**
- Happy path: full workflow from requirements to verification
- Dependency violation: skip step, verify blocked
- ACL validation: dangerous patterns detected
- Atomic rollback: failure during approval
- Concurrent access: two approvals simultaneously (SQL only)
- Template inheritance: project overrides protocol template

---

### Task 2.5: Fix Template Resolution
**Priority:** 🟠 High  
**Effort:** 3 hours

**Changes:**
```python
# src/gap/core/path.py
def resolve_template(self, manifest: GapManifest, name: str) -> Path:
    # 1. Check explicit mapping
    if name in manifest.templates:
        mapped_path = self.root / manifest.templates[name]
        if mapped_path.exists():
            return mapped_path
    
    # 2. Check local templates/
    local_path = self.root / f"templates/{name}.md"
    if local_path.exists():
        return local_path
    
    # 3. Check parent protocols (NEW: dynamic resolution)
    for protocol_ref in manifest.extends:
        protocol_path = self.package_root / "protocols" / protocol_ref.protocol
        template_path = protocol_path / "templates" / f"{name}.md"
        if template_path.exists():
            return template_path
    
    # 4. Check package protocols (fallback)
    pkg_path = self.package_root / "protocols" / manifest.name / "templates" / f"{name}.md"
    if pkg_path.exists():
        return pkg_path
    
    raise FileNotFoundError(f"Template '{name}' not found in inheritance chain")
```

---

## Sprint 2 Deliverables

- ✅ ACL validation with dangerous pattern detection
- ✅ Software engineering protocol complete with templates
- ✅ Integrity checking command
- ✅ 80%+ test coverage
- ✅ Template inheritance works correctly

**Exit Criteria:**
- Security model fully enforced
- All protocols have complete templates
- Test suite passes with high coverage
- No known critical bugs

---

## Sprint 3: Hardening & Documentation (Week 5-6)

### Goal: Production-grade quality and user experience

### Task 3.1: Error Message Improvements
**Priority:** 🟡 Medium  
**Effort:** 4 hours

**Examples:**

Before:
```
Error: Template 'design' not found.
```

After:
```
❌ Template 'design' not found

Searched in:
  1. ./templates/design.md (not found)
  2. ./protocols/instructional/templates/design.md (not found)
  
Hint: Check your manifest.yaml 'templates' mapping or create the template file.
```

**Apply to:**
- Template resolution errors
- Manifest validation errors
- State machine violations
- ACL validation failures

---

### Task 3.2: API Documentation
**Priority:** 🟡 Medium  
**Effort:** 8 hours

**Setup Sphinx:**
```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs/api
```

**Document:**
- All public classes and methods
- Usage examples for each command
- Integration guide for tool builders
- Protocol authoring guide

**Generate:**
```bash
cd docs/api
make html
```

---

### Task 3.3: Clean Up Dead Code
**Priority:** 🟡 Medium  
**Effort:** 2 hours

**Remove:**
- `src/gated_agent/session.py` (or document as future feature)
- `src/gated_agent/registry.py` (replaced by manifest.py)
- Unused imports
- Commented-out code

**Update:**
- `src/gated_agent/README.md` to reflect actual implementation
- Remove references to removed modules

---

### Task 3.4: Performance Optimization
**Priority:** 🟢 Low  
**Effort:** 4 hours

**Optimizations:**

1. **Cache file existence checks:**
```python
# src/gap/core/ledger.py
class YamlLedger(Ledger):
    def __init__(self, root: Path):
        super().__init__(root)
        self._file_cache = {}
        self._cache_timestamp = None
    
    def _file_exists(self, path: Path) -> bool:
        # Cache for 1 second
        now = time.time()
        if self._cache_timestamp and (now - self._cache_timestamp) < 1:
            return self._file_cache.get(str(path), path.exists())
        
        # Refresh cache
        self._file_cache.clear()
        exists = path.exists()
        self._file_cache[str(path)] = exists
        self._cache_timestamp = now
        return exists
```

2. **Optimize SQL queries:**
```python
# src/gap/core/sql_ledger.py
def get_status(self, manifest):
    # Single query instead of N queries
    with self.Session() as session:
        db_steps = session.query(Step)\
            .filter_by(project_id=self.project_id)\
            .all()
        db_map = {s.name: s for s in db_steps}
    # ... rest of logic ...
```

---

### Task 3.5: User Experience Polish
**Priority:** 🟡 Medium  
**Effort:** 6 hours

**Improvements:**

1. **Progress indicators:**
```python
# For long operations
with typer.progressbar(manifest.flow) as progress:
    for step in progress:
        # ... validation ...
```

2. **Colored diff for proposals:**
```python
@app.command("diff")
def diff_proposal(step: str):
    """Show changes between proposal and live artifact."""
    # Use difflib to show colored diff
```

3. **Interactive mode:**
```python
@app.command("wizard")
def wizard():
    """Interactive workflow for creating projects."""
    # Step-by-step prompts
```

4. **Better status display:**
```
🔍 Protocol: software-engineering (v0.1.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ requirements    COMPLETE  (approved by alice, 2 days ago)
🟢 design          UNLOCKED  (ready to scribe)
🔒 plan            LOCKED    (waiting for: design)
🔒 implementation  LOCKED    (waiting for: plan)
🔒 verification    LOCKED    (waiting for: implementation)
```

---

### Task 3.6: Security Audit
**Priority:** 🔴 Critical  
**Effort:** 8 hours

**Audit Checklist:**

- [ ] Path traversal attacks (../ in ACL paths)
- [ ] Command injection in exec whitelist
- [ ] YAML bomb attacks in manifest
- [ ] Race conditions in file operations
- [ ] Symlink attacks
- [ ] Permission escalation via ACL
- [ ] Ledger tampering
- [ ] Proposal injection

**Mitigations:**
```python
# Path sanitization
def sanitize_path(path: str) -> str:
    normalized = os.path.normpath(path)
    if normalized.startswith(".."):
        raise SecurityError("Path traversal detected")
    return normalized

# Command sanitization
def sanitize_command(cmd: str) -> str:
    if any(char in cmd for char in [";", "&", "|", "`"]):
        raise SecurityError("Command injection detected")
    return cmd
```

---

### Task 3.7: Release Documentation
**Priority:** 🔴 Critical  
**Effort:** 6 hours

**Create:**

1. **CHANGELOG.md** - All changes from v0.1.0
2. **MIGRATION_GUIDE.md** - How to upgrade from v0.1.0
3. **QUICKSTART.md** - 5-minute tutorial
4. **FAQ.md** - Common questions
5. **TROUBLESHOOTING.md** - Common issues and solutions

**Update:**
- README.md with new features
- Installation instructions
- Example workflows

---

## Sprint 3 Deliverables

- ✅ Clear, helpful error messages
- ✅ Complete API documentation
- ✅ No dead code
- ✅ Performance optimized
- ✅ Polished UX
- ✅ Security audit complete
- ✅ Release documentation ready

**Exit Criteria:**
- All documentation complete
- Security audit passed
- Performance acceptable
- User testing positive
- Ready for v0.2.0 release

---

## Release Checklist

### Pre-Release

- [ ] All tests passing (80%+ coverage)
- [ ] No critical or high priority bugs
- [ ] Security audit complete
- [ ] Documentation complete
- [ ] Performance benchmarks acceptable
- [ ] User acceptance testing done

### Release Process

1. **Version bump:** Update pyproject.toml to 0.2.0
2. **Tag release:** `git tag v0.2.0`
3. **Build package:** `python -m build`
4. **Test install:** `pip install dist/gated-agent-protocol-0.2.0.tar.gz`
5. **Publish to PyPI:** `twine upload dist/*`
6. **GitHub release:** Create release with changelog
7. **Announce:** Update README, post to community

### Post-Release

- [ ] Monitor for bug reports
- [ ] Update documentation based on feedback
- [ ] Plan v0.3.0 features

---

## Success Metrics

**Quality Metrics:**
- Test coverage: ≥80%
- Critical bugs: 0
- High priority bugs: 0
- Documentation coverage: 100% of public API

**Performance Metrics:**
- `gap check status`: <100ms for typical project
- `gap scribe create`: <500ms
- `gap gate approve`: <200ms

**User Metrics:**
- Installation success rate: >95%
- First workflow completion: >80%
- User satisfaction: >4/5

---

## Risk Management

### High Risk Items

**Risk:** ACL integration breaks existing workflows  
**Mitigation:** Feature flag for ACL enforcement, gradual rollout

**Risk:** SQL ledger has production bugs  
**Mitigation:** Extensive testing, keep YAML as default

**Risk:** Breaking changes upset users  
**Mitigation:** Clear migration guide, deprecation warnings

### Contingency Plans

**If Sprint 1 overruns:**
- Defer Task 1.5 (manifest validation) to Sprint 2
- Focus on BUG-001, BUG-002, BUG-003 only

**If Sprint 2 overruns:**
- Defer Task 2.4 (full test suite) to Sprint 3
- Maintain 60% coverage minimum

**If Sprint 3 overruns:**
- Release as v0.2.0-beta
- Complete polish in v0.2.1

---

## Team Allocation

**Recommended Team:**
- 1 Senior Engineer (architecture, security)
- 1 Mid-level Engineer (implementation, testing)
- 1 Technical Writer (documentation)

**Alternative (Solo):**
- 8-10 weeks instead of 6
- Focus on critical path only

---

## Post-v0.2.0 Roadmap

**v0.3.0 (Future):**
- Visual workflow editor
- Plugin system
- Remote ledger for teams
- Rollback capability
- Proposal diffing
- ACL simulator

**v1.0.0 (Future):**
- Production hardened
- Enterprise features
- Full IDE integrations
- Compliance certifications

---

**End of Release Plan**

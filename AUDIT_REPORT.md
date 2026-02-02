# GAP (Gated Agent Protocol) - Deep Code Audit

**Date:** February 2, 2026  
**Auditor:** Kiro AI  
**Scope:** Complete codebase analysis including architecture, implementation, security model, and logic flow

---

## Executive Summary

GAP is a **security framework for autonomous AI agents** that wraps probabilistic LLMs in a deterministic state machine. The core innovation is moving agent permissions from prompt-level suggestions to kernel-level enforcement through embedded ACLs and file-system-backed state transitions.

**Architecture Status:** 🟡 **Partially Complete**
- Core state machine: ✅ Functional
- YAML ledger: ✅ Complete
- SQL ledger: 🟡 Incomplete (factory integration broken)
- Security kernel: ✅ Functional but not integrated with CLI
- Template system: ✅ Working with inheritance

---

## 1. Architecture Overview

### 1.1 The Three-Layer Model

```
┌─────────────────────────────────────────┐
│   CLI Layer (gap commands)              │
│   - check, scribe, gate, migrate        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Core Engine (state machine)           │
│   - Manifest, Ledger, PathManager       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│   Security Kernel (gated_agent)         │
│   - ACLEnforcer, Registry, Session      │
└─────────────────────────────────────────┘
```

### 1.2 State Machine Logic

The system enforces a dependency-based workflow:

1. **LOCKED**: Dependencies not met (cannot scribe)
2. **UNLOCKED**: Dependencies met, ready for agent work
3. **PENDING**: Proposal exists in `.gap/proposals/`
4. **COMPLETE**: File exists in live location + ledger entry

**Key Insight:** Status is calculated **hybrid-style** - the ledger stores metadata (approver, timestamp) but file existence is the ultimate truth source.

---

## 2. Core Components Analysis

### 2.1 Manifest System (`manifest.py`)

**Purpose:** Define protocol workflows as dependency graphs

**Schema:**
```python
class Step:
    step: str              # Unique ID
    artifact: str          # Output file path
    gate: GateType         # "manual" or "auto"
    needs: List[str]       # Dependencies
    template: Optional[str] # Template name
```

**Strengths:**
- Clean Pydantic models with validation
- Supports protocol inheritance via `extends`
- Template mapping for domain-specific terminology

**Issues:**
- ❌ No validation that `needs` references exist
- ❌ No cycle detection in dependency graph
- ❌ `template` field optional but required by scribe logic

**Recommendation:** Add manifest validation command that checks:
- All `needs` references point to valid steps
- No circular dependencies
- All steps have resolvable templates

### 2.2 State Engine (`state.py`, `ledger.py`)

**Purpose:** Track workflow progress and enforce sequencing

**The Hybrid Check Algorithm:**
```python
def get_status(manifest):
    for step in manifest.flow:
        # 1. Check dependencies (in-memory)
        deps_met = all(dep is COMPLETE for dep in step.needs)
        
        # 2. Check file system (truth source)
        is_live = (root / step.artifact).exists()
        is_proposed = (root / ".gap/proposals" / step.artifact).exists()
        
        # 3. Calculate status
        if is_live: return COMPLETE
        elif is_proposed: return PENDING
        elif deps_met: return UNLOCKED
        else: return LOCKED
```

**Strengths:**
- ✅ File system is ultimate truth (prevents ledger drift)
- ✅ Preserves metadata when available
- ✅ Clean abstraction via `Ledger` interface

**Issues:**
- ⚠️ Race condition: If file is deleted after approval, status reverts to UNLOCKED
- ⚠️ No atomic operations (file move + ledger update not transactional)
- ⚠️ Proposal detection doesn't verify proposal is for correct step

**Recommendation:**
- Add file integrity checks (checksums in ledger)
- Implement atomic gate approval (transaction-like)
- Store proposal metadata to prevent mismatches

### 2.3 SQL Ledger (`sql_ledger.py`)

**Purpose:** Alternative backend for multi-user/audit scenarios

**Schema:**
```
projects (id, name, protocol)
  └─ steps (id, project_id, name, status, approver, timestamp)
       └─ history (id, step_id, old_status, new_status, actor, timestamp)
```

**Strengths:**
- ✅ Full audit trail via `history` table
- ✅ Concurrent-safe with SQLAlchemy
- ✅ Same hybrid logic as YAML ledger

**Critical Issues:**
- ❌ **Factory integration broken** - `get_ledger()` signature mismatch
  - Factory defined as: `get_ledger(root: Path) -> Ledger`
  - Called as: `get_ledger(root, manifest)`
  - SqlLedger needs: `SqlLedger(db_url, project_name, protocol, root)`
- ❌ Factory has incomplete logic (just `pass` statement)
- ❌ Tests pass manifest but factory doesn't accept it

**Fix Required:**
```python
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

### 2.4 Scribe Engine (`scribe.py`)

**Purpose:** Generate artifacts from templates with gate-aware routing

**Flow:**
```
1. Load manifest + check state (unless --force)
2. Resolve template (local → parent protocol → package)
3. Render with Jinja2
4. Route based on gate type:
   - manual → .gap/proposals/
   - auto → live location
```

**Strengths:**
- ✅ Template inheritance via PathManager
- ✅ STDIN support for large context (JSON/YAML)
- ✅ Dry-run mode for testing
- ✅ Respects state machine (blocks if LOCKED)

**Issues:**
- ⚠️ Template resolution fallback is hardcoded for "course"/"campaign"
- ⚠️ No validation that rendered content matches expected schema
- ⚠️ Overwrites existing proposals without warning
- ❌ Doesn't extract/validate ACL blocks (security gap!)

**Security Gap:** The scribe should validate that manual-gated artifacts contain ACL blocks before writing to proposals.

### 2.5 Gate Command (`gate.py`)

**Purpose:** Approve proposals and transition state

**Flow:**
```
1. Locate proposal in .gap/proposals/
2. Move to live location (shutil.move)
3. Update ledger to COMPLETE
```

**Critical Issues:**
- ❌ **Not atomic** - if ledger update fails, file is moved but state is wrong
- ❌ No validation of artifact content before approval
- ❌ No ACL extraction/storage for next gate
- ❌ No backup of overwritten files
- ⚠️ Silent failure if proposal directory structure doesn't match

**Recommendation:**
```python
def approve(step, manifest_path):
    # 1. Validate artifact (schema, ACL block if required)
    validate_artifact(proposal_path, step_def)
    
    # 2. Backup existing file if present
    if target_path.exists():
        backup(target_path)
    
    # 3. Atomic operation
    with transaction():
        shutil.move(proposal_path, target_path)
        ledger.update_status(step, COMPLETE)
        extract_and_store_acl(target_path)  # For next gate
```

---

## 3. Security Model Analysis

### 3.1 ACL Enforcer (`security.py`)

**Purpose:** Parse embedded ACL blocks and enforce file/exec permissions

**Extraction Logic:**
```python
pattern = r"##\s+Access Control.*?\n```yaml\n(.*?)\n```"
```

**Strengths:**
- ✅ Clean regex-based extraction
- ✅ Glob pattern support via `fnmatch`
- ✅ Deny-by-default security model
- ✅ Clear error messages

**Issues:**
- ⚠️ Regex assumes triple backticks (```) but spec shows single quotes (''')
- ⚠️ No validation of YAML schema (could have typos like `allow_wrte`)
- ⚠️ Path normalization doesn't handle `../` escapes
- ❌ **Not integrated with CLI** - exists but never called!

**Critical Security Gap:**
The ACLEnforcer is a standalone module but is **never invoked** by the gap CLI commands. The security model is documented but not enforced.

**Integration Required:**
```python
# In gate.py approve():
if step_def.gate == GateType.MANUAL:
    # Extract ACL for validation
    enforcer = ACLEnforcer(content=proposal_content)
    if not enforcer.context.allowed_writes:
        warn("No ACL block found - environment will be read-only")
    
    # Store ACL for next gate's use
    store_acl(step, enforcer.context)
```

### 3.2 Session Manager (`session.py`)

**Purpose:** Track agent work sessions with artifact archiving

**Features:**
- Session-based isolation
- Artifact archiving
- Context loading for prompt injection

**Issues:**
- ❌ **Never used** - no CLI integration
- ⚠️ Session ID collision possible (timestamp-based)
- ⚠️ No session cleanup/expiry
- ⚠️ `.gap/gap.yaml` vs `.gap/status.yaml` confusion

**Status:** Appears to be from an earlier design iteration. Current implementation uses `.gap/status.yaml` directly without sessions.

### 3.3 Registry (`registry.py`)

**Purpose:** Discover and load protocol manifests

**Issues:**
- ❌ Searches for `domains/` directory that doesn't exist in codebase
- ❌ Uses different schema than `manifest.py` (GateSchema vs Step)
- ❌ Never called by CLI
- ⚠️ Appears to be for a different manifest format (gates vs flow)

**Status:** Legacy code from earlier design. Current implementation uses `load_manifest()` directly.

---

## 4. Logic Flow Analysis

### 4.1 Happy Path: Software Development

```
1. gap check status manifest.yaml
   → requirements: UNLOCKED (no deps)
   → design: LOCKED (needs requirements)

2. gap scribe create requirements
   → Renders templates/requirements.md
   → Writes to .gap/proposals/docs/requirements.md

3. gap gate list
   → Shows: docs/requirements.md

4. gap gate approve requirements
   → Moves to docs/requirements.md
   → Updates ledger: requirements = COMPLETE
   → design becomes UNLOCKED

5. Repeat for design, plan, implementation, verification
```

**Works correctly** ✅

### 4.2 Edge Case: Dependency Violation

**Scenario:** User manually creates `docs/design.md` without completing requirements

**Expected:** System should detect and warn/block

**Actual:**
```python
# In get_status():
if is_live: return COMPLETE  # File exists = complete
```

**Result:** ❌ System marks design as COMPLETE even though requirements was skipped

**Impact:** Breaks the entire state machine guarantee

**Fix Required:**
```python
if is_live:
    # Verify dependencies before marking complete
    if not all(dep is COMPLETE for dep in step.needs):
        warn(f"{step} file exists but dependencies not met")
        return UNLOCKED  # Or INVALID state
    return COMPLETE
```

### 4.3 Edge Case: File Deletion

**Scenario:** User deletes approved `docs/requirements.md`

**Expected:** System should detect drift and require re-approval

**Actual:**
```python
if is_live: return COMPLETE
elif is_proposed: return PENDING
elif deps_met: return UNLOCKED
```

**Result:** ✅ Correctly reverts to UNLOCKED (file is truth source)

**But:** Ledger still shows old approval metadata, causing confusion

**Recommendation:** Add `gap check integrity` command that detects drift

### 4.4 Edge Case: Concurrent Modifications

**Scenario:** Two users approve different proposals simultaneously

**YAML Ledger:**
- ❌ Last write wins (no locking)
- ❌ Possible corruption if YAML write interrupted

**SQL Ledger:**
- ✅ Database handles concurrency
- ✅ History table preserves both actions

**Recommendation:** Add file locking for YAML ledger or document SQL requirement for multi-user

---

## 5. Test Coverage Analysis

### 5.1 Existing Tests

**test_manifest.py:**
- ✅ Loads instructional protocol
- ✅ Loads software-engineering protocol
- ✅ Validates basic structure

**test_state.py:**
- ✅ Initial locking logic
- ⚠️ Fragile (depends on file system state)

**test_sql_ledger.py:**
- ✅ Initial state calculation
- ✅ Status updates with metadata
- ✅ Dependency unlocking
- ✅ Uses tmp_path for isolation

**test_factory_integration.py:**
- ✅ Default YAML ledger
- ❌ SQL factory test will fail (signature mismatch)

### 5.2 Missing Test Coverage

**Critical gaps:**
- ❌ No tests for `scribe create` command
- ❌ No tests for `gate approve` command
- ❌ No tests for ACLEnforcer integration
- ❌ No tests for template inheritance
- ❌ No tests for circular dependency detection
- ❌ No tests for concurrent access
- ❌ No tests for malformed manifests
- ❌ No tests for ACL block extraction
- ❌ No integration tests (end-to-end workflow)

**Recommendation:** Achieve 80%+ coverage before production use

---

## 6. Protocol Definitions Analysis

### 6.1 Instructional Protocol

**Flow:** requirements → design_course → design_section → task → verification

**Strengths:**
- ✅ Clear pedagogical progression
- ✅ Socratic method alignment
- ✅ Auto-gate for assessments (low risk)

**Issues:**
- ⚠️ No ACL blocks in templates (security model not applied)
- ⚠️ Template variables not documented

### 6.2 Software Engineering Protocol

**Flow:** requirements → design → plan → implementation → verification

**Strengths:**
- ✅ Matches industry standard SDLC
- ✅ Manual gates for critical decisions
- ✅ Traceability standard defined

**Issues:**
- ❌ Templates missing (only manifest exists)
- ❌ No ACL blocks in plan template
- ❌ `implementation` step has `gate: auto` but should require ACL

**Critical:** The software protocol is incomplete - templates don't exist

---

## 7. Documentation Quality

### 7.1 Strengths

- ✅ Excellent whitepaper explaining theory
- ✅ Clear README with quick start
- ✅ Detailed standards documents
- ✅ Integration guide for tool builders

### 7.2 Gaps

- ❌ No API documentation
- ❌ No architecture diagrams
- ❌ Template variable reference missing
- ❌ No troubleshooting guide
- ❌ Security model documented but not implemented
- ⚠️ Inconsistency between docs and code (sessions, registry)

---

## 8. Security Assessment

### 8.1 Threat Model

**Threat:** Malicious/confused agent attempts unauthorized file access

**Mitigation:** ACL-based whitelisting

**Status:** 🔴 **Not Implemented**
- ACLEnforcer exists but never called
- No integration with file I/O
- No exec command filtering

**Threat:** Agent bypasses state machine by manual file creation

**Mitigation:** Hybrid file-system checks

**Status:** 🟡 **Partially Mitigated**
- File existence checked
- But no dependency validation on existing files

**Threat:** Ledger tampering

**Mitigation:** File system as truth source

**Status:** ✅ **Mitigated**
- Ledger is metadata only
- File existence is authoritative

**Threat:** Proposal injection (malicious ACL blocks)

**Mitigation:** Human review before approval

**Status:** 🟡 **Relies on Human**
- No automated validation
- No ACL schema checking
- No dangerous pattern detection (e.g., `allow_write: ["**"]`)

### 8.2 Security Recommendations

**Priority 1 (Critical):**
1. Integrate ACLEnforcer with gate approval
2. Validate ACL blocks before approval
3. Detect dangerous patterns (wildcards, system paths)
4. Fix dependency validation for existing files

**Priority 2 (High):**
5. Add atomic operations for gate approval
6. Implement file integrity checks
7. Add audit logging for all state transitions

**Priority 3 (Medium):**
8. Add session isolation
9. Implement proposal signing/verification
10. Add rollback capability

---

## 9. Code Quality Assessment

### 9.1 Strengths

- ✅ Clean separation of concerns
- ✅ Type hints throughout
- ✅ Pydantic for validation
- ✅ Abstract interfaces (Ledger)
- ✅ Consistent naming conventions
- ✅ Good error messages

### 9.2 Issues

**Architecture:**
- ❌ Incomplete factory pattern (SQL ledger)
- ❌ Unused modules (session, registry)
- ⚠️ Two manifest schemas (gap.core vs gated_agent)

**Error Handling:**
- ⚠️ Broad exception catching (`except Exception`)
- ⚠️ Silent failures in ACL parsing
- ❌ No rollback on partial failures

**Code Duplication:**
- ⚠️ Status calculation logic duplicated (YAML vs SQL)
- ⚠️ Path resolution logic scattered

**Dependencies:**
- ✅ Minimal external deps
- ✅ No network calls (sovereignty maintained)
- ⚠️ SQLAlchemy adds significant weight

---

## 10. Critical Bugs

### 10.1 Blocker Issues

**BUG-001: Factory Signature Mismatch**
- **Severity:** 🔴 Critical
- **Impact:** SQL ledger completely broken
- **Location:** `src/gap/core/factory.py:8`
- **Fix:** Update signature to accept manifest parameter

**BUG-002: Missing Dependency Validation**
- **Severity:** 🔴 Critical  
- **Impact:** State machine can be bypassed
- **Location:** `src/gap/core/ledger.py:42`
- **Fix:** Validate dependencies before marking COMPLETE

**BUG-003: ACL Enforcer Not Integrated**
- **Severity:** 🔴 Critical
- **Impact:** Security model not enforced
- **Location:** `src/gap/commands/gate.py`
- **Fix:** Call ACLEnforcer during approval

### 10.2 High Priority Issues

**BUG-004: Non-Atomic Gate Approval**
- **Severity:** 🟠 High
- **Impact:** Inconsistent state on failure
- **Location:** `src/gap/commands/gate.py:70-86`

**BUG-005: Template Resolution Hardcoded**
- **Severity:** 🟠 High
- **Impact:** Breaks protocol extensibility
- **Location:** `src/gap/core/path.py:35-40`

**BUG-006: No Circular Dependency Detection**
- **Severity:** 🟠 High
- **Impact:** Infinite loops possible
- **Location:** `src/gap/core/manifest.py`

---

## 11. Performance Considerations

**File System Scanning:**
- Current: O(n) for each status check (n = number of steps)
- Impact: Negligible for typical workflows (<20 steps)
- Optimization: Cache file existence checks

**Template Resolution:**
- Current: Sequential search through inheritance chain
- Impact: Low (typically 1-2 lookups)
- Optimization: Build template index on manifest load

**SQL Ledger:**
- Current: One query per step in get_status()
- Impact: Could be slow for large projects
- Optimization: Single query with JOIN

**Overall:** Performance is acceptable for intended use cases

---

## 12. Recommendations

### 12.1 Immediate Actions (Before Production)

1. **Fix factory.py** - Update signature and implement SQL logic
2. **Integrate ACLEnforcer** - Call from gate approve command
3. **Add dependency validation** - Check deps before marking complete
4. **Make gate approval atomic** - Transaction-like behavior
5. **Add manifest validation** - Detect cycles, missing refs
6. **Create missing templates** - Software engineering protocol incomplete

### 12.2 Short Term (Next Release)

7. **Comprehensive test suite** - Aim for 80% coverage
8. **ACL validation** - Schema checking, dangerous pattern detection
9. **Integrity checking** - `gap check integrity` command
10. **Better error messages** - User-friendly guidance
11. **Remove dead code** - session.py, registry.py cleanup
12. **API documentation** - Sphinx or similar

### 12.3 Long Term (Future Versions)

13. **Visual workflow editor** - GUI for manifest creation
14. **Plugin system** - Custom validators, gates
15. **Remote ledger** - Shared state for teams
16. **Rollback capability** - Undo approvals
17. **Proposal diffing** - Show changes before approval
18. **ACL simulator** - Test permissions before approval

---

## 13. Conclusion

### 13.1 Overall Assessment

**Concept:** ⭐⭐⭐⭐⭐ Excellent
- Solves real problem with novel approach
- Well-documented theory
- Clear value proposition

**Implementation:** ⭐⭐⭐☆☆ Good but Incomplete
- Core state machine works
- Critical security features not integrated
- SQL backend broken
- Missing test coverage

**Production Readiness:** 🔴 Not Ready
- Critical bugs must be fixed
- Security model must be enforced
- Test coverage must improve

### 13.2 Path to Production

**Phase 1: Fix Critical Bugs (1-2 weeks)**
- Factory signature
- Dependency validation
- ACL integration

**Phase 2: Complete Implementation (2-3 weeks)**
- Missing templates
- Test suite
- ACL validation

**Phase 3: Hardening (2-3 weeks)**
- Security audit
- Performance testing
- Documentation completion

**Estimated Time to Production:** 5-8 weeks

### 13.3 Final Verdict

GAP represents an **innovative and necessary** approach to AI agent safety. The theoretical foundation is solid and the core implementation demonstrates the concept effectively. However, the gap between documentation and implementation is significant - the security model is well-designed but not enforced, and critical components are incomplete.

With focused effort on the identified issues, this could become a **production-grade framework** for safe autonomous agents. The architecture is sound and extensible. The main work is connecting the pieces that already exist.

**Recommendation:** Do not deploy to production until BUG-001, BUG-002, and BUG-003 are resolved. The current implementation provides workflow management but not the promised security guarantees.

---

**End of Audit Report**

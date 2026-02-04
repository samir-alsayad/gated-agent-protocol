# GAP v1.0 Release Plan

## Current State
- **Docs**: ✅ Canonical (Whitepaper v2, Schema Standards, Integration Guide).
- **Code**: 🟡 Sprint 1 Complete (Critical bugs fixed), but does NOT reflect new concepts.

---

## The Gap Between Docs and Code

| Concept (Docs) | Code Reality | Work Required |
|----------------|--------------|---------------|
| **Law (Project Manifest)** | `.gap/manifest.yaml` exists | ✅ Rename conceptually, minor schema update |
| **Exception (Session Config)** | `.gap/status.yaml` only | 🔴 Session folder structure not implemented |
| **Checkpoints** (`explicit`/`every`/`batch`) | Not in manifest schema | 🟠 Add `checkpoints` block to schema |
| **Phases** (Req/Des/Pol/Task/Exec) | `flow` with steps | ✅ Rename `step` → `phase` for clarity |
| **Traceability** (EARS → Props → Checks) | Not enforced | 🔴 Requires artifact parser (future) |
| **Boolean Gates** (`gate: true/false`) | Uses `gate: manual/auto` | 🟠 Update enum values |

---

## Release Tiers

### Tier 1: Minimum Viable Release (MVP)
**Goal**: Ship what works. Don't break promises.

1.  **Update Manifest Schema** (~4h)
    - Add `checkpoints.strategy` and `checkpoints.after_tasks`.
    - Change `gate: manual` → `gate: true`.
    - Validate backward compatibility.

2.  **Rename for Clarity** (~2h)
    - `step` → `phase` in code comments/docs.
    - Update CLI help text to use "Phases" language.

3.  **README Rewrite** (~2h)
    - Align with Whitepaper v2.
    - Remove SDK claims (not implemented).
    - Add "Quick Start" section.

4.  **Cleanup Dead Code** (~2h)
    - Remove `session.py`, `registry.py` (unused).

**Outcome**: A coherent, honest v0.3.0 release.

---

### Tier 2: Full Canon Compliance (v1.0)
**Goal**: Code matches all documented features.

5.  **Implement Session Model** (~8h)
    - Create `.gap/gap.yaml` (active session tracker).
    - Create `.gap/sessions/[id]/config.yaml` (exception overrides).
    - Implement `gap session create`, `gap session activate`.
    - Merge session exceptions with project manifest at runtime.

6.  **Implement Checkpoint Enforcement** (~6h)
    - Read `checkpoints.strategy` from manifest.
    - Pause execution at designated task IDs.
    - Add `gap gate continue` command.

7.  **Split Manifest into Protocol/Project** (~4h)
    - `protocols/[name]/manifest.yaml` = Protocol DNA.
    - `.gap/manifest.yaml` = Project Law (references protocol).
    - This matches `SCHEMA_PROTOCOL.md` + `SCHEMA_PROJECT.md`.

**Outcome**: Full v1.0 release matching Whitepaper.

---

### Tier 3: Advanced Features (v1.x)
**Goal**: Nice-to-haves for adoption.

8.  **Traceability Parser** (Future)
    - Parse `_Requirements: X_` from task files.
    - Validate links exist.
    - `gap check traceability` command.

9.  **ACL Schema Validation** (From Sprint 2)
    - Dangerous pattern detection.
    - `gap check acl` command.

10. **Visual Workflow Editor** (Future)
    - Web UI for manifest creation.

---

## Recommended Release Path

| Version | Contents | Timeline |
|---------|----------|----------|
| **v0.3.0** | Tier 1 (MVP) | 1 week |
| **v0.5.0** | Tier 1 + Session Model | 2 weeks |
| **v1.0.0** | Tier 1 + Tier 2 (Full) | 4 weeks |

---

## Immediate Actions

1.  [ ] Decide: Ship Tier 1 now, or wait for Tier 2?
2.  [ ] Update `pyproject.toml` version.
3.  [ ] Create `CHANGELOG.md`.
4.  [ ] Run full test suite (`pytest`).
5.  [ ] Manual end-to-end test of workflow.

---

## Questions for You

1.  **Session Model**: Is this a v1.0 requirement, or can we ship without it?
2.  **Traceability Enforcement**: Is this a "nice to have" or a "must have"?
3.  **Backward Compatibility**: Should `gate: manual` still work, or hard-switch to `gate: true`?

# GAP Requirements (Single Source of Truth)

**Last Updated:** 2026-02-03  
**Status:** Living document - this is the ONE place for requirements

---

## What GAP Actually Is

A framework for human-AI collaboration where:
1. AI proposes work (generates artifacts)
2. Human approves at gates (manual or auto)
3. Everything is traceable (audit trail)
4. Security is enforced (ACLs control what AI can do)

**Core Insight:** GAP uses itself. An AI agent uses GAP to create curriculum, get approval, then help students learn.

---

## The School Use Case (Why This Matters)

**The Vision:**
- AI agent uses GAP to create learning curriculum
- User approves each step (or sets auto-approval)
- Student works through atoms (small exercises)
- Tutor agent helps when student is stuck
- System tracks progress

**The Flow:**
```
1. Agent proposes curriculum (using GAP workflow)
   → User approves (or auto-approves)
   
2. Student reads lesson (codex.md)
   → Student does exercise
   → Student writes reflection
   
3. Tutor helps if stuck (doesn't give answers)
   
4. Student moves to next atom
```

**What Exists Now:**
- School structure (Campaign → Module → Atom)
- Manual workflow (student does everything)
- No AI agents yet
- No GAP integration yet

**What Needs to Exist:**
- AI agent can use GAP to create curriculum
- Tutor agent can help students
- GAP tracks progress through atoms
- Clear approval gates

---

## The Roles Question (Still Figuring Out)

**From SYSTEM_ARCH.md:**
- Librarian (organizes knowledge)
- Tutor (helps student)
- Critic (reviews code)
- Smith (generates blueprints)

**The Real Question:**
- Is Tutor enough for learning?
- Are other roles for different protocols (software vs instructional)?
- Do we need all 4 or is this over-engineering?

**Current Thinking:**
- Start with Tutor (helps student learn)
- See if we need more roles later
- Don't build what we don't need yet

---

## What GAP Must Do (Core Requirements)

### 1. State Machine
- Track workflow progress (LOCKED → UNLOCKED → PENDING → COMPLETE)
- Enforce dependencies (can't skip steps)
- Support both manual and auto approval gates

### 2. Security (ACL Enforcement)
- Control what AI can write
- Control what AI can execute
- Deny by default

### 3. Templates
- Generate artifacts from templates
- Support protocol inheritance
- Jinja2 rendering

### 4. Audit Trail
- Track all approvals
- Track who did what when
- Immutable history

### 5. Multiple Protocols
- Instructional (for learning)
- Software (for coding)
- Research (for experiments)
- Each protocol defines its own workflow

---

## What's Missing (Needs to Be Built)

### 1. SDK for AI Agents
**Why:** AI agents need to interact with GAP programmatically

**What:**
```python
from gap.sdk import GAPClient

client = GAPClient(project_root=".")
client.scribe("requirements")  # Generate artifact
client.approve("requirements")  # Approve step
status = client.get_status()   # Check progress
```

### 2. Agent Integration
**Why:** School needs AI agents to create curriculum and help students

**What:**
- Agent can propose curriculum steps
- Agent can read student reflections
- Agent can provide hints (not answers)
- Agent respects ACL restrictions

### 3. Validation Framework (Maybe)
**Why:** Might need to validate reflections, code quality, etc.

**What:**
- Pluggable validators
- Protocol-specific validation rules
- Not sure if this is needed yet

---

## What's Working (Don't Break)

- CLI commands (gap check, gap scribe, gap gate)
- State machine logic
- ACL enforcement
- YAML ledger
- SQL ledger (optional)
- Template system
- 15 tests passing

---

## The Refactoring Plan (High Level)

### Phase 1: Clean Up
- Merge gated_agent into gap (single package)
- Remove dead code
- Fix architecture confusion
- Keep tests passing

### Phase 2: Build SDK
- Create gap.sdk module
- Simple API for AI agents
- Document with examples
- Test with School use case

### Phase 3: School Integration
- Connect School to GAP
- Build Tutor agent
- Prove the concept works
- See what else is needed

### Phase 4: Polish
- Documentation
- Examples
- Release v0.2.0

---

## Open Questions (Need Answers)

1. **Roles:** Do we need all 4 roles or just Tutor?
2. **Validation:** Do we need automated validation or is manual approval enough?
3. **Progress Tracking:** Do we need a dashboard or is CLI status enough?
4. **Portfolio:** Do we need export/showcase features or is git history enough?

**Decision:** Don't build until we know we need it.

---

## Documentation Strategy (How to Not Repeat This Mess)

### Keep:
- `REQUIREMENTS.md` (this file) - single source of truth
- `AUDIT_REPORT.md` - what's broken
- `ARCHITECTURE.md` - how it works
- Code comments - implementation details

### Archive:
- All the conflicting vision/decision/use-case docs
- Move to `.archive/docs/`
- Keep for reference but not authoritative

### Rule:
- If it's not in REQUIREMENTS.md, it's not a requirement
- If it's not in code, it doesn't exist
- If it's aspirational, mark it clearly as "Future"

---

## Next Steps

1. Archive conflicting docs
2. Fix critical bugs (already done)
3. Start Phase 1 refactoring
4. Build SDK (Phase 2)
5. Test with School (Phase 3)

**Focus:** Make GAP work for School. That's the killer use case. Build what's needed, nothing more.

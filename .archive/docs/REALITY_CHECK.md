# Reality Check: What Actually Exists vs What's Aspirational

## Purpose
This document separates **signal** (what exists) from **noise** (what's been hallucinated or is aspirational) based on actual source files.

---

## 1. The School of First Principles (REAL)

### What Actually Exists ✅

**Structure:**
- Campaign → Module → Atom hierarchy (real, in use)
- Example: `domains/computing/campaigns/05_sovereign_user/modules/04_local_anchoring/01_binary_discovery/`

**Files in Each Atom:**
- `codex.md` - The lesson (real, written by human)
- `reflection.md` - Student's learning proof (real, written by student)
- `discovery.sh` - Student's work (real, written by student)

**The Learning Flow (REAL):**
1. Student reads codex.md
2. Student does the exercise (writes code, runs commands)
3. Student writes reflection.md (what they learned, what confused them)
4. Student moves to next atom

**manifest.yaml (REAL):**
```yaml
extends:
  - protocol: instructional
    role: librarian
    scope: /
  - protocol: software
    role: smith
    scope: /domains/computing
```

**SYSTEM_ARCH.md mentions 4 roles:**
- Librarian (archivist)
- Tutor (instructor)
- Critic (reviewer)
- Smith (drafter)

---

## 2. What's Hallucinated/Aspirational ❌

### AI Agent Roles (NOT IMPLEMENTED)

**The Document Says:**
- "Librarian organizes knowledge, maps prerequisites"
- "Tutor provides Socratic guidance, validates reflections"
- "Critic reviews code, checks security"
- "Smith generates initial blueprints"

**The Reality:**
- No AI agents are actually running
- No code exists for Librarian, Tutor, Critic, or Smith
- These are ASPIRATIONAL roles, not implemented features
- The student is doing everything manually right now

### Automated Validation (NOT IMPLEMENTED)

**The Document Says:**
- "AI Tutor validates reflection (Socratic questioning)"
- "If validated → Move to next atom"
- "If gaps found → Tutor guides deeper"

**The Reality:**
- No automated validation exists
- No Socratic questioning system
- Student manually decides when to move on
- No AI is reading or validating reflections

### GAP Integration (NOT IMPLEMENTED)

**The Document Says:**
- "gap scribe create atom_binary_discovery"
- "gap gate approve atom_binary_discovery"
- "AI Tutor reads reflection.md and validates"

**The Reality:**
- GAP is not integrated with School yet
- No commands are being run
- No state machine tracking atom progress
- This is all PLANNED, not REAL

### Security Enforcement (NOT IMPLEMENTED)

**The Document Says:**
- "Zero-Execution: AI agents CANNOT run shell commands"
- "Reflective Locking: Progress requires human-written reflection"
- "ACL blocks prevent AI from doing the work"

**The Reality:**
- No AI agents exist to block
- No ACL enforcement is running
- Student is just working through atoms manually
- Security model is DESIGNED but not DEPLOYED

### Missing Features (ACKNOWLEDGED)

**The Document Correctly Identifies:**
- ❌ AI Agent Integration
- ❌ Reflection Validation
- ❌ Progress Tracking
- ❌ Portfolio Generation

**These are honest gaps, not hallucinations.**

---

## 3. What's Real About GAP

### Currently Working ✅

**Core Engine:**
- State machine (LOCKED → UNLOCKED → PENDING → COMPLETE)
- YAML ledger (`.gap/status.yaml`)
- SQL ledger (optional)
- ACL enforcement (`ACLEnforcer` class exists)
- Template system (Jinja2)

**CLI Commands:**
- `gap check status` - Show workflow status
- `gap check manifest` - Validate manifest
- `gap scribe create` - Generate artifact from template
- `gap gate approve` - Approve proposal

**Protocols:**
- `instructional` protocol exists (manifest.yaml + templates)
- `software-engineering` protocol exists (manifest.yaml + templates)

**Tests:**
- 15 tests passing
- Core functionality validated

### What's Missing ❌

**SDK for AI Agents:**
- No `gap.sdk` module exists
- No `GAPClient` class
- No way for AI to interact with GAP programmatically

**Reflection Validator:**
- No validation framework
- No Socratic questioning
- No gap detection

**Progress Dashboard:**
- No `gap show progress` command
- No visual tracking

**Portfolio Export:**
- No `gap export portfolio` command
- No showcase generation

---

## 4. The Real Question: What Roles Are Actually Needed?

### From SYSTEM_ARCH.md

**The 4 Roles:**
1. **Librarian** (archivist) - "Memory linkage & Prerequisite mapping"
2. **Tutor** (instructor) - "Socratic guidance & Reflective Gate validation"
3. **Critic** (reviewer) - "Foundry code audit & security checking"
4. **Smith** (drafter) - "Initial blueprint generation (MD-only)"

### The Real Workflow (What Student Actually Does)

1. Read codex.md (the lesson)
2. Do the exercise (write code, run commands)
3. Write reflection.md (what you learned)
4. Get help if stuck (ask questions)
5. Move to next atom

### The Question

**Which roles are actually needed for THIS workflow?**

**Tutor (instructor):**
- Helps when student is stuck
- Answers questions about the lesson
- Provides hints without giving answers
- **NEEDED** ✅

**Librarian (archivist):**
- Maps prerequisites
- Organizes knowledge
- **MAYBE NOT NEEDED?** The curriculum structure already handles this
- Atoms are already in order (01, 02, 03...)
- Dependencies are implicit in the sequence

**Critic (reviewer):**
- Reviews code
- Checks security
- **FOR WHAT?** This is learning, not production code
- Maybe this is for the "Foundry" (building actual projects)?
- Maybe this is for the SOFTWARE protocol, not INSTRUCTIONAL?

**Smith (drafter):**
- Generates initial blueprints
- **FOR WHAT?** The codex already exists
- Maybe this is for generating NEW atoms?
- Maybe this is for the SOFTWARE protocol?

### Hypothesis

**For the INSTRUCTIONAL protocol (School):**
- **Tutor** is the main role (helps student learn)
- **Librarian** might be redundant (structure handles prerequisites)
- **Critic** and **Smith** might be for OTHER protocols

**For the SOFTWARE protocol (building projects):**
- **Smith** generates initial code/design
- **Critic** reviews code quality
- **Librarian** might organize documentation
- **Tutor** might not be needed

### The Real Design Question

**Should each protocol define its own roles?**

```yaml
# instructional protocol
roles:
  - tutor: "Helps student learn, validates understanding"

# software protocol
roles:
  - smith: "Generates initial code"
  - critic: "Reviews code quality"
  - librarian: "Organizes documentation"
```

**Or are these universal roles that apply differently per protocol?**

---

## 5. What Should Actually Be Built

### For School to Work (Minimum Viable)

**1. Tutor Agent Integration**
- AI that can read reflection.md
- AI that can ask clarifying questions
- AI that can provide hints (not answers)
- AI that validates understanding

**2. Basic Progress Tracking**
- Track which atoms are complete
- Show what's next
- Simple status view

**3. GAP Integration**
- Use GAP state machine for atom progression
- Use GAP templates for codex/reflection
- Use GAP ACLs to prevent AI from doing the work

### For GAP to Support School (Minimum Viable)

**1. SDK for AI Agents**
- Simple API to read artifacts
- Simple API to check status
- Simple API to provide feedback
- Role-based permissions

**2. Validation Framework**
- Pluggable validators
- Reflection validator as example
- Gap detection
- Hint generation

**3. Multi-Protocol Support**
- Keep instructional protocol
- Keep software protocol
- Each defines its own workflow
- Shared core engine

---

## 6. The Truth About the Refactoring

### What the Refactor Plan Says

**Goals:**
- Clean architecture
- Production readiness
- Clear integration path
- Consistent protocols
- Documentation accuracy

**These are all CORRECT** ✅

### What the Refactor Plan Misses

**The School Use Case:**
- Refactor plan focuses on "AI coding safety"
- School is about "AI learning guidance"
- These are DIFFERENT use cases
- Both need GAP, but for different reasons

**The SDK Priority:**
- Refactor plan mentions SDK
- But doesn't prioritize it
- School NEEDS the SDK to work
- SDK should be Phase 1, not Phase 3

**The Validation Framework:**
- Refactor plan doesn't mention it
- School NEEDS validation
- This should be added to the plan

### What Should Change

**1. Clarify the Vision**
- GAP is for human-AI collaboration
- Multiple use cases (learning, coding, research)
- Each use case is a protocol
- Core engine is universal

**2. Prioritize the SDK**
- Make it real, not aspirational
- Simple, clean API
- Well-documented
- Example integrations

**3. Add Validation Framework**
- Pluggable validators
- Reflection validator for instructional
- Code validator for software
- Extensible for new protocols

**4. Keep Multiple Protocols**
- Don't simplify to single use case
- Each protocol is valuable
- Shared core, different workflows

---

## 7. Next Steps

### Immediate Questions for User

**1. Which roles are actually needed for School?**
- Just Tutor?
- Tutor + Librarian?
- All 4 roles?
- Different roles per protocol?

**2. What should the Tutor actually do?**
- Answer questions when stuck?
- Validate reflections?
- Provide hints?
- All of the above?

**3. Should GAP integration happen now or later?**
- Build School first, integrate GAP later?
- Integrate GAP now, build on top of it?
- Parallel development?

### After Clarification

**1. Update USE_CASE_SCHOOL.md**
- Remove hallucinations
- Keep only what's real or clearly marked as planned
- Simplify language
- Focus on actual workflow

**2. Update Refactor Plan**
- Add SDK as priority
- Add validation framework
- Keep multi-protocol support
- Align with School use case

**3. Create Implementation Plan**
- Phase 1: Core refactor (clean architecture)
- Phase 2: SDK + validation (enable School)
- Phase 3: School integration (prove it works)
- Phase 4: Documentation + examples (make it usable)

---

## Conclusion

**What's Real:**
- School structure (Campaign → Module → Atom)
- Student workflow (read → do → reflect → move on)
- GAP core engine (state machine, ACLs, templates)
- Instructional protocol (manifest + templates)

**What's Aspirational:**
- AI agent roles (Librarian, Tutor, Critic, Smith)
- Automated validation
- GAP integration with School
- Progress tracking
- Portfolio generation

**What's Unclear:**
- Which roles are actually needed?
- What should each role do?
- Should roles be protocol-specific or universal?

**What's Next:**
- User clarifies role requirements
- Update docs to remove hallucinations
- Update refactor plan to support School
- Build the SDK and validation framework

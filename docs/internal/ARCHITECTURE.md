# GAP Architecture: Two-Package Design

## The Confusion

The codebase has **two separate packages** in `src/`:
1. `gap/` - The CLI tool and workflow engine
2. `gated_agent/` - The security kernel and SDK

This creates confusion because:
- Only `gap` is configured in `pyproject.toml` as the main package
- `gated_agent` appears to be a separate package but shares the same repo
- The naming suggests `gated_agent` is the parent, but `gap` is what users install

## Current State Analysis

### Package 1: `gap` (The CLI Tool)
**Location:** `src/gap/`  
**Entry Point:** `gap` command  
**Purpose:** User-facing workflow management

**Structure:**
```
gap/
├── commands/          # CLI commands (check, scribe, gate, migrate)
├── core/             # State machine, ledger, manifest parsing
├── protocols/        # Built-in protocol definitions
└── main.py          # CLI entry point
```

**What it does:**
- Provides `gap check status`, `gap scribe create`, `gap gate approve` commands
- Manages state machine and workflow progression
- Reads/writes `.gap/status.yaml` ledger
- Handles template rendering and file operations

### Package 2: `gated_agent` (The Security SDK)
**Location:** `src/gated_agent/`  
**Entry Point:** None (library only)  
**Purpose:** Security enforcement for tool harnesses

**Structure:**
```
gated_agent/
├── security.py       # ACLEnforcer (used by gap)
├── registry.py       # Protocol discovery (NOT used)
├── session.py        # Session management (NOT used)
└── cli.py           # Validation CLI (NOT used)
```

**What it's supposed to do (per README):**
- Provide security primitives for IDE integrations
- Allow external tools to enforce GAP constraints
- Registry for protocol discovery

**What it actually does:**
- Only `security.py` (ACLEnforcer) is used by `gap/commands/gate.py`
- Everything else is dead code

## The Design Intent (From Documentation)

Based on the whitepaper and integration guide, the intended architecture was:

```
┌─────────────────────────────────────────────┐
│  IDE / Tool Harness (Cursor, VSCode, etc.)  │
│  - Imports gated_agent SDK                  │
│  - Enforces ACLs at runtime                 │
│  - Restricts agent file access              │
└──────────────┬──────────────────────────────┘
               │ uses
               ▼
┌─────────────────────────────────────────────┐
│  gated_agent (Security Kernel)              │
│  - ACLEnforcer                              │
│  - Registry                                 │
│  - Session Manager                          │
└──────────────┬──────────────────────────────┘
               │ used by
               ▼
┌─────────────────────────────────────────────┐
│  gap (CLI Tool)                             │
│  - Workflow management                      │
│  - State machine                            │
│  - Template rendering                       │
└─────────────────────────────────────────────┘
```

**The idea:** 
- `gap` is the standalone CLI for humans
- `gated_agent` is the SDK for tool builders
- IDEs import `gated_agent` to enforce security at runtime

## The Reality

**What actually happens:**
1. Users install `gated-agent-protocol` package
2. They get the `gap` CLI command
3. `gap` internally imports `ACLEnforcer` from `gated_agent`
4. No external tools actually use `gated_agent` SDK (it's not documented how)

**Problems:**
1. **Package naming mismatch:** PyPI package is `gated-agent-protocol` but the CLI is `gap`
2. **Dead code:** `registry.py`, `session.py`, `cli.py` are unused
3. **Incomplete SDK:** No clear API for tool builders to use
4. **Confusing structure:** Two packages in one repo with unclear boundaries

## Recommendations

### Option 1: Merge Into Single Package (Recommended)
**Rationale:** The SDK isn't being used externally, and the separation adds complexity

**Changes:**
```
src/gap/
├── commands/          # CLI commands
├── core/             # State machine, ledger, manifest
├── security/         # Move gated_agent/security.py here
├── protocols/        # Protocol definitions
└── main.py
```

**Benefits:**
- Simpler architecture
- Clear single package
- Remove dead code
- Easier to maintain

**Migration:**
```bash
mv src/gated_agent/security.py src/gap/core/security.py
rm -rf src/gated_agent/  # Remove dead code
# Update imports in gate.py
```

### Option 2: Properly Separate Packages
**Rationale:** Keep the SDK vision but implement it correctly

**Changes:**
1. Make `gated_agent` a proper standalone package
2. Publish it separately to PyPI as `gated-agent-sdk`
3. Make `gap` depend on `gated-agent-sdk`
4. Document the SDK API for tool builders
5. Remove dead code or implement missing features

**Structure:**
```
packages/
├── gated-agent-sdk/     # Separate repo/package
│   ├── security.py      # ACL enforcement
│   ├── types.py         # Shared types
│   └── __init__.py
│
└── gap/                 # Main package
    ├── commands/
    ├── core/
    └── main.py
```

**Benefits:**
- Clean separation of concerns
- SDK can be versioned independently
- Tool builders have clear integration path
- Follows Python packaging best practices

### Option 3: Keep Current But Clean Up
**Rationale:** Minimal changes, just remove confusion

**Changes:**
1. Delete unused files: `registry.py`, `session.py`, `cli.py`
2. Rename `gated_agent` → `gap.security` (move into gap package)
3. Update documentation to reflect reality
4. Remove SDK claims from README

**Benefits:**
- Minimal code changes
- Removes dead code
- Honest about what the package does

## My Recommendation

**Go with Option 1: Merge Into Single Package**

**Why:**
1. The SDK isn't being used by external tools (no evidence in docs or examples)
2. Only `ACLEnforcer` is actually used, and only by `gap` itself
3. The "two package" design adds complexity without benefit
4. Simpler to maintain and understand
5. Can always extract SDK later if needed

**Implementation:**
```bash
# 1. Move security module
mv src/gated_agent/security.py src/gap/core/security.py

# 2. Update import in gate.py
# from gated_agent.security import ACLEnforcer
# to
# from gap.core.security import ACLEnforcer

# 3. Remove dead code
rm -rf src/gated_agent/

# 4. Update pyproject.toml if needed
# (already only packages gap)

# 5. Update documentation
```

## Current Usage

The only place `gated_agent` is used:

```python
# src/gap/commands/gate.py
from gated_agent.security import ACLEnforcer

# Used during approval to extract ACL blocks
enforcer = ACLEnforcer(content=content)
```

That's it. Everything else in `gated_agent/` is unused.

## Conclusion

The two-package structure was an architectural vision that was never fully implemented. The SDK components (`registry.py`, `session.py`) don't work with the current manifest format and aren't used anywhere.

**Recommendation:** Merge `gated_agent` into `gap` as a submodule, remove dead code, and simplify the architecture. If external tool integration becomes a priority later, we can extract a proper SDK at that time.

---

**Status:** Architectural debt identified  
**Impact:** Medium (confusing but not breaking)  
**Priority:** Should be addressed in Sprint 2 or 3

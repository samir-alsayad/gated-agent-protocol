# GAP CLI Reference

The `gap` command line interface is the primary way to interact with the Gated Agent Protocol.

## Commands

### `gap check status`
Validates the status of a project against its manifest.

```bash
gap check status manifest.yaml
```

**Output:**
```
🔍 Protocol: software-engineering (Version: 0.1.0)
----------------------------------------
🟢 requirements: unlocked
🔒 design: locked
🔒 plan: locked
```

Status indicators:
- 🟢 `unlocked` — Ready to scribe
- 🔒 `locked` — Dependencies not met
- ⏳ `pending` — Proposal waiting for approval
- ✅ `complete` — Approved and live
- ⚠️ `invalid` — File exists but dependencies not met (state machine bypassed)

---

### `gap scribe create`
Generates artifacts from templates.

```bash
gap scribe create requirements --manifest manifest.yaml
```

Options:
- `--dry-run`: Print output to stdout instead of writing file
- `--data KEY=VALUE`: Pass custom data to the template

**Behavior:**
- If `gate: true` → Writes to `.gap/proposals/`
- If `gate: false` → Writes directly to live artifact

---

### `gap gate list`
Lists all pending proposals waiting for approval.

```bash
gap gate list --manifest manifest.yaml
```

---

### `gap gate approve`
Approves a proposal and moves it to the live artifact.

```bash
gap gate approve requirements --manifest manifest.yaml
```

**What happens:**
1. Validates the proposal exists
2. Extracts ACL from the artifact (if present)
3. Moves file from `.gap/proposals/` → live location
4. Updates `.gap/status.yaml` ledger
5. Stores ACL in `.gap/acls/` for next phase

---

### `gap migrate`
Migrates state from YAML ledger to SQL ledger.

```bash
gap migrate yaml-to-sql --manifest manifest.yaml
```

Requires `GAP_DB_URL` environment variable.

---

## Planned Commands (v1.1+)

These commands are documented but not yet implemented:

- `gap init` — Initialize a new project from a protocol
- `gap log` — Display the immutable ledger history
- `gap inspect` — Review pending proposals with ACL extraction

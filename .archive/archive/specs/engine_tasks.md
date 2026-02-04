# Tasks: GAP Engine Implementation

## 0. Build System & Setup
- [ ] **0.1** Initialize `src/` Layout
    - Create `pyproject.toml` (poetry/uv).
    - Create `src/gap/__init__.py`.
    - Create `tests/` directory.

## 1. Core Logic (The Brain)
- [ ] **1.1** Implement `GapManifest` (Pydantic)
    - Define `Step`, `ProtocolRef`, `GapManifest` models.
    - **Test**: `tests/core/test_manifest.py` (Validates Prop 1).
- [ ] **1.2** Implement `StateEngine`
    - Implement `GapStatus` model (reads `.gap/status.yaml`).
    - Logic for `LOCKED` vs `UNLOCKED`.
    - **Test**: `tests/core/test_state.py` (Validates Prop 2).
- [ ] **1.3** Implement `PathManager`
    - Safe path resolution and sanitization.
    - **Inheritance Logic**: Implement `resolve_template` (Project -> Parent).
    - **Test**: `tests/core/test_path.py` (Verify multi-level lookups).

## 2. The Validator (`gap check`)
- [ ] **2.1** Implement `check` command (Typer)
    - Wire up `GapManifest` validation.
    - Implement `--json` output flag.
- [ ] **2.2** Verify Deep Dependency Checks
    - Ensure `extends: [protocol]` actually checks `protocols/`.
    - **Test**: `tests/commands/test_check.py` (Validates Prop 5).

## 3. The Scribe (`gap scribe`)
- [ ] **3.1** Implement Template Engine
    - Jinja2 integration.
    - STDIN JSON parsing.
- [ ] **3.2** Implement Safe Writer
    - Logic: If Manual -> `.gap/proposals/`.
    - Logic: If Auto -> Target.
    - **Test**: `tests/commands/test_scribe.py` (Validates Prop 3, 4).

## 4. The Gate (`gap gate`)
- [ ] **4.1** Implement `gate list`
    - Scan `.gap/proposals/`.
- [ ] **4.2** Implement `gate approve`
    - Atomic Move logic.
    - Ledger append logic.
    - **Test**: `tests/commands/test_gate.py`.

## 5. Integration
- [ ] **5.1** OpenCode Interop Test
    - Verify `--json` output matches schema.
    - Verify STDIN input works for large context.

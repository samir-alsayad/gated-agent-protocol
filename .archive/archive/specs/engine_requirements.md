# Requirements: GAP Engine (The Tool)

This document defines the functional requirements for the Gated Agent Protocol (GAP) Engine, the sovereign CLI tool that enforces protocol compliance and enables safe agentic workflows.

## Functional Requirements

### 1. Verification & Validation (`gap check`)
**Problem:** Users and Agents can easily misconfigure `manifest.yaml`, break dependency contracts, or misplace files, leading to silent failures.

**Solution:**
*   Strict Schema Validation for `manifest.yaml` (Project & Protocol) using Pydantic.
*   Deep Dependency Checking (Verify `extends` points to real protocols).
*   Term Mapping Verification (Ensure "Campaign" maps to existing template).
*   Path Integrity Check (Verify file existence against manifest).

**Components:** `Validator`, `ManifestParser`, `PathManager`

**Properties:** 1-4

---

### 2. The Scribe Engine (`gap scribe`)
**Problem:** Agents hallucinate filenames, formats, or overwrite live files. Manual file creation is tedious and error-prone.

**Solution:**
*   Template-based generation (Jinja2).
*   **Inheritance Resolution**: Automatically resolves templates from Parent Protocols if missing locally (Project -> Protocol -> Libraries).
*   STDIN input for large context (JSON).
*   **Safe-Write Mode**: Writes to `.gap/proposals/` if Gate is `manual`.
*   **Direct-Write Mode**: Writes to Target if Gate is `auto`.

**Components:** `Scribe`, `TemplateEngine`, `InputHandler`

**Properties:** 5-8

---

### 3. State Machine & Gating (`gap gate`)
**Problem:** No enforcement of the "Sequence". Users can skip "Design" and go straight to "Execution". FS scanning is slow and lacks metadata (Who approved it? When?).

**Solution:**
*   **State Persistence**: Store transition history in `.gap/status.yaml` (The Ledger).
*   **Desync Detection**: Verify Ledger against File System (Trust but Verify).
*   Atomic transition from `proposals/` -> `live/` (The Gate).
*   Dual Gate Logic (`auto` vs `manual`).

**Components:** `StateEngine`, `Ledger`, `GateKeeper`

**Properties:** 9-12

---

### 4. Interoperability (The Client Interface)
**Problem:** External tools (OpenCode, Aider) struggle to parse human-readable CLI output/errors, making integration brittle.

**Solution:**
*   `--json` flag for all outputs providing structured status and errors.
*   Standard POSIX exit codes (0=Success, 1=Error).
*   Python Library API (`import gap.core`) for direct integration without subprocess.

**Components:** `CLIInterface`, `JSONFormatter`

**Properties:** 13-15

---

### 5. Constraint Checklist
**Problem:** Tools often bloat with unnecessary dependencies or call home, violating Sovereignty.

**Solution:**
*   **Zero Network**: The Engine must not make external network requests.
*   **Manifest Truth**: Configuration is *only* read from `manifest.yaml` files.
*   **Stateless**: The Engine processes the current state of files; no hidden DB.

**Components:** `ConstraintEnforcer`

**Properties:** 16-18

# Standard: Access Control List (ACL) Specification
**Version 1.0 (Embedded Blocks)**

## 1. Objective
To enforce **Plan-Derived Access Control**, every artifact that acts as a "Gate Pillar" (e.g., `plan.md`, `diagnosis.md`) MUST contain an embedded, machine-readable Access Control List.

## 2. The Logic of Containment
1.  **Context (Read)**: Agents have open read access to the workspace (to support Embeddings/RAG).
2.  **Action (Write)**: Write access is **Denied by Default**.
3.  **Escalation**: To bypass the lock, the Agent must specify an `Access Control` block.

## 3. The Spec Block
The implementation uses a standard Markdown Section `## Access Control` containing a standard YAML Code Block.

### Schema
```markdown
## Access Control
'''yaml
# 1. Write Whitelist (Required for mutation)
allow_write:
  - "src/target_file.py"
  - "tests/target_test.py"
  - "docs/updates/**"

# 2. Exec Whitelist (Required for shell commands)
allow_exec:
  - "pytest tests/"
  - "npm run build"
'''
```

### Constraints
- **Case Sensitive**: Paths are case sensitive on Linux.
- **Globs**: simple shell globs (`*`, `**`) are supported via `fnmatch`.
- **Precedence**: An explicit `allow_write` overrides the default deny.

## 4. The Harness Responsibility
The GAP Tool Harness MUST:
1.  Scan the approved artifact for `## Access Control`.
2.  Extract the YAML content.
3.  Inject these rules into the Proxy File System.
4.  **REJECT** any I/O operation that does not match the whitelist.

## 5. Security Posture
- If the block is **Missing**: The environment is Read-Only.
- If the block is **Empty**: The environment is Read-Only.
- If the block contains **Wildcards (`**`)**: The user should be warned "High Risk" before approving.

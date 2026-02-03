# Standard: Access Control List (ACL) Specification
**Version 1.0 (Embedded Blocks)**

## 1. Objective
To enforce **Plan-Derived Access Control**. 
The ACL is not a separate decision; it is the **technical derivation** of the Task Decision.

## 2. The Logic of Derivation
1.  **Input**: Approved Task (e.g., "Edit `src/main.py`").
2.  **Derivation**: The Agent proposes the specific ACL block required to execute that Task.
3.  **Approval**: When the User approves the Task, they implicitly approve the **Minimum Necessary ACL** to perform it.
4.  **Enforcement**: The Harness enforces the ACL during the Execution Phase.


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

# Archived ACL Logic & Templates

This file contains the Access Control List (ACL) logic and template sections removed from the Gated Agent Protocol (GAP) core in March 2026.

## 1. Core Models (src/gap/core/models.py)

```python
class FilesystemACL(BaseModel):
    write: List[str] = Field(default_factory=list)
    read: List[str] = Field(default_factory=list)

class ACLDefinition(BaseModel):
    filesystem: FilesystemACL = Field(default_factory=FilesystemACL)
    shell: List[str] = Field(default_factory=list)
    tools: Dict[str, List[str]] = Field(default_factory=dict) # allowed/blocked tools

# From PlanEnvelope:
class PlanEnvelope(BaseModel):
    acl: ACLDefinition = Field(default_factory=ACLDefinition)
```

## 2. Task Template (task.md)

```markdown
## 1. Access Control (ACL)
*Automatically derived from approved tasks. The Harness will enforce this.*

```yaml
allow_write: [{{ allowed_paths }}]
allow_exec: [{{ allowed_commands }}]
```
```

## 3. Plan Template (plan.md)

```markdown
## 4. Final Execution Envelope (ACL)
*Automatically derived from approved tasks and enforced by the Harness.*

```yaml
allow_write: [{{ allowed_paths }}]
allow_exec: [{{ allowed_commands }}]
```
```

## 4. Machine-Readable Tasks (tasks.yaml)

```yaml
# From Task objects:
outputs: ["src/path/to/file.py"]
```

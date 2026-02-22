# GAP `src/core` Code Walkthrough

This document contains a block-by-block explanation of every Python file in `src/gap/core/`.
You can review the actual code and read the plain English explanations above each block. 
If you want to delete a file or change a block, just leave a comment here!

---

## 1. `state.py`
This file defines the basic "vocabulary" of the GAP state machine.

```python
from enum import Enum
from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel
import yaml

from gap.core.manifest import GapManifest
```
**Explanation:** Imports necessary standard libraries and Pydantic (used for creating strict data schemas).

```python
class StepStatus(str, Enum):
    # This defines the 5 possible states any step (like 'design' or 'implementation') can be in.
    LOCKED = "locked"       # The previous steps aren't finished yet.
    UNLOCKED = "unlocked"   # Previous steps are done, ready for the agent to write a proposal.
    PENDING = "pending"     # The agent wrote a proposal (in .gap/proposals), waiting for human approval.
    COMPLETE = "complete"   # Human approved it, it is now live code.
    INVALID = "invalid"     # Code exists, but the ledger says the previous step isn't done! Someone bypassed GAP.
```
```python
class StepData(BaseModel):
    # A tiny data box to hold the status of a step, PLUS metadata about when it was approved and by who.
    status: StepStatus
    timestamp: Optional[str] = None
    approver: Optional[str] = None
```
```python
class GapStatus(BaseModel):
    # A dictionary mapping step names (e.g. "design") to their StepData (e.g. {status: complete, approver: samir}).
    steps: Dict[str, StepData] = {} 
```

---

## 2. `models.py`
This file defines the strict data schemas for the new Phase 1 Plan Layer.

```python
from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field

# --- Task Models ---

class Task(BaseModel):
    """
    A logical work unit (Proposed Change Unit).
    Purely describes necessity, without execution context.
    """
    id: str
    description: str
    # 'traces_to' ensures this task is legally linked to a known Design Property ID.
    traces_to: Optional[str] = None
    # 'outputs' specifies exactly what files this task intends to modify.
    outputs: List[str] = Field(default_factory=list)

class TaskList(BaseModel):
    """Schema for parsing the .gap/tasks.yaml file into Python objects."""
    tasks: List[Task] = Field(default_factory=list)
```
```python
# --- Plan Models ---

class FilesystemACL(BaseModel):
    # What absolute/relative paths is the agent allowed to write or read?
    write: List[str] = Field(default_factory=list)
    read: List[str] = Field(default_factory=list)

class ACLDefinition(BaseModel):
    filesystem: FilesystemACL = Field(default_factory=FilesystemACL)
    # What shell commands can it execute? (e.g. ['pytest'])
    shell: List[str] = Field(default_factory=list)
    # What tools from the Runner framework can it use?
    tools: Dict[str, List[str]] = Field(default_factory=dict)
```
```python
class CognitionDefinition(BaseModel):
    # Where does the agent run, and what model powers it for this specific task?
    execution: Literal['local', 'cloud'] = 'local'
    model: str
    temperature: Optional[float] = None

class PlanEnvelope(BaseModel):
    """
    The execution authorization for a single Task. 
    It combines ACLs, Cognition, and Checkpoints into one single rulebook.
    """
    acl: ACLDefinition = Field(default_factory=ACLDefinition)
    cognition: CognitionDefinition
    # Checkpoints: When must the runner pause and ask for human permission? (e.g. 'after_completion')
    checkpoints: List[str] = Field(default_factory=list)

class Plan(BaseModel):
    """Schema for parsing the entire .gap/plan.yaml file."""
    # A dictionary bridging the Task ID ("T-1") to its specific PlanEnvelope rulebook.
    plan: Dict[str, PlanEnvelope] = Field(default_factory=dict)
```

---

## 3. `scope_manifest.py`
This extracts the `ACL` blocks out of files so that `gap check` can print them. It parses YAML embedded in Markdown.

```python
from pathlib import Path
import re
import yaml
from typing import List, Optional

class ACLContext:
    # A raw data holder for write and execute permissions.
    def __init__(self):
        self.allowed_writes: List[str] = []
        self.allowed_execs: List[str] = []
```
```python
class ScopeParser:
    """
    Extracts the YAML block under 'ACL' or 'Access Control' headings in a markdown file.
    Note: It does not ENFORCE security, it just READS the requested permissions.
    """
    def __init__(self, content: str = ""):
        self.context = ACLContext()
        if content:
            self.parse_from_content(content)

    def parse_from_content(self, content: str):
        # Regex to find ```yaml blocks that are directly beneath an ACL heading.
        pattern = r"(?:##|###) (?:Access Control|ACL|Governance)\s+```yaml\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            yaml_str = match.group(1)
            try:
                # Turn the yaml string into python lists
                data = yaml.safe_load(yaml_str)
                if data:
                    self.context.allowed_writes = data.get('allow_write', [])
                    self.context.allowed_execs = data.get('allow_exec', [])
            except Exception:
                pass # If it crashes, it just silently ignores it.

    @staticmethod
    def extract_from_file(path: Path) -> 'ScopeParser':
        # Convenience method to open a file and parse it.
        if not path.exists():
            return ScopeParser()
        return ScopeParser(path.read_text())
```
**(Verdict question: Now that we strictly use `plan.yaml` instead of embedded markdown ACL blocks, this file is completely obsolete! I mark this as an AI hallucination. Do you want to DELETE it?)**

---

## 4. `manifest.py`
This parses the main `manifest.yaml` (e.g. `software-engineering`) to lay out the strict 6-step project workflow so GAP knows what files it should be expecting.

```python
from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional, Dict, Union
from pydantic import BaseModel, Field, field_validator, model_validator

class CheckpointStrategy(str, Enum):
    # Old global policy configuration. Now largely superseded by per-task checkpoints in plan.yaml!
    EXPLICIT = "explicit"
    EVERY = "every"
    BATCH = "batch"

class Checkpoints(BaseModel):
    strategy: CheckpointStrategy = CheckpointStrategy.EXPLICIT
    after_tasks: List[str] = Field(default_factory=list)
```
```python
class Step(BaseModel):
    # Maps directly to a single "- step: requirements" block in manifest.yaml
    step: str
    name: Optional[str] = None
    artifact: str # e.g. "docs/requirements.md"
    view: Optional[str] = None  # Optional human readable counterpart (e.g. for YAML tasks)
    gate: bool = True  # Does this require `gap gate approve`?
    needs: List[str] = Field(default_factory=list) # Which steps must finish before this unlocks?
    action: Optional[str] = None 
    template: Optional[str] = None
    description: Optional[str] = None
    phase_class: Optional[str] = None
    
    @field_validator('gate', mode='before')
    @classmethod
    def parse_gate(cls, v):
        # Gracefully converts words like "true", "manual", "auto", "no" into Boolean True/False
        if isinstance(v, bool): return v
        if isinstance(v, str):
            if v.lower() in ('true', 'manual', 'yes', '1'): return True
            if v.lower() in ('false', 'auto', 'no', '0'): return False
        raise ValueError(f"Invalid gate value: {v}")
```
```python
class PhaseClass(BaseModel):
    # Allows grouping steps into "alignment" vs "execution" phases.
    phase_class: str = Field(alias='class')
    steps: List[Step] = Field(default_factory=list)
    class Config: populate_by_name = True

class ProtocolRef(BaseModel):
    protocol: str
    role: Optional[str] = None
```
```python
class GapManifest(BaseModel):
    # The absolute parent container parsing the whole manifest.yaml file.
    kind: Literal['protocol', 'project']
    name: str
    version: str
    description: str
    flow: List[Union[Step, PhaseClass]] = Field(default_factory=list)
    extends: List[ProtocolRef] = Field(default_factory=list)
    checkpoints: Optional[Checkpoints] = None
    templates: Dict[str, str] = Field(default_factory=dict)
    
    #... helper functions below to flatten the nested steps ...
```

---

## 5. `factory.py`
Originally designed to choose between SQL databases and YAML files. Since SQL is gone, it just blindly returns the `YamlLedger`.

```python
import os
from pathlib import Path
from typing import Optional
from gap.core.ledger import Ledger, YamlLedger
from gap.core.manifest import GapManifest

def get_ledger(root: Path, manifest: GapManifest) -> Ledger:
    """
    Very simple factory. It literally just returns a YamlLedger object.
    """
    return YamlLedger(root)
```
**(Verdict: Over-engineered hallucination. We can easily delete this file and just instantiate `YamlLedger()` wherever we need it.)**

---

## 6. `ledger.py`
The "Database Manager." It reads the `.gap/status.yaml` file to tell `gap` what steps are completed, and dynamically checks reality to see if human activity bypassed the protocol.

```python
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
import yaml
from typing import Optional

from gap.core.state import GapStatus, StepData, StepStatus
from gap.core.manifest import GapManifest

class Ledger(ABC):
    # An abstract base class demanding that any ledger we write MUST have `get_status` and `update_status`.
    def __init__(self, root: Path):
        self.root = root
```
```python
class YamlLedger(Ledger):
    def get_status(self, manifest: GapManifest) -> GapStatus:
        # Step 1: Read the historical .gap/status.yaml ledger log.
        ledger_path = self.root / ".gap/status.yaml"
        ledger = GapStatus()
        if ledger_path.exists():
            with open(ledger_path) as f:
                data = yaml.safe_load(f)
                if data: ledger = GapStatus(**data)
        
        # Step 2: CROSS-EXAMINE REALITY (The "Hybrid Check")
        # We don't just blindly trust the ledger. We look at the actual hard drive.
        real_status = GapStatus()
        
        for step in manifest.flow:
            # Did the steps required before this one finish?
            dependencies_met = all( ... ) 
            
            # Does the file actually exist in out project? (e.g. docs/design.md)
            is_live = (self.root / step.artifact).exists()
            
            # Does a pending proposal exist waiting for approval?
            is_proposed = (self.root / ".gap/proposals" / step.artifact).exists()
            
            current = StepStatus.LOCKED
            
            # Check for Drifting: If human created file without completing previous steps
            if is_live:
                if not dependencies_met: current = StepStatus.INVALID
                else: current = StepStatus.COMPLETE
            elif is_proposed:
                current = StepStatus.PENDING
            elif dependencies_met:
                current = StepStatus.UNLOCKED
                
            # Copy over who approved it and when from the historical log.
            step_data = StepData(status=current)
            real_status.steps[step.step] = step_data
            
        return real_status

    def update_status(self, step: str, status: StepStatus, approver: str = "user", timestamp=None):
        # Writes the `status: complete` directly into `.gap/status.yaml`. invoked by `gap gate approve`.
```

---

## 7. `auditor.py`
The Traceability Engine. Uses regex parsing and python models to ensure that every Code change traces to a Task, every Task traces to a Design, and every Design traces to a Requirement.

```python
import re
from pathlib import Path
import yaml
from typing import List, Dict, Set, Optional
from gap.core.validator import ValidationError
from gap.core.manifest import GapManifest
from gap.core.models import TaskList

class TraceabilityAuditor:
    # Look for magical strings like "(Traces to: D-01)"
    ID_PATTERN = r"(?:(?:G|R|FR|NFR|DP|PROP|P|TASK|H|T)-[A-Z0-9_\-]+)|(?:<!-- id: (.*?) -->)"
    TRACES_TO_PATTERN = r"\(Traces to: (.*?)\)"
    VALIDATES_PATTERN = r"\(Validates: (.*?)\)"

    # ... init and setup ...

    def audit(self) -> List[ValidationError]:
        # Massive validation routine.
        # Grab all the IDs present in Requirements, Design, and Tasks.
        # Check if Design.md validates the Requirements IDs.
        # Check if Tasks.yaml traces to valid Design IDs.
        # Warn if there are "Orphan" designs or tasks that don't trace to anything.
        return errors
        
```
**(Verdict: This demands perfect markdown syntax linking from the AI crashes the pipeline easily for petty formatting mistakes. Do you want to DELETE it?)**

---

## 8. `path.py`
Template locating engine.

```python
class PathManager:
    # A class that tries 3 different ways to find a "template" markdown file.
    def resolve_template(self, manifest: GapManifest, name: str) -> Path:
        # First: Ask manifest explicit mappings
        # Second: Look in the global /templates folder
        # Third: Hardcoded fallback logic checking other protocols 
```
**(Verdict: Over-engineering hallucination. `manifest.yaml` explicitly defines the filepaths for every step. We do not need a massive 3-layered fallback locator. DELETE).**

---

## 9. `validator.py`
Algorithms protecting against user configuration mistakes in `.yaml` files.

```python
class ManifestValidator:
    # Runs Topological Sorts and Graph Cycle Detection.
    def _check_circular_deps(self, manifest: GapManifest) -> List[ValidationError]:
        # What if the user wrote:
        # Step A needs Step B
        # Step B needs Step A?
        # This graph algorithm detects that.
        
    def _check_missing_refs(self, manifest: GapManifest) -> List[ValidationError]:
        # What if Step C needs Step X... but Step X doesn't exist?
```
**(Verdict: Classic AI Over-engineering. `manifest.yaml` is a static, fixed 6-step file written by a person, not dynamically generated code. Nobody is going to accidentally write an infinite cycle in 20 lines of hardcoded configuration mapping. DELETE).**

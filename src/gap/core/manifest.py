from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional, Dict, Union
from pydantic import BaseModel, Field, field_validator

class CheckpointStrategy(str, Enum):
    """When to pause execution for approval."""
    EXPLICIT = "explicit"  # Pause at listed task IDs
    EVERY = "every"        # Pause after every task
    BATCH = "batch"        # Run all, review at end

class Checkpoints(BaseModel):
    """Execution checkpoint configuration."""
    strategy: CheckpointStrategy = CheckpointStrategy.EXPLICIT
    after_tasks: List[str] = Field(default_factory=list)

class Step(BaseModel):
    step: str
    name: Optional[str] = None
    artifact: str
    gate: bool  # true = requires approval, false = autonomous
    needs: List[str] = Field(default_factory=list)
    action: Optional[str] = None # e.g. 'scribe'
    template: Optional[str] = None
    description: Optional[str] = None
    
    @field_validator('gate', mode='before')
    @classmethod
    def parse_gate(cls, v):
        """Handle both bool and string values from YAML."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            if v.lower() in ('true', 'manual', 'yes', '1'):
                return True
            if v.lower() in ('false', 'auto', 'no', '0'):
                return False
        raise ValueError(f"Invalid gate value: {v}")

class ProtocolRef(BaseModel):
    protocol: str
    role: Optional[str] = None

class GapManifest(BaseModel):
    kind: Literal['protocol', 'project']
    name: str
    version: str
    description: str
    flow: List[Step] = Field(default_factory=list)
    extends: List[ProtocolRef] = Field(default_factory=list)
    
    # Execution configuration
    checkpoints: Optional[Checkpoints] = None
    
    # Mapping for Project implementation (e.g. Course -> Campaign)
    templates: Dict[str, str] = Field(default_factory=dict)

def load_manifest(path: Path) -> GapManifest:
    import yaml
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    
    return GapManifest(**data)
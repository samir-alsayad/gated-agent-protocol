from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional, Dict, Union
from pydantic import BaseModel, Field, field_validator, model_validator

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
    gate: bool = True  # true = requires approval, false = autonomous
    needs: List[str] = Field(default_factory=list)
    action: Optional[str] = None # e.g. 'scribe'
    template: Optional[str] = None
    description: Optional[str] = None
    phase_class: Optional[str] = None  # Set by parent PhaseClass
    
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

class PhaseClass(BaseModel):
    """A class of steps (alignment or execution)."""
    phase_class: str = Field(alias='class')
    steps: List[Step] = Field(default_factory=list)
    
    class Config:
        populate_by_name = True

class ProtocolRef(BaseModel):
    protocol: str
    role: Optional[str] = None

class GapManifest(BaseModel):
    kind: Literal['protocol', 'project']
    name: str
    version: str
    description: str
    flow: List[Union[Step, PhaseClass]] = Field(default_factory=list)
    extends: List[ProtocolRef] = Field(default_factory=list)
    
    # Execution configuration
    checkpoints: Optional[Checkpoints] = None
    
    # Mapping for Project implementation (e.g. Course -> Campaign)
    templates: Dict[str, str] = Field(default_factory=dict)
    
    def get_flat_steps(self) -> List[Step]:
        """Flatten nested PhaseClass structure into a list of Steps with phase_class set."""
        flat = []
        for item in self.flow:
            if isinstance(item, PhaseClass):
                for step in item.steps:
                    step.phase_class = item.phase_class
                    flat.append(step)
            else:
                flat.append(item)
        return flat
    
    def get_alignment_steps(self) -> List[Step]:
        """Get only alignment phase steps."""
        return [s for s in self.get_flat_steps() if s.phase_class == 'alignment']
    
    def get_execution_steps(self) -> List[Step]:
        """Get only execution phase steps."""
        return [s for s in self.get_flat_steps() if s.phase_class == 'execution']

def load_manifest(path: Path) -> GapManifest:
    import yaml
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    
    return GapManifest(**data)
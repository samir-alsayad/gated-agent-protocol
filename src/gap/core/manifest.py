from enum import Enum
from pathlib import Path
from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field

class GateType(str, Enum):
    MANUAL = "manual"
    AUTO = "auto"

class Step(BaseModel):
    step: str
    name: Optional[str] = None
    artifact: str
    gate: GateType
    needs: List[str] = Field(default_factory=list)
    action: Optional[str] = None # e.g. 'scribe'
    template: Optional[str] = None

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
    
    # Mapping for Project implementation (e.g. Course -> Campaign)
    templates: Dict[str, str] = Field(default_factory=dict)

def load_manifest(path: Path) -> GapManifest:
    import yaml
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    
    return GapManifest(**data)
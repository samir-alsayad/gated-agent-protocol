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
    traces_to: Optional[str] = None
    outputs: List[str] = Field(default_factory=list)

class TaskList(BaseModel):
    """Schema for .gap/tasks.yaml"""
    tasks: List[Task] = Field(default_factory=list)

# --- Plan Models ---

class FilesystemACL(BaseModel):
    write: List[str] = Field(default_factory=list)
    read: List[str] = Field(default_factory=list)

class ACLDefinition(BaseModel):
    filesystem: FilesystemACL = Field(default_factory=FilesystemACL)
    shell: List[str] = Field(default_factory=list)
    tools: Dict[str, List[str]] = Field(default_factory=dict) # allowed/blocked tools

class CognitionDefinition(BaseModel):
    execution: Literal['local', 'cloud'] = 'local'
    model: str
    temperature: Optional[float] = None

class PlanEnvelope(BaseModel):
    """
    The execution authorization for a single Task.
    """
    acl: ACLDefinition = Field(default_factory=ACLDefinition)
    cognition: CognitionDefinition
    checkpoints: List[str] = Field(default_factory=list)

class Plan(BaseModel):
    """Schema for .gap/plan.yaml"""
    # Mapping of Task ID -> Execution Envelope
    plan: Dict[str, PlanEnvelope] = Field(default_factory=dict)

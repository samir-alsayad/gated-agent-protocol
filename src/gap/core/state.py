from enum import Enum
from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel
import yaml

from gap.core.manifest import GapManifest, GateType

class StepStatus(str, Enum):
    LOCKED = "locked"       # Dependencies not met
    UNLOCKED = "unlocked"   # Dependencies met, ready for Scribe
    PENDING = "pending"     # Proposal exists, waiting for Gate
    COMPLETE = "complete"   # File exists in Live & Ledger
    INVALID = "invalid"     # File exists but dependencies not met (drift detected)

class StepData(BaseModel):
    status: StepStatus
    timestamp: Optional[str] = None
    approver: Optional[str] = None

class GapStatus(BaseModel):
    # Map step_name -> Data
    steps: Dict[str, StepData] = {} 

# get_status moved to gap.core.ledger.YamlLedger
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
import yaml
from typing import Optional

from gap.core.state import GapStatus, StepData, StepStatus
from gap.core.manifest import GapManifest

class Ledger(ABC):
    def __init__(self, root: Path):
        self.root = root

    @abstractmethod
    def get_status(self, manifest: GapManifest) -> GapStatus:
        """Calculate the current status of all steps in the manifest."""
        pass

    @abstractmethod
    def update_status(self, step: str, status: StepStatus, approver: str = "user", timestamp: Optional[datetime] = None) -> None:
        """Update the status of a specific step in the ledger."""
        pass

class YamlLedger(Ledger):
    def get_status(self, manifest: GapManifest) -> GapStatus:
        # 1. Load Ledger (if exists)
        ledger_path = self.root / ".gap/status.yaml"
        ledger = GapStatus()
        if ledger_path.exists():
            with open(ledger_path) as f:
                data = yaml.safe_load(f)
                if data:
                    ledger = GapStatus(**data)
        
        # 2. Re-calculate Status based on Reality (Hybrid Check)
        real_status = GapStatus()
        
        for step in manifest.flow:
            # Check Dependencies
            dependencies_met = all(
                real_status.steps.get(dep, StepData(status=StepStatus.LOCKED)).status == StepStatus.COMPLETE
                for dep in step.needs
            )
            
            # Check File Existence
            artifact_path = self.root / step.artifact
            is_live = artifact_path.exists()
            
            # Check Proposal Existence
            proposal_path = self.root / ".gap/proposals" / step.artifact
            is_proposed = proposal_path.exists()
            
            current = StepStatus.LOCKED
            
            if is_live:
                # CRITICAL: Validate dependencies before marking complete
                if not dependencies_met:
                    # File exists but dependencies not met - this is drift/bypass
                    current = StepStatus.INVALID
                else:
                    # HYBRID CHECK: Files are truth
                    current = StepStatus.COMPLETE
            elif is_proposed:
                current = StepStatus.PENDING
            elif dependencies_met:
                current = StepStatus.UNLOCKED
                
            # If ledger has more info (like timestamp), preserve it
            step_data = StepData(status=current)
            
            if current == StepStatus.COMPLETE and step.step in ledger.steps:
                 # Restore metadata if available
                 old_data = ledger.steps[step.step]
                 if old_data.status == StepStatus.COMPLETE:
                     step_data.timestamp = old_data.timestamp
                     step_data.approver = old_data.approver
            
            real_status.steps[step.step] = step_data
            
        return real_status

    def update_status(self, step: str, status: StepStatus, approver: str = "user", timestamp: Optional[datetime] = None) -> None:
        ledger_path = self.root / ".gap/status.yaml"
        current_data = {}
        
        if ledger_path.exists():
            with open(ledger_path) as f:
                current_data = yaml.safe_load(f) or {}
                
        if "steps" not in current_data:
            current_data["steps"] = {}
            
        ts = timestamp or datetime.now()
        
        current_data["steps"][step] = {
            "status": status.value,
            "timestamp": ts.isoformat(),
            "approver": approver
        }
        
        # Ensure dir exists
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(ledger_path, "w") as f:
            yaml.safe_dump(current_data, f)

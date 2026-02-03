"""
GAP Agent Harness - Governance Layer for AI Coding Agents

This module demonstrates how to integrate GAP into any agentic coding tool
(OpenCode, Cursor, Cline, etc.) to enforce the "State Machine of Work".

Usage:
    from gap_harness import GAPHarness
    
    harness = GAPHarness("path/to/project")
    
    # Before any action, check permission
    if harness.can_write("src/login.py"):
        # Proceed with write
    else:
        # Agent must stop and request approval
"""

import subprocess
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class StepStatus(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    PENDING = "pending"
    COMPLETE = "complete"
    INVALID = "invalid"


@dataclass
class WorkflowState:
    """Current state of the GAP workflow."""
    protocol_name: str
    version: str
    current_phase: str
    current_status: StepStatus
    next_action: str  # What the agent should do


class GAPHarness:
    """
    The GAP Harness wraps the gap CLI and provides a Python API
    for agents to check permissions before acting.
    """
    
    def __init__(self, project_root: str, manifest_path: str = "manifest.yaml"):
        self.root = Path(project_root)
        self.manifest_path = self.root / manifest_path
        
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"No manifest found at {self.manifest_path}")
    
    def get_status(self) -> dict:
        """Get the current workflow status from GAP."""
        result = subprocess.run(
            ["gap", "check", "status", str(self.manifest_path), "--json"],
            capture_output=True,
            text=True,
            cwd=str(self.root)
        )
        
        # For now, parse the text output (JSON flag is future work)
        # This is a simplified parser
        lines = result.stdout.strip().split("\n")
        status = {}
        
        for line in lines:
            if "🟢" in line:
                step = line.split(":")[0].replace("🟢", "").strip()
                status[step] = StepStatus.UNLOCKED
            elif "🔒" in line:
                step = line.split(":")[0].replace("🔒", "").strip()
                status[step] = StepStatus.LOCKED
            elif "⚠️" in line:
                step = line.split(":")[0].replace("⚠️", "").strip()
                status[step] = StepStatus.INVALID
            elif "✅" in line:
                step = line.split(":")[0].replace("✅", "").strip()
                status[step] = StepStatus.COMPLETE
        
        return status
    
    def get_current_phase(self) -> Optional[str]:
        """Get the first unlocked phase (where agent should work)."""
        status = self.get_status()
        for step, state in status.items():
            if state == StepStatus.UNLOCKED:
                return step
        return None
    
    def can_proceed(self, target_phase: str) -> bool:
        """Check if the agent can work on a specific phase."""
        status = self.get_status()
        phase_status = status.get(target_phase)
        
        if phase_status in (StepStatus.UNLOCKED, StepStatus.PENDING):
            return True
        return False
    
    def can_write(self, file_path: str) -> bool:
        """
        Check if the agent has permission to write to a file.
        
        This checks:
        1. Is the current phase's gate approved?
        2. Does the ACL allow writes to this path?
        """
        # Get current phase
        current = self.get_current_phase()
        if not current:
            return False  # No unlocked phase = no writes allowed
        
        # Check ACL (if exists)
        acl_path = self.root / ".gap" / "acls" / f"{current}.yaml"
        if acl_path.exists():
            import yaml
            with open(acl_path) as f:
                acl = yaml.safe_load(f)
            
            allowed_writes = acl.get("allowed_writes", [])
            # Simple glob matching
            from fnmatch import fnmatch
            for pattern in allowed_writes:
                if fnmatch(file_path, pattern):
                    return True
            return False
        
        # No ACL = default allow (but warn)
        return True
    
    def propose(self, phase: str, content: str) -> Path:
        """
        Write content to the proposal directory (not live).
        Returns the path where the proposal was written.
        """
        result = subprocess.run(
            ["gap", "scribe", "create", phase, "--dry-run"],
            capture_output=True,
            text=True,
            cwd=str(self.root)
        )
        
        # Get the artifact path from manifest
        # For now, just write to .gap/proposals/
        proposal_dir = self.root / ".gap" / "proposals"
        proposal_dir.mkdir(parents=True, exist_ok=True)
        
        # Write proposal
        proposal_path = proposal_dir / f"{phase}.md"
        proposal_path.write_text(content)
        
        return proposal_path
    
    def request_approval(self, phase: str) -> str:
        """
        Generate a message for the human requesting approval.
        The agent should display this and STOP.
        """
        return f"""
┌─────────────────────────────────────────────────────────┐
│  🚦 GAP CHECKPOINT: Approval Required                   │
├─────────────────────────────────────────────────────────┤
│  Phase: {phase:<45} │
│                                                         │
│  A proposal has been written to:                        │
│  .gap/proposals/{phase}.md                              │
│                                                         │
│  To approve and continue:                               │
│  $ gap gate approve {phase}                             │
│                                                         │
│  To reject:                                             │
│  $ gap gate reject {phase}                              │
└─────────────────────────────────────────────────────────┘
"""


# =============================================================================
# EXAMPLE USAGE: How an Agent Would Use This
# =============================================================================

def example_agent_loop():
    """
    Example of how an AI coding agent would use GAP for governance.
    """
    
    harness = GAPHarness("/path/to/project")
    
    # 1. Check current state
    current_phase = harness.get_current_phase()
    print(f"Current phase: {current_phase}")
    
    if not current_phase:
        print("All phases complete or locked. Nothing to do.")
        return
    
    # 2. Do work for current phase
    if current_phase == "requirements":
        # Agent gathers requirements
        content = """
# Requirements

## User Stories
- As a user, I want to log in with email/password
- As a user, I want to reset my password

## Constraints
- Must use existing auth library
- No third-party OAuth for v1
"""
        # Write to proposal (NOT live)
        proposal_path = harness.propose("requirements", content)
        print(f"Proposal written to: {proposal_path}")
        
        # 3. STOP and request approval
        print(harness.request_approval("requirements"))
        return  # Agent MUST stop here!
    
    elif current_phase == "design":
        # Check if we can write to specific files
        if harness.can_write("src/auth/login.py"):
            print("I can write to auth files")
        else:
            print("No permission for auth files yet")


if __name__ == "__main__":
    example_agent_loop()

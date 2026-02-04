"""
GAP Agent Harness - The Sovereign Governance Layer

This module implements the "Effective Policy" resolution and the 5-phase 
Decision/Execution loop defined in the GAP v2.0 Whitepaper.

Canon:
1. Decision Phases (Mandatory Gating): Requirements, Design, Policy, Tasks.
2. Execution Phase (Optional Gating): Derived output, ACL-enforced.
3. Law vs Exception: Manifest (Law) + Session Config (Exception).
"""

import os
import yaml
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from fnmatch import fnmatch


class StepStatus(Enum):
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    PENDING = "pending"
    COMPLETE = "complete"


@dataclass
class EffectivePolicy:
    """The resolved governance rules for the current session."""
    mode: str = "gated"  # gated | autonomous
    task_granularity: str = "function"
    checkpoint_strategy: str = "explicit"
    after_tasks: List[str] = field(default_factory=list)


class GAPHarness:
    """
    The GAP Harness resolves 'Project Law' against 'Session Exceptions'
    and enforces the 'Decision Chain of Custody'.
    """

    DECISION_PHASES = ["requirements", "design", "policy", "task"]
    EXECUTION_PHASES = ["execution"]

    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.manifest_path = self.root / "manifest.yaml"
        self.session_reg_path = self.root / ".gap" / "gap.yaml"
        
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Missing Project Law: {self.manifest_path}")

    # --- 1. Policy Resolution (Law vs Exception) ---

    def _get_active_session_id(self) -> Optional[str]:
        if not self.session_reg_path.exists():
            return None
        with open(self.session_reg_path) as f:
            reg = yaml.safe_load(f)
            return reg.get("active_session")

    def get_effective_policy(self) -> EffectivePolicy:
        """
        Constructs the Effective Policy by applying explicit Session Exceptions 
        to immutable Project Law.
        """
        # A. Load Project Law (Defaults)
        with open(self.manifest_path) as f:
            manifest = yaml.safe_load(f)
            law = manifest.get("execution", {})

        policy = EffectivePolicy(
            mode=law.get("mode", "gated"),
            task_granularity=law.get("task_granularity", {}).get("max_scope", "function"),
            checkpoint_strategy=law.get("checkpoints", {}).get("strategy", "explicit"),
            after_tasks=law.get("checkpoints", {}).get("after_tasks", [])
        )

        # B. Apply Session Exceptions (Declared Deviations)
        session_id = self._get_active_session_id()
        if session_id:
            config_path = self.root / ".gap" / "sessions" / session_id / "config.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    session_config = yaml.safe_load(f)
                    exceptions = session_config.get("execution_exceptions", {})
                    
                    if "mode" in exceptions:
                        policy.mode = exceptions["mode"]
                    if "task_granularity" in exceptions:
                        policy.task_granularity = exceptions["task_granularity"].get("max_scope", policy.task_granularity)
                    if "checkpoints" in exceptions:
                        cp = exceptions["checkpoints"]
                        policy.checkpoint_strategy = cp.get("strategy", policy.checkpoint_strategy)
                        policy.after_tasks = cp.get("after_tasks", policy.after_tasks)

        return policy

    # --- 2. State & Phase Management ---

    def get_current_phase(self) -> Optional[str]:
        """Query the ledger to find the active phase."""
        result = subprocess.run(
            ["gap", "check", "status", "--manifest", str(self.manifest_path)],
            capture_output=True, text=True, cwd=str(self.root)
        )
        # Simplified parser for status output
        for line in result.stdout.split("\n"):
            if "🟢" in line:
                return line.split(":")[0].replace("🟢", "").strip()
        return None

    def is_decision_phase(self, phase: str) -> bool:
        return phase in self.DECISION_PHASES

    def is_execution_phase(self, phase: str) -> bool:
        return phase in self.EXECUTION_PHASES

    # --- 3. Enforcement Loop ---

    def can_write(self, file_path: str) -> bool:
        """
        Decision records MUST be proposed. 
        Execution output is allowed IF it matches the task-derived ACL.
        """
        phase = self.get_current_phase()
        if not phase: return False

        # Rule: No implicit authority for decisions
        if self.is_decision_phase(phase):
            return False

        # Rule: Execution requires ACL match
        acl_path = self.root / ".gap" / "acls" / f"{phase}.yaml"
        if not acl_path.exists():
            return False

        with open(acl_path) as f:
            acl = yaml.safe_load(f)
            for pattern in acl.get("allow_write", []):
                if fnmatch(file_path, pattern):
                    return True
        return False

    def should_pause(self, last_task_id: str) -> bool:
        """Based on effective policy checkpoints."""
        policy = self.get_effective_policy()
        
        if policy.checkpoint_strategy == "every":
            return True
        if policy.checkpoint_strategy == "explicit" and last_task_id in policy.after_tasks:
            return True
        return False

    def propose(self, phase: str, content: str):
        """Mandatory for Decision Phases."""
        proposal_dir = self.root / ".gap" / "proposals"
        proposal_dir.mkdir(parents=True, exist_ok=True)
        
        # In a real tool, the artifact path would come from the manifest
        # Here we assume a simple mapping for the example
        if phase == "policy":
            proposal_path = proposal_dir / "policy.md"
        else:
            proposal_path = proposal_dir / f"{phase}.md"
        
        with open(proposal_path, "w") as f:
            f.write(content)
        return proposal_path

    def checkpoint_message(self, phase: str, task_id: Optional[str] = None) -> str:
        header = "🚦 GAP MANDATORY GATE" if self.is_decision_phase(phase) else "🛑 GAP EXECUTION PAUSE"
        msg = f"Phase: {phase}"
        if task_id: msg += f" | Task: {task_id}"
        
        return f"\n{header}\n{msg}\nReview required before proceeding.\n$ gap gate approve {phase}\n"


# --- 4. The Sovereign Agent Loop ---

def run_agent_loop():
    harness = GAPHarness(os.getcwd())
    phase = harness.get_current_phase()
    
    if not phase:
        print("Chain of Custody complete.")
        return

    # A. Decision Phase (Mandatory Gating)
    if harness.is_decision_phase(phase):
        print(f"[*] Entering Decision Phase: {phase}")
        # Agent generates proposal...
        proposal_content = f"# {phase.capitalize()}\n\nProposed decisions..."
        harness.propose(phase, proposal_content)
        print(harness.checkpoint_message(phase))
        return

    # B. Execution Phase (ACL-Bound Output)
    elif harness.is_execution_phase(phase):
        print(f"[*] Entering Execution Phase: {phase}")
        policy = harness.get_effective_policy()
        
        # Mock task execution
        tasks = ["1.1", "1.2"] 
        for tid in tasks:
            # 1. ACL Check
            if not harness.can_write("src/output.py"):
                print("[-] Access Denied by ACL")
                return
            
            # 2. Work...
            print(f"[+] Executing Task {tid}")
            
            # 3. Checkpoint check
            if harness.should_pause(tid):
                print(harness.checkpoint_message(phase, tid))
                return


if __name__ == "__main__":
    run_agent_loop()

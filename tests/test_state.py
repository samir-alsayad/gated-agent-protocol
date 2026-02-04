import pytest
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.ledger import YamlLedger
from gap.core.state import StepStatus

# Removed old fixture


def test_initial_state_locking(mock_manifest):
    """
    Verify that in a pristine environment (no ledger, no files),
    dependent steps are LOCKED.
    """
    root = Path.cwd()
    ledger = YamlLedger(root)
    status = ledger.get_status(mock_manifest)
    
    # Step A (No dependencies) -> Unlocked
    assert status.steps["step_a"].status == StepStatus.UNLOCKED
    
    # Step B (Needs A) -> Locked
    assert status.steps["step_b"].status == StepStatus.LOCKED

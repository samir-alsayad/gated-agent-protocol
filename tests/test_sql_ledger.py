import pytest
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.sql_ledger import SqlLedger
from gap.core.state import StepStatus

# Removed old fixture


@pytest.fixture
def sql_ledger(tmp_path):
    """Create a SqlLedger backed by a temporary SQLite DB."""
    # We use a tmp_path for the root to simulate the FS
    db_url = f"sqlite:///{tmp_path}/ledger.db"
    return SqlLedger(
        db_url=db_url,
        project_name="test_project",
        protocol="instructional",
        root=tmp_path
    )

def test_sql_ledger_initial_state(sql_ledger, mock_manifest):
    """Verify initial locked state logic works with SQL backend."""
    status = sql_ledger.get_status(mock_manifest)
    
    # Step A should be UNLOCKED (no deps)
    assert status.steps["step_a"].status == StepStatus.UNLOCKED
    
    # Step B should be LOCKED (depends on A)
    assert status.steps["step_b"].status == StepStatus.LOCKED

def test_sql_ledger_update(sql_ledger, mock_manifest):
    """Verify we can update logic and it persists."""
    # 1. Update 'step_a' to COMPLETE
    sql_ledger.update_status("step_a", StepStatus.COMPLETE, approver="Tester")
    
    # 2. Simulate File Creation
    step_a = next(s for s in mock_manifest.flow if s.step == "step_a")
    (sql_ledger.root / step_a.artifact).touch()
    
    # 3. Check Status
    status = sql_ledger.get_status(mock_manifest)
    assert status.steps["step_a"].status == StepStatus.COMPLETE
    
    # 4. Dependency Unlocking
    # Now step_b should be UNLOCKED
    assert status.steps["step_b"].status == StepStatus.UNLOCKED

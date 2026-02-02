import pytest
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.sql_ledger import SqlLedger
from gap.core.state import StepStatus

@pytest.fixture
def instructional_manifest():
    root = Path.cwd()
    path = root / "src/gap/protocols/instructional/manifest.yaml"
    return load_manifest(path)

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

def test_sql_ledger_initial_state(sql_ledger, instructional_manifest):
    """Verify initial locked state logic works with SQL backend."""
    status = sql_ledger.get_status(instructional_manifest)
    
    # Requirements should be UNLOCKED (no deps)
    # But since file doesn't exist in tmp_path, it's NOT COMPLETE.
    assert status.steps["requirements"].status == StepStatus.UNLOCKED
    
    # Design should be LOCKED (depends on requirements)
    assert status.steps["design_course"].status == StepStatus.LOCKED

def test_sql_ledger_update(sql_ledger, instructional_manifest):
    """Verify we can update logic and it persists."""
    # 1. Update 'requirements' to COMPLETE
    sql_ledger.update_status("requirements", StepStatus.COMPLETE, approver="Tester")
    
    # 2. Simulate File Creation (Hybrid Check)
    # The Ledger trusts the DB update for status_update logic, 
    # BUT get_status checks FS. 
    # If we mark COMPLETE in DB but file doesn't exist, get_status returns UNLOCKED (drift).
    # So we MUST create the file too.
    
    # Create the artifact file
    req_step = next(s for s in instructional_manifest.flow if s.step == "requirements")
    (sql_ledger.root / req_step.artifact).parent.mkdir(parents=True, exist_ok=True)
    (sql_ledger.root / req_step.artifact).touch()
    
    # 3. Check Status
    status = sql_ledger.get_status(instructional_manifest)
    assert status.steps["requirements"].status == StepStatus.COMPLETE
    assert status.steps["requirements"].approver == "Tester"
    
    # 4. Dependency Unlocking
    # Now design_course should be UNLOCKED
    assert status.steps["design_course"].status == StepStatus.UNLOCKED

import pytest
import os
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.factory import get_ledger
from gap.core.sql_ledger import SqlLedger
from gap.core.ledger import YamlLedger

@pytest.fixture
def clean_env():
    """Ensure GAP_DB_URL is clean before and after test."""
    if "GAP_DB_URL" in os.environ:
        del os.environ["GAP_DB_URL"]
    yield
    if "GAP_DB_URL" in os.environ:
        del os.environ["GAP_DB_URL"]

def test_factory_default(clean_env):
    """Verify default is YamlLedger."""
    root = Path.cwd()
    # We pass a dummy manifest, factory doesn't check it for YamlLedger
    manifest = None 
    ledger = get_ledger(root, manifest)
    assert isinstance(ledger, YamlLedger)

def test_factory_sql_override(clean_env, tmp_path):
    """Verify GAP_DB_URL triggers SqlLedger."""
    db_url = f"sqlite:///{tmp_path}/integration.db"
    os.environ["GAP_DB_URL"] = db_url
    
    # We need a real manifest object for SqlLedger initialization (names)
    # Create a dummy one
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text("""
kind: protocol
name: integration_test
version: 0.1.0
description: Test
flow:
  - step: requirements
    gate: manual
    artifact: docs/req.md
""")
    manifest = load_manifest(manifest_path)
    
    root = tmp_path
    ledger = get_ledger(root, manifest)
    assert isinstance(ledger, SqlLedger)
    assert ledger.project_name == "integration_test"
    
    # Verify it works end-to-end
    status = ledger.get_status(manifest)
    assert "requirements" in status.steps

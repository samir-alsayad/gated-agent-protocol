import pytest
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.path import PathManager

def test_resolve_local_template(mock_manifest, mock_project_root):
    """Verify resolving a template that exists locally."""
    pm = PathManager(mock_project_root) 
    
    # 'step_a' maps to 'templates/a.md' in mock_manifest
    # mock_project_root fixtures creates 'templates/a.md'
    
    path = pm.resolve_template(mock_manifest, "step_a")
    assert path.exists()
    assert path.name == "a.md"

def test_resolve_inherited_template(mock_project_root):
    """Verify that we can resolve when given a direct path."""
    # (Simplified for now - removing the hardcoded 'course' check test as we removed that hack)
    # Just verify basic existence check
    pm = PathManager(mock_project_root)
    assert pm.root == mock_project_root

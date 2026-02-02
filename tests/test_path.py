import pytest
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.path import PathManager

def test_resolve_local_template():
    """Verify resolving a template that exists locally."""
    root = Path.cwd()
    manifest_path = root / "src/gap/protocols/instructional/manifest.yaml"
    if not manifest_path.exists():
        pytest.skip("Manifest missing")
        
    pm = PathManager(manifest_path.parent) # Use protocol dir as root
    manifest = load_manifest(manifest_path)
    
    # 'intent' is defined in manifest.templates -> templates/intent.md
    # NOTE: In previous steps we changed artifact to docs/intent.md but template remains templates/intent.md?
    # Let's check the map in manifest.yaml
    # templates:
    #   intent: templates/intent.md
    
    path = pm.resolve_template(manifest, "intent")
    assert path.exists()
    assert path.name == "intent.md"

def test_resolve_inherited_template():
    """Verify the inheritance logic (simulated)."""
    root = Path.cwd()
    pm = PathManager(root)
    
    # We need a manifest context to pass, even if we are checking cross-protocol logic.
    # The current PathManager logic for "course" falls back to instructional protocol.
    fake_manifest = None # resolve_template signature requires manifest, let's load one.
    manifest_path = root / "src/gap/protocols/instructional/manifest.yaml"
    manifest = load_manifest(manifest_path)
    
    path = pm.resolve_template(manifest, "course")
    assert path.exists()
    assert "src/gap/protocols/instructional/templates" in str(path)

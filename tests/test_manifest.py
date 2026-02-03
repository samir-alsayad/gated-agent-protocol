import pytest
from pathlib import Path
from gap.core.manifest import load_manifest, GapManifest

def test_load_instructional_manifest():
    """Verify we can load the built-in instructional manifest."""
    root = Path.cwd()
    manifest_path = root / "src/gap/protocols/instructional/manifest.yaml"
    
    # Ensure the file exists before testing (sanity check)
    if not manifest_path.exists():
        pytest.skip(f"Manifest not found at {manifest_path}")

    manifest = load_manifest(manifest_path)
    
    assert isinstance(manifest, GapManifest)
    assert manifest.name == "instructional"
    assert len(manifest.flow) > 0
    
    # Check specific steps
    req_step = next(s for s in manifest.flow if s.step == "requirements")
    assert req_step.gate == True  # gate: true = requires approval
    assert req_step.artifact == "docs/intent.md"

def test_load_software_manifest():
    """Verify we can load the new software-engineering manifest."""
    root = Path.cwd()
    manifest_path = root / "src/gap/protocols/software-engineering/manifest.yaml"
    
    if not manifest_path.exists():
        pytest.skip(f"Manifest not found at {manifest_path}")

    manifest = load_manifest(manifest_path)
    assert manifest.name == "software-engineering"
    
    # Verify dependency chain
    design_step = next(s for s in manifest.flow if s.step == "design")
    assert "requirements" in design_step.needs

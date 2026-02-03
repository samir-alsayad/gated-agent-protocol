import pytest
from gap.core.manifest import GapManifest, Step, GateType
from gap.core.validator import ManifestValidator


def test_valid_manifest():
    """Test that a valid manifest passes validation."""
    manifest = GapManifest(
        kind="protocol",
        name="test",
        version="1.0.0",
        description="Test protocol",
        flow=[
            Step(step="requirements", artifact="docs/req.md", gate=GateType.MANUAL, needs=[]),
            Step(step="design", artifact="docs/design.md", gate=GateType.MANUAL, needs=["requirements"]),
            Step(step="implementation", artifact="docs/impl.md", gate=GateType.AUTO, needs=["design"]),
        ]
    )
    
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    assert len(errors) == 0


def test_circular_dependency():
    """Test detection of circular dependencies."""
    manifest = GapManifest(
        kind="protocol",
        name="test",
        version="1.0.0",
        description="Test protocol",
        flow=[
            Step(step="a", artifact="a.md", gate=GateType.MANUAL, needs=["b"]),
            Step(step="b", artifact="b.md", gate=GateType.MANUAL, needs=["c"]),
            Step(step="c", artifact="c.md", gate=GateType.MANUAL, needs=["a"]),
        ]
    )
    
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    assert len(errors) > 0
    assert any("circular" in str(err).lower() for err in errors)


def test_missing_reference():
    """Test detection of missing step references."""
    manifest = GapManifest(
        kind="protocol",
        name="test",
        version="1.0.0",
        description="Test protocol",
        flow=[
            Step(step="requirements", artifact="docs/req.md", gate=GateType.MANUAL, needs=[]),
            Step(step="design", artifact="docs/design.md", gate=GateType.MANUAL, needs=["nonexistent"]),
        ]
    )
    
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    assert len(errors) > 0
    assert any("unknown step" in str(err).lower() for err in errors)


def test_duplicate_steps():
    """Test detection of duplicate step IDs."""
    manifest = GapManifest(
        kind="protocol",
        name="test",
        version="1.0.0",
        description="Test protocol",
        flow=[
            Step(step="requirements", artifact="docs/req1.md", gate=GateType.MANUAL, needs=[]),
            Step(step="requirements", artifact="docs/req2.md", gate=GateType.MANUAL, needs=[]),
        ]
    )
    
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    assert len(errors) > 0
    assert any("duplicate" in str(err).lower() for err in errors)


def test_self_dependency():
    """Test detection of self-referencing dependencies."""
    manifest = GapManifest(
        kind="protocol",
        name="test",
        version="1.0.0",
        description="Test protocol",
        flow=[
            Step(step="requirements", artifact="docs/req.md", gate=GateType.MANUAL, needs=["requirements"]),
        ]
    )
    
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    assert len(errors) > 0
    assert any("depends on itself" in str(err).lower() for err in errors)


def test_complex_valid_dag():
    """Test a complex but valid dependency graph."""
    manifest = GapManifest(
        kind="protocol",
        name="test",
        version="1.0.0",
        description="Test protocol",
        flow=[
            Step(step="a", artifact="a.md", gate=GateType.MANUAL, needs=[]),
            Step(step="b", artifact="b.md", gate=GateType.MANUAL, needs=[]),
            Step(step="c", artifact="c.md", gate=GateType.MANUAL, needs=["a", "b"]),
            Step(step="d", artifact="d.md", gate=GateType.MANUAL, needs=["c"]),
            Step(step="e", artifact="e.md", gate=GateType.MANUAL, needs=["a"]),
        ]
    )
    
    validator = ManifestValidator()
    errors = validator.validate(manifest)
    
    assert len(errors) == 0

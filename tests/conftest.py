import pytest
from pathlib import Path
from gap.core.manifest import GapManifest, Step

@pytest.fixture
def mock_manifest():
    """Returns a stable, generic manifest for testing core logic."""
    return GapManifest(
        kind="protocol",
        name="test-protocol",
        version="0.0.1",
        description="A stable protocol for unit testing.",
        flow=[
            Step(step="step_a", artifact="a.md", gate=False),
            Step(step="step_b", artifact="b.md", gate=True, needs=["step_a"]),
            Step(step="step_c", artifact="c.md", gate=False, needs=["step_b"]),
        ],
        templates={
            "step_a": "templates/a.md",
            "step_b": "templates/b.md"
        }
    )

@pytest.fixture
def mock_project_root(tmp_path):
    """Creates a temporary project structure with templates."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "a.md").write_text("# Template A")
    (templates_dir / "b.md").write_text("# Template B")
    return tmp_path

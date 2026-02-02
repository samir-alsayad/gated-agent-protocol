import typer
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader

from gap.core.manifest import load_manifest, GateType
from gap.core.state import StepStatus
from gap.core.path import PathManager
from gap.core.factory import get_ledger

app = typer.Typer(help="Generate artifacts from templates.")

def read_input_data() -> Dict[str, Any]:
    """Read JSON/YAML from STDIN if available."""
    if sys.stdin.isatty():
        return {}
    
    content = sys.stdin.read().strip()
    if not content:
        return {}
        
    try:
        # Try JSON first
        return json.loads(content)
    except json.JSONDecodeError:
        try:
            # Try YAML
            return yaml.safe_load(content)
        except yaml.YAMLError:
            typer.secho("Error: Input is neither valid JSON nor YAML.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

@app.command("create")
def create(
    step: str = typer.Argument(..., help="Name of the step to run (e.g. 'design_course')."),
    manifest_path: Path = typer.Option(Path("manifest.yaml"), "--manifest", "-m", help="Path to manifest.yaml"),
    force: bool = typer.Option(False, "--force", "-f", help="Bypass state checks."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print output to stdout instead of writing file.")
):
    """
    Generate an artifact from a template.
    """
    # 1. Load Context
    if not manifest_path.exists():
        typer.secho(f"Error: Manifest not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    manifest = load_manifest(manifest_path)
    root = manifest_path.parent
    
    # 2. Check State
    if not force:
        ledger = get_ledger(root, manifest)
        state = ledger.get_status(manifest)
        step_data = state.steps.get(step)
        
        if not step_data:
             typer.secho(f"Error: Step '{step}' not found in calculated state.", fg=typer.colors.RED)
             raise typer.Exit(code=1)
             
        if step_data.status == StepStatus.LOCKED:
            typer.secho(f"❌ Step '{step}' is LOCKED. Complete previous steps first.", fg=typer.colors.RED)
            typer.echo("    Use --force to override.")
            raise typer.Exit(code=1)
            
        if step_data.status == StepStatus.COMPLETE:
            typer.secho(f"Warning: Step '{step}' is already COMPLETE.", fg=typer.colors.YELLOW)
            # We allow re-scribing (overwrite logic handled later), but warn user.

    # 3. Find Step Definition
    step_def = next((s for s in manifest.flow if s.step == step), None)
    if not step_def:
        typer.secho(f"Error: Step definition missing for '{step}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    template_name = step_def.template or step  # Default to step name if template not specified
    # However, manifest.yaml usually has explicit artifact paths. 
    # Let's look at how we defined manifests.
    # The step definition has 'artifact' (output path).
    # It does NOT strictly have a 'template' field in our current Step model, but we updated it earlier?
    # Let's check `manifest.py`.
    # Yes: `template: Optional[str] = None`
    
    # If template is not explicit, we might infer it or use the artifact name?
    # Actually, in Pydantic model we added 'template'. 
    # If it's missing, we need a convention.
    # Convention: If `artifact` is `docs/design.md`, template is `design`.
    # Let's use the 'map' in manifest if available.
    
    template_key = step
    if step in manifest.templates:
        template_key = manifest.templates[step]
        
    # 4. Resolve Template
    pm = PathManager(root)
    try:
        # We try to search for the template file. 
        # Since PathManager.resolve_template expects a NAME (e.g. 'course'), not a path.
        # We pass `template_key`.
        template_path = pm.resolve_template(manifest, template_key)
    except FileNotFoundError:
        # Fallback: if explicit template field is set
        if step_def.template:
             try:
                 template_path = pm.resolve_template(manifest, step_def.template)
             except FileNotFoundError:
                 typer.secho(f"Error: Template '{step_def.template}' not found.", fg=typer.colors.RED)
                 raise typer.Exit(code=1)
        else:
            typer.secho(f"Error: Could not resolve template for '{step}'.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    # 5. Render Content
    data = read_input_data()
    # Inject Standard Variables
    data['project_name'] = manifest.name
    data['step_name'] = step_def.name
    
    env = Environment(loader=FileSystemLoader(str(template_path.parent)))
    template = env.get_template(template_path.name)
    rendered_content = template.render(**data)
    
    # 6. Write (The Gate)
    target_path = root / step_def.artifact
    
    if dry_run:
        typer.echo(f"--- Dry Run: {target_path} ---")
        typer.echo(rendered_content)
        return

    if step_def.gate == GateType.MANUAL:
        # Write to Proposal
        proposal_dir = root / ".gap/proposals"
        proposal_dir.mkdir(parents=True, exist_ok=True)
        # We keep the directory structure of the artifact
        # e.g. artifacts/design.md -> .gap/proposals/artifacts/design.md
        # This handles nested artifacts correctly.
        proposal_write_path = proposal_dir / step_def.artifact
        
        # Ensure parent dirs exist in proposals
        proposal_write_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(proposal_write_path, "w") as f:
            f.write(rendered_content)
            
        typer.secho(f"📝 Proposal written to: {proposal_write_path}", fg=typer.colors.YELLOW)
        typer.echo("Run 'gap gate list' to see pending proposals.")
        
    elif step_def.gate == GateType.AUTO:
        # Write Directly to Live
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w") as f:
            f.write(rendered_content)
        typer.secho(f"✅ Scribed to Live: {target_path}", fg=typer.colors.GREEN)

import typer
import shutil
import yaml
import time
from pathlib import Path
from datetime import datetime

from gap.core.manifest import load_manifest
from gap.core.state import StepStatus
from gap.core.factory import get_ledger

app = typer.Typer(help="Manage approvals and state transitions.")

@app.command("list")
def list_proposals(
    manifest_path: Path = typer.Option(Path("manifest.yaml"), "--manifest", "-m", help="Path to manifest.yaml")
):
    """
    List all pending proposals waiting for approval.
    """
    if not manifest_path.exists():
        typer.secho(f"Error: Manifest not found at {manifest_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    root = manifest_path.parent
    proposal_dir = root / ".gap/proposals"
    
    if not proposal_dir.exists():
        typer.echo("No active proposals directory.")
        return

    # Find all files recursively in proposals
    proposals = [p for p in proposal_dir.glob("**/*") if p.is_file()]
    
    if not proposals:
        typer.echo("No pending proposals.")
        return
        
    typer.echo("📂 Pending Proposals:")
    for p in proposals:
        # simple relpath
        rel = p.relative_to(proposal_dir)
        typer.echo(f" - {rel}")

@app.command("approve")
def approve(
    step: str = typer.Argument(..., help="The step name to approve (e.g. 'design_course')."),
    manifest_path: Path = typer.Option(Path("manifest.yaml"), "--manifest", "-m", help="Path to manifest.yaml")
):
    """
    Approve a proposal.
    Moves file from .gap/proposals/ -> Live.
    Updates .gap/status.yaml.
    Extracts and stores ACL for next gate.
    """
    # 1. Load Context
    if not manifest_path.exists():
        typer.secho(f"Error: Manifest not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    manifest = load_manifest(manifest_path)
    root = manifest_path.parent
    
    # 2. Find Step
    step_def = next((s for s in manifest.flow if s.step == step), None)
    if not step_def:
        typer.secho(f"Error: Step '{step}' not found in manifest.", fg=typer.colors.RED)
        raise typer.Exit(code=1)


    # 4. Locate Proposal (Standard flow for requirements, design, tasks, etc)
    proposal_path = root / ".gap/proposals" / step_def.artifact
    if not proposal_path.exists():
        typer.secho(f"Error: No proposal found for step '{step}' at {proposal_path}.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    # 4. Move to Live (The Gate) - with atomic rollback
    target_path = root / step_def.artifact
    backup_path = None
    
    try:
        # Backup existing file if present
        if target_path.exists():
            backup_path = target_path.with_suffix(target_path.suffix + ".bak")
            shutil.copy2(target_path, backup_path)
        
        # Move proposal to live
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(proposal_path), str(target_path))
        
        # Update ledger (State Persistence)
        ledger = get_ledger(root, manifest)
        ledger.update_status(step, StepStatus.COMPLETE, approver="user")
        
        # Success - remove backup
        if backup_path and backup_path.exists():
            backup_path.unlink()
        
        typer.secho(f"✅ Approved! Moved to: {target_path}", fg=typer.colors.GREEN)
        
    except Exception as e:
        # Rollback on failure
        if backup_path and backup_path.exists():
            shutil.move(str(backup_path), str(target_path))
            typer.secho("⚠️  Rolled back changes due to error.", fg=typer.colors.YELLOW)
        
        typer.secho(f"❌ Approval failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

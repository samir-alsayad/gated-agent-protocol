import typer
import shutil
import yaml
import time
from pathlib import Path
from datetime import datetime

from gap.core.manifest import load_manifest
from gap.core.state import StepStatus
from gap.core.factory import get_ledger
from gap.core.scope_manifest import ScopeParser

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

    # 3. Special Handling for 'plan' step
    if step == "plan":
        plan_path = root / step_def.artifact
        tasks_path = root / ".gap/tasks.yaml"
        
        if not plan_path.exists():
            typer.secho(f"Error: No plan found at {step_def.artifact}. Please construct the plan manually.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        with open(plan_path) as f:
            plan_data = yaml.safe_load(f)
            
        from gap.core.models import Plan, TaskList
        try:
            plan_obj = Plan(**(plan_data or {}))
        except Exception as e:
            typer.secho(f"❌ Invalid Plan format:\n{e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        if tasks_path.exists():
            with open(tasks_path) as f:
                tasks_data = yaml.safe_load(f)
            if tasks_data:
                task_list = TaskList(**tasks_data)
                task_ids = {t.id for t in task_list.tasks}
                plan_task_ids = set(plan_obj.plan.keys())
                
                missing = task_ids - plan_task_ids
                if missing:
                    typer.secho(f"⚠️  Warning: Plan is missing envelopes for tasks: {', '.join(missing)}", fg=typer.colors.YELLOW)
                    if not typer.confirm("Approve incomplete plan?"):
                        raise typer.Exit(code=0)
                
                extra = plan_task_ids - task_ids
                if extra:
                    typer.secho(f"⚠️  Warning: Plan contains envelopes for unknown tasks: {', '.join(extra)}", fg=typer.colors.YELLOW)
                    
        ledger = get_ledger(root, manifest)
        ledger.update_status(step, StepStatus.COMPLETE, approver="user")
        typer.secho(f"✅ Plan Approved and Locked!", fg=typer.colors.GREEN)
        return

    # 4. Locate Proposal (Standard flow for requirements, design, tasks, etc)
    proposal_path = root / ".gap/proposals" / step_def.artifact
    if not proposal_path.exists():
        typer.secho(f"Error: No proposal found for step '{step}' at {proposal_path}.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    # 4. Extract and Validate ACL (Security Integration)
    with open(proposal_path, 'r') as f:
        content = f.read()
    
    parser = ScopeParser(content=content)
    
    # Warn if no ACL for manual gates
    if step_def.gate:  # gate: true = requires approval
        if not parser.context.allowed_writes and not parser.context.allowed_execs:
            typer.secho(
                "⚠️  Warning: No ACL block found in proposal.",
                fg=typer.colors.YELLOW
            )
            typer.secho(
                "    Next gate will be read-only by default.",
                fg=typer.colors.YELLOW
            )
            if not typer.confirm("Continue with approval?"):
                raise typer.Exit(0)
    
    # Store ACL for next gate's use
    acl_dir = root / ".gap" / "acls"
    acl_dir.mkdir(parents=True, exist_ok=True)
    acl_path = acl_dir / f"{step}.yaml"
    
    with open(acl_path, "w") as f:
        yaml.dump({
            "allow_write": parser.context.allowed_writes,
            "allow_exec": parser.context.allowed_execs
        }, f)
    
    # 5. Move to Live (The Gate) - with atomic rollback
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
        if parser.context.allowed_writes or parser.context.allowed_execs:
            typer.secho(f"🔒 ACL stored for next gate: {acl_path}", fg=typer.colors.BLUE)
        
    except Exception as e:
        # Rollback on failure
        if backup_path and backup_path.exists():
            shutil.move(str(backup_path), str(target_path))
            typer.secho("⚠️  Rolled back changes due to error.", fg=typer.colors.YELLOW)
        
        typer.secho(f"❌ Approval failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

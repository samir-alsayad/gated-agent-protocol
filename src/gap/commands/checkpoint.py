import typer
import yaml
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.factory import get_ledger
from gap.core.state import StepStatus
from gap.core.models import Plan

app = typer.Typer(help="Runtime execution gates.")

@app.command("verify")
def verify(
    task_id: str = typer.Argument(..., help="The ID of the task (e.g. 'T-1')"),
    phase: str = typer.Option("before_start", "--phase", "-p", help="The checkpoint phase (e.g. 'before_start', 'after_completion')"),
    manifest_path: Path = typer.Option(Path("manifest.yaml"), "--manifest", "-m", help="Path to manifest.yaml")
):
    """
    Check if the Agent is allowed to proceed past a specific phase of a task.
    Exits with code 0 (Allowed) or 1 (Blocked).
    """
    try:
        manifest = load_manifest(manifest_path)
        root = manifest_path.parent
        ledger = get_ledger(root, manifest)
        
        plan_path = root / ".gap/plan.yaml"
        if not plan_path.exists():
            typer.secho(f"🛑 Blocked: No plan.yaml found. Cannot authorize execution.", fg=typer.colors.RED)
            raise typer.Exit(1)
            
        with open(plan_path) as f:
            plan_data = yaml.safe_load(f)
            
        try:
            plan = Plan(**(plan_data or {}))
        except Exception as e:
            typer.secho(f"🛑 Blocked: Invalid plan.yaml format: {e}", fg=typer.colors.RED)
            raise typer.Exit(1)
            
        if task_id not in plan.plan:
            typer.secho(f"🛑 Blocked: Task '{task_id}' is not authorized in the Plan envelope.", fg=typer.colors.RED)
            raise typer.Exit(1)
            
        envelope = plan.plan[task_id]
        
        # If this phase is not explicitly listed as a checkpoint, allow progression.
        if phase not in envelope.checkpoints:
            typer.secho(f"🟢 Proceeding: No '{phase}' checkpoint required for {task_id}.", fg=typer.colors.GREEN)
            raise typer.Exit(0)
            
        # Check Ledger for Approval
        step_key = f"checkpoint:{task_id}:{phase}"
        approval = ledger.get_approval(step_key)
        
        if approval and approval.status == StepStatus.COMPLETE:
            typer.secho(f"✅ Pass: '{phase}' checkpoint for {task_id} approved by {approval.approver}.", fg=typer.colors.GREEN)
            raise typer.Exit(0)

        # Blocking
        typer.secho(f"🛑 Checkpoint Reached: {task_id} at phase '{phase}'", fg=typer.colors.RED)
        typer.secho(f"   Action Required by Supervisor:", fg=typer.colors.YELLOW)
        typer.secho(f"   $ gap checkpoint approve {task_id} --phase {phase}", fg=typer.colors.YELLOW)
        raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("approve")
def approve(
    task_id: str = typer.Argument(..., help="The ID of the task to approve (e.g. 'T-1')"),
    phase: str = typer.Option("before_start", "--phase", "-p", help="The checkpoint phase to clear"),
    manifest_path: Path = typer.Option(Path("manifest.yaml"), "--manifest", "-m", help="Path to manifest.yaml")
):
    """
    Manually approve a task checkpoint, clearing it in the ledger.
    """
    try:
        manifest = load_manifest(manifest_path)
        root = manifest_path.parent
        ledger = get_ledger(root, manifest)
        
        step_key = f"checkpoint:{task_id}:{phase}"
        ledger.update_status(step_key, StepStatus.COMPLETE, approver="user")
        
        typer.secho(f"✅ Cleared '{phase}' checkpoint for {task_id}", fg=typer.colors.GREEN)
        
    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

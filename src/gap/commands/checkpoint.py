import typer
import sys
from pathlib import Path
from gap.core.manifest import load_manifest, CheckpointStrategy
from gap.core.factory import get_ledger
from gap.core.state import StepStatus

app = typer.Typer(help="Runtime execution gates.")

@app.command("verify")
def verify(
    task_id: str = typer.Argument(..., help="The ID of the task about to be executed (e.g. 'Task-1')"),
    manifest_path: Path = typer.Option("manifest.yaml", "--manifest", "-m", help="Path to manifest.yaml"),
    root: Path = typer.Option(Path.cwd(), "--root", "-r", help="Project root directory"),
):
    """
    Check if the Agent is allowed to proceed with the given task.
    Exits with code 0 (Allowed) or 1 (Blocked).
    """
    try:
        manifest = load_manifest(manifest_path)
        ledger = get_ledger(root, manifest)
        
        # 1. Check Strategy
        config = manifest.checkpoints
        if not config:
            # Default: No checkpoints implies RUN? Or explicit-none?
            # Safe default: Allow run if not configured.
            typer.secho(f"🟢 No checkpoints configured. Proceeding.", fg=typer.colors.GREEN)
            raise typer.Exit(0)
            
        strategy = config.strategy
        
        # 2. Determine if Pause is Required
        should_pause = False
        
        if strategy == CheckpointStrategy.EVERY:
            should_pause = True
        elif strategy == CheckpointStrategy.EXPLICIT:
            if task_id in config.after_tasks:
                should_pause = True
        elif strategy == CheckpointStrategy.BATCH:
            should_pause = False
            
        if not should_pause:
             typer.secho(f"🟢 Checkpoint passed (Strategy: {strategy}). Proceeding.", fg=typer.colors.GREEN)
             raise typer.Exit(0)
             
        # 3. Check Ledger for Approval
        step_key = f"task:{task_id}"
        approval = ledger.get_approval(step_key)
        
        if approval and approval.status == StepStatus.COMPLETE:
            typer.secho(f"✅ Checkpoint approved by {approval.approver}. Proceeding.", fg=typer.colors.GREEN)
            raise typer.Exit(0)

        # Blocking
        typer.secho(f"🛑 Checkpoint Reached: {task_id}", fg=typer.colors.RED)
        typer.secho(f"   Strategy: {strategy}", fg=typer.colors.YELLOW)
        typer.secho(f"   Action Required: gap checkpoint approve {task_id}", fg=typer.colors.YELLOW)
        raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

@app.command("approve")
def approve(
    task_id: str = typer.Argument(..., help="The ID of the task to approve (e.g. 'Task-1')"),
    manifest_path: Path = typer.Option("manifest.yaml", "--manifest", "-m", help="Path to manifest.yaml"),
    root: Path = typer.Option(Path.cwd(), "--root", "-r", help="Project root directory"),
):
    """
    Manually approve a task checkpoint.
    """
    try:
        manifest = load_manifest(manifest_path)
        ledger = get_ledger(root, manifest)
        
        step_key = f"task:{task_id}"
        ledger.update_status(step_key, StepStatus.COMPLETE, approver="user")
        
        typer.secho(f"✅ Approved checkpoint for {task_id}", fg=typer.colors.GREEN)
        
    except typer.Exit:
        raise
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(1)

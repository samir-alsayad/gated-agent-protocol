import typer
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.state import StepStatus
from gap.core.factory import get_ledger

app = typer.Typer(help="Verify protocol compliance.")

@app.command("status")
def status(
    path: Path = typer.Argument(..., help="Path to manifest.yaml")
):
    """
    Check the status of a GAP Project.
    """
    try:
        manifest = load_manifest(path)
        root = path.parent
        ledger = get_ledger(root, manifest)
        state = ledger.get_status(manifest)
        
        typer.echo(f"🔍 Protocol: {manifest.name} (Version: {manifest.version})")
        typer.echo("-" * 40)
        
        for step_id, data in state.steps.items():
            icon = "🔒"
            color = typer.colors.RED
            
            if data.status == StepStatus.UNLOCKED: 
                icon = "🟢"
                color = typer.colors.GREEN
            elif data.status == StepStatus.PENDING: 
                icon = "⏳"
                color = typer.colors.YELLOW
            elif data.status == StepStatus.COMPLETE: 
                icon = "✅"
                color = typer.colors.BLUE
            elif data.status == StepStatus.LOCKED:
                icon = "🔒"
                color = typer.colors.WHITE
            elif data.status == StepStatus.INVALID:
                icon = "⚠️"
                color = typer.colors.RED
            
            typer.secho(f"{icon} {step_id}: {data.status.value}", fg=color)
            
            # Show warning for INVALID status
            if data.status == StepStatus.INVALID:
                typer.secho(
                    f"   └─ WARNING: File exists but dependencies not met (state machine bypassed)",
                    fg=typer.colors.RED
                )
            
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

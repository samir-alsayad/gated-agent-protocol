import typer
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.state import StepStatus
from gap.core.factory import get_ledger
from gap.core.validator import ManifestValidator

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


@app.command("manifest")
def check_manifest(
    path: Path = typer.Argument(..., help="Path to manifest.yaml")
):
    """
    Validate manifest structure and dependencies.
    Detects circular dependencies, missing references, and other configuration errors.
    """
    try:
        manifest = load_manifest(path)
        validator = ManifestValidator()
        errors = validator.validate(manifest)
        
        if errors:
            typer.secho(f"❌ Manifest validation failed ({len(errors)} issues found):", fg=typer.colors.RED)
            typer.echo()
            for err in errors:
                if err.severity == "error":
                    typer.secho(f"  • {err.message}", fg=typer.colors.RED)
                else:
                    typer.secho(f"  • {err.message}", fg=typer.colors.YELLOW)
            raise typer.Exit(code=1)
        
        typer.secho(f"✅ Manifest is valid", fg=typer.colors.GREEN)
        typer.echo(f"   Protocol: {manifest.name} v{manifest.version}")
        typer.echo(f"   Steps: {len(manifest.flow)}")
        
    except FileNotFoundError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
@app.command("traceability")
def check_traceability(
    path: Path = typer.Argument(..., help="Path to manifest.yaml")
):
    """
    Validate referential integrity (The Trinity).
    Ensures: Tasks -> Design Properties -> Requirements.
    """
    from gap.core.auditor import TraceabilityAuditor
    
    try:
        manifest = load_manifest(path)
        root = path.parent
        auditor = TraceabilityAuditor(root, manifest)
        errors = auditor.audit()
        
        if errors:
            has_errors = any(e.severity == "error" for e in errors)
            title = "❌ Traceability Audit failed:" if has_errors else "⚠️ Traceability Audit found warnings:"
            color = typer.colors.RED if has_errors else typer.colors.YELLOW
            
            typer.secho(title, fg=color)
            for err in errors:
                err_color = typer.colors.RED if err.severity == "error" else typer.colors.YELLOW
                typer.secho(f"  • {err}", fg=err_color)
            
            if has_errors:
                raise typer.Exit(code=1)
        else:
            typer.secho("✅ Traceability is healthy. All items are linked to their pedigree.", fg=typer.colors.GREEN)
            
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

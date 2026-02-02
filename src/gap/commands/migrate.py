import typer
from pathlib import Path
from gap.core.manifest import load_manifest
from gap.core.ledger import YamlLedger
from gap.core.sql_ledger import SqlLedger
from gap.core.state import StepStatus
import os

app = typer.Typer(help="Migrate state from YAML to SQL.")

@app.command("run")
def run(
    manifest_path: Path = typer.Option(Path("manifest.yaml"), "--manifest", "-m", help="Path to manifest.yaml"),
    db_url: str = typer.Option(None, "--db", help="Target Database URL (defaults to env var GAP_DB_URL)")
):
    """
    Migrate the current project's .gap/status.yaml to the target SQL database.
    """
    # 1. Resolve DB URL
    target_db = db_url or os.environ.get("GAP_DB_URL")
    if not target_db:
        typer.secho("Error: No database URL provided. Set GAP_DB_URL or use --db.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    # 2. Load Context
    if not manifest_path.exists():
        typer.secho("Error: Manifest not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    manifest = load_manifest(manifest_path)
    root = manifest_path.parent
    
    # 3. Load Source (YAML)
    source_ledger = YamlLedger(root)
    # We need access to the raw data, but Ledger interface abstracts it.
    # However, YamlLedger.get_status returns "Calculated" status (Hybrid).
    # We want the *recorded* status from status.yaml to preserve history (timestamps/approvers).
    # So we should probably peek at the file directly, OR trust the YamlLedger implementation?
    
    # YamlLedger.get_status reads the file and merges with reality. 
    # That's actually GOOD. We want to migrate the "Effective State".
    # BUT, we also want the metadata (Approver/Timestamp) which might be lost if we only look at calculated state?
    # YamlLedger.get_status DOES preserve metadata if the step is complete.
    
    current_status = source_ledger.get_status(manifest)
    
    # 4. Load Target (SQL)
    target_ledger = SqlLedger(
        db_url=target_db,
        project_name=manifest.name,
        protocol=manifest.kind + "-" + manifest.version, # Rough protocol ID
        root=root
    )
    
    # 5. Execute Migration
    typer.echo(f"🚀 Migrating Project '{manifest.name}' to {target_db}...")
    
    count = 0
    for step_name, data in current_status.steps.items():
        if data.status == StepStatus.COMPLETE:
            # Use data.timestamp and data.approver
            ts = None
            if data.timestamp:
                try:
                    # Parse ISO format back to datetime
                    # Simple fromisoformat
                    from datetime import datetime
                    ts = datetime.fromisoformat(data.timestamp)
                except ValueError:
                    pass
            
            target_ledger.update_status(
                step=step_name, 
                status=StepStatus.COMPLETE, 
                approver=data.approver or "migration_tool",
                timestamp=ts
            )
            count += 1
            
    typer.secho(f"✅ Migrated {count} steps to SQL.", fg=typer.colors.GREEN)

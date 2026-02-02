import os
from pathlib import Path
from typing import Optional

from gap.core.ledger import Ledger, YamlLedger
from gap.core.sql_ledger import SqlLedger
from gap.core.manifest import GapManifest

def get_ledger(root: Path, manifest: GapManifest) -> Ledger:
    """
    Factory to return the appropriate Ledger implementation.
    Prioritizes SQL if GAP_DB_URL is set, otherwise defaults to YAML.
    
    Args:
        root: Project root directory
        manifest: Loaded manifest (required for SQL ledger initialization)
    
    Returns:
        Ledger implementation (YamlLedger or SqlLedger)
    """
    db_url = os.environ.get("GAP_DB_URL")
    
    if db_url:
        # Use SQL ledger with project metadata from manifest
        return SqlLedger(
            db_url=db_url,
            project_name=manifest.name,
            protocol=f"{manifest.kind}-{manifest.version}",
            root=root
        )
    
    # Default to YAML ledger
    return YamlLedger(root)

import os
from pathlib import Path
from typing import Optional

from gap.core.ledger import Ledger, YamlLedger
from gap.core.manifest import GapManifest

def get_ledger(root: Path, manifest: GapManifest) -> Ledger:
    """
    Factory to return the appropriate Ledger implementation.
    Returns the YamlLedger (in GAP, the ledger is always a simple file).
    
    Args:
        root: Project root directory
        manifest: Loaded manifest
    
    Returns:
        Ledger implementation (YamlLedger)
    """
    return YamlLedger(root)


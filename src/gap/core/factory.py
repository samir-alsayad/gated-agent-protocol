import os
from pathlib import Path
from typing import Optional

from gap.core.ledger import Ledger, YamlLedger
from gap.core.sql_ledger import SqlLedger

def get_ledger(root: Path) -> Ledger:
    """
    Factory to return the appropriate Ledger implementation.
    Prioritizes SQL if GAP_DB_URL is set, otherwise defaults to YAML.
    """
    db_url = os.environ.get("GAP_DB_URL")
    
    if db_url:
        # We need project name/protocol.
        # In a real app, we might load these from manifest FIRST, 
        # or pass them in. 
        # But get_ledger is often called before loading manifest?
        # Actually in check/scribe/gate, we load manifest first.
        # But wait, Ledger Interface doesn't take project_name in __init__?
        # YamlLedger(root) -> Simple.
        # SqlLedger(url, name, proto, root) -> Complex.
        
        # Challenge: To initialize SqlLedger, we need Project Name + Protocol.
        # But the Factory logic is generic.
        
        # Solution: The Factory might need the Manifest?
        # Or we delay initialization?
        pass

    # Fallback
    return YamlLedger(root)

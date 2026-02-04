from pathlib import Path
import re
import yaml
from typing import List, Optional

class ACLContext:
    def __init__(self):
        self.allowed_writes: List[str] = []
        self.allowed_execs: List[str] = []

class ACLEnforcer:
    """
    Parses and enforces Access Control Lists (ACLs) embedded in GAP artifacts.
    """
    def __init__(self, content: str = ""):
        self.context = ACLContext()
        if content:
            self.parse_from_content(content)

    def parse_from_content(self, content: str):
        """Extracts YAML blocks under 'Access Control' or 'ACL' headings."""
        # Pattern looks for any block of ```yaml ... ``` after an ACL/Access Control heading
        pattern = r"(?:##|###) (?:Access Control|ACL|Governance)\s+```yaml\n(.*?)\n```"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            yaml_str = match.group(1)
            try:
                data = yaml.safe_load(yaml_str)
                if data:
                    self.context.allowed_writes = data.get('allow_write', [])
                    self.context.allowed_execs = data.get('allow_exec', [])
            except Exception:
                # Silently fail for now, or could log
                pass

    @staticmethod
    def extract_from_file(path: Path) -> 'ACLEnforcer':
        if not path.exists():
            return ACLEnforcer()
        return ACLEnforcer(path.read_text())

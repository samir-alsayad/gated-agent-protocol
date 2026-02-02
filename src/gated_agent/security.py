import yaml
import fnmatch
import os
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ACLContext:
    allowed_writes: List[str]
    allowed_execs: List[str]

class ACLEnforcer:
    """
    The Security Kernel for GAP.
    Extracts embedded ACL blocks from Markdown artifacts and enforces them.
    """
    def __init__(self, artifact_path: Optional[str] = None, content: Optional[str] = None):
        if content:
            self.context = self._parse_content(content)
        elif artifact_path:
            self.context = self._parse_from_file(artifact_path)
        else:
            self.context = ACLContext([], [])

    def _parse_from_file(self, artifact_path: str) -> ACLContext:
        try:
            with open(artifact_path, 'r') as f:
                content = f.read()
            return self._parse_content(content)
        except Exception as e:
            print(f"[GAP SECURITY] Failed to read ACL file {artifact_path}: {e}")
            return ACLContext([], [])
    
    def _parse_content(self, content: str) -> ACLContext:
        """
        Scans markdown content for the '## Access Control' section and parses the YAML block.
        """
        try:
            # Regex to find the Access Control section and the first YAML block within it
            # Supports both ```yaml and '''yaml formats
            pattern = r"##\s+Access Control.*?\n```yaml\n(.*?)\n```"
            match = re.search(pattern, content, re.DOTALL)

            if not match:
                # Try alternative format with single quotes
                pattern = r"##\s+Access Control.*?\n'''yaml\n(.*?)\n'''"
                match = re.search(pattern, content, re.DOTALL)

            if not match:
                return ACLContext([], [])
            
            yaml_content = match.group(1)
            data = yaml.safe_load(yaml_content) or {}
            
            return ACLContext(
                allowed_writes=data.get("allow_write", []),
                allowed_execs=data.get("allow_exec", [])
            )
            
        except Exception as e:
            print(f"[GAP SECURITY] Failed to parse ACL: {e}")
            return ACLContext([], [])

    def validate_write(self, target_path: str) -> bool:
        """
        Intervention Hook: Should we allow writing to this path?
        """
        # 1. Normalize path
        normalized = os.path.normpath(target_path)
        
        # 2. Check whitelist (Globs supported)
        for pattern in self.context.allowed_writes:
            if fnmatch.fnmatch(normalized, pattern):
                return True
                
        # 3. Deny by default
        raise PermissionError(f"[GAP SECURITY] WRITE DENIED: '{target_path}' is not in the ACL Whitelist.")

    def validate_exec(self, command: str) -> bool:
        """
        Intervention Hook: Should we allow this shell command?
        """
        # Exact match or prefix match required
        for pattern in self.context.allowed_execs:
            if command == pattern or command.startswith(pattern):
                return True
                
        raise PermissionError(f"[GAP SECURITY] EXEC DENIED: '{command}' is not in the ACL Whitelist.")
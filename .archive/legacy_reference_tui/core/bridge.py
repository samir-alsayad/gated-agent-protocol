from pathlib import Path
from ..security.safety import is_safe_path
from ..security.acl import parse_acl

class FileSystemBridge:
    def __init__(self, root: Path, acl_whitelist: set = None):
        self.root = root
        self.acl_whitelist = acl_whitelist or set()

    def write_artifact(self, path: str, content: str, allowed_path: str = None) -> bool:
        """
        Writes content to path, enforcing Safety and ACL.
        Returns True if successful, False if blocked.
        """
        if not is_safe_path(self.root, path):
            print(f"🛑 SECURITY ALERT: Attempted write to unsafe path: {path}")
            return False
            
        # 1. SPEC CHECK (Global Whitelist)
        if self.acl_whitelist:
            if Path(path).name not in self.acl_whitelist:
                 print(f"🛑 ACL VIOLATION: '{Path(path).name}' is NOT in the Approved Access Control List.")
                 # print(f"   Allowed: {self.acl_whitelist}")
                 return False

        # 2. TASK PROMISE CHECK (Finer grain)
        if allowed_path:
             target = Path(path).name
             allowed = Path(allowed_path).name
             if target != allowed:
                 print(f"🛑 TASK VIOLATION: Agent tried to write to '{target}' but Task Promise was '{allowed}'")
                 return False

        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            f.write(content)
        print(f"   -> Written to {path}")
        return True

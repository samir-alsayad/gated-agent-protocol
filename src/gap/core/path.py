from pathlib import Path
from typing import Optional
from gap.core.manifest import GapManifest

class PathManager:
    def __init__(self, root: Optional[Path] = None):
        self.package_root = Path(__file__).parent.parent # src/gap
        if root is None:
            self.root = self.package_root / "protocols"
        else:
            self.root = root
        
    def resolve_template(self, manifest: GapManifest, name: str) -> Path:
        """
        1. Check Local Templates (in manifest.templates)
        2. Check Parent Protocols
        """
        # 1. Local Lookup
        # Check explicit mapping first
        if name in manifest.templates:
            # Try finding it relative to root (Project override)
            mapped_path = self.root / manifest.templates[name]
            if mapped_path.exists():
                return mapped_path
            
            # Try finding it relative to package protocols (if root failed)
            # This handles cases where manifest points to 'protocols/instructional/...' 
            # and we are running from a random dir.
            pkg_mapped_path = self.package_root / manifest.templates[name]
            if pkg_mapped_path.exists():
                return pkg_mapped_path
                
        # Default Convention
        local_path = self.root / f"templates/{name}.md"
        if local_path.exists():
            return local_path
            
        # Hardcoded Parent Check (Simulating Inheritance for now)
        # In the real engine, we would load the 'extends' path dynamically.
        if name == "course" or name == "campaign":
             # Fallback to Instructional Protocol (Internal Package)
             protocol_path = self.package_root / "protocols/instructional/templates/course.md"
             if protocol_path.exists():
                 return protocol_path
                 
        raise FileNotFoundError(f"Template '{name}' not found.")
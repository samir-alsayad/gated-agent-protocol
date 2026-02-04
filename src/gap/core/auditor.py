import re
from pathlib import Path
from typing import List, Dict, Set, Optional
from gap.core.validator import ValidationError

class TraceabilityAuditor:
    """
    Audits GAP artifacts for referential integrity (The Trinity).
    Ensures: Tasks -> Design Properties -> Requirements.
    """
    
    # ID Patterns
    ID_PATTERN = r"(?:(?:G|R|FR|NFR|DP|PROP|P|TASK|H|T)-[A-Z0-9_\-]+)|(?:<!-- id: (.*?) -->)"
    
    # Citation Patterns
    TRACES_TO_PATTERN = r"\(Traces to: (.*?)\)"
    VALIDATES_PATTERN = r"\(Validates: (.*?)\)"

    def __init__(self, root: Path):
        self.root = root

    def audit(self) -> List[ValidationError]:
        """Performs a full audit of the project artifacts."""
        errors = []
        
        # 1. Parse all IDs
        req_ids = self._extract_ids(self.root / "specs/requirements.md")
        design_ids = self._extract_ids(self.root / "specs/design.md")
        task_ids = self._extract_ids(self.root / "specs/tasks.md")
        
        # 2. Check Design -> Requirements
        errors.extend(self._audit_links(
            self.root / "specs/design.md", 
            valid_targets=req_ids, 
            link_pattern=self.VALIDATES_PATTERN,
            context="Design Property"
        ))

        # 3. Check Tasks -> Design/Requirements
        valid_task_targets = design_ids | req_ids
        errors.extend(self._audit_links(
            self.root / "specs/tasks.md", 
            valid_targets=valid_task_targets, 
            link_pattern=self.TRACES_TO_PATTERN,
            context="Task"
        ))
        
        # 4. Check for Orphans (Items with no outbound link)
        # We only enforce this for non-Requirements
        errors.extend(self._check_orphans(self.root / "specs/design.md", self.VALIDATES_PATTERN, "Design Property"))
        errors.extend(self._check_orphans(self.root / "specs/tasks.md", self.TRACES_TO_PATTERN, "Task"))

        return errors

    def _extract_ids(self, path: Path) -> Set[str]:
        """Extracts all IDs defined in a file."""
        if not path.exists():
            return set()
        
        content = path.read_text()
        ids = set()
        
        # Match standard IDs (R-01, etc)
        matches = re.finditer(self.ID_PATTERN, content)
        for match in matches:
            if match.group(0).startswith("<!--"):
                ids.add(match.group(1)) # Group 1 is for HTML comments
            else:
                ids.add(match.group(0))
        
        return ids

    def _audit_links(self, path: Path, valid_targets: Set[str], link_pattern: str, context: str) -> List[ValidationError]:
        """Checks if citations in a file point to existing IDs."""
        if not path.exists():
            return []
        
        errors = []
        content = path.read_text()
        
        matches = re.finditer(link_pattern, content)
        for match in matches:
            raw_targets = match.group(1)
            # Split by comma for multiple targets
            targets = [t.strip() for t in raw_targets.split(",")]
            
            for target in targets:
                if target not in valid_targets:
                    errors.append(ValidationError(
                        f"{context} in {path.name} cites unknown ID: '{target}'",
                        severity="error"
                    ))
        
        return errors

    def _check_orphans(self, path: Path, link_pattern: str, context: str) -> List[ValidationError]:
        """Ensures every item has at least one outbound link."""
        if not path.exists():
            return []
        
        errors = []
        content = path.read_text()
        
        # Simple heuristic: Split by list items or sections
        # This is L1 (Syntactic), so we look for lines starting with - or * that define an ID
        lines = content.splitlines()
        for line in lines:
            line = line.strip()
            # If the line defines an ID (e.g. * **P-01**)
            found_id = re.search(self.ID_PATTERN, line)
            if found_id:
                # But does NOT have a link
                if not re.search(link_pattern, line):
                    errors.append(ValidationError(
                        f"Orphaned Intent: {context} '{found_id.group(0)}' has no traceability link.",
                        severity="warning"
                    ))
        
        return errors

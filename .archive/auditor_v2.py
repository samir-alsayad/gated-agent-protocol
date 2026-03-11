import re
from pathlib import Path
from typing import List, Dict, Set, Optional
from gap.core.validator import ValidationError
from gap.core.manifest import GapManifest

class TraceabilityAuditor:
    """
    Simpler, regex-based auditor for Markdown artifacts.
    Ensures: Tasks -> Design Properties -> Requirements.
    """
    
    # ID Patterns (e.g., R-01, DP-01, T-01)
    ID_PATTERN = r"(?:(?:G|R|FR|NFR|DP|PROP|P|T|H)-[A-Z0-9_\-]+)|(?:<!-- id: (.*?) -->)"
    
    # Citation Patterns
    TRACES_TO_PATTERN = r"\(Traces to: (.*?)\)"
    VALIDATES_PATTERN = r"\(Validates: (.*?)\)"

    def __init__(self, root: Path, manifest: GapManifest):
        self.root = root
        self.manifest = manifest
        self._artifact_map = {step.step: step.artifact for step in manifest.get_flat_steps()}

    def _get_artifact_path(self, step_id: str) -> Optional[Path]:
        if step_id in self._artifact_map:
            # Handle glob patterns if necessary, but scribe usually targets single files
            artifact_str = self._artifact_map[step_id]
            if "*" in artifact_str:
                return None # Skip directory check for now
            return self.root / artifact_str
        return None

    def audit(self) -> List[ValidationError]:
        """Performs a full audit of the project artifacts via regex."""
        errors = []
        
        req_path = self._get_artifact_path("requirements")
        design_path = self._get_artifact_path("design")
        tasks_path = self._get_artifact_path("tasks")
        
        # 1. Parse all IDs
        req_ids = self._extract_ids(req_path) if req_path else set()
        design_ids = self._extract_ids(design_path) if design_path else set()
        
        # 2. Check Design -> Requirements
        if design_path:
            errors.extend(self._audit_links(
                design_path, 
                valid_targets=req_ids, 
                link_pattern=self.VALIDATES_PATTERN,
                context="Design Property"
            ))

        # 3. Check Tasks -> (Design | Requirements)
        if tasks_path:
            valid_task_targets = design_ids | req_ids
            errors.extend(self._audit_links(
                tasks_path,
                valid_targets=valid_task_targets,
                link_pattern=self.TRACES_TO_PATTERN,
                context="Task"
            ))
            
            # Check for orphans in tasks
            errors.extend(self._check_orphans(tasks_path, self.TRACES_TO_PATTERN, "Task"))

        # 4. Check for Orphans in Design
        if design_path:
            errors.extend(self._check_orphans(design_path, self.VALIDATES_PATTERN, "Design Property"))

        return errors

    def _extract_ids(self, path: Path) -> Set[str]:
        if not path or not path.exists():
            return set()
        
        content = path.read_text()
        ids = set()
        matches = re.finditer(self.ID_PATTERN, content)
        for match in matches:
            if match.group(0).startswith("<!--"):
                ids.add(match.group(1))
            else:
                ids.add(match.group(0))
        return ids

    def _audit_links(self, path: Path, valid_targets: Set[str], link_pattern: str, context: str) -> List[ValidationError]:
        if not path or not path.exists():
            return []
        
        errors = []
        content = path.read_text()
        matches = re.finditer(link_pattern, content)
        for match in matches:
            raw_targets = match.group(1)
            targets = [t.strip() for t in raw_targets.split(",")]
            for target in targets:
                if target not in valid_targets:
                    errors.append(ValidationError(
                        f"{context} in {path.name} cites unknown ID: '{target}'",
                        severity="error"
                    ))
        return errors

    def _check_orphans(self, path: Path, link_pattern: str, context: str) -> List[ValidationError]:
        if not path or not path.exists():
            return []
        
        errors = []
        lines = path.read_text().splitlines()
        for line in lines:
            line = line.strip()
            found_id = re.search(self.ID_PATTERN, line)
            if found_id:
                if not re.search(link_pattern, line):
                    errors.append(ValidationError(
                        f"Orphaned Intent: {context} '{found_id.group(0)}' has no traceability link.",
                        severity="warning"
                    ))
        return errors

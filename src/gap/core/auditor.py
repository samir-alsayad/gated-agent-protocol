import re
from pathlib import Path
import yaml
from typing import List, Dict, Set, Optional
from gap.core.validator import ValidationError
from gap.core.manifest import GapManifest
from gap.core.models import TaskList

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

    def __init__(self, root: Path, manifest: GapManifest):
        self.root = root
        self.manifest = manifest
        self._artifact_map = {step.step: step.artifact for step in manifest.get_flat_steps()}

    def _get_artifact_path(self, step_id: str) -> Optional[Path]:
        if step_id in self._artifact_map:
            return self.root / self._artifact_map[step_id]
        return None

    def audit(self) -> List[ValidationError]:
        """Performs a full audit of the project artifacts."""
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

        # 3. Check Tasks YAML
        if tasks_path and tasks_path.exists():
            valid_task_targets = design_ids | req_ids
            errors.extend(self._audit_yaml_tasks(tasks_path, valid_task_targets))
        
        # 4. Check for Orphans in MD files
        if design_path:
            errors.extend(self._check_orphans(design_path, self.VALIDATES_PATTERN, "Design Property"))

        return errors

    def _audit_yaml_tasks(self, path: Path, valid_targets: Set[str]) -> List[ValidationError]:
        errors = []
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)
            
            if not data:
                return []
                
            task_list = TaskList(**data)
            for task in task_list.tasks:
                if not task.traces_to:
                    errors.append(ValidationError(
                        f"Orphaned Intent: Task '{task.id}' has no traceability link.",
                        severity="warning"
                    ))
                else:
                    targets = [t.strip() for t in task.traces_to.split(",")]
                    for t in targets:
                        if t not in valid_targets:
                            errors.append(ValidationError(
                                f"Task '{task.id}' cites unknown ID: '{t}'",
                                severity="error"
                            ))
        except Exception as e:
            errors.append(ValidationError(f"Failed to parse tasks YAML: {e}", severity="error"))
            
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

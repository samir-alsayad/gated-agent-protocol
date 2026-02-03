"""
Manifest validation to detect configuration errors before runtime.
"""
from typing import List, Set, Dict
from gap.core.manifest import GapManifest


class ValidationError:
    def __init__(self, message: str, severity: str = "error"):
        self.message = message
        self.severity = severity
    
    def __str__(self):
        return f"[{self.severity.upper()}] {self.message}"


class ManifestValidator:
    """Validates manifest structure and dependencies."""
    
    def validate(self, manifest: GapManifest) -> List[ValidationError]:
        """Run all validation checks and return list of errors."""
        errors = []
        errors.extend(self._check_circular_deps(manifest))
        errors.extend(self._check_missing_refs(manifest))
        errors.extend(self._check_duplicate_steps(manifest))
        errors.extend(self._check_self_dependency(manifest))
        return errors
    
    def _check_circular_deps(self, manifest: GapManifest) -> List[ValidationError]:
        """Detect circular dependencies using topological sort."""
        errors = []
        
        # Build adjacency list
        graph: Dict[str, List[str]] = {}
        for step in manifest.flow:
            graph[step.step] = step.needs
        
        # Track visited nodes and recursion stack
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        
        def has_cycle(node: str, path: List[str]) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, path.copy()):
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    errors.append(ValidationError(
                        f"Circular dependency detected: {' -> '.join(cycle)}",
                        severity="error"
                    ))
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Check each node
        for step in manifest.flow:
            if step.step not in visited:
                has_cycle(step.step, [])
        
        return errors
    
    def _check_missing_refs(self, manifest: GapManifest) -> List[ValidationError]:
        """Verify all 'needs' references point to valid steps."""
        errors = []
        
        # Build set of valid step names
        valid_steps = {step.step for step in manifest.flow}
        
        for step in manifest.flow:
            for dep in step.needs:
                if dep not in valid_steps:
                    errors.append(ValidationError(
                        f"Step '{step.step}' depends on unknown step '{dep}'",
                        severity="error"
                    ))
        
        return errors
    
    def _check_duplicate_steps(self, manifest: GapManifest) -> List[ValidationError]:
        """Check for duplicate step IDs."""
        errors = []
        seen = set()
        
        for step in manifest.flow:
            if step.step in seen:
                errors.append(ValidationError(
                    f"Duplicate step ID: '{step.step}'",
                    severity="error"
                ))
            seen.add(step.step)
        
        return errors
    
    def _check_self_dependency(self, manifest: GapManifest) -> List[ValidationError]:
        """Check if any step depends on itself."""
        errors = []
        
        for step in manifest.flow:
            if step.step in step.needs:
                errors.append(ValidationError(
                    f"Step '{step.step}' depends on itself",
                    severity="error"
                ))
        
        return errors

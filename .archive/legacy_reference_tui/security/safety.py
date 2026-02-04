from pathlib import Path

def is_safe_path(root: Path, path_str: str) -> bool:
    """
    Prevent traversal attacks (e.g. ../../etc/passwd).
    Ensures path_str is within root.
    """
    try:
        target = (root / path_str).resolve()
        resolved_root = root.resolve()
        return resolved_root in target.parents or target == resolved_root
    except Exception:
        return False

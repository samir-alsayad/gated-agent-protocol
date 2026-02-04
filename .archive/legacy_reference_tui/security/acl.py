from pathlib import Path
import re
import yaml

def parse_acl(root: Path) -> set:
    """
    Extracts ACL YAML from specs/tasks.md.
    Returns a set of allowed filenames.
    """
    p = root / "specs/tasks.md"
    if not p.exists():
        return set()
        
    with open(p, "r") as f:
        content = f.read()
    
    # Extract YAML block under ## Access Control
    # Pattern looks for ## Access Control\n```yaml\n(content)\n```
    pattern = r"## Access Control\s+```yaml\n(.*?)\n```"
    match = re.search(pattern, content, re.DOTALL)
    
    allowed_files = set()
    if match:
        yaml_str = match.group(1)
        try:
            data = yaml.safe_load(yaml_str)
            if data and 'allow_write' in data:
                allowed_files = set(data['allow_write'])
                print(f"🔒 ACL Loaded: {len(allowed_files)} file(s) whitelisted.")
        except Exception as e:
            print(f"⚠️ Failed to parse ACL: {e}")
    
    # SYSTEM ARTIFACTS (Implicitly Whitelisted)
    allowed_files.add("walkthrough.md")
    
    return allowed_files

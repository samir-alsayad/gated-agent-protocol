import re
from pathlib import Path
from typing import List

class FlowStep:
    def __init__(self, name, artifact, category):
        self.name = name
        self.step = name
        self.artifact = artifact
        self.category = category

class Task:
    """Represents an execution task parsed from tasks.md"""
    def __init__(self, id, file, status="pending", phase_class=None):
        self.id = id
        self.file = file
        self.status = status
        self.phase_class = phase_class  # 'alignment' or 'execution'

    def __repr__(self):
        return f"Task({self.id}, {self.file}, {self.status}, {self.phase_class})"

def parse_tasks(tasks_path: Path) -> List[Task]:
    """Simple parser for GAP tasks.md using [ ] and (File: ...) markers."""
    if not tasks_path.exists():
        return []
        
    tasks = []
    content = tasks_path.read_text()
    
    # regex to find patterns like: - [ ] T-01: ... (File: src/main.py)
    pattern = r"- \[ \] ([\w-]+): .*\(File: (.*)\)"
    matches = re.finditer(pattern, content)
    
    for match in matches:
        t_id = match.group(1)
        t_file = match.group(2).strip()
        tasks.append(Task(t_id, t_file))
        
    return tasks

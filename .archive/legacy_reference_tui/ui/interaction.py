import json
from datetime import datetime
from pathlib import Path

class InteractionManager:
    def __init__(self, root: Path):
        self.root = root
        
        # Session Logging
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = self.root / ".gap/sessions"
        self.session_log_file = self.log_dir / f"{self.session_id}.log.jsonl"

    def log(self, entry):
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
        entry['timestamp'] = datetime.now().isoformat()
        with open(self.session_log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def ask_human(self, task_id, context=""):
        print(f"\n✋ GAP INTERRUPTION: Authorization Required for '{task_id}'")
        if context:
            print(f"   Context: {context}")
        print(f"   >> Approve? (y/n)")
        choice = input("   > ").strip().lower()
        
        self.log({
            "type": "human_interaction",
            "task_id": task_id,
            "choice": choice
        })
        
        return choice

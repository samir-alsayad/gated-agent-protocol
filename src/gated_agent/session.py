import os
import shutil
import yaml
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict

class BaseSessionManager(ABC):
    """Abstract interface for GAP session persistence."""
    
    @abstractmethod
    def start_session(self, protocol_id: str) -> str:
        """Initialize a new session and return its ID."""
        pass

    @abstractmethod
    def archive_artifact(self, session_id: str, filename: str, content: str):
        """Store an artifact in the session archive."""
        pass

    @abstractmethod
    def get_history(self, session_id: str) -> Dict[str, str]:
        """Retrieve all archived artifacts for a session."""
        pass

class LocalSessionManager(BaseSessionManager):
    """Default implementation using the local .gap directory."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = os.path.abspath(project_root)
        self.gap_dir = os.path.join(self.project_root, ".gap")
        self.sessions_dir = os.path.join(self.gap_dir, "sessions")
        self.config_path = os.path.join(self.gap_dir, "gap.yaml")

    def _ensure_gap(self):
        """Ensure .gap structure exists."""
        os.makedirs(self.sessions_dir, exist_ok=True)
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                yaml.dump({"active_session": None, "sessions": []}, f)

    def start_session(self, protocol_id: str) -> str:
        self._ensure_gap()
        session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{protocol_id}"
        session_path = os.path.join(self.sessions_dir, session_id)
        os.makedirs(session_path, exist_ok=True)
        
        # Update config
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f) or {}
        
        config["active_session"] = session_id
        if "sessions" not in config: config["sessions"] = []
        if session_id not in config["sessions"]:
            config["sessions"].append(session_id)
            
        with open(self.config_path, "w") as f:
            yaml.dump(config, f)
            
        return session_id

    def archive_artifact(self, session_id: str, filename: str, content: str):
        session_path = os.path.join(self.sessions_dir, session_id)
        if not os.path.exists(session_path):
            os.makedirs(session_path, exist_ok=True)
            
        archive_path = os.path.join(session_path, filename)
        with open(archive_path, "w") as f:
            f.write(content.strip())

    def get_history(self, session_id: str) -> Dict[str, str]:
        session_path = os.path.join(self.sessions_dir, session_id)
        history = {}
        if os.path.exists(session_path):
            for file in os.listdir(session_path):
                if file.endswith(".md") or file.endswith(".yaml") or file.endswith(".json"):
                    with open(os.path.join(session_path, file), "r") as f:
                        history[file] = f.read()
        return history

class Session:
    """High-level orchestration for GAP sessions."""
    
    def __init__(self, protocol_id: str, manager: Optional[BaseSessionManager] = None):
        self.protocol_id = protocol_id
        self.manager = manager or LocalSessionManager()
        self.session_id = self.manager.start_session(protocol_id)

    def archive(self, filename: str, content: str):
        """Archive an artifact in the session store."""
        self.manager.archive_artifact(self.session_id, filename, content)

    def check_artifact(self, filename: str) -> bool:
        """Check if an artifact exists in the current session."""
        history = self.manager.get_history(self.session_id)
        return filename in history

    def load_context(self) -> str:
        """Returns a combined string of all artifacts in the current session for prompt injection."""
        history = self.manager.get_history(self.session_id)
        context = ""
        for filename, content in history.items():
            context += f"\n--- {filename} ---\n{content}\n"
        return context

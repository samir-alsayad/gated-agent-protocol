from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from .flow import Task

class Harness(ABC):
    """
    Abstract Base Class for GAP Execution Harnesses.
    Defines the contract for executing tasks within a GAP project.
    """
    def __init__(self, root: Path, api_key: str):
        self.root = root
        self.api_key = api_key

    @abstractmethod
    def execute(self, tasks: List[Task], checkpoints: List[str] = None) -> bool:
        """
        Executes a list of tasks.
        Returns True if all tasks completed successfully, False otherwise.
        """
        pass

class HarnessFactory:
    """Factory to create the appropriate harness based on user selection."""
    @staticmethod
    def create(harness_type: str, root: Path, api_key: str, model: str = None) -> Harness:
        if harness_type == "legacy":
            from .harnesses.legacy import LegacyHarness
            return LegacyHarness(root, api_key)
        elif harness_type == "gptme":
            from .harnesses.gptme import GptmeHarness
            return GptmeHarness(root, api_key, model=model)
        else:
            raise ValueError(f"Unknown harness type: {harness_type}")


from pathlib import Path
from typing import List
from ..harness import Harness
from ..flow import Task
from ..bridge import FileSystemBridge
from ..agent.llm import GatedLLM
from ..agent.prompts import Prompts
from ..agent.context import ContextManager
from ..ui.interaction import InteractionManager

class LegacyHarness(Harness):
    """
    The 'Old Model' execution harness.
    Performs step-by-step task execution with gated checkpoints.
    """
    def __init__(self, root: Path, api_key: str):
        super().__init__(root, api_key)
        self.llm = GatedLLM(root, api_key)
        self.bridge = FileSystemBridge(root)
        self.interaction = InteractionManager(root)
        self.context_mgr = ContextManager(root)

    def execute(self, tasks: List[Task], checkpoints: List[str] = None) -> bool:
        checkpoints = checkpoints or []
        print(f"\n🚀 Starting Legacy Execution for {len(tasks)} tasks...")

        for task in tasks:
            print(f"\n--- Task: {task.id} ({task.file}) ---")
            
            # 1. Checkpoint Gate
            if task.id in checkpoints:
                print(f"🛑 GAP CHECKPOINT: {task.id}")
                choice = self.interaction.ask_human("checkpoint", f"Execution paused at task: {task.id}. Proceed?")
                if choice != 'y':
                    print("❌ Execution halted by user.")
                    return False

            # 2. Context & Generation
            context = self.context_mgr.read_all_specs()
            prompt = Prompts.execution_task(task, context)
            
            print(f"    (Agent is working on {task.file}...)")
            content = self.llm.chat(prompt)

            # 3. Write Artifact
            success = self.bridge.write_artifact(task.file, content, allowed_path=task.file)
            if not success:
                print(f"🛑 Execution failed at task {task.id} due to security violation.")
                return False
            
            task.status = "completed"
            
        print("\n✅ Legacy Execution Completed.")
        return True

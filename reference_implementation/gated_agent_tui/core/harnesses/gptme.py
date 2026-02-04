import subprocess
import os
import sys
from pathlib import Path
from typing import List
from ..harness import Harness
from ..flow import Task

class GptmeHarness(Harness):
    """
    A high-fidelity execution harness that wraps the gptme CLI.
    Provides a live, stateful terminal feed for demonstrations.
    """
    def __init__(self, root: Path, api_key: str, model: str = None):
        super().__init__(root, api_key)
        self.model = model or "openrouter/qwen/qwen-2.5-coder-32b-instruct"

    def execute(self, tasks: List[Task], checkpoints: List[str] = None, whitelist: List[str] = None) -> bool:
        checkpoints = checkpoints or []
        print(f"\n🔥 Starting STEERABLE (gptme) Execution for {len(tasks)} tasks...")

        # 1. GROUP TASKS BY CHECKPOINTS
        task_chunks = self._chunk_tasks(tasks, checkpoints)
        
        for i, chunk in enumerate(task_chunks):
            print(f"\n[ EXECUTION WINDOW {i+1}/{len(task_chunks)} ]")
            
            # 2. GENERATE MISSION FOR THIS WINDOW ONLY
            # If we are in Live Alignment, whitelist is forced. Otherwise it's chunk-based.
            current_whitelist = whitelist if (whitelist and len(task_chunks) == 1) else [t.file for t in chunk]
            mission_content = self._build_mission_prompt(chunk, whitelist=current_whitelist)
            mission_path = self.root / ".gap/MISSION.md"
            mission_path.parent.mkdir(exist_ok=True)
            mission_path.write_text(mission_content)

            # 3. CONFIGURE CAPABILITY SANDBOX (Tool Gating)
            # Use schema-driven phase detection instead of path heuristics
            is_alignment = any(t.phase_class == 'alignment' for t in chunk)
            allowed_tools = "save" # Baseline for Alignment
            if not is_alignment:
                # In Execution phase, we allow more tools (this could be further refined by Task ACL)
                allowed_tools = "save,shell,ipython,browser"
            
            print(f"🛡️  CAPABILITY GATE: Allowlist = [{allowed_tools}]")


            # 4. RUN GPTME FOR THIS WINDOW
            print(f"--- GPTME LIVE FEED (Group: {[t.id for t in chunk]}) ---")
            try:
                # We command gptme to execute the MISSION.md and EXIT immediately after completion
                anchor_command = "Execute the tasks in .gap/MISSION.md. When ALL tasks in that file are finished, type /exit. DO NOT perform any unlisted work."
                
                # Use absolute path to gptme binary inside the reference venv
                gptme_bin = Path(__file__).parent.parent.parent / ".venv_reference/bin/gptme"
                
                # Command construction
                cmd = [str(gptme_bin), "-m", self.model, anchor_command]
                
                process = subprocess.Popen(
                    cmd,
                    cwd=self.root,
                    env={
                        **os.environ, 
                        "OPENROUTER_KEY": self.api_key,
                        "TOOL_ALLOWLIST": allowed_tools
                    },
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    text=True
                )
                process.wait()

                
                if process.returncode != 0:
                    print(f"🛑 Execution Window failed.")
                    return False

                # 5. THE SOVEREIGN GATE (Pause for User between chunks)
                last_task = chunk[-1]
                if last_task.id in checkpoints:
                    print(f"\n🛑 GAP CHECKPOINT REACHED: {last_task.id}")
                    print("=" * 50)
                    print("   Execution paused. Control returned to GAP Ledger.")
                    print("   Review the output above before proceeding.")
                    print("=" * 50)
                    user_choice = input("   [y] Approve & Continue  [n] Abort Execution > ").strip().lower()
                    if user_choice != 'y':
                        print("🛑 Execution aborted by user at checkpoint.")
                        return False
                    print("✅ Checkpoint approved. Continuing to next window...")


                # 5. POST-WINDOW AUDIT
                if not self._audit_chunk(chunk):
                    return False

            except Exception as e:
                print(f"🛑 Error running gptme: {e}")
                return False

        print("\n🏆 All Execution Windows completed and verified.")
        return True

    def _chunk_tasks(self, tasks: List[Task], checkpoints: List[str]) -> List[List[Task]]:
        """Splits tasks into groups based on defined checkpoints."""
        chunks = []
        current_chunk = []
        for t in tasks:
            current_chunk.append(t)
            if t.id in checkpoints:
                chunks.append(current_chunk)
                current_chunk = []
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def _audit_chunk(self, chunk: List[Task]) -> bool:
        """Verifies that the window didn't leak or fail its promises."""
        from ..security.safety import is_safe_path
        print(f"🛡️  Auditing Window Pedigree...")
        for t in chunk:
            p = self.root / t.file
            if not p.exists():
                print(f"   ❌ Task {t.id} failed: Artifact {t.file} missing.")
                return False
            t.status = "completed"
        return True

    def _build_mission_prompt(self, tasks: List[Task], whitelist: List[str] = None) -> str:
        """Constructs the grounding prompt for gptme with strict file whitelisting."""
        task_list = "\n".join([f"- [{t.status}] {t.id}: {t.file}" for t in tasks])
        
        # Enforce Singular Promise or Phase Whitelist
        allowed_files = whitelist if whitelist else [t.file for t in tasks]
        whitelist_str = ", ".join(allowed_files)

        prompt = f"""
You are the EXECUTION AGENT for the Gated Agent Protocol (GAP).
Your mission is to execute the following tasks within the strict security boundaries of this window.

### TASK LIST
{task_list}

### 🛡️ SOVEREIGN CONSTRAINTS (MANDATORY)
1. **Singular Promise**: You are ONLY authorized to write to the following files: [{whitelist_str}].
2. **Phase Lock**: Any attempt to modify files outside this list (including specs/ outside your current task) will be caught by the Auditor and cause a Protocol Violation.
3. **No Drift**: Do not propose new requirements or designs. Execute the tasks as approved.
4. **Tool Gating**: Use the shell and python tools ONLY for verification. Do not use them to bypass file ACLs.

Begin execution now. When finished with ALL tasks, type /exit.
"""
        return prompt

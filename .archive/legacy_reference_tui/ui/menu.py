import sys
import os
from pathlib import Path
from ..core.flow import FlowStep, Task
from ..core.state import load_manifest, get_ledger, CheckpointStrategy, StepStatus
from ..agent.llm import GatedLLM
from ..agent.context import ContextManager
from ..agent.prompts import Prompts
from ..core.bridge import FileSystemBridge
from .interaction import InteractionManager


class Dashboard:
    def __init__(self, root: Path, api_key: str):
        self.root = root
        self.llm = GatedLLM(root, api_key)
        self.context_mgr = ContextManager(root)
        self.io = FileSystemBridge(root)
        self.interaction = InteractionManager(root)
        
        # Load Core State
        self.manifest = load_manifest(root / "manifest.yaml")
        if not (root / ".gap").exists():
            (root / ".gap").mkdir(exist_ok=True)
        self.ledger = get_ledger(root, self.manifest)
        
        # Load ACL (Lazy)
        from ..security.acl import parse_acl
        self.io.acl_whitelist = parse_acl(root)

    def main_loop(self):
        print(f"-> Attaching Gated Agent to Project Root: {self.root}")
        print("=== GATED AGENT V2 (Modular Architecture) ===")
        
        # Initial Spark
        user_intent = ""
        # Heuristic check for existing project
        if not (self.root / "specs").exists():
            print("\n>>> THE SPARK")
            print("What should we build/write/research today?")
            user_intent = input("   > ").strip()

        while True:
            print("\n" + "="*40)
            print("   DASHBOARD")
            print("="*40)
            print(" [1] PHASE 1: PLANNING (Domain Agnostic)")
            print(" [2] PHASE 2: EXECUTION (tasks -> code)")
            print(" [3] PHASE 3: VERIFICATION (walkthrough)")
            print(" [q] QUIT")
            
            choice = input("\nSelect Phase > ").strip().lower()
            
            if choice == '1':
                self.run_phase_planning(user_intent)
            elif choice == '2':
                self.run_phase_execution()
            elif choice == '3':
                self.run_phase_verification()
            elif choice == 'q':
                print("Exiting.")
                break
            else:
                print("Invalid choice.")

    def run_phase_planning(self, user_intent):
        print("\n>>> PHASE 1: DECISION FLOW")
        
        # Multi-Domain Selection
        print("Select Domain:")
        print(" [1] Coding (requirements -> design -> tasks)")
        print(" [2] Storytelling (synopsis -> characters -> chapters)")
        print(" [3] Science (hypothesis -> methodology -> experiments)")
        domain_choice = input("   > ").strip()
        
        flow = []
        if domain_choice == '2': # Story
             flow = [
                 FlowStep("synopsis", "specs/synopsis.md", "core"),
                 FlowStep("characters", "specs/characters.md", "core"),
                 FlowStep("plot", "specs/plot.md", "core"),
                 FlowStep("chapters", "specs/chapters.md", "planning")
             ]
        elif domain_choice == '3': # Science
             flow = [
                 FlowStep("hypothesis", "specs/hypothesis.md", "core"),
                 FlowStep("methodology", "specs/methodology.md", "core"),
                 FlowStep("safety", "specs/safety.md", "governance"),
                 FlowStep("experiments", "specs/experiments.md", "planning")
             ]
        else: # Coding (Default)
             flow = [
                FlowStep("requirements", "specs/requirements.md", "core"),
                FlowStep("design", "specs/design.md", "core"),
                FlowStep("policy", "specs/policy.md", "governance"),
                FlowStep("tasks", "specs/tasks.md", "planning")
            ]

        for step in flow:
            p = self.root / step.artifact
            
            if p.exists():
                print(f"\n--- Step: {step.name} ({step.step}) ---")
                print(f"   Artifact {step.artifact} exists.")
                print("   > Press ENTER to Skip, or type instructions to UPDATE:")
                update_instruction = input("   > ").strip()
                
                if not update_instruction:
                    continue
                
                self.run_flow_step(step, user_intent, differential_intent=update_instruction)
            else:
                self.run_flow_step(step, user_intent)

    def run_flow_step(self, step, user_intent=None, differential_intent=None):
        print(f"\n--- Step: {step.name} ({step.step}) ---")
        
        # Context Construction
        context = ""
        if user_intent:
             context += f"USER INTENT: {user_intent}\n\n"
             
        specs_dir = self.root / "specs"
        if specs_dir.exists():
            for f in specs_dir.glob("*.md"):
                if f.name != Path(step.artifact).name: # Don't include self
                    context += f"Existing Spec ({f.name}):\n{f.read_text()}\n\n"

        # Check for Differential Update
        existing_content = self.context_mgr.read_artifact(step.artifact)
        prompt_template = ""
        
        if existing_content:
            print(f"   -> Detected existing {step.artifact}. Loading for Differential Update.")
            prompt_template = Prompts.differential_update(existing_content, differential_intent)
        else:
            prompt_template = f"# {step.name}\n\n[Generate content based on Context]"

        # Construct Final Prompt
        final_prompt = Prompts.fill_template(prompt_template, context)
        original_prompt = final_prompt # SAVE BASELINE
        
        # LLM Call
        print("    (Agent is Thinking...)")
        content = self.llm.chat(final_prompt)
        
        print(f"🤖 Agent Proposed Content for {step.step}:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        # Feedback Loop (Gate)
        while True:
            print("🛑 GAP: BLOCKED (Gate is Closed).")
            choice = self.interaction.ask_human(step.step, f"Agent wants to write to {step.artifact}")
            
            if choice == 'y':
                self.io.write_artifact(step.artifact, content, allowed_path=step.artifact)
                break
            elif choice == 'n':
                print("   ❌ Denied.")
                print("   [r] Refine: Keep current draft but fix specific issues.")
                print("   [d] Discard: Throw away draft and retry from baseline.")
                mode = input("   Select Mode > ").strip().lower()
                
                print("   >> Instructions/Reason:")
                feedback = input("   > ").strip()
                
                if mode == 'd':
                    # DISCARD -> RESTORE BASELINE
                    print("   🗑️ Discarding Draft. Rolling back to Baseline.")
                    final_prompt = original_prompt + f"\n\nCONSTRAINT: previous attempts failed. \nUSER FEEDBACK: {feedback}"
                else:
                    # REFINE -> APPEND CONTEXT
                    print("   🛠️ Refining Draft.")
                    final_prompt += f"\n\nUSER REJECTED PREVIOUS DRAFT. FIX THIS:\n{feedback}"
                
                content = self.llm.chat(final_prompt)
                print(f"🤖 Agent Proposed Content (Retry):")
                print("-" * 40)
                print(content)
                print("-" * 40)
            else:
                 break

    def run_phase_execution(self):
        print("\n>>> PHASE 2: EXECUTION")
        # 1. Parse Tasks logic (Needs to be ported)
        # For brevity in this V2 scaffold, I'll implement a placeholder
        # In real V2, this calls parsing logic in `core/flow.py`
        print("(Execution Logic would run here - similar to V1)")
        
        # Reload ACL
        from ..security.acl import parse_acl
        self.io.acl_whitelist = parse_acl(self.root)
        
    def run_phase_verification(self):
        print("\n>>> PHASE 3: VERIFICATION")
        self.io.write_artifact("walkthrough.md", "# Walkthrough\n\nGenerated by V2.", allowed_path="walkthrough.md")
        print("✅ Walkthrough generated.")

import sys
from pathlib import Path
from ..core.flow import Step

class ProgrammaticForms:
    """
    Deterministic forms for Protocol-controlled steps.
    Enforces Separation of Concerns: GAP controls policy/gates, Agent controls content.
    """
    def __init__(self, root: Path):
        self.root = root

    def run_policy_wizard(self, step: Step) -> str:
        """
        Interactively gathers Policy settings and generates the artifact.
        Does NOT involve the LLM.
        """
        print(f"\n🛡️  PROTOCOL FORM: {step.name}")
        print("========================================")
        print("Define the security boundaries for this project.\n")

        # 1. ACL (File Access)
        print("--- 1. Access Control List (ACL) ---")
        print("Where is the agent allowed to write?")
        print(" [a] Strict:     src/*.py only (No config/root files)")
        print(" [b] Standard:   src/ and tests/ (Recommended)")
        print(" [c] Permissive: Entire Project Root (Risky)")
        
        acl_choice = input("Select ACL > ").strip().lower()
        if acl_choice == 'a':
            acl_rule = "src/*.py"
            acl_desc = "Strict (Source only)"
        elif acl_choice == 'c':
            acl_rule = "**/*"
            acl_desc = "Permissive (All files)"
        else:
            acl_rule = "src/, tests/"
            acl_desc = "Standard (Src + Tests)"

        # 2. Tool Permissions
        print("\n--- 2. Tool Capabilities ---")
        print("What tools can the agent use?")
        print(" [1] Safe:       read, save (No Execution)")
        print(" [2] Standard:   read, save, ipython (Code Execution)")
        print(" [3] Sovereign:  read, save, ipython, shell (Full System Access)")
        
        tool_choice = input("Select Tools > ").strip().lower()
        if tool_choice == '1':
            tools = "read, save"
            tool_desc = "Safe (No Execute)"
        elif tool_choice == '3':
            tools = "read, save, ipython, shell"
            tool_desc = "Sovereign (Shell Access)"
        else:
            tools = "read, save, ipython"
            tool_desc = "Standard (Python Execution)"

        # Generate Content
        content = f"""# Project Policy

## Security Configuration
**Generated via Protocol Form (Deterministic)**

### Access Control List (ACL)
- Rule: `{acl_rule}`
- Mode: {acl_desc}

### Capability Gates (Tools)
- Allowed: `{tools}`
- Mode: {tool_desc}

### Compliance
This policy enforces the boundaries for the Execution Phase.
Any attempt to access files outside the ACL or use unauthorized tools will be rejected by the Kernel.
"""
        return content

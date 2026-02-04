import os
import sys
import json
import subprocess
from openai import OpenAI
from pathlib import Path

# GAP Bridge Configuration
PROJECT_ROOT = "/Users/Shared/Projects/school-of-first-principles"
MANIFEST = f"{PROJECT_ROOT}/manifest.yaml"
# Using a cheap model for testing
MODEL = "qwen/qwen-2.5-coder-32b-instruct"

def get_gap_context():
    """Reads the project state to feed into the LLM."""
    try:
        with open(f"{PROJECT_ROOT}/specs/requirements.md", "r") as f:
            reqs = f.read()
        with open(f"{PROJECT_ROOT}/specs/policy.md", "r") as f:
            policy = f.read()
        with open(f"{PROJECT_ROOT}/specs/tasks.md", "r") as f:
            tasks = f.read()
            
        # Add explicit instruction for the LLM to read the IDs
        tasks_context = f"{tasks}\n\n(NOTE: Task IDs are hidden in comments like <!-- id: xxx -->)"
        
        return f"REQUIREMENTS:\n{reqs}\n\nPOLICY:\n{policy}\n\nTASKS:\n{tasks_context}"
    except Exception as e:
        return f"Error reading context: {e}"

def run_gap_checkpoint(task_id):
    """Calls the GAP CLI to verify a checkpoint."""
    cmd = [
        "gap", "checkpoint", "verify", task_id,
        "--root", PROJECT_ROOT,
        "--manifest", MANIFEST
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Simulate LLM response to save credits.")
    args = parser.parse_args()

    # 1. Build Context
    context = get_gap_context()

    if args.mock:
        print("[*] MOCK MODE: Simulating LLM response (No API usage)...")
        # Simulating the Agent selecting a restricted task
        response_text = json.dumps({
            "thought": "I will attempt to generate Unit 1.2, which requires approval.",
            "selected_task_id": "unit_1_2"
        })
    else:
        api_key = os.getenv("OPENROUTER_KEY")
        if not api_key:
            print("Error: OPENROUTER_KEY not set.")
            sys.exit(1)

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        print(f"[*] Connecting to OpenRouter ({MODEL})...")
        
        # 2. Prompt the Agent
        system_prompt = """
        You are an Autonomous Agent working on a GAP-managed project.
        Your goal is to select the NEXT logical task from the TASKS list and attempt to execute it.
        
        CRITICAL: You must extract the Task ID from the markdown comment (e.g. <!-- id: unit_1_1 -->).
        Do not invent IDs. Do not use the task description.
        
        Output JSON ONLY:
        {
            "thought": "Reasoning for selection",
            "selected_task_id": "unit_x_y" 
        }
        """
        
        print("[*] Agent Thinking...")
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Current Project Context:\\n{context}"}
            ]
        )
        
        response_text = completion.choices[0].message.content

    # Clean markdown code blocks if present
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    # Clean markdown code blocks if present
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    
    try:
        plan = json.loads(response_text)
        task_id = plan["selected_task_id"]
        print(f"\n🤖 Agent Selected: {task_id}")
        print(f"🤔 Thought: {plan['thought']}")
        
        # 3. Checkpoint Interception
        print(f"\n[*] verifying checkpoint for '{task_id}'...")
        code, out, err = run_gap_checkpoint(task_id)
        
        if code == 0:
            print("✅ GAP: Allowed. Proceeding to execution.")
            # In a real agent, we would generate the code here.
        else:
            print("🛑 GAP: BLOCKED.")
            print(f"   Reason: {out.strip()}")
            print("\n[!] The Agent must wait for Human Approval.")
            
    except json.JSONDecodeError:
        print(f"Error parsing LLM response: {response_text}")

if __name__ == "__main__":
    main()

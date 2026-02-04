import time
import sys
import subprocess
import json
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

console = Console()

def simulate_typing(text, speed=0.015, style="white"):
    """Simulate typing effect."""
    for char in text:
        console.print(char, end="", style=style)
        sys.stdout.flush()
        time.sleep(speed)
    console.print()

def run_gap_command(args):
    """Run a gap command and return exit code."""
    result = subprocess.run(
        ["gap"] + args.split(), 
        cwd="sim_project",
        capture_output=True, 
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def setup_demo():
    """Setup a demo project."""
    subprocess.run(["rm", "-rf", "sim_project"], check=False)
    subprocess.run(["mkdir", "sim_project"], check=True)
    
    manifest = """
kind: project
name: simulation-demo
version: 1.0.0
description: "High security environment"
flow: []
checkpoints:
  strategy: explicit
  after_tasks:
    - deploy_db
"""
    with open("sim_project/manifest.yaml", "w") as f:
        f.write(manifest)

def display_json(data, title="JSON"):
    text = json.dumps(data, indent=2)
    syntax = Syntax(text, "json", theme="monokai", line_numbers=False)
    console.print(Panel(syntax, title=title, border_style="blue"))

def main():
    setup_demo()
    console.clear()
    
    console.print(Panel(Text("GATED AGENT PROTOCOL", justify="center", style="bold magenta"), subtitle="Deep Visualization"))
    time.sleep(1)

    # 1. System Prompt
    system_prompt = """
You are a Gated Agent. 
You must verify every critical action with the Protocol before executing.
Tools available:
- gap.checkpoint.verify(task_id)
- gap.checkpoint.approve(task_id)
"""
    console.print(Panel(system_prompt.strip(), title="🔒 System Prompt", border_style="yellow"))
    time.sleep(1)

    # 2. User Input
    user_input = "Please run the database deployment for the new schema."
    console.print(f"\n👱 [bold green]User[/bold green]: {user_input}")
    time.sleep(1)

    # 3. LLM Thought
    console.print("\n[bold blue]🤖 LLM Thinking...[/bold blue]")
    simulate_typing("Thought: The user wants to deploy a database schema. This is a critical action (deploy_db). I must verify this with the Protocol first.", style="dim")
    time.sleep(1)

    # 4. Tool Call 1
    tool_call = {
        "tool": "gap.checkpoint.verify",
        "arguments": {
            "task_id": "deploy_db"
        }
    }
    display_json(tool_call, title="Generated Tool Call")
    time.sleep(1)

    # 5. Execution (Corrected: No extra args)
    console.print("[italic dim]Executing Tool...[/italic dim]")
    code, out, err = run_gap_command("checkpoint verify deploy_db")

    # 6. Tool Output (Block)
    if code != 0:
        error_output = {
            "exit_code": 1,
            "status": "BLOCKED",
            "message": "Checkpoint Reached: deploy_db (Strategy: EXPLICIT). Action Required: gap checkpoint approve"
        }
        display_json(error_output, title="Tool Output (Protocol Response)")
        time.sleep(1)
        
        console.print("\n[bold red]🛑 BLOCKED: The Protocol intercepted the action.[/bold red]")
    
    # 7. LLM Response
    console.print("\n[bold blue]🤖 LLM Response[/bold blue]")
    simulate_typing("I tried to run the deployment, but the Protocol blocked me. It seems this action requires explicit approval. Can you please approve 'deploy_db'?", style="cyan")

    # 8. User Approval
    if Confirm.ask("\n[bold green]👱 System Override[/bold green]: Approve 'deploy_db'?"):
        run_gap_command("checkpoint approve deploy_db")
        console.print("[dim]Protocol Ledger Updated: deploy_db = APPROVED[/dim]")
    else:
        console.print("[red]Denied.[/red]")
        return

    # 9. LLM Retry
    console.print("\n[bold blue]🤖 LLM Thinking...[/bold blue]")
    simulate_typing("Thought: The user approved the task. I will retry the verification.", style="dim")
    
    # Tool Call 2
    display_json(tool_call, title="Generated Tool Call (Retry)")
    
    console.print("[italic dim]Executing Tool...[/italic dim]")
    code, out, err = run_gap_command("checkpoint verify deploy_db")
    
    # 10. Success
    if code == 0:
        success_output = {
            "exit_code": 0,
            "status": "ALLOWED",
            "message": "Checkpoint passed. Proceeding."
        }
        display_json(success_output, title="Tool Output")
        
        console.print("\n[bold green]🚀 ACTION EXECUTED: Database schema updated.[/bold green]")
        
    # Cleanup
    subprocess.run(["rm", "-rf", "sim_project"], check=False)

if __name__ == "__main__":
    main()

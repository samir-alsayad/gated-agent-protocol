import os
import sys
import argparse
from pathlib import Path
from .ui.menu import Dashboard

def main():
    parser = argparse.ArgumentParser(
        description="Gated Agent TUI - Reference Implementation",
        prog="gated_agent_tui"
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Path to the project directory containing manifest.yaml"
    )
    parser.add_argument(
        "--driver",
        choices=["reference", "gptme"],
        default="reference",
        help="Execution driver: 'reference' (classic TUI) or 'gptme' (live stream)"
    )
    parser.add_argument(
        "--model",
        help="Model identifier (e.g., 'openrouter/qwen/qwen-2.5-coder-32b-instruct')"
    )
    
    args = parser.parse_args()
    
    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a valid directory.")
        sys.exit(1)
              
    api_key = os.getenv("OPENROUTER_KEY")
    if not api_key:
        print("Error: OPENROUTER_KEY not set.")
        sys.exit(1)
        
    dashboard = Dashboard(root, api_key, driver=args.driver, model=args.model)

    dashboard.main_loop()

if __name__ == "__main__":
    main()


import os
import sys
from pathlib import Path
from .ui.menu import Dashboard

def main():
    root = Path.cwd()
    if len(sys.argv) > 1:
         potential_root = Path(sys.argv[1])
         if potential_root.is_dir():
             root = potential_root
             
    api_key = os.getenv("OPENROUTER_KEY")
    if not api_key:
        print("Error: OPENROUTER_KEY not set.")
        sys.exit(1)
        
    dashboard = Dashboard(root, api_key)
    dashboard.main_loop()

if __name__ == "__main__":
    main()

import sys
import os
from pathlib import Path

# 1. Add GAP Source to Path (so we can import both 'gap' and 'gated_agent_tui')
GAP_SRC = Path(__file__).resolve().parent.parent / "src"
REF_IMPL = Path(__file__).resolve().parent.parent / "reference_implementation"

if GAP_SRC.exists():
    sys.path.append(str(GAP_SRC))
else:
    print(f"Warning: GAP Source not found at {GAP_SRC}")

if REF_IMPL.exists():
     sys.path.append(str(REF_IMPL))

# 2. Run
try:
    from gated_agent_tui.main import main
    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Error importing V2 Agent: {e}")
    print("Make sure you are running from /Users/Shared/Projects/test")

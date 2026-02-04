import os
import ast
from pathlib import Path

class ContextManager:
    def __init__(self, root: Path):
        self.root = root

    def read_artifact(self, path: str) -> str:
        p = self.root / path
        if p.exists():
            with open(p, "r") as f:
                return f.read()
        return ""

    def generate_repo_map(self) -> str:
        """Scans the project for .py files and extracts signatures using AST."""
        repo_map = "PROJECT STRUCTURE & API:\n"
        
        for root, dirs, files in os.walk(self.root):
            if ".gap" in root or "__pycache__" in root or "gated_agent_tui" in root:
                continue
                
            for file in files:
                if file.endswith(".py"):
                    path = Path(root) / file
                    try:
                        rel_path = path.relative_to(self.root)
                        repo_map += f"\nFile: {rel_path}\n"
                        
                        with open(path, "r") as f:
                            tree = ast.parse(f.read())
                            
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                repo_map += f"  class {node.name}:\n"
                                for item in node.body:
                                    if isinstance(item, ast.FunctionDef):
                                        args = [a.arg for a in item.args.args]
                                        if 'self' in args: args.remove('self')
                                        repo_map += f"    def {item.name}({', '.join(args)})\n"
                            elif isinstance(node, ast.FunctionDef):
                                # Top level functions (simple heuristic)
                                if not isinstance(node, ast.ClassDef): 
                                     pass # AST walking is flat, complex to infer parent easily without node transformer
                    except Exception:
                         # repo_map += f"  (Error parsing {file})\n"
                         pass
        return repo_map

    def read_all_specs(self) -> str:
        """Reads all Markdown files in the specs/ directory to build global context."""
        context = ""
        specs_dir = self.root / "specs"
        if specs_dir.exists():
            for f in sorted(specs_dir.glob("*.md")):
                context += f"--- SPEC: {f.name} ---\n"
                context += f.read_text()
                context += "\n\n"
        return context

import os
import json
from pathlib import Path
from datetime import datetime
from openai import OpenAI

class GatedLLM:
    def __init__(self, root: Path, api_key: str):
        self.root = root
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = "qwen/qwen-2.5-coder-32b-instruct"
        
        # Session Logging
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = self.root / ".gap/sessions"
        self.session_log_file = self.log_dir / f"{self.session_id}.log.jsonl"

    def log_session(self, entry):
        # Lazy creation of log dir
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
        entry['timestamp'] = datetime.now().isoformat()
        with open(self.session_log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def chat(self, prompt, system="You are a helpful Sovereign Agent."):
        """Simple wrapper for LLM call."""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )
            content = completion.choices[0].message.content
            
            # LOGGING
            self.log_session({
                "type": "llm_interaction",
                "prompt": prompt,
                "response": content
            })
            
            return content
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return "Error generating content."

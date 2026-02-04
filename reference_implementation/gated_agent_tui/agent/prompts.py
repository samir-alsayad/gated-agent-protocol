class Prompts:
    
    @staticmethod
    def differential_update(existing_content, differential_intent=""):
        update_instruction = ""
        if differential_intent:
            update_instruction = f"\n\nUPDATE REQUEST: {differential_intent}"
            
        return f"\n\n--- CURRENT VERSION (FOR UPDATE) ---\n{existing_content}\n\nINSTRUCTION: The user wants to UPDATE the above artifact. User Intent is PARAMOUNT. {update_instruction}\n1. ONLY change what the User asked for.\n2. Do NOT add unrequested features.\n3. If the User gives specific numbers vs defaults, USE THEM.\n4. Maintain existing structure."

    @staticmethod
    def fill_template(template_content, context):
        return f"Fill out or Update the following Markdown Template based on the Context.\n\nTEMPLATE:\n{template_content}\n\nCONTEXT:\n{context}\n\nOUTPUT ONLY THE FILLED MARKDOWN."

    @staticmethod
    def code_gen(filename, context, repo_map):
        return f"""You are a Python Expert. Write the COMPLETE, EXECUTABLE code for the file `{filename}`.

RULES:
1. OUTPUT PURE CODE ONLY. Do NOT use markdown code blocks (```python). Just the raw code.
2. NO PLACEHOLDERS. Do NOT use things like `WIDTH = ,` or `pass`. You must implement full functionality with real values.
3. FULL IMPLEMENTATION. Do not truncate the code.
4. ROBUSTNESS. Ensure all variables are defined.
5. USE EXISTING APIS. Check the REPO MAP below.

CONTEXT:
{context}

REPO MAP (Existing Codebase):
{repo_map}

BEGIN CODE:"""

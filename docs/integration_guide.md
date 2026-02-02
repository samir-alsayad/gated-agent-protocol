# GAP Integration Guide: Building a Protocol-Aware Tool

**Target Audience:** IDE Developers (OpenCode, Cursor), Agent Framework Builders (LangChain, AutoGen).

---

## 1. The Practical Flow
"Supporting GAP" means your tool stops being a passive executor and becomes a **Protocol Enforcer**.

### Step A: Detection (The "Is this a GAP Project?" Check)
When your tool opens a folder, it must check for `.gap/gap.yaml`.

**The Session Registry:**
Instead of a single global mode, the tool manages **Sessions**.
- Reads `.gap/gap.yaml` -> `active_session`.
- Loads context from `.gap/sessions/[active_session]/`.

### Step B: Resolution (The "Load Rules" Step)
```python
def load_protocol(root_path):
    # 1. Read the Registry
    with open(os.path.join(root_path, ".gap/gap.yaml")) as f:
        config = yaml.safe_load(f)
    
    # 2. Find the Active Session
    active_id = config['active_session']
    session = next(s for s in config['sessions'] if s['id'] == active_id)

    # 3. Load the Protocol
    return Registry().get_manifest(session['protocol'])
```

### Step C: The Enforcement Loop (The "Main Loop")
This is the biggest change. You must **Intervene** in the Agent's context.

**Standard Agent Loop:**
USER -> LLM -> TOOL -> USER

**GAP Agent Loop:**
```python
current_gate = protocol.gates[0] # e.g. "Planning"

while task_active:
# HARNESS LOGIC (Conceptual)

gate_index = 0
current_gate = protocol.gates[gate_index]

while True:
    # 1. SETUP SANDBOX
    # If this gate is "Synthesis", we load the ACL from the artifact approved in the PREVIOUS step.
    if current_gate.id == "gate_synthesis":
        last_artifact_path = protocol.gates[gate_index - 1].output_artifacts[0]
        enforcer = ACLEnforcer(last_artifact_path)
    
    # 2. RESTRICT TOOLS
    # Tools are filtered by the Gate's permissions AND the ACL Enforcer
    available_tools = filter_tools(all_tools, current_gate.permissions, enforcer)
    
    # 3. RUN AGENT
    # We tell the agent specifically what artifact it must produce
    system_prompt = f"Current Gate: {current_gate.id}. Output Required: {current_gate.output_artifacts}"
    response = agents.run(prompt, tools=available_tools)
    
    # 4. REVIEW & ADVANCE
    # The user reviews the output artifact. Approval unlocks the next gate.
    if user_approves(response):
        gate_index += 1
        if gate_index < len(protocol.gates):
            current_gate = protocol.gates[gate_index]
        else:
            print("Protocol Complete!")
            break
```

## 2. What this feels like to the User
1.  **Safety**: They see the IDE say *"Agent Restricted: Planning Mode"*.
2.  **Trust**: They see the Agent ask *"I need write access to `src/main.py`. Approve?"*
3.  **Control**: They know the Agent *cannot* touch `database.db` because it wasn't in the plan.

## 3. The "Harness" Responsibility
Your tool acts as the **Harness**. You are the "Container" that holds the "Probabilistic Drift" in check.

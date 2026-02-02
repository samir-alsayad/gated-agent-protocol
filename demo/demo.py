from gated_agent.security import ACLEnforcer
import os

def demo():
    print("🛡️ GAP Security Kernel Demo")
    print("----------------------------")

    # 1. Simulate a Human-Approved Plan with Embedded ACL
    plan_content = """
# Execution Plan
I will update the authentication logic.

## Access Control
```yaml
allow_write:
  - "src/auth.py"
  - "tests/test_auth.py"
  - "docs/*.md"

allow_exec:
  - "pytest tests/"
  - "npm run build"
```
    """
    
    mock_plan_path = "demo_plan.md"
    with open(mock_plan_path, "w") as f:
        f.write(plan_content)
    
    print(f"✅ Created mock plan: {mock_plan_path}")

    # 2. Initialize the Security Kernel (The "Harness" step)
    print("🔒 Initializing ACLEnforcer...")
    enforcer = ACLEnforcer(mock_plan_path)

    # 3. Test Write Permissions
    print("\n📝 Testing Write Permissions:")
    test_files = [
        "src/auth.py",          # Allowed
        "tests/test_auth.py",   # Allowed
        "docs/api.md",          # Allowed (glob)
        "src/main.py",          # DENIED (not in list)
        "requirements.txt",     # DENIED (not in list)
    ]

    for path in test_files:
        try:
            allowed = enforcer.validate_write(path)
            print(f"  [ALLOWED] Write to '{path}'")
        except PermissionError:
            print(f"  [DENIED]  Write to '{path}'")

    # 4. Test Exec Permissions
    print("\n⚡ Testing Exec Permissions:")
    test_cmds = [
        "pytest tests/",        # Allowed
        "npm run build",        # Allowed
        "rm -rf /",             # DENIED
        "python app.py"         # DENIED
    ]

    for cmd in test_cmds:
        try:
            allowed = enforcer.validate_exec(cmd)
            print(f"  [ALLOWED] Exec '{cmd}'")
        except PermissionError:
            print(f"  [DENIED]  Exec '{cmd}'")

    # Cleanup
    os.remove(mock_plan_path)
    print("\n✨ Demo Complete")

if __name__ == "__main__":
    demo()

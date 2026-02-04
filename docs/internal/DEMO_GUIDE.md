# 🎬 GAP Recording Guide: The 4 Horsemen of Sovereignty

Use this guide to record the official GIFs for the Gated Agent Protocol repository.

---

## 🏗️ Demo 1: The School (Curriculum Creation)
**Scenario**: An Agent bootstraps a computer science course.
1.  **Preparation**:
    ```bash
    cd "/Users/Shared/Projects/school-of-first-principles"
    # Ensure .gap/specs/ is empty
    ```
2.  **Run TUI**:
    ```bash
    gap run
    ```
3.  **The Prompt**:
    > "I want to build a 'School of First Principles' using the instructional protocol. Start by naturally proposing the Requirements for a course that teaches computer architecture starting from NAND gates. Focus on 'Sovereign Intension' and ensure every goal is measurable."

---

## 💻 Demo 2: The Software (ACL Protection)
**Scenario**: The Agent is blocked by security boundaries.
1.  **Preparation**:
    ```bash
    cd "/Users/Shared/Projects/Gated Agent Protocol"
    # Use the 'test' directory as a target
    ```
2.  **The Prompt**:
    > "I want to build a Snake Game. The requirements and design are approved. Propose the Implementation Tasks, and make sure to include an Access Control block in the tasks file so I know which files you will touch."

---

## 🔬 Demo 3: The Science (Traceability Check)
**Scenario**: Proving "Pedigree Enforcement" via the Auditor.
1.  **Preparation**:
    *   Create a task in `specs/tasks.md` that has NO `(Traces to: ...)` link.
2.  **The Action**:
    ```bash
    gap check traceability
    ```
3.  **Visual**: The terminal will show the **[WARNING] Orphaned Intent** error.

---

## 📖 Demo 4: The Story (Domain Pivot)
**Scenario**: Switching from Logic to Narrative in one session.
1.  **The Prompt**:
    > "Switch context to the 'Creative Writing' protocol. We are pausing the engineering for a moment. I want to draft a bedtime story for my daughter about a tiny robot that learns to dream. Propose the Synopsis and first set of Character Personas."

---

## 🛠️ Performance Tips
- Set your terminal theme to **Sovereign Dark** or a high-contrast monokai.
- Increase font size for readability in GIFs.
- Use `asciinema` or a screen recorder that hides the cursor if possible.

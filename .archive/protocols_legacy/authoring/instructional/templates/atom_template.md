# Atomic Unit: {{ unit_title }} <!-- AGENT: The exact topic title -->

**Campaign**: {{ campaign_name }}
**Prerequisites**: {{ prerequisites }} <!-- AGENT: List required previous units or "None" -->
**Goal**: {{ unit_goal }} <!-- AGENT: What will the student be able to DO after this? -->

## The Theory
<!-- AGENT: Explain the core concept briefly. Use 1st principles. -->
{{ theory_explanation }}

### The Pattern (Transfer Learning)
<!-- AGENT: Provide a concrete code example of the concept in a DIFFERENT context.
     The student must adapt this pattern to solve the Mission.
     Example: If teaching SIGUSR1, show how to catch SIGINT. -->
```{{ language }}
{{ pattern_code_example }}
```

### The Toolbox (Concepts)
<!-- AGENT: List 2-3 key terms or tools -->
1.  **{{ concept_1 }}**: {{ concept_1_definition }}
2.  **{{ concept_2 }}**: {{ concept_2_definition }}

## The Mission (Ground Zero)
**Protocol**: Start with an EMPTY file. Do not copy-paste.

1.  **Setup**: Create `{{ main_file }}`.
2.  **Step 1**: {{ step_1_instruction }} <!-- AGENT: Actionable instruction -->
3.  **Step 2**: {{ step_2_instruction }}
4.  **Step 3**: {{ step_3_instruction }}

## Verification (The Proof)
1.  Run the code/action.
2.  Expected Output:
    ```text
    {{ expected_output }} <!-- AGENT: Precise string to match -->
    ```

---

## Understanding (Socratic Check)
<!-- AGENT: 2 Questions that check deep understanding (not just syntax) -->
*   [ ] {{ question_1 }}
*   [ ] {{ question_2 }}

## My Journal
<!-- STUDENT AREA: Do not fill. Leave blank for student. -->
*   **Date**:
*   **Learnings**:
*   **Code**:
    ```{{ language }}
    # Paste your solution here
    ```

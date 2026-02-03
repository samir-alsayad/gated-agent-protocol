# Gated Decisions and Gated Execution

## 1. Overview

GAP separates **decision authority** from **execution throughput** in order to preserve user intent while enabling high-volume, agent-assisted work. This separation applies uniformly across domains such as software development, curriculum creation, and authoring.

At the core of GAP is a strict rule:

> **Authority is granted only through explicit user approval of decision records. Execution output never acquires authority implicitly.**

This chapter formalizes how decisions are gated, how execution proceeds, and how the two interact.

---

## 2. Decision Records

In GAP, all intentional work is governed by **decision records**. Decision records encode commitments that constrain all downstream derivations.

GAP defines three classes of decision records:

* **Requirements** — intent decisions
  Define what must be true, what problem is being solved, and what constraints apply.
* **Design** — structural decisions
  Define how the requirements are satisfied through structure, organization, or strategy.
* **Policy** — governance decisions
  Define the constraints, gating granularity, and execution mode (Autonomous vs Gated).
* **Tasks** — operational decisions
  Define what specific actions will be taken to realize the design.

Although they differ in scope and resolution, all three are ontologically identical:
they are **explicit decisions that bind future work**.

---

## 3. Mandatory Decision Gating

All decision records are subject to **mandatory gating**.

A decision record:
* may be proposed by an agent,
* must be reviewed by the user,
* becomes authoritative **only** upon explicit user approval.

Until approved, a decision record:
* has no binding authority,
* may not constrain downstream derivations,
* may be revised or discarded freely.

This rule applies uniformly to Requirements, Design, Policy and Tasks.
There are no exceptions.

The purpose of mandatory decision gating is to prevent:
* implicit authority transfer,
* agent-driven intent drift,
* decisions being “smuggled in” through execution output.

---

## 4. Tasks Are Decisions, Not Execution

Tasks are frequently mistaken for execution. In GAP, this is explicitly incorrect.

A **Task** is a decision to perform a specific action.
**Execution** is the act of carrying out that decision.

For example:
* “Write Chapter 3 exploring X from POV Y” is a task decision.
* The actual prose of Chapter 3 is execution output.
* “Implement authentication using OAuth2” is a task decision.
* The resulting code is execution output.

Tasks therefore belong fully within the decision-record hierarchy and are subject to the same mandatory gating as Requirements, Design and Policy.

---

## 5. Execution Output

Execution output consists of all derived material produced by carrying out approved task decisions. Examples include:
* prose, pages, scenes
* code, functions, modules
* lessons, exercises, assessments

Execution output is **mutable by default** and **non-authoritative**.

Execution output:
* may be generated continuously,
* may be revised, replaced, or discarded,
* does not constrain future work unless explicitly promoted.

Execution exists to produce volume, not authority.

---

## 6. Optional Execution Gating

While decision gating is mandatory, **execution gating is optional**.

GAP allows execution output to be gated at any granularity, including:
* page by page,
* function by function,
* lesson by lesson,
* batch or milestone level.

However:
* execution gating is never required,
* execution may proceed freely without gating if explicitly enabled,
* gating execution does not create authority on its own.

Execution gating exists to support:
* fine-grained review,
* incremental validation,
* human comfort and oversight.

It is a capability, not a constraint.

---

## 7. Escalation from Execution to Decision

During execution, new information may emerge that:
* contradicts existing decisions,
* reveals missing constraints,
* forces a previously unmade choice.

When this occurs, GAP requires **explicit escalation**.

Execution output may be:
* promoted into a **proposed decision record**,
* submitted for user review,
* gated through the normal decision-approval process.

No execution output may silently redefine intent or structure.

---

## 8. Authority Rules (Summary)

The following rules are normative in GAP:

1. Requirements, Design, and Tasks are all decision records.
2. All decision records require explicit user approval.
3. Approved decision records are authoritative and constrain all downstream work.
4. Execution output is always derived and non-authoritative.
5. Execution gating is optional; decision gating is mandatory.
6. Authority may only move upward through explicit escalation and approval.

---

## 9. Domain Independence

This model is domain-agnostic.

The same authority mechanics apply to:
* writing a book,
* designing a curriculum,
* developing software,
* or any other intentional creation process.

Only the *execution units* differ.
The rules governing authority do not.

---

## 10. Intent Preservation as the Core Goal

GAP does not exist to slow work down.
It exists to ensure that high-throughput execution never erodes user-owned intent.

By making decisions explicit, gated, and authoritative—while allowing execution to flow freely—GAP enables agents to act as co-authors without becoming decision-makers.

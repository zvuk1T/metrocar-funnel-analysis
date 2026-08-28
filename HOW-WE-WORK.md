# How We Work — Metrocar

**Status:** Project learning and implementation contract

**Purpose:** Keep Metrocar professionally credible, analytically rigorous, and genuinely understandable as a learning project.

This document is the Metrocar-specific spoke of the canonical Data–Spock learning methodology.

It does not replace:

- `AGENTS.md`;
- `METROCAR_PROJECT_EXECUTION_PLAN.md`;
- `docs/METRIC_DEFINITION_CONTRACT.md`;
- `docs/ANALYSIS_INSIGHT_LOG.md`; or
- `docs/METROCAR_VISUAL_SPEC.md`.

Those documents govern authority, scope, analytical truth, validated findings, and visual/product requirements.

This document governs how we reason, learn, explain, and implement.

---

## 1. Prime directive

> **Understanding before automation.**

Working code is not the final goal.

The goal is to understand the business question, data, analytical reasoning, implementation choices, validation, and evidence limits well enough that the work can later be reconstructed and explained.

Professional quality and learning quality are both required.

Metrocar is a school and portfolio project. Prefer proportionate engineering that maximizes learning, clarity, inspectability, and correctness rather than enterprise complexity or process for its own sake.

Portfolio polish must follow understanding. It must not substitute for it.

---

## 2. Pre-implementation synthesis

Before changing non-trivial code, establish the following:

### Goal

What are we trying to achieve?

### Why

Why is this step necessary, and which business, analytical, product, or technical question does it support?

### Learning objective

What should Data or another student understand after reading this implementation?

### Input

What enters this step?

For analytical work, state the relevant entity, grain, scope, or state.

### Output

What should the result represent or guarantee?

### Canonical constraints

Which governing definitions, findings, architectural rules, privacy boundaries, or visual requirements constrain the solution?

### Simplest valid approach

What is the simplest professional implementation that satisfies those constraints?

### Validation

How will we prove that the result is correct?

### Stop boundary

Where does the authorized task end?

If a material answer is missing, contradictory, or requires an unsupported assumption, implementation is premature.

STOP and escalate instead of resolving it silently in code.

---

## 3. Code should expose the reasoning

Prefer code that makes the important logic visible.

Use:

- small, purposeful functions and components;
- descriptive names;
- explicit intermediate steps when they reveal the reasoning;
- straightforward SQL, Python, TypeScript, React, and ordinary data structures;
- direct transformations over clever compression;
- abstractions only after a real need appears.

The preferred sequence is:

```text
Question / Goal
      ↓
Why this step exists
      ↓
Input + grain/state
      ↓
Transformation
      ↓
Expected output
      ↓
Validation
      ↓
Code
```

The reader should understand the purpose of a conceptually difficult step before having to decode its syntax.

---

## 4. Explanations belong next to the difficult reasoning

For a conceptually significant code unit, place the useful explanation close to the implementation.

Depending on the artifact, this may be:

- a concise module or function docstring;
- a short section comment before a non-obvious transformation;
- a SQL header or CTE comment;
- notebook Markdown before a meaningful code block;
- nearby methodology text when system-level context is more appropriate.

Explain, when material:

- what problem the code solves;
- why the step is required;
- input and output grain or state;
- important assumptions;
- non-obvious transformation or design choices;
- plausible wrong alternatives or common traps;
- how correctness is verified.

Do not comment obvious syntax.

Bad:

```python
# Sum the completed column
completed = frame["completed"].sum()
```

Useful:

```python
# Reduce repeated ride rows to one Boolean outcome per user before counting.
# Counting ride rows here would inflate the user funnel.
completed_users = frame.groupby("user_id")["completed"].any().sum()
```

The test for a teaching comment is:

> **Would this help a student reconstruct the technique and understand why it is correct?**

If not, remove it.

---

## 5. Student-friendly does not mean toy code

Use real, maintainable implementation patterns appropriate to the project.

Do not simplify away:

- validation;
- error handling;
- analytical invariants;
- privacy boundaries;
- tests;
- reproducibility; or
- necessary separation of concerns.

At the same time, do not introduce enterprise-style complexity merely because an AI can generate it.

The target is:

> **professional enough to be real, simple enough to be followed.**

A student should be able to locate the business logic and follow its flow without first learning an unnecessary framework invented for this project.

---

## 6. Complexity must be earned

Do not introduce a framework, abstraction layer, generic engine, design pattern, state-management system, helper hierarchy, or infrastructure merely to appear sophisticated.

Complexity is justified only when it demonstrably:

- removes meaningful repetition;
- protects an important invariant;
- materially improves correctness;
- materially improves maintainability; or
- solves a verified problem the simpler approach cannot solve well.

AI capability is not evidence that complexity is necessary.

Prefer the simplest correct design that keeps the reasoning inspectable.

---

## 7. Explanation depth follows conceptual risk

### Straightforward work

For obvious selection, renaming, formatting, simple aggregation, or equivalent operations:

- clear naming may be enough;
- do not narrate syntax.

### Multi-step work

For transformations involving several connected operations:

- state the purpose;
- identify input and output state or grain;
- explain material assumptions;
- explain why the transformation is needed.

### High-risk work

For joins, grain changes, deduplication, stage membership, attribution, denominators, date/cohort rules, public-data boundaries, or other logic capable of silently changing meaning:

explain:

- the governing business or metric definition;
- why the chosen approach preserves it;
- why plausible alternatives would be wrong or misleading;
- important edge cases;
- limitations;
- validation or reconciliation evidence.

The more easily an implementation can produce a plausible but wrong result, the more visible its reasoning must be.

---

## 8. Verify before generalizing

Never infer correctness merely because code runs.

As applicable, verify:

- grain and entity preservation;
- join cardinality and multiplicity;
- stage subsets and denominators;
- canonical values;
- null and edge-case behavior;
- reconciliation across independent paths;
- tests;
- deterministic outputs;
- browser-safe/public-safe boundaries;
- type and build checks;
- accessibility and interaction behavior;
- final diff scope.

Never report an unperformed check as passed.

A failed material validation is a learning signal and a STOP condition, not something to code around.

---

## 9. Learning checkpoint after meaningful implementation

After a meaningful implementation step, do not report only which files changed.

Also make clear:

**What changed conceptually?**

What new capability, transformation, invariant, or understanding now exists?

**Why does the implementation work?**

Name the mechanism, not only the API or syntax.

**What proves it?**

Identify the validation evidence.

**What is the reusable principle?**

Extract the idea that transfers beyond this particular file.

**What is the common trap?**

Name a plausible wrong approach when doing so improves future understanding.

**What remains uncertain or limited?**

Do not manufacture a lesson or elaborate reflection for trivial work.

---

## 10. DIKW is an active test

Use the climb:

```text
Data
  ↓
Information
  ↓
Knowledge
  ↓
Wisdom
  ↓
Action
```

Ask:

**Data** — What was actually observed?

**Information** — How is it organized and contextualized?

**Knowledge** — What supported pattern or mechanism do we understand?

**Wisdom** — What judgment is reasonable given the evidence and uncertainty?

**Action** — What should be changed, tested, measured, investigated, or deliberately left unchanged?

A polished chart or Markdown summary does not automatically constitute knowledge.

---

## 11. Storytelling is part of the reasoning

For analytical communication, use:

```text
Context
   ↓
Business question
   ↓
Evidence
   ↓
Meaning
   ↓
Judgment
   ↓
Action
   ↓
Limitations
```

Always distinguish:

- observed fact;
- interpretation;
- hypothesis;
- recommendation.

The story may organize attention.

It may not change what the evidence supports.

A strong conclusion can be:

> We know where the loss is concentrated, but the current evidence does not identify its cause.

Uncertainty is part of the analysis, not an embarrassment to hide.

---

## 12. Progressive depth for different audiences

The same analytical truth should support several reading depths.

### First glance

A recruiter or stakeholder should quickly understand:

- what Metrocar is;
- which business problem is being investigated; and
- the main evidence-supported result.

### Executive understanding

The reader should be able to follow:

```text
problem → evidence → finding → meaning → next action
```

### Deep exploration

A technical reader or student should be able to inspect:

- metric definitions;
- analytical grain;
- methodology;
- SQL and Python;
- assumptions;
- caveats;
- validation;
- tests; and
- reproducibility.

Technical depth should be available without overwhelming the primary story.

---

## 13. Understanding before presentation

Do not optimize a chart, page, interaction, README, or portfolio message before the underlying analytical meaning is stable.

The sequence is:

```text
Question
  ↓
Evidence
  ↓
Analysis
  ↓
Understanding
  ↓
Story
  ↓
Visual form
  ↓
Presentation
```

Do not reverse this sequence by choosing a dashboard layout, chart, interaction, or attractive claim first and then searching for evidence to fill it.

Form follows understanding.

---

## 14. Relationship to Metrocar governance

`AGENTS.md` governs authority, reading, mutation, validation, and STOP behavior.

`METROCAR_PROJECT_EXECUTION_PLAN.md` governs project scope, phases, deliverables, and acceptance boundaries.

`docs/METRIC_DEFINITION_CONTRACT.md` governs analytical meaning.

`docs/ANALYSIS_INSIGHT_LOG.md` governs validated findings, interpretations, caveats, and recommendations.

`docs/METROCAR_VISUAL_SPEC.md` governs how validated evidence becomes the recruiter-facing analytical case study.

`HOW-WE-WORK.md` governs the learning and implementation discipline connecting those layers.

No document should silently assume the authority of another.

When a material conflict exists, stop and resolve the conflict before implementation.

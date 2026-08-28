# AGENTS.md

## Purpose

This document defines the binding working method for all agents in this repository. Reading project documents does not authorize implementation, scope changes, Git actions, or progression through a phase gate.

## Mandatory Tiered Reading

Read documents in the following order.

### Tier 1 — Every Task

1. Read `AGENTS.md` completely.
2. Read `HOW-WE-WORK.md` completely.
3. Read the governing sections of `METROCAR_PROJECT_EXECUTION_PLAN.md`, including:
   - project and phase status;
   - the current authorized task;
   - the document map and ownership;
   - the applicable readiness gate or checkpoint;
   - relevant changelog entries.
4. Read the explicit task authorization, brief, or handover.

Before acting, identify the authorized scope, permitted files, protected files, required evidence, and next mandatory stop.

Before any non-trivial code or analytical implementation task, complete the Pre-Implementation Synthesis defined in `HOW-WE-WORK.md` before mutation.

### Tier 2 — Task-Dependent Governance

Read these after Tier 1 when relevant:

- For metric calculation, analytical implementation, validation, interpretation, visualization, or insight logging: read `docs/METRIC_DEFINITION_CONTRACT.md` completely.
- When Phase 1 evidence is used: read the relevant sections of `docs/data_quality_report.md`.
- When creating, changing, or relying on a finding: read `docs/ANALYSIS_INSIGHT_LOG.md` and all related records.
- For notebook work: read the canonical SQL, Python modules/functions, tests, and source documentation used by that notebook.

### Tier 3 — Execution Materials

Read only the source files, schemas, tests, and supporting documents directly required by the authorized task.

If a required document is missing, contradictory, or materially ambiguous, stop and request a planning decision. Do not resolve governance or business-definition conflicts independently.

The execution plan governs scope and phase status. The Metric Contract governs analytical definitions. The accepted data-quality report provides Phase 1 evidence. The Insight Log governs the status of findings. Code and prior outputs cannot silently override them.

## Scope and Ownership

Agents must not independently change project scope, business definitions, metrics, stages, filters, windows, segments, or assumptions.

The user and planning assistant are the exclusive content editors of these protected documents:

- `AGENTS.md`
- `METROCAR_PROJECT_EXECUTION_PLAN.md`
- `docs/METRIC_DEFINITION_CONTRACT.md`

Implementation agents, including Kimi, must never edit, regenerate, reformat, rename, move, restore, delete, merge, conflict-resolve, or otherwise alter these files.

An implementation agent may stage, commit, or push an already reviewed, planning-owned change to a protected document only when the user gives explicit, task-specific authorization for the named file and named Git actions. This is transport authority only. The agent must not alter any byte of the reviewed change and must verify that the diff matches it without unrelated content. Any discrepancy, merge conflict, required edit, or additional change is a mandatory stop.

Without explicit authorization, implementation agents may only propose protected-document changes in their handover.

Write access to `docs/ANALYSIS_INSIGHT_LOG.md` must be explicitly assigned for the task. Otherwise, proposed entries belong in the handover. Treat the accepted `docs/data_quality_report.md`, source databases, source tables, and raw source files as read-only unless a separate authorization states otherwise.

## Communication and Learning Standard

All project deliverables must be written in English.

Make the work understandable to a student:

- explain why a material step is needed before explaining how it works;
- use plain language and define necessary technical terms;
- connect transformations and validations to their business purpose;
- explain joins, filters, assumptions, and edge cases when they materially affect results;
- keep explanations proportional to complexity and consequence.

Routine setup should remain concise. Important reasoning must not be hidden behind abstractions or unexplained code.

## Code Standard

Prefer simple, explicit, deterministic, and readable SQL and Python.

- Use descriptive names and small purposeful steps.
- Prefer direct SQL and straightforward Python over unnecessary frameworks or abstraction layers.
- Avoid premature optimization, speculative generalization, and overengineering.
- Add dependencies or infrastructure only when the authorized task requires them.
- Preserve the analytical grain and rules defined by the Metric Contract.
- Keep extraction, transformation, validation, and presentation separable when this improves verification.
- Do not change a business rule inside code to make a result or test pass.

If implementation reveals a schema conflict, missing definition, unexpected data condition, or required scope expansion, preserve the evidence and stop for a planning decision.

## Reproducibility and Traceability

A notebook is the student-facing analytical narrative. It is not the sole source of truth for analytical logic.

Every published metric or finding must be reproducible through one or both of:

- exact saved SQL identified by repository-relative path and stable query, CTE, statement, or output name;
- a canonical Python module and function identified by repository-relative path, import path, and function name.

Notebook-only calculations are insufficient final evidence. A notebook should invoke or clearly reference the canonical SQL or Python implementation and record the relevant parameters and source-data cutoff.

Every published metric must reference its governing Metric Contract section and its exact SQL and/or canonical Python implementation. Every finding must have an Insight Log ID and reproducibility reference. Every recommendation must identify the Validated finding or findings supporting it. Observations, interpretations, and recommendations must remain distinct.

Screenshots, copied result tables, and undocumented manual calculations may supplement evidence but cannot replace reproducible logic.

## Notebook Documentation

Place a Markdown explanation before every significant code cell or coherent group of closely related cells.

As applicable, explain:

- why the step is needed;
- the business question or validation objective;
- the input and analytical grain;
- the transformation, join, or filter;
- the governing contract rule;
- the expected output;
- how success will be validated.

Import-only, configuration-only, and simple display cells may share a short explanation. Avoid unexplained monolithic cells.

## Secrets

Never open, expose, print, log, copy, stage, or commit:

- `.env` files;
- credentials, tokens, passwords, or private keys;
- connection strings;
- other secret-bearing files or values.

Authorized processes may consume already configured environment variables, but documentation and logs may refer only to variable names. Use sanitized placeholders. Before any authorized commit, verify that staged changes contain no secrets or local environment files.

## Phase Gates and Checkpoints

Every readiness gate and checkpoint in the execution plan is mandatory.

At a checkpoint:

1. stop implementation;
2. summarize completed work and affected files;
3. report the exact validation and test evidence;
4. disclose unresolved issues and limitations;
5. identify the proposed next action;
6. wait for explicit authorization.

Approval of one task does not authorize another task or phase. Meeting readiness conditions does not itself authorize implementation. A failed material validation, governance conflict, or required scope expansion is an automatic stop.

## Validation

Run all validations required by the authorized task, execution plan, and Metric Contract.

As applicable, verify:

- analytical grain and base-population preservation;
- join direction, cardinality, and row multiplication;
- filters, date boundaries, nulls, and explicit unknown categories;
- stage membership, subset relationships, and monotonicity;
- segmented-to-overall reconciliation;
- edge cases and data-quality exceptions;
- reproducibility through the canonical SQL or Python source;
- relevant automated tests.

Record what was run and the result. Never report an unrun check as passed, treat absence of an error as proof of correctness, or publish a result with an unresolved material validation failure.

Detailed analytical rules belong in `docs/METRIC_DEFINITION_CONTRACT.md` and must not be duplicated or redefined here.

## Git Discipline

Keep changes small, scoped, and reviewable.

- Inspect the working state before editing.
- Preserve unrelated and pre-existing user changes.
- Modify only authorized files.
- Avoid unrelated cleanup, mass formatting, or opportunistic refactoring.
- Review the final diff for scope, accidental changes, generated files, and secrets.
- Run required validations before any authorized commit.
- Do not stage, commit, or push unless explicitly authorized.
- Keep commit and push as separate authorization gates by default. Data may explicitly bundle them for a small, already-reviewed, low-risk change with fixed scope; the agent must still verify the approved diff, clean working state, and remote divergence before a normal non-force push.
- Use a clear task-specific commit message.
- Do not rewrite history, discard user work, or use destructive Git operations without explicit approval.

Protected-document handling must always follow the stricter ownership rule above.

## Completion Standard

A task is complete only when:

- the authorized scope is satisfied;
- ownership and protected-file boundaries were respected;
- the result is understandable and reproducible;
- required traceability is present;
- validation and tests passed, or limitations were accurately reported;
- no unsupported business assumption was introduced;
- the agent stopped at the required checkpoint.

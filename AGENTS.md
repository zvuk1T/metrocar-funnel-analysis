# AGENTS.md

## Purpose

This document defines the binding working method for all agents in this repository. Reading project documents does not authorize implementation, scope changes, Git actions, or progression through a phase gate.

## Mandatory Tiered Reading

Read documents in the following order.

### Tier 1 — Every Task

1. Read `AGENTS.md` completely.
2. Read `HOW-WE-WORK.md` completely.
3. Read the governing sections of `METROCAR_PROJECT_EXECUTION_PLAN.md`, including:
   - current project and reset status;
   - the current authorized task;
   - the document map and ownership;
   - the applicable gate or checkpoint;
   - the relevant reset note.
4. Read the explicit task authorization, brief, or handover.

Before acting, identify the authorized scope, permitted files, governance-controlled files and ownership boundaries, required evidence, and next mandatory stop.

Before any non-trivial code or analytical implementation task, complete the Pre-Implementation Synthesis defined in `HOW-WE-WORK.md` before mutation.

### Tier 2 — Task-Dependent Governance

Read these after Tier 1 when relevant:

- For questions about the original MasterSchool curriculum, assignment provenance, or historical requirements: read `docs/MASTERSCHOOL_METROCAR_SOURCE_BRIEF.md` completely.
- For metric calculation, analytical implementation, validation, interpretation, visualization, or insight logging: read `docs/METRIC_DEFINITION_CONTRACT.md` completely.
- When accepted structural or source-profile evidence is used: read the relevant sections of `docs/data_quality_report.md`.
- When creating, changing, or relying on a finding: read `docs/ANALYSIS_INSIGHT_LOG.md` and all related records.
- For work on the primary learner-facing main analytical Python document, or on any separately authorized supplementary notebook or walkthrough: read the canonical SQL, supporting Python modules/functions, tests, and source documentation used by that analytical step.

### Tier 3 — Execution Materials

Read only the source files, schemas, tests, and supporting documents directly required by the authorized task.

If a required document is missing, contradictory, or materially ambiguous, stop and request a planning decision. Do not resolve governance or business-definition conflicts independently.

The execution plan governs current scope, status, and gates. The MasterSchool Source Brief governs reconstruction of the original curriculum, not current metric meaning. The Metric Contract governs current analytical definitions. The accepted data-quality report provides snapshot-specific structural evidence. The Insight Log governs the status of current findings. Code, archived documents, and prior outputs cannot silently override them.

## Scope, Ownership, and Active Crew Roles

Agents must not independently change project scope, business definitions, metrics, stages, filters, windows, segments, assumptions, findings, recommendations, phase status, or authorization boundaries.

Task scope must remain explicit and bounded. Calibrate its size under the proportional task-scope rule in `HOW-WE-WORK.md`; bounded does not mean smallest possible.

### Active Crew responsibilities

- **Data — project owner, learner, and final authority.** Data owns project scope, analytical meaning, Learning PASS, destructive-operation authorization, Git transport authorization, phase progression, and deployment approval.
- **Troi — reasoning, learning, review, storytelling, and coordination.** Troi provides learning guidance, analytical review, business interpretation, storytelling, coordination, review of actual artifacts and diffs, and preparation of bounded tasks. Troi does not perform repository or Git mutation.
- **Spock — research, audit, synthesis, and substantial drafting.** Spock performs deep repository research, architecture analysis, comparison of alternatives and trade-offs, reasoned forecasting of likely consequences, substantial Markdown drafting, preparation of exact repository-ready documentation text, recommendations, and implementation briefs. Spock does not perform repository mutation, Python or SQL implementation, tests, frontend implementation, command execution, Git or GitHub operations, or deployment.
- **Geordi — repository implementation.** Geordi performs repository inspection and, under explicit bounded authorization, repository mutation, application of approved Markdown changes, Python, SQL, analytical tests, frontend work, technical validation, command execution, and Git or GitHub operations. Geordi reports implementation evidence and stops at every required boundary.

### Prompt routing

For substantive repository work, Data and Troi first agree the objective, decisions, scope, and acceptance conditions. Troi sends Spock a concise read-only research brief.

Spock returns analysis, recommendations, risks, and any required repository-ready draft content. Spock must not invoke Geordi, open or manage another agent or chat, or author the final authorization-bearing Geordi execution prompt unless Data explicitly authorizes that exact action.

Troi reviews Spock’s findings with Data and writes the complete final copy-ready Geordi task. Only the version explicitly approved by Data may be sent to Geordi.

A trivial, exact, mechanical change may bypass Spock when additional research would add no material analytical, architectural, documentation, or safety value.

Data holds final substantive decision authority for the governance-controlled documents:

- `AGENTS.md`
- `METROCAR_PROJECT_EXECUTION_PLAN.md`
- `docs/METRIC_DEFINITION_CONTRACT.md`

This authority governs what may be decided. It does not make those files repository-write-protected. Troi and Spock may prepare and review proposed content within their active roles. Geordi may apply a Data-approved change only when the current bounded task explicitly authorizes the named file or files and the intended substantive change.

Such authorization must provide enough scope to determine:

- which file or files may change;
- the objective or content intent;
- what must remain unchanged;
- required validation;
- the mandatory STOP boundary.

Repository mutation authority does not transfer planning or analytical decision authority.

Geordi must not independently invent, expand, reinterpret, or change:

- governance;
- project scope;
- business or metric definitions;
- analytical grain;
- funnel stages;
- filters or windows;
- attribution rules;
- formulas;
- assumptions;
- accepted evidence or findings;
- recommendations;
- phase status;
- authorization boundaries.

When a task supplies exact replacement text, Geordi must apply it faithfully. If repository context makes exact application impossible without a substantive decision, Geordi must STOP and report the discrepancy.

When a task supplies bounded semantic intent rather than exact replacement text, Geordi must make the least expansive faithful edit that fully implements the authorized decision and must report the exact resulting diff for review.

Reading, research, or planning does not authorize mutation.

Mutation does not authorize staging, commit, push, deployment, destructive Git operations, or progression into another task or phase.

Those remain separate authorization gates except where Data explicitly bundles actions under the proportional Git rule.

If an authorized governance edit reveals an unexpected conflicting diff, missing canonical source, merge conflict, substantive ambiguity, or required scope expansion, preserve the evidence and STOP rather than resolving the issue independently.

Write access to `docs/ANALYSIS_INSIGHT_LOG.md` must still be explicitly assigned for the task. Otherwise, proposed entries belong in the handover.

Treat the accepted `docs/data_quality_report.md`, source databases, source tables, and raw source files as read-only unless a separate authorization explicitly states otherwise.

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

The main analytical Python document is both the real Python analytical implementation and the primary learner-facing course. It must keep the actual analysis understandable from top to bottom, remain governed by the Metric Contract, and retain the supporting SQL, tests, and reconciliation evidence required for reproducibility.

Every published metric or finding must be reproducible through one or both of:

- exact saved SQL identified by repository-relative path and stable query, CTE, statement, or output name;
- an approved canonical Python implementation identified by repository-relative path and a durable locator.

An approved canonical Python implementation may use either of the following forms, or an approved combination of them; neither form requires the other:

- a learner-facing analytical notebook or cell-based `.py` document, identified by a stable named section, `# %%` analytical section where applicable, named output, or other durable locator; or
- a supporting Python module and function, identified by repository-relative path, import path, and function name where applicable.

The canonical reference must record the relevant parameters and source-data cutoff. A learner-facing analytical artifact may itself be canonical when it is explicit, reproducible, inspectable, testable where appropriate, traceable to governed metric definitions, and understandable by Data. In that case, it does not need to duplicate or invoke a separate Python module or function. A supporting module or function remains optional and should be introduced only when it materially improves correctness, reuse, validation, or maintainability.

A supplementary notebook or walkthrough may be added later only under separate authorization and for a concrete supplementary purpose. If it is not itself the approved canonical Python implementation, it must reuse or execute the real analytical implementation, or clearly reference or reconcile to it, rather than reproduce it. It must not be required to understand the real Python analysis, become a second implementation, redefine metric meaning, or replace the main analytical Python document as the primary learning path. The main document and any supplementary artifact must record the relevant parameters and source-data cutoff.

Every published metric must reference its governing Metric Contract section and its exact SQL and/or canonical Python implementation. Every finding must have an Insight Log ID and reproducibility reference. Every recommendation must identify the Validated finding or findings supporting it. Observations, interpretations, and recommendations must remain distinct.

Screenshots, copied result tables, and undocumented manual calculations may supplement evidence but cannot replace reproducible logic.

## Main Analytical Python Document

Before every significant analytical concept or question, or coherent group of closely related steps, place a concise `# %% [markdown]` learning block next to the actual analytical code in the main cell-based Python document. Follow the learner-facing reading spine in `HOW-WE-WORK.md` rather than duplicating it here.

As applicable, explain:

- the topic or business question and why the step is needed;
- the approach, input, and analytical grain or state;
- the relevant DataCamp learning pointer when a material technique first appears;
- the transformation, join, or filter;
- the governing contract rule;
- the result or observation and how it is validated;
- the notes Data needs to explain or reconstruct the step;
- the next question opened by the result.

Import-only, configuration-only, and simple display steps may share a short explanation. Avoid unexplained monolithic code sections.

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

Keep changes bounded, proportionate, scoped, and reviewable. The proportional task-scope rule does not relax the exact-file, unrelated-work, validation, or Git safeguards below.

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

Governance-controlled document handling must always follow the decision-authority, explicit-mutation-authorization, Git-gate, and STOP rules above.

## Completion Standard

A task is complete only when:

- the authorized scope is satisfied;
- decision-authority, ownership, and authorized file-scope boundaries were respected;
- the result is understandable and reproducible;
- required traceability is present;
- validation and tests passed, or limitations were accurately reported;
- no unsupported business assumption was introduced;
- the agent stopped at the required checkpoint.

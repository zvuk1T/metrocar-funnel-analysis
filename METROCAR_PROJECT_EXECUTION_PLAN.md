# Metrocar Funnel Analysis — Current Rebuild Plan

> **Status:** DOCUMENTATION RESET CHECKPOINT — ANALYTICAL REBUILD AWAITS A SEPARATELY APPROVED QUESTION-FIRST TASK
>
> **Current next gate:** Data and Troi define and approve the first business question, evidence contract, learning path, validation requirements, and bounded STOP point.
>
> This document does not authorize analytical implementation, database access, frontend work, repository mutation outside an explicitly approved task, Git transport, deployment, or progression into another task.

## 1. Purpose

This document governs what the current Metrocar rebuild is doing now.

It records:

- the trusted reset checkpoint;
- the active document map;
- the current objective;
- the analytical working sequence;
- the gates required for each analytical slice;
- the next eligible task; and
- the current STOP boundaries.

It intentionally does not reproduce the previous project history, prescribe an unapproved frontend architecture, or create a speculative multi-phase roadmap.

Authority, mutation rules, Crew responsibilities, validation discipline, and Git gates remain governed by `AGENTS.md`.

Learning and reasoning methodology remain governed by `HOW-WE-WORK.md`.

## 2. Trusted Reset Checkpoint

The documentation reset begins from the pushed MasterSchool Source Brief checkpoint:

- branch: `main`;
- checkpoint commit: `2ee20cdbf5893ea88a0380e889eaf2725524bba7`;
- commit message: `docs: add MasterSchool Metrocar source brief`.

This commit identifies the historical starting checkpoint for the documentation reset. Current Git state must still be independently verified before every repository task.

At this reset checkpoint:

- `docs/MASTERSCHOOL_METROCAR_SOURCE_BRIEF.md` is the accepted historical reconstruction of the original MasterSchool curriculum.
- `docs/METRIC_DEFINITION_CONTRACT.md` remains the authority for current Metrocar analytical meaning until Data approves a separate analytical review or amendment.
- `docs/data_quality_report.md` remains accepted, snapshot-specific structural and source evidence.
- `docs/ANALYSIS_INSIGHT_LOG.md` is the active register for the rebuild and contains no current accepted findings after the documentation reset.
- The six earlier Phase 3 records remain preserved as historically validated records in Git history and the local archive. They do not preselect the new analytical story.
- Previous analytical code, outputs, tests, frontend work, visual plans, and architectural decisions may be inspected later as historical or regression evidence when an authorized task requires them. Their existence does not make them current architecture or current findings.
- No frontend architecture or recruiter-facing story is currently approved.

## 3. Active Document Map

| Document | Current role |
|---|---|
| `AGENTS.md` | Defines who may decide, research, review, mutate, validate, use Git, and authorize progression. |
| `HOW-WE-WORK.md` | Defines how Data learns, how analysis is explained, how Technical PASS and Learning PASS differ, and how evidence becomes judgment. |
| `METROCAR_PROJECT_EXECUTION_PLAN.md` | Defines the current rebuild status, objective, next gate, and STOP boundaries. |
| `README.md` | Provides the public repository entry point. It summarizes but cannot override canonical documents. |
| `docs/MASTERSCHOOL_METROCAR_SOURCE_BRIEF.md` | Reconstructs what the original MasterSchool curriculum taught and required. It is historical source authority, not current metric or implementation authority. |
| `docs/METRIC_DEFINITION_CONTRACT.md` | Defines current analytical grain, stages, joins, filters, attribution, formulas, assumptions, and validation rules. |
| `docs/ANALYSIS_INSIGHT_LOG.md` | Registers current governed findings and their evidence status. |
| `docs/data_quality_report.md` | Preserves accepted structural and source-profile evidence for its recorded snapshot. |
| `docs/DATACAMP_PYTHON_REFERENCE.md` | Provides verified Python/Pandas learning navigation. |
| `docs/DATACAMP_SQL_REFERENCE.md` | Provides verified SQL learning navigation. |

The following material is historical only and is not part of mandatory active reading:

- `.local_archive/docs/METROCAR_PROJECT_EXECUTION_PLAN.md`;
- `.local_archive/docs/docs/ANALYSIS_INSIGHT_LOG.md`;
- `.local_archive/docs/docs/METROCAR_VISUAL_SPEC.md`; and
- `.local_archive/docs/docs/IMPLEMENTATION_RESET_RETROSPECTIVE.md`.

The local archive is git-ignored. Git history remains the tracked recovery path for historical versions that were previously committed.

## 4. Current Objective

Rebuild Metrocar as an understandable, recruiter-facing funnel-analysis case study in which every material result follows this sequence:

```text
original MasterSchool source
→ business question
→ required evidence and analytical grain
→ verified DataCamp learning path
→ understandable SQL and/or Python/Pandas analysis
→ semantic validation
→ Technical PASS
→ Data understanding and Learning PASS
→ interpretation and judgment
→ current finding status
→ next question
```

The rebuild must demonstrate:

```text
question
→ evidence
→ reasoning
→ judgment
→ result
```

Code sophistication is not the goal.

The analytical implementation should prefer:

- understanding before automation;
- WHY before HOW;
- business question before technique;
- one visible analytical idea at a time;
- explicit source and grain;
- visible joins, filters, and transformations;
- descriptive intermediate variables;
- DataCamp-learnable SQL and Pandas;
- evidence-bounded interpretation; and
- proportionate validation.

## 5. Analytical Slice Gate

No analytical slice begins until Data and Troi approve a bounded brief containing:

1. the audience and decision;
2. the business question;
3. the measurable analytical question;
4. source tables and required fields;
5. input and output grain;
6. cohort, cutoff, filters, and assumptions;
7. the applicable current Metric Contract definitions;
8. any distinction or conflict between the historical Source Brief and current Metric Contract;
9. the required SQL and/or Python/Pandas evidence;
10. verified DataCamp learning paths for material techniques;
11. semantic validation and reconciliation requirements;
12. the exact permitted files and mutation scope;
13. the teach-back expectations for Data; and
14. the mandatory STOP point.

If the proposed question requires a new or changed metric definition, the Metric Contract review and Data decision occur before implementation.

Geordi may implement only the exact approved slice. Completion of one slice does not authorize another.

## 6. Acceptance for an Analytical Slice

### Technical PASS

Technical PASS applies only to the stated artifact, source state, parameters, and evidence scope.

As applicable, it requires evidence for:

- source and analytical grain;
- joins and cardinality;
- base-population preservation;
- stage membership and subset relationships;
- filters, cutoff, and cohort boundaries;
- formulas and denominators;
- missing or unavailable values;
- segmented-to-overall reconciliation;
- SQL/Pandas or independent-path reconciliation;
- relevant tests; and
- material limitations.

Technical PASS does not prove that Data understands the analysis.

### Learning PASS

Only Data grants Learning PASS.

Data must be able to explain:

- why the step exists;
- what enters and leaves it;
- the relevant grain;
- why the source, join, filter, or calculation is appropriate;
- what the result supports;
- what it does not support;
- how it was validated; and
- where the material technique can be relearned.

Learning PASS does not prove that a real Metrocar finding exists.

### Finding acceptance

A result becomes a current governed finding only after:

- its evidence is reproducible;
- applicable Technical PASS is recorded;
- Troi reviews the actual artifact and interpretation;
- limitations and alternative explanations are visible;
- the claim does not exceed the evidence; and
- an explicitly authorized update records it in `docs/ANALYSIS_INSIGHT_LOG.md`.

A previous historical finding does not become current merely because its old code or result still exists.

## 7. Current Next Task

The next eligible planning task is:

> Data and Troi select the first business question for the clean analytical rebuild and define its evidence contract, analytical grain, applicable Metric Contract rules, verified DataCamp path, validation requirements, Learning PASS expectations, exact implementation boundary, and STOP point.

This plan does not choose that question.

It also does not authorize Spock or Geordi to begin its analysis.

## 8. Historical and Current Analytical Boundaries

The MasterSchool Source Brief answers:

> What did the original curriculum teach and require?

The Metric Contract answers:

> What do current Metrocar analytical metrics mean?

The active Insight Log answers:

> What has the current rebuild established?

The data-quality report answers:

> What structural source evidence was accepted for its recorded snapshot?

These roles must not be collapsed.

A difference between the historical curriculum and the current Metric Contract must be recorded as a distinction or conflict. It must not be resolved silently by rewriting either source.

Previous implementation and findings may later be used as regression evidence, comparison material, or audit history. They must not dictate the new question, architecture, interpretation, or recruiter-facing conclusion.

## 9. Frontend Boundary

Frontend and portfolio presentation remain deferred until the analytical story contains enough accepted evidence to justify them.

No previous Visual Spec, dashboard layout, technology stack, component architecture, hosting target, chart sequence, or selected conclusion currently governs the rebuild.

A later frontend task must:

- consume only accepted analytical evidence;
- preserve Metric Contract meaning;
- present findings already accepted through the active Insight Log;
- remain separate from analytical authority; and
- receive its own Data-approved scope and acceptance conditions.

## 10. STOP Boundaries

This plan does not authorize:

- changing the Metric Contract;
- selecting a business question without Data and Troi approval;
- analytical implementation;
- database access;
- treating historical findings as current findings;
- frontend or visualization implementation;
- modifying archived history;
- staging, committing, or pushing;
- deployment;
- deleting historical work; or
- progressing automatically into another slice.

A material conflict, missing definition, unsupported assumption, validation failure, or required scope expansion is a STOP condition.

## 11. Documentation Reset Note

On 2026-09-02, the active documentation model was reset to separate current authority from retained history.

The reset:

- made the MasterSchool Source Brief the central historical curriculum reference;
- replaced the accumulated execution plan with this concise current plan;
- reset the active Insight Log without changing the historical status of earlier records;
- removed the old Visual Spec from current authority;
- retained the implementation-reset retrospective as local historical reasoning;
- preserved the Metric Contract without changing analytical meaning;
- kept the data-quality and DataCamp references active; and
- granted no analytical, frontend, Git, or deployment authority.

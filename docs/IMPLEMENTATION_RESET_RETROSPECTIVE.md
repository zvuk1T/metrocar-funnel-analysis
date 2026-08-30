# Metrocar Implementation Reset Retrospective

## Status and purpose

This document records why Metrocar implementation work stopped at the
pre-reset checkpoint and what must change before implementation restarts. It is
a retrospective and restart guide, not a governance authority. It does not
change metric definitions, accepted analytical evidence, project scope, phase
status, or Git authorization.

This retrospective is intentionally self-contained. Unlike `AGENTS.md` or an
ordinary task prompt, it is not meant to be mandatory reading before every
repository operation. Its archival length is deliberate: a future chat,
implementation restart, or similar project should be able to understand the
failure analysis and restart model without reconstructing them from old chats.
That purpose does not justify repeating the document's content in routine
instructions or prompts.

The complete authored state that existed before any possible reset was
preserved at this Git checkpoint:

- commit: `cb863f727d7d6ea5a7fa3e77699097ba2056f1da`
- message: `chore: preserve pre-reset Metrocar work`

That commit is an archival safety checkpoint. It makes the work recoverable; it
does not accept the implementation, learning walkthrough, Phase 4 prototype,
README claims, or any other previously unaccepted artifact.

This retrospective uses three labels throughout:

- **Observed project fact** — something supported by the repository, its Git
  history, accepted evidence, or Data's recorded reset decision.
- **Diagnosis** — an explanation of how the observed condition contributed to
  the failure mode. A diagnosis is retrospective interpretation, not a new
  business rule.
- **Corrective principle** — a proposed operating rule for the restart. Where
  adoption would require a governance change, it remains a proposal until Data
  authorizes that change separately.

**Subsequent policy alignment.** Historical descriptions below retain the
earlier beginner-to-intermediate target because that was the policy under
which the calibration and reset occurred. Data has since changed the
forward-looking analytical rule: DataCamp remains the learning boundary, but
beginner, intermediate, and advanced DataCamp-learnable techniques are all
eligible when Data can understand, explain, and approximately reconstruct
their use. Frontend/web engineering is now explicitly outside that analytical
DataCamp requirement.

## 1. Why implementation stopped

Metrocar did not stop because its accepted analytical evidence had been shown
to be wrong. It stopped because technical correctness became easier to prove
than the project's central learning outcome: Data must be able to read,
understand, explain, reproduce, and defend the analysis at the agreed learning
level.

The project had accumulated a technically credible analytical core, a separate
student walkthrough, public-data generation, and a frontend prototype. At the
same time, the distance between the canonical implementation and the intended
beginner-to-intermediate learning experience had grown. Further local
refactoring risked preserving that architecture while repeatedly translating
around it. Data therefore chose to stop incremental refinement and reconsider
the implementation structure from verified knowledge.

**Observed project fact.** Tests, source-cardinality checks, SQL/Pandas
reconciliation, and accepted checkpoints demonstrated analytical consistency.
The accepted User Funnel remained `23,608 → 17,623 → 12,406 → 6,233`; the
accepted Ride Funnel remained `385,477 → 223,652 → 212,628 → 148,464`; and the
shared source cutoff remained `2022-04-24 20:00:00`.

**Diagnosis.** These checks answered whether two implementations agreed and
whether contract rules were preserved. They did not answer whether Data could
follow the code in reading order or reconstruct the analysis independently.

**Corrective principle.** Technical evidence remains necessary, but no longer
stands in for learning acceptance. The restart must make correctness and human
comprehension separate, explicit gates.

## 2. What Metrocar was trying to achieve

Metrocar has always had two legitimate goals:

1. produce a reproducible, professionally credible funnel analysis; and
2. make the analytical reasoning learnable at a DataCamp/MasterSchool
   beginner-to-intermediate level.

The governing documents had already established this intention and its
supporting boundaries:

- `docs/METRIC_DEFINITION_CONTRACT.md` owns metric meaning and analytical
  grain;
- `docs/data_quality_report.md` preserves accepted Phase 1 evidence;
- `docs/ANALYSIS_INSIGHT_LOG.md` separates observations, interpretations,
  recommendations, and acceptance status;
- canonical SQL and Pandas provide reproducible analytical implementations;
- `HOW-WE-WORK.md` defines the learning and explainability expectations;
- `AGENTS.md` protects scope, evidence, secrets, unrelated work, and phase
  gates;
- Data, Troi, and Spock have distinct approval, planning/review, and execution
  responsibilities.

The failure was not the existence of professional validation or governance. It
was that the system increasingly optimized for proving completion while the
learning experience remained a downstream translation problem.

### 2.1 What the project-level operating instructions already required

The learning principles in this retrospective were not invented after the
failure. Before the problematic implementation was created, the project and
custom operating instructions had already established the following model.

Responsibility was separated deliberately:

- Data was the project owner, learner, and final decision authority.
- Troi owned reasoning, learning guidance, planning, analytical review,
  storytelling, and the preparation of bounded Spock tasks.
- Spock owned repository inspection and authorized execution, including file
  mutation, tests, validation, and separately authorized Git work.

Repository state and authorization were also explicit:

- Current repository sources outranked chat memory and older summaries.
- Canonical preflight was required before repository recommendations or tasks.
- Reading and planning did not authorize mutation.
- Mutation did not automatically authorize staging, commit, push, deployment,
  phase progression, or another task.
- Troi-to-Spock work had to be bounded by an objective, exact scope, validation,
  and an explicit STOP.
- Silent scope expansion was forbidden, and unrelated or pre-existing
  working-tree changes had to be preserved.

The learning standard was already substantive rather than cosmetic:

- Understanding came before automation, and WHY came before HOW.
- Data was expected to understand the business question, analytical grain,
  transformations, joins, assumptions, validation, evidence limits, and
  business meaning.
- DataCamp beginner-to-intermediate analytical complexity was the normal target,
  using recognizable Pandas and SQL idioms.
- Preferred analytical constructs included ordinary filtering, Boolean masks,
  new columns, `groupby`, `agg`, `any`, `sum`, `count`, `nunique`, `notna`,
  `isna`, `merge`, simple ratios, and ordinary SQL.
- Class hierarchies, generic analytical engines or frameworks, deep helper
  stacks, speculative abstraction, clever compression, and unnecessary
  defensive machinery were discouraged.
- Text or Markdown was expected to teach while code demonstrated. An ordinary
  code cell would normally show one analytical idea through short, explicit
  transformations.
- The Metric Contract governed analytical meaning. Student-friendly code could
  not weaken validation, reproducibility, privacy, tests, or analytical
  invariants.
- Storytelling had to distinguish observed fact, interpretation, hypothesis,
  and recommendation.
- Portfolio, frontend, and automation work could not outrun analytical
  understanding.
- A meaningful slice was incomplete if Data could not explain why each material
  step existed, what it did, and how it was validated.

The reset was therefore not caused by an absence of explicit learning rules.
It was caused by repeated failure to convert those rules into hard
implementation and acceptance gates.

## 3. What happened, why it mattered, and what should change

### 3.1 Technical correctness became the dominant acceptance signal

**Observed project fact.** The repository contains detailed tests, validation
totals, subset and monotonicity checks, segmented reconciliation, and live
SQL/Pandas comparison. User Funnel calibration reached `all_match=True` and
preserved the accepted cutoff and counts. Ride Funnel regression also remained
reconciled.

**Diagnosis.** These are strong regression controls, but their clarity made
them the easiest evidence to report. Completion reports could therefore look
decisive even when the harder question — whether Data understood the artifact
— had not been answered.

**Corrective principle.** Every analytical slice must produce two decisions:
a technical PASS and a learning PASS. Neither can imply the other.

### 3.2 Technical PASS and learning PASS were treated as one gate

**Observed project fact.** Prior calibration reviews correctly verified grain,
membership, attribution, formulas, interfaces, tests, and live reconciliation.
Data's later reset decision clarified that this did not establish personal
understanding of the implementation.

**Diagnosis.** The acceptance language compressed two different questions into
one: “Is the result correct?” and “Can the learner explain how it was produced?”
The first had objective automated evidence; the second needed artifact-level
human review.

**Corrective principle.** A slice is not fully accepted until both gates are
recorded separately. Technical PASS may occur first, but phase progression must
wait for learning PASS.

### 3.3 “Student-friendly” was sometimes accepted by proxy

**Observed project fact.** Spock produced completion reports describing
implementations as simpler, explicit, or DataCamp-appropriate. Those reports
were legitimate execution evidence. At some checkpoints, Troi relied
materially on those reports, focused diff evidence, and technical validation
when recommending that the intended learning level had been reached. Troi had
not always independently reviewed the complete learner-facing artifact in the
same top-to-bottom order Data would experience it. Data's later direct review
of the file exposed the mismatch between the reported learning level and the
actual reading experience.

**Diagnosis.** Execution review and learning review became partially collapsed
into one evidence stream. The implementation agent therefore supplied part of
the evidence for its own pedagogical acceptance, while Troi's independent
artifact-level review was too narrow at those checkpoints. An agent can assess
syntax, helper count, comments, and apparent conceptual load, but its
self-assessment of complexity cannot prove learner comprehension.

**Corrective principle.** Spock reports evidence; Troi independently reviews
the actual artifact and its complete reading experience; Data gives final
learning acceptance. “Student-friendly” cannot be accepted solely from the
implementation agent's self-report.

### 3.4 A locally simplified User Funnel was generalized too far

**Observed project fact.** The accepted User Funnel calibration replaced
duplicate-resolution machinery with a clearer flow: validate source conditions,
aggregate ride flags, anchor on downloads, left-join signups and flags, derive
stages and attribution, then validate. SQL was calibrated to the same model.

**Diagnosis.** This was a real improvement to one analytical path. It did not
automatically simplify the rest of `analysis/funnel.py`, the Ride Funnel,
cross-cutting validation, segment production, reconciliation, or the reading
experience of the project as a whole.

**Corrective principle.** Evaluate simplicity at three levels: the changed
section, the containing artifact, and the learner's end-to-end path. A local
improvement may pass locally without establishing system-wide learning PASS.

### 3.5 Production code and the learning walkthrough diverged

**Observed project fact.** At the archival checkpoint, `analysis/funnel.py` is
a large canonical module containing parameter handling, source checks, User and
Ride Funnel construction, summaries, segments, and validation. The later
`learning/metrocar_walkthrough.py` is a separate cell-based teaching artifact
that reconstructs and explains parts of the analysis and reconciles them to
canonical results.

**Diagnosis.** The canonical implementation was allowed to optimize for broad
correctness and compatibility, while the walkthrough was expected to translate
that complexity later. This created two mental models: the code that proves the
analysis and the code the learner is expected to understand. Translation work
then became permanent architectural debt.

**Corrective principle.** The simplest accepted analytical path should be the
canonical path wherever possible. A walkthrough may add narrative and staged
display, but should not need to hide or substantially reinterpret the core
implementation.

### 3.6 The DataCamp complexity rule was not enforceable enough

**Observed project fact.** Metrocar governance already contained a concrete
DataCamp beginner-to-intermediate analytical requirement before the reset.
`HOW-WE-WORK.md` named preferred constructs including filtering, Boolean masks,
new columns, `groupby`, `agg`, `any`, `sum`, `count`, `nunique`, `notna`,
`isna`, `merge`, simple ratios, and ordinary SQL. It also discouraged class
hierarchies, generic analytical engines or frameworks, deep helper stacks,
speculative abstractions, dense or clever code, and unsupported defensive
machinery. The detailed verified DataCamp maps were not initially
project-local, which weakened discoverability, but the underlying simplicity
requirement already existed.

**Diagnosis.** The primary failure was enforcement. The DataCamp rule operated
as a default rather than a hard acceptance boundary, and the existing wording
allowed production robustness to exceed the target when it appeared justified.
There was no mandatory pre-mutation check reconciling every proposed analytical
construct with the approved learning vocabulary, and no automatic STOP before
an out-of-vocabulary construct was introduced. Technical correctness could
therefore win repeated local trade-offs over learning simplicity. More
documentation alone would not have solved this problem.

**Corrective principle.** At the pre-reset checkpoint, the proposed restart
rule was that analytical Python and SQL should remain inside the project-local
verified beginner-to-intermediate vocabulary unless Data approved a specific
exception. That statement remains historically accurate, but it no longer
defines the forward-looking policy.

Data subsequently replaced the difficulty ceiling with this rule:

> Metrocar analytical code may use DataCamp-learnable techniques at any level
> — beginner, intermediate, or advanced — provided Data can learn, understand,
> explain, and approximately reconstruct the implementation and its role in
> the analysis.

The project-local Python and SQL maps are starting references, not exhaustive
catalogs. Non-obvious or advanced techniques should identify a genuine
official DataCamp learning path when reasonably possible. The acceptance
boundary is Data's understanding and the clarity of the combined analytical
architecture, not the course difficulty label. Correctness, validation,
privacy, reproducibility, and tests remain mandatory without creating a
separate production-complexity bypass.

### 3.7 Project-critical DataCamp maps lived outside Metrocar

**Observed project fact.** The verified Python and SQL reference maps
originally lived outside this repository. Public-safe copies now exist as
`docs/DATACAMP_PYTHON_REFERENCE.md` and
`docs/DATACAMP_SQL_REFERENCE.md`. They preserve verified course structure,
concept summaries, typical idioms, complexity calibration, and Metrocar
transfer guidance without making DataCamp an authority over metric meaning.

**Diagnosis.** Detailed reference material supporting an existing complexity
constraint is easy to omit from a new chat and hard to audit when it is not
available in the working repository. That weakened consistent application of
the rule even though the rule itself already existed.

**Corrective principle.** Durable project-critical knowledge belongs in the
repository, in a public-safe form, and prompts should point to it rather than
reproduce it.

### 3.8 Instruction duplication accumulated

**Observed project fact.** Related rules and explanations appeared across
ChatGPT Project/custom instructions, `AGENTS.md`, `HOW-WE-WORK.md`, the
execution plan, handovers, and Troi-to-Spock prompts. Repetition was often added
to prevent a known failure from recurring.

**Diagnosis.** Repetition increased context volume without guaranteeing
salience. It also created stale variants, possible contradictions, and more
interpretive work before task execution. A rule repeated six times is not
necessarily six times stronger.

**Corrective principle.** State each stable rule once in the authority that
owns it. Other documents and prompts should link or route to that source and
repeat only the task-specific consequence.

Current official agent guidance supports this direction. OpenAI describes a
short repository instruction file as a map into deeper, versioned project
knowledge. GitHub recommends short, self-contained instructions and
path-specific guidance where global instructions would be overloaded.
Anthropic similarly recommends concise, structured project instructions and
warns that long or conflicting instruction layers reduce adherence. These are
tool-specific implementations of the same general lesson: context needs
architecture, not accumulation.

### 3.9 `AGENTS.md` became too much of an instruction manual

**Observed project fact.** `AGENTS.md` contains durable and valuable safeguards,
including reading order, ownership, validation, phase gates, secrets, Git
discipline, and completion criteria. It also asks every task to load several
other documents and carries substantial explanatory content itself.

**Diagnosis.** As the file grew, its routing purpose competed with procedural
detail. Universal guardrails, analytical policy, learning guidance, and task
workflow became harder to distinguish. The cost is paid at the start of every
task, including small ones.

**Corrective principle.** In a future separately authorized governance pass,
`AGENTS.md` should primarily route agents to the correct authority and retain
only universal execution guardrails that genuinely apply to every task. It
should not duplicate the content of the documents it routes to.

### 3.10 The execution plan accumulated too many responsibilities

**Observed project fact.** `METROCAR_PROJECT_EXECUTION_PLAN.md` carries project
status, current authorization, document ownership, requirements, architecture,
phase gates, implementation plans, acceptance evidence, historical decisions,
and a changelog.

**Diagnosis.** Combining active plan, specification, status ledger, evidence
archive, and history makes the document harder to scan and more likely to
contain stale details. A small status update can require navigating a large
mixed-purpose record.

**Corrective principle.** Future planning should separate current work and
status from durable requirements and retrospective history. One document may
route to the others, but should not need to restate all of them.

### 3.11 Long chats and handovers carried too much project memory

**Observed project fact.** Successive tasks relied on detailed prompts and
handoffs to reproduce checkpoint SHAs, accepted evidence, protected files,
previous decisions, validation history, and next steps.

**Diagnosis.** Chat context is transient, can be summarized, and is difficult
to audit as project truth. Large handovers also compete with the current task
for attention and can perpetuate outdated interpretations.

**Corrective principle.** Repository-local documents are durable memory. A
handover is a small navigation aid: it identifies the verified state, current
objective, authoritative sources, exact next task, and unresolved decisions.
The next chat must re-verify live repository state.

### 3.12 Phase 4 work outran learning acceptance

**Observed project fact.** The archived state includes a public-data generator
and tests plus an Astro/React/TypeScript/Plotly frontend prototype with a Funnel
Explorer and browser-facing aggregate data. The execution plan still leaves
Phase 4 paused and awaiting separate authorization, and the prototype was not
accepted as the final story-first portfolio experience.

**Diagnosis.** Presentation architecture progressed while Data's personal
learning acceptance of the analytical implementation was unresolved. That
created pressure to preserve downstream interfaces and artifacts before the
upstream learning model was stable.

**Corrective principle.** Presentation follows understanding. Public-data and
frontend work must wait until the analytical concepts they present have both
technical PASS and learning PASS.

### 3.13 Troi-to-Spock prompts showed two opposite failure modes

**Observed project fact.** Prompts often repeated governance, expected state,
protected files, evidence, validations, and STOP language in substantial detail.
The reset review also identified tasks whose scope was broad enough to combine
multiple conceptual changes or large path groups.

**Diagnosis.** Excessive ceremony hides the task's main decision; over-broad
scope hides the causal relationship between one change and its review evidence.
Both make it harder to notice when the work has crossed a learning or safety
boundary.

**Corrective principle.** Future prompts should read like focused issues:
objective, exact scope and files, task-specific constraints, validation, Git
authority if any, and STOP/report. Stable rules should be referenced, and one
analytical idea should be handled at a time.

### 3.14 The destructive-reset draft exposed a concrete safety risk

**Observed project fact.** A recent reset draft used broad directory patterns
such as `analysis/**`, `tests/**`, `learning/**`, and `web/**` before an exact
deletion manifest had been reviewed.

**Diagnosis.** A broad path can contain accepted work, untracked authored work,
or files added after the draft was written. Pattern-level authorization cannot
show exactly which bytes will disappear.

**Corrective principle.** Destructive work requires an exact manifest first,
tracked/untracked classification, a safety checkpoint when useful, Data's
approval of the exact paths, and a deletion task naming those paths. Broad globs
are acceptable only when the complete directory has been explicitly and
knowingly authorized.

### 3.15 The safety correction worked

**Observed project fact.** Before any deletion or rebuild, the complete current
authored state was enumerated, reviewed for secrets and generated material,
committed, and pushed at
`cb863f727d7d6ea5a7fa3e77699097ba2056f1da` with message
`chore: preserve pre-reset Metrocar work`.

**Diagnosis.** The checkpoint separated preservation from later destructive
decisions. It removed urgency from the reset because the prior state became
recoverable and auditable.

**Corrective principle.** Preserve before reset. A checkpoint does not confer
acceptance, but it gives Data a safe basis for exact later decisions.

## 4. What worked and must be preserved

The reset does **not** restart Metrocar from ignorance. It restarts
implementation from verified knowledge.

The following remain valuable and are not invalidated by the learning failure:

- `docs/METRIC_DEFINITION_CONTRACT.md` and its ownership of metric meaning;
- accepted data-quality evidence in `docs/data_quality_report.md`;
- the accepted source cutoff and funnel counts as regression evidence;
- validated Phase 3 findings in `docs/ANALYSIS_INSIGHT_LOG.md`, including their
  distinction between observation, interpretation, recommendation, and
  limitation;
- the evidence that canonical SQL and Pandas reconciled, including identifiers,
  stage membership, attribution, counts, rates, segments, and relevant
  validation totals;
- the accepted User Funnel calibration checkpoints and the analytical lessons
  they demonstrated, even though they did not settle whole-project learning
  acceptance;
- Git history and stable checkpoints, including the pre-reset archival commit;
- `docs/DATACAMP_PYTHON_REFERENCE.md` and
  `docs/DATACAMP_SQL_REFERENCE.md` as the project-local learning vocabulary and
  refresher map;
- Data / Troi / Spock responsibility separation;
- explicit mutation, Git, deployment, and phase authorization gates;
- preservation of unrelated tracked and untracked work;
- credential safety and the rule that analytical processes may consume
  configured credentials without exposing them;
- the discipline of validating grain, join cardinality, subsets,
  monotonicity, segments, and anomalies rather than simplifying away material
  evidence.

These assets form the regression oracle and knowledge base for a simpler
implementation. They should not be rewritten merely because the prior
architecture missed the learning objective.

## 5. Root-cause summary

| Symptom | Root cause | Corrective principle |
|---|---|---|
| Complex analytical code despite a simple-code goal | The existing DataCamp rule remained a default with a production-complexity bypass, so technical architecture repeatedly won local trade-offs over learner comprehension | Require a genuine official DataCamp learning path at any level, Data understanding, and an inspectable combined analytical architecture |
| Technical PASS was treated as learning PASS | Automated evidence was clearer and easier to report than human comprehension | Record two independent gates; require both before acceptance |
| Agent self-report stood in for artifact-level review | Execution and learning review partially collapsed, and Troi's complete top-to-bottom artifact review was missing at some checkpoints | Troi reviews the actual artifact; Data gives final learning acceptance |
| One simple User Funnel path suggested whole-project simplicity | Local simplification was generalized across a larger architecture | Review section, artifact, and end-to-end learner path separately |
| Production and walkthrough code diverged | Teaching was deferred to a translation layer | Make the simplest accepted path canonical; use walkthroughs for narrative, not conceptual substitution |
| DataCamp references lived outside the project | The detailed verified vocabulary was not initially project-local, weakening discovery and consistent review of the existing rule | Keep public-safe verified reference maps in the repository |
| Instruction duplication | Each correction was copied into more layers instead of assigned one owner | One authority per concern; route and reference rather than restate |
| Context overload and reduced salience | Universal, historical, and task-specific material arrived together | Use progressive disclosure and load only what the current task needs |
| `AGENTS.md` became manual-like | Routing, policy, explanation, and procedure accumulated in one startup file | Keep routing and universal guardrails central; move detail to owned documents |
| Execution-plan overload | Current plan, requirements, history, evidence, and changelog shared one file | Separate active status from stable specification and retrospective history |
| Handover overload | Chats were used as durable project memory | Keep truth in Git; make handovers short maps to verified sources |
| Premature Phase 4 work | Downstream presentation progressed before upstream learning acceptance | Presentation cannot outrun accepted analytical understanding |
| Broad prompts | Several concepts or path groups were bundled under one authorization | Scope one reviewable idea and exact files per task |
| Repetitive ceremonial prompts | Stable safeguards were reproduced instead of referenced | Use issue-like prompts containing only task-specific detail |
| Broad deletion patterns | Exact targets had not been enumerated before destructive authorization | Manifest first, checkpoint if useful, approve exact paths, then delete |

## 6. Restart operating model

The following model is intended for the next Metrocar implementation attempt
and is reusable for similar learning-centered analytical projects. It records
the desired restart behavior; it does not itself authorize edits to governance
or implementation.

### 6.1 Durable memory and progressive disclosure

Repository-local, version-controlled documents are durable project memory.
Chat history, agent memory, and handovers are navigation aids.

Use progressive disclosure:

1. start with a short routing document and the current task;
2. read the single authority for each relevant concern;
3. load only the source, tests, evidence, and history required for that task;
4. avoid repeating those sources in the prompt;
5. record any accepted durable result back in its owning repository document
   through a separately authorized change.

This aligns with current official guidance across coding agents. OpenAI's
repository-engineering guidance emphasizes a concise map into structured,
versioned knowledge; its Codex prompting guidance recommends adding only the
context and boundaries that materially help the requested result. GitHub
separates repository-wide, path-specific, and task prompt instructions.
Anthropic separates persistent project instructions from scoped rules and
task-specific procedures. The common operating lesson is to place context at
the narrowest durable scope where it remains authoritative.

### 6.2 One authority per concern

| Concern | Conceptual owner | What belongs there |
|---|---|---|
| Routing and universal execution safety | `AGENTS.md` | Authority map, protected boundaries, universal gates, secrets, Git safety, mandatory STOP behavior |
| Learning and implementation philosophy | `HOW-WE-WORK.md` | Why-before-how, explainability, teaching sequence, simplicity principles |
| Analytical vocabulary and refresher map | `docs/DATACAMP_*_REFERENCE.md` | Verified currently relevant DataCamp learning paths, idioms, and lookup guidance; not an exhaustive catalog or difficulty ceiling |
| Metric meaning | `docs/METRIC_DEFINITION_CONTRACT.md` | Grain, population, stages, filters, attribution, formulas, parameters, validation meaning |
| Validated findings | `docs/ANALYSIS_INSIGHT_LOG.md` | Evidence, status, limitations, reproducibility, interpretations, recommendations |
| Current work and status | Active execution plan | Current phase, authorized task, readiness gate, immediate dependencies |
| Reasons a prior approach changed | Retrospective/history | Observed facts, diagnoses, decisions, retained value, restart lessons |
| Public project entry | `README.md` | Concise public purpose, results, reproducibility path, and navigation |

Stable instructions should appear once in their owning layer. A prompt may say
which authority applies and state the task-specific consequence; it should not
copy the whole authority.

### 6.3 Proportional Troi-to-Spock prompts

Future execution prompts should be issue-like and contain:

- **Objective** — one observable outcome;
- **Scope** — exact files or exact read-only surfaces;
- **Task-specific constraints** — only what is unusual for this task;
- **Validation** — commands and artifact-level evidence required;
- **Git authorization** — explicitly absent or precisely granted;
- **STOP/report** — the checkpoint and information Data/Troi need next.

Repository, branch, expected checkpoint, and preservation constraints remain
appropriate when they materially protect the task. Long histories and full
restatements of stable governance do not.

### 6.4 Analytical complexity gate

Before any analytical mutation, the pre-implementation synthesis should name:

1. the business question and analytical grain;
2. the governing Metric Contract section;
3. the relevant official DataCamp course, chapter, concept, or realistic
   learning path, using the project-local maps as starting references;
4. the intended filters, joins, grouping, Boolean derivations, and summaries;
5. any non-obvious or advanced analytical technique and why it fits the
   question;
6. how the result will be validated against accepted evidence.

Beginner, intermediate, and advanced techniques are all eligible. DataCamp is
the analytical learning boundary, not a maximum difficulty level. A technique
must have a genuine official DataCamp learning path, and Data must be able to
learn why it is needed and explain its input, output, grain, assumptions, and
validation.

Passing the construct-level check is not enough by itself. The composition must
still expose the business question, source tables, filters, joins,
transformations, calculations, assumptions, and evidence limits without
unnecessary indirection. Correctness, validation, privacy, reproducibility,
and tests remain mandatory, but they do not permit an analytical architecture
that bypasses Data's learning and explainability requirement.

### 6.5 Separate acceptance gates

#### Technical PASS

Technical PASS verifies, as applicable:

- correct base population and analytical grain;
- explicit join direction and cardinality;
- contract-faithful stages, filters, windows, segments, attribution, and
  formulas;
- null, unknown, anomaly, subset, monotonicity, and reconciliation behavior;
- credential-free tests and authorized live comparison;
- exact diff scope and regression evidence.

#### Learning PASS

Learning PASS verifies that:

- Data can read the artifact from top to bottom in its intended order;
- WHY appears before HOW for material steps;
- Data can identify the business purpose, source, and grain;
- material techniques have identifiable official DataCamp learning paths;
- Data can approximately reconstruct and explain the analytical approach;
- the canonical implementation and teaching narrative do not require competing
  mental models.

No analytical slice is fully accepted until both pass. A technically correct
slice awaiting Data's learning review remains technically validated but not
implementation-accepted.

### 6.6 Review responsibilities

- **Spock** executes the authorized task, validates it, reports evidence and
  limitations, and stops. The completion report is evidence, not final proof.
- **Troi** reviews the actual diff and the learner-facing artifact in reading
  order before recommending acceptance. Troi checks both the contract and the
  learning model rather than relying on the completion summary.
- **Data** owns final scope, metric approval, learning acceptance, phase
  authorization, destructive authorization, Git transport approval, and
  deployment approval.

No role should infer the next gate from success at the previous one.

### 6.7 One analytical idea at a time

Use this sequence:

`business question → source and grain → simplest Pandas or SQL implementation → Data learning review → technical validation → equivalent second implementation where needed → reconciliation → next concept`

The sequence may pause after any arrow. It should not bundle a second concept
merely because the same file is already open.

Early Data review prevents a technically complete but pedagogically unsuitable
approach from becoming the dependency of later work.

### 6.8 Presentation follows understanding

Public-data schemas, frontend components, charts, annotations, and portfolio
copy should be downstream of accepted analytical understanding. Phase 4 should
not determine the shape of unfinished learning code, and a browser-ready
artifact should not be treated as evidence that the analytical learning gate
passed.

When presentation resumes, each published metric and finding must still trace
to the Metric Contract, canonical reproducible logic, and accepted Insight Log
records. Storytelling may simplify presentation, not business meaning.

The analytical DataCamp-learning requirement does not govern HTML, CSS, Astro,
React, TypeScript, frontend component architecture, responsive design,
browser-side Plotly integration, build tooling, or deployment configuration.
Frontend work may be AI-assisted or vibe-coded. Data may choose to disclose
that assistance publicly, but this retrospective does not prescribe wording.

This separate boundary does not justify unnecessary web architecture. The
frontend should remain conventional for the selected stack, use a small number
of meaningful layers and components, keep data flow direct, and avoid
speculative abstractions or infrastructure. Data's frontend acceptance goal is
high-level orientation: he should know where the page starts, where analytical
data is loaded, which components render the main sections, where styles and
configuration live, and how validated output reaches the browser. Independent
frontend reconstruction is not required.

### 6.9 Destructive-operation protocol

Before any deletion, replacement, or broad reset:

1. perform canonical Git preflight;
2. enumerate the exact candidate files, including untracked files;
3. classify each target as tracked, untracked, ignored/generated, accepted,
   unaccepted, or unrelated;
4. review for secrets and local-only material without opening prohibited secret
   files;
5. create a recoverable checkpoint when preservation is useful;
6. obtain Data's approval for the exact manifest;
7. issue a deletion task that names exact paths;
8. verify the post-operation manifest and Git state;
9. stop before rebuild unless rebuild is separately authorized.

Broad globs are not substitutes for a manifest. They may be used only after the
entire matched directory is deliberately in scope and its contents have been
reviewed.

## 7. Next-chat handover standard

A Metrocar handover should be short enough to verify quickly and should point
to repository-local truth.

Use this format:

```text
METROCAR HANDOVER

Repository:
Branch:
Verified local/tracking/live HEAD:
Working-tree and index state:

Current objective:

Authority documents to read:
- <only the documents relevant to this objective>

Exact next task:

Frozen scope:
- permitted files or read-only surfaces
- protected files and prohibited actions specific to this task

Required validation and STOP boundary:

Unresolved decisions:
- <decision owner and exact question, or "none">
```

Do not copy the entire project history into every new chat. The new chat should
verify current repository-local sources and use the handover as a map. Historical
context should be loaded from Git and the relevant retrospective only when it
affects the current decision.

## 8. Definition of success

Success is not:

> “The agent produced sophisticated correct code.”

Success is:

> “Data understands, can explain, reproduce, and defend the analysis; the
> implementation remains professionally credible, uses genuine DataCamp
> learning paths at whatever level the problem requires, and keeps the
> analytical architecture understandable; validation demonstrates that the
> implementation is correct.”

This definition intentionally keeps professional credibility, learning level,
and validation together. Removing any one of them would repeat the failure in a
different direction.

## 9. Transferable lessons beyond Metrocar

- Repository-local truth beats chat memory.
- Map to authoritative knowledge; do not duplicate it.
- Assign one authority per concern.
- Less prompt can produce better focus when the repository already contains the
  durable context.
- Agent self-report is evidence, not acceptance.
- Technical correctness and human comprehension are separate gates.
- Analytical complexity must have an identifiable DataCamp learning path and
  remain understandable in composition; a difficulty label is not the gate.
- Local simplification does not prove system-level simplicity.
- Teaching should shape the core analytical architecture, not merely explain it
  afterward.
- Presentation cannot outrun understanding.
- Destructive tasks require manifests and exact authorization.
- Preserve recoverable checkpoints before resets.
- When repeated corrections fail, reconsider the architecture instead of adding
  another instruction.
- Governance should reduce ambiguity without becoming the work itself.
- Historical evidence should remain available without loading every historical
  detail into every task.

## 10. Limits and next mandatory stop

This document explains the implementation reset and proposes a restart model.
It does not authorize deletion, refactoring, governance edits, analytical
implementation, database access, Phase 4 work, staging, committing, pushing, or
deployment.

The next action is review by Data and Troi. Any governance restructuring,
deletion manifest, or implementation restart requires a separate explicit
authorization.

## 11. References

### Internal Metrocar sources

- `AGENTS.md` — current execution boundaries, ownership, validation, phase
  gates, secrets, and Git discipline.
- `HOW-WE-WORK.md` — learning philosophy, pre-implementation synthesis, and
  student-explainability expectations.
- `METROCAR_PROJECT_EXECUTION_PLAN.md` — accepted checkpoints, phase status,
  document ownership, calibration history, and Phase 4 gate.
- `docs/METRIC_DEFINITION_CONTRACT.md` — authoritative metric definitions and
  analytical invariants.
- `docs/data_quality_report.md` — accepted data-quality evidence.
- `docs/ANALYSIS_INSIGHT_LOG.md` — validated Phase 3 findings and evidence
  status.
- `docs/DATACAMP_PYTHON_REFERENCE.md` and
  `docs/DATACAMP_SQL_REFERENCE.md` — project-local verified learning vocabulary
  and refresher maps.
- `analysis/funnel.py`, `analysis/reconcile.py`,
  `learning/metrocar_walkthrough.py`, `analysis/public_data.py`,
  `tests/test_public_data.py`, and `web/` — implementation, learning,
  reconciliation, and archived Phase 4A structure inspected at the pre-reset
  checkpoint.
- Git commit `cb863f727d7d6ea5a7fa3e77699097ba2056f1da` — recoverable archival state,
  not acceptance evidence.

### Current official external guidance

- OpenAI, [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — supports a concise repository map, structured versioned knowledge, progressive disclosure, and human steering with mechanical feedback loops.
- OpenAI, [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/) — supports planning before substantial changes, issue-like task descriptions, relevant file context, and bounded reviewable work.
- OpenAI, [Prompting](https://developers.openai.com/codex/prompting/) — supports result-first prompts, only material context and boundaries, explicit verification, approval gates, and human review of important output.
- OpenAI, [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/) — documents repository-scoped instruction discovery and the use of nested instructions for narrower directory concerns.
- GitHub, [About customizing GitHub Copilot responses](https://docs.github.com/en/copilot/concepts/prompting/response-customization) — recommends short, self-contained repository guidance and separates repository-wide, path-specific, and task-specific instruction scopes.
- Anthropic, [How Claude remembers your project](https://code.claude.com/docs/en/memory) — recommends concise, specific, structured project instructions, scoped rules for narrower concerns, and removal of outdated or conflicting guidance.

These sources inform the operational recommendations in this retrospective.
They do not override Metrocar governance, metric definitions, or Data's approval
authority.

# How We Work and Learn — Metrocar

**Status:** Project learning, understanding, and implementation contract

**Purpose:** Keep Metrocar professionally credible, analytically rigorous, and genuinely understandable as a learning project.

This document is the Metrocar-specific learning and implementation methodology for Data and the active Crew defined in `AGENTS.md`.

It does not replace:

- `AGENTS.md`;
- `METROCAR_PROJECT_EXECUTION_PLAN.md`;
- `docs/MASTERSCHOOL_METROCAR_SOURCE_BRIEF.md`;
- `docs/METRIC_DEFINITION_CONTRACT.md`; or
- `docs/ANALYSIS_INSIGHT_LOG.md`.

Those documents have separate roles: authority and safety, current rebuild status and gates, historical curriculum reconstruction, current analytical meaning, and current finding status.

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

What is the simplest coherent professional design that satisfies the authorized outcome and those constraints?

### Validation

How will we prove that the result is correct?

### Stop boundary

Where does the authorized task end?

If a material answer is missing, contradictory, or requires an unsupported assumption, implementation is premature.

STOP and escalate instead of resolving it silently in code.

For analytical work, the question-to-next-question contract in Section 10 is
part of this pre-implementation synthesis.

### Proportional task scope

“Simplest valid approach” means the simplest coherent design that satisfies the authorized outcome. It does not mean the smallest possible task.

Choose task scope using:

1. conceptual cohesion;
2. learning value;
3. reviewability;
4. actual project risk;
5. reversibility;
6. validation needs;
7. coordination and handover cost.

The preferred task is proportionate, conceptually coherent, outcome-complete within its authorized boundary, understandable, reviewable, rational relative to actual project risk, reversible where practical, and large enough to avoid unnecessary handovers and process overhead.

A single Geordi task may include several tightly related analytical steps when they share one business question, analytical grain, mental model, and validation path and are easier for Data to understand and review together.

“One analytical idea at a time” governs reading order, teaching sequence, and visible reasoning inside the main analytical Python document. It does not require one transformation, one function, or one file per Geordi task, and it is not a rule for microscopic implementation slices.

Metrocar is a school and recruiter-facing portfolio project, not a live client production system. Ordinary local mistakes in Python, SQL, tests, the main analytical document, and frontend code are normally recoverable learning signals and do not require enterprise-level ceremony or artificial task fragmentation.

When choices compete, preserve this priority:

```text
business question
→ correct grain
→ understandable DataCamp-learnable analysis
→ validation
→ interpretation
→ evidence-backed judgment
→ recruiter-facing communication
```

This calibration does not weaken strict controls over analytical meaning, grain, Metric Contract definitions, accepted evidence, secrets, destructive operations, Git history, unsupported public claims, required validation, or mandatory STOP conditions.

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
- a `# %% [markdown]` block before meaningful code in the main analytical Python document;
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

### Analytical code calibration

For Metrocar analytical Python and SQL, including the canonical production
implementation, DataCamp is the learning boundary, not a difficulty ceiling:

> **Metrocar analytical code may use DataCamp-learnable techniques at any
> level — beginner, intermediate, or advanced — provided Data can learn,
> understand, explain, and approximately reconstruct the implementation and
> its role in the analysis.**

The difficulty label is not the constraint. A technique is acceptable when it
has a genuine official DataCamp learning path, Data can understand why it is
needed and what enters and leaves the step, and its use keeps the analytical
grain, assumptions, transformations, and validation visible.

The project-local Python and SQL reference maps contain the paths currently
most relevant to Metrocar. They are starting maps, not exhaustive catalogs of
everything DataCamp teaches.

Every newly introduced material analytical technique must have a credible
official DataCamp learning path before it enters implementation. Record its
first-appearance mapping and mapping basis as defined in the DataCamp learning
bridge below.

A technique absent from the project-local maps may still be used when a
credible official Course → Chapter → Concept path can be verified. If no such
path can be identified, the technique is not ready: verify the path, choose an
understandable mapped alternative, or stop for a Data decision.

The DataCamp path teaches the technique. It does not define Metrocar business
meaning; the Metric Contract remains authoritative for that meaning.

Ordinary Pandas tools include:

- filtering and Boolean masks;
- new columns;
- `groupby`, `agg`, `any`, `sum`, `count`, and `nunique`;
- `notna` and `isna`;
- `merge` and ordinary merge validation; and
- simple ratios.

Ordinary SQL tools include:

- `SELECT`, `WHERE`, and `CASE`;
- `GROUP BY` and aggregate functions;
- ordinary joins, including `LEFT JOIN`;
- simple subqueries and CTEs;
- `EXISTS`; and
- window functions when the analytical problem genuinely requires them.

Judge complexity by conceptual load, not by whether one operation is labelled
“advanced.” Prefer one analytical idea at a time, short explicit
transformations, descriptive intermediate variables, and top-to-bottom
readable logic. `validate=` or another ordinary integrity check is not
automatically too advanced when it makes an expected relationship explicit.

A collection of individually DataCamp-learnable techniques can still be
unacceptable when their composition creates unnecessary indirection or makes
the business question, grain, sources, filters, joins, calculations,
assumptions, validation, or evidence limits difficult to follow.

Do not use these as the analytical default:

- class hierarchies;
- generic analytical engines or frameworks;
- deep helper stacks;
- speculative abstractions;
- clever compression or dense one-liners; or
- defensive machinery for hypothetical cases unsupported by verified project evidence.

Correctness, validation, reproducibility, privacy, security, tests, and the
Metric Contract remain mandatory. They are not a separate permission to hide
the analysis behind implementation that Data cannot learn and explain. Meet
those requirements with an understandable analytical design; if the proposed
composition becomes opaque, simplify or reconsider the design rather than
bypassing the learning requirement.

> **Use the DataCamp learning path that fits the analytical problem, then keep
> the Metrocar reasoning visible enough for Data to explain and reconstruct.**

### Web and frontend implementation boundary

The analytical learning rule applies to Python/Pandas analysis, SQL analysis,
statistics, analytical transformations and validation, and analytical tests
whose logic forms part of the analytical mental model.

It does not apply to HTML, CSS, Astro, React, TypeScript, frontend component
architecture, responsive layout, browser-side Plotly integration, package or
build tooling, or deployment configuration. Those technologies do not need a
DataCamp course mapping. Frontend work may be AI-assisted or vibe-coded.

This separation does not authorize unnecessary frontend complexity. The
frontend may exceed Data's coding knowledge, but it should not exceed the
complexity actually required by the portfolio experience. Prefer standard
Astro, HTML, CSS, and TypeScript patterns; a small number of meaningful
components; direct data flow; descriptive names; limited state; minimal
dependencies; and clear separation between the data artifact, page/layout,
components, styles, and configuration.

Avoid elaborate state management, deep component hierarchies, generic design
systems, unnecessary service or repository layers, meta-framework machinery,
and clever TypeScript abstractions unless the portfolio experience genuinely
requires them.

Data's frontend comprehension goal is high-level orientation. Data should be
able to identify where the page starts, where analytical data is loaded, which
component renders each main section, where styles live, which files are
configuration, and how validated analytical output reaches the browser. Data
is not required to reconstruct frontend code independently as he is expected
to do with the analytical implementation.

### The main analytical document is the course

The main cell-based analytical Python document combines two responsibilities:

- the real analytical Python implementation; and
- the primary learner-facing Metrocar course.

Its `# %% [markdown]` learning blocks and the actual code cells that follow form
one top-to-bottom analytical sequence. The code cells must contain the real
analysis used by the project, not a teaching reconstruction of a different
implementation.

For each meaningful analytical concept or question, use this learner-facing
reading spine proportionately:

```text
Topic / Question
→ 🎯 Goal
→ 🧠 Approach and WHY
→ 📚 DataCamp learning pointer
→ Actual analytical code
→ ✅ Result / Observation
→ ✅ Notes for Students
→ ➡️ Next question
```

The learning block should make the purpose, input and output grain or state,
material assumptions, and intended check understandable before the reader has
to decode the code. The result or observation must stay within the available
evidence. Notes for Students should capture only the validation meaning,
important limitation, reusable principle, or common trap needed to understand
and reconstruct the step.

Prefer one analytical idea per ordinary code cell or coherent group of cells.
If a cell becomes long because it contains several analytical ideas, split the
ideas instead of compressing the syntax. Infrastructure or setup code may
legitimately be longer when necessary, but it must not become the model for
analytical teaching code.

Do not move conceptual explanation into excessive inline comments merely to
shorten Markdown, and do not comment obvious syntax. Keep the explanation and
comment discipline consistent with Section 4.

A separate notebook or walkthrough is optional and supplementary. It may be
added later for a concrete presentation, interoperability, or review need, but
it must reuse the real implementation. It must not be required to understand
the analysis, duplicate the analytical logic, redefine metric meaning, or
replace the main analytical Python document as the primary learning path.

### DataCamp learning bridge and Learning PASS

DataCamp is the analytical learning boundary and a refresher reference, not a
difficulty ceiling or analytical authority over Metrocar. The Metric Contract
governs Metrocar meaning. The project-local DataCamp maps are verified starting
references, not an exhaustive catalog.

Before implementation, every newly introduced material analytical technique
must have a credible official DataCamp learning path. Record the mapping in the
slice package at its first appearance in the pre-implementation synthesis, and
add a public-safe refresher when the technique is first taught publicly.

Record each mapping as:

| Technique | First appearance | Course → Chapter → Concept | Why it is needed | Mapping basis |
|---|---|---|---|---|

Use one mapping basis:

- `CONFIRMED_PRIVATE` — confirmed against authorized private study material;
- `CONFIRMED_PUBLIC` — confirmed against current official public DataCamp
  course, chapter, or concept sources;
- `PROJECT_MAP_ONLY` — supported only by a verified public-safe project-local
  reference map; or
- `UNVERIFIED` — not yet supported well enough to satisfy the learning gate.

Chapter may be omitted when a course-level reference is sufficient. An
`UNVERIFIED` technique must be verified or replaced before implementation. Do
not repeat a mapping for later uses of the same technique unless its role
changes materially.

When the technique is first taught publicly, the main analytical Python
document must show one compact public-safe refresher:

```text
📚 DataCamp refresher

Course: <verified official course>
Chapter: <verified official chapter when useful>
Concept: <short description of the technique used here>
```

Use only verified official names and official links. The reference identifies
where to relearn the technique; the Metrocar artifact must provide its own
original application, reasoning, examples, and validation.

For each meaningful analytical slice, assemble one proportionate learning
package, beginning with pre-implementation synthesis and continuing across the
authorized task, the main analytical Python document, validation evidence, and
review report:

- the business question, exact repository checkpoint, reviewed files or
  sections, and slice boundary;
- input and output grain, source and relationship path, assumptions, and
  limitations;
- the intended top-to-bottom reading order, with WHY before HOW;
- the first-appearance technique mappings, why each technique is needed, and
  material common traps;
- semantic validation evidence, including what each material check protects
  and what fixture or candidate evidence cannot establish; and
- the specific reasoning Data must explain during teach-back.

The required order is:

```text
verified DataCamp learning path
→ actual implementation and adjacent learner-facing explanation in the main analytical Python document
→ semantic validation supported by tests, SQL, and reconciliation as applicable
→ Troi reviews the actual artifact in reading order
→ Data explains the reasoning
→ Data grants or withholds Learning PASS for the stated checkpoint and slice
```

Technical PASS and Learning PASS are independent decisions.

Technical PASS records that the applicable grain, joins, stage logic, formulas,
edge cases, tests, and reconciliation checks passed at the stated checkpoint.
It does not prove understanding.

Learning PASS records Data's judgment that he can explain why each material
step exists, its inputs and outputs, grain, assumptions, and validation, and
can approximately reconstruct the analytical approach. Geordi, Spock, and Troi
may provide evidence or recommendations; only Data grants Learning PASS.
Neither PASS may be inferred from the other.

A candidate or fixture-based slice may receive a scope-limited Technical PASS
and Learning PASS before separately authorized full-snapshot reconciliation.
Those decisions apply only to the identified artifact, checkpoint, analytical
slice, and reviewed evidence. They do not by themselves authorize database
access, full-snapshot reconciliation, canonical promotion, downstream
publication, or the next slice. Canonical promotion or publication requires
the separately authorized full-snapshot evidence and every other applicable
acceptance and authorization gate.

If Data cannot explain a material step, Learning PASS is withheld. Identify the
exact gap, return to the mapped concept, simplify or redesign the Metrocar
application, rerun the affected semantic validation, have Troi review the
changed artifact, and repeat Data's teach-back. Do not preserve an opaque
design merely because it already has Technical PASS.

A later material change reopens Learning PASS for the affected slice. Material
changes include changes to grain; source or join path and cardinality; stage
membership; cohort or cutoff rules; attribution; denominators or formulas;
missing, unknown, or unavailable-value treatment; validation meaning; or the
composition of analytical techniques. Pure naming, formatting, or comment
cleanup that preserves meaning and the reviewed mental model does not reopen
the gate.

Authorized private study may be used to understand teaching sequence, idioms,
prerequisites, intermediate steps, and common mistakes. Public Metrocar content
must remain original. Never publish DataCamp exercise solutions or starter
code, full prompts or paid lesson content, transcripts or platform feedback,
account, progress, or XP data, private notes, or private study-repository paths.

Do not create a parallel learning manual, ledger, or score. A self-test may
support teach-back, but it is diagnostic and unscored and cannot grant Learning
PASS.

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

## 10. Question-to-next-question analytical contract

Every meaningful analytical slice begins with a question, not a selected
conclusion.

Apply this contract proportionately to pre-implementation synthesis,
sections of the main analytical Python document, proposed Insight Log records,
interpretation and recommendation review, and recruiter-facing analytical
stories. A technical helper or individual test does not require its own
standalone story.

Use this order:

```text
Audience and decision
→ Context
→ Business question
→ Analytical question
→ Evidence contract
→ Analysis and validation
→ Verified fact
→ Interpretation
→ Alternative explanations or hypotheses
→ Judgment
→ Recommendation or action when justified
→ Limitations and consequences
→ Next question
```

| Component | Minimum required answer or evidence | Claim and ownership boundary |
|---|---|---|
| Audience and decision | Who owns the underlying Metrocar business decision or uncertainty, who will read the artifact, and why the answer matters now | The decision owner determines analytical relevance. The reader determines communication depth and emphasis, not the result |
| Context | Accepted facts, scope, constraints, and prior evidence needed to understand the question | Context may orient the analysis but may not become an assumed conclusion |
| Business question | The decision-relevant question in business language | It requires Data approval when it changes project scope |
| Analytical question | A specific, measurable question whose answer would inform the business question | Question before technique |
| Evidence contract | Source, cohort, grain, metric, segment, cutoff, assumptions, validation, and evidence ceiling | The Metric Contract remains authoritative for analytical meaning |
| Analysis and validation | Reproducible logic and the checks required to trust it | Technical correctness applies only to the stated artifact and evidence state |
| Verified fact | What was directly observed, at which grain and scope, after applicable validation | A fixture fact is not a Metrocar business finding |
| Interpretation | What the verified fact may mean for the analytical and business questions | It must be labeled as interpretation and remain within the evidence |
| Alternative explanations or hypotheses | Material plausible explanations that the current evidence cannot distinguish | A hypothesis is not a finding or causal claim |
| Judgment | What the evidence currently supports, does not support, and why | Data owns final project judgment; Crew members may recommend |
| Recommendation or action | The smallest justified action, experiment, validation, or deliberate non-action | A final business recommendation requires applicable Validated findings and Data approval |
| Limitations and consequences | Unknowns, assumptions, trade-offs, risks, omitted outcomes, and what could change the judgment | Uncertainty remains visible |
| Next question | The smallest material uncertainty opened by the current answer | It must not be used to avoid making the bounded judgment already supported |

The underlying Metrocar decision owner and the artifact reader are not
necessarily the same audience.

A hypothetical business stakeholder determines which question and evidence are
decision-relevant. A recruiter, technical reader, or student determines the
appropriate communication depth, reading order, and progressive disclosure.
Portfolio appeal must not determine the analytical result.

A meaningful analytical slice is closed when it can state:

```text
This is the question we answered.
This is the evidence and grain used.
This is what the evidence supports.
This is the judgment currently justified.
This is what remains unknown.
This is the next question.
```

Closure does not require artificial finality. An open next question does not
excuse failure to make a supported judgment about the current one.

Always distinguish:

- a fact directly supported by validated evidence;
- an interpretation of that fact;
- a hypothesis requiring additional evidence;
- a recommendation combining evidence with context and judgment; and
- an implemented outcome that must later be observed.

No claim is promoted automatically from one category to another.

---

## 11. DIKW evidence ceilings and metric integrity

Use DIKW as an evidence gate, not a decorative label.

The working definitions are:

- **Data** — traceable observations at a known grain.
- **Information** — observations organized and contextualized for a defined
  question.
- **Knowledge** — a validated pattern or transferable mechanism within the
  stated evidence scope.
- **Wisdom** — context-sensitive judgment with explicit assumptions,
  alternatives, consequences, and trade-offs.
- **Action** — a separately authorized intervention, experiment,
  measurement, investigation, or deliberate non-action.

For the empirical path, Knowledge means the strongest supported understanding
permitted by the analytical design. A validated descriptive pattern may be
Knowledge without establishing a causal mechanism.

For the learning path, Knowledge requires Data to explain the mechanism,
distinguish it from a plausible alternative, and transfer the principle to a
different example.

Two related paths operate in Metrocar:

```text
Empirical project path

source records
→ governed information
→ candidate pattern
→ Validated finding
→ context-sensitive judgment
→ authorized action or publication
```

```text
Data's learning path

observed code or result
→ understood transformation
→ reconstructed method
→ transferable analytical principle
→ independent judgment
```

Apply these evidence ceilings:

| Evidence state | May establish | Does not establish |
|---|---|---|
| Fixture-only semantic analysis | That governed logic behaves correctly on the designed fixture | A real Metrocar pattern, causality, or business recommendation |
| Candidate clean-room implementation | A coherent candidate method with scope-limited validation | Canonical promotion, a real Metrocar finding, or publication |
| Authorized full-snapshot result | A reproducible observed pattern eligible for finding review | An automatically Validated interpretation or recommendation |
| Validated Insight Log finding | A validated pattern within its recorded population, cutoff, and limitations | Causality unless the analytical design supports it |
| Interpretation | A plausible evidence-bounded meaning | A new observed fact |
| Hypothesis | A testable possible explanation | An established cause |
| Recommendation | A context-sensitive judgment supported by applicable Validated findings | A guaranteed outcome or authorization to act |
| Recruiter-facing publication | Communication of already accepted evidence and judgment | New analytical authority or stronger evidence |

Technical PASS and Learning PASS remain independent under Section 5,
subsection `DataCamp learning bridge and Learning PASS`.

Technical PASS applies to the technical reliability of the stated artifact and
evidence scope.

Learning PASS applies to Data’s understanding of the stated analytical slice
and reviewed mental model.

Neither PASS may exceed the evidence ceiling of the reviewed artifact, produce
a Metrocar finding by itself, establish causality, or authorize publication or
business action.

### Metric-integrity check

This check operationalizes a Goodhart-style caution: a useful measure can
become misleading when optimization focuses on the measure rather than the
underlying outcome. This is not a reason to reject metrics.

Before a material metric or metric family is first introduced into an
analytical slice, or materially repurposed, and again before it supports a
materially new interpretation, recommendation, or optimization target, ask:

- What underlying user or business outcome is this metric intended to
  represent?
- Is it an outcome, proxy, process measure, or diagnostic indicator?
- What important value or consequence does it omit?
- How could the metric improve while the underlying outcome stays unchanged or
  becomes worse?
- What could deteriorate while the metric improves?
- Which adjacent count, rate, segment, qualitative evidence, or next question
  would expose that distortion?
- Is the metric being used as evidence, a diagnostic signal, or an
  optimization target?
- Which limitation must remain visible in the story?

Answer the check proportionately. Mark a question as not applicable with a
reason instead of inventing a hypothetical failure mode.

For funnel analysis:

- stage counts require their cohort and denominator context;
- Percent of Top requires the exact top-stage count and does not describe the
  adjacent transition;
- Percent of Previous describes the adjacent transition but not total survival
  from entry;
- absolute drop-off requires its corresponding population and rate; and
- relative drop-off requires its corresponding count and denominator.

Read stage counts, cohort, Percent of Top, Percent of Previous, absolute
drop-off, and relative drop-off as connected evidence rather than treating one
measure as the complete funnel story.

A funnel metric may be analytically correct while remaining incomplete
evidence of user value, service quality, satisfaction, retention,
profitability, or long-term business outcomes.

Record the check in the existing pre-implementation synthesis when a metric is
first introduced into a slice or materially repurposed.

Revisit it during interpretation and recommendation review when the metric is
used for a materially stronger claim, an optimization target, or a different
decision.

Use the existing Insight Log, main analytical Python document, and public
limitations fields when the caution is material.

Do not create a separate metric-integrity ledger, redefine the Metric Contract,
or introduce another metric through this check.

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

`METROCAR_PROJECT_EXECUTION_PLAN.md` governs the current rebuild objective, status, active document map, next gate, and STOP boundaries.

`docs/MASTERSCHOOL_METROCAR_SOURCE_BRIEF.md` governs reconstruction of what the original MasterSchool curriculum taught and required. It does not govern current metric meaning or implementation.

`docs/METRIC_DEFINITION_CONTRACT.md` governs analytical meaning.

`docs/ANALYSIS_INSIGHT_LOG.md` governs the status of current findings, interpretations, caveats, and recommendations.

Recruiter-facing visual and product requirements are approved later, after the analytical story exists. An archived visual plan has no current authority.

`HOW-WE-WORK.md` governs the learning and implementation discipline connecting those layers.

No document should silently assume the authority of another.

When a material conflict exists, stop and resolve the conflict before implementation.

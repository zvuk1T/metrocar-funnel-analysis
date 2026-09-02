
# MasterSchool Metrocar Source Brief

## Document Status and Purpose

**Document type:** Historical curriculum source reconstruction  
**Historical subject:** MasterSchool DA107.4 — Metrocar project  
**Current-project role:** Stable source reference, not an implementation plan  
**Public-safety status:** Original synthesis and paraphrase; no private lesson text, screenshots, credentials, account information, or submission data

This document reconstructs the original MasterSchool Metrocar curriculum reviewed manually by Data and Troi. It preserves the assignment’s business problem, learning sequence, analytical expectations, database model, funnel concepts, formulas, teaching patterns, and historical delivery context.

The original MasterSchool project has already been completed and submitted. This brief does not recreate that submission and does not define the current Metrocar implementation.

In particular, this document does not govern:

- current metric definitions;
- current analytical architecture;
- current SQL or Python organization;
- current validated findings;
- frontend technology or page design;
- portfolio publication decisions; or
- future business-question scope.

Those matters belong to the current Metrocar governance and analytical documents. If a later governed definition differs from the historical curriculum, the difference should remain explicit rather than being backported into this brief as if MasterSchool originally taught it.

This document should change only when:

1. an error is found in this reconstruction; or
2. additional original MasterSchool evidence is reviewed and supports a correction or addition.

Ordinary changes to the current codebase, Metric Contract, business questions, findings, frontend, or portfolio story are not reasons to rewrite this historical source.

---

## Source and Scope Rules

The authoritative source for this reconstruction is the page-by-page review performed by Data and Troi using the original MasterSchool pages and supplied screenshots.

The reconstruction records different evidence strengths:

| Label | Meaning in this brief |
|---|---|
| **Explicit requirement** | The reviewed lesson directly required the activity or deliverable. |
| **Suggestion / guidance** | The course proposed an analytical direction without making it the only acceptable choice. |
| **Curriculum / code-complexity signal** | The teaching sequence or example indicates the expected level and style of work but is not a formal acceptance criterion. |
| **Historical submission mechanic** | A requirement of the original school-delivery process, not of the current portfolio rebuild. |
| **Optional / advanced learning** | Material explicitly positioned beyond the baseline Metrocar analytical work. |
| **Reconstruction uncertainty** | The reviewed evidence was insufficient to support a more precise historical claim. |
| **Future-rebuild implication** | A non-authoritative analytical lesson that later planning may consider without attributing it to MasterSchool as an explicit rule. |

The document does not use old Metrocar code or the current Metric Contract as evidence of what MasterSchool originally required. It also does not speculate about lessons that were not reviewed.

Metrocar should be described publicly as an **educational ride-sharing analytical case study**, not as a real internal client engagement.

---

## Curriculum Placement

Metrocar was the final sprint of:

**DA107 — Analytical Thinking**

The visible sequence was:

| Sequence | Curriculum unit | Relationship to Metrocar |
|---:|---|---|
| 1 | DA107.1 — Introduction to Pandas | Established foundational Pandas knowledge. |
| 2 | DA107.2 — Statistics and Visualization | Established descriptive statistics and visualization background. |
| 3 | DA107.3 — Regression and EDA | Exposed students to regression and exploratory analysis. |
| 4 | DA107.4 — Metrocar project final week | Applied prior learning to a ride-sharing funnel case study. |

This placement indicates that Metrocar was an applied capstone following Pandas, statistics, visualization, regression, and EDA exposure.

Prior exposure did not automatically make every earlier topic a Metrocar requirement. Regression, for example, was available in the learning background but was not established as a baseline requirement by the reviewed core Metrocar lessons.

The curriculum and examples signaled student-readable analytical work:

- direct SQL;
- direct Pandas;
- visible intermediate transformations;
- grain-aware joins and aggregation;
- visualization;
- business interpretation; and
- evidence-backed communication.

Code sophistication was not the learning objective.

---

## Original Project Sequence

The visible DA107.4 Core Learning sequence was:

1. Metrocar Project — Part 1
2. Metrocar project — SQL quiz
3. Insights on the Customer Funnel
4. Project Submission Guidelines
5. Quiz 1 — Developing Metrocar Funnel Metrics
6. Quiz 2 — Present the Funnel Results to Stakeholders
7. Project submission form

Metrocar Project — Part 1 contained four reviewed lessons:

1. Project Overview
2. Key Requirements
3. Understanding the Metrocar Database
4. Constructing the Customer Funnel

The separate Advanced Learning area contained:

- Intermediate Regression with statsmodels in Python — DataCamp;
- Customer Analytics and A/B Testing in Python — DataCamp; and
- an additional quiz.

Some lessons displayed inside the Core Learning area were marked “Optional” by the platform. That status appears to describe progression or completion mechanics. It should not automatically be interpreted as evidence that the lesson’s analytical content was unimportant.

Two different classifications therefore matter:

- **Platform status:** required or optional for course progression.
- **Analytical status:** core, supporting, or advanced for understanding Metrocar.

---

## Part 1 — Project Overview

### Business context

Metrocar was presented as a ride-sharing case study with a business model comparable to services such as Uber or Lyft. The platform connects riders with drivers.

The broad analytical workflow was:
```text
understand the business and data
→ explore and query the database
→ construct funnel metrics
→ investigate business questions
→ visualize the evidence
→ communicate conclusions and recommendations
```

The project was framed as a short analytical capstone organized over several days:

| Approximate period | Main activity |
|---|---|
| Early | Explore Metrocar data using SQL and Pandas. |
| Middle | Develop funnel metrics, investigate business questions, and create visualizations. |
| Later | Improve visual communication and present results to stakeholders. |

This is a curriculum and code-complexity signal. The original assignment was not designed as a large software-engineering system.

### Conceptual customer journey

The Project Overview presented seven conceptual business stages:

1. App Download
2. Signup
3. Ride Request
4. Driver Acceptance
5. Ride
6. Payment
7. Review

This sequence describes the conceptual business journey. It is not itself a single grain-controlled analytical table.

The reviewed curriculum later used separate analytical funnels:

| Representation | Stages | Analytical grain |
|---|---|---|
| Conceptual business journey | Download → Signup → Request → Driver Acceptance → Ride → Payment → Review | Business-process description; no single row grain established by the list alone. |
| Core customer funnel | Download → Signup → Requested at least one ride → Completed at least one ride | Course-described user/person funnel, with an important pre-signup download-proxy nuance. |
| Optional ride funnel | Ride Request → Ride Finished → Ride Paid → Ride Reviewed | Ride-level representation. |

These representations should not be silently collapsed into one funnel. Driver acceptance, payment, and review belong to the conceptual journey, but they were not all separate stages in the reviewed core user-level funnel.

---

## Original Business Questions

The business-question families below come from the reviewed MasterSchool curriculum.

The final column records analytical implications identified during reconstruction for use by a future rebuild. Those cautions are not presented as verbatim or explicitly formalized MasterSchool requirements unless the curriculum evidence separately established them.

| Question family | Curriculum status | Intended analytical direction | Future-rebuild evidence implication |
|---|---|---|---|
| Funnel drop-offs and first completed ride | Suggested core direction | Identify transitions that may prevent entrants from reaching a first completed ride. | A large drop-off identifies a pattern requiring investigation; it does not establish its cause. |
| Platform performance and marketing allocation | Suggested core direction | Compare iOS, Android, and Web performance and discuss possible marketing focus. | Platform volume or conversion alone does not prove the optimal marketing allocation. |
| Age groups and target customers | Suggested core direction | Compare age groups across relevant funnel stages and identify groups that may contain target customers. | Descriptive performance does not by itself establish customer value, profitability, or causality. |
| Time of day and possible surge pricing | Suggested core direction | Derive request hour or time period, aggregate demand, visualize peaks and troughs, and discuss implications. | Demand peaks do not prove that surge pricing should be implemented or that it would increase profit. |
| Lowest-conversion transition | Suggested core direction | Identify the weakest adjacent conversion and consider possible improvements. | A future rebuild should distinguish the observed transition result from its interpretation and any proposed action. |
| Student-defined questions | Explicitly encouraged | Replace or extend some suggested questions when the student can justify their business importance. | A new question should be identified as a student-defined extension rather than an original prescribed question. |

A typical time-of-day analysis pattern was:
```text
request timestamp
→ derive hour or time period
→ aggregate demand
→ visualize peaks and troughs
→ discuss business implications
```

The curriculum supported deeper student-defined analysis. Such work is historically consistent when it is clearly identified as an extension and its relevance is justified.

---

## Part 1 — Key Requirements

The Key Requirements lesson was the strongest reviewed source for the original project’s analytical acceptance criteria.

### Analytical and visualization requirements

| Requirement | Classification | Reconstructed expectation |
|---|---|---|
| Funnel visualization | Explicit requirement | Clearly represent the funnel stages. The reviewed Key Requirements evidence did not establish one mandatory chart type or library beyond effective communication. |
| Meaningful insights | Explicit requirement | Move beyond presenting counts and identify patterns relevant to the business questions. |
| Evidence-backed recommendations | Explicit requirement | Recommendations should be reasonable and supported by evidence from the data. |
| Focused drill-down | Explicit requirement | Investigate approximately one or two specific funnel areas in greater depth. |
| Areas of opportunity | Explicit requirement | Connect the deeper analysis to plausible areas such as marketing spend, product development, or another business action. |
| Supporting visuals | Explicit requirement | Visualize the deeper findings rather than relying only on verbal description. |

The curriculum therefore signaled a preference for focused analytical depth rather than a dashboard containing every possible metric.

### Historical analytical toolchain

The reviewed material associated the following tools with the original project:

| Purpose | Historical tools |
|---|---|
| Data access | SQLAlchemy and Pandas |
| Analysis | Pandas |
| Visualization | Matplotlib, Seaborn, and/or Plotly |
| SQL practice | A separate SQL quiz explicitly required SQL queries |

SQL and Pandas both belonged to the original learning design. The reviewed evidence does not establish that every final metric had to be independently implemented in both languages.

### Stakeholder storytelling

The intended audience was non-technical.

The reviewed communication guidance emphasized:

- one clear takeaway per slide;
- limited text density;
- details delivered through the spoken explanation when appropriate;
- avoidance of unnecessary statistical jargon;
- approximately one or two charts per slide; and
- a clear connection between every chart and the stated takeaway.

The visualization guidance emphasized:

- an appropriate chart type;
- a clear title;
- readable axis and tick labels; and
- minimal, purposeful use of color.

The transferable principle was:
```text
deep analysis
→ simple stakeholder communication
```

The reviewed curriculum explicitly required meaningful insights, reasonable evidence-supported recommendations, and clear stakeholder communication.

It did not formalize observed results, interpretation, and recommendations as three named analytical categories. For a future rebuild, keeping those layers visibly separate is a useful implication of the evidence-backed recommendation requirement rather than an explicit historical MasterSchool framework.

---

## Part 1 — Understanding the Metrocar Database

### Database model and analytical grain

The reviewed database contained five core tables.

| Table | Reconstructed grain or source limitation | Analytical role |
|---|---|---|
| `app_downloads` | One row per app download | Top-of-funnel acquisition activity, including a unique download identifier, platform, and download timestamp. |
| `signups` | One row per registered user | Registered-user stage, including a user identifier, a relationship back toward the download/session, signup time, and age grouping. |
| `ride_requests` | One row per ride request or ride | Ride activity, including ride, user, and driver identifiers; request and later ride timestamps; locations; and cancellation-related information. One user can have many ride rows. |
| `transactions` | Exact analytical grain and relationship cardinality were not sufficiently established from the reviewed curriculum page and are not inferred here. | Connects ride activity to payment outcomes, payment status, successful-payment counts, and collected monetary amount. |
| `reviews` | Exact analytical grain and relationship cardinality were not sufficiently established from the reviewed curriculum page and are not inferred here. | Supports analysis of review or rating behavior associated with rides, users, or drivers, including the final conceptual review stage and an optional ride-level funnel. |

A simplified relational model presented by the reviewed material is:
```text
app_downloads
     │
     ▼
signups
     │
     ▼
ride_requests
     ├────────► transactions
     └────────► reviews
```

This diagram records the relational direction relevant to the curriculum. It does not establish exact cardinalities for `transactions` or `reviews`.

The central grain distinction explicitly demonstrated by the course was:
```text
ride-row count ≠ unique-user count
```

A user may request multiple rides. Counting `ride_requests` rows therefore answers a different question from counting distinct users who requested at least one ride.

The reviewed lesson demonstrated:

- `pd.merge()`;
- choosing an appropriate join type;
- choosing the correct join key;
- combining tables with different source grains; and
- preserving downloads without signup through a left-join-style approach.

Together with the ride-row versus unique-user examples, this made the analytical entity being counted central to interpreting a join.

The reviewed curriculum did not establish a formal framework for join-cardinality validation, row-multiplication testing, or base-population preservation checks.

For a future rebuild, the historical examples imply a stronger validation discipline in which material joins document:

- input and output grain;
- relationship and key;
- join type;
- possible row multiplication; and
- whether the intended analytical population remains represented.

That formal checklist is a future-rebuild implication rather than an explicit historical MasterSchool requirement.

### Ten descriptive database questions

The database-understanding lesson guided the student through ten questions:

1. How many app downloads occurred?
2. How many registered users were present?
3. How many ride requests occurred?
4. How many rides were requested versus completed?
5. How does the number of ride requests compare with the number of unique users requesting rides?
6. What was the average ride duration from pickup to drop-off?
7. How many rides were accepted by a driver?
8. How many successful payments occurred, and what total amount was collected?
9. How were ride requests distributed by platform?
10. What was the signup-to-ride-request drop-off?

These questions primarily supported:

- descriptive EDA;
- database understanding;
- grain awareness; and
- SQL and Pandas practice.

They were not, by themselves, the complete stakeholder decision framework.

### Database-to-Pandas workflow

The lesson demonstrated this general workflow:
```text
PostgreSQL database
→ SQLAlchemy engine or connection
→ inspect available tables
→ load queried tables into Pandas
→ filter, merge, derive, group, and aggregate
```

The reviewed examples used APIs such as:

- `pd.read_sql()`;
- `pd.read_sql_table()`;
- Boolean masks;
- `.loc[]`;
- `pd.merge()`;
- `pd.concat()`;
- `.groupby()`;
- `.agg()`;
- `.nunique()`;
- `.mean()`; and
- `.std()`.

The lesson distinguished two operations:

- **Merge:** combine columns using relational keys.
- **Concatenation:** stack compatible row sets.

A left join was demonstrated for the download-to-signup relationship so that downloads without a subsequent signup could remain represented.

The aggregation mental model was:
```text
raw rows
→ group by entity or category
→ aggregate
→ summary table
```

### SQL and Pandas as complementary paths

The same descriptive questions appeared in two learning contexts:
```text
descriptive analytical question
├── SQL solution in the SQL quiz
└── Pandas-oriented solution in the database-understanding lesson
```

The course contrasted the working styles:
```text
SQL
SELECT / JOIN / WHERE / GROUP BY
→ one declarative query
```
```text
Pandas
load
→ filter
→ merge
→ derive
→ group
→ aggregate
```

Method chaining was possible, but it was not the teaching objective. Visible intermediate variables and step-by-step reasoning were more consistent with the lesson.

---

## Part 1 — Constructing the Customer Funnel

### Evidence boundary for the lesson format

The historical lesson URL contained wording that suggested construction “in SQL,” but the rendered lesson demonstrated Python and Pandas. This reconstruction treats the rendered lesson content as the stronger evidence.

### Common analytical basis

The lesson’s core problem was:
```text
different source grains
→ establish a common analytical basis
→ construct stage membership
→ count entities at each stage
→ calculate conversion or drop-off
→ segment the funnel
```

For the core funnel, the questions were:

- How many people downloaded the app?
- How many signed up?
- How many requested at least one ride?
- How many completed at least one ride?

“At least one” is essential. The request and completion stages count people or users who reached the stage, not ride rows.

### Grain validation

Before treating `signups` as one row per registered user, the lesson compared total user identifiers with distinct user identifiers.

The historical course example contained:

- **17,623 registered users**

This number records a course-side example. It is not a substitute for recomputing a current governed result.

### Ride-level to user-level reduction

`ride_requests` begins at ride grain. The lesson derived whether each ride was finished from the presence of a drop-off timestamp and then reduced those ride rows to user-level stage membership.

Conceptually:
```text
ride row
→ finished? yes/no
→ group by user
→ any finished ride?
→ one completion Boolean per user
```

This produced stage flags equivalent to:

- requested at least one ride;
- completed at least one ride.

The historical course-side values were:

- **12,406 unique users requested at least one ride**
- **6,233 unique users completed at least one ride**

These are historical curriculum examples rather than current analytical authority.

### Base analytical table

The lesson recommended a direct base table with explicit stage and segmentation columns.

Conceptually:
```text
one download-derived entrant or person proxy
│
├── downloaded
├── signed_up
├── requested_ride
├── completed_ride
│
├── platform
├── age_group
└── download_date
```

The teaching pattern was:

- one compatible row grain;
- explicit Boolean stage columns;
- segmentation columns beside the stage flags; and
- straightforward aggregation of those flags.

This is a curriculum and code-complexity signal rather than a requirement for one exact current table design.

### Downloads without signups

The course explicitly preserved downloads that never led to signup. Excluding them would remove part of the top-of-funnel population represented in the lesson.

There is an important terminology nuance:

- the course described the funnel as user-level;
- before signup, however, no registered `user_id` exists;
- an unregistered download therefore acts as a person-level or entrant proxy.

This brief preserves that original-course nuance rather than silently replacing it with a later identity model.

Where segmentation information was unavailable for unregistered top-of-funnel entrants, the lesson supported keeping an explicit `Unknown`-style category instead of silently dropping those rows.

### Funnel monotonicity

The lesson stated that funnel counts should decrease as stages progress.

This is preserved as an original curriculum validation signal. It describes the expected nested-stage funnel taught in the lesson and is not a reconstruction of later Metric Contract rules.

### Segmentation

The lesson suggested segmenting the funnel by dimensions such as:

- age group;
- platform; and
- date of download.

Segmentation was therefore part of the original Metrocar analytical direction, not a later portfolio invention.

### Optional ride-level funnel

The course separately suggested a ride-level funnel:
```text
Ride Request
→ Ride Finished
→ Ride Paid
→ Ride Reviewed
```

This was distinct from the core customer funnel:

| Funnel | Grain | Status |
|---|---|---|
| Download → Signup → Requested at least one ride → Completed at least one ride | Course-described person/user level, with a pre-signup download proxy | Core analytical learning |
| Request → Finished → Paid → Reviewed | Ride level | Optional extension |

---

## SQL Quiz — Descriptive Data Understanding

The SQL quiz explicitly required the student to write SQL queries for the same ten descriptive database questions introduced in the Pandas-oriented lesson.

Its primary purposes were:

- SQL practice;
- exploratory data understanding; and
- grain awareness.

The implied SQL concepts included:

- `COUNT`;
- `COUNT(DISTINCT ...)`;
- `SUM`;
- `AVG`;
- `WHERE`;
- null filtering;
- `GROUP BY`;
- ordinary joins;
- timestamp arithmetic; and
- simple ratios.

The central analytical distinction was again:
```text
event or ride rows ≠ distinct users or entities
```

The SQL quiz established SQL as an explicit part of the Metrocar learning design. It did not establish that every final funnel metric had to be implemented twice.

---

## Insights on the Customer Funnel

This lesson shifted the emphasis from data construction to business interpretation.

The presented sequence was:
```text
construct data correctly
→ calculate metrics
→ interpret patterns
→ formulate justified conclusions
→ communicate to stakeholders
```

It reinforced a question-first analytical order:
```text
business question
→ required evidence
→ appropriate summary or visualization
→ analysis
```

Rather than starting with a chosen technique, the lesson directed the student to decide which summaries and visualizations were needed for the business question.

The lesson revisited the original question families and explicitly allowed justified student-defined questions.

### Advanced Plotly ideas

An Advanced Plotly section suggested optional presentation features such as:

- an interactive or dynamic funnel;
- filters for platform, age, or date;
- absolute stage counts;
- switching between Percent of Previous and Percent of Top; and
- displaying a user funnel, a ride funnel, or both.

These were advanced or optional presentation ideas. They were not established as baseline analytical requirements by the reviewed reconstruction.

---

## Quiz 1 — Developing Metrocar Funnel Metrics

Quiz 1 tested:

1. SQL window-function concepts;
2. core user-level stage populations;
3. conversion formulas;
4. Percent of Previous; and
5. Percent of Top.

The specifically relevant SQL concepts were:

- `LAG()`;
- `FIRST_VALUE()`;
- `OVER(...)`; and
- ordered window semantics.

Given an ordered stage-summary table:
```text
stage             users
download          ...
signup            ...
ride_requested    ...
ride_completed    ...
```

the conceptual roles were:
```text
LAG(users)
→ previous-stage denominator
→ Percent of Previous
```
```text
FIRST_VALUE(users)
→ selected first-stage denominator
→ Percent of Top
```

This places window functions inside the original Metrocar learning envelope. It does not imply that every funnel query had to use them. Their demonstrated value was making ordered-stage denominator logic visible.

---

## Funnel Definitions and Formulas

Assume an ordered analytical funnel with stage counts:

- \(N_1\) = selected first stage;
- \(N_2\) = second stage;
- \(N_3\) = third stage.

### Percent of Previous

For downstream stage \(i\):

\[
\text{Percent of Previous}_i
=
\frac{N_i}{N_{i-1}}
\]

Examples:

\[
\text{Stage 2 Percent of Previous}
=
\frac{N_2}{N_1}
\]

\[
\text{Stage 3 Percent of Previous}
=
\frac{N_3}{N_2}
\]

Meaning:

> What share of the immediately preceding stage continued to this stage?

### Percent of Top

For downstream stage \(i\):

\[
\text{Percent of Top}_i
=
\frac{N_i}{N_1}
\]

Examples:

\[
\text{Stage 2 Percent of Top}
=
\frac{N_2}{N_1}
\]

\[
\text{Stage 3 Percent of Top}
=
\frac{N_3}{N_1}
\]

Meaning:

> What share of the selected funnel’s starting population reached this stage?

### “Top” is scope-dependent

“Top” does not always mean app download. It means the first stage of the selected analytical funnel or sub-funnel.

For example:
```text
Signup
→ Ride Requested
→ Ride Completed
```

In this sub-funnel, Signup is the top.

Using the course-side examples:

\[
\frac{12{,}406}{17{,}623}
\approx 70.4\%
\]

This is Signup → Ride Requested conversion.

\[
\frac{6{,}233}{17{,}623}
\approx 35.4\%
\]

This is Signup → Ride Completed as Percent of Top when Signup is the selected top.

\[
\frac{6{,}233}{12{,}406}
\approx 50.2\%
\]

This is Ride Requested → Ride Completed as Percent of Previous.

The course examples demonstrate that the denominator is part of the metric meaning.

For a future rebuild, reporting a percentage together with its starting population is a useful analytical implication of that lesson.

The supplied authoritative reconstruction does not establish a confirmed historical download-stage count. No top-of-funnel download value is inferred from quiz arithmetic, answer options, or the three confirmed downstream examples.

---

## SQL and Pandas Learning Signals

### SQL concepts

The reviewed curriculum supported:

- selection and filtering;
- aggregate functions;
- distinct-entity counting;
- grouping;
- ordinary joins;
- timestamp arithmetic;
- simple ratios;
- null-aware conditions; and
- ordered window functions where they clarify funnel denominators.

### Pandas concepts

The funnel-construction and database lessons used or suggested:

- `count`;
- `sum`;
- `nunique`;
- `agg`;
- `notna`;
- `loc`;
- `groupby`;
- `any`;
- Boolean filtering;
- `iloc`;
- `shift`;
- transposition such as `.T`;
- `copy`;
- new Boolean columns;
- simple user-defined functions; and
- segment-level grouping.

### Learning roles

| Area | Primary curriculum role |
|---|---|
| SQL | Query relational data, answer descriptive questions, practice entity-aware counting, and express ordered denominator logic. |
| Pandas | Load relational data, expose intermediate transformations, merge tables, reduce grains, create stage flags, aggregate funnels, and segment results. |
| Visualization | Communicate funnel structure and deeper findings to a non-technical audience. |
| Interpretation | Turn descriptive evidence into conclusions and possible recommendations relevant to the selected business question. |

### Automated table loading

The course also showed a more automated pattern that loaded several database tables into a dictionary using a loop.

The lesson noted a readability trade-off: later analysis can become harder to follow when tables are referenced indirectly through dictionary keys rather than descriptive DataFrame variables.

This was optional or advanced learning and a code-complexity signal:

> More automation is not automatically better analytical code.

---

## DataCamp Learning Map

These mappings were checked against official public DataCamp course structure during the curriculum reconstruction.

They identify places to learn or refresh techniques. They do not define Metrocar’s business meaning.

Because exact chapter names were not sufficiently established in the source pack, the map uses **Course → relevant concept area** rather than inventing chapter titles.

| Technique area | Course → relevant concept area | Why it relates to Metrocar | Mapping basis |
|---|---|---|---|
| Filtering, adding columns, counting, grouping, indexing, and missing values | **Data Manipulation with pandas** → Boolean filtering, new columns, `.groupby()`, `.agg()`, `.loc[]`, `.iloc[]`, and missing-value handling | Supports stage flags, filtered populations, grouped summaries, and explicit unknown handling. | `CONFIRMED_PUBLIC` |
| Relationships, merges, left joins, concatenation, and integrity concepts | **Joining Data with pandas** → table relationships, one-to-many relationships, merges, left joins, concatenation, and merge-integrity concepts | Supports understanding download-to-signup and user-to-ride relationships. Formal current-project validation remains separate from the historical course reconstruction. | `CONFIRMED_PUBLIC` |
| Loading relational data into Pandas | **Introduction to Importing Data in Python** → working with relational databases in Python | Supports database engines, table inspection, queries, and DataFrame loading. | `CONFIRMED_PUBLIC` |
| Database engines and relational structure | **Introduction to Databases in Python** → engines, connections, relational structure, querying, and selecting database data | Provides a closely related refresher for the database-to-Pandas workflow. | `CONFIRMED_PUBLIC` |
| Small reusable transformations | **Introduction to Functions in Python** → functions, parameters, and return values | Supports simple funnel or rate functions without requiring a framework. | `CONFIRMED_PUBLIC` |
| Ordered denominator logic | **PostgreSQL Summary Stats and Window Functions** → `OVER`, ordering and partitioning, `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, and window frames | Especially relevant to Quiz 1 and ordered stage-summary calculations. | `CONFIRMED_PUBLIC` |
| Previous-row comparison in Pandas | **Manipulating Time Series Data in Python** → `.shift()` | Provides a technique-level association for accessing a preceding row. DataCamp teaches it in a time-series context, not specifically as a funnel method. | `CONFIRMED_PUBLIC` |

---

## Core vs Optional or Advanced Learning

| Core analytical learning | Optional or advanced learning |
|---|---|
| Relational database understanding | Intermediate regression with statsmodels |
| Table and entity grain | Customer analytics and A/B testing |
| Keys, joins, and row-count awareness | Advanced interactive Plotly features |
| Descriptive SQL | Optional ride-level funnel visualization |
| Pandas filtering and merging | Automated dictionary-and-loop table loading |
| Aggregation and distinct-entity counting | Additional advanced quiz material |
| User-level funnel construction |  |
| Boolean stage membership |  |
| Percent of Previous |  |
| Percent of Top |  |
| Segmentation |  |
| Funnel visualization |  |
| Focused drill-down |  |
| Interpretation |  |
| Evidence-backed recommendations |  |
| Stakeholder storytelling |  |

Regression appeared both in the prior DA107 learning background and in optional advanced material. Neither placement establishes regression as a baseline Metrocar analytical requirement.

Likewise, customer analytics, A/B testing, advanced interactive presentation, and the optional ride funnel should not be presented as mandatory parts of the reviewed core assignment.

---

## Historical Submission Mechanics

The original MasterSchool project had school-specific delivery mechanics. The reviewed Key Requirements evidence included approximately:

- a Google Colab notebook or uploaded `.ipynb`;
- visible notebook outputs;
- a recorded presentation;
- a slide deck or PDF;
- a short presentation of approximately three to five minutes; and
- speaker-view presentation.

These are historical submission mechanics. They are not current portfolio requirements.

### Quiz 2 and Tableau

Quiz 2 — Present the Funnel Results to Stakeholders — was historically associated with Tableau or dashboard presentation.

Data and Troi intentionally did not review that lesson in detail because Tableau is not part of the current rebuild and the transferable storytelling expectations had already been captured from Key Requirements and Insights on the Customer Funnel.

No unreviewed Tableau-specific requirement is inferred from this brief.

### Submission guidelines and form

The Project Submission Guidelines and project submission form existed historically but were intentionally not reviewed in detail during this reconstruction.

Data had already completed and submitted the original project. No additional analytical or delivery requirement is inferred from those unreviewed materials.

---

## Code-Complexity Profile

The curriculum signaled a direct and inspectable analytical style.

Its examples and teaching sequence favored:

- direct SQL;
- straightforward Pandas;
- descriptive intermediate variables;
- visible grain changes;
- explicit Boolean stage columns;
- simple aggregation;
- small user-defined functions where useful;
- question-first analysis; and
- clear inspection of entity counts and joins.

The following were not established as original requirements:

- classes;
- generic funnel engines;
- deep helper stacks;
- analytical frameworks;
- dense method chains;
- clever compression; or
- software architecture designed for hypothetical future cases.

The course’s comparison between declarative SQL and stepwise Pandas, together with its warning about automated dictionary loading, indicates that readability and visible reasoning mattered more than abstraction for its own sake.

This is a code-complexity signal, not a prohibition against every abstraction in a future implementation.

---

## Implications for a Future Rebuild

The following implications are non-authoritative planning guidance derived from the historical curriculum:

- Preserve question-first reasoning: business question before technique or chart.
- Keep conceptual journey, user/person funnel, and ride funnel distinct.
- Make entity grain, join direction, cardinality, and denominator choices visible.
- Add formal join-cardinality and row-multiplication validation where current methodology requires it, without attributing that framework to MasterSchool.
- Preserve SQL and Pandas learnability even if later implementation becomes more robust.
- Identify original MasterSchool questions separately from later portfolio extensions.
- Label deeper student-defined questions as extensions and justify their business relevance.
- Keep observed results, interpretation, hypotheses, and recommendations visibly separate while recognizing that MasterSchool did not formalize those as named categories in the reviewed material.
- Retain evidence limits when considering marketing, pricing, targeting, or product actions.
- Do not treat optional advanced tooling as a baseline analytical requirement.
- Prefer readable analytical steps over unnecessary abstraction.
- Keep stakeholder presentation subordinate to analytical evidence.
- When current governed definitions intentionally differ from this historical baseline, document the difference without rewriting the historical source.

This section does not prescribe current files, modules, libraries, frontend architecture, visualization technology, portfolio layout, findings, or recommendations.

---

## Reconstructed Curriculum Map

| Curriculum position | Reviewed purpose | Historical classification | Durable takeaway |
|---|---|---|---|
| DA107.1–DA107.3 | Pandas, statistics, visualization, regression, and EDA background | Prerequisite learning context | Prior exposure does not automatically create a Metrocar requirement. |
| Part 1 — Project Overview | Introduce the business, journey, workflow, and suggested questions | Core | Understand the case before selecting techniques. |
| Part 1 — Key Requirements | Define analytical, visualization, recommendation, and storytelling expectations | Core and strongest reviewed rubric source | Produce a focused funnel analysis with meaningful insights, evidence-backed recommendations, and clear stakeholder communication. |
| Part 1 — Understanding the Metrocar Database | Explore tables and answer descriptive questions through a Pandas-oriented workflow | Core | Learn the schema, distinguish row and entity counts, and understand relational keys and join types before building metrics. |
| Part 1 — Constructing the Customer Funnel | Reduce incompatible grains to a common analytical basis and construct stage membership | Core | Count compatible entities, preserve downloads without signup, and keep grain changes visible. |
| SQL Quiz | Answer the descriptive questions using SQL | Core SQL learning | Distinguish event counts from unique-entity counts and practice relational analysis. |
| Insights on the Customer Funnel | Move from construction to interpretation and communication | Core | Let the business question determine the required summaries and visualizations. |
| Advanced Plotly section | Suggest interactive filters, label modes, and separate funnels | Optional / advanced | Interactivity can deepen presentation but is not the analytical baseline. |
| Quiz 1 — Developing Metrocar Funnel Metrics | Test stage populations, formulas, and ordered SQL window concepts | Core metric learning | The denominator and selected funnel top are part of the metric definition. |
| Quiz 2 — Present the Funnel Results to Stakeholders | Historically associated with Tableau or dashboard presentation | Not reviewed in detail | Do not infer unreviewed Tableau-specific requirements. |
| Project Submission Guidelines and form | Support historical course delivery | Historical submission mechanics; not reviewed in detail | Do not confuse the old submission process with the current portfolio rebuild. |
| Advanced Learning | Regression, customer analytics, A/B testing, and an additional quiz | Optional / advanced | These topics were available beyond the core Metrocar analytical baseline. |

---

## Durable Historical Baseline

The original Metrocar learning problem can be summarized as:
```text
Understand a relational ride-sharing dataset
→ inspect table and entity grain
→ construct a person/user funnel from different source grains
→ calculate Percent of Previous and Percent of Top
→ segment and visualize the funnel
→ investigate one or two meaningful business questions
→ develop evidence-backed insights and recommendations
→ communicate clearly to non-technical stakeholders
```

The durable lesson was not to build the most sophisticated application.

It was to show that the student could move coherently from:
```text
business question
→ data and grain
→ SQL/Pandas analysis
→ evidence and insight
→ recommendation
→ stakeholder communication
```


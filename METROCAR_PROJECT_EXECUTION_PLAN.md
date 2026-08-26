# Metrocar Funnel Analysis — VS Code Agent Execution Plan

> **Plan status:** PHASE 1 SCHEMA RECONCILIATION IN PROGRESS — PHASE 2 BLOCKED
>
> The user has approved the clean-room product direction. Execute only the phase explicitly authorized by the current prompt and Section 12. Stop at its checkpoint; later phases remain blocked until separately approved.

## 1. Purpose of This Document

This file will be the single implementation brief for a VS Code coding agent. When complete, it must contain enough verified context, constraints, acceptance criteria, work phases, and validation steps for the agent to finish the Metrocar rebuild without guessing the user's intent or the verified analytical requirements.

The final agent must:

1. inspect the existing repository before changing anything;
2. preserve useful existing work and avoid overwriting user files unnecessarily;
3. use only verified project requirements and clearly documented user decisions;
4. produce reproducible analysis from the source data;
5. keep credentials and other secrets out of tracked files, notebooks, logs, screenshots, and deliverables;
6. verify calculations, charts, narrative claims, and final artifacts before declaring the project complete;
7. stop and ask the user when a genuinely consequential ambiguity remains.

## 2. Source Register and Authority

### 2.1 Source reviewed

- MasterSchool, **Metrocar Project - Part 1 → 1. Project Overview**
- Source URL: <https://app.masterschool.com/campus/lesson/Metrocar-Project---Part-1-a18b/Project-Overview-0d57>
- Content captured: project objective, logistics, business background, funnel stages, business questions, connection method, and database schema.
- MasterSchool, **Metrocar Project - Part 1 → 2. Key Requirements**
- Source URL: <https://app.masterschool.com/campus/lesson/Metrocar-Project---Part-1-a18b/Key-Requirements-2638>
- Content captured: submission format, required tools, funnel-analysis criteria, recommendation criteria, presentation constraints, and chart-quality criteria.
- MasterSchool, **Metrocar Project - Part 1 → 3. Understanding the database**
- Source URL: <https://app.masterschool.com/campus/lesson/Metrocar-Project---Part-1-a18b/Understanding-the-database-a026>
- Content captured: ten required Pandas questions for database understanding and initial funnel construction, plus reminders to verify table descriptions and join keys.
- MasterSchool, **Metrocar Project - Part 1 → 4. Constructing the customer funnel in SQL**
- Source URL: <https://app.masterschool.com/campus/lesson/Metrocar-Project---Part-1-a18b/Constructing-the-customer-funnel-in-SQL-fc18>
- Content captured: common-granularity rule, decreasing-count invariant, Python/Pandas funnel construction, drop-off calculation, Percent of Top, Percent of Previous, and suggested Pandas operations.
- MasterSchool, **Metrocar project - SQL quiz → Explore the Metrocar Data with SQL**
- Source form: 12 user-provided screenshots covering the quiz introduction and questions 1–10; one question screenshot was duplicated.
- Content captured: each of the ten database-understanding questions requires an SQL query, the minimum passing grade is 60, attempts are unlimited for the sprint, and multiple-choice candidate values are shown.
- MasterSchool, **Constructing the Customer Funnel → Tips & Tricks code examples**
- Source form: 9 user-provided screenshots plus the representative Pandas expression `base_table.groupby("platform")[[...]].sum().T`.
- Content captured: user-level grain checks; at-least-one requested/completed ride logic; one Boolean base table per compatible grain; inclusion of unregistered downloads; `Unknown` category handling; simple funnel/rate functions; platform, age, and download-date segmentation; Percent of Previous/Top; and the separate request → finished → paid → reviewed rides funnel.
- MasterSchool Notion, **Insights on the Customer Funnel**
- Source URL: <https://masterschool.notion.site/Insights-on-the-Customer-Funnel-28eadd0472c94fac9951d53f7f33e915>
- Content captured: conclusion-focused sprint goal, suggested and custom business-question policy, analysis-first visualization planning, and advanced interactive-dashboard requirements for filters, label modes, and separate user/ride funnels.
- MasterSchool Notion, **Project submission guidelines**
- Source URL: <https://masterschool.notion.site/Project-submission-guidelines-f87e9abceb8d49fabf355a81f55cd221>
- Content captured: required static Plotly funnel image; notebook purpose and documentation expectations; video format, hosting flexibility, screen-share and camera requirements; concise non-technical storytelling guidance; optional Plotly/Dash dashboard status; recommended presentation structure; and the historical deadline shown on the page.

### 2.2 Remaining planning inputs

- Further user-specified product, design, and portfolio preferences
- Final technology, hosting, repository-structure, and Data Gym Brain integration decisions

The MasterSchool submission form is explicitly **out of scope**. The original project was submitted approximately two years ago, and this work is an independent portfolio rebuild rather than a resubmission.

### 2.3 Conflict-resolution rule

Apply instructions in this order:

1. the user's explicit decisions and additions;
2. the approved acceptance criteria for the current portfolio rebuild;
3. MasterSchool's analytical and business requirements used as source material;
4. this execution plan;
5. the agent's implementation judgment.

Historical MasterSchool submission logistics and deadlines do not define the current deliverables.

If two higher-authority instructions conflict, document the conflict and ask the user before implementation.

## 3. Confirmed Project Brief

### 3.1 Project title

**Project Overview: Funnel Analysis Mastery Project**

Working project name: **Metrocar Funnel Analysis**.

### 3.2 Business context

Metrocar is a ride-sharing platform, comparable to Uber or Lyft. It connects riders with drivers through a mobile application and acts as the intermediary that facilitates ride requests and ride completion.

### 3.3 Objective

Analyze Metrocar's customer funnel to identify meaningful drop-off points and opportunities for improvement. Use evidence from the data to present insights and actionable recommendations to stakeholders.

Confirmed methods from the original brief:

- use SQL to collect and query data;
- use Pandas for further analysis;
- create meaningful data visualizations;
- explain every recommendation using insights derived from the data;
- communicate the analysis and recommendations clearly to stakeholders.

Do not invent metrics or recommendations. Every material conclusion must be traceable to a reproducible query or analysis step.

The current objective is to rebuild the project as a modern, recruiter-facing interactive web application and to evaluate how well the selected z.ai coding agent can execute an unambiguous specification.

### 3.4 Current requirements and historical delivery context

The MasterSchool pages remain authoritative for the business problem, data-analysis expectations, funnel logic, and storytelling principles. Their submission mechanics are historical reference only.

#### 3.4.1 Historical MasterSchool submission package — do not execute

The original assignment requested a Colab or Jupyter notebook, a Plotly funnel image, presentation materials, and a short recorded presentation submitted through a form. The source also displayed the old deadline `EOD Sunday (04/08)`.

The implementing agent must **not** open or complete a MasterSchool submission form, target that historical deadline, or create a video, slide deck, PDF, or Colab submission merely to satisfy the old rubric. Those artifacts may be added later only if the user explicitly requests them for portfolio purposes.

#### 3.4.2 Current analysis and visualization requirements

- Retrieve and validate data reproducibly with **SQLAlchemy 2.x, psycopg 3, raw SQL, and Pandas**.
- Use SQLAlchemy's synchronous engine/connection layer with the `psycopg` PostgreSQL driver; do not build ORM models.
- Perform the analytical transformations with **Pandas** or an equally auditable Python step where justified.
- Use **Plotly as a mandatory visualization technology** for the primary funnel and the interactive recruiter experience.
- Render interactive figures in the web frontend with **Plotly.js or the selected framework's Plotly binding**.
- Do **not** build the new application with Dash and do not require a Dash/Python web server for public interaction.
- Matplotlib and Seaborn may be used for supporting analysis where they are the clearest choice, but they do not replace the Plotly implementation.
- Keep every published metric traceable to the validated SQL/Pandas pipeline. Canonical repeatable analysis lives in readable `.py` files; a notebook is optional as an explanatory portfolio artifact and must not become a second conflicting source of metric logic.

#### 3.4.3 Funnel-analysis criteria

- Create funnel visualizations that adequately represent the different analysis stages.
- Produce meaningful insights from the funnel analysis.
- Make reasonable recommendations that are explicitly supported by evidence extracted from the data.
- Select **one or two specific funnel sections** for a deeper analysis.
- Identify concrete opportunity areas within those sections, such as increasing or reducing marketing spend or prioritizing product-feature development.
- Visualize the evidence supporting the selected deep dives.

#### 3.4.4 Data-storytelling criteria for the website

- Design the primary experience for a **non-technical stakeholder or recruiter audience**.
- Avoid unnecessary implementation detail and overly technical statistical language in the main narrative.
- Address every required business question with the finding, the analyst's clearly stated reasoning, and an evidence-backed recommendation.
- Highlight material data irregularities, limitations, and caveats that affect interpretation.
- Assumptions about facts not specified in the brief are allowed only when they are identified clearly as assumptions.
- Give every page section or insight card a clear takeaway.
- Keep visible copy concise and move methodology or nuance into progressive disclosure where appropriate.
- Ensure every chart directly supports its surrounding takeaway.
- Choose chart types appropriate for the data and intended message.
- Give charts clear titles, axis labels, and tick labels.
- Use color minimally, consistently, and intentionally.

Use the original recommended presentation sequence as a website storytelling pattern:

1. **Context** — briefly identify the included funnel steps;
2. **Key Results** — for each business question, state the question, finding, and recommendation concisely;
3. **Conclusion** — reiterate one or two highest-priority takeaways or recommendations.

#### 3.4.5 Current portfolio-rebuild acceptance checklist

Before handoff, the implementing agent must verify and report `PASS` or `FAIL` for each applicable item:

- no MasterSchool submission-form, deadline, recording, or slide-deck work was performed unless separately requested by the user;
- SQLAlchemy and Pandas used to obtain data;
- psycopg 3 is used as the synchronous PostgreSQL driver beneath the SQLAlchemy 2.x engine, without SQLAlchemy ORM models or asynchronous database code;
- Pandas used for analysis;
- primary funnel and recruiter-facing interactive charts are implemented with Plotly/Plotly.js;
- the deployed application has no Dash runtime dependency;
- the public application reads only validated, precomputed, non-sensitive analytical data and makes no live database connection;
- the frontend is implemented with Astro, React interactive islands, TypeScript, and Plotly.js;
- Python and frontend code remain proportionate to a student project: direct transformations, small focused functions/components, and no unnecessary frameworks or abstraction layers;
- every transformation and analysis step is reproducible and documented in code, a notebook, or both;
- both confirmed funnel grains are represented accurately and clearly;
- the user funnel implements Downloaded → Signed Up → Requested at Least One Ride → Completed at Least One Ride at a compatible person/download grain;
- the rides funnel implements Requested → Finished → Paid → Reviewed at ride grain;
- platform, age-range, and date-range controls behave according to documented metric rules;
- the user can compare two platforms or two age groups side by side without changing metric definitions or counting grain; date remains a filter;
- absolute counts and Percent of Top/Percent of Previous modes reconcile to the canonical stage table;
- insights and recommendations are evidence-backed;
- one or two funnel sections receive a meaningful visual deep dive;
- the single-page web experience is understandable to recruiters, the project author, and students encountering the analysis for the first time;
- every required business question is answered with a finding, reasoning, and recommendation;
- material data irregularities, assumptions, limitations, and caveats are stated clearly;
- all charts use appropriate forms, titles, labels, ticks, accessible interaction, and restrained color;
- the public site and repository expose no database credentials or other secrets;
- a recruiter can reach the deployed experience directly from the repository without local setup;
- analysis, SQL, generated public data, frontend, tests, and documentation are organized coherently in one repository;
- one documented command reruns the approved analysis, validates results, and regenerates the browser-safe data consumed by the web application;
- the canonical analytical pipeline is implemented in readable `.py` files and runs inside a standard `venv` defined by `requirements.txt`;
- the project documents how to add a new business question, its SQL/Pandas analysis, validation, Plotly view, insight narrative, and recommendation without restructuring the application;
- all public-facing product copy is written in clear English;
- the interface follows a serious, elegant business-dashboard direction rather than a playful or purely decorative style;
- the visual system uses the confirmed light foundation, dark-navy typography, and restrained blue-green accents;
- the single page follows the confirmed section order and uses tabs for the two funnel views;
- important metrics provide an expandable `How was this calculated?` explanation and a path to the full production SQL in the repository;
- exploratory and practice SQL remain repository-only and cannot be loaded by the production refresh command or linked as authoritative methodology;
- code explanations are proportional to difficulty and allow a student to follow the business question, transformation, and validation without comments that merely restate obvious syntax;
- the repository provides a short student-oriented reading order for the analysis, production SQL, generated outputs, and frontend;
- the production site is deployed on Render and its deployment configuration is reproducible from the repository;
- automated checks and a documented manual QA pass succeed for the analysis and web application.

## 4. Confirmed Metrocar Funnel

Use the following business sequence as the initial funnel definition:

1. **App Download** — a user downloads the Metrocar app from the App Store or Google Play Store.
2. **Signup** — the user creates an account and supplies the required account and payment information.
3. **Request Ride** — the user requests a ride with pickup, destination, and capacity information.
4. **Driver Acceptance** — a nearby driver accepts the ride request.
5. **Ride** — the driver picks up the user and completes the trip to the destination.
6. **Payment** — the user is charged after the ride.
7. **Review** — the user can rate the driver and leave a written review.

The conceptual sequence above describes the business lifecycle. Do not force all seven concepts into one mixed-grain chart. The confirmed implementation uses the two compatible funnels in Section 4.2, while exact source-column qualification for paid and reviewed rides remains subject to schema validation.

### 4.1 Confirmed funnel-construction rules

#### 4.1.1 Establish one compatible counting basis

- Explore the detail available at every stage before calculating funnel conversion.
- Select and document a common entity/grain that can be represented consistently across all stages in the same funnel.
- Do not combine event counts, ride counts, sessions, downloads, and unique users in one decreasing sequence unless they have first been transformed into a genuinely compatible basis.
- If the business questions require a ride-level subfunnel, model it as a separate compatible funnel rather than mixing ride-level and user-level values in one sequence.
- Record the chosen grain, qualifying condition, source, join path, and deduplication rule for every stage in the metric dictionary.

The supplied `User-Level Granularity` screenshots confirm the intended pattern:

- validate one-row-per-user tables with `count` versus `nunique` checks;
- recognize that ride requests contain repeated `user_id` values because one user can request multiple rides;
- reduce ride activity to one Boolean outcome per user with a clear `groupby("user_id")` aggregation such as `any()`;
- count a user as having requested or completed a ride when that user has done so at least once;
- preserve downloads that never became registered users rather than losing the first funnel stage.

Recompute all counts against the approved database. Numeric outputs visible in the screenshots are examples and must not be hard-coded as expected production results.

#### 4.1.2 Build one canonical funnel-stage table

Combine the stage-level results in a single ordered Pandas table. At minimum, include:

- `stage_order`;
- `stage_key`;
- `stage_label`;
- `stage_count`;
- `previous_stage_count`;
- `dropoff_count`;
- `percent_of_top`;
- `percent_of_previous`;
- `dropoff_percent`;
- counting grain and qualifying-rule reference;
- validation status and notes.

Keep full-precision numeric values in the analytical table and apply display rounding only in Plotly views, optional exported artifacts, and the website. Use this canonical output for methodology artifacts, the recruiter-facing web application, and automated QA.

#### 4.1.3 Required formulas

For ordered stage count `C_i`, first-stage count `C_0`, and previous-stage count `C_(i-1)`:

- `percent_of_top_i = C_i / C_0 × 100`
- `percent_of_previous_i = C_i / C_(i-1) × 100` for stages after the first
- `dropoff_count_i = C_(i-1) - C_i` for stages after the first
- `dropoff_percent_i = (C_(i-1) - C_i) / C_(i-1) × 100` for stages after the first

For the top stage, set `percent_of_top` to `100`. Represent previous-stage metrics as not applicable, or as `100` only when a presentation convention requires it and that convention is explicitly documented. Handle zero denominators explicitly; never hide an undefined rate by coercing it silently to zero.

Interpretation:

- **Percent of Top** shows the share of initial funnel entrants who reached each stage.
- **Percent of Previous** shows progression from the immediately preceding stage.
- **Drop-off Percent** is the complement of Percent of Previous for valid nonzero denominators.

#### 4.1.4 Funnel invariants and failure handling

- The source expects counts to decrease strictly through the funnel and never increase.
- Enforce `C_i <= C_(i-1)` as a hard automated invariant.
- Treat equality as a warning that requires inspection and explanation because the source expects a strict decrease.
- Treat any increase as a failed validation, usually indicating an incompatible grain, incorrect qualification rule, duplicate-producing join, or stage-order error.
- Do not force monotonicity by deleting or altering valid observations. Fix the definition or model separate compatible funnels when the business process genuinely uses different grains.
- Confirm that all calculated rates stay within valid bounds and reconcile stage counts to the baseline metrics in Section 6.4.

#### 4.1.5 SQL/Pandas interpretation

The lesson route/title refers to constructing the funnel in SQL, while its body explicitly requests Python code, Pandas calculations, and Pandas operations such as `count()`, `sum()`, `.iloc[]`, and `.shift()`. The Key Requirements page also specifies SQLAlchemy/Pandas data retrieval and Pandas analysis.

Therefore, the clean-room implementation must:

- use SQL or SQLAlchemy queries for secure, auditable data access and appropriate database-side extraction;
- use Pandas to combine validated stage results and calculate the canonical funnel table;
- use direct SQL aggregations as independent validation where useful;
- not treat the page title alone as a requirement to implement the entire funnel exclusively in SQL;
- prefer clear, tested vectorized logic; the listed Pandas functions are useful references rather than mandatory syntax when an equivalent implementation is clearer.

#### 4.1.6 Required simplicity level

This is a strong student project, not an enterprise data platform. Prefer transparent Pandas transformations that a student can read from top to bottom.

Use the official examples as the complexity benchmark:

- Boolean stage columns;
- `notna()`, `groupby()`, `agg()`, `any()`, `sum()`, Boolean masks, and `.T` where they express the intent directly;
- a small function that receives a copied base DataFrame and returns funnel counts;
- a small function that receives ordered counts and returns Percent of Top/Previous and drop-off metrics;
- one clearly constructed base table per compatible grain.

A representative segmented aggregation may remain as direct as:

```python
funnel = base_table.groupby("platform")[stage_columns].sum().T
```

Do not introduce a custom pipeline framework, generic query builder, class hierarchy, plugin system, dependency-injection layer, or design pattern merely to appear sophisticated. Add an abstraction only when it removes demonstrated repetition or protects a verified invariant. Prefer named intermediate variables, short functions, ordinary data structures, readable SQL, and focused tests over clever compression.

### 4.2 Confirmed dual-funnel interactive scope

The Insights page defines two distinct funnel views. They must not share incompatible counting grains:

#### 4.2.1 User funnel

- Uses a compatible person/download-level entity throughout and contains four ordered stages: **Downloaded App → Signed Up → Requested at Least One Ride → Completed at Least One Ride**.
- Build one base table with one row per compatible funnel entity and one Boolean column per stage.
- Preserve downloads without a matching signup. Under the course assumption, each unregistered download may be treated as one person for this funnel.
- For registered users, reduce repeated ride rows to per-user Booleans; `any()` is the intended simple aggregation pattern for at-least-one requested or completed ride.
- Validate the exact completion condition against the live schema; the supplied example derives `is_finished` from a non-null `dropoff_ts`.
- Include `platform`, derived `age_group`, and download date in the base table for filtering and segmentation.
- Fill missing categorical attributes created by non-registration with an explicit display category such as `Unknown`; never silently drop those first-stage entities.
- Shows absolute stage counts and conversion context.

#### 4.2.2 Rides funnel

- Begins with ride requests.
- Uses ride-level granularity throughout.
- Uses the confirmed ordered sequence **Ride Requested → Ride Finished → Ride Paid → Ride Reviewed**.
- Build a separate ride-grain base table and aggregation rather than reusing incompatible user counts.
- Finalize and validate the exact qualifying source columns, timestamp/null rules, deduplication, and transaction/review handling before publishing results.

#### 4.2.3 Required interactive behavior

The final interactive experience must allow stakeholders, recruiters, or students to:

- switch between the user funnel and rides funnel with clearly labeled tabs in one shared visualization area;
- filter supported views by platform;
- filter supported views by age range;
- filter by date range using an explicitly documented date/cohort rule;
- compare two platforms or two age groups side by side; date remains a filter rather than a comparison dimension in the first version;
- see the absolute count at every stage;
- switch percentage labels between Percent of Previous and Percent of Top;
- understand which filters are unavailable or not meaningful for a stage instead of receiving a misleading result;
- reset filters and return to the validated default view;
- receive a clear empty/error state when a filter combination has no valid observations.

The official page presents these as advanced Plotly tasks. Because the user has independently confirmed a public interactive website as a portfolio goal, the capabilities above are minimum product behavior for the modern site. **Plotly is mandatory**: the selected frontend must render the interactive analytical views with Plotly.js directly or through a compatible framework binding.

Every filtered result must be calculated from the same validated metric definitions as the unfiltered funnel. Filter logic must be tested for non-inflating joins, stable grain, valid denominators, and correct stage order.

## 5. Confirmed Business Questions

Use the following as the clean-room starting question set. The final approved scope must answer them unless the user explicitly approves replacing selected questions under Section 5.1, as permitted by MasterSchool:

1. Which funnel steps should Metrocar research and improve?
2. Are specific drop-off points preventing users from completing their first ride?
3. How does funnel performance differ across `ios`, `android`, and `web`?
4. Based on platform performance, where should Metrocar focus its marketing budget for the upcoming year?
5. Which age groups perform best at each funnel stage?
6. Which age group or groups most likely contain Metrocar's target customers?
7. How are ride requests distributed throughout the day, and what does that imply for a potential surge-pricing strategy?
8. Which part of the funnel has the lowest conversion rate?
9. What evidence-backed action could improve the lowest-converting part of the funnel?

The final analysis must distinguish observed facts from interpretations and recommendations.

### 5.1 Custom business-question policy

MasterSchool explicitly permits and encourages replacing some suggested questions with original business questions. Any custom question must:

- arise from a defensible business or product decision;
- be answerable with the available data or clearly labeled as requiring additional data;
- be stated precisely before its metric or visualization is designed;
- explain why it is more valuable than the suggested question it replaces;
- identify the intended stakeholder and decision;
- be emphasized and justified in the methodology documentation and website insight narrative;
- receive user approval before it changes the agreed analysis scope.

After exploratory data analysis, the agent should propose a small set of candidate original questions with rationale, required fields, method, expected visualization, and decision value. Do not select questions merely because they produce visually interesting charts.

The Insights page recommends beginning with the summaries and visualizations required to answer stakeholder questions, reflecting a real workplace setting in which stakeholders provide questions but not analytical instructions. Therefore, every planned chart must trace back to an approved business question or decision.

## 6. Confirmed Data Source and Schema

The project uses a generated Metrocar dataset inspired by publicly available Uber/Lyft data.

### 6.1 Credential handling

The MasterSchool page provides a PostgreSQL connection URL for SQLAlchemy and Pandas. Treat it as a secret.

- Load it at runtime from the environment variable `METROCAR_DATABASE_URL`.
- Never paste the real URL into this Markdown file, source code, notebooks, Git history, terminal transcripts, charts, presentation slides, or exported reports.
- Provide a safe `.env.example` containing only `METROCAR_DATABASE_URL=` if the repository needs environment setup documentation.
- Ensure `.env` is ignored by Git before using it.
- Redact credentials from errors and connection diagnostics.

#### 6.1.1 Confirmed Python/PostgreSQL connection stack

Use **SQLAlchemy 2.x with psycopg 3** in synchronous mode:

- install the driver as `psycopg[binary]` in `requirements.txt` for the simplest cross-platform student setup;
- create a SQLAlchemy engine using the `postgresql+psycopg` dialect and the secret loaded from `METROCAR_DATABASE_URL`; if the historical URL uses the generic `postgresql://` scheme, normalize only that scheme in memory without printing or rewriting the credential;
- execute readable parameterized SQL and load approved results into Pandas;
- use SQLAlchemy only for the engine, connections, transactions, parameter binding, and Pandas compatibility;
- do not define ORM models, add an asynchronous driver, or introduce a connection-pool package beyond what this small batch analysis requires;
- keep production SQL in versioned `.sql` files where practical so it remains easy to study and test.

`psycopg` is the package name for psycopg 3. Do not install a nonexistent `psycopg3` package, and do not start new code with legacy `psycopg2` unless a verified compatibility constraint requires it.

### 6.2 Tables

The names below were reconciled with the live PostgreSQL schema on 2026-08-26. The verified live schema is authoritative where the earlier instructional description differed.

#### `app_downloads`

- `app_download_key` — unique identifier for an app download
- `platform` — `ios`, `android`, or `web`
- `download_ts` — download timestamp

#### `signups`

- `user_id` — primary identifier for a user
- `session_id` — app-download/session identifier
- `signup_ts` — signup timestamp
- `age_range` — user's age-range segment

#### `ride_requests`

- `ride_id` — primary identifier for a ride
- `user_id` — foreign key to the requesting user
- `driver_id` — foreign key to the driver
- `request_ts` — ride-request timestamp
- `accept_ts` — driver-acceptance timestamp
- `pickup_location` — pickup coordinates
- `dropoff_location` — destination/drop-off coordinates
- `pickup_ts` — pickup timestamp
- `dropoff_ts` — drop-off timestamp
- `cancel_ts` — cancellation timestamp; acceptance, pickup, and drop-off timestamps can be null

#### `transactions`

- `transaction_id` — non-null candidate primary identifier; uniqueness must be confirmed by the live Phase 1 test
- `ride_id` — foreign key to a ride
- `purchase_amount_usd` — purchase amount in USD
- `charge_status` — exact live values `Approved` or `Decline`
- `transaction_ts` — transaction timestamp

#### `reviews`

- `review_id` — primary identifier for a review
- `ride_id` — foreign key to a ride
- `driver_id` — foreign key to a driver
- `user_id` — foreign key to the requesting user
- `rating` — rating from 0 to 5
- `review` — review text supplied by the user

All inspected timestamp columns use PostgreSQL `timestamp without time zone`. Their timezone is therefore unknown; treat them as source-local values and do not apply an invented timezone conversion. Phase 1 also found 24,727 rides with both `accept_ts` and `cancel_ts`, but none with both cancellation and pickup or drop-off. Treat this as a valid cancel-after-accept outcome, not a separate funnel stage; its analytical treatment belongs in the Phase 2 metric contract.

### 6.3 Provisional relationships to validate

The column descriptions imply these joins, but the implementing agent must validate uniqueness, cardinality, null behavior, and referential coverage before relying on them:

- `app_downloads.app_download_key` → `signups.session_id`
- `signups.user_id` → `ride_requests.user_id`
- `ride_requests.ride_id` → `transactions.ride_id`
- `ride_requests.ride_id` → `reviews.ride_id`

The agent must test for duplicates and one-to-many relationships before joining. It must not use a many-to-many join that silently inflates funnel counts or revenue.

### 6.4 Confirmed database-understanding questions

The project uses these questions to guide the initial Pandas work and begin constructing the customer funnel. The final implementation must answer every question reproducibly:

1. How many times was the app downloaded?
2. How many users signed up in the app?
3. How many rides were requested through the app?
4. How many requested rides were completed?
5. How many ride requests were made, and how many unique users requested a ride?
6. What was the average ride duration from pickup to drop-off?
7. How many rides were accepted by a driver?
8. For how many rides was payment collected successfully, and what total amount was collected?
9. How many ride requests occurred on each platform?
10. What was the drop-off from users signing up to users requesting a ride?

#### 6.4.1 Implementation requirements

- Use the table and column descriptions in Section 6.2 to plan joins, then validate the actual keys and cardinalities as required by Section 6.3.
- Obtain data with the confirmed SQLAlchemy/Pandas workflow and perform the requested analysis in Pandas.
- Provide an auditable SQL query for each of the ten quiz questions. Queries may share tested CTEs or views, but every final answer must be traceable to a clearly identified SQL result.
- Independently reconcile important SQL results with Pandas calculations so the repository demonstrates both database querying and analytical validation.
- Give every result a clearly named metric, explicit unit, denominator where relevant, and reproducible calculation path.
- Keep event counts and distinct-entity counts separate. In particular, do not confuse ride-request rows with unique requesting users.
- Define the qualifying rules for `completed ride`, `accepted ride`, and `successful payment` in the metric dictionary before calculating them.
- Do not infer those qualifying rules silently from column names; confirm them against later instructions and validate them against actual null/status patterns.
- State the time unit used for average ride duration and exclude or separately report invalid or incomplete timestamp pairs.
- Validate platform attribution through the download → signup → ride-request join and prove that the join does not multiply ride requests.
- For the signup-to-request drop-off, state the counting grain, numerator, denominator, conversion formula, and drop-off formula explicitly.
- Cross-check critical totals with an independent aggregation where practical.

#### 6.4.2 Required baseline output

Create one auditable baseline-metrics table containing at least:

- metric identifier;
- human-readable metric name;
- value;
- unit;
- source table or tables;
- counting grain;
- qualifying condition;
- distinct/deduplication rule;
- validation status;
- notes or limitations.

This baseline table must feed the canonical analysis, any optional notebook, later funnel calculations, website data products, and QA checks so the same metric is not reimplemented differently across deliverables.

#### 6.4.3 Quiz evidence and answer-value policy

The quiz introduction confirms:

- its purpose is to guide SQL queries that explain the Metrocar database and construct the customer funnel;
- every question should be answered by writing an SQL query;
- the minimum passing grade is `60`;
- the learner may retake the quiz as many times as necessary during the sprint.

The supplied screenshots contain multiple-choice candidate values for counts, durations, payment totals, platform totals, and drop-off. Those choices are **not authoritative project data** and must not be copied into code, fixtures, tests, documentation, the notebook, or the website as expected results.

Required clean-room handling:

1. write the metric definition and SQL query without using the candidate values;
2. run the query against the approved data source;
3. validate the result independently with Pandas or a second aggregation where practical;
4. only after validation, compare the independently computed result with the quiz choices as a secondary sanity check;
5. if the computed result does not match a choice, investigate definitions, joins, filters, data version, and null handling rather than forcing the result to fit the quiz.

Do not use the historical score of `60/100` as evidence that any particular old answer, query, or metric definition was correct.

## 7. Historical Five-Day Learning Sequence — planning reference only

The five-day schedule describes the original course sprint. It does not impose a current deadline, but its sequence remains a useful dependency order for the rebuild.

### Day 1 — Explore the Metrocar data with SQL and Pandas

- establish secure database access;
- inspect the tables, columns, data types, row counts, nulls, duplicates, value ranges, timestamps, and join coverage;
- understand the ride-sharing business model and the available representation of each funnel stage;
- document data-quality findings before calculating business metrics.

### Days 2 and 3 — Develop Metrocar funnel metrics

- define reproducible funnel-stage rules;
- analyze the data against every required business question;
- reach evidence-backed conclusions;
- start building meaningful visualizations.

### Day 4 — Refine visualizations

- revise charts according to data-storytelling principles;
- make each chart directly support a finding or decision;
- implement and refine the required Plotly interactions for the web experience without Dash.

### Day 5 — Present results to stakeholders

- translate the validated findings into the recruiter-facing website narrative;
- connect insights to recommendations;
- validate the live experience and repository handoff. No recording or MasterSchool submission is required.

## 8. Staged Technical Execution Workflow

Execute this workflow in explicit phases. A phase prompt authorizes only the named phase and its prerequisites; it never authorizes later work automatically.

### Phase 0 — Repository and environment audit

- inventory files created for the new clean-room project only;
- identify what can be preserved or repaired;
- record Python and dependency versions;
- establish a standard project-local `venv` from a pinned `requirements.txt` and the confirmed secret-loading method;
- do not inspect or import the historical Dash project, notebook, slides, or recording until the clean-room plan is complete and user-approved, as required by Section 11.2;
- do not replace existing user work without first understanding it.

Use this confirmed, intentionally simple repository layout as components are introduced:

```text
README.md
requirements.txt
.env.example
.gitignore
analysis/
sql/
  production/
  practice/
docs/
tests/
web/
  public/data/
```

`analysis/` contains the canonical small Python modules. `sql/production/` contains validated queries; `sql/practice/` is isolated learning work. `web/` contains the Astro project, and only validated browser-safe generated files may enter `web/public/data/`. Do not create empty nested architecture speculatively; add files and subfolders only when the current phase needs them.

### Phase 1 — Data access and structural profiling

- connect through `METROCAR_DATABASE_URL`;
- enumerate expected tables and verify required columns;
- capture safe schema metadata without exposing credentials;
- profile rows, keys, duplicates, nulls, categorical values, and timestamp bounds;
- validate the provisional relationships in Section 6.3;
- fail clearly if the live schema differs from this specification.

### Phase 2 — Metric-definition contract

Before calculating results, create a compact metric dictionary containing:

- the business meaning of each funnel stage;
- the source table and qualifying condition;
- the counting grain;
- the deduplication rule;
- the time-window rule;
- the segment attribution rule for platform and age;
- conversion and drop-off formulas;
- known limitations.

This contract must be reviewed against the approved metric requirements and the user's final scope decisions. Do not allow funnel counts to be silently distorted by repeated ride requests, multiple transactions, or multiple reviews.

### Phase 3 — Reproducible analysis

- write SQL that extracts only required fields and produces auditable intermediate datasets;
- keep the canonical rerunnable pipeline in small `.py` modules; notebooks may explain or explore but must import/reuse canonical functions instead of duplicating business logic;
- use Pandas for validation, additional calculations, segmentation, and chart-ready outputs;
- construct the user base table with one compatible entity per row, Boolean funnel-stage columns, and retained `Unknown` values for unregistered downloads;
- construct a separate ride-grain base table for requested, finished, paid, and reviewed stages;
- use straightforward Pandas operations such as `groupby`, `any`, `sum`, Boolean masks, and transpose where they clearly express the calculation;
- keep funnel and rate functions small, avoid mutating caller-owned DataFrames, and copy inputs when a function performs intermediate transformations;
- document each non-trivial change of grain, join, derived stage flag, denominator, and business-rule decision at the point where a student needs that context;
- build the single canonical funnel-stage table and formulas defined in Section 4.1;
- assert decreasing stage counts, valid rate bounds, safe denominators, and reconciliation to Section 6.4 baseline metrics;
- answer every business question in Section 5;
- save important intermediate tables or summaries only when they improve reproducibility;
- add assertions for key invariants and reconcile totals across analysis paths;
- refuse unnecessary abstraction: do not build a generic analytics framework when a few readable functions and tables solve the confirmed problem.

### Phase 4 — Visual analysis and storytelling

- create the full user-level funnel and separate ride-level funnel defined in Section 4.2;
- implement or prepare the validated data products for platform, age-range, and date-range filters;
- provide absolute stage counts and switchable Percent of Top/Percent of Previous labels;
- visualize important drop-offs and conversion rates;
- compare funnel performance by platform and age range;
- visualize ride-request distribution by hour of day;
- create focused supporting charts for the strongest recommendations;
- perform a visual deep dive into one or two selected funnel sections;
- avoid decorative charts that do not answer a required question;
- use appropriate chart types with clear titles, axis labels, and tick labels;
- use color minimally and consistently;
- design website-ready visuals for a non-technical audience and keep each insight section focused on the smallest useful set of charts;
- implement the primary funnel and supporting interactive analytical views with Plotly/Plotly.js;
- optionally export a static Plotly funnel for README, social preview, or graceful fallback use.

### Phase 5 — Recommendations

For every recommendation, provide:

1. the decision or action proposed;
2. the supporting metric or pattern;
3. the affected funnel stage or customer segment;
4. expected business impact;
5. uncertainty, limitation, or follow-up test;
6. a clear separation between evidence and inference.

### Phase 6 — Deliverables and validation

Prepare and validate at least the following confirmed deliverables:

- reproducible SQL/SQLAlchemy data access and Pandas analysis;
- documented metric definitions and validated, web-ready aggregate outputs;
- Plotly-based user- and ride-funnel views with the confirmed filter and label behavior;
- focused Plotly insight views for the selected deep dives;
- a responsive, accessible Astro web application using React/TypeScript islands and Plotly.js, with no Dash runtime dependency;
- one documented command that reruns the analysis, fails safely on invalid results, and regenerates the public data;
- completed calculation, visual, interaction, narrative, accessibility, responsiveness, and security QA;
- a Render-deployed recruiter-facing interactive website implementing the confirmed dual-funnel and filter behavior;
- a prominent repository link to the live demo and concise instructions for viewing the analysis without local setup;
- concise methodology and data-lineage documentation sufficient to reproduce every published metric;
- a student-oriented reading guide and proportional code/SQL explanations that satisfy Section 9.1;
- a final `PASS`/`FAIL` report against Section 3.4.5 and the approved website acceptance criteria.

No MasterSchool form, deadline, slide deck, PDF, presentation recording, or Colab link is required. Exact filenames, folder layout, refresh-command implementation, Render build configuration, and optional supporting artifacts remain pending user decisions and the later repository audit.

## 9. Quality and Reproducibility Rules

- Use deterministic, rerunnable analysis steps.
- Keep raw extraction, cleaning, metric calculation, visualization, and narrative interpretation logically separated.
- Never hard-code a result that can be calculated.
- Confirm that joins do not inflate counts or revenue.
- Make null-handling and cancellation logic explicit.
- Label units, time zones, denominators, and filters.
- Ensure every chart matches the underlying table and every narrative number matches the final calculation.
- State material data limitations rather than hiding them.
- Prefer a small number of decision-useful findings over a large number of superficial observations.
- Keep web-page sections concise, takeaway-led, and understandable without technical implementation knowledge.
- Limit each insight section to the smallest useful set of charts and verify that every chart directly supports its takeaway.
- Use chart types, labeling, tick marks, and restrained color intentionally.

### 9.1 Proportional student-facing explanation standard

Every production analysis file must be understandable to a student following the project for the first time. Explanation depth must scale with conceptual difficulty rather than line count.

#### Level 1 — straightforward code

For obvious selection, renaming, simple filtering, `groupby().sum()`, or display formatting:

- use clear variable and function names;
- add no comment when the code and surrounding section already state the intent;
- add at most a short purpose comment when business context would otherwise be missing.

Do not write comments that merely translate syntax, such as `# sum the column` above `.sum()`.

#### Level 2 — multi-step transformation

For several connected Pandas operations, reusable funnel functions, segment preparation, or public-data export:

- state the input and output grain;
- explain the business purpose and why the transformation is needed;
- document material assumptions and null handling;
- use a short docstring or compact explanatory block rather than narrating every line.

#### Level 3 — conceptually difficult or high-risk logic

For multi-table joins, entity/grain reconciliation, unregistered-download handling, ride qualification, payment/review deduplication, date/cohort attribution, conversion denominators, or non-obvious validation:

- begin with the business question and metric definition;
- identify source tables and join keys;
- explain the chosen grain and why plausible alternatives were rejected;
- walk through the transformation in a small number of conceptual steps;
- state assumptions, edge cases, and data limitations;
- show the validation or reconciliation that makes the result trustworthy.

Use notebook Markdown cells only when a notebook is intentionally included as an explanatory artifact. Canonical `.py` and `.sql` files must remain understandable without requiring that optional notebook.

For production SQL, use a concise header containing the business question, output grain, and important filters. Comment only non-obvious CTEs, joins, window logic, or deduplication decisions. Keep comments synchronized with the query.

The repository README or methodology index must provide a short reading order that tells a student where to begin, which analysis files build the two base tables, where funnel metrics are calculated, where validation occurs, how public outputs are generated, and how those outputs reach the Plotly components.

## 10. Decisions Still Open

- Exact stage qualification and entity mapping within the confirmed user-level and ride-level funnels
- Exact definitions of accepted, completed, paid, and reviewed rides
- Date-range filtering and cohort-attribution semantics across funnel stages
- Exact name and orchestration implementation for the confirmed one-command analytical refresh
- Exact Render static-site build and deployment configuration
- Availability, condition, and reuse value of the historical Dash source files and presentation assets
- Remaining interactive controls and comparison behaviors beyond the confirmed side-by-side segment comparison
- Exact sticky/in-page navigation behavior within the confirmed single-page section order
- Detailed spacing, typography scale, chart palette, and component tokens within the confirmed light, navy, and blue-green business-dashboard direction
- Exact accessibility target and portfolio branding treatment; the public product language is confirmed as English
- Future Data Gym Brain integration boundary and reusable artifact contract
- Exact single-repository folder layout and final filenames

The implementing agent must not resolve these items by assumption while this plan remains `IN PROGRESS`.

## 11. User Additions

### 11.1 Confirmed portfolio goal: interactive recruiter-facing website

This project was originally completed and submitted approximately two years ago. The current work is a fresh portfolio rebuild, not a MasterSchool resubmission. It is also a deliberate test of how precisely the selected z.ai coding agent can execute a complete written specification.

The final repository must include a publicly accessible, modern **single-page** web application through which a potential recruiter, the project author, or a student can interact with and understand the Metrocar funnel. This remains intentionally proportionate to a strong school project rather than expanding into a large multi-page product.

Confirmed high-level outcomes:

- A recruiter who lands on the GitHub repository can immediately find and open a live web demo.
- The demo allows the recruiter to explore the funnel interactively rather than only viewing static screenshots or notebook output.
- The experience communicates the business problem, funnel stages, key metrics, important drop-offs, segment insights, and recommendations clearly.
- The repository and website together demonstrate data analysis, data storytelling, visualization, software craftsmanship, and product thinking.
- SQL, Python analysis, generated public data, frontend code, tests, and documentation live in one GitHub repository because this remains one coherent school-project rebuild.
- The project demonstrates an **end-to-end analytical product**: data access, metric design, validation, analysis, insight generation, visualization, web delivery, and quality assurance form one coherent system.
- Plotly powers the analytical visualizations, while the surrounding site provides the narrative, navigation, layout, accessibility, and portfolio polish.
- Dash is not part of the new application architecture.
- All public-facing content is written in English.
- The visual direction is a serious, elegant business dashboard appropriate for answering business questions.

Minimum recruiter-experience principles:

- no local setup should be required to view the deployed demo;
- the live-demo path from the repository should be obvious and require as few clicks as practical;
- the first screen should quickly explain what Metrocar is, what was analyzed, and why it matters;
- the first screen should communicate that this is a complete end-to-end analytical product, not an isolated chart or notebook;
- interactions should reveal useful detail and support exploration rather than exist only as decoration;
- supported segment comparisons should be available side by side where they improve the business analysis;
- methodology, definitions, and student-oriented explanations should remain understandable without forcing technical detail into the primary story;
- the interface should be responsive, accessible, visually coherent, and fast enough for portfolio review;
- displayed metrics must come from the validated analysis pipeline and reconcile with the canonical analytical outputs;
- historical/project data must be described honestly and must not be presented as live production data;
- the deployed application must never expose the database connection string or other secrets to the browser or public repository.

The confirmed frontend stack is **Astro + React interactive islands + TypeScript + Plotly.js**. The confirmed hosting target is a static deployment on **Render**, following the user's successful experience with that platform. Do not replace this stack or hosting target without explicit user approval.

### 11.2 Existing historical Dash implementation and presentation

The user previously completed a working interactive version with Dash and used it in the original presentation. The Dash work went beyond the minimum project requirements, and the mentor responded very positively to the result.

The user also has the completed presentation video and may provide the video and other historical project assets for review.

#### Clean-room planning rule

The historical implementation must **not** influence the new plan while official requirements and the user's current product vision are being defined. Do not inspect, summarize, import, execute, or copy from the old Dash project, old notebook, or old presentation during the clean-room planning phase.

Required sequence:

1. review all relevant official MasterSchool pages;
2. capture the user's current goals and modernization requirements independently;
3. define the new analysis, product, architecture, deliverables, acceptance criteria, and implementation plan without reference to the old solution;
4. obtain the user's approval of that clean-room plan;
5. only then perform a separate legacy-project audit;
6. compare the old work with the approved new plan and propose reuse candidates without changing the approved scope silently;
7. reuse an old artifact only after its calculations, security, compatibility, quality, and fit with the new plan have been revalidated.

The purpose of the later legacy audit is comparison and selective recovery, not requirements discovery. If the old project conflicts with the approved new plan, the new plan wins unless the user explicitly approves a change.

When the clean-room plan is complete and approved, the agent may inventory supplied historical materials, including where available:

- Dash source code;
- notebooks and SQL;
- generated datasets or aggregates;
- charts and exported assets;
- slide deck and PDF;
- presentation recording;
- README or submission notes.

Use these materials to identify potentially reusable analysis, effective interactions, strong storytelling choices, and useful assets. Do not assume that the old implementation, dependencies, calculations, or visual design are still correct merely because the presentation was successful. Revalidate metrics against the final analysis pipeline and review old code for security, reproducibility, compatibility, and maintainability.

The new deliverable is intended to be a complete modern web application, not an automatic recreation of the old Dash application. The clean-room plan must select its preferred architecture without consulting the old implementation. During the later legacy audit, useful calculations, content, interaction ideas, and validated assets may be proposed for reuse, but the Dash application framework itself must not be revived as the new runtime.

### 11.3 Portfolio-wide web-project convention

The user is intentionally turning analysis projects into browsable web experiences. The Metrocar project should fit that broader portfolio strategy while retaining its own business story and visual identity.

The final GitHub repository and live site should therefore feel like one coherent portfolio case study: problem, method, interactive evidence, conclusions, recommendations, and implementation quality should be easy to discover without requiring a recruiter to run a notebook.

### 11.4 Confirmed product hierarchy: insight-first, method-supported

The user considers the SQL quiz and related queries foundational work for understanding and validating the database. The following `Insights on Funnel Analysis` material is the most interesting and important part of the project and should receive the strongest treatment on the final website.

Apply this product hierarchy:

1. **Insights and decisions** — the primary recruiter-facing content.
2. **Interactive funnel evidence** — lets the recruiter explore and verify the story visually.
3. **Recommendations and expected business relevance** — turns findings into product and marketing decisions.
4. **Methodology and SQL/Pandas evidence** — available through progressive disclosure for technical credibility.
5. **Raw implementation detail** — retained in the repository and optional methodology artifacts, not allowed to overwhelm the main site narrative.

The website must not become a SQL tutorial or a visual dump of quiz answers. SQL queries and baseline questions should function as the trustworthy analytical foundation, reproducibility layer, and QA evidence behind the displayed metrics.

For every website insight, provide a consistent story unit containing:

- the business question;
- the key finding in plain language;
- the supporting metric or comparison;
- an appropriate interactive or static visualization;
- why the finding matters;
- an evidence-backed recommendation or decision implication;
- a caveat, limitation, or proposed next test when relevant;
- a link or expandable path to the supporting methodology without forcing technical detail into the main narrative.

Provisional recruiter journey to refine with the user:

1. concise executive takeaway;
2. interactive end-to-end funnel;
3. focused insight stories and side-by-side segment comparisons;
4. recommendations;
5. optional methodology, notebook, and repository details.

The page must support additional evidence-backed business questions discovered during the new analysis without requiring a structural rewrite. New questions should enter through the same reusable insight-story pattern rather than becoming disconnected custom sections.

No actual insight, number, ranking, or recommendation may be copied from the historical project during clean-room planning. The content hierarchy is confirmed, but the insight content itself must come from the official requirements and the newly validated analysis.

### 11.5 Confirmed implementation boundary and future Data Gym Brain use

Use this working architecture unless the user later approves a better equivalent:

1. SQL/SQLAlchemy and Pandas create validated, versionable analytical outputs from the source database.
2. A deterministic export step writes only the precomputed, non-sensitive aggregates and metadata required by the public experience.
3. The public frontend reads those versioned static outputs and never queries the source database or receives database credentials.
4. Plotly.js, directly or through the selected frontend framework, renders the interactive charts.
5. The surrounding web application owns navigation, narrative, filters, responsive layout, accessibility, and portfolio presentation.
6. No public application backend, Dash server, or Dash component architecture is used.
7. The product is delivered as one coherent page with in-page navigation and progressive disclosure instead of separate content pages.
8. Analysis, SQL, generated public data, frontend, tests, and documentation live in one repository with clear boundaries between source data work and browser-safe artifacts.
9. One documented command reruns the approved SQL/Pandas analysis, executes validation checks, and regenerates the public analytical outputs. It must stop on validation failure and must never publish partially validated results.
10. Python uses a project-local `venv` and pinned `requirements.txt`; canonical repeatable analysis is implemented in `.py` files, while any notebook remains an optional explanatory client of that code.
11. PostgreSQL access uses a synchronous SQLAlchemy 2.x engine with the psycopg 3 driver and readable raw SQL, without ORM or async infrastructure.

The user may later reuse parts of this project in the **Data Gym Brain Project**. The current workspace contains no reliable specification for that project, so the implementing agent must not invent an integration. It should instead keep metric definitions, validated aggregate schemas, insight content, and reusable frontend components modular and documented so a later integration can be designed without rewriting the analysis.

### 11.6 Extensible business questions and SQL practice

The user plans to continue improving the project, asking new business questions, and practicing SQL against the Metrocar database after the first public version is complete. Maintainability and learning value are therefore product requirements, not optional cleanup.

- Keep exploratory or practice SQL separate from production metric queries so experiments cannot silently change published results.
- Keep practice SQL repository-only. The public website may link only to polished, validated production SQL associated with a published metric.
- Organize production questions as reusable analytical units with a stable identifier, business definition, SQL/Pandas implementation, validation, public-safe output, visualization, finding, caveat, and recommendation.
- Provide a documented workflow and template for adding a new question end to end.
- Avoid hard-coded page structures that require custom wiring for every new insight; use reusable insight and comparison components where practical.
- Preserve readable SQL and explanatory comments so a student can learn from the repository without weakening the production pipeline.
- Allow the public story to grow selectively: a new analysis should appear on the website only after it is validated and contributes a meaningful business conclusion.
- Keep the web presentation engaging through purposeful Plotly interaction, comparison, hierarchy, and progressive disclosure—not through distracting animation or ornamental effects.

### 11.7 Confirmed page structure and interaction presentation

Use this single-page order:

1. **Hero and project context**
2. **Executive Summary and key KPIs**
3. **Interactive Funnel Explorer**
4. **Segment Comparison**
5. **Key Business Insights**
6. **Recommendations**
7. **Methodology, Data Quality, and SQL**
8. **GitHub repository link**

Presentation rules:

- Show the user and rides funnels in one shared area with labeled tabs, not as two long duplicate sections.
- Support side-by-side comparison for platform and age group; use date as a filter in the first version.
- Provide a concise expandable `How was this calculated?` explanation for important metrics, with a link to the complete production SQL in the repository.
- Keep practice SQL separate from the production query linked by the public metric explanation.
- Use a light interface foundation, dark-navy typography, and restrained blue-green accents.
- Preserve generous spacing, clear hierarchy, and readable annotations so the dashboard remains serious and accessible to students.
- Use purposeful hover, selection, filtering, and transitions to make the presentation engaging; avoid visual effects that do not improve understanding.

## 12. Staged Execution Gates

### 12.1 Current authorization: Phase 0 setup and Phase 1 only

The preflight agent read the complete plan and confirmed that the workspace contains only this Markdown file. The user approved moving forward through controlled prompts.

The current phase prompt may authorize the agent to:

- create the minimal root safeguards and Phase 1 folders/files required by the confirmed layout;
- create `.gitignore`, `.env.example`, pinned `requirements.txt`, the project-local `venv`, and small database/profiling modules;
- check whether `METROCAR_DATABASE_URL` is available without printing its value;
- connect read-only to the approved PostgreSQL database when the secret is available;
- inspect schema metadata, keys, duplicates, nulls, categories, timestamp bounds, and join cardinalities;
- create tests for credential safety, connection configuration, schema expectations, and non-inflating join checks;
- write a credential-free data-quality/profile report.

During this authorization, the agent must not:

- calculate or publish final funnel metrics, insight conclusions, or recommendations;
- generate browser-facing analytical datasets;
- scaffold or implement the Astro frontend;
- inspect or reuse historical Dash, notebook, slide, or presentation assets;
- commit, deploy, or perform destructive operations;
- continue into Phase 2 without a new approval prompt.

If the database credential is absent, the agent must finish all safe local setup it can, report the exact non-secret configuration step required from the user, and stop. It must never ask the user to paste the credential into chat or a tracked file.

### 12.1.1 Interim review after credential-free setup

The first Phase 1 pass created the minimal Python environment, safeguards, profiling modules, SQL, tests, and README. The credential was correctly absent, so no live database query was attempted. An independent review found that the scope discipline and current `SELECT` queries are appropriate, but live profiling is not yet authorized. Complete one small credential-free remediation pass first:

- enforce PostgreSQL read-only sessions at the connection level, not only by convention in the current query text;
- prevent both engine-construction and connection failures from exposing the URL or a chained underlying exception in a full traceback;
- route the documented profiling command through one safe runner that checks the connection and exits with a credential-free message;
- make schema validation fail clearly or produce a useful partial report when an expected table or column is missing, rather than crashing during later profiling queries;
- either enumerate public tables so additional tables can truly be reported or remove the unsupported extra-table claim;
- add structural evidence for inconsistent ride-stage combinations, including pickup without acceptance, drop-off without pickup or acceptance, cancellation combined with later stages, approved payment without a completed ride, and review without a completed ride;
- make `sql/production/01_structural_profile.sql` accurately match the Python profile or label and document it as a deliberately compact manual subset;
- add credential-free tests for read-only configuration, sentinel-secret redaction in the full failure path, graceful schema mismatch handling, and the corrected reporting behavior;
- rerun the complete credential-free test suite and stop with a concise correction report.

During this remediation pass, do not create or read `.env`, connect to the database, generate `docs/data_quality_report.md`, calculate metrics, begin Phase 2, scaffold the frontend, inspect historical assets, commit, or deploy. Live Phase 1 profiling becomes eligible only after this correction report is reviewed.

### 12.1.2 Live Phase 1 authorization

The credential-free remediation is verified complete: 28 tests pass and the four live-database tests skip because `.env` is absent. The user may now configure `.env` locally, and a fresh agent chat may run only the safe Phase 1 runner, live schema/profile tests, and credential-free data-quality report. Stop at the Phase 1 checkpoint in Section 12.2. Do not print the URL, calculate final metrics, begin Phase 2, build the frontend, inspect legacy assets, commit, or deploy.

### 12.1.3 Live-schema reconciliation

The live Phase 1 runner connected read-only and produced the credential-free report. The database revealed three plan differences: `dropoff_location` replaces `destination_location`, `review` replaces `free_response`, and `transactions.transaction_id` exists as a non-null candidate key. The exact payment-status values are `Approved` and `Decline`. Reconcile code, tests, SQL, and the generated report with these verified facts; validate `transaction_id` uniqueness; require zero remaining schema mismatches and a fully passing test suite; then stop for Phase 2 review. The implementation agent must follow Section 12.4 and must not edit this plan.

### 12.2 Phase 1 checkpoint

Before requesting Phase 2 approval, report:

- files created or changed;
- installed and pinned dependency versions;
- database connectivity status without credential disclosure;
- actual schema versus Section 6.2;
- table profiles and join-cardinality findings;
- candidate definitions and unresolved risks for requested, accepted, completed, paid, and reviewed rides;
- date/time-zone findings relevant to cohort rules;
- commands and tests executed with their results;
- every ambiguity requiring a user decision.

Stop after the report. Phase 2 becomes eligible only after the user and planning assistant review these findings and update the metric-definition contract.

### 12.3 Full-build readiness

Later phases may proceed only when their prerequisites are satisfied:

- all current portfolio deliverables and acceptance criteria remain captured without historical submission work;
- metric definitions needed by the next phase are unambiguous or explicitly isolated as blocked;
- secrets and access instructions remain safe;
- the previous phase's acceptance checks pass;
- the user explicitly approves the next phase.

### 12.4 Canonical plan ownership

The user and the planning assistant exclusively maintain `METROCAR_PROJECT_EXECUTION_PLAN.md`. Implementation agents, including Kimi, must treat it as read-only: they may read it and may stage, commit, or push an already reviewed plan change made by the planning assistant, but they must not edit, rewrite, rename, restore, or delete it. Proposed plan changes belong in the checkpoint report for the planning assistant to incorporate. If an implementation agent observes an unexpected plan diff, it must stop and report it without attempting repair.

## 13. Change Log

- **2026-08-26:** Reconciled the canonical plan with the live Phase 1 schema: adopted `dropoff_location`, `review`, candidate key `transaction_id`, and exact `Approved`/`Decline` statuses; recorded unknown timestamp timezone and valid cancel-after-accept behavior. Reserved all future canonical-plan edits for the user and planning assistant after an implementation-agent edit accidentally truncated the file; implementation agents may now read and commit reviewed plan changes but may never modify the plan themselves.
- **2026-08-26:** Verified the completed credential-free remediation, including gated joins and fully skipped partial-report rendering. Independently confirmed 28 tests pass and four database tests skip. Authorized live Phase 1 profiling in a fresh agent chat while keeping Phase 2 and all later work blocked until the generated data-quality report is reviewed.
- **2026-08-26:** Reviewed the first Phase 1 credential-free implementation report and the created files. Confirmed 9 local tests pass and 4 database tests skip because `.env` is absent. Kept Phase 2 blocked and added a credential-free remediation gate for connection-level read-only enforcement, full-path secret redaction, a safe runner, graceful schema mismatch handling, stronger structural ride-status evidence, accurate SQL/Python scope wording, and focused regression tests before any live database access.
- **2026-08-26:** Reviewed and accepted the z.ai preflight report. Confirmed the workspace contains only the plan and that no implementation or historical asset inspection occurred. Changed the status to staged execution, authorized only Phase 0 setup plus Phase 1 structural profiling, added explicit allowed/forbidden actions and checkpoint reporting, and fixed the initial simple repository layout. Deferred Python Plotly unless a concrete analysis-layer need is demonstrated because Plotly.js owns the confirmed frontend visualization layer.
- **2026-08-26:** Added a proportional explanation standard for student readability. Straightforward code relies on clear naming and minimal comments; multi-step transformations explain purpose, grain, assumptions, and null handling; high-risk logic explains the business definition, joins, alternatives, edge cases, and validation. Required concise SQL headers, synchronized non-obvious comments, and a repository reading guide from analysis through Plotly delivery.
- **2026-08-26:** Confirmed the simple Python execution model: canonical analysis in readable `.py` files, optional explanatory notebooks only, a project-local `venv`, and pinned `requirements.txt`. Confirmed practice SQL as repository-only and public links as validated production SQL only. Selected synchronous SQLAlchemy 2.x plus psycopg 3 (`psycopg[binary]`) for PostgreSQL access, using raw SQL and no ORM or async layer.
- **2026-08-26:** Added nine official Tips & Tricks screenshots and the supplied segmented `groupby(...).sum().T` example. Confirmed the simple Boolean-base-table approach; four-stage user and ride funnels; unregistered-download preservation; `Unknown` handling; platform/age/date segmentation; and a strict student-project simplicity budget. Also finalized the page section order, funnel tabs, platform/age comparison with date filtering, expandable calculation explanations, repository SQL links, and the light navy/blue-green visual direction.
- **2026-08-26:** Finalized Astro, React interactive islands, TypeScript, and Plotly.js as the frontend stack and Render as the deployment target. Confirmed a single command for analysis, validation, and safe-data regeneration. Added extensibility requirements for future business questions, isolated SQL practice, reusable insight units, and an engaging but business-appropriate interactive presentation.
- **2026-08-26:** Confirmed a static-data public architecture and one-repository delivery. The analysis pipeline computes and validates the funnel from the source database, exports only safe precomputed aggregates, and the public app makes no live database call. Recorded Astro plus React/TypeScript Plotly islands and Render as leading—but not yet final—stack and hosting choices based on the user's current experience.
- **2026-08-26:** Confirmed the first product-design decisions: one proportionate single-page school-project experience; English-only public copy; an audience that includes recruiters, the author, and students; a serious and elegant business-dashboard direction; an explicit end-to-end analytical-product message; required side-by-side segment comparison; and a reusable insight pattern that can absorb additional business questions discovered during analysis.
- **2026-08-26:** Corrected the project scope after user clarification. The original MasterSchool project was submitted two years ago; the current work is an independent portfolio rebuild and z.ai agent test, so the submission form, historical deadline, Colab submission, slide deck, PDF, and recording are not current deliverables. Made Plotly/Plotly.js mandatory, excluded Dash from the new runtime, defined the analysis-to-frontend boundary, and recorded future modular reuse in Data Gym Brain without inventing an integration contract.
- **2026-08-26:** Added the Project submission guidelines source. Confirmed the mandatory single-image Plotly funnel, report-like proof-of-work notebook, maximum five-minute video with screen share and visible camera, flexible recording hosts, concise non-technical content rules, optional Plotly/Dash dashboard status, recommended presentation flow, and historical EOD Sunday (04/08) deadline caveat. Reconciled these rules with the stricter 3–5 minute requirement already captured from Key Requirements.
- **2026-08-26:** Added the Insights on the Customer Funnel source. Confirmed separate full user-level and ride-request-based ride-level funnels; platform, age, and date filters; absolute labels; Percent of Top/Previous switching; and a policy for original, justified business questions. Promoted the official advanced dashboard behavior to minimum functionality for the user's recruiter-facing website without locking the final stack to Plotly.
- **2026-08-26:** Added the user-provided SQL quiz screenshots as a reviewed source. Confirmed one SQL query per database-understanding question, a passing grade of 60, and unlimited sprint attempts. Added a strict policy that multiple-choice values and the historical score are non-authoritative until independently reproduced and validated.
- **2026-08-26:** Added the user's insight-first product hierarchy. SQL quiz work is treated as the data-understanding, reproducibility, and QA foundation, while the recruiter-facing website prioritizes interactive evidence, clear insights, business meaning, and recommendations with technical methodology available through progressive disclosure.
- **2026-08-26:** Completed the four-page Part 1 review. Added the funnel common-granularity rule, canonical ordered stage table, Percent of Top/Previous and drop-off formulas, monotonicity and denominator validation, and an explicit SQL/SQLAlchemy-for-access plus Pandas-for-analysis interpretation of the title/body mismatch.
- **2026-08-26:** Added the Understanding the Database source and converted its ten Pandas questions into explicit analysis tasks, definition safeguards, join validations, and a required auditable baseline-metrics table shared across deliverables.
- **2026-08-26:** Added the user's clean-room planning rule. Official requirements and the new product plan must be completed and approved before any historical Dash code, notebook, presentation, or video is inspected. Legacy work may only be audited afterward for separately validated reuse candidates.
- **2026-08-26:** Recorded the existence of the successful historical Dash implementation and presentation video for a later legacy audit, clarified that the new deliverable is a complete modern website rather than an automatic Dash recreation, and captured the user's wider portfolio convention of turning analysis projects into browsable web experiences.
- **2026-08-26:** Added the user's confirmed modernization goal: a public, recruiter-facing, interactive Metrocar funnel website linked clearly from GitHub. Added recruiter-experience and security principles while leaving stack, hosting, interaction design, and branding decisions open for later review.
- **2026-08-26:** Added the Key Requirements source. Confirmed the submission package, 3–5 minute speaker-view video, executed notebook, slide PDF, required analysis tools, funnel deep dive, evidence-backed recommendation criteria, non-technical storytelling rules, chart constraints, and an explicit acceptance checklist.
- **2026-08-26:** Created the living execution plan from the Project Overview page. Added confirmed business context, funnel stages, questions, schema, five-day logistics, provisional workflow, security rules, and readiness gate.

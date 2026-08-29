# Associate Data Analyst in SQL — Metrocar reference map

> **Metrocar project reference.** This map helps readers find where an analytical technique is taught and how it can transfer to Metrocar. It is a navigation aid, not a replica of DataCamp.
>
> **Source check:** track membership and the named chapters were verified against the current official DataCamp track and course pages plus course metadata on 2026-08-29. DataCamp remains the source of truth for course content and current catalog structure.

## Source and privacy boundary

Record only verified track, course, and chapter identity; concise concept summaries; code-complexity calibration; and transfer guidance.

Do **not** copy full lessons, transcripts, exercise prompts, starter code, verified solutions, platform feedback, account data, progress, XP, or other paid/private course content into this map. Do not copy private study material into Metrocar.

Metrocar material may reference verified official DataCamp course or chapter names and official links, but it must demonstrate Metrocar's own application of the concept. It must not expose private repository paths or private study content.

## Navigation model

```text
Track
→ Course
→ useful verified Chapter
→ Core concepts
→ Typical analytical idioms
→ Project/Metrocar transfer
```

## Verified track structure

Official track: [Associate Data Analyst in SQL](https://app.datacamp.com/learn/career-tracks/associate-data-analyst-in-sql)

1. [Introduction to SQL](https://www.datacamp.com/courses/introduction-to-sql)
2. [Intermediate SQL](https://www.datacamp.com/courses/intermediate-sql)
3. [Joining Data in SQL](https://www.datacamp.com/courses/joining-data-in-sql)
4. [Data Manipulation in SQL](https://www.datacamp.com/courses/data-manipulation-in-sql)
5. [PostgreSQL Summary Stats and Window Functions](https://www.datacamp.com/courses/postgresql-summary-stats-and-window-functions)
6. [Functions for Manipulating Data in PostgreSQL](https://www.datacamp.com/courses/functions-for-manipulating-data-in-postgresql)
7. [Introduction to Statistics](https://www.datacamp.com/courses/introduction-to-statistics)
8. [Exploratory Data Analysis in SQL](https://www.datacamp.com/courses/exploratory-data-analysis-in-sql)
9. [Data-Driven Decision Making in SQL](https://www.datacamp.com/courses/data-driven-decision-making-in-sql)
10. [Understanding Data Visualization](https://www.datacamp.com/courses/understanding-data-visualization)
11. [Data Communication Concepts](https://www.datacamp.com/courses/data-communication-concepts)

The verified track structure matches this eleven-course order.

## Course navigation

| Course | Role, concepts, and typical idioms | Code-complexity signal | Metrocar relevance | Useful verified refresher chapters |
|---|---|---|---|---|
| Introduction to SQL | Relational tables and fields; `SELECT`, `FROM`, `DISTINCT`, aliases | Short retrieval queries with one clear purpose | Direct | Course-level reference is enough |
| Intermediate SQL | Filtering, aggregates, sorting, `GROUP BY`, `HAVING`, readable aliases | Direct queries that answer one grouped question | Direct | Course-level reference is enough |
| Joining Data in SQL | Join keys, table relationships, INNER/LEFT joins, sets, and subqueries | One relationship and join choice at a time | Direct | Introducing Inner Joins; Outer Joins, Cross Joins and Self Joins; Set Theory for SQL Joins; Subqueries |
| Data Manipulation in SQL | `CASE`, subqueries, correlated and nested queries, CTEs, and window functions | Intermediate query composition with named steps | Direct | We'll take the CASE; Short and Simple Subqueries; Correlated Queries, Nested Queries, and Common Table Expressions; Window Functions |
| PostgreSQL Summary Stats and Window Functions | `OVER`, `PARTITION BY`, ordering, ranking, lag/lead, and windowed aggregates | Intermediate; use when row-level context must be preserved | Later / conditional | Introduction to window functions |
| Functions for Manipulating Data in PostgreSQL | Data types, date/time operations, strings, and PostgreSQL-specific functions | Function-level transformations; keep dialect dependence visible | Supporting | Working with DATE/TIME Functions and Operators |
| Introduction to Statistics | Center, spread, probability, distributions, correlation, and hypothesis testing | Conceptual foundation rather than a query pattern | Supporting | Course-level reference is enough |
| Exploratory Data Analysis in SQL | Inspect schemas and keys, count rows, check missing values, study relationships, and aggregate timestamps | A sequence of small diagnostic queries | Direct | What's in the Database?; Working with Dates and Timestamps |
| Data-Driven Decision Making in SQL | Translate a business question into aggregates, joins, KPIs, subqueries, `EXISTS`, and justified OLAP | Progress from simple decision query to advanced SQL only when earned | Direct | All four verified chapters listed below |
| Understanding Data Visualization | Interpret distributions, relationships, color, shape, and plot quality | Visual judgment without unnecessary coding | Supporting | Course-level reference is enough |
| Data Communication Concepts | Structure evidence, central insight, audience translation, written reports, and presentations | Clear claims and limitations before polish | Supporting | Course-level reference is enough |

## Detailed Metrocar transfer

### Joining Data in SQL

Verified chapters:

- [Introducing Inner Joins](https://campus.datacamp.com/courses/joining-data-in-sql/introducing-inner-joins)
- [Outer Joins, Cross Joins and Self Joins](https://campus.datacamp.com/courses/joining-data-in-sql/outer-joins-cross-joins-and-self-joins)
- [Set Theory for SQL Joins](https://campus.datacamp.com/courses/joining-data-in-sql/set-theory-for-sql-joins)
- [Subqueries](https://campus.datacamp.com/courses/joining-data-in-sql/subqueries-4)

| Core concept | Typical analytical idioms | Metrocar transfer |
|---|---|---|
| Join-key reasoning | explicit `ON` conditions and qualified column names | State how downloads, signups, rides, transactions, and reviews relate |
| Relational cardinality | check key uniqueness and expected one-to-many relationships | Protect the governed user or ride grain |
| INNER join | retain matched records when the question truly requires both sides | Use only when loss of unmatched base records is intended |
| LEFT join | preserve every row from the declared base table | Keep downloads or another funnel base population when later events are missing |
| Missing relationship evidence | null checks after a LEFT join | Separate “no later event” from a broken join |
| Set or subquery concepts | use only when the relationship is clearer than an ordinary join | Avoid advanced-looking syntax when a direct join communicates the question better |

### Data Manipulation in SQL

Verified chapters:

- [We'll take the CASE](https://campus.datacamp.com/courses/data-manipulation-in-sql/well-take-the-case)
- [Short and Simple Subqueries](https://campus.datacamp.com/courses/data-manipulation-in-sql/short-and-simple-subqueries)
- [Correlated Queries, Nested Queries, and Common Table Expressions](https://campus.datacamp.com/courses/data-manipulation-in-sql/correlated-queries-nested-queries-and-common-table-expressions)
- [Window Functions](https://campus.datacamp.com/courses/data-manipulation-in-sql/window-functions-4)

| Core concept | Typical analytical idioms | Metrocar transfer |
|---|---|---|
| Conditional logic | `CASE WHEN ... THEN ... END` | Build explicit stage flags or conditional counts |
| Simple subqueries | small `SELECT` inside `WHERE`, `FROM`, or `SELECT` | Isolate one prerequisite population or summary |
| CTEs | `WITH` plus descriptive step names | Show the analytical sequence without a deep helper stack |
| Correlated or nested queries | reference outer rows only when the relationship requires it | Use for genuine per-entity logic, not as decoration |
| Window functions | `OVER (...)` with partition and order | Select or compare ordered events while preserving rows |

Current DataCamp metadata was used for these concept families. No private companion exercise content was consulted or copied.

### Exploratory Data Analysis in SQL

Useful verified chapters:

- [What's in the Database?](https://campus.datacamp.com/courses/exploratory-data-analysis-in-sql/whats-in-the-database)
- [Working with Dates and Timestamps](https://campus.datacamp.com/courses/exploratory-data-analysis-in-sql/working-with-dates-and-timestamps)

| Core concept | Typical analytical idioms | Metrocar transfer |
|---|---|---|
| Table and schema exploration | inspect tables, columns, types, and sample rows | Confirm where each event and identifier lives |
| Relationship and key reasoning | counts, distinct counts, and joins for diagnosis | Test whether assumed keys preserve the analytical grain |
| Missing-value checks | null counts and conditional summaries | Quantify source limitations before funnel calculation |
| Timestamp investigation | date extraction, intervals, and date grouping | Investigate source hours or event timing without silently changing the snapshot |
| Relationship exploration | small joins plus reconciliation counts | Validate how tables connect before making a claim |

### Data-Driven Decision Making in SQL

Verified chapters:

- [Introduction to business intelligence for a online movie rental database](https://campus.datacamp.com/courses/data-driven-decision-making-in-sql/introduction-to-business-intelligence-for-a-online-movie-rental-database)
- [Decision Making with simple SQL queries](https://campus.datacamp.com/courses/data-driven-decision-making-in-sql/decision-making-with-simple-sql-queries)
- [Data Driven Decision Making with advanced SQL queries](https://campus.datacamp.com/courses/data-driven-decision-making-in-sql/data-driven-decision-making-with-advanced-sql-queries)
- [Data Driven Decision Making with OLAP SQL queries](https://campus.datacamp.com/courses/data-driven-decision-making-in-sql/data-driven-decision-making-with-olap-sql-queries)

> Source-fidelity note: DataCamp currently displays “for **a** online movie rental database.” The grammatical typo is preserved here because chapter identity must not be silently normalized.

The useful learning progression is:

```text
simple business question
→ aggregation
→ GROUP BY
→ LEFT JOIN
→ business KPIs
→ subqueries
→ EXISTS
→ more advanced analytical SQL only when justified
```

For Metrocar, this progression means starting from the decision and base population, then adding only the joins or query layers required to compute and validate the governed metric. OLAP operators are later/conditional, not a default for a straightforward funnel.

## Code-level calibration

The intended project-learning range is:

`DataCamp beginner → intermediate analytical level`

Intermediate is the normal Masterschool working level.

- Prefer short, direct analytical code.
- Teach one analytical idea at a time.
- Explicit intermediate variables are good.
- Familiar pandas idioms such as filtering, Boolean masks, new columns, `groupby`, `agg`, `any`, `sum`, `count`, `nunique`, `notna`, `isna`, `merge`, and simple ratios are normal.
- Familiar SQL such as `SELECT`, `WHERE`, `CASE`, `GROUP BY`, aggregates, ordinary joins including `LEFT JOIN`, simple subqueries, CTEs, `EXISTS`, and window functions is legitimate when genuinely required by the learning progression.
- Judge complexity by conceptual load, not by whether one feature is called “advanced.”
- Student code should not default to class hierarchies, generic engines or frameworks, deep helper stacks, speculative abstractions, dense one-liners, or defensive machinery for hypothetical cases unsupported by evidence.
- Production robustness may exceed student complexity when correctness, validation, reproducibility, privacy, or verified edge cases require it.

> Learn the analytical idea in DataCamp form first; add production robustness only when a verified requirement earns it.

## Future Metrocar refresher convention

Use this compact public-safe pattern when a material technique first appears:

```text
📚 DataCamp refresher

Course: <verified official course>
Chapter: <verified official chapter when useful>
Concept: <one short sentence describing the technique>
```

Rules:

- Add a refresher only when a material technique is first introduced.
- Do not repeat the same reference in every cell.
- Prefer Course → Chapter → Concept.
- Omit the chapter when a course-level reference is enough.
- Use only verified official DataCamp names and official links.
- Do not expose private repository paths in public Metrocar artifacts.
- Never copy exercise prompts, starter code, solutions, transcripts, feedback, account data, or paid/private lesson content into Metrocar.
- Metrocar must demonstrate its own transfer and application of the concept.

The purpose is retrieval: readers should know where to return in DataCamp to relearn the technique more deeply.

## SQL Metrocar lookup

| Metrocar need | Course | Verified refresher chapter |
|---|---|---|
| Inspect tables and relationships | Exploratory Data Analysis in SQL | What's in the Database? |
| Write straightforward joins | Joining Data in SQL | Introducing Inner Joins / Outer Joins, Cross Joins and Self Joins |
| Preserve a base population with `LEFT JOIN` | Data-Driven Decision Making in SQL | Decision Making with simple SQL queries |
| Calculate grouped funnel measures or KPIs | Intermediate SQL / Data-Driven Decision Making in SQL | Course-level / Decision Making with simple SQL queries |
| Use conditional aggregation | Data Manipulation in SQL | We'll take the CASE |
| Use a simple subquery | Data Manipulation in SQL | Short and Simple Subqueries |
| Use existence logic when genuinely useful | Data-Driven Decision Making in SQL | Data Driven Decision Making with advanced SQL queries |
| Investigate source hours or dates | Exploratory Data Analysis in SQL | Working with Dates and Timestamps |
| Use window functions | PostgreSQL Summary Stats and Window Functions | Introduction to window functions |

## Maintenance note

Re-check DataCamp before using this map as evidence for a future change. If the catalog changes, update the verified identity here; do not reconstruct unseen chapters or lessons from memory.

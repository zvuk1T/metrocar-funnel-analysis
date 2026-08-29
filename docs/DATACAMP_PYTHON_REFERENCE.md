# Data Analyst in Python — Metrocar reference map

> **Metrocar project reference.** This map helps readers find where an analytical technique is taught and how it can transfer to Metrocar. It is a navigation aid, not a replica of DataCamp.
>
> **Source check:** track membership and the named chapters were verified against the current official DataCamp track page and course metadata on 2026-08-29. DataCamp remains the source of truth for course content and current catalog structure.

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

Official track: [Data Analyst in Python](https://app.datacamp.com/learn/career-tracks/data-analyst-with-python)

1. [Introduction to Python](https://www.datacamp.com/courses/intro-to-python-for-data-science)
2. [Intermediate Python](https://www.datacamp.com/courses/intermediate-python)
3. [Data Manipulation with pandas](https://www.datacamp.com/courses/data-manipulation-with-pandas)
4. [Joining Data with pandas](https://www.datacamp.com/courses/joining-data-with-pandas)
5. [Introduction to Statistics in Python](https://www.datacamp.com/courses/introduction-to-statistics-in-python)
6. [Introduction to Data Visualization with Seaborn](https://www.datacamp.com/courses/introduction-to-data-visualization-with-seaborn)
7. [Exploratory Data Analysis in Python](https://www.datacamp.com/courses/exploratory-data-analysis-in-python)
8. [Sampling in Python](https://www.datacamp.com/courses/sampling-in-python)
9. [Hypothesis Testing in Python](https://www.datacamp.com/courses/hypothesis-testing-in-python)

The verified track structure matches this nine-course order.

## Course navigation

| Course | Role, concepts, and typical idioms | Code-complexity signal | Metrocar relevance | Useful verified refresher chapters |
|---|---|---|---|---|
| Introduction to Python | Python values, variables, lists, functions, packages, and NumPy foundations | Short expressions and direct function calls | Supporting | Course-level reference is enough |
| Intermediate Python | Dictionaries, pandas DataFrames, comparison and Boolean logic, filtering, loops, and basic plotting | Explicit conditions and small step-by-step transformations | Direct | Course-level reference is enough |
| Data Manipulation with pandas | Inspect, filter, transform, aggregate, count, deduplicate, handle missing values, and calculate ratios | Familiar DataFrame methods plus intermediate variables | Direct | Transforming DataFrames; Aggregating DataFrames; Slicing and Indexing DataFrames; Creating and Visualizing DataFrames |
| Joining Data with pandas | Choose keys, reason about table relationships, merge without unintended row loss, and validate integrity | One merge at a time with explicit keys and join type | Direct | Data Merging Basics; Merging Tables With Different Join Types; Advanced Merging and Concatenating; Merging Ordered and Time-Series Data |
| Introduction to Statistics in Python | Summary statistics, distributions, probability, correlation, and experimental design | Intermediate statistical reasoning; use only when the question requires it | Supporting | Course-level reference is enough |
| Introduction to Data Visualization with Seaborn | Choose plots for categorical and quantitative relationships; label and customize for interpretation | Direct plotting calls with purposeful encodings | Supporting | Course-level reference is enough |
| Exploratory Data Analysis in Python | Inspect and validate data, clean inconsistent values, study relationships, and turn exploration into a testable action | Several small checks assembled into an evidence chain | Direct | Getting to Know a Dataset; Data Cleaning and Imputation; Relationships in Data; Turning Exploratory Analysis into Action |
| Sampling in Python | Random, stratified, and cluster sampling; sampling and bootstrap distributions | Intermediate and conditional on inferential scope | Later / conditional | Course-level reference is enough |
| Hypothesis Testing in Python | Select and interpret common tests, p-values, confidence intervals, and error types | Intermediate; requires explicit assumptions and a real hypothesis | Later / conditional | Course-level reference is enough |

## Detailed Metrocar transfer

### Data Manipulation with pandas

Verified chapters:

- [Transforming DataFrames](https://campus.datacamp.com/courses/data-manipulation-with-pandas/transforming-dataframes)
- [Aggregating DataFrames](https://campus.datacamp.com/courses/data-manipulation-with-pandas/aggregating-dataframes)
- [Slicing and Indexing DataFrames](https://campus.datacamp.com/courses/data-manipulation-with-pandas/slicing-and-indexing-dataframes)
- [Creating and Visualizing DataFrames](https://campus.datacamp.com/courses/data-manipulation-with-pandas/creating-and-visualizing-dataframes)

| Core concept | Typical analytical idioms | Metrocar transfer |
|---|---|---|
| Inspection and subsetting | `.head()`, `.info()`, column selection, `.loc[]` | Confirm source shape and inspect only fields needed for a funnel question |
| Boolean filtering | Boolean masks, `.notna()`, `.isna()` | Define explicit stage eligibility and investigate missing timestamps |
| New columns | Direct column assignment from simple expressions | Create readable flags or durations before summarizing |
| Grouped summaries | `.groupby()`, `.agg()`, named aggregations | Calculate stage totals or quality checks by a governed segment |
| Counts and entity reduction | `.sum()`, `.count()`, `.nunique()`, duplicate handling | Reduce repeated observations to the required user or ride grain |
| Proportions and simple ratios | Named numerator and denominator variables | Calculate conversion measures without hiding the denominator |
| Missing values | Missingness checks and explicit handling | Preserve evidence about incomplete journeys instead of silently dropping it |

**Pedagogical signal:** DataCamp typically teaches one analytical idea at a time through short, explicit transformations and intermediate variables. Metrocar learning code should keep that clarity even when production validation is added.

### Joining Data with pandas

Verified chapters:

- [Data Merging Basics](https://campus.datacamp.com/courses/joining-data-with-pandas/data-merging-basics)
- [Merging Tables With Different Join Types](https://campus.datacamp.com/courses/joining-data-with-pandas/merging-tables-with-different-join-types)
- [Advanced Merging and Concatenating](https://campus.datacamp.com/courses/joining-data-with-pandas/advanced-merging-and-concatenating)
- [Merging Ordered and Time-Series Data](https://campus.datacamp.com/courses/joining-data-with-pandas/merging-ordered-and-time-series-data)

| Core concept | Typical analytical idioms | Metrocar transfer |
|---|---|---|
| Join-key reasoning | `.merge(..., on=...)` with named keys | Make the relationship between users, downloads, signups, rides, and reviews explicit |
| One-to-one and one-to-many relationships | Inspect key uniqueness before merging | Prevent accidental row multiplication at the governed grain |
| Population preservation | `how="left"` | Preserve downloads or another base population when a later event is absent |
| Missing rows after joins | Post-merge missingness and row-count checks | Distinguish “no later event” from an unintended join failure |
| Multi-table joins | One readable merge at a time | Keep the analytical path inspectable across several event tables |
| Integrity validation | `validate=` plus before/after counts | State and test the expected merge cardinality |
| Semi/anti join logic | Membership filters only when they clarify the question | Find entities with or without a related event when that is the actual question |
| Ordered or time-aware joins | Ordered/time-aware merge only when event timing requires it | Avoid adding time-aware complexity to ordinary relational joins |

### Exploratory Data Analysis in Python

Verified chapters:

- [Getting to Know a Dataset](https://campus.datacamp.com/courses/exploratory-data-analysis-in-python/getting-to-know-a-dataset)
- [Data Cleaning and Imputation](https://campus.datacamp.com/courses/exploratory-data-analysis-in-python/data-cleaning-and-imputation)
- [Relationships in Data](https://campus.datacamp.com/courses/exploratory-data-analysis-in-python/relationships-in-data)
- [Turning Exploratory Analysis into Action](https://campus.datacamp.com/courses/exploratory-data-analysis-in-python/turning-exploratory-analysis-into-action)

| Core concept | Typical analytical idioms | Metrocar transfer |
|---|---|---|
| Initial inspection and validation | shape, data types, value counts, descriptive summaries | Check analytical grain and stage fields before calculating a funnel |
| Grouped checks | `.groupby().agg(...)`, including named aggregations | Reconcile overall and segmented counts |
| Missing and inconsistent values | explicit null and category checks | Surface source limitations before interpreting drop-off |
| Categorical and numerical relationships | grouped summaries and suitable plots | Test whether an observed pattern is stable enough to discuss |
| Date/time relationships | parsed timestamps, durations, date grouping | Investigate timing without silently changing the accepted snapshot |
| Exploration to action | observation → hypothesis → validation → bounded action | Keep findings separate from unsupported recommendations |

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

## Python Metrocar lookup

| Metrocar need | Course | Verified refresher chapter |
|---|---|---|
| Inspect DataFrame structure | Data Manipulation with pandas | Transforming DataFrames |
| Reduce repeated observations by entity | Data Manipulation with pandas | Aggregating DataFrames |
| Calculate grouped stage counts | Data Manipulation with pandas | Aggregating DataFrames |
| Preserve downloads without signup | Joining Data with pandas | Merging Tables With Different Join Types |
| Understand one-to-many relationships | Joining Data with pandas | Data Merging Basics |
| Validate merge cardinality or integrity | Joining Data with pandas | Advanced Merging and Concatenating |
| Inspect missing or inconsistent values | Exploratory Data Analysis in Python | Getting to Know a Dataset / Data Cleaning and Imputation |
| Investigate relationships before making a claim | Exploratory Data Analysis in Python | Relationships in Data |

## Maintenance note

Re-check DataCamp before using this map as evidence for a future change. If the catalog changes, update the verified identity here; do not reconstruct unseen chapters or lessons from memory.

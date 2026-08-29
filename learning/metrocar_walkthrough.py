# %% [markdown]
# # Metrocar Student Learning Walkthrough — Slice 1
#
# This walkthrough is a teaching reconstruction of Metrocar's **User Funnel**.
# It uses simple Pandas steps so that the analytical choices stay visible, then
# checks the result against the canonical production implementation.
#
# Run this file from the repository root with:
#
# ```bash
# .venv/bin/python learning/metrocar_walkthrough.py
# ```
#
# The walkthrough reads the configured database through `analysis.db`. It does
# not contain or print connection credentials.

# %% [markdown]
# ## 1. 🚕 What is Metrocar?
#
# Metrocar is a ride-hailing service. A potential customer first downloads the
# app, may create an account, may request one or more rides, and may complete a
# ride. That journey gives the business a funnel: a sequence of progressively
# stronger customer actions.
#
# Slice 1 studies only the entrant-level User Funnel:
#
# ```text
# Downloaded → Signed Up → Requested → Completed
# ```
#
# Transactions and reviews belong to the separate Ride Funnel and are not part
# of this teaching slice.

# %% [markdown]
# ## 2. 🎯 Business objective
#
# A funnel helps Metrocar see where potential customers stop progressing. The
# immediate objective is to build a trustworthy baseline at one compatible
# grain. Later slices can use that foundation to investigate conversion,
# segments, timing, and evidence-backed actions without mixing unlike units.
#
# The source snapshot is analyzed in full: there is no cohort start or end date.
# One shared source cutoff determines which source events were observable when
# the snapshot was measured.

# %% [markdown]
# ## 3. 💼 Approved business questions
#
# The complete project is governed by these nine questions:
#
# 1. Which funnel steps should Metrocar research and improve?
# 2. Are specific drop-off points preventing users from completing their first ride?
# 3. How does funnel performance differ across `ios`, `android`, and `web`?
# 4. Based on platform performance, where should Metrocar focus its marketing budget for the upcoming year?
# 5. Which age groups perform best at each funnel stage?
# 6. Which age group or groups most likely contain Metrocar's target customers?
# 7. How are ride requests distributed throughout the day, and what does that imply for a potential surge-pricing strategy?
# 8. Which part of the funnel has the lowest conversion rate?
# 9. What evidence-backed action could improve the lowest-converting part of the funnel?
#
# Slice 1 does not answer all nine. It establishes the analytical foundation
# needed to answer them reliably in later work.

# %% [markdown]
# ## 4. 🗂️ The three source tables
#
# Each table contributes a different part of the customer journey:
#
# - `app_downloads` supplies the download entrant and its `app_download_key`.
# - `signups` connects a download session to a registered `user_id`.
# - `ride_requests` records ride activity for a registered user.
#
# The relationship path is:
#
# ```text
# app_downloads.app_download_key
#              ↓
#       signups.session_id
#              ↓
#        signups.user_id
#              ↓
#    ride_requests.user_id
# ```

# %% [markdown]
# ## 5. 🧠 Analytical grain
#
# **Grain** means what one row represents. The governed User Funnel grain is one
# distinct `app_download_key`: one download entrant. It is not proof of one
# unique physical person.
#
# Ride requests have a different grain: one row represents one ride request, so
# the same `user_id` can appear many times. Joining those raw rows directly to
# entrants would duplicate some entrants and inflate the funnel. We first reduce
# ride activity to one pair of Boolean outcomes per user, then join those flags
# through the signup relationship.
#
# 🧠 Mental model:
#
# ```text
# many ride rows → one set of flags per user → one signup row → one entrant row
# ```
#
# Downloads without signup must stay in the base because they are a real first-
# stage drop-off, not missing data to discard.

# %% [markdown]
# ## 6. 🔍 Inspect the source structure
#
# 🎯 Goal: load only the three tables and columns needed for this slice, using
# the repository's read-only database access. We resolve the cutoff with the
# canonical implementation so the teaching and production calculations observe
# the same snapshot.
#
# Pandas and SQLAlchemy are third-party packages supplied by `.venv`. `analysis`
# is local Metrocar project code. Interactive execution may start without the
# repository root on Python's import path, so this setup locates that root and
# makes the local import explicit.

# %%
import sys
from pathlib import Path


candidate_roots = [Path.cwd(), *Path.cwd().parents]
if "__file__" in globals():
    walkthrough_directory = Path(__file__).resolve().parent
    candidate_roots.extend(
        [walkthrough_directory, *walkthrough_directory.parents]
    )

repository_root = next(
    (
        candidate
        for candidate in candidate_roots
        if (candidate / "analysis").is_dir()
        and (candidate / "METROCAR_PROJECT_EXECUTION_PLAN.md").is_file()
    ),
    None,
)
if repository_root is None:
    raise RuntimeError(
        "Could not locate the Metrocar repository root. In VS Code, open the "
        "Metrocar repository and run this cell from the repository root or "
        "the learning directory."
    )

available_import_roots = {
    Path(path_entry).resolve() if path_entry else Path.cwd()
    for path_entry in sys.path
}
if repository_root not in available_import_roots:
    sys.path.insert(0, str(repository_root))

import pandas as pd
from sqlalchemy import text

from analysis import funnel
from analysis.db import get_engine

# %%

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 120)

engine = get_engine()
parameters = funnel.resolve_parameters(engine)
source_cutoff = parameters.source_cutoff

assert parameters.cohort_start is None
assert parameters.cohort_end_exclusive is None

with engine.connect() as connection:
    app_downloads = pd.read_sql_query(
        text(
            """
            SELECT app_download_key, download_ts
            FROM app_downloads
            """
        ),
        connection,
    )
    signups = pd.read_sql_query(
        text(
            """
            SELECT user_id, session_id, signup_ts
            FROM signups
            """
        ),
        connection,
    )
    ride_requests = pd.read_sql_query(
        text(
            """
            SELECT ride_id, user_id, request_ts, dropoff_ts
            FROM ride_requests
            """
        ),
        connection,
    )

print(f"Canonical source cutoff: {source_cutoff}")
print("Cohort window: full snapshot (no cohort start or end)")

# %% [markdown]
# The canonical cutoff rule retains a source row when its governing timestamp is
# missing or no later than the shared cutoff. A completed ride additionally
# requires `dropoff_ts` to be present and observed by that same cutoff.

# %%
app_downloads["download_ts"] = pd.to_datetime(app_downloads["download_ts"])
signups["signup_ts"] = pd.to_datetime(signups["signup_ts"])
ride_requests["request_ts"] = pd.to_datetime(ride_requests["request_ts"])
ride_requests["dropoff_ts"] = pd.to_datetime(ride_requests["dropoff_ts"])

observed_downloads = app_downloads.loc[
    app_downloads["download_ts"].isna()
    | app_downloads["download_ts"].le(source_cutoff)
].copy()
observed_signups = signups.loc[
    signups["signup_ts"].isna() | signups["signup_ts"].le(source_cutoff)
].copy()
observed_rides = ride_requests.loc[
    ride_requests["request_ts"].isna()
    | ride_requests["request_ts"].le(source_cutoff)
].copy()

# %% [markdown]
# Before joining, compare rows with distinct identifiers. Equal download counts
# show that each accepted-snapshot download key is already one row. Equal signup
# counts show that each registered user is one row. Ride rows should outnumber
# distinct ride users because a user can request several rides.

# %%
source_structure = pd.DataFrame(
    [
        {
            "source": "app_downloads",
            "rows": len(observed_downloads),
            "identifier": "app_download_key",
            "distinct_identifiers": observed_downloads[
                "app_download_key"
            ].nunique(dropna=False),
        },
        {
            "source": "signups",
            "rows": len(observed_signups),
            "identifier": "user_id",
            "distinct_identifiers": observed_signups["user_id"].nunique(
                dropna=False
            ),
        },
        {
            "source": "ride_requests",
            "rows": len(observed_rides),
            "identifier": "user_id",
            "distinct_identifiers": observed_rides["user_id"].nunique(
                dropna=True
            ),
        },
    ]
)
source_structure["repeated_rows"] = (
    source_structure["rows"] - source_structure["distinct_identifiers"]
)
print("\nSource grain checks:")
print(source_structure.to_string(index=False))

assert observed_downloads["app_download_key"].notna().all()
assert observed_downloads["app_download_key"].is_unique
assert observed_signups["user_id"].notna().all()
assert observed_signups["user_id"].is_unique
assert observed_signups["session_id"].notna().all()
assert observed_signups["session_id"].is_unique
assert not observed_rides["user_id"].is_unique

# %% [markdown]
# Join coverage checks answer two preservation questions before we build the
# funnel. First, every observed signup should connect to a download. Second,
# every ride user should connect to a signup. We also count downloads with no
# signup; those entrants must survive the final LEFT JOIN.

# %%
download_keys = observed_downloads["app_download_key"]
signup_sessions = observed_signups["session_id"]
ride_user_ids = observed_rides["user_id"].dropna()
signup_user_ids = observed_signups["user_id"]

unmatched_signup_rows = int((~signup_sessions.isin(download_keys)).sum())
unmatched_ride_rows = int((~ride_user_ids.isin(signup_user_ids)).sum())
downloads_without_signup = int((~download_keys.isin(signup_sessions)).sum())

join_coverage = pd.Series(
    {
        "signup rows without a matching download": unmatched_signup_rows,
        "ride rows without a matching signup user": unmatched_ride_rows,
        "downloads without signup to preserve": downloads_without_signup,
    },
    name="rows",
)
print("\nJoin coverage and preservation checks:")
print(join_coverage.to_string())

assert unmatched_signup_rows == 0
assert unmatched_ride_rows == 0
assert downloads_without_signup > 0

# %% [markdown]
# ## 7. 💻 Build per-user ride flags
#
# 🎯 Goal: change ride-request grain into user grain before any entrant join.
# Each result row represents one registered user and answers two yes/no
# questions: did this user request at least one observed ride, and did this user
# complete at least one governed Finished ride?
#
# `Completed` means `dropoff_ts` is present and no later than the source cutoff.
# That is the governed Finished condition for this funnel.

# %%
ride_activity = observed_rides.loc[observed_rides["user_id"].notna()].copy()
ride_activity["requested"] = True
ride_activity["completed"] = (
    ride_activity["dropoff_ts"].notna()
    & ride_activity["dropoff_ts"].le(source_cutoff)
)

user_ride_flags = (
    ride_activity.groupby("user_id", as_index=False)
    .agg(
        requested=("requested", "any"),
        completed=("completed", "any"),
    )
)

assert user_ride_flags["user_id"].is_unique
assert not (user_ride_flags["completed"] & ~user_ride_flags["requested"]).any()

print("\nPer-user ride flags:")
print(user_ride_flags.head().to_string(index=False))
print(f"Rows after reducing ride activity to user grain: {len(user_ride_flags):,}")

# %% [markdown]
# ⚠️ Common trap: joining `ride_requests` directly would create one entrant copy
# per ride. `groupby(...).agg(any)` prevents frequent riders from increasing the
# number of funnel entrants.

# %% [markdown]
# ## 8. 🔗 Attach ride flags to signups
#
# The bridge from a signup to ride activity is `user_id`. A LEFT JOIN keeps all
# signups, including people with no ride. Missing ride flags therefore mean
# `False`, not an extra entrant. Each flag stays Boolean because the question is
# whether the user ever reached the stage, not how many rides they requested.

# %%
signup_teaching = observed_signups[["session_id", "user_id"]].merge(
    user_ride_flags,
    how="left",
    on="user_id",
    validate="one_to_one",
)
signup_teaching["requested"] = signup_teaching["requested"].eq(True)
signup_teaching["completed"] = signup_teaching["completed"].eq(True)

assert signup_teaching["session_id"].is_unique
assert not (signup_teaching["completed"] & ~signup_teaching["requested"]).any()

print("\nSignup-level teaching table:")
print(signup_teaching.head().to_string(index=False))

# %% [markdown]
# ## 9. 🔗 Build the entrant-level User Funnel base
#
# `app_downloads` is the left/base table because downloads define who entered
# this funnel. An INNER JOIN would delete every download without a signup and
# hide the first measured drop-off. The preserving LEFT JOIN keeps those rows
# and attaches later-stage evidence when it exists.
#
# The four Boolean stages must form this subset chain:
#
# ```text
# Completed ⊆ Requested ⊆ Signed Up ⊆ Downloaded
# ```

# %%
entrant_base = observed_downloads[["app_download_key"]].merge(
    signup_teaching,
    how="left",
    left_on="app_download_key",
    right_on="session_id",
    validate="one_to_one",
    indicator=True,
)

entrant_base["downloaded"] = True
entrant_base["signed_up"] = entrant_base["_merge"].eq("both")
entrant_base["requested"] = (
    entrant_base["signed_up"] & entrant_base["requested"].eq(True)
)
entrant_base["completed"] = (
    entrant_base["requested"] & entrant_base["completed"].eq(True)
)

entrant_base = entrant_base[
    [
        "app_download_key",
        "downloaded",
        "signed_up",
        "requested",
        "completed",
    ]
]

print("\nEntrant-level teaching base:")
print(entrant_base.head().to_string(index=False))

# %% [markdown]
# ## 10. 📊 Count the User Funnel stages
#
# Because every stage is Boolean at entrant grain, summing a stage column gives
# its entrant count. The calculation below derives the result from the teaching
# base; it does not hard-code expected production counts.

# %%
stage_order = [
    ("downloaded", "Downloaded"),
    ("signed_up", "Signed Up"),
    ("requested", "Requested"),
    ("completed", "Completed"),
]

teaching_user_counts = {
    stage_key: int(entrant_base[stage_key].sum())
    for stage_key, _ in stage_order
}

teaching_funnel = pd.DataFrame(
    [
        {
            "stage_order": order,
            "stage_key": stage_key,
            "stage_label": stage_label,
            "stage_count": teaching_user_counts[stage_key],
        }
        for order, (stage_key, stage_label) in enumerate(stage_order, start=1)
    ]
)

print("\nTeaching User Funnel:")
print(teaching_funnel.to_string(index=False))

# %% [markdown]
# ## 11. ✅ Validate the teaching reconstruction
#
# Validation connects technical checks to their business purpose:
#
# - grain preservation prevents double-counting entrants;
# - subset checks prove that nobody reaches a later stage without its
#   predecessor;
# - monotonicity confirms the ordered funnel never grows;
# - no-signup preservation proves first-stage drop-off remains measurable;
# - exact canonical reconciliation proves the simpler teaching path produces
#   the same governed result as production logic for this cutoff.

# %%
assert len(entrant_base) == len(observed_downloads)
assert entrant_base["app_download_key"].is_unique

assert not (entrant_base["signed_up"] & ~entrant_base["downloaded"]).any()
assert not (entrant_base["requested"] & ~entrant_base["signed_up"]).any()
assert not (entrant_base["completed"] & ~entrant_base["requested"]).any()

ordered_counts = [
    teaching_user_counts[stage_key] for stage_key, _ in stage_order
]
assert all(
    current_count <= previous_count
    for previous_count, current_count in zip(
        ordered_counts, ordered_counts[1:]
    )
)

preserved_no_signup = int((~entrant_base["signed_up"]).sum())
assert preserved_no_signup == downloads_without_signup

canonical_result = funnel.run_funnel_analysis(engine, parameters=parameters)
canonical_user_counts = {
    stage_key: int(canonical_result["user_counts"][stage_key])
    for stage_key, _ in stage_order
}

count_differences = {
    stage_key: {
        "teaching": teaching_user_counts[stage_key],
        "canonical": canonical_user_counts[stage_key],
    }
    for stage_key, _ in stage_order
    if teaching_user_counts[stage_key] != canonical_user_counts[stage_key]
}
if count_differences:
    raise AssertionError(
        "Teaching User Funnel does not reconcile with canonical output: "
        f"{count_differences}"
    )

reconciliation = teaching_funnel[["stage_order", "stage_label"]].copy()
reconciliation["teaching_count"] = [
    teaching_user_counts[stage_key] for stage_key, _ in stage_order
]
reconciliation["canonical_count"] = [
    canonical_user_counts[stage_key] for stage_key, _ in stage_order
]
reconciliation["exact_match"] = (
    reconciliation["teaching_count"] == reconciliation["canonical_count"]
)

print("\nExact teaching-to-canonical reconciliation:")
print(reconciliation.to_string(index=False))
print("\n✅ VERIFIED: the teaching User Funnel exactly matches canonical output.")

engine.dispose()

# %% [markdown]
# ## 12. 💡 Learning recap
#
# - **Why is grain the first major decision?** It determines what one row and
#   every count mean. A consistent entrant grain makes the stages comparable.
# - **Why aggregate rides before joining?** Users can request many rides. One
#   Boolean outcome per user prevents those repeated events from duplicating
#   entrants.
# - **Why anchor on downloads?** A download is the governed User Funnel entry,
#   so every measured entrant begins there.
# - **Why is LEFT JOIN required?** It preserves downloads that did not become
#   signups, making the first drop-off visible.
# - **What do the Boolean stages mean?** `downloaded` marks every entrant;
#   `signed_up` marks a connected signup; `requested` marks at least one observed
#   ride request; `completed` marks at least one Finished ride observed by the
#   cutoff.
# - **How did we prove the teaching calculation is trustworthy?** We checked
#   grain, subsets, monotonicity, and preservation, then required every teaching
#   count to equal `analysis.funnel.run_funnel_analysis()` exactly.

# %% [markdown]
# ## 13. 🎓 Interview self-test
#
# Try answering these without looking back:
#
# 1. What is the analytical grain of the User Funnel, and why?
# 2. Why can one `user_id` appear on many ride-request rows?
# 3. What error would occur if raw ride rows were joined directly to entrants?
# 4. What would an INNER JOIN incorrectly remove?
# 5. How is `Completed` defined at entrant grain?
# 6. What role does the source cutoff play in a full-snapshot analysis?
# 7. Which checks prove that the stage chain is internally valid?
# 8. How did you verify that the teaching implementation is trustworthy?

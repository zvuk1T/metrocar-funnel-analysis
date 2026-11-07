# %% [markdown]
# # Metrocar Funnel Analysis
#
# Metrocar is a ride-sharing platform that connects riders and drivers. This
# project analyzes Metrocar's customer funnel. Later, we will use evidence from
# the data to identify meaningful drop-offs and support recommendations.

# %% [markdown]
# ## 1. Access the source data
#
# 🎯 **Goal**
#
# Connect Python to the Metrocar PostgreSQL database and load the five source
# tables into pandas.
#
# 🧠 **Approach and WHY**
#
# SQLAlchemy creates the database engine that manages the connection from
# Python. psycopg is the PostgreSQL driver that SQLAlchemy uses underneath.
# pandas sends the SQL queries and stores each result as a DataFrame.
#
# The database URL stays in the local `METROCAR_DATABASE_URL` environment
# variable rather than in this source file. When the URL uses the general
# `postgresql://` prefix, we add `+psycopg` so SQLAlchemy uses the psycopg 3
# driver. The database transaction is set to read-only before any table is
# loaded.
#
# 📚 **DataCamp**
#
# [Introduction to Importing Data in Python](https://www.datacamp.com/courses/introduction-to-importing-data-in-python)
# → Working with relational databases in Python
#
# This is where database engines and loading relational data into pandas can be
# relearned.

# %%
import os

import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.getenv("METROCAR_DATABASE_URL")
if not database_url:
    raise RuntimeError("METROCAR_DATABASE_URL is not set.")

if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )

engine = create_engine(database_url)

# %%
with engine.connect() as connection:
    connection.execute(text("SET TRANSACTION READ ONLY"))

    app_downloads = pd.read_sql_query(
        text("SELECT * FROM app_downloads"),
        connection,
    )
    signups = pd.read_sql_query(
        text("SELECT * FROM signups"),
        connection,
    )
    ride_requests = pd.read_sql_query(
        text("SELECT * FROM ride_requests"),
        connection,
    )
    transactions = pd.read_sql_query(
        text("SELECT * FROM transactions"),
        connection,
    )
    reviews = pd.read_sql_query(
        text("SELECT * FROM reviews"),
        connection,
    )

# %% [markdown]
# `.shape` reports `(rows, columns)`, so these outputs confirm that each table
# was loaded without inspecting or interpreting its contents.

# %%
print("app_downloads:", app_downloads.shape)
print("signups:", signups.shape)
print("ride_requests:", ride_requests.shape)
print("transactions:", transactions.shape)
print("reviews:", reviews.shape)

# %% [markdown]
# ✅ **Result / Observation**
#
# The connection succeeded and the five source tables were loaded:
#
# - `app_downloads` → 23,608 rows / 3 columns
# - `signups` → 17,623 rows / 4 columns
# - `ride_requests` → 385,477 rows / 10 columns
# - `transactions` → 223,652 rows / 5 columns
# - `reviews` → 156,211 rows / 6 columns
#
# These counts confirm data availability; they are not funnel metrics.
#
# ### ✅ Notes for Students
#
# A successful database connection proves that we can access the data; it does
# not mean that we understand the data. Before calculating metrics, first
# understand what one row represents and how the tables relate.
#
# ➡️ **Next question**
#
# **What data do we actually have, and what does one row in each table
# represent?**

# %% [markdown]
# ## 2. Customer funnel
#
# 🎯 **Goal**
#
# Show how recorded downloads progress to signup, at least one ride request,
# and at least one completed ride.
#
# 🧠 **Approach and WHY**
#
# Keep downloads on the left so downloads without signup remain in the funnel.
# Each row represents one `app_download_key`, not a verified unique person.
# Use `isin()` to check whether a signup user appears among requesting or
# completing users. Repeated rides do not increase that user's stage count.
# A completed ride has a recorded `dropoff_ts`, as in the existing contract.
#
# 📚 **DataCamp:** Data Manipulation with pandas; Joining Data with pandas.

# %%
customer_funnel_base = app_downloads[["app_download_key"]].merge(
    signups[["session_id", "user_id"]],
    left_on="app_download_key",
    right_on="session_id",
    how="left",
    validate="one_to_one",
)

assert customer_funnel_base["app_download_key"].is_unique
assert len(customer_funnel_base) == len(app_downloads)

completed_rides = ride_requests.loc[ride_requests["dropoff_ts"].notna()]

customer_funnel_base["signed_up"] = customer_funnel_base["session_id"].notna()
customer_funnel_base["requested"] = (
    customer_funnel_base["signed_up"]
    & customer_funnel_base["user_id"].isin(ride_requests["user_id"].dropna())
)
customer_funnel_base["completed"] = (
    customer_funnel_base["requested"]
    & customer_funnel_base["user_id"].isin(completed_rides["user_id"].dropna())
)

customer_funnel = pd.DataFrame({
    "stage": ["Download", "Signup", "Requested ≥1", "Completed ≥1"],
    "count": [
        len(customer_funnel_base),
        int(customer_funnel_base["signed_up"].sum()),
        int(customer_funnel_base["requested"].sum()),
        int(customer_funnel_base["completed"].sum()),
    ],
})
customer_funnel

# %% [markdown]
# Plot the calculated counts in journey order. The figure displays the result;
# it does not perform another funnel calculation.
#
# 📚 **DataCamp:** Introduction to Data Visualization with Plotly in Python.

# %%
metrocar_customer_funnel = px.funnel(
    customer_funnel,
    x="count",
    y="stage",
    text="count",
    title="Metrocar Customer Funnel",
    color_discrete_sequence=["#636EFA"],
)
metrocar_customer_funnel.update_traces(
    texttemplate="%{value:,.0f}",
    textposition="inside",
)
metrocar_customer_funnel

# %% [markdown]
# ## 3. Ride funnel
#
# 🎯 **Goal**
#
# Show how individual ride requests progress to Finished, Paid, and Reviewed.
#
# 🧠 **Approach and WHY**
#
# This time one row is one `ride_id`. Finished requires a drop-off; Paid also
# requires an Approved payment; Reviewed also requires a review. Membership
# checks count a ride once even when it has several transactions or reviews.
# Reviews outside the Paid stage do not enter the strict funnel.
#
# 📚 **DataCamp:** Data Manipulation with pandas — filtering and membership.

# %%
approved_ride_ids = transactions.loc[
    transactions["charge_status"].eq("Approved"), "ride_id"
].dropna()
reviewed_ride_ids = reviews["ride_id"].dropna()

ride_funnel_base = ride_requests[["ride_id", "dropoff_ts"]].copy()
assert ride_funnel_base["ride_id"].notna().all()
assert ride_funnel_base["ride_id"].is_unique

ride_funnel_base["finished"] = ride_funnel_base["dropoff_ts"].notna()
ride_funnel_base["paid"] = (
    ride_funnel_base["finished"]
    & ride_funnel_base["ride_id"].isin(approved_ride_ids)
)
ride_funnel_base["reviewed"] = (
    ride_funnel_base["paid"]
    & ride_funnel_base["ride_id"].isin(reviewed_ride_ids)
)

ride_funnel = pd.DataFrame({
    "stage": ["Request", "Finished", "Paid", "Reviewed"],
    "count": [
        len(ride_funnel_base),
        int(ride_funnel_base["finished"].sum()),
        int(ride_funnel_base["paid"].sum()),
        int(ride_funnel_base["reviewed"].sum()),
    ],
})
ride_funnel

# %%
metrocar_ride_funnel = px.funnel(
    ride_funnel,
    x="count",
    y="stage",
    text="count",
    title="Metrocar Ride Funnel",
    color_discrete_sequence=["#636EFA"],
)
metrocar_ride_funnel.update_traces(
    texttemplate="%{value:,.0f}",
    textposition="inside",
)
metrocar_ride_funnel

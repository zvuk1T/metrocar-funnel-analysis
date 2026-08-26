"""Expected Metrocar schema, from Section 6.2 of the execution plan.

This is the single source of truth for what Phase 1 validates against. The
profiler compares the live database to these expectations and reports any
mismatch instead of failing silently.
"""

# Expected columns per table, in the order described by the plan.
EXPECTED_TABLES: dict[str, list[str]] = {
    "app_downloads": ["app_download_key", "platform", "download_ts"],
    "signups": ["user_id", "session_id", "signup_ts", "age_range"],
    "ride_requests": [
        "ride_id",
        "user_id",
        "driver_id",
        "request_ts",
        "accept_ts",
        "pickup_location",
        "destination_location",
        "pickup_ts",
        "dropoff_ts",
        "cancel_ts",
    ],
    "transactions": [
        "ride_id",
        "purchase_amount_usd",
        "charge_status",
        "transaction_ts",
    ],
    "reviews": ["review_id", "ride_id", "driver_id", "user_id", "rating", "free_response"],
}

# Columns that must be unique and non-null (candidate primary keys).
UNIQUE_KEYS: dict[str, str] = {
    "app_downloads": "app_download_key",
    "signups": "user_id",
    "ride_requests": "ride_id",
    "reviews": "review_id",
}

# Provisional relationships from Section 6.3 to validate.
# Each entry: (left_table, left_key, right_table, right_key, description).
PROVISIONAL_JOINS: list[tuple[str, str, str, str, str]] = [
    ("app_downloads", "app_download_key", "signups", "session_id",
     "each signup links to one app download"),
    ("signups", "user_id", "ride_requests", "user_id",
     "each ride request links to one signed-up user"),
    ("ride_requests", "ride_id", "transactions", "ride_id",
     "each transaction links to one ride"),
    ("ride_requests", "ride_id", "reviews", "ride_id",
     "each review links to one ride"),
]

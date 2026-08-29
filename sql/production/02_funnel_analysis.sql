-- Canonical Phase 2 funnel analysis.
--
-- Contract: docs/METRIC_DEFINITION_CONTRACT.md, especially Sections 2-12.
-- Parameters are source-local naive timestamps:
--   :cohort_start         inclusive entrant timestamp, nullable
--   :cohort_end_exclusive exclusive entrant timestamp, nullable
--   :source_cutoff        one shared observation cutoff for the run
--
-- Reconciliation loads the named statements in this file. Keep the
-- ``-- name`` / ``-- end`` markers stable. Repeated downstream activity is
-- reduced before preserving LEFT JOINs. Material source-cardinality anomalies
-- are reported separately by the ``source_validation`` statement.

-- name: source_cutoff
SELECT MAX(source_timestamp)::timestamp AS source_cutoff
FROM (
  SELECT MAX(download_ts) AS source_timestamp FROM app_downloads
  UNION ALL
  SELECT MAX(signup_ts) FROM signups
  UNION ALL
  SELECT MAX(request_ts) FROM ride_requests
  UNION ALL
  SELECT MAX(accept_ts) FROM ride_requests
  UNION ALL
  SELECT MAX(pickup_ts) FROM ride_requests
  UNION ALL
  SELECT MAX(dropoff_ts) FROM ride_requests
  UNION ALL
  SELECT MAX(cancel_ts) FROM ride_requests
  UNION ALL
  SELECT MAX(transaction_ts) FROM transactions
) observed_timestamps;
-- end

-- name: user_base
WITH ride_flags_by_user AS (
  SELECT
    user_id,
    TRUE AS requested,
    BOOL_OR(
      dropoff_ts IS NOT NULL
      AND dropoff_ts <= CAST(:source_cutoff AS timestamp)
    ) AS completed
  FROM ride_requests
  WHERE user_id IS NOT NULL
    AND (
      request_ts IS NULL
      OR request_ts <= CAST(:source_cutoff AS timestamp)
    )
  GROUP BY user_id
)
SELECT
  d.app_download_key,
  d.download_ts,
  d.platform,
  CASE
    WHEN s.session_id IS NULL THEN 'Not available — no signup'
    ELSE s.age_range
  END AS age_group,
  TRUE AS downloaded,
  (s.session_id IS NOT NULL) AS signed_up,
  (s.session_id IS NOT NULL AND COALESCE(r.requested, FALSE)) AS requested,
  (
    s.session_id IS NOT NULL
    AND COALESCE(r.requested, FALSE)
    AND COALESCE(r.completed, FALSE)
  ) AS completed,
  1::bigint AS download_row_count,
  (CASE WHEN s.session_id IS NULL THEN 0 ELSE 1 END)::bigint AS signup_count,
  (
    CASE
      WHEN s.session_id IS NOT NULL AND s.user_id IS NOT NULL THEN 1
      ELSE 0
    END
  )::bigint AS signup_user_count,
  FALSE AS download_ts_conflict,
  (d.download_ts IS NULL) AS download_ts_missing,
  FALSE AS platform_conflict,
  (d.platform IS NULL) AS platform_missing,
  (d.platform IS NOT NULL AND d.platform NOT IN ('ios', 'android', 'web'))
    AS platform_unexpected,
  (s.session_id IS NOT NULL AND s.user_id IS NULL) AS signup_user_missing,
  FALSE AS signup_user_conflict,
  (s.session_id IS NOT NULL AND s.age_range IS NULL) AS age_missing,
  FALSE AS age_conflict,
  (
    s.session_id IS NOT NULL
    AND s.age_range IS NOT NULL
    AND s.age_range NOT IN ('18-24', '25-34', '35-44', '45-54', 'Unknown')
  ) AS age_unexpected
FROM app_downloads d
LEFT JOIN signups s
  ON s.session_id = d.app_download_key
 AND (
   s.signup_ts IS NULL
   OR s.signup_ts <= CAST(:source_cutoff AS timestamp)
 )
LEFT JOIN ride_flags_by_user r ON r.user_id = s.user_id
WHERE (
        d.download_ts IS NULL
        OR d.download_ts <= CAST(:source_cutoff AS timestamp)
      )
  AND (
        CAST(:cohort_start AS timestamp) IS NULL
        OR d.download_ts >= CAST(:cohort_start AS timestamp)
      )
  AND (
        CAST(:cohort_end_exclusive AS timestamp) IS NULL
        OR d.download_ts < CAST(:cohort_end_exclusive AS timestamp)
      )
ORDER BY d.app_download_key;
-- end

-- name: ride_base
WITH download_by_key AS (
  SELECT
    app_download_key,
    CASE
      WHEN COUNT(DISTINCT platform) = 1
       AND COUNT(*) FILTER (WHERE platform IS NULL) = 0
      THEN MIN(platform)
      ELSE NULL
    END AS platform,
    (COUNT(DISTINCT platform) > 1) AS platform_conflict,
    BOOL_OR(platform IS NULL) AS platform_source_missing
  FROM app_downloads
  WHERE download_ts IS NULL
     OR download_ts <= CAST(:source_cutoff AS timestamp)
  GROUP BY app_download_key
),
observed_signups AS (
  SELECT user_id, session_id, age_range
  FROM signups
  WHERE signup_ts IS NULL
     OR signup_ts <= CAST(:source_cutoff AS timestamp)
),
signup_download_rows AS (
  SELECT
    s.user_id,
    s.session_id,
    s.age_range,
    d.app_download_key AS matched_download_key,
    d.platform,
    COALESCE(d.platform_conflict, FALSE) AS source_platform_conflict,
    COALESCE(d.platform_source_missing, FALSE) AS source_platform_missing
  FROM observed_signups s
  LEFT JOIN download_by_key d ON d.app_download_key = s.session_id
),
attribution_by_user AS (
  SELECT
    user_id,
    COUNT(*)::bigint AS signup_count,
    COUNT(DISTINCT session_id)::bigint AS signup_session_count,
    BOOL_OR(session_id IS NULL) AS signup_session_missing,
    BOOL_OR(matched_download_key IS NULL) AS download_missing,
    CASE
      WHEN COUNT(DISTINCT platform) = 1
       AND COUNT(*) FILTER (WHERE platform IS NULL) = 0
       AND NOT BOOL_OR(source_platform_conflict)
      THEN MIN(platform)
      ELSE NULL
    END AS platform,
    (
      COUNT(DISTINCT platform) > 1
      OR BOOL_OR(source_platform_conflict)
    ) AS platform_conflict,
    (
      BOOL_OR(platform IS NULL)
      OR BOOL_OR(source_platform_missing)
    ) AS platform_source_missing,
    CASE
      WHEN COUNT(DISTINCT age_range) = 1
       AND COUNT(*) FILTER (WHERE age_range IS NULL) = 0
      THEN MIN(age_range)
      ELSE NULL
    END AS age_range,
    BOOL_OR(age_range IS NULL) AS age_source_missing,
    (COUNT(DISTINCT age_range) > 1) AS age_conflict
  FROM signup_download_rows
  WHERE user_id IS NOT NULL
  GROUP BY user_id
),
ride_source AS (
  SELECT
    ride_id,
    COUNT(*)::bigint AS ride_row_count,
    CASE
      WHEN COUNT(DISTINCT user_id) = 1
       AND COUNT(*) FILTER (WHERE user_id IS NULL) = 0
      THEN MIN(user_id)
      ELSE NULL
    END AS user_id,
    (COUNT(DISTINCT user_id) > 1) AS ride_user_conflict,
    BOOL_OR(user_id IS NULL) AS ride_user_missing,
    MIN(request_ts) AS request_ts,
    (COUNT(DISTINCT request_ts) > 1) AS request_ts_conflict,
    BOOL_OR(request_ts IS NULL) AS request_ts_missing,
    MIN(accept_ts) AS accept_ts,
    MIN(pickup_ts) AS pickup_ts,
    MIN(dropoff_ts) AS dropoff_ts,
    MIN(cancel_ts) AS cancel_ts,
    TRUE AS requested,
    BOOL_OR(
      dropoff_ts IS NOT NULL
      AND dropoff_ts <= CAST(:source_cutoff AS timestamp)
    ) AS finished,
    BOOL_OR(
      accept_ts IS NOT NULL
      AND accept_ts <= CAST(:source_cutoff AS timestamp)
    ) AS accepted,
    BOOL_OR(
      accept_ts IS NOT NULL
      AND accept_ts <= CAST(:source_cutoff AS timestamp)
      AND cancel_ts IS NOT NULL
      AND cancel_ts <= CAST(:source_cutoff AS timestamp)
      AND cancel_ts >= accept_ts
    ) AS cancel_after_accept,
    BOOL_OR(dropoff_ts IS NOT NULL AND pickup_ts IS NULL)
      AS dropoff_without_pickup,
    BOOL_OR(pickup_ts IS NOT NULL AND accept_ts IS NULL)
      AS pickup_without_accept,
    BOOL_OR(dropoff_ts IS NOT NULL AND accept_ts IS NULL)
      AS dropoff_without_accept,
    BOOL_OR(cancel_ts IS NOT NULL AND pickup_ts IS NOT NULL)
      AS cancel_with_pickup,
    BOOL_OR(cancel_ts IS NOT NULL AND dropoff_ts IS NOT NULL)
      AS cancel_with_dropoff,
    BOOL_OR(
      accept_ts IS NOT NULL AND cancel_ts IS NOT NULL AND cancel_ts < accept_ts
    ) AS cancel_before_accept_anomaly,
    BOOL_OR(accept_ts < request_ts) AS accept_before_request,
    BOOL_OR(pickup_ts < accept_ts) AS pickup_before_accept,
    BOOL_OR(dropoff_ts < pickup_ts) AS dropoff_before_pickup
  FROM ride_requests
  WHERE request_ts IS NULL
     OR request_ts <= CAST(:source_cutoff AS timestamp)
  GROUP BY ride_id
),
transaction_by_ride AS (
  SELECT
    ride_id,
    COUNT(*)::bigint AS tx_count,
    COUNT(*) FILTER (WHERE charge_status = 'Approved')::bigint
      AS approved_count,
    BOOL_OR(charge_status = 'Approved') AS has_approved
  FROM transactions
  WHERE transaction_ts IS NULL
     OR transaction_ts <= CAST(:source_cutoff AS timestamp)
  GROUP BY ride_id
),
review_by_ride AS (
  SELECT ride_id, COUNT(*)::bigint AS review_count, TRUE AS has_review
  FROM reviews
  GROUP BY ride_id
),
ride_fact AS (
  SELECT
    r.*,
    a.signup_count,
    a.signup_session_count,
    a.signup_session_missing,
    a.download_missing,
    a.platform,
    a.platform_conflict,
    a.platform_source_missing,
    a.age_range,
    a.age_source_missing,
    a.age_conflict,
    COALESCE(t.tx_count, 0)::bigint AS tx_count,
    COALESCE(t.approved_count, 0)::bigint AS approved_count,
    COALESCE(t.has_approved, FALSE) AS has_approved,
    COALESCE(v.review_count, 0)::bigint AS review_count,
    COALESCE(v.has_review, FALSE) AS has_review
  FROM ride_source r
  LEFT JOIN attribution_by_user a ON a.user_id = r.user_id
  LEFT JOIN transaction_by_ride t ON t.ride_id = r.ride_id
  LEFT JOIN review_by_ride v ON v.ride_id = r.ride_id
),
cohort_base AS (
  SELECT
    ride_id,
    user_id,
    request_ts,
    accept_ts,
    pickup_ts,
    dropoff_ts,
    cancel_ts,
    platform,
    CASE
      WHEN ride_user_conflict THEN NULL
      WHEN signup_count IS NULL THEN 'Not available — no signup'
      ELSE age_range
    END AS age_group,
    requested,
    finished,
    (finished AND has_approved) AS paid,
    (finished AND has_approved AND has_review) AS reviewed,
    accepted,
    cancel_after_accept,
    has_approved,
    has_review,
    ride_row_count,
    COALESCE(signup_count, 0)::bigint AS signup_count,
    COALESCE(signup_session_count, 0)::bigint AS signup_session_count,
    tx_count,
    approved_count,
    review_count,
    ride_user_conflict,
    ride_user_missing,
    request_ts_conflict,
    request_ts_missing,
    (NOT ride_user_conflict AND signup_count IS NULL) AS signup_missing,
    COALESCE(signup_session_missing, FALSE) AS signup_session_missing,
    COALESCE(download_missing, signup_count IS NULL) AS download_missing,
    COALESCE(platform_conflict, FALSE) AS platform_conflict,
    (platform IS NULL OR COALESCE(platform_source_missing, FALSE))
      AS platform_missing,
    (platform IS NOT NULL AND platform NOT IN ('ios', 'android', 'web'))
      AS platform_unexpected,
    (
      signup_count IS NOT NULL
      AND (COALESCE(age_source_missing, FALSE) OR age_range IS NULL)
    ) AS age_missing,
    COALESCE(age_conflict, FALSE) AS age_conflict,
    (
      signup_count IS NOT NULL
      AND age_range IS NOT NULL
      AND age_range NOT IN ('18-24', '25-34', '35-44', '45-54', 'Unknown')
    ) AS age_unexpected,
    dropoff_without_pickup,
    pickup_without_accept,
    dropoff_without_accept,
    cancel_with_pickup,
    cancel_with_dropoff,
    cancel_before_accept_anomaly,
    accept_before_request,
    pickup_before_accept,
    dropoff_before_pickup
  FROM ride_fact
)
SELECT *
FROM cohort_base
WHERE (
        CAST(:cohort_start AS timestamp) IS NULL
        OR request_ts >= CAST(:cohort_start AS timestamp)
      )
  AND (
        CAST(:cohort_end_exclusive AS timestamp) IS NULL
        OR request_ts < CAST(:cohort_end_exclusive AS timestamp)
      )
ORDER BY ride_id;
-- end

-- name: source_validation
WITH downloads AS (
  SELECT app_download_key
  FROM app_downloads
  WHERE download_ts IS NULL
     OR download_ts <= CAST(:source_cutoff AS timestamp)
),
signups_observed AS (
  SELECT user_id, session_id
  FROM signups
  WHERE signup_ts IS NULL
     OR signup_ts <= CAST(:source_cutoff AS timestamp)
),
rides AS (
  SELECT ride_id, user_id
  FROM ride_requests
  WHERE request_ts IS NULL
     OR request_ts <= CAST(:source_cutoff AS timestamp)
),
transactions_observed AS (
  SELECT ride_id, charge_status
  FROM transactions
  WHERE transaction_ts IS NULL
     OR transaction_ts <= CAST(:source_cutoff AS timestamp)
),
download_keys AS (
  SELECT app_download_key FROM downloads GROUP BY app_download_key
),
signup_users AS (
  SELECT user_id FROM signups_observed WHERE user_id IS NOT NULL GROUP BY user_id
),
ride_ids AS (
  SELECT ride_id FROM rides GROUP BY ride_id
),
download_duplicates AS (
  SELECT app_download_key FROM downloads
  GROUP BY app_download_key HAVING COUNT(*) > 1
),
ride_duplicates AS (
  SELECT ride_id FROM rides GROUP BY ride_id HAVING COUNT(*) > 1
),
signup_session_duplicates AS (
  SELECT session_id FROM signups_observed WHERE session_id IS NOT NULL
  GROUP BY session_id HAVING COUNT(*) > 1
),
signup_session_user_conflicts AS (
  SELECT session_id FROM signups_observed WHERE session_id IS NOT NULL
  GROUP BY session_id HAVING COUNT(DISTINCT user_id) > 1
),
signup_user_duplicates AS (
  SELECT user_id FROM signups_observed WHERE user_id IS NOT NULL
  GROUP BY user_id HAVING COUNT(*) > 1
),
transaction_duplicates AS (
  SELECT ride_id FROM transactions_observed
  GROUP BY ride_id HAVING COUNT(*) > 1
),
approved_duplicates AS (
  SELECT ride_id FROM transactions_observed
  WHERE charge_status = 'Approved'
  GROUP BY ride_id HAVING COUNT(*) > 1
),
review_duplicates AS (
  SELECT ride_id FROM reviews GROUP BY ride_id HAVING COUNT(*) > 1
)
SELECT
  (SELECT COUNT(*) FROM download_duplicates)::bigint
    AS duplicate_app_download_keys,
  (SELECT COUNT(*) FROM ride_duplicates)::bigint AS duplicate_ride_ids,
  (SELECT COUNT(*) FROM signup_session_duplicates)::bigint
    AS signup_sessions_with_multiple_rows,
  (SELECT COUNT(*) FROM signup_session_user_conflicts)::bigint
    AS signup_sessions_with_multiple_users,
  (SELECT COUNT(*) FROM signup_user_duplicates)::bigint
    AS signup_users_with_multiple_rows,
  (SELECT COUNT(*) FROM transaction_duplicates)::bigint
    AS rides_with_multiple_transactions,
  (SELECT COUNT(*) FROM approved_duplicates)::bigint
    AS rides_with_multiple_approved,
  (SELECT COUNT(*) FROM review_duplicates)::bigint
    AS rides_with_multiple_reviews,
  (
    SELECT COUNT(*) FROM signups_observed s
    LEFT JOIN download_keys d ON d.app_download_key = s.session_id
    WHERE d.app_download_key IS NULL
  )::bigint AS unmatched_signup_rows,
  (
    SELECT COUNT(*) FROM rides r
    LEFT JOIN signup_users s ON s.user_id = r.user_id
    WHERE s.user_id IS NULL
  )::bigint AS unmatched_ride_rows,
  (
    SELECT COUNT(*) FROM transactions_observed t
    LEFT JOIN ride_ids r ON r.ride_id = t.ride_id
    WHERE r.ride_id IS NULL
  )::bigint AS unmatched_transaction_rows,
  (
    SELECT COUNT(*) FROM reviews v
    LEFT JOIN ride_ids r ON r.ride_id = v.ride_id
    WHERE r.ride_id IS NULL
  )::bigint AS unmatched_review_rows;
-- end

-- Canonical Phase 3 business-insight cross-checks.
--
-- Contract: docs/METRIC_DEFINITION_CONTRACT.md, especially Sections 6-10.
-- This file does not rebuild either Phase 2 funnel. Its bounded purpose is an
-- independent registered-user first-ride diagnostic. Equal earliest request
-- timestamps remain ambiguous; ride_id is never used as a tie-break.
--
-- Parameters use the accepted Phase 2 conventions:
--   :cohort_start         inclusive ride-entry timestamp, nullable
--   :cohort_end_exclusive exclusive ride-entry timestamp, nullable
--   :source_cutoff        shared source observation cutoff

-- name: first_ride_diagnostic
WITH observed_signup_users AS (
  SELECT DISTINCT user_id
  FROM signups
  WHERE user_id IS NOT NULL
    AND (
      signup_ts IS NULL
      OR signup_ts <= CAST(:source_cutoff AS timestamp)
    )
),
ride_by_id AS (
  SELECT
    ride_id,
    CASE
      WHEN COUNT(DISTINCT user_id) = 1
       AND COUNT(*) FILTER (WHERE user_id IS NULL) = 0
      THEN MIN(user_id)
      ELSE NULL
    END AS user_id,
    MIN(request_ts) AS request_ts,
    BOOL_OR(request_ts IS NULL) AS request_ts_missing,
    (COUNT(DISTINCT request_ts) > 1) AS request_ts_conflict,
    BOOL_OR(
      accept_ts IS NOT NULL
      AND accept_ts <= CAST(:source_cutoff AS timestamp)
    ) AS accepted,
    BOOL_OR(
      pickup_ts IS NOT NULL
      AND pickup_ts <= CAST(:source_cutoff AS timestamp)
    ) AS picked_up,
    BOOL_OR(
      dropoff_ts IS NOT NULL
      AND dropoff_ts <= CAST(:source_cutoff AS timestamp)
    ) AS finished,
    BOOL_OR(
      cancel_ts IS NOT NULL
      AND cancel_ts <= CAST(:source_cutoff AS timestamp)
    ) AS cancellation_observed,
    BOOL_OR(
      accept_ts IS NOT NULL
      AND accept_ts <= CAST(:source_cutoff AS timestamp)
      AND cancel_ts IS NOT NULL
      AND cancel_ts <= CAST(:source_cutoff AS timestamp)
      AND cancel_ts >= accept_ts
    ) AS cancel_after_accept
  FROM ride_requests
  WHERE request_ts IS NULL
     OR request_ts <= CAST(:source_cutoff AS timestamp)
  GROUP BY ride_id
),
ride_cohort AS (
  SELECT *
  FROM ride_by_id
  WHERE (
          CAST(:cohort_start AS timestamp) IS NULL
          OR request_ts >= CAST(:cohort_start AS timestamp)
        )
    AND (
          CAST(:cohort_end_exclusive AS timestamp) IS NULL
          OR request_ts < CAST(:cohort_end_exclusive AS timestamp)
        )
),
registered_rides AS (
  SELECT r.*
  FROM ride_cohort r
  JOIN observed_signup_users s ON s.user_id = r.user_id
),
user_checks AS (
  SELECT
    user_id,
    BOOL_OR(request_ts_missing) AS missing_request_ts,
    BOOL_OR(request_ts_conflict) AS conflicting_request_ts,
    MIN(request_ts) AS earliest_request_ts,
    BOOL_OR(finished) AS ever_finished
  FROM registered_rides
  GROUP BY user_id
),
earliest_candidates AS (
  SELECT
    r.user_id,
    COUNT(*)::bigint AS earliest_candidate_count
  FROM registered_rides r
  JOIN user_checks u
    ON u.user_id = r.user_id
   AND r.request_ts = u.earliest_request_ts
  GROUP BY r.user_id
),
user_diagnostic AS (
  SELECT
    u.*,
    COALESCE(e.earliest_candidate_count, 0)::bigint
      AS earliest_candidate_count,
    (
      u.missing_request_ts
      OR u.conflicting_request_ts
      OR COALESCE(e.earliest_candidate_count, 0) > 1
    ) AS ambiguous
  FROM user_checks u
  LEFT JOIN earliest_candidates e ON e.user_id = u.user_id
),
selected_first_rides AS (
  SELECT
    r.*,
    u.ever_finished
  FROM registered_rides r
  JOIN user_diagnostic u
    ON u.user_id = r.user_id
   AND NOT u.ambiguous
   AND r.request_ts = u.earliest_request_ts
)
SELECT
  (SELECT COUNT(*) FROM user_diagnostic)::bigint
    AS registered_users_with_request,
  (
    SELECT COUNT(*) FROM user_diagnostic WHERE missing_request_ts
  )::bigint AS users_with_missing_request_ts,
  (
    SELECT COUNT(*) FROM user_diagnostic WHERE conflicting_request_ts
  )::bigint AS users_with_conflicting_request_ts,
  (
    SELECT COUNT(*) FROM user_diagnostic WHERE earliest_candidate_count > 1
  )::bigint AS users_with_earliest_tie,
  (
    SELECT COUNT(*) FROM user_diagnostic WHERE ambiguous
  )::bigint AS ambiguous_users,
  (
    SELECT COUNT(*) FROM user_diagnostic WHERE NOT ambiguous
  )::bigint AS unambiguous_users,
  (SELECT COUNT(*) FROM selected_first_rides)::bigint
    AS selected_first_rides,
  (SELECT COUNT(*) FROM selected_first_rides)::bigint
    AS requested_first_rides,
  (
    SELECT COUNT(*) FROM selected_first_rides WHERE accepted
  )::bigint AS accepted_first_rides,
  (
    SELECT COUNT(*) FROM selected_first_rides WHERE picked_up
  )::bigint AS picked_up_first_rides,
  (
    SELECT COUNT(*) FROM selected_first_rides WHERE finished
  )::bigint AS finished_first_rides,
  (
    SELECT COUNT(*) FROM selected_first_rides WHERE cancellation_observed
  )::bigint AS any_cancellation_evidence,
  (
    SELECT COUNT(*) FROM selected_first_rides WHERE cancel_after_accept
  )::bigint AS cancel_after_accept_first_rides,
  (
    SELECT COUNT(*)
    FROM selected_first_rides
    WHERE cancellation_observed AND NOT accepted
  )::bigint AS cancelled_without_recorded_acceptance,
  (
    SELECT COUNT(*)
    FROM selected_first_rides
    WHERE NOT finished AND ever_finished
  )::bigint AS first_unfinished_but_later_finished;
-- end

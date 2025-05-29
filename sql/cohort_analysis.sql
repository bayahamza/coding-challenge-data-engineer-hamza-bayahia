WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', signup_date) AS cohort_month
  FROM users
),
user_activity AS (
  SELECT
    e.user_id,
    DATE_TRUNC('week', e.timestamp) AS activity_week
  FROM events e
  JOIN cohorts c ON e.user_id = c.user_id
),
cohort_retention AS (
  SELECT
    c.cohort_month,
    ua.activity_week,
    COUNT(DISTINCT ua.user_id) AS retained_users,
    EXTRACT(WEEK FROM ua.activity_week) - EXTRACT(WEEK FROM c.cohort_month) AS week_number
  FROM cohorts c
  JOIN user_activity ua ON c.user_id = ua.user_id
  WHERE EXTRACT(WEEK FROM ua.activity_week) - EXTRACT(WEEK FROM c.cohort_month) BETWEEN 0 AND 7
  GROUP BY 1, 2, 4
)
SELECT *
FROM cohort_retention
ORDER BY cohort_month, week_number;

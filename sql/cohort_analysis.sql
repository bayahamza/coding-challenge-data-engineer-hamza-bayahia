WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', signup_date) AS cohort_month,
    signup_date
  FROM users
),
user_activity AS (
  SELECT
    e.user_id,
    e.timestamp AS activity_date
  FROM events e
),
retention_data AS (
  SELECT
    c.cohort_month,
    DATE_TRUNC('week', ua.activity_date) AS activity_week,
    COUNT(DISTINCT ua.user_id) AS retained_users,
    FLOOR(EXTRACT(DAY FROM ua.activity_date - c.signup_date) / 7) AS week_number
  FROM cohorts c
  JOIN user_activity ua ON c.user_id = ua.user_id
  WHERE ua.activity_date >= c.signup_date
    AND FLOOR(EXTRACT(DAY FROM ua.activity_date - c.signup_date) / 7) BETWEEN 0 AND 7
  GROUP BY 1, 2, 4
)
SELECT *
FROM retention_data
ORDER BY cohort_month, week_number;

SELECT
  DATE_TRUNC('week', timestamp) AS week,
  COUNT(DISTINCT user_id) AS weekly_active_users
FROM events
GROUP BY 1
ORDER BY 1;

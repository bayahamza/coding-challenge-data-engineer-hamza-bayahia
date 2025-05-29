# Data Engineer Challenge – Strategy Summary

## Part I – Data Exploration & SQL Optimization

### 1. Objective
Analyze user behavior from an e-commerce PostgreSQL database to compute:
- Weekly active users (WAU)
- Revenue per product category

### 2. Dataset & Setup
- Created 3 tables: `users`, `products`, `events`
- Inserted:
  - 1,000 users over 12 months
  - 20 products across 5 categories
  - 50,000 user events (viewed, add-to-cart, purchased)

### 3. Queries & Benchmarks

#### 📘 Weekly Active Users

```sql
SELECT
  DATE_TRUNC('week', timestamp) AS week,
  COUNT(DISTINCT user_id) AS weekly_active_users
FROM events
GROUP BY 1
ORDER BY 1;

Time: ~0.053 sec
Result: 53 rows


Revenue by Category

SELECT
  p.category,
  SUM(p.price) AS total_revenue
FROM events e
JOIN products p ON e.product_id = p.product_id
WHERE e.event_type = 'purchased'
GROUP BY p.category
ORDER BY total_revenue DESC;

Time: ~0.012 sec
Result: 5 rows

Optimizations

CREATE INDEX idx_events_user_time ON events(user_id, timestamp);
CREATE INDEX idx_events_product_type ON events(product_id, event_type);
CREATE INDEX idx_products_category ON products(category);

Post-optimization performance:
WAU: ~0.043 sec
Revenue: ~0.010 sec


---

##  Part II – Cohort Analysis (User Retention)

### 1. Objective
Track weekly retention of users grouped by their signup month (cohort analysis).

### 2. Approach
- Users grouped by `DATE_TRUNC('month', signup_date)`
- Events tracked weekly up to 8 weeks post-signup
- Data pivoted into a retention matrix
- Visualized with Seaborn heatmap

### 3. SQL Query

```sql
WITH cohorts AS (
  SELECT user_id, DATE_TRUNC('month', signup_date) AS cohort_month
  FROM users
),
user_activity AS (
  SELECT e.user_id, DATE_TRUNC('week', e.timestamp) AS activity_week
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
ORDER BY cohort_month, week_number;```

Result (Heatmap)

---

##  Part III – Behavioral Segmentation with AI & Elasticsearch

### 1. Objective
Cluster users based on their search behavior to identify intent-driven segments.

### 2. Data Source
Logs retrieved from Elasticsearch `user_logs` index. Each document contains:
- `user_id`
- `search_query`
- `clicked_product_ids`
- `timestamp`

### 3. AI & Clustering Pipeline

- Search queries vectorized using HuggingFace `sentence-transformers` (MiniLM-L6-v2)
- Vectors clustered via `KMeans` into 4 user types:
  - `tech_enthusiast`
  - `lifestyle_shopper`
  - `fitness_focused`
  - `bargain_hunter`
- Clusters assigned back into Elasticsearch using the `_update` API

### 4. Example Document

```json
{
  "user_id": "abc123",
  "search_query": "wireless headphones",
  "clicked_product_ids": ["p01", "p02"],
  "timestamp": "2025-04-01T12:30:00Z",
  "segment": "tech_enthusiast"
}

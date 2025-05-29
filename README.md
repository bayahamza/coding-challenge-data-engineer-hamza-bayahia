#  YouCan – Data Engineer Challenge

This project is a full data engineering pipeline built for an e-commerce platform, including:

- SQL performance optimization
- User retention cohort analysis
- AI-powered behavioral segmentation via Elasticsearch

---

##  Challenge Breakdown

### Part I – SQL Query Optimization

- PostgreSQL database with `users`, `products`, and `events`
- Optimized queries:
  - Weekly active users
  - Revenue per category
- Indexed critical fields to improve performance
- Benchmarked using Python

### Part II – Cohort Retention Analysis

- Grouped users by signup month
- Calculated retention week by week (8 weeks)
- Visualized with a heatmap via Seaborn

### Part III – AI + Segmentation with Elasticsearch

- Search logs stored in Elasticsearch
- Queries embedded using `sentence-transformers`
- KMeans clustering into 4 user segments
- Updated documents with `"segment": ...` field

---

##  Project Structure
coding-challenge-data-engineer-hamza-bayahia/
├── docker-compose.yml
├── notebooks/
│ └── cohort_analysis.ipynb
├── scripts/
│ ├── create_tables.py
│ ├── insert_data.py
│ ├── insert_logs.py
│ ├── benchmark.py
│ ├── optimize_sql.py
│ └── segmentation.py
├── sql/
│ ├── weekly_active_users.sql
│ ├── revenue_per_category.sql
│ ├── add_indexes.sql
│ └── cohort_analysis.sql
├── doc/
│ └── strategy_summary.md


---


## Run

1. Launch environment:
```bash
docker compose up -d

## Run SQL scripts from Python:
python scripts/create_tables.py
python scripts/insert_data.py
python scripts/benchmark.py

## Run Cohort analysis:

jupyter notebook notebooks/cohort_analysis.ipynb

## Run AI segmentation:

python scripts/insert_logs.py
python scripts/segmentation.py


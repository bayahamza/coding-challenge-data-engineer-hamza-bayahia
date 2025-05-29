from faker import Faker
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import random

es = Elasticsearch("http://localhost:9200")

if not es.indices.exists(index="user_logs"):
    es.indices.create(index="user_logs")

faker = Faker()
product_keywords = [
    "wireless headphones", "gaming laptop", "organic shampoo", "running shoes",
    "yoga mat", "usb charger", "led lamp", "iphone case", "winter jacket", "smartwatch"
]

for _ in range(1000):
    doc = {
        "user_id": faker.uuid4(),
        "search_query": random.choice(product_keywords),
        "clicked_product_ids": [f"p{random.randint(1, 20)}" for _ in range(random.randint(1, 3))],
        "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
    }
    es.index(index="user_logs", body=doc)

print("✅ 1000 logs utilisateurs insérés dans l'index 'user_logs'.")

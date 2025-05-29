from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from tqdm import tqdm

import numpy as np

es = Elasticsearch("http://localhost:9200")

query = {
    "size": 1000,
    "_source": ["user_id", "search_query"],
    "query": {"match_all": {}}
}
res = es.search(index="user_logs", body=query, scroll="2m")

docs = res['hits']['hits']
user_ids = [doc['_source']['user_id'] for doc in docs]
queries = [doc['_source']['search_query'] for doc in docs]

model = SentenceTransformer('all-MiniLM-L6-v2')
vectors = model.encode(queries)

n_clusters = 4
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
labels = kmeans.fit_predict(vectors)

segment_names = {
    0: "tech_enthusiast",
    1: "lifestyle_shopper",
    2: "fitness_focused",
    3: "bargain_hunter"
}

print("🔄 Mise à jour des documents avec les segments...")

for i, doc_id in enumerate([doc['_id'] for doc in docs]):
    segment = segment_names[labels[i]]
    es.update(index="user_logs", id=doc_id, body={
        "doc": {"segment": segment}
    })

print("✅ Segmentation terminée et index mise à jour.")

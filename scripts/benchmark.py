import psycopg2
import time

conn = psycopg2.connect(
    dbname="youcan",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def load_query(path):
    with open(path, 'r') as file:
        return file.read()

def benchmark_query(name, query):
    print(f"\n▶️ Exécution de la requête : {name}")
    start = time.time()
    cur.execute(query)
    rows = cur.fetchall()
    end = time.time()
    print(f"⏱️ Temps d'exécution : {round(end - start, 4)} secondes")
    print(f"🔢 Résultat : {len(rows)} lignes")

queries = {
    "Weekly Active Users": load_query("sql/weekly_active_users.sql"),
    "Revenue by Category": load_query("sql/revenue_per_category.sql")
}


for name, query in queries.items():
    benchmark_query(name, query)

cur.close()
conn.close()

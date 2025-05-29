import psycopg2

conn = psycopg2.connect(
    dbname="youcan",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

with open("sql/add_indexes.sql", 'r') as f:
    cur.execute(f.read())

conn.commit()
cur.close()
conn.close()

print("✅ Index SQL créés avec succès.")

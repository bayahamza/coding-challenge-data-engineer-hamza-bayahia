import psycopg2

conn = psycopg2.connect(
    dbname="youcan",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    signup_date DATE NOT NULL,
    country VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(100),
    price DECIMAL NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    event_type VARCHAR(50) CHECK (event_type IN ('viewed', 'add-to-cart', 'purchased')),
    product_id INT REFERENCES products(product_id),
    timestamp TIMESTAMP NOT NULL
);
""")

conn.commit()
cur.close()
conn.close()
print("✅ Tables PostgreSQL créées avec succès.")

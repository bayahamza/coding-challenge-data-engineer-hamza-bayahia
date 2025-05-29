import psycopg2
import random
from datetime import datetime, timedelta
from faker import Faker

conn = psycopg2.connect(
    dbname="youcan",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
faker = Faker()

NUM_USERS = 1000
NUM_PRODUCTS = 20
NUM_EVENTS = 50000

countries = ['Morocco', 'France', 'USA', 'Germany', 'Spain']

categories = ['electronics', 'fashion', 'home', 'toys', 'books']

def random_date_last_year():
    start_date = datetime.now() - timedelta(days=365)
    return start_date + timedelta(days=random.randint(0, 365))

print("Insertion des utilisateurs...")
for _ in range(NUM_USERS):
    signup = random_date_last_year()
    country = random.choice(countries)
    cur.execute("INSERT INTO users (signup_date, country) VALUES (%s, %s)", (signup.date(), country))

print("Insertion des produits...")
for _ in range(NUM_PRODUCTS):
    category = random.choice(categories)
    price = round(random.uniform(5.0, 300.0), 2)
    cur.execute("INSERT INTO products (category, price) VALUES (%s, %s)", (category, price))

print("Insertion des événements...")
event_types = ['viewed', 'add-to-cart', 'purchased']
for _ in range(NUM_EVENTS):
    user_id = random.randint(1, NUM_USERS)
    product_id = random.randint(1, NUM_PRODUCTS)
    event_type = random.choice(event_types)
    timestamp = random_date_last_year()
    cur.execute("""
        INSERT INTO events (user_id, event_type, product_id, timestamp)
        VALUES (%s, %s, %s, %s)
    """, (user_id, event_type, product_id, timestamp))

conn.commit()
cur.close()
conn.close()
print("✅ Données insérées avec succès.")
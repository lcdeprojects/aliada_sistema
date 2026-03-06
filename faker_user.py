from faker import Faker
import sqlite3
from datetime import datetime

# Register custom datetime adapter to suppress deprecation warning
def adapt_datetime_iso(val):
    return val.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime_iso)

fake = Faker('pt_BR')
Faker.seed(42) 

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

total_registros = 30
data = []

for i in range(total_registros):
    data.append({
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'age': fake.random_int(min=18, max=80),
        'phone': fake.phone_number(),
        'height': fake.random_int(min=150, max=200),
        'weight': fake.random_int(min=50, max=100),
        'created_at': fake.date_time_this_year(),
        'updated_at': fake.date_time_this_year(),
    })

print(f"Inserting {len(data)} patients...")

cursor.executemany("""
INSERT INTO aliada_patientrecord (first_name, last_name, email, age, phone, height, weight, created_at, updated_at)
VALUES (:first_name, :last_name, :email, :age, :phone, :height, :weight, :created_at, :updated_at)
""", data)

conn.commit()
cursor.close()
conn.close()

print("Done.")



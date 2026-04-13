import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bank.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
""")

# Insert demo user
cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
               ("ravi@bank.com", "password123"))

conn.commit()
conn.close()

print("✅ Database seeded successfully!")
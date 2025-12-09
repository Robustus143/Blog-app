import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%blog%'")
tables = cursor.fetchall()
print("Blog-related tables:")
for table in tables:
    print(f"  - {table[0]}")
conn.close()

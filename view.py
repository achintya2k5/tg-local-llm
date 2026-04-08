import sqlite3

conn = sqlite3.connect("messages_tele.db")
c = conn.cursor()

# List all tables
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()
print("Tables:", tables)

# For each table, print first 5 rows
for (table_name,) in tables:
    print(f"\nData in {table_name}:")
    c.execute(f"SELECT * FROM {table_name} LIMIT 100;")
    rows = c.fetchall()
    for row in rows:
        print(row)

conn.close()
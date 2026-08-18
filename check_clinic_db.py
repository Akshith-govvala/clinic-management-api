import sqlite3

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
tables = cursor.fetchall()
print("Tables in clinic.db:", tables)

# Check if tables have data
for table in ["patients", "doctors", "appointments"]:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Records in {table}: {count}")
    except sqlite3.Error as e:
        print(f"Table {table} does not exist in clinic.db: {e}")

conn.close()

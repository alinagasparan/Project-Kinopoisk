from db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM actor LIMIT 5;")
print(cur.fetchall())

cur.close()
conn.close()
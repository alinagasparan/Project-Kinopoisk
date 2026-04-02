import db
from db import user_register

conn = db.get_connection()
cur = conn.cursor()

#cur.execute("SELECT * FROM film LIMIT 5;")
print(db.get_count(conn, "film"))

cur.close()
conn.close()
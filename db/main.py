import db

conn = db.get_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM movies LIMIT 5;")
print(cur.fetchall())
print(db.get_count(conn, "movies"))
cur.execute("SELECT title FROM public.movies WHERE movie_id=133")
print(cur.fetchall())
print(db.user_register(conn, "user1", "123"))
print(db.user_register(conn, "user2", "123"))
print(db.add_film_to_list(conn, 2, 133, "1"))

print(db.add_film_to_list(conn, 2, 384, "1"))
print(db.get_film_info(conn, "133"))

print(db.get_users_profile(conn, "2"))
print(db.change_users_profile(conn, 2, avatar_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYwXnoBB-1rPdF2psD03z5MmPFwfES03F9ew&s"))
print(db.write_comment_on_film(conn, 2, 384, "i liked it"))

print(db.user_login(conn, "user2", "123"))
cur.close()
conn.close()
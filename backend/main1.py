import sys
import os
sys.path.append(os.path.dirname(__file__))

import db
def get_films_by_search(text):
    conn = db.get_connection()
    try:
        if not text or text.strip() == "":
            return []

        films = db.search_film_by_name(conn, text)

        result = []
        for film in films:
            info = db.get_film_info(conn, film["movie_id"])

            result.append({
                "id": film["movie_id"],
                "title": film["title"],
                "poster_link": info["poster_link"] if info else "",
                "description": info["description"] if info else "",
                "year": info["release_year"] if info else None
            })

        return result

    finally:
        conn.close()

def register_user(user_name, user_password, avatar_url=None):
    conn = db.get_connection()
    try:
        user_id = db.user_register(conn, user_name, user_password, avatar_url)

        return {
            "id": user_id,
            "username": user_name
        }

    finally:
        conn.close()

def check_user_login(username, password):
    conn = db.get_connection()
    try:
        user_id = db.user_login(conn, username, password)
        if user_id:
            return {
                "username": username,
                "id": user_id
            }
        else:
            return None
    finally:
        conn.close()

def get_films_by_genre(genre_name):
    conn = db.get_connection()
    try:
        return db.search_film_with_filters()
    finally:
        conn.close()

def get_films_with_filters(title=None, genre=None, actor=None, year=None, sort_by=None, sort_order="asc"):
    conn = db.get_connection()
    try:
        return db.search_film_with_filters(conn, title=title, genre=genre, actor=actor, year=year, sort_by=sort_by, sort_order=sort_order)
    finally:
        conn.close()
def get_user_profile(user_id):
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, user_name, avatar_url FROM users_schema.users WHERE id=%s",
                (user_id,)
            )
            user = cur.fetchone()

        if not user:
            return None
        seen_films = db.get_films_from_users_list(conn, user_id, 3)   # просмотрено
        planned_films = db.get_films_from_users_list(conn, user_id, 1)  # запланировано

        return {
            "id": user[0],
            "username": user[1],
            "avatar": user[2],

            "seen": seen_films,
            "planned": planned_films
        }

    finally:
        conn.close()
def change_user_avatar(user_id, avatar_url):
    conn = db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users_schema.users
                SET avatar_url = %s
                WHERE id = %s;
            """, (avatar_url, user_id))
            conn.commit()
        user_profile = db.get_users_profile(conn, user_id)
        if user_profile:
            return user_profile['avatar_url']
        return None
    finally:
        conn.close()
def update_user_profile(user_id, username=None, password=None, avatar=None):
    conn = db.get_connection()
    try:
        user = db.change_users_profile(
            conn,
            user_id,
            user_name=username,
            user_password=password,
            avatar_url=avatar
        )

        if user:
            return {
                "id": user[0],
                "username": user[1],
                "avatar": user[2]
            }

        return None

    finally:
        conn.close()
def get_all_movies_with_details():
    conn = db.get_connection()
    films_basic = db.get_all_films(conn)
    all_movies = []

    with conn.cursor(cursor_factory=db.RealDictCursor) as cur:
        for film in films_basic:
            movie_id = film['movie_id']
            query = """SELECT movie_id, title, poster_link, release_year
                       FROM public.movies
                       WHERE movie_id = %s;"""
            cur.execute(query, (movie_id,))
            movie = cur.fetchone()
            if movie:
                all_movies.append(movie)

    return all_movies

def add_movie_to_user_list(user_id, movie_id, status):
    conn = db.get_connection()
    try:
        status_map = {
            "seen": 3,
            "planned": 1
        }
        status_id = status_map.get(status)

        if status_id is None:
            raise ValueError("Неверный статус")

        return db.add_film_to_list(conn, user_id, movie_id, status_id)

    finally:
        conn.close()
from ml import search_movies

def chat_with_ml(message):
   
    if not message or message.strip() == "":
        return []

    try:
        results = search_movies(message, top_k=10)
        
        response = []
        for film in results:
            response.append({
                "title": film["title"],
                "year": film["year"],
                "genre": film["genre"],
                "rating": film["rating"],
                "overview": film["overview"]
            })

        return response

    except Exception as e:
        return [{"error": str(e)}]
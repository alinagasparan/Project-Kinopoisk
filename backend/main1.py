import sys
import os
sys.path.append(os.path.dirname(__file__))
import ml.ml
import database.db
def get_films_by_search(text):
    conn = database.db.get_connection()
    try:
        if not text or text.strip() == "":
            return []

        films = database.db.search_film_by_name(conn, text)

        result = []
        for film in films:
            info = database.db.get_film_info(conn, film["movie_id"])

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
    conn = database.db.get_connection()
    try:
        user_id = database.db.user_register(conn, user_name, user_password, avatar_url)

        return {
            "id": user_id,
            "username": user_name
        }

    finally:
        conn.close()

def check_user_login(username, password):
    conn = database.db.get_connection()
    try:
        user_id = database.db.user_login(conn, username, password)
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
    conn = database.db.get_connection()
    try:
        return database.db.search_film_with_filters()
    finally:
        conn.close()

def get_films_with_filters(title=None, genre=None, actor=None, year=None, sort_by=None, sort_order="asc"):
    conn = database.db.get_connection()
    try:
        return database.db.search_film_with_filters(conn, title=title, genre=genre, actor=actor, year=year, sort_by=sort_by, sort_order=sort_order)
    finally:
        conn.close()
def get_user_profile(user_id):
    conn = database.db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, user_name, avatar_url FROM users_schema.users WHERE id=%s",
                (user_id,)
            )
            user = cur.fetchone()

        if not user:
            return None
        seen_films = database.db.get_films_from_users_list(conn, user_id, 3)   # просмотрено
        planned_films = database.db.get_films_from_users_list(conn, user_id, 1)  # запланировано

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
    conn = database.db.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users_schema.users
                SET avatar_url = %s
                WHERE id = %s;
            """, (avatar_url, user_id))
            conn.commit()
        user_profile = database.db.get_users_profile(conn, user_id)
        if user_profile:
            return user_profile['avatar_url']
        return None
    finally:
        conn.close()
def update_user_profile(user_id, username=None, password=None, avatar=None):
    conn = database.db.get_connection()
    try:
        user = database.db.change_users_profile(
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
    conn = database.db.get_connection()
    films_basic = database.db.get_all_films(conn)
    all_movies = []


    with conn.cursor(cursor_factory=database.db.RealDictCursor) as cur:
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
    conn = database.db.get_connection()
    try:
        status_map = {
            "seen": 3,
            "planned": 1
        }
        status_id = status_map.get(status)

        if status_id is None:
            raise ValueError("Неверный статус")

        return database.db.add_film_to_list(conn, user_id, movie_id, status_id)

    finally:
        conn.close()

def chat_with_ml(message):

    if not message or message.strip() == "":
        return []

    try:
        results = ml.ml.search_movies(message, top_k=10)

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

#фильмы для премьеры
def get_latest_movies(limit=4):
    # Вместо проблемной db.search_film_with_filters 
    # используем вашу же функцию с правильной сортировкой
    films = get_all_movies_newest_first() 
    
    result = []
    # Берем только первые limit фильмов (например, 4)
    for film in films[:limit]:
        result.append({
            "id": film["movie_id"],
            "title": film["title"],
            "year": film["release_year"],
            "poster": film["poster_link"]
        })
    return result


from psycopg2.extras import RealDictCursor


def add_movie(conn, title, overview, release_year, poster_link, genres=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        
        # проверка на дубликат
        cur.execute(
            "SELECT movie_id FROM public.Movies WHERE LOWER(title) = LOWER(%s);",
            (title,)
        )
        existing = cur.fetchone()

        if existing:
            return {
                "error": "Фильм уже существует",
                "movie_id": existing["movie_id"]
            }

        # добавление фильма
        cur.execute("""
            INSERT INTO public.Movies (title, overview, release_year, poster_link)
            VALUES (%s, %s, %s, %s)
            RETURNING movie_id, title, poster_link, release_year;
        """, (title, overview, release_year, poster_link))

        movie = cur.fetchone()
        movie_id = movie["movie_id"]

        # --- добавление жанров ---
        if genres:
            for genre in genres:
                # создаем жанр если его нет
                cur.execute("""
                    INSERT INTO public.genres (genre_name)
                    VALUES (%s)
                    ON CONFLICT (genre_name) DO NOTHING
                    RETURNING genre_id;
                """, (genre,))
                
                result = cur.fetchone()

                if result:
                    genre_id = result["genre_id"]
                else:
                    cur.execute("""
                        SELECT genre_id 
                        FROM public.genres 
                        WHERE genre_name = %s;
                    """, (genre,))
                    genre_id = cur.fetchone()["genre_id"]

                # связываем фильм и жанр
                cur.execute("""
                    INSERT INTO public.movie_genres (movie_id, genre_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (movie_id, genre_id))

        conn.commit()
        return movie

#    Возвращает список фильмов по одному жанру для фронта
 #   в формате: id, title, poster, year
def get_movies_by_genre_front(genre_name):


    conn = database.db.get_connection()
    try:
        films = database.db.search_film_with_filters(conn, genre=genre_name)
        result = []
        for film in films:
            info = database.db.get_film_info(conn, film["movie_id"])
            result.append({
                "id": film["movie_id"],
                "title": film["title"],
                "poster": info.get("poster_link") if info else None,
            })
        return result
    finally:
        conn.close()
''' Возвращает все фильмы, отсортированные по алфавиту.
    ascending=True -> A→Z, ascending=False -> Z→A '''
def get_all_movies_sorted_by_title(ascending=True):
    conn = database.db.get_connection()
    try:
        order_direction = "ASC" if ascending else "DESC"
        with conn.cursor(cursor_factory=db.RealDictCursor) as cur:
            cur.execute(f"""
                SELECT movie_id, title, poster_link, release_year
                FROM public.movies
                ORDER BY title {order_direction};
            """)
            return cur.fetchall()
    finally:
        conn.close()

    #Возвращает все фильмы, отсортированные от новых к старым (по году выпуска, descending)

def get_all_movies_newest_first():

    conn = database.db.get_connection()
    try:
        with conn.cursor(cursor_factory=db.RealDictCursor) as cur:
            cur.execute("""
                SELECT movie_id, title, poster_link, release_year
                FROM public.movies
                ORDER BY release_year DESC;
            """)
            return cur.fetchall()
    finally:
        conn.close()
#фильп по году
def get_films_by_year(conn, year):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT 
            m.movie_id,
            m.title,
            m.release_year,
            m.poster_link
        FROM public.Movies m
        WHERE m.release_year = %s
        ORDER BY m.title;
        """
        cur.execute(query, (year,))
        return cur.fetchall()
#добавление комментов

def add_comment(user_id, movie_id, text):
    conn = database.db.get_connection()

    try:
        comment = database.db.write_comment_on_film(conn, user_id, movie_id, text)

        return {
            "id": comment["id"],
            "user_id": comment["user_id"],
            "movie_id": comment["movie_id"],
            "text": comment["comm"],
            "created_at": str(comment["created_at"])
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()
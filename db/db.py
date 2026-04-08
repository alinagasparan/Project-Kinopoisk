import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2 import errors
from psycopg2.extras import RealDictCursor

load_dotenv()
#Подключение к серверу для работы с базой python -c "from dotenv import load_dotenv; print('OK')"
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

#Количество элементов в таблице
def get_count(conn, table_name):
    with conn.cursor() as cur:
        query = sql.SQL("SELECT COUNT(*) FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        result = cur.fetchone()
        return (f"{result[0]} элементов в таблице {table_name}")

#Регистрация пользователя
def user_register(conn, user_name, user_password, avatar_url=None):
    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO users_schema.users (user_name, user_password, avatar_url)
                VALUES (%s, %s, %s)
                RETURNING id;
                """
            cur.execute(query, (user_name, user_password, avatar_url))
            user_id = cur.fetchone()[0]

        conn.commit()
        return user_id

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Username already exists")
        return None

#Вход в систему
def user_login(conn, nickname, password):
    with conn.cursor() as cur:
        query = """SELECT id, user_password 
        FROM users_schema.users
        WHERE LOWER(user_name) = LOWER(%s);"""
        cur.execute(query, (nickname,))
        user = cur.fetchone()
        if user is None:
            return None
        id, user_password = user
        if user_password == password:
            return id
        return None

#Данные из профиля пользователя
def get_users_profile(conn, user_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """ SELECT user_name, user_password, avatar_url
        FROM users_schema.users
        WHERE id = %s;"""
        cur.execute(query, (user_id,))
        return cur.fetchone()

#Возвращает обновленного пользователя
def change_users_profile(conn, user_id, user_name=None, user_password=None, avatar_url=None):
    with conn.cursor() as cur:
        values = []
        fields = []
        if user_name is not None:
            fields.append("user_name = %s")
            values.append(user_name)
        if user_password is not None:
            fields.append("user_password = %s")
            values.append(user_password)
        if avatar_url is not None:
            fields.append("avatar_url = %s")
            values.append(avatar_url)

        if not fields:
            return
        query = f""" 
            UPDATE users_schema.users
            SET {', '.join(fields)}
            WHERE id = %s;"""
        cur.execute(query, (*values, user_id))
        conn.commit()
        cur.execute("""SELECT * FROM users_schema.users WHERE id = %s;""", (user_id,))
        return cur.fetchone()

def get_all_films(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """SELECT movie_id FROM public.movies"""
        cur.execute(query)
        return cur.fetchall()

#Добавление фильма в список. True если добавился, False если фильм был в другом списке и просто его статус поменялся
def add_film_to_list(conn, user_id, movie_id, status_id):
    with conn.cursor() as cur:
        query = """
        INSERT INTO users_schema.user_movies (user_id, movie_id, status_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, movie_id) 
        DO UPDATE SET status_id = EXCLUDED.status_id
        RETURNING xmax = 0 AS inserted;"""
        cur.execute(query, (user_id, movie_id, status_id))
        inserted = cur.fetchone()[0]
        conn.commit()
        return inserted

#Словарь из названий фильмов, которые в списке у пользователя, список передается через status
def get_films_from_users_list(conn, user_id, status_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """SELECT f.movie_id, f.title FROM users_schema.user_movies um
        JOIN public.movies f ON f.movie_id = um.movie_id
        WHERE um.user_id = %s AND um.status_id = %s;"""
        cur.execute(query, (user_id, status_id))
        films = cur.fetchall()
    return films

#Удаление фильма из списка. Возвращает количество удаленных строк. 1 - успешно
def remove_film_from_list(conn, user_id, movie_id, status_id):
    with conn.cursor() as cur:
        query = """DELETE FROM users_schema.user_movies 
        WHERE user_id = %s AND movie_id = %s AND status_id = %s;"""
        cur.execute(query, (user_id, movie_id, status_id))
        deleted_rows = cur.rowcount
        conn.commit()
        return deleted_rows

#Поиск фильма по названию. Возвращает словарь из id фильма и названия
def search_film_by_name(conn, film_name):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """SELECT movie_id, title FROM public.movies 
        WHERE LOWER(title) LIKE LOWER(%s);"""
        cur.execute(query, (f"%{film_name}%",))
        films = cur.fetchall()
        conn.commit()
        return films

#Информация по фильму
def get_film_info(conn, movie_id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """ SELECT 
            m.title,
            m.overview AS description,
            m.release_year,
            m.poster_link,
            d.name AS director,
            STRING_AGG(DISTINCT g.genre_name, ', ') AS categories,
            STRING_AGG(DISTINCT a.name, ', ') AS actors
        FROM Movies m
        LEFT JOIN Directors d ON m.director_id = d.director_id
        LEFT JOIN Movie_Genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genres g ON mg.genre_id = g.genre_id
        LEFT JOIN Movie_Actors ma ON m.movie_id = ma.movie_id
        LEFT JOIN Actors a ON ma.actor_id = a.actor_id
        WHERE m.movie_id = %s
        GROUP BY m.title, m.overview, m.release_year, m.poster_link, d.name;"""
        cur.execute(query, (movie_id,))
        film = cur.fetchone()
        return film


#Фильтры для поиска. Название, жанр, актёр, год выпуска. + Сортировка по году, названию, возрастному ограничению
def search_film_with_filters(conn, title=None, genre=None, actor=None, year=None):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT DISTINCT 
            m.movie_id, 
            m.title, 
            m.release_year,
            m.poster_link
        FROM Movies m
        LEFT JOIN Movie_Genres mg ON m.movie_id = mg.movie_id
        LEFT JOIN Genres g ON mg.genre_id = g.genre_id
        LEFT JOIN Movie_Actors ma ON m.movie_id = ma.movie_id
        LEFT JOIN Actors a ON ma.actor_id = a.actor_id
        WHERE 1=1
        """
        params = []

        if title:
            query += " AND m.title ILIKE %s"
            params.append(f"%{title}%")

        if genre:
            query += " AND g.genre_name ILIKE %s"
            params.append(f"%{genre}%")  # добавлены %

        if actor:
            query += " AND a.name ILIKE %s"
            params.append(f"%{actor}%")

        if year:
            query += " AND m.release_year = %s"
            params.append(year)  # оставляем int

        cur.execute(query, params)
        return cur.fetchall()

def write_comment_on_film(conn, user_id, movie_id, text):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """INSERT INTO users_schema.comments(user_id, movie_id, comm) 
        VALUES (%s, %s, %s)
        RETURNING id, user_id, movie_id, comm, created_at;"""
        cur.execute(query, (user_id, movie_id, text))
        conn.commit()
        comment = cur.fetchone()
        return comment
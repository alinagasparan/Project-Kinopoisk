import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import sql

load_dotenv()
#Подключение к серверу для работы с базой
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
    with conn.cursor() as cur:
        query = """
        INSERT INTO users_schema.users (user_name, user_password, avatar_url) VALUES (%s, %s, %s)
        RETURNING id;"""
        cur.execute(query, (user_name, user_password, avatar_url))
        user_id = cur.fetchone()[0]
    conn.commit()
    return user_id



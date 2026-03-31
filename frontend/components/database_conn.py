import streamlit as st
import pandas as pd

def get_all_movies():
    # Имитация получения всех данных из БД
    data = {
        'id': [1, 2, 3, 4],
        'title': ['Интерстеллар', 'Матрица', 'Шрек', 'Во все тяжкие'],
        'genre': ['Научная фантастика', 'Боевик', 'Мультфильм', 'Драма'],
        'year': [2014, 1999, 2001, 2008],
        'poster': [
            'https://upload.wikimedia.org/wikipedia/ru/c/c3/Interstellar_2014.jpg',
            'https://upload.wikimedia.org/wikipedia/ru/9/9d/Matrix-DVD.jpg',
            'https://upload.wikimedia.org/wikipedia/ru/thumb/3/39/Shrek.jpg/960px-Shrek.jpg',
            'https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/0485e770-2e82-4a39-a97e-9bcc5abcc421/3840x'
        ]
    }
    return pd.DataFrame(data)

def get_movie_by_id(movie_id):
    # Имитация получения данных об одном фильме
    df = get_all_movies()
    return df[df['id'] == movie_id].iloc[0]
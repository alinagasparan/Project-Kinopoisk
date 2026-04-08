import streamlit as st
import pandas as pd
from backend.main1 import get_all_movies_with_details
from components.movie_cards import render_movie_card
from assets.styles import apply_styles, filter_panel

# Настройка страницы
st.set_page_config(page_title="Catalog", layout="wide")
apply_styles()

st.title("Библиотека кино")

with st.container(key="catalog"):
    # Оставляем колонки, чтобы кнопки фильтров были сбоку
    main_col, filter_col = st.columns([4, 1])

    with filter_col:
        st.markdown("### 🔍 Фильтры")
        # Кнопки отрисовываются, но их результат (film_types и т.д.) пока не используется
        film_types, genres, sort_by = filter_panel()

    with main_col:
        # 1. ЗАГРУЗКА ДАННЫХ
        # Всегда загружаем все фильмы, игнорируя состояние фильтров
        movies = get_all_movies_with_details()
        data = pd.DataFrame(movies) if movies else pd.DataFrame()

        # 2. ПРИВЕДЕНИЕ КЛЮЧЕЙ К ЕДИНОМУ ВИДУ
        if not data.empty:
            data = data.rename(columns={
                "movie_id": "id",
                "poster_link": "poster",
                "release_year": "year"
            })

        # 3. ОТОБРАЖЕНИЕ КАРТОЧЕК
        if data.empty:
            st.warning("В каталоге пока пусто 🍿")
        else:
            # Сетка по 3 карточки в ряд
            cols_per_row = 3
            rows_count = len(data)
            
            for i in range(0, rows_count, cols_per_row):
                columns = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < rows_count:
                        row = data.iloc[i + j]
                        with columns[j]:
                            render_movie_card(
                                movie_id=row['id'],
                                title=row['title'],
                                img_url=row.get('poster', '')
                            )
import streamlit as st
import pandas as pd
from components.database_conn import get_all_movies
from components.movie_cards import render_movie_card 
from assets.styles import apply_styles          
from utils import show_sidebar_mascot  

st.set_page_config(page_title="Catalog", layout="wide")
apply_styles()
show_sidebar_mascot()

st.title("🎬 Библиотека кино")

#Получаем данные из нашего нового компонента БД
data = get_all_movies()

main_col, filter_col = st.columns([4, 1])

with filter_col:
    st.markdown("### 🔍 Фильтры")
with main_col:
    if data.empty:
        st.warning("В библиотеке пока нет фильмов 🍿")
    else:
        rows_count = len(data)
        cols_per_row = 3
        
        for i in range(0, rows_count, cols_per_row):
            columns = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < rows_count:
                    row = data.iloc[i + j]
                    with columns[j]:
                        render_movie_card(
                            title=row['title'], 
                            img_url=row['poster'], 
                            genre=row['genre'], 
                            year=row['year']
                        )
import streamlit as st

def render_movie_card(title, img_url, genre, year):
    """
    Функция создает HTML-структуру карточки.
    Все сложные стили (высота, цвета, тени) подтянутся автоматически 
    из класса 'movie-card', который мы прописали в styles.py.
    """
    st.markdown(f'''
        <div class="movie-card">
            <img src="{img_url}">
            <div class="card-content">
                <h4>{title}</h4>
                <p>{genre} • {year}</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
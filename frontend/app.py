import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from assets.styles import apply_styles, search_style
from backend.main1 import get_films_by_search

st.set_page_config(layout="wide", page_title="Cinemind")

apply_styles()
search_style()

# Страницы
home = st.Page("pages/01_Home.py", title="Главная", default=True)
catalog = st.Page("pages/02_Catalog.py", title="Каталог")
assistant = st.Page("pages/03_Assistant.py", title="Ассистент")
profile = st.Page("pages/04_Profile.py", title="Профиль")
details = st.Page("pages/05_Details.py", title="Детали")
auth = st.Page("pages/06_Auth.py", title="Войти")
pg = st.navigation([home, catalog, assistant, auth, profile, details], position="hidden")

# Инициализация session_state для поиска
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# Шапка
with st.container(key="navbar"):

    col_menu, col_title, col_search, col_none, col_auth = st.columns([0.9, 1.2, 3.4, 0.8, 0.8])

    with col_menu:
        with st.popover("📂 Меню"):
            st.page_link(home, label="Главная", icon="🏠")
            st.page_link(catalog, label="Каталог", icon="🎬")
            st.page_link(assistant, label="Ассистент", icon="🐱")

    with col_title:
        st.markdown('<div class="nav-logo">Cinemind</div>', unsafe_allow_html=True)

    with col_search:
        search_query = st.text_input(
            "",
            placeholder="Найти фильм...",
            label_visibility="collapsed",
            key="search_input"
        )
        
    with col_auth:
        if "user" in st.session_state and st.session_state.user:
        # Если пользователь вошел, показываем кнопку Профиль
            if st.button("Профиль", use_container_width=True, key="nav_profile_btn"):
                st.switch_page(profile)
        else:
            # Если данных нет, показываем кнопку Войти
            if st.button("Войти", use_container_width=True, key="nav_login_btn"):
                st.switch_page(auth)


# Обновляем результаты при изменении запроса
if search_query and search_query != st.session_state.last_query:
    st.session_state.last_query = search_query
    st.session_state.search_results = get_films_by_search(search_query)
elif not search_query:
    st.session_state.last_query = ""
    st.session_state.search_results = []

# Карточки результатов
if search_query and st.session_state.search_results:
    films = st.session_state.search_results
    st.markdown(
        f'<div class="search-results-header">Найдено: {len(films)}</div>',
        unsafe_allow_html=True
    )

    for film in films:
        title = film.get("title", "Без названия")
        year  = film.get("year", "")
        # Используем постер из данных или заглушку
        poster = film.get("poster") or "https://via.placeholder.com/45x65?text=?"
        year_html = f'<div class="film-year">📅 {year}</div>' if year else ""

        # HTML-карточка (визуал)
        # ВАЖНО: Весь HTML должен быть внутри одного st.markdown
        st.markdown(f"""
        <div class="film-result-card">
            <div class="film-poster-container">
                <img src="{poster}" class="film-poster-img" style="width:40px; height:60px; object-fit:cover; border-radius:4px;">
            </div>
            <div class="film-info">
                <div class="film-title">{title}</div>
                {year_html}
            </div>
            <div class="film-arrow"></div>
        </div>
        """, unsafe_allow_html=True)

        btn_label = f"{title} ({year})" if year else title

        if st.button(btn_label, key=f"f_res_{film['id']}", use_container_width=True):
            # Устанавливаем ключи, которые ожидает 05_Details.py
            st.session_state.selected_movie = film.get("title")  # Название фильма
            st.session_state.selected_film_id = film.get("id")   # ID фильма
            
            # Очищаем результаты поиска для чистого возврата
            st.session_state.search_results = []
            st.session_state.last_query = ""
            
            # Переходим на страницу деталей
            st.switch_page(details)

elif search_query and not st.session_state.search_results:
    st.caption("😕 Ничего не найдено — попробуйте другой запрос")
    
pg.run()
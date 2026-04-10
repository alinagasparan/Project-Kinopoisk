import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import base64
from pathlib import Path

import streamlit as st
from assets.styles import apply_styles, search_style
from backend.main1 import get_films_by_search

st.set_page_config(layout="wide", page_title="Cinemind")
apply_styles()
search_style()

home = st.Page("pages/01_Home.py", title="Главная", default=True)
catalog = st.Page("pages/02_Catalog.py", title="Каталог")
assistant = st.Page("pages/03_Assistant.py", title="Ассистент")
profile = st.Page("pages/04_Profile.py", title="Профиль")
details = st.Page("pages/05_Details.py", title="Детали")
auth = st.Page("pages/06_Auth.py", title="Войти")

pg = st.navigation([home, catalog, assistant, auth, profile, details], position="hidden")

# Инициализация
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "last_page" not in st.session_state:
    st.session_state.last_page = pg.title
if "clear_search" not in st.session_state:
    st.session_state.clear_search = False

# Если объект текущей страницы изменился (пользователь кликнул в меню)
if st.session_state.last_page != pg.title:
    st.session_state.search_results = []
    st.session_state.last_query = ""
    st.session_state.last_page = pg.title
    st.session_state.clear_search = True # Включаем флаг для очистки поля ввода

# Над шапкой
FRONTEND_DIR = Path(__file__).resolve().parent
mascot_path = FRONTEND_DIR / "assets" / "navbar_img.jpg"
if mascot_path.exists():
    with open(mascot_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <div style="width: 100%; max-height: 230px; overflow: hidden; margin-top: -3rem; margin-bottom: 1rem; border-radius: 0 0 15px 15px;">
            <img src="data:image/jpg;base64,{img_data}" style="width: 100%; max-height: 230px; object-fit: cover; display: block;">
        </div>
    """, unsafe_allow_html=True)

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
        if st.session_state.clear_search:
            st.session_state.search_input = ""
            st.session_state.clear_search = False

        search_query = st.text_input(
            "Поиск",
            placeholder="Найти фильм...",
            label_visibility="collapsed",
            key="search_input"
        )

    with col_auth:
        if st.session_state.get("user"):
            if st.button("Профиль", use_container_width=True, key="nav_prof"):
                st.switch_page(profile)
        else:
            if st.button("Войти", use_container_width=True, key="nav_auth"):
                st.switch_page(auth)

# Обработка поиска
if search_query and search_query != st.session_state.last_query:
    st.session_state.last_query = search_query
    st.session_state.search_results = get_films_by_search(search_query)
elif not search_query:
    st.session_state.search_results = []
    st.session_state.last_query = ""

# Показываем результаты только если мы на главной и есть запрос
if pg.title == home.title and search_query and st.session_state.search_results:
    with st.container():
        films = st.session_state.search_results
        st.markdown(f'<div class="search-results-header">Найдено: {len(films)}</div>', unsafe_allow_html=True)

        for film in films:
            title = film.get("title", "Без названия")
            year = film.get("year", "")
            poster = film.get("poster_link") or "https://via.placeholder.com/45x65?text=?"
            
            st.markdown(f"""
            <div class="film-result-card">
                <div class="film-poster-container">
                    <img src="{poster}" style="width:40px; height:60px; object-fit:cover; border-radius:4px;">
                </div>
                <div class="film-info">
                    <div class="film-title" style="color:#e2e8f0; font-weight:600;">{title}</div>
                    <div class="film-year">📅 {year}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Смотреть {title}", key=f"f_res_{film['id']}", use_container_width=True):
                st.session_state.selected_movie = title
                st.session_state.selected_movie_id = film.get("id")
                # Сбрасываем поиск перед уходом
                st.session_state.search_results = []
                st.session_state.last_query = ""
                st.session_state.clear_search = True
                st.switch_page(details)

pg.run()
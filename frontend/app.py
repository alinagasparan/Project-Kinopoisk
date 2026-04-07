import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from assets.styles import apply_styles
from backend.main1 import get_films_by_search

apply_styles()

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

# Шапка
st.title("🎬 Cinemind 🎬")

with st.container(key="navbar"):
    col1, col2, col3 = st.columns([1.5, 5, 0.7])

    with col1:
        with st.popover("📂 Меню навигации"):
            st.page_link("pages/01_Home.py", label="Главная", icon="🏠")
            st.page_link("pages/02_Catalog.py", label="Каталог", icon="🎬")
            st.page_link("pages/03_Assistant.py", label="Ассистент", icon="🐱")
            st.page_link("pages/04_Profile.py", label="Профиль")
            st.page_link("pages/05_Details.py", label="Детали")

    with col2:
        search_query = st.text_input(
            "",
            placeholder="Поиск фильма по названию...  |  Например: Дюна",
            label_visibility="collapsed",
            key="search_input"
        )

        # Запрашиваем результаты только когда запрос изменился
        if search_query and search_query != st.session_state.last_query:
            st.session_state.last_query = search_query
            st.session_state.search_results = get_films_by_search(search_query)

        elif not search_query:
            st.session_state.last_query = ""
            st.session_state.search_results = []

        # Выпадающий список результатов
        if search_query and st.session_state.search_results:
            films = st.session_state.search_results

            # Метки: "Название (год)" или просто "Название"
            labels = []
            for f in films:
                year = f.get("year")
                label = f["title"]
                if year:
                    label += f" ({year})"
                labels.append(label)

            placeholder_option = "🔍 Выберите фильм из списка..."
            options = [placeholder_option] + labels

            selected = st.selectbox(
                "Результаты поиска",
                options=options,
                label_visibility="collapsed",
                key="search_select"
            )

            # Переход при выборе фильма
            if selected and selected != placeholder_option:
                idx = labels.index(selected)
                chosen_film = films[idx]

                st.session_state.selected_movie = chosen_film["title"]
                st.session_state.selected_film_id = chosen_film["id"]

                # Сбрасываем поиск чтобы не зацикливалось
                st.session_state.search_results = []
                st.session_state.last_query = ""

                st.switch_page("pages/05_Details.py")

        elif search_query and search_query == st.session_state.last_query and not st.session_state.search_results:
            st.caption("😕 Ничего не найдено. Попробуйте другой запрос.")

    with col3:
        if st.button("Войти"):
            st.switch_page("pages/06_Auth.py")

pg.run()
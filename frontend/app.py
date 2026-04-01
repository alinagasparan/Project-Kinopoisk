import streamlit as st
from assets.styles import apply_styles

# Главный файл, работа с окнами(Тут пока что Шапка сайта)

# Конфигурация (сайдбар изначально закрыт, а CSS его добьет)
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

apply_styles()

home = st.Page("pages/01_Home.py", title="Главная", default=True)
catalog = st.Page("pages/02_Catalog.py", title="Каталог")
assistant = st.Page("pages/03_Assistant.py", title="Ассистент")
profile = st.Page("pages/04_Profile.py", title="Профиль") # В дальнейшем будет скрыто
details = st.Page("pages/05_Details.py", title="Детали") # В дальнейшем будет скрыто

pg = st.navigation([home, catalog, assistant, profile, details], position="hidden")

with st.container():
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        with col1:
            with st.popover("📂 Меню навигации"):
                st.page_link("pages/01_Home.py", label="Главная", icon="🏠")
                st.page_link("pages/02_Catalog.py", label="Каталог", icon="🎬")
                st.page_link("pages/03_Assistant.py", label="Кинокотик", icon="🐱")
                st.page_link("pages/04_Profile.py", label="Профиль") # В дальнейшем будет скрыто
                st.page_link("pages/05_Details.py", label="Детали") # В дальнейшем будет скрыто

    with col2:
        search_query = st.text_input("", placeholder="Поиск фильма по названию...  |  Например: Дюна", label_visibility="collapsed")

    with col3:
        st.button("Профиль")

pg.run()
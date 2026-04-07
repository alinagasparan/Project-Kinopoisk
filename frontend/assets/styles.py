import streamlit as st

def apply_styles():
    """Функция наводит общую красоту на странице"""
    
    style_html = """
    <style>
        /* Скрываем сайдбар */
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        /* Убираем отступ сверху */
        .block-container {
            padding-top: 0rem;
        }

        /* Убираем у всех */
        [data-testid="stHorizontalBlock"] {
            background-color: transparent !important;
            border-bottom: none !important;
            border-radius: 0 !important;
        }

        /* Шапка  */
        .st-key-navbar [data-testid="stHorizontalBlock"] {
            background-color: #060407 !important;
            padding: 10px 30px !important;
            border-radius: 16px !important;
            border-bottom: 2px solid #610f2e !important;
            align-items: center !important;
        }

        /* Фон за карточками */
        .st-key-premieres,
        .st-key-catalog {
            background-color: #060407 !important;
            padding: 20px !important;
            border-radius: 16px !important;
            border-bottom: 2px solid #610f2e !important;
            margin-bottom: 16px !important;
        }

        /* Анимация появления */
        .stApp {
            animation: fadeIn 0.8s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Минимальная ширина колонок */
        [data-testid="stColumn"] {
            min-width: 0 !important;
        }

        /* Кноки Streamlit*/
        div[data-testid="stButton"] > button {
            background-color: #610f2e !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            transition: 0.2s;
            padding: 10px !important;
        }
        
        div[data-testid="stButton"] > button:hover {
            background-color: #a20e47 !important;
            transform: scale(1.02);
        }

        /* Карточки */
        /* Стилизуем сам контейнер карточки (находим по префиксу ключа) */
        div[class*="st-key-movie_card_"] {
            background: #1e223b;
            border-radius: 14px;
            transition: 0.3s ease;
            border: 1px solid rgba(255,255,255,0.1);
            overflow: hidden;
            margin-bottom: 10px;
        }

        /* Эффект наведения на всю карточку */
        div[class*="st-key-movie_card_"]:hover {
            transform: translateY(-6px);
            border-color: #a20e47;
            box-shadow: 0 15px 25px rgba(0,0,0,0.5);
        }

        /* Убираем стандартные отступы Streamlit между постером и кнопкой */
        div[class*="st-key-movie_card_"] div[data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }

        /*Кнопки карточек */
        /* Сдвигаем кнопку вверх, чтобы прилепить к постеру */
        div[class*="st-key-movie_card_"] div[data-testid="stButton"] {
            margin-top: -13px !important;
        }

        /* Уникальный стиль для кнопки с названием фильма */
        div[class*="st-key-movie_card_"] div[data-testid="stButton"] > button {
            background: transparent !important;
            font-size: 14px !important;
            color: #e2e8f0 !important;
            white-space: normal !important;
            line-height: 1.2;
            height: 3.5em !important; 
            transform: none !important;
            box-shadow: none !important;
            border-radius: 15px !important;
            overflow: hidden !important;
        }

        /* Hover только для кнопки внутри карточки */
        div[class*="st-key-movie_card_"] div[data-testid="stButton"] > button:hover {
            background: #a20e47 !important;
            color: white !important;
        }

        /* Кот-помощник фиксированный */
        .mascot-container {
            position: fixed;
            bottom: 0px;
            left: 10px;
            z-index: 9999;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .mascot-container:hover {
            transform: scale(1.1);
        }

        /* Вход рег */
        .st-key-auth_form {
            background-color: #060407 !important;
            padding: 30px !important;
            border-radius: 16px !important;
            border: 1px solid #610f2e !important;
            max-width: 500px !important;
            margin: 0 auto !important;
        }

        /* Кнопки переключения */
        .st-key-btn_login button,
        .st-key-btn_register button {
            background-color: transparent !important;
            border: 1px solid #610f2e !important;
            color: #e2e8f0 !important;
            font-size: 15px !important;
            padding: 8px !important;
            border-radius: 10px !important;
            width: 150px;  
        }
        .st-key-btn_login button{
            position: fixed;
            bottom: 10px;
            left: 20px;
        }
        .st-key-btn_register button{
            position: fixed;
            bottom: 10px;
            left: 180px;
        }

        .st-key-btn_login button:hover,
        .st-key-btn_register button:hover {
            background-color: #610f2e !important;
            color: #ffffff !important;
        }

        /* Родительский контейнер для позиционирования */
        .card-container {
            position: relative;
            z-index: 1;
        }

    </style>
    """
    
    st.markdown(style_html, unsafe_allow_html=True)

def filter_panel():
    st.markdown("""
        <div style="background:#242330; padding:10px 16px; margin-bottom: 5px;">
            <span style="color:#ffffff; font-weight:500; font-size:14px; letter-spacing:1px;">ТИП</span>
        </div>
    """, unsafe_allow_html=True)
    
    film = st.checkbox("Фильм")
    serial = st.checkbox("TV Сериал")

    st.markdown("""
        <div style="background:#242330; padding:10px 16px; margin-top:16px; margin-bottom: 5px;">
            <span style="color:#ffffff; font-weight:500; font-size:14px; letter-spacing:1px;">ЖАНР</span>
        </div>
    """, unsafe_allow_html=True)
    
    fantastika = st.checkbox("Фантастика")
    boevik = st.checkbox("Боевик")
    comedy = st.checkbox("Комедия")
    drama = st.checkbox("Драма")
    horror = st.checkbox("Ужасы")
    mult = st.checkbox("Мультфильмы")

    st.markdown("""
        <div style="background:#242330; padding:10px 16px; margin-top:16px; margin-bottom: 5px;">
            <span style="color:#ffffff; font-weight:500; font-size:14px; letter-spacing:1px;">СОРТИРОВКА</span>
        </div>
    """, unsafe_allow_html=True)
    
    sort_by = st.radio(
        label="",
        options=["По рейтингу", "По популярности", "По алфавиту", "По дате выхода"],
        label_visibility="collapsed"
    )

    film_types = [t for t, v in [("Фильм", film), ("TV Сериал", serial)] if v]
    genres = [g for g, v in [
        ("Фантастика", fantastika), ("Боевик", boevik), ("Комедия", comedy),
        ("Драма", drama), ("Ужасы", horror), ("Мультфильмы", mult)
    ] if v]

    return film_types, genres, sort_by
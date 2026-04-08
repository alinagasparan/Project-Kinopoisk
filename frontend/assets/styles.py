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

def search_style():
    """Стили в шапке"""
    
    style_html = """
    <style>

        /* Шапка  */

        .block-container {
            max-width: 95% !important; /* Увеличиваем полезную ширину до 95% */
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            padding-top: 1rem !important;
        }

        /* Убираем ограничение ширины для навигации */
        .st-key-navbar {
            width: 100% !important;
        }
        /* Выравнивание содержимого колонок в шапке по центру */
        .st-key-navbar [data-testid="stHorizontalBlock"] {
            align-items: center !important;
        }

        /* Стилизация самого поповера, чтобы он не выбивался из дизайна */
        .st-key-navbar div[data-testid="stPopover"] > button {
            background-color: transparent !important;
            border: 1px solid #610f2e !important;
            color: white !important;
            width: 100%;
        }

        .st-key-navbar [data-testid="stHorizontalBlock"] {
            background-color: #060407 !important;
            padding: 10px 30px !important;
            border-radius: 16px !important;
            border-bottom: 2px solid #610f2e !important;
            align-items: center !important;
        }
        
        /* ─── Выравнивание колонок в шапке ─── */
        /* Находим контейнер navbar и заставляем все элементы внутри стоять по центру */
        .st-key-navbar [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 1rem !important;
        }

        /* ─── Поле поиска в шапке ─── */
        .st-key-navbar div[data-testid="stTextInput"] {
            position: relative;
        }
        
        /* Иконка лупы */
        .st-key-navbar div[data-testid="stTextInput"]::before {
            content: "🔍";
            position: absolute;
            left: 0.7rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.9rem;
            z-index: 10;
            opacity: 0.6;
            pointer-events: none;
        }

        .st-key-navbar div[data-testid="stTextInput"] input {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(97,15,46,0.6) !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
            padding: 0.5rem 1rem 0.5rem 2.2rem !important; /* Уменьшили отступы для компактности */
            height: 38px !important; /* Фиксированная высота как у кнопок */
            font-size: 0.85rem !important;
        }

        .st-key-navbar div[data-testid="stTextInput"] input:focus {
            border-color: #a20e47 !important;
            background: rgba(255,255,255,0.1) !important;
            box-shadow: 0 0 10px rgba(162,14,71,0.2) !important;
        }

        /* ─── Стилизация Popover (Меню) ─── */
        .st-key-navbar div[data-testid="stPopover"] > button {
            background-color: transparent !important;
            border: 1px solid rgba(97,15,46,0.6) !important;
            color: white !important;
            height: 38px !important;
            border-radius: 10px !important;
            transition: 0.3s !important;
        }

        .st-key-navbar div[data-testid="stPopover"] > button:hover {
            border-color: #a20e47 !important;
            background: rgba(162,14,71,0.1) !important;
        }

        /* ─── Результаты поиска (выпадающий список) ─── */
        .search-results-header {
            font-family: 'Inter', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            color: rgba(200,200,200,0.45);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 1rem 0 0.5rem 0.2rem;
        }

        .film-result-card {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            padding: 0.6rem 0.9rem;
            margin: 0.25rem 0;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 10px;
            transition: 0.2s;
        }

        .film-result-card:hover {
            background: rgba(97,15,46,0.2);
            border-color: rgba(162,14,71,0.5);
            transform: translateX(5px);
            cursor: pointer;
        }

        .film-result-card .film-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #e2e8f0;
        }

        .film-result-card .film-year {
            font-size: 0.75rem;
            color: #a20e47;
        }

        /* ─── Логотип (Название сайта) ─── */
        .nav-logo {
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #c74c74);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: flex-start; 
            letter-spacing: 0.5px;
            /* Сдвигаем логотип чуть выше */
            margin-top: -4px !important; 
            padding-left: 5px;
        }
        
        .film-poster-container {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 60px;
            flex-shrink: 0; /* Чтобы картинка не сжималась */
            overflow: hidden;
            border-radius: 5px;
            background: #121212;
        }

        .film-result-card {
            display: flex;
            align-items: center;
            gap: 15px; /* Отступ между постером и текстом */
            padding: 8px 12px;
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            margin-bottom: 8px;
            position: relative;
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
            <span style="color:#ffffff; font-weight:500; font-size:14px; letter-spacing:1px;">ГОД ВЫПУСКА</span>
        </div>
    """, unsafe_allow_html=True)
    year_input = st.selectbox(
        label="",
        options=["Любой"] + list(range(2025, 1969, -1)),
        label_visibility="collapsed"
    )
    selected_year = None if year_input == "Любой" else int(year_input)

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
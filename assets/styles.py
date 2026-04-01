import streamlit as st

def apply_styles():
    """Функция наводит общую красоту на странице"""
    
    style_html = """
    <style>

        /* Полностью скрываем сайдбар и кнопку его открытия */
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        /* Убираем лишние отступы сверху, чтобы шапка была вплотную */
        .stAppHeader {
            display: none;
        }
        
        /* Шапка сайта */
        .nav-wrapper {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 70px;
            background-color: #1a1a1a;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 1000;
            border-bottom: 2px solid #e50914; /* Красная линия в стиле онлайн-кинотеатра */
        }

        .main-content {
            margin-top: 100px;
        }

        /* Анимация появления */
        .stApp {
            animation: fadeIn 0.8s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Стиль карточки фильма */
        .movie-card {
            background: #1f2937;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: 0.3s ease;
            text-align: center;
            display: flex;
            flex-direction: column;
            height: 520px;
            margin-bottom: 25px;
        }

        .movie-card:hover {
            transform: translateY(-5px);
            border-color: #e50914;
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }

        .movie-card img {
            width: 100%;
            height: 350px;
            object-fit: cover; 
            border-radius: 5px;
            margin-bottom: 10px;
        }

        /* Заголовок */
        .movie-card h4 {
            font-size: 1.1rem;
            line-height: 1.3;
            height: 3.9em;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            margin: 5px 0;
            color: #ffffff;
        }

        /* Кастомизация стандартных кнопок Streamlit */
        div.stButton > button {
            background-color: #e50914 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            transition: 0.2s;
        }
        
        div.stButton > button:hover {
            background-color: #ff0f1a !important;
            transform: scale(1.02);
        }
        
    </style>
    """
    
    st.markdown(style_html, unsafe_allow_html=True)
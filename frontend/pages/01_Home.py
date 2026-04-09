import streamlit as st
from components.movie_cards import render_movie_card
from utils import show_mascot   
from backend.main1 import get_latest_movies
from assets.styles import apply_styles 

st.set_page_config(page_title="Home", layout="wide")
apply_styles()

st.subheader("🔥 Премьеры")

# Получаем данные из БД
latest_movies = get_latest_movies(limit=4)

if not latest_movies:
    st.info("Список премьер скоро обновится!")
else:
    with st.container(key="premieres"):
        # Создаем колонки по количеству полученных фильмов
        cols = st.columns(len(latest_movies), gap="medium")
        
        for i, movie in enumerate(latest_movies):
            with cols[i]:
                render_movie_card(
                    movie_id=movie["id"],
                    title=movie["title"], 
                    img_url=movie["poster"] if movie["poster"] else "https://via.placeholder.com/500x750?text=No+Poster"
                )

st.divider()

st.subheader("📰 Последние события киномира")

def render_news(image_url, title, text):
    with st.container():
        col1, col2 = st.columns([1, 2.2])
        with col1:
            st.image(image_url, use_container_width=True)
        with col2:
            st.markdown(f'<div class="news-title">{title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="news-text">{text}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


render_news(
    "https://www.kinonews.ru/insimgs/2026/newsimg/big/newsimg140537.webp",
    "Питер Динклэйдж вступает в схватку с ксеноморфами",
    "Звезда 'Игры престолов' присоединился к касту второго сезона сериала 'Чужой: Земля'. Инсайдеры сообщают, что его персонаж станет ключевым антагонистом, представляющим интересы корпорации Weyland-Yutani в самом начале её пути."
)

render_news(
    "https://www.kinonews.ru/insimgs/2026/newsimg/middle/newsimg140530.webp",
    "Возвращение Чарли: Ума Турман в 'Декстер: Воскрешение'",
    "Showtime подтвердил полноценное возвращение Умы Турман. Её героиня, бывший спецназовец, станет основной угрозой для Декстера Моргана во втором сезоне. Съемки стартуют уже этим летом в Майами."
)

render_news(
    "https://www.kinonews.ru/insimgs/2026/newsimg/big/newsimg140513.webp",
    "Ной Хоули переосмыслит аргентинский хоррор 'Одержимые'",
    "Студия Warner Bros. официально запустила производство ремейка культового хоррора Terrified. Режиссер обещает сохранить атмосферу оригинального фильма Демьяна Ругны, добавив в неё масштаб голливудских блокбастеров."
)

render_news(
    "https://cdnstatic.rg.ru/crop1300x868/uploads/images/gallery/cef1ebf8/3_65f68158.jpg",
    "Marvel готовит анонс нового 'Человека-паука'",
    "Кевин Файги подтвердил, что сценарий четвертой части приключений Питера Паркера с Томом Холландом официально завершен. Сюжет сфокусируется на 'уличном' уровне супергероя, а к роли Сорвиголовы может вернуться Чарли Кокс."
)

render_news(
    "https://www.afisha.uz/uploads/media/2024/11/277305010bb57436aa34ed6e2fe12593_lf.jpg",
    "Кристофер Нолан собирает звездный каст для нового секретного проекта",
    "К Мэтту Дэймону и Тому Холланду в новом фильме Нолана присоединились Энн Хэтэуэй и Зендея. О сюжете известно лишь то, что это не будет научно-фантастическим триллером в духе 'Начала', а скорее историческим эпиком."
)

show_mascot()
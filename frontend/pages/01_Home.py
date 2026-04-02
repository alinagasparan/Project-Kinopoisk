import streamlit as st
from components.movie_cards import render_movie_card
from assets.styles import apply_styles          
from utils import show_mascot   

# Главное окно (Премьеры, Новости)

st.set_page_config(page_title="Cinemind",layout="wide")
apply_styles()

st.title("🎬 Cinemind 🎬")

st.subheader("🔥 Премьеры недели")

titles = ["Человек-паук: Возвращение домой", "Вонка", "Игра престолов", "Во все тяжкие"]
posters = [
    "https://upload.wikimedia.org/wikipedia/ru/5/5a/Spider-Man_Homecoming_logo.jpg",
    "https://upload.wikimedia.org/wikipedia/ru/thumb/9/95/Wonka_%28film%2C_2023%29.jpg/500px-Wonka_%28film%2C_2023%29.jpg",
    "https://upload.wikimedia.org/wikipedia/ru/4/49/Game_of_Thrones.jpg",
    "https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/0485e770-2e82-4a39-a97e-9bcc5abcc421/3840x"
]
cols = st.columns(4)

for i, col in enumerate(cols):
    with col:
        render_movie_card(
            title=titles[i], 
            img_url=posters[i], 
            genre="🍿 Скоро", 
            year="2026"
        )

# Новости
st.divider()
st.subheader("📰 Новости кино")
st.write("— Объявлена дата выхода нового сезона 'Истребителя демонов'!")
st.write("— Режиссер Кристофер Нолан работает над новым секретным проектом.")

show_mascot()
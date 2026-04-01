import streamlit as st
from assets.styles import apply_styles          

# Окно определенного фильма/сериала(Вся информация о нем)

st.set_page_config(page_title="Details", layout="wide")
apply_styles()

movie_name = st.session_state.get("selected_movie", "Не выбрано")

col_img, col_info = st.columns([1, 2])

with col_img:
    st.image("https://i.pinimg.com/736x/51/71/24/517124fcea493bad8d49e69181131902.jpg")

with col_info:
    st.title(movie_name)
    st.write("**Год:** 2024 | **Страна:** США | **Жанр:** Фантастика")
    st.write("**Описание:** Очень крутое описание сюжета, которое заставляет тебя нажать кнопку просмотра.")
    
    st.selectbox("Статус", ["Не смотрел", "Запланировано", "Просмотрено"])
    st.button("❤️ В избранное")

st.divider()
st.subheader("💬 Комментарии")
st.text_area("Оставь свой отзыв:")
st.button("Отправить")
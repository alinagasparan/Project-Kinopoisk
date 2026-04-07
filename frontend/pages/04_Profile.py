import streamlit as st
from assets.styles import apply_styles          

if "user" not in st.session_state:
    st.warning("Сначала войдите!")
    st.stop()
st.set_page_config(page_title="Profile", layout="wide")

col1, col2 = st.columns([1, 2])

with col1:
    st.image("https://i.pinimg.com/736x/60/22/7e/60227e815aa98cbb58bd60ca271acc09.jpg", caption="Твой аватар")
    st.button("Сменить фото")

with col2:
    st.header("Никнейм: MovieLover2026")

st.divider()
tab_seen, tab_plan = st.tabs(["✅ Просмотрено", "⏳ Запланировано"])
with tab_seen:
    st.write("1. Интерстеллар")
    st.write("2. Матрица")

if st.button("Выйти из аккаунта"):
    # Очищаем данные пользователя
    if "user" in st.session_state:
        del st.session_state.user
    if "is_logged_in" in st.session_state:
        st.session_state.is_logged_in = False
    
    st.rerun() # Шапка сразу изменится на "Войти"
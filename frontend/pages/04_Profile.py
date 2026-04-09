import streamlit as st
from assets.styles import apply_styles  
from backend.main1 import get_user_profile, change_user_avatar, add_movie 
from backend.db import get_connection 

if "user" not in st.session_state:
    st.warning("Сначала войдите!")
    st.stop()
st.set_page_config(page_title="Profile", layout="wide")
apply_styles()

user_info = get_user_profile(st.session_state.user['id'])

if user_info:
    
    if st.button("← Главное меню"):
        st.switch_page("pages/01_Home.py")

    col_avatar, col_info = st.columns([1, 2])

    with col_avatar:
        avatar_url = user_info['avatar'] if user_info['avatar'] else "https://www.kindpng.com/picc/m/736-7367385_cat-circle-cat-icon-png-transparent-png.png"
        st.image(avatar_url, use_container_width=True)
        
        new_avatar = st.text_input("URL нового аватара", placeholder="https://link-to-image.com/...")
        if st.button("Обновить фото", key="btn_update_avatar"):
            if new_avatar:
                result = change_user_avatar(user_info['id'], new_avatar)
                if result:
                    st.success("Фото обновлено!")
                    st.rerun()
                else:
                    st.error("Не удалось обновить фото.")
            else:
                st.warning("Введите URL аватара.")

    with col_info:
        st.title(f"Профиль: {user_info['username']}")
        
        st.markdown(f"""
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <span style="background: #1e223b; padding: 5px 15px; border-radius: 20px; color: #e2e8f0;">🆔 ID: {user_info['id']}</span>
                <span style="background: #610f2e; padding: 5px 15px; border-radius: 20px; color: white;">🎬 Фильмов в списках: {len(user_info['seen']) + len(user_info['planned'])}</span>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("Управление аккаунтом")
        if st.button("Log Out"):
            del st.session_state.user
            st.session_state.is_logged_in = False
            st.switch_page("pages/01_Home.py")

    st.divider()

    tab_seen, tab_plan = st.tabs(["✅ Просмотрено", "⏳ Запланировано"])

    with tab_seen:
        if user_info['seen']:
            for film in user_info['seen']:
                st.markdown(f"**{film['title']}**")
        else:
            st.info("Вы еще не отметили ни одного просмотренного фильма.")

    with tab_plan:
        if user_info['planned']:
            for film in user_info['planned']:
                st.markdown(f"**{film['title']}**")
        else:
            st.info("Ваш список 'Запланировано' пока пуст.")

    # Блок админа
    if user_info['username'].lower() == "admin":
        st.divider()
        st.subheader("Добавление нового фильма")

        title = st.text_input("Название фильма", key="admin_title")
        overview = st.text_area("Описание фильма", key="admin_overview")
        year = st.number_input("Год выпуска", min_value=1900, max_value=2100, key="admin_year")
        genres = st.text_input("Жанр", key="genres")
        poster = st.text_input("Ссылка на постер", key="admin_poster")
        if st.button("Добавить фильм", key="admin_add_movie"):
            conn = get_connection()
            result = add_movie(conn, title, overview, year, poster, genres)
            if "error" in result:
                st.warning(result["error"])
            else:
                st.success(f"Фильм добавлен! ID: {result['movie_id']}")
                st.json(result)

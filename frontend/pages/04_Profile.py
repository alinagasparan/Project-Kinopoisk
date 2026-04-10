import streamlit as st
from assets.styles import apply_styles  
from components.movie_cards import render_movie_card
from backend.main1 import get_user_profile, change_user_avatar, add_movie, get_all_movies_with_details

if "user" not in st.session_state:
    st.warning("Сначала войдите!")
    st.stop()

st.set_page_config(page_title="Profile", layout="wide")
apply_styles()

user_info = get_user_profile(st.session_state.user['id'])

# --- ОПРЕДЕЛЕНИЕ ФРАГМЕНТА ДЛЯ АДМИНКИ ---
@st.fragment
def render_admin_panel():
    st.divider()
    st.subheader("Добавление нового фильма")

    # Форма внутри фрагмента изолирует ввод данных от остальной страницы
    with st.form("admin_add_movie_form", clear_on_submit=True):
        title = st.text_input("Название фильма")
        overview = st.text_area("Описание фильма")
        year = st.number_input("Год выпуска", min_value=1900, max_value=2100, value=2024)
        genres_input = st.text_input("Жанры (через запятую)")
        poster = st.text_input("Ссылка на постер")
        
        submit_button = st.form_submit_button("Добавить фильм")

        if submit_button:
            if not title or not poster:
                st.warning("Название и ссылка на постер обязательны!")
            else:
                result = add_movie(title, overview, year, poster, genres_input)
                
                if isinstance(result, dict) and "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"Фильм '{title}' успешно добавлен!")
                    # Очищаем кеш, чтобы фильм появился в поиске/каталоге без перезагрузки профиля
                    st.cache_data.clear()

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
        if st.button("Выйти из аккаунта"):
            del st.session_state.user
            st.session_state.is_logged_in = False
            st.switch_page("pages/01_Home.py")

    st.divider()

    tab_seen, tab_plan = st.tabs(["✅ Просмотрено", "⏳ Запланировано"])

    # Загрузка данных (происходит только при общей перезагрузке страницы)
    with st.spinner("Загружаем постеры ваших фильмов..."):
        all_movies_data = get_all_movies_with_details()
        poster_map = {}
        for m in all_movies_data:
            mid = m.get('movie_id') or m.get('id')
            if mid:
                poster_map[mid] = m.get('poster_link') or m.get('poster') or ""

    def render_custom_grid(user_movies, empty_msg):
        if not user_movies:
            st.info(empty_msg)
            return

        cols_per_row = 5
        for i in range(0, len(user_movies), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(user_movies):
                    film = user_movies[i + j]
                    m_id = film['movie_id']
                    img_url = poster_map.get(m_id) or ""
                    
                    with cols[j]:
                        render_movie_card(
                            movie_id=m_id,
                            title=film['title'],
                            img_url=img_url
                        )

    with tab_seen:
        render_custom_grid(user_info['seen'], "Вы еще не отметили ни одного просмотренного фильма.")

    with tab_plan:
        render_custom_grid(user_info['planned'], "Ваш список 'Запланировано' пока пуст.")

    # --- ВЫЗОВ ФРАГМЕНТА АДМИНА ---
    if user_info['username'].lower() == "admin":
        render_admin_panel()
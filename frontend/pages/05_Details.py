import streamlit as st
from assets.styles import apply_styles
from backend.main1 import get_films_by_search

st.set_page_config(page_title="Детали фильма", layout="wide")
apply_styles()

movie_title = st.session_state.get("selected_movie")
movie_id = st.session_state.get("selected_film_id")

if not movie_title or not movie_id:
    st.warning("Фильм не выбран. Пожалуйста, вернитесь на главную страницу.")
    if st.button("На главную"):
        st.switch_page("pages/01_Home.py")
    st.stop()

found_films = get_films_by_search(movie_title)

movie_data = next((f for f in found_films if f["id"] == movie_id), None)

if movie_data:
    if st.button("← Назад к каталогу"):
        st.switch_page("pages/01_Home.py")

    col_img, col_info = st.columns([1, 2], gap="large")

    with col_img:
        #постер
        st.image("https://i.pinimg.com/736x/51/71/24/517124fcea493bad8d49e69181131902.jpg", use_container_width=True)
        
        # Плашка с рейтингом
        st.markdown(f"""
            <div style="background: #610f2e; padding: 15px; border-radius: 12px; text-align: center; margin-top: 10px;">
                <span style="color: white; font-size: 1.2rem; font-weight: bold;">★ Рейтинг: {movie_data['rating']}</span>
            </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.title(movie_data['title'])

        st.markdown(f"""
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <span style="background: #1e223b; padding: 5px 15px; border-radius: 20px; color: #e2e8f0;">📅 {movie_data['year']}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Описание")
        st.write(movie_data['description'] if movie_data['description'] else "Описание отсутствует.")
        
        st.divider()
        
    
        st.selectbox("Статус", ["Не смотрел", "Запланировано", "Просмотрено"], key="status_select")

    # Секция комментариев
    st.divider()
    st.subheader("💬 Комментарии")
    with st.container():
        comment = st.text_area("Оставь свой отзыв:", placeholder="Напишите, что вы думаете о фильме...")
        if st.button("Отправить"):
            if comment:
                st.success("Отзыв отправлен!")
            else:
                st.error("Текст комментария не может быть пустым.")

else:
    st.error("К сожалению, информация о фильме не найдена.")
    if st.button("Вернуться назад"):
        st.switch_page("pages/01_Home.py")
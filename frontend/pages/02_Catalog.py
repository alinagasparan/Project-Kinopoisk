import streamlit as st
from backend.main1 import get_all_movies_with_details,  get_movies_by_genre_front
from components.movie_cards import render_movie_card
from assets.styles import apply_styles, filter_panel

st.set_page_config(page_title="Catalog", layout="wide")
apply_styles()

st.title("Библиотека кино")

BATCH_SIZE = 30
if "catalog_shown" not in st.session_state:
    st.session_state.catalog_shown = BATCH_SIZE

def normalize(film: dict) -> dict:
    """Приводим данные из разных функций к единому стандарту"""
    return {
        "id":     film.get("id") or film.get("movie_id"),
        "title":  film.get("title", ""),
        "poster": film.get("poster") or film.get("poster_link", ""),
        "year":   film.get("year") or film.get("release_year"),
    }

with st.container(key="catalog"):
    main_col, filter_col = st.columns([4, 1])

    with filter_col:
        st.markdown("### 🔍 Фильтры")
        selected_genres, sort_selection, selected_year = filter_panel()

        if st.button("Сбросить фильтры", use_container_width=True):
            st.session_state.catalog_shown = BATCH_SIZE
            st.rerun()

    with st.spinner("Загрузка фильмов..."):
        if not selected_genres:
            # Если жанры не выбраны — тянем всё из базы
            raw_data = get_all_movies_with_details()
        else:
            # Если жанры выбраны — ищем пересечение (фильмы, подходящие под ВСЕ жанры)
            genre_sets = []
            movie_map = {}
            for g in selected_genres:
                films = get_movies_by_genre_front(g) 
                current_ids = set()
                for f in films:
                    f_norm = normalize(f)
                    mid = f_norm["id"]
                    current_ids.add(mid)
                    movie_map[mid] = f_norm
                genre_sets.append(current_ids)
            
            common_ids = set.intersection(*genre_sets) if genre_sets else set()
            raw_data = [movie_map[mid] for mid in common_ids]

    # Нормализуем результат
    movies = [normalize(f) for f in (raw_data or [])]

    if sort_selection == "По алфавиту":
        movies.sort(key=lambda x: str(x["title"]).lower())
    elif sort_selection == "По дате выхода":
        movies.sort(key=lambda x: x["year"] if x["year"] else 0, reverse=True)

    with main_col:
        if not movies:
            st.warning("Ничего не найдено с такими фильтрами 🍿")
        else:
            shown = st.session_state.catalog_shown
            page_data = movies[:shown]

            cols_per_row = 3
            for i in range(0, len(page_data), cols_per_row):
                columns = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(page_data):
                        m = page_data[i + j]
                        with columns[j]:
                            render_movie_card(
                                movie_id=m["id"],
                                title=m["title"],
                                img_url=m["poster"]
                            )

            if shown < len(movies):
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                if st.button("Загрузить ещё", use_container_width=True):
                    st.session_state.catalog_shown += BATCH_SIZE
                    st.rerun()
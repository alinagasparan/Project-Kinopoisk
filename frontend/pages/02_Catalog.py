import streamlit as st
from backend.main1 import get_all_movies_with_details,  get_movies_by_genre_front, get_films_by_year
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
        all_filters_results = []
        movie_map = {}

        # Фильтр по жанрам
        if selected_genres:
            genre_sets = []
            for g in selected_genres:
                films = get_movies_by_genre_front(g) 
                current_ids = set()
                for f in films:
                    f_norm = normalize(f)
                    mid = f_norm["id"]
                    current_ids.add(mid)
                    movie_map[mid] = f_norm
                genre_sets.append(current_ids)
            
            if genre_sets:
                # Находим фильмы, которые подходят под ВСЕ выбранные жанры
                common_genre_ids = set.intersection(*genre_sets)
                all_filters_results.append(common_genre_ids)

        # фильтр по году
        if selected_year and selected_year != "Любой":
            year_films = get_films_by_year(selected_year)
            year_ids = set()
            for f in year_films:
                f_norm = normalize(f)
                mid = f_norm["id"]
                year_ids.add(mid)
                movie_map[mid] = f_norm
            all_filters_results.append(year_ids)

        if not all_filters_results:
            # Если ни один фильтр не выбран — берем всё
            raw_data = get_all_movies_with_details()
        else:
            # Находим пересечение ЖАНРОВ и ГОДА
            final_ids = set.intersection(*all_filters_results)
            raw_data = [movie_map[mid] for mid in final_ids]

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
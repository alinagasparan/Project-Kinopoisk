import streamlit as st

def render_movie_card(film_id, title, img_url):
    with st.container(key=f"movie_card_{film_id}"):
        
        st.markdown(f"""
            <img src="{img_url}" 
            style="width: 100%;
            aspect-ratio: 2/3;
            object-fit: cover; 
            border-radius: 14px 14px 0 0; 
            display: block;
            padding: 10px">
        """, unsafe_allow_html=True)

        if st.button(title, key=f"btn_{film_id}", use_container_width=True):
            st.session_state.selected_movie = title
            st.session_state.selected_film_id = film_id
            st.switch_page("pages/05_Details.py")
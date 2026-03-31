import streamlit as st
from pathlib import Path

FRONTEND_DIR = Path(__file__).parent

def show_sidebar_mascot():
    """Вывод маскота"""

    mascot_path = FRONTEND_DIR / "assets" / "cinecat.png"
    
    with st.sidebar:
        if mascot_path.exists():
            st.image(str(mascot_path)) 
        else:
            st.title("🐱")
            st.warning("Кот потерялся (файл не найден)")

        st.info("Привет! Я Кино-Кот, твой помощник. Давай выберем фильм?")
        st.button("Жми, помогу!", use_container_width=True)
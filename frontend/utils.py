import streamlit as st
from pathlib import Path

FRONTEND_DIR = Path(__file__).resolve().parent

def show_mascot():
    mascot_path = FRONTEND_DIR / "assets" / "cinecat.png"
    
    with st.container():
        st.image(str(mascot_path), width=150) 
        st.write("Привет! Я Кинокотик. Помочь?")
        st.markdown('</div>', unsafe_allow_html=True)

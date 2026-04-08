import streamlit as st
from pathlib import Path
import base64

FRONTEND_DIR = Path(__file__).resolve().parent

def show_mascot():
    mascot_path = FRONTEND_DIR / "assets" / "cinemindcat.png"
    
    with open(mascot_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()
    
    st.markdown(f"""
        <div class="mascot-container">
            <img src="data:image/png;base64,{img_data}" width="100">
            <p style="
                color: white;
                background: #242330;
                padding: 5px 10px;
                border-radius: 8px;
                font-size: 12px;
                text-align: center;
                margin-top: 5px;
            ">Привет! Помочь?</p>
        </div>
    """, unsafe_allow_html=True)

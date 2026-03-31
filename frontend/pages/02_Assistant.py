import streamlit as st
from assets.styles import apply_styles          
from utils import show_sidebar_mascot  

st.set_page_config(page_title="Cinemind Assistant", layout="centered")
apply_styles()
show_sidebar_mascot()

st.title("🤖 Твой кино-бро")
st.caption("Помощник Cinemind на связи. Готов обсудить кино!")

# Инициализация истории чата в браузере пользователя
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Привет! Я твой персональный Кино-кот помощник. Какой жанр сегодня в приоритете?"}
    ]

# Отрисовка всех сообщений, которые хранятся в текущей сессии
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Напиши свои предпочтения..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = "Твой запрос принят! Как только мой бэкенд-мозг допилят, я проанализирую это и выдам идеальный фильм. 🍿"
    
    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.markdown("### О помощнике")
    st.info("Кино-кот использует ML для анализа твоих предпочтений. (В разработке)")
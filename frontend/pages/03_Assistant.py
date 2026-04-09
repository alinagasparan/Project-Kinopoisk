import streamlit as st
from assets.styles import apply_styles
import backend.main1 as logic  

st.set_page_config(page_title="Cinemind Assistant", layout="wide", page_icon="🐱")
apply_styles()

st.title("🐱 Твой Кино-Кот")

# Если пользователь не вошел
if not st.session_state.get("is_logged_in"):
    st.warning("Мяу! 🐾 Чтобы поболтать с Кино-котом, нужно войти в аккаунт.")
    if st.button("Перейти к авторизации"):
        st.switch_page("pages/06_Auth.py") 
    st.stop()

current_user = st.session_state.user
user_id = current_user['id']
username = current_user['username']

st.caption(f"Мяу, {username}! Помощник Cinemind на связи. Разваливайся поудобнее, обсудим кино!")

# Создаем уникальный ключ для истории текущего пользователя
history_key = f"messages_{user_id}"

if history_key not in st.session_state:
    st.session_state[history_key] = [
        {"role": "assistant", "content": f"Мяу, {username}! Я твой персональный Кино-кот. Расскажи, о чем должен быть фильм, а я выберу лапкой что-нибудь классное! 🐾"}
    ]

# Отрисовка истории сообщений текущего пользователя
for message in st.session_state[history_key]:
    with st.chat_message(message["role"], avatar="🐱" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Обработка ввода пользователя
if prompt := st.chat_input("Напиши свои предпочтения (например, 'хочу кино про шпионов')..."):
    # Добавляем сообщение пользователя в его личную историю
    st.session_state[history_key].append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Получаем ответ от ML-модели
    with st.chat_message("assistant", avatar="🐱"):
        with st.spinner("Кино-кот шуршит в коробках с фильмами... 🐾"):
            try:
                results = logic.chat_with_ml(prompt)
            except Exception as e:
                results = [{"error": f"Ошибка системы: {str(e)}"}]

            # Логика формирования ответа
            if not results:
                response = "Хм, в моих мисках пусто — ничего не нашлось. Попробуй уточнить запрос, мяу! 🐈‍⬛"
            
            elif isinstance(results, list) and len(results) > 0 and "error" in results[0]:
                error_msg = results[0]["error"]
                response = f"Ой, у котика хвост запутался... Ошибка: `{error_msg}` 🙀"
            
            else:
                response = "Смотри, какую годноту я выудил для тебя:\n\n"
                for film in results:
                    title = film.get("title", "Без названия")
                    year = film.get("year", "н/д")
                    rating = film.get("rating", "—")
                    genre = film.get("genre", "не указан")
                    overview = film.get("overview") or "Описание где-то потерялось..."
                    
                    response += f"🎬 **{title}** ({year})\n"
                    response += f"⭐ Рейтинг: {rating} | 🎭 Жанр: {genre}\n"
                    response += f"📝 {overview[:200]}...\n\n"
                
                response += "Что-нибудь из этого заставляет тебя мурчать? 🐈"

            st.markdown(response)
    
    # Сохраняем ответ ассистента в личную историю пользователя
    st.session_state[history_key].append({"role": "assistant", "content": response})
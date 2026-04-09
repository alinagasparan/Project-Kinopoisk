import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
import sys
import re
import pickle 
import os
from pathlib import Path

# Настройка NLTK для избежания ошибок
def setup_nltk():
    """Настройка NLTK с правильными путями"""
    try:
        # Создаем папку для данных NLTK в текущей директории
        nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        nltk.data.path.append(nltk_data_dir)
        
        # Скачиваем stopwords с подавлением вывода
        nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)
        return set(stopwords.words('english'))
    except Exception as e:
        print(f"Предупреждение: Не удалось загрузить stopwords: {e}")
        return set()

# Инициализация стоп-слов
try:
    stop_words = setup_nltk()
except:
    stop_words = set()

# Инициализирует Sentence Transformer модель (используем более легкую модель)
def initialize_model():
    """Инициализация модели с обработкой ошибок"""
    try:
        # Используем более легкую модель для уменьшения времени загрузки
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Ошибка загрузки модели: {e}")
        raise

# Функция, которая создает список стоп-слов и слов из списка
def get_stop_phrases():
    english_stopwords = stop_words if stop_words else setup_nltk()
    
    custom_stop_phrases = {
        "hi", "hello", "movie about", "show me", "i want a movie about", 
        "please", "can you", "find", "give me", "search for", 
        "how are you", "i want", "the", "a", "an", "and", "or", "but"
    }
    return english_stopwords.union(custom_stop_phrases)

# Функция, которая убирает слова и оставляет только ключевые слова
def extract_keywords(query, stop_phrases):
    query = query.lower()
    words = query.split()
    keywords = [w for w in words if w not in stop_phrases and len(w) > 2]
    return keywords

def keyword_mask(text, keywords):
    if not keywords:
        return True
    text = text.lower()
    return any(k in text for k in keywords)  # Изменено на any для лучшего поиска

# Функция извлечения жанров из списка
def extract_genres(query, all_genres):
    if not all_genres:
        return []
    
    query_lower = query.lower()
    matched = []
    
    for genre in all_genres:
        genre_lower = genre.lower()
        # Проверяем вхождение жанра в запрос
        if genre_lower in query_lower:
            matched.append(genre)
        # Проверяем отдельные слова
        elif any(word in genre_lower for word in query_lower.split() if len(word) > 3):
            matched.append(genre)
    
    return list(set(matched))

# Загрузка файлов с правильной обработкой пути
def download_csv():
    """Загрузка CSV файла с поиском в разных местах"""
    possible_paths = [
        './movies_posters.csv',
        './data/movies_posters.csv',
        '../movies_posters.csv',
        Path(__file__).parent / 'movies_posters.csv',
        Path(__file__).parent.parent / 'movies_posters.csv'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                # Проверяем наличие нужных колонок
                if 'synopsis' not in df.columns and 'Overview' in df.columns:
                    df['synopsis'] = df['Overview']
                df = df.dropna(subset=['synopsis'])
                print(f"Файл загружен: {path}")
                return df
            except Exception as e:
                print(f"Ошибка загрузки {path}: {e}")
                continue
    
    raise FileNotFoundError("Не найден файл movies_posters.csv")

# Функция подготовки данных о жанре
def prepare_genre(df):
    if 'genres' in df.columns:
        df['genres'] = df['genres'].fillna('')
        df['Genre_List'] = df['genres'].apply(
            lambda g: [x.strip().lower() for x in str(g).split(',') if x.strip()]
        )
        all_genres = set()
        for g_list in df['Genre_List']:
            for genre in g_list:
                if genre:  
                    all_genres.add(genre)
        return df, all_genres
    return df, set()

def save_all(df, movie_embeddings, kmeans, filename='movie_data.pkl'):
    """Сохранение данных с проверкой"""
    try:
        with open(filename, 'wb') as f:
            pickle.dump({
                'df': df, 
                'embeddings': movie_embeddings, 
                'kmeans': kmeans
            }, f)
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def load_all(filename='movie_data.pkl'):
    """Загрузка данных с проверкой"""
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                return data['df'], data['embeddings'], data['kmeans']
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
    return None, None, None

def create_movie_embeddings(df, model):
    """Создание эмбеддингов с обработкой ошибок"""
    try:
        text_column = 'synopsis' if 'synopsis' in df.columns else 'Overview'
        movie_embeddings = model.encode(
            df[text_column].tolist(), 
            show_progress_bar=False,  # Отключаем прогресс-бар для Streamlit
            batch_size=32,  # Уменьшаем batch size
            convert_to_numpy=True
        )
        return movie_embeddings
    except Exception as e:
        print(f"Ошибка создания эмбеддингов: {e}")
        raise

# Функция создания кластеров
def perform_clustering(movie_embeddings):
    """Кластеризация с обработкой ошибок"""
    k = min(50, len(movie_embeddings) // 10)  # Адаптивное количество кластеров
    if k < 2:
        k = 2
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(movie_embeddings)
    return kmeans

# Фильтрация по жанрам
def filter_by_genres(df, query_genres):
    if not query_genres or 'Genre_List' not in df.columns:
        return df.copy()
    
    genre_mask = df['Genre_List'].apply(
        lambda gs: any(
            any(qg in g or g in qg for g in gs) 
            for qg in query_genres
        )
    )
    return df[genre_mask].copy() if genre_mask.any() else df.copy()

# Фильтрует фильмы по ключевым словам в описании
def filter_by_keywords(df, keywords):
    if not keywords:
        return df.copy()
    
    text_column = 'synopsis' if 'synopsis' in df.columns else 'Overview'
    mask = df[text_column].apply(lambda x: keyword_mask(x, keywords))
    return df[mask].copy() if mask.any() else df.copy()

# Функция нахождения наиболее подходящих кластеров
def get_relevant_clusters(query_vec, centroids):
    n_clusters = min(5, len(centroids))
    cluster_scores = cosine_similarity(query_vec, centroids)[0]
    best_clusters = np.argsort(cluster_scores)[::-1][:n_clusters]
    return best_clusters

# Объединяет индексы из фильтрации и кластеров
def combine_indices(filtered_indices, cluster_indices, max_indices=100):
    combined = list(dict.fromkeys(filtered_indices + cluster_indices))
    return combined[:max_indices]

# Вычисляет бонус за совпадение жанров
def calculate_genre_bonus(row, query_genres):
    if not query_genres or 'Genre_List' not in row.index:
        return 0
    
    movie_genres = row['Genre_List']
    matches = 0
    for qg in query_genres:
        for mg in movie_genres:
            if qg in mg or mg in qg:
                matches += 1
                break
    
    if matches:
        return min(0.15, matches * 0.05)
    return 0

def calculate_rating_score(rating_str):
    if pd.isna(rating_str) or rating_str == 'N/A':
        return 0
    
    try:
        match = re.search(r'(\d+\.?\d*)', str(rating_str))
        if match:
            rating = float(match.group(1))
            return min(1.0, rating / 10.0)  # Нормализуем к 10-балльной шкале
    except:
        pass
    return 0

# Вычисляет итоговый скор фильма
def calculate_final_score(score, genre_bonus, rating_score):
    return score * 0.7 + genre_bonus + rating_score * 0.2

# Ранжирует фильмы и возвращает топ результатов
def rank_movies(df, combined_indices, scores, query_genres, top_n=50):
    if len(scores) == 0:
        return []
    
    top_n = min(top_n, len(scores))
    top_positions = np.argsort(scores)[::-1][:top_n]
    final_results = []
    
    for pos in top_positions:
        original_idx = combined_indices[pos]
        row = df.iloc[original_idx]
        score = scores[pos]
        genre_bonus = calculate_genre_bonus(row, query_genres)
        rating_score = calculate_rating_score(row.get('rating', 'N/A'))
        final_score = calculate_final_score(score, genre_bonus, rating_score)
        final_results.append((original_idx, final_score))
    
    return sorted(final_results, key=lambda x: x[1], reverse=True)

def train_model():
    """Обучение модели с обработкой ошибок"""
    print("Загрузка данных...")
    df = download_csv()
    
    print("Подготовка данных...")
    df, all_genres = prepare_genre(df)
    
    print("Инициализация модели...")
    model = initialize_model()
    
    print("Создание эмбеддингов фильмов...")
    movie_embeddings = create_movie_embeddings(df, model)
    
    print("Кластеризация...")
    kmeans = perform_clustering(movie_embeddings)
    
    # Добавляем кластеры в DataFrame
    df['cluster'] = kmeans.labels_
    
    print("Сохранение обученной модели...")
    save_all(df, movie_embeddings, kmeans)
    
    return df, movie_embeddings, kmeans, all_genres, model

# Глобальные переменные
df = None
movie_embeddings = None
kmeans = None
all_genres = None
model = None
centroids = None
stop_phrases = None

def initialize_system():
    """Инициализация всей системы"""
    global df, movie_embeddings, kmeans, all_genres, model, centroids, stop_phrases
    
    # Загружаем или обучаем модель
    print("Проверка наличия сохраненной модели...")
    df, movie_embeddings, kmeans = load_all()
    
    if df is None:
        print("Модель не найдена. Начинаем обучение...")
        df, movie_embeddings, kmeans, all_genres, model = train_model()
    else:
        print("Модель загружена. Подготовка к использованию...")
        df, all_genres = prepare_genre(df)
        model = initialize_model()
        # Убеждаемся, что кластеры есть в df
        if 'cluster' not in df.columns and kmeans is not None:
            df['cluster'] = kmeans.labels_
    
    # Получаем центроиды кластеров
    if kmeans is not None:
        centroids = kmeans.cluster_centers_
    stop_phrases = get_stop_phrases()
    
    print("Система готова к работе!")

# Функция для поиска фильмов
def search_movies(query, top_k=10):
    """Поиск фильмов с обработкой ошибок"""
    global df, movie_embeddings, kmeans, all_genres, model, centroids, stop_phrases
    
    # Проверяем инициализацию
    if df is None:
        initialize_system()
    
    if df is None or df.empty:
        return []
    
    try:
        keywords = extract_keywords(query, stop_phrases)
        query_genres = extract_genres(query, all_genres)
        
        df_filtered = filter_by_genres(df, query_genres)
        df_filtered = filter_by_keywords(df_filtered, keywords)
        
        if df_filtered.empty:
            df_filtered = df.copy()
        
        query_vec = model.encode([query])
        
        if centroids is not None and len(centroids) > 0:
            best_clusters = get_relevant_clusters(query_vec, centroids)
            cluster_mask = df['cluster'].isin(best_clusters)
            cluster_indices = df[cluster_mask].index.tolist()
        else:
            cluster_indices = []
        
        filtered_indices = df_filtered.index.tolist()
        combined_indices = combine_indices(filtered_indices, cluster_indices)
        
        if len(combined_indices) == 0:
            combined_indices = list(range(len(df)))
        
        combined_embeddings = movie_embeddings[combined_indices]
        scores = cosine_similarity(query_vec, combined_embeddings)[0]
        
        ranked_results = rank_movies(df, combined_indices, scores, query_genres, top_k)
        
        results = []
        for rank, (idx, score) in enumerate(ranked_results, 1):
            row = df.iloc[idx]
            
            # Форматирование рейтинга для отображения
            rating_value = row.get('rating', 'N/A')
            if pd.notna(rating_value) and rating_value != 'N/A':
                try:
                    match = re.search(r'(\d+\.?\d*)', str(rating_value))
                    if match:
                        rating_value = match.group(1)
                except:
                    pass
            
            # Получаем правильные названия колонок
            title = row.get('title', row.get('Series_Title', 'Unknown'))
            year = row.get('year', row.get('Released_Year', 'N/A'))
            genres = row.get('genres', row.get('Genre', 'N/A'))
            director = row.get('directors', row.get('Director', 'N/A'))
            cast = row.get('cast', row.get('Star1', 'N/A'))
            synopsis = row.get('synopsis', row.get('Overview', 'No description'))
            poster_url = row.get('poster_url', row.get('Poster_Link', ''))
            
            results.append({
                "rank": rank,
                "title": str(title),
                "year": str(year),
                "genre": str(genres),
                "rating": str(rating_value),
                "director": str(director),
                "cast": str(cast),
                "synopsis": str(synopsis),
                "poster_url": str(poster_url),
                "score": float(score)
            })
        
        return results
        
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return []

# Инициализируем систему при загрузке модуля
initialize_system()


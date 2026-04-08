import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from transformers import pipeline


def initialize_nltk():
    nltk.download('stopwords', quiet=True)
    return set(stopwords.words('english'))

#Инициализирует Sentence Transformer модель
def initialize_model():
    return SentenceTransformer('sentence-transformers/msmarco-distilbert-base-tas-b')

#Функция, которая создает список стоп-слов и слов из списка
def get_stop_phrases():
    english_stopwords = set(stopwords.words('english'))

    custom_stop_phrases = [
        "hi", "hello", "movie about", "show me", "i want a movie about", "please", "can you",
        "find",
        "give me", "search for", "how are you", "i want"
    ]
    return english_stopwords.union(custom_stop_phrases)

#Функция, которая убирает слова и оставляет только ключевые слова
def extract_keywords(query, stop_phrases):
    query = query.lower()
    words = query.split()
    keywords = [w for w in words if w not in stop_phrases]
    return keywords


#Функция извлечения жанров из списка(возможно аналогия готова)
def extract_genres(query, all_genres):
   
    query_lower = query.lower()
    matched = []
    
    for genre in all_genres:
        genre_lower = genre.lower()
      
        if genre_lower in query_lower or query_lower in genre_lower:
            matched.append(genre)
      
        elif any(word in genre_lower for word in query_lower.split() if len(word) > 3):
            matched.append(genre)
    
    return list(set(matched))

#Загрузка файлов из бзд
def dowonload_csv():
    df = pd.read_csv('./imdb_top_1000.csv')
    df = df.dropna(subset=['Overview'])
    return df

#Функция подготовки данных о жанре
def prepare_genre(df):
    if 'Genre' in df.columns:
        df['Genre'] = df['Genre'].fillna('')
        df['Genre_List'] = df['Genre'].apply(lambda g: [x.strip().lower() for x in str(g).split(',') if x.strip()])
        all_genres = set()
        for g_list in df['Genre_List']:
            for genre in g_list:
                if genre:  
                    all_genres.add(genre)
        return df, all_genres
    return df, set()

#Функция создания эмбеддинга
def create_movie_embeddings(df, model):
    model = SentenceTransformer('sentence-transformers/msmarco-distilbert-base-tas-b')
    movie_embeddings = model.encode(df['Overview'].tolist(), show_progress_bar=True)
    return movie_embeddings

#Функция создания кластеров
def perform_clustering(df, movie_embeddings):
    k=50
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(movie_embeddings)
    centroids = kmeans.cluster_centers_
    return df,centroids

#Фильтрация по жанрам
def filter_by_genres(df, query_genres):
    if not query_genres:
        return df.copy()
    genre_mask = df['Genre_List'].apply(
        lambda gs: any(
            any(qg in g or g in qg for g in gs) 
            for qg in query_genres
        )
    )
    return df[genre_mask].copy()


#Фильтрует фильмы по ключевым словам в описании
def filter_by_keywords(df, keywords):
    if not keywords:
        return df.copy()
    
    return df[df['Overview'].apply(lambda x: keyword_mask(x, keywords))]


#Функция нахождения наиболее подходящих кластеров
def get_relevant_clusters(query_vec, centroids):
    n_clusters=5
    cluster_scores = cosine_similarity(query_vec, centroids)[0]
    best_clusters = np.argsort(cluster_scores)[::-1][:min(n_clusters, len(centroids))]
    return best_clusters


#Объединяет индексы из фильтрации и кластеров
def combine_indices(filtered_indices, cluster_indices, max_indices=100):
    combined = list(dict.fromkeys(filtered_indices + cluster_indices))
    return combined[:max_indices]

#Вычисляет бонус за совпадение жанров
def calculate_genre_bonus(row, query_genres):
    if not query_genres:
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

#Вычисляет нормализованный рейтинг IMDB
def calculate_rating_score(row):
    rating = row.get('IMDB_Rating', 0)
    if pd.notna(rating):
        return float(rating) / 10
    return 0

#Вычисляет нормализованный Metascore
def calculate_metascore(row):
    meta = row.get('Meta_score', 0)
    if pd.notna(meta):
        return float(meta) / 100
    return 0

 #Вычисляет итоговый скор фильма
def calculate_final_score(score, genre_bonus, rating_score, meta_score):
    return score * 0.7 + rating_score * 0.2 + meta_score * 0.05 + genre_bonus

#Ранжирует фильмы и возвращает топ результатов
def rank_movies(df, combined_indices, scores, query_genres, top_n=50):
    top_positions = np.argsort(scores)[::-1][:min(top_n, len(scores))]
    final_results = []
    for pos in top_positions:
        original_idx = combined_indices[pos]
        row = df.iloc[original_idx]
        score = scores[pos]
        genre_bonus = calculate_genre_bonus(row, query_genres)
        rating_score = calculate_rating_score(row)
        meta_score = calculate_metascore(row)
        final_score = calculate_final_score(score, genre_bonus, rating_score, meta_score)
        final_results.append((original_idx, final_score))
    
    return sorted(final_results, key=lambda x: x[1], reverse=True)


def process_query(query, df, all_genres, model, movie_embeddings, centroids, stop_phrases, ner_pipeline):
    
    keywords = extract_keywords(query, stop_phrases)
    query_genres = extract_genres(query, all_genres)
    entities = extract_entities(query, ner_pipeline)
    
    df_filtered = filter_by_genres(df, query_genres)
    df_filtered = filter_by_keywords(df_filtered, keywords)
    
    if df_filtered.empty:
        print("По вашему запросу фильмов не найдено. Ищем похожие...")
        df_filtered = df.copy()
    
    query_vec = model.encode([query])
    
    best_clusters = get_relevant_clusters(query_vec, centroids)
    
    filtered_indices = df_filtered.index.tolist()
    cluster_mask = df['cluster'].isin(best_clusters)
    cluster_indices = df[cluster_mask].index.tolist()
    
    combined_indices = combine_indices(filtered_indices, cluster_indices)
    
    if len(combined_indices) == 0:
        combined_indices = list(range(len(df)))
    
    combined_embeddings = movie_embeddings[combined_indices]
    scores = cosine_similarity(query_vec, combined_embeddings)[0]
    
    ranked_results = rank_movies(df, combined_indices, scores, query_genres)
    
    return ranked_results




stop_phrases = get_stop_phrases()
df = download_csv()
df, all_genres = prepare_genre(df)
model = initialize_model()
movie_embeddings = create_movie_embeddings(df, model)
df, centroids = perform_clustering(df, movie_embeddings)


def search_movies(query, top_k=10):    
    keywords = extract_keywords(query, stop_phrases)
    query_genres = extract_genres(query, all_genres)
    
    df_filtered = filter_by_genres(df, query_genres)
    df_filtered = filter_by_keywords(df_filtered, keywords)
    
    if df_filtered.empty:
        df_filtered = df.copy()
    
    query_vec = model.encode([query])
    
    best_clusters = get_relevant_clusters(query_vec, centroids)
    
    filtered_indices = df_filtered.index.tolist()
    cluster_mask = df['cluster'].isin(best_clusters)
    cluster_indices = df[cluster_mask].index.tolist()
    
    combined_indices = combine_indices(filtered_indices, cluster_indices)
    
    if len(combined_indices) == 0:
        combined_indices = list(range(len(df)))
    
    combined_embeddings = movie_embeddings[combined_indices]
    scores = cosine_similarity(query_vec, combined_embeddings)[0]
    
    ranked_results = rank_movies(df, combined_indices, scores, query_genres, top_k)
    
    results = []
    for rank, (idx, score) in enumerate(ranked_results, 1):
        row = df.iloc[idx]
        results.append({
            "rank": rank,
            "title": row.get('Series_Title', row.get('Title', 'Unknown')),
            "year": str(row.get('Released_Year', row.get('Year', 'N/A'))),
            "genre": row.get('Genre', 'N/A'),
            "rating": str(row.get('IMDB_Rating', 'N/A')),
            "meta_score": str(row.get('Meta_score', 'N/A')),
            "director": row.get('Director', 'N/A'),
            "stars": f"{row.get('Star1', '')}, {row.get('Star2', '')}, {row.get('Star3', '')}".strip(', '),
            "overview": row.get('Overview', 'No description'),
            "score": float(score)
        })
    
    return results







   # query = input("\n Опиши фильм: ")
   # if query.lower() in ('exit', 'quit'):
     #   break


   # keywords = extract_keywords(query,stop_phrases)# что-то надо 
   # query_genres = extract_genres(query, all_genres)

   # def genre_mask_func(genre_cell, query_genres):
      #  genres = [g.strip().lower() for g in genre_cell.split(',')]
      #  return any(q.lower() in genres for q in query_genres)
        
    #if query_genres:
        #genre_mask = df['Genre_List'].apply(
           # lambda gs: any(
              #  any(qg in g or g in qg for g in gs) 
              #  for qg in query_genres
          #  )
      #  )
       # df_filtered = df[genre_mask].copy()
   # else:
      #  df_filtered = df.copy()
    
    
   # def keyword_mask(text, keywords):
      #  text = text.lower()
      #  return all(k in text for k in keywords)

    #if keywords:
      #  df_filtered = df_filtered[df_filtered['Overview'].apply(lambda x: keyword_mask(x, keywords))]

   # if df_filtered.empty:
    #    print("По вашему запросу фильмов не найдено. Но может вас заинтересует следующее")
    
   # query_vec = model.encode([query])

   # filtered_indices = df_filtered.index.tolist()
   # cluster_mask = df['cluster'].isin(best_clusters)
   # cluster_indices = df[cluster_mask].index.tolist()
    
   # combined_indices = list(dict.fromkeys(filtered_indices + cluster_indices))[:100]
    
   # if len(combined_indices) == 0:
   #     combined_indices = list(range(len(df)))
    
   # combined_embeddings = movie_embeddings[combined_indices]
   # scores = cosine_similarity(query_vec, combined_embeddings)[0]
    
   # top_n = min(50, len(scores))
   # top_positions = np.argsort(scores)[::-1][:top_n]
    
   # final_results = []
   # for pos in top_positions:
   #     original_idx = combined_indices[pos]
   #     row = df.iloc[original_idx]
        
   #     score = scores[pos]
        
    #    genre_bonus = 0
    #    if query_genres and 'Genre_List' in df.columns and len(df['Genre_List']) > 0:
     #       movie_genres = row['Genre_List']
     #       matches = 0
     #       for qg in query_genres:
     #           for mg in movie_genres:
      #              if qg in mg or mg in qg:
      #                  matches += 1
      #                  break
      #      if matches:
      #          genre_bonus = min(0.15, matches * 0.05) 
        
       # rating = row.get('IMDB_Rating', 0)
       # if pd.notna(rating):
      #      vote_score = float(rating) / 10
      #  else:
       #     vote_score = 0
        
      #  meta = row.get('Meta_score', 0)
      #  if pd.notna(meta):
       #     meta_score = float(meta) / 100
      #  else:
       #     meta_score = 0
        
     #   final_score = score * 0.7 + vote_score * 0.2 + meta_score * 0.05 + genre_bonus
     #   final_results.append((original_idx, final_score))
    
   # if not final_results:
     #   print("\n Ничего не найдено.\n")
    #    continue
    
  #  final_results = sorted(final_results, key=lambda x: x[1], reverse=True)
  #  top_final = [idx for idx, _ in final_results[:10]]
    
  #  print(f"\n Топ-10 фильмов:\n")
   # print("="*80)
   # for rank, i in enumerate(top_final, 1):
    #    row = df.iloc[i]
    #    title = row.get('Series_Title', row.get('Title', 'Unknown'))
    #    year = row.get('Released_Year', row.get('Year', 'N/A'))
    #    genre = row.get('Genre', 'N/A')
    #    rating = row.get('IMDB_Rating', 'N/A')
    #    meta = row.get('Meta_score', 'N/A')
    #    overview = row.get('Overview', 'No description')
        
    #    print(f"{rank}. {title} ({year})")
   #     print(f"    Жанры: {genre}")
   #     print(f"    {rating}/10 |  Metascore: {meta}")
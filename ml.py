import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

df = pd.read_csv('../movies.csv')
df = df.dropna(subset=['overview'])

if 'genres' in df.columns:
    df['genres'] = df['genres'].fillna('')

model = SentenceTransformer('all-MiniLM-L6-v2')
movie_embeddings = model.encode(df['overview'].tolist(), show_progress_bar=True)

K = 50
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(movie_embeddings)
centroids = kmeans.cluster_centers_

while True:
    query = input("\n Опиши фильм: ")
    if query.lower() in ('exit', 'quit'):
        break

    query_vec = model.encode([query])

    cluster_scores = cosine_similarity(query_vec, centroids)[0]
    best_clusters = np.argsort(cluster_scores)[::-1][:3]

    cluster_mask = df['cluster'].isin(best_clusters)
    cluster_indices = np.where(cluster_mask)[0]  

    cluster_embeddings = movie_embeddings[cluster_indices]

    scores = cosine_similarity(query_vec, cluster_embeddings)[0]

    top_n = min(50, len(scores))
    top_local = scores.argsort()[::-1][:top_n]
    top_indices = cluster_indices[top_local]
    final_scores = []
    for idx, score in zip(top_indices, scores[top_local]):
        row = df.iloc[idx] 
        vote = row['vote_average'] if 'vote_average' in df.columns else 0
        popularity = row['popularity'] if 'popularity' in df.columns else 0
        final_score = score * 0.7 + vote * 0.2 - popularity * 0.1
        final_scores.append((idx, final_score))
    if not final_scores:
            print("\nНичего не найдено по вашему запросу.\n")
            continue
    final_scores = sorted(final_scores, key=lambda x: x[1], reverse=True)
    top_final = [idx for idx, _ in final_scores[:5]]

    print(f"\n Топ-5 фильмов:\n")
    for rank, i in enumerate(top_final, 1):
        row = df.iloc[i]
        print(f"{rank}. {row['title']} ({row['release_date']}) |  {row['vote_average']} |  {row['popularity']}")
        print(f"   {row['overview'][:150]}...\n")
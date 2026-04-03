import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer('all-MiniLM-L6-v2')  

df = pd.read_csv('../movies.csv') 
df = df.dropna(subset=['overview'])


movie_embeddings = model.encode(df['overview'].tolist(), show_progress_bar=True)



while True:
    query = input("\nОпиши фильм: ")
    
    if query.lower() in ('exit', 'quit'):
        break
    
    query_vec = model.encode([query])
    
    
    scores = cosine_similarity(query_vec, movie_embeddings)[0]
    
    
    top_indices = scores.argsort()[-5:][::-1]
    
    print("\n Топ-5 фильмов по смыслу:\n")
    for rank, i in enumerate(top_indices, 1):
        row = df.iloc[i]
        print(f"{rank}. {row['title']} ({row['release_date']}) |  {row['vote_average']} |  {row['popularity']}")
        print(f"   {row['overview'][:150]}...\n")

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("dataset/movies.csv")

# Combine important columns
movies["tags"] = movies["genre"] + " " + movies["language"]

# Convert text into vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies["tags"]).toarray()

# Calculate similarity
similarity = cosine_similarity(vectors)

def recommend(movie_name):
    movie_index = movies[movies["title"] == movie_name].index
    
    if len(movie_index) == 0:
        return ["Movie not found"]
    
    movie_index = movie_index[0]
    distances = similarity[movie_index]
    
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        
    return recommended_movies
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies=pd.read_csv("tmdb_5000_movies.csv")
credits=pd.read_csv("tmdb_5000_credits.csv")

movies=movies[["id","title","overview","genres"]]
movies["overview"]=movies["overview"].fillna("")
movies["tags"]=movies["overview"]+movies["genres"]

cv=CountVectorizer(max_features=5000,stop_words="english")
vectors=cv.fit_transform(movies["tags"]).toarray()

similarity=cosine_similarity(vectors)

def recommend(movie):
    
    recommended_movies = []
    similarity_score=[]

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        similarity_score.append(round(i[1]*100, 2))

    return recommended_movies, similarity_score
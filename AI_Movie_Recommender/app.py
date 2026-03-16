import streamlit as st
import pandas as pd
from recommender import recommend
import requests

API_KEY = "780b9ae352c854c4135b3b1b753e7b99"
st.set_page_config(page_title="AI Movie Recommender", layout="wide")
st.title("AI Movie Recommendation System")

movies = pd.read_csv("tmdb_5000_movies.csv")
movie_list = movies["title"].values

def fetch_poster(movie_name):   
    url = f"https://api.themoviedb.org/3/search/movie?api_key=780b9ae352c854c4135b3b1b753e7b99&query={movie_name}"
    data = requests.get(url).json()
    try:
        poster_path = data["results"][0]["poster_path"]
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        return None

selected_movie = st.selectbox(
    "Select a Movie",
    movie_list
)

if st.button("Recommend"):    
    names, scores = recommend(selected_movie)
    st.subheader("Recommended Movies")
    cols = st.columns(5)
    for i in range(5):
        poster = fetch_poster(names[i])
        with cols[i]:
            if poster:
                st.image(poster)

            st.write(names[i])
            st.write(f"Similarity: {scores[i]}%")
            st.write("AI Suggestion based on story & genre similarity")

import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")

# -------------------- LOAD DATA --------------------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------- TMDB API --------------------
API_KEY = "b2ee40766dea8b4b64da9866989fdc64"  

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    movie = movie.strip()
    
    if movie not in movies['title'].values:
        return [], []
    
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

# -------------------- UI --------------------
st.markdown(
    "<h1 style='text-align: center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

st.write("")

# Dropdown
selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# Button
if st.button("Recommend"):

    with st.spinner("Fetching recommendations..."):
        names, posters = recommend(selected_movie)

    if len(names) == 0:
        st.error("Movie not found")
    else:
        st.subheader("Recommended Movies")

        col1, col2, col3, col4, col5 = st.columns(5)

        for idx, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.image(posters[idx])
                st.caption(names[idx])
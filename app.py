import os 
import streamlit as st 
import pickle 
import pandas as pd
import requests 
import time 
# ----------------------------------------------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5898299d23f73f30e80860a386376aa5&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    movie_path = data['homepage']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return {"full_path": full_path, "movie_path": movie_path}

def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    dist = similarity[index]
    
    recommended_movies_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:quantity+1]
    
    recommended_movies = []
    recommended_movie_poster = []
    recommended_movie_path = []
    
    for i in recommended_movies_list:
        recommended_movies.append(movies.iloc[i[0]]['title'])
        # Fetching posters and TMDB links
        movie_id = movies.iloc[i[0]].movie_id
        poster_data = fetch_poster(movie_id)
        recommended_movie_poster.append(poster_data["full_path"])
        recommended_movie_path.append(poster_data["movie_path"])
    
    return recommended_movies, recommended_movie_poster, recommended_movie_path

# Load data -------------------------------------------------------
similarity = pickle.load(open('similarity.pkl', 'rb'))  
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Recommender System"
)

st.title('Movie Recommender System')

movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

with st.sidebar:
    quantity = st.slider("How many movie recommendations you want?", min_value=1, max_value=10, value=5)

if st.button('Get Recommendations'):
    # Create a progress bar
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success("Your Recommendations are on the way :D")        

    # Fetch recommendations
    names, posters, path = recommend(movie_name)

    # Show recommendations
    cols = st.columns(3)
    for i in range(quantity):
        with cols[i % 3]:
            st.write('---')
            st.write(names[i])
            if posters[i]:
                st.image(posters[i], width=200, use_column_width = 'auto')
                st.link_button("Visit page", path[i])
            else:
                st.write("No poster available")
    
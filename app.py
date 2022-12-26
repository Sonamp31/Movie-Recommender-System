import streamlit as st
import pickle
import pandas as pd
import requests

similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))

    data = response.json()

    return "https://image.tmdb.org/t/p/original" + data['poster_path']


def recommend(movie_name):
    movie_index = movie[movie['title'] == movie_name].index[0]     # To get index of searched movie and store it in movie_index
    distance = similarity[movie_index]        # To store similarity values of provided movie with all other.
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]       # To store 5 Most similar movies having lowest distance for that create list of tuple(movie_id,similarities) and sort it according to similarity values reversely.

    recommended_movies = []
    recommend_movies_poster = []
    for i in movie_list:
        movie_id = movie.iloc[i[0]].movie_id
        recommended_movies.append(movie.iloc[i[0]].title)  # To print title of movies
        recommend_movies_poster.append(fetch_poster(movie_id))  #To display posters of movie
    return recommended_movies,recommend_movies_poster


st.title('Movie Recommender System')

movie_dict = pickle.load(open('movie_dict.pkl','rb'))    #open movie_dict.pkl in movie_dict as read binary mode
movie = pd.DataFrame(movie_dict)

#To generate selectbox for searching movie from dropdown
selected_movie_name = st.selectbox(
    'What kind of movie you want to watch?',
    movie['title'].values)

if st.button('Recommend'):
    names,poster = recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])

import streamlit as st
import pandas as pd

data = pd.read_csv("data/data.csv")
movies = pd.read_csv("data/movie.csv")

st.set_page_config(layout="wide")
st.title('Netfizz')

st.write("---")

best_10 = movies.sort_values(by="reviews_count", ascending=False).iloc[:10 , :]

cols1 = st.columns(5)

for ele, col in zip(best_10.index[:5], cols1):
    current_movie = best_10.loc[[ele]]
    with col:
        st.markdown("### " + current_movie.at[ele, "title"])
        url = current_movie.at[ele, "image_path"]
        st.image(url)
        st.write("**Year :** ", str(int(current_movie.at[ele, "movie_Year"])))
        genres = []
        for genre in ["Adventure","Animation","Children","Comedy","Fantasy","Romance","Drama","Action","Crime","Thriller",
                    "Horror","Mystery","Sci-Fi","IMAX","War","Musical","Documentary","Western","Film-Noir"]:
            if current_movie.at[ele, genre]:
                genres.append(genre)
        st.write("**Genres :** ", ", ".join(genres))
        st.write("**Rating :** ", str(round(current_movie.at[ele, "mean_rating"],1)))
        with st.expander("See overview"):
            st.write(current_movie.at[ele, "overview"])
        
        
st.write("---")

sliders = {}

for id in best_10.index:
    sliders[id] = st.slider('Expected rating', min_value=1., max_value=5., step=0.5)

cols2 = st.columns(5)

for ele, col in zip(best_10.index[5:], cols2):
    current_movie = best_10.loc[[ele]]
    with col:
        st.markdown("### " + current_movie.at[ele, "title"])
        url = current_movie.at[ele, "image_path"]
        st.image(url)
        st.write("**Year :** ", str(int(current_movie.at[ele, "movie_Year"])))
        genres = []
        for genre in ["Adventure","Animation","Children","Comedy","Fantasy","Romance","Drama","Action","Crime","Thriller",
                    "Horror","Mystery","Sci-Fi","IMAX","War","Musical","Documentary","Western","Film-Noir"]:
            if current_movie.at[ele, genre]:
                genres.append(genre)
        st.write("**Genres :** ", ", ".join(genres))
        st.write("**Rating :** ", str(round(current_movie.at[ele, "mean_rating"],1)))
        with st.expander("See overview"):
            st.write(current_movie.at[ele, "overview"])
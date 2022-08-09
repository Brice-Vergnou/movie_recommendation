import streamlit as st
import pandas as pd
from content_model import get_recommendations_metadata
from colab_model import train, get_metadata_recommendations

data = pd.read_csv("data/data.csv")
movies = pd.read_csv("data/movie.csv")



st.set_page_config(layout="wide")
st.title('Netfizz')

st.write("---")

best_10 = movies.sort_values(by="reviews_count", ascending=False).iloc[:10 , :]

ratings = {}

def name_to_rating(rats):
    for key, value in rats.items():
        if value == 'I don\'t know':
            rats[key] = -1
        if value == 'Not for me':
            rats[key] = 1
        if value == 'Could be good':
            rats[key] = 3
        if value == 'Looks appealing':
            rats[key] = 5
    return rats

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
        ratings[ele] = st.radio("What do you think about it?", ('I don\'t know','Not for me', 'Could be good', 'Looks appealing'), key=ele, horizontal=True)
        
        
st.write("---")



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
        ratings[ele] = st.radio("What do you think about it?", ('I don\'t know','Not for me', 'Could be good', 'Looks appealing'), key=ele, horizontal=True)
            
st.write(ratings)

_,_, btn_col, _,_ = st.columns(5)

with btn_col:
    btn = st.button('Confirm my choice')
    if btn:
        real_ratings = name_to_rating(ratings)
        
        best_ratings = list()
        for (key, value) in real_ratings.items():
            if value == 5:
                best_ratings.append(key)
                        
        content_movies = list()
        for movie in best_ratings:
            content_movies.append(get_recommendations_metadata(movie, movies, n_best=1))
        st.write(content_movies)
        
        for key in real_ratings.keys():
            if real_ratings[key] != -1:
                data_for_df = {"userId":666666}
                data_for_df["movieId"] = key
                data_for_df["rating"] = real_ratings[key]
                data = data.append(pd.DataFrame(data_for_df, index=[data.index[-1] +1]))
        
        svd = train(data)
        colab_movies = get_metadata_recommendations(svd, 666666, data, n_best=10-len(content_movies))
        st.write(colab_movies)
        # 3. complete with the colab filtering model
        # 4. update the results on page
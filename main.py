from random import shuffle, randint
import numpy as np
import streamlit as st
import pandas as pd
from content_model import get_metadata_content
from colab_model import train, get_metadata_colab
st.set_page_config(layout="wide")

radio_count = 0
form_count = 0
data = pd.read_csv("data/data.csv")
movies = pd.read_csv("data/movie.csv")

st.title('Netfizz 🥂')

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

def refresh(ratings):
    # Get the new recommended movies based on the two models we have and the ratings given by the user
    global movies, data
    real_ratings = name_to_rating(ratings)
            
    best_ratings = list()
    for (key, value) in real_ratings.items():
        if value == 5:
            best_ratings.append(key)
                    
    content_movies = list()
    for movie in best_ratings:
        content_movies.append(get_recommendations_metadata(movie, movies, n_best=1))
    
    
    for key in real_ratings.keys():
        if real_ratings[key] != -1:
            data_for_df = {"userId":666666}
            data_for_df["movieId"] = key
            data_for_df["rating"] = real_ratings[key]
            data = data.append(pd.DataFrame(data_for_df, index=[data.index[-1] +1]))
    
    svd = train(data)
    colab_movies = get_metadata_colab(svd, 666666, data, n_best=5-len(content_movies))
    
    best_10 = colab_movies
    for movie in content_movies:
        best_10.update(movie)
    
    best_10 = pd.DataFrame(best_10).T
    
    main(best_10)

def main(best_10=None):
    global radio_count, form_count
    
    
    st.write("---")
    
    
    
    if best_10 is None:
        # If we don't have a given set of movies, we're going to suggest 10 of the 30 most rated movies
        best_10 = movies.sort_values(by="reviews_count", ascending=False).iloc[:30   , :]
        best_10 = best_10.sample(n=10)
        best_10["genres"] = np.nan
        best_10["genres"] = best_10["genres"].astype('object')
        for ele in best_10.index:
            genres = []
            for genre in ["Adventure","Animation","Children","Comedy","Fantasy","Romance","Drama","Action","Crime","Thriller",
                        "Horror","Mystery","Sci-Fi","IMAX","War","Musical","Documentary","Western","Film-Noir"]:
                if best_10.at[ele, genre]:
                    genres.append(genre)
            best_10.at[ele, "genres"] = genres

    
    ratings = {}

    cols1 = st.columns(5)

    form = st.form(key=str(form_count))
    form_count += 1
    
    for ele, col in zip(best_10.index[:5], cols1):
        current_movie = best_10.loc[[ele]]
        with col:
            title = current_movie.at[ele, "title"]
            st.markdown("### " + title)
            url = current_movie.at[ele, "image_path"]
            if url is not None:
                st.image(url)
            st.write("**Year :** ", str(int(current_movie.at[ele, "movie_Year"])))
            genres = current_movie.at[ele, "genres"]
            st.write("**Genres :** ", ", ".join(genres))
            st.write("**Rating :** ", str(round(current_movie.at[ele, "mean_rating"],1)))
            with st.expander("See overview"):
                if current_movie.at[ele, "overview"] is not None:
                    st.write(current_movie.at[ele, "overview"])
                else:
                    st.write("Not available")
            ratings[radio_count] = form.radio(f"What do you think about \"{title}\" ?", ('I don\'t know','Not for me', 'Could be good', 'Looks appealing'), key=radio_count, horizontal=True)
            radio_count += 1

    btn = form.form_submit_button('Generate Some Text')
    st.write(form.inputs())
    
    if btn:
        
        refresh(ratings=ratings)
        
if __name__=="__main__":
    main()

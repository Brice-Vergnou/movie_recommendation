from content_model import get_metadata_content
from colab_model import train, get_metadata_colab
import pandas as pd
import numpy as np

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
    
def get_recommendations(ratings, movie_df, data_df):
    # Get the new recommended movies based on the two models we have and the ratings given by the user
    real_ratings = name_to_rating(ratings)
            
    best_ratings = list()
    for (key, value) in real_ratings.items():
        if value == 5:
            best_ratings.append(key)
                    
    content_movies = list()
    for movie in best_ratings:
        content_movies.append(get_metadata_content(movie, movie_df, n_best=1))
    
    
    for key in real_ratings.keys():
        if real_ratings[key] != -1:
            data_for_df = {"userId":666666}
            data_for_df["movieId"] = key
            data_for_df["rating"] = real_ratings[key]
            data_df = data_df.append(pd.DataFrame(data_for_df, index=[data_df.index[-1] +1]))
    
    svd = train(data_df)
    colab_movies = get_metadata_colab(svd, 666666, data_df, n_best=5-len(content_movies))
    
    best_5 = colab_movies
    for movie in content_movies:
        best_5.update(movie)
    
    return best_5

def first_5(movie_df):
    """Return 5 of the 30 most rated movies, in the same format we use in colab_model and content_model

    Args:
        movie_df (pd.DataFrame): the movie datafram

    Returns:
        dict:  dictionary with 5 keys, corresponding to the recommended movie ID's. For each key, it contains a dictionary with all the features
    """
    best_5 = movie_df.sort_values(by="reviews_count", ascending=False).iloc[:30   , :]
    best_5 = best_5.sample(n=5)
    best_5["genres"] = np.nan
    best_5["genres"] = best_5["genres"].astype('object')
    for ele in best_5.index:
        genres = []
        for genre in ["Adventure","Animation","Children","Comedy","Fantasy","Romance","Drama","Action","Crime","Thriller",
                    "Horror","Mystery","Sci-Fi","IMAX","War","Musical","Documentary","Western","Film-Noir"]:
            if best_5.at[ele, genre]:
                genres.append(genre)
        best_5.at[ele, "genres"] = genres
    best_5 = best_5[["movieId","title","movie_Year","mean_rating","overview","image_path","genres"]].to_dict("records")
    movies = []
    for movie in best_5:
        movies.append(movie)
    return movies
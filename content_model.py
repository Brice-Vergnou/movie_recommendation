from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer



def get_metadata_content(movie_id, movie_data, n_best=5):
    """Returned the metadata of the n most close movies to the one passed as an argument according to the content features

    Args:
        movie_id (int): id of the movies we want to find the most closest results
        movie_data (pd.DataFrame): DF preprocessed like in the eda notebook
        n_best (int, optional):number of movies we want. Defaults to 5.

    Returns:
    dict: dictionary with n keys, corresponding to the recommended movie ID's. For each key, it contains a dictionary with all the features
    """
    tfidf = TfidfVectorizer(stop_words='english')
    movie_data['overview'] = movie_data['overview'].fillna('')
    tfidf_matrix = tfidf.fit_transform(movie_data['overview'])

    cos_sim_data = pd.DataFrame(cosine_similarity(tfidf_matrix))
    best_ids =cos_sim_data.loc[movie_id].sort_values(ascending=False).index.tolist()[1:n_best+1]
    movies_recomm =  movie_data.loc[best_ids]
    
    reco = dict(movies_recomm)
    metadata = {}
    for id in movies_recomm.index:

        metadata[id] = {}
        
        title = reco["title"][id]
        year = reco["movie_Year"][id]
        mean_rating = reco["mean_rating"][id]
        genres = []
        for genre in ["Adventure","Animation","Children","Comedy","Fantasy","Romance","Drama","Action","Crime","Thriller",
                    "Horror","Mystery","Sci-Fi","IMAX","War","Musical","Documentary","Western","Film-Noir"]:
            if reco[genre][id]:
                genres.append(genre)
        overview = reco["overview"][id]
        image_path = reco["image_path"][id]

        
        metadata[id]["movie_Year"] = year
        metadata[id]["title"] = title
        metadata[id]["mean_rating"] = mean_rating
        metadata[id]["genres"] = genres
        metadata[id]["overview"] = overview
        metadata[id]["image_path"] = image_path
    return metadata
    

    

if __name__=="__main__":
    data = pd.read_csv("data/movie.csv")
    pprint(get__metadata_content(435,data))
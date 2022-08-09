#%%
import numpy as np
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import cross_validate
from collections import defaultdict # allows us to automatically create keys with fewer lines
from surprise.model_selection import GridSearchCV
from surprise.dump import dump
from tqdm import tqdm
from pprint import pprint




def train(df_data):
    features = ["userId","movieId","rating"]


    reader = Reader()
    data = Dataset.load_from_df(df_data[features], reader)

    # param_grid = {'n_epochs': [10], 'lr_all': [0.002, 0.005],
    #               'reg_all': [0.2, 0.4, 0.6]}
    # gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)

    # gs.fit(data)

    # # best RMSE score
    # print(gs.best_score['rmse'])

    # # combination of parameters that gave the best RMSE score
    # print(gs.best_params['rmse'])

    svd = SVD(verbose=True,**{'n_epochs': 5, 'lr_all': 0.005, 'reg_all': 0.2}) # Found by GridSearch 

    trainset = data.build_full_trainset()
    svd.fit(trainset)
    
    return svd

def take_second(elem):
    return elem[1]

def return_n_best(svd, user_id, colab_data, n=5):
    results = defaultdict(list)
    for id in tqdm(colab_data.movieId):
        _, _, _, est, _ = svd.predict(user_id, id)
        results[id] = est
        
    items = results.items()
    final = sorted(items, key=take_second, reverse=True)[:n]
    
    return final

def get_metadata_recommendations(svd, user_id, colab_data, n_best=5):
    metadata = {}
    for i in range(n_best):
        predictions = return_n_best(svd, user_id, colab_data, n_best)[i]
        id, _ = predictions
        metadata[id] = {}

        row = colab_data[colab_data.movieId == id].iloc[0]
        row = dict(row)

        title = row["title"]
        year = row["movie_Year"]
        mean_rating = row["mean_rating"]
        overview = row["overview"]
        image_path = row["image_path"]
        genres = []
        for genre in ["Adventure","Animation","Children","Comedy","Fantasy","Romance","Drama","Action","Crime","Thriller",
                    "Horror","Mystery","Sci-Fi","IMAX","War","Musical","Documentary","Western","Film-Noir"]:
            if row[genre]:
                genres.append(genre)

        
        metadata[id]["year"] = year
        metadata[id]["title"] = title
        metadata[id]["mean_rating"] = mean_rating
        metadata[id]["genres"] = genres
        metadata[id]["overview"] = overview
        metadata[id]["image_path"] = image_path
    return metadata

if __name__=="__main__":
    df_data = pd.read_csv("data/data.csv")
    svd = train(df_data)
    pprint(get_metadata_recommendations(svd, 0, colab_data=df_data))
    dump("data/model.pkl",algo=svd)
# %%
from pprint import pprint
from numpy import positive
import tensorflow as tf
import pandas as pd
import os
from pprint import pprint
import tensorflow_recommenders as tfrs

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #  So tensorflow stops yelling at me for misc stuff


movies_df = pd.read_csv("data/movie.csv")
ratings_df = pd.read_csv("data/ratings.csv")
movies = tf.data.Dataset.from_tensor_slices(dict(movies_df))
ratings = tf.data.Dataset.from_tensor_slices(dict(ratings_df))

# for x in data.take(1).as_numpy_iterator():
#    pprint(x)
    
SEED = 42
embedding_dimension = 64

tf.random.set_seed(SEED)
shuffled = ratings.shuffle(len(ratings), seed=SEED, reshuffle_each_iteration=False)

train = shuffled.take(80_000)
test = shuffled.skip(80_000).take(len(ratings) - 80_000)

unique_movie_titles = movies_df.title.unique()
unique_user_ids = ratings_df.userId.unique()

# We're going to build a two towers retrieval model, so we can build each tower separately and combine them later

user_model = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.StringLookup(  # convert ids to integers
    ),
    tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension) # embedding for unknown tokens
])

movie_model = tf.keras.Sequential([ # same as user but for movie
    tf.keras.layers.experimental.preprocessing.StringLookup(  
        vocabulary=unique_movie_titles, mask_token=None
    ),
    tf.keras.layers.Embedding(len(unique_movie_titles) + 1, embedding_dimension) 
])

class RankingModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        # We're going to build a two towers retrieval model, so we can build each tower separately and combine them later
        
        # Compute embeddings for users.
        self.user_embeddings = tf.keras.Sequential([
        tf.keras.layers.StringLookup(
            vocabulary=unique_user_ids, mask_token=None),
        tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension)
        ])

        # Compute embeddings for movies.
        self.movie_embeddings = tf.keras.Sequential([
        tf.keras.layers.StringLookup(
            vocabulary=unique_movie_titles, mask_token=None),
        tf.keras.layers.Embedding(len(unique_movie_titles) + 1, embedding_dimension)
        ])

        # Compute predictions.
        self.ratings = tf.keras.Sequential([
        # Learn multiple dense layers.
        tf.keras.layers.Dense(256, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        # Make rating predictions in the final layer.
        tf.keras.layers.Dense(1)
    ])
    
    def call(self, inputs):
        user_id, movie_title = inputs
        user_embedding = self.user_embeddings(user_id)
        movie_embedding = self.movie_embeddings(movie_title)
        return self.ratings(tf.concat([user_embedding, movie_embedding], axis=1))





task = tfrs.tasks.Ranking( # this task object both gives us a loss function and metric computation
    loss = tf.keras.losses.MeanSquaredError(),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

class MovielenModel(tfrs.models.Model):
    
    def __init__(self, user_model, movie_model) :
        super().__init__()
        self.user_model = user_model
        self.movie_model = movie_model
        self.task = task
        self.ranking_model = RankingModel()
        
    def call(self, features):
        return self.ranking_model((features["user_id"], features["movie_title"]))
        
    def compute_loss(self, features):
        labels = features.pop("user_rating")
        rating_predictions = self(features)
        print(type(self))
        return self.task(labels=labels, predictions=rating_predictions)
   
"""
model = MovielenModel(
    user_model=user_model,
    movie_model=movie_model
    )
model.compile(optimizer=tf.keras.optimizers.Adagrad(le=0.1))

cached_train = train.shuffle(100_000).batch(8192).cache()
cached_test = test.batch(4096).cache()

model.fit(cached_train, epochs=3)

model.evaluate(cached_test, return_dict=True)

# Create a model that takes in raw query features, and
index = tfrs.layers.factorized_top_k.BruteForce(model.user_model)
# recommends movies out of the entire movies dataset.
index.index_from_dataset(
  tf.data.Dataset.zip((movies.batch(100), movies.batch(100).map(model.movie_model)))
)
 """
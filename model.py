import numpy as np
import tensorflow as tf
import pandas as pd
import os
from pprint import pprint
import tensorflow_recommenders as tfrs

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #  So tensorflow stops yelling at me for misc stuff


movies_df = pd.read_csv("data/movie.csv")
ratings_df = pd.read_csv("data/ratings.csv")
data_df = pd.read_csv("data/data.csv")
data = tf.data.Dataset.from_tensor_slices(dict(data_df))
movies = data.map(lambda x: x["title"])


# for x in data.take(1).as_numpy_iterator():
#    pprint(x)
    
SEED = 42
embedding_dimension = 64

tf.random.set_seed(SEED)
shuffled = data.shuffle(len(data), seed=SEED, reshuffle_each_iteration=False)

train = shuffled.take(80_000)
test = shuffled.skip(80_000).take(len(data) - 80_000)

unique_movie_titles = np.unique(np.concatenate(list(movies.batch(1000))))
unique_user_ids = np.unique(np.concatenate(list(data.batch(1_000).map(
    lambda x: x["userId"]))))

print(unique_user_ids)


# We're going to build a two towers retrieval model, so we can build each tower separately and combine them later

class UserModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        self.user_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=unique_user_ids, mask_token=None),
            tf.keras.layers.Embedding(len(unique_user_ids) + 1, embedding_dimension),
        ])


        self.normalized_day = tf.keras.layers.Normalization(
            axis=None
        )
        self.normalized_day.adapt(ratings_df.review_Day)
        
        
        self.normalized_month = tf.keras.layers.Normalization(
            axis=None
        )
        self.normalized_month.adapt(ratings_df.review_Month)
        
        
        self.normalized_year = tf.keras.layers.Normalization(
            axis=None
        )
        self.normalized_year.adapt(ratings_df.review_Year)
        
        self.normalized_weekday = tf.keras.layers.Normalization(
            axis=None
        )
        self.normalized_weekday.adapt(ratings_df.review_week_day)
        

    def call(self, inputs):

        return tf.concat([
            self.user_embedding(inputs["user_id"]),
            self.normalized_day(inputs["review_Day"]),
            self.normalized_month(inputs["review_Month"]),
            self.normalized_year(inputs["review_Year"]),
            self.normalized_weekday(inputs["review_week_day"])
        ], axis=1) 



class MovieModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        max_tokens = 10_000

        self.title_vectorizer = tf.keras.layers.TextVectorization(
            max_tokens=max_tokens)
        self.title_text_embedding = tf.keras.Sequential([
        self.title_vectorizer,
        tf.keras.layers.Embedding(max_tokens, embedding_dimension, mask_zero=True),
        tf.keras.layers.GlobalAveragePooling1D(),
        ])
        self.title_vectorizer.adapt(unique_movie_titles)
        
        self.normalized_year = tf.keras.layers.Normalization(
            axis=None
        )
        self.normalized_year.adapt(movies_df.movie_Year)

    def call(self, inputs):
        return tf.concat([
            self.title_text_embedding(inputs["movie_title"]),
            self.normalized_year(inputs["movie_Year"])
        ], axis=1)


class MovielensModel(tfrs.models.Model):

    def __init__(self):
        super().__init__()
        self.query_model = tf.keras.Sequential([
        UserModel(),
        tf.keras.layers.Dense(32)
        ])
        self.candidate_model = tf.keras.Sequential([
        MovieModel(),
        tf.keras.layers.Dense(32)
        ])
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=movies.batch(128).map(self.candidate_model),
            ),
        )

    def compute_loss(self, features):
        query_embeddings = self.query_model({
            "user_id": features["user_id"],
            "review_Day": features["review_Day"],
            "review_Month": features["review_Month"],
            "review_Year": features["review_Year"],
            "review_week_day": features["review_week_day"],
        })
        
        movie_embeddings = self.candidate_model({
            "movie_title" : features["movie_title"],
            "movie_Year" : features["movie_Year"]
            })

        return self.task(query_embeddings, movie_embeddings)
   

model = MovielensModel()
model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))

cached_train = train.shuffle(100_000).batch(2048)
cached_test = test.batch(4096).cache()

model.fit(cached_train, epochs=3)

train_accuracy = model.evaluate(
    cached_train, return_dict=True)["factorized_top_k/top_100_categorical_accuracy"]
test_accuracy = model.evaluate(
    cached_test, return_dict=True)["factorized_top_k/top_100_categorical_accuracy"]

print(f"Top-100 accuracy (train): {train_accuracy:.2f}.")
print(f"Top-100 accuracy (test): {test_accuracy:.2f}.")
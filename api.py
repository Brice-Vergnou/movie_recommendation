from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from helper_functions import get_recommendations, first_5
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import JSONResponse

data = pd.read_csv("data/data.csv")
movies = pd.read_csv("data/movie.csv")

class Item(BaseModel):
    movie_1_rating: Union[str, None] = "I don't know"
    movie_1_id: int
    movie_2_rating: Union[str, None] = "I don't know"
    movie_2_id: int
    movie_3_rating: Union[str, None] = "I don't know"
    movie_3_id: int
    movie_4_rating: Union[str, None] = "I don't know"
    movie_4_id: int
    movie_5_rating: Union[str, None] = "I don't know"
    movie_5_id: int

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.2",
    "http://127.0.0.2:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def create_item(item: Item):
    items = item.dict()
    rating_names = ["movie_1_rating","movie_2_rating","movie_3_rating","movie_4_rating","movie_5_rating"]
    movie_ids = ["movie_1_id","movie_2_id","movie_3_id","movie_4_id","movie_5_id"]
    ratings = {}
    for rating, id_name in zip(rating_names, movie_ids):
        movie_id = items[id_name]
        ratings[movie_id] = items[rating]
    predicted_movies = get_recommendations(ratings, movies, data)
    return predicted_movies

@app.get("/")
async def give_basic_movies():
    headers={"Access-Control-Allow-Origin":"*"}
    return JSONResponse(content=first_5(movies), headers=headers)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port="8000")
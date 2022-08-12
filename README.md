# Movie recommendation

About a year ago, I made a Spotify Recommendation project that I wasn't quite proud of, because it wouldn't work like a normal recommendation system. In this project, I used [the movielens dataset](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip) to create a more realistic model. The model is hybrid ( it both uses content-based filtering and collaborative filtering ).

Then, I turned this model into an API using FastAPI and rendered it in a website. The results are quite satisfying to me.

### From this
![image](https://user-images.githubusercontent.com/86613710/184403606-9ed268eb-178f-4f81-8ff3-07d0a3cf3ff9.png)
### To this
![The recommendations ](https://user-images.githubusercontent.com/86613710/184407901-ad20ebf7-0954-45be-b7a5-fce96a7934f9.png)

If you want to test it and have it deployed on internet, here are the following steps:


- Install the repo :
```
git clone https://github.com/Brice-Vergnou/movie_recommendation.git
cd movie_recommendation
```

- Get the right libraries :
```bash
pip install -r requirements.txt
```

- Deploy the web page locally thanks to the live server extension from Visual Studio
- Deploy the API locally :
```bash
uvicorn api:app --reload
```

- Install ngrok
- Change your config file to :
```yaml
authtoken: <your_token>
tunnels:
  live:
    proto: http
    addr: 5500 # You can change the port to whatever you want, as long as it is the web port
  api:
    proto: http
    addr: 8000 # Same thing with the API port
```
- Start all your tunnels:
```
ngrok start --all
```

- Get a CORS proxy :
```
# From any folder
git clone https://github.com/Rob--W/cors-anywhere.git
cd cors-anywhere/
npm install
heroku create
git push heroku master
```

- Change the urls used in ```script.js``` in the first lines by your api server url and heroku proxy url

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

app = FastAPI()

API_TOKEN =  os.getenv("API_KEY")
MOVIE_DB = "http://db_service:8000"

def get_movies():
    health_status = requests.get(url=f"{MOVIE_DB}/health")

    if health_status.json()["status"] == "ok":
        movies = requests.get(url=f"{MOVIE_DB}/read")

        return movies.json()
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/")
def get_desc():
    return {"description": "This is the business logic service, which allows users to receive movie descriptions based on the provided id. To get a description, use the endpoint /description?id=value."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/description")
def get_description(id: str):
    movies = get_movies()

    max_id = [movie['id'] for movie in movies]

    if int(id) not in max_id:
        return {"error": "there is no movie with provided id"}

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "qwen/qwen2.5-vl-72b-instruct:free",
            "messages":[
                {
                    "role": "system",
                    "content":
                    f"""
                    List of movies: {movies}

                    You are a movie description system. Given a list of movies, the user will provide a movie ID, and you will return the corresponding movie's description.

                    Each movie in the list will have the following format:
                    - Id: A unique identifier for the movie
                    - Title: The title of the movie
                    - Director: The director of the movie

                    Your task is to find the movie with the given ID, retrieve its description, and return it.

                    Example:  
                    Movies List:
                    [
                        {{"id": 1, "title": "Inception", "director": "Christopher Nolan"}},
                        {{"id": 2, "title": "The Godfather", "director": "Francis Ford Coppola"}},
                        {{"id": 3, "title": "Pulp Fiction", "director": "Quentin Tarantino"}}
                    ]

                    User: 2

                    Expected result: A cinematic masterpiece directed by Francis Ford Coppola, The Godfather (1972) is a gripping crime drama that follows the powerful Corleone mafia family, exploring themes of loyalty, power, and betrayal.
                    """
                },
                {
                    "role": "user", 
                    "content": f"Provided id: {id}"
                }
            ]
        })
    )

    description = response.json()['choices'][0]['message']['content']

    return {
        "movie":
        list(
            filter(lambda x: x["id"] == int(id),
                movies)
        )[0],
        "description": description
        }


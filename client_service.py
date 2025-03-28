from fastapi import FastAPI, HTTPException, Header
from dotenv import load_dotenv
from pydantic import BaseModel
import requests
import os

class Movie(BaseModel):
    id: int = None
    title: str
    director: str

app = FastAPI()

load_dotenv()
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
MOVIE_DB = "http://db_service:8000"
BUSINESS_SERVICE = "http://business_service:8000"

def authorise_user(authorization):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def get_desc():
    return {"description": "This is the client service, the only service that can interact with external users. You can add new movies to the database using the /movies/write endpoint and retrieve existing movies with the /movies/read endpoint. The /description?id=value endpoint returns a description of a movie based on the provided preferences."}

@app.get("/health")
def checker_health():
    return {"status": "ok"}

@app.get("/movies/read")
def get_movies(authorization: str = Header(None)):
    authorise_user(authorization)
    
    checker_health = requests.get(url=f"{MOVIE_DB}/health")

    if checker_health.json()["status"] == "ok":

        movies = requests.get(url=f"{MOVIE_DB}/read")
        return movies.json()
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")
    
@app.post("/movies/write", status_code=201)
def add_movie(movie: Movie, authorization: str = Header(None)):
    authorise_user(authorization)

    checker_health = requests.get(url=f"{MOVIE_DB}/health",)

    if checker_health.json()["status"] == "ok":
        response = requests.post(f"{MOVIE_DB}/write", json={"title": movie.title, "director": movie.director})

        if response.status_code == 201:
            return {"movie": response.json()}
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to add movie")
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/description")
def get_movie_desc(id, authorization: str = Header(None)):
    authorise_user(authorization)

    checker_health = requests.get(url=f"{BUSINESS_SERVICE}/health")

    if checker_health.json()["status"] == "ok":

        response = requests.get(f"{BUSINESS_SERVICE}/description?id={id}")

        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to get description")
    else:
        raise HTTPException(status_code=503, detail="Service unavailable")
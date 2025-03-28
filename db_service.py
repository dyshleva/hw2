from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

movie_db = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan"},
    {"id": 2, "title": "The Godfather", "director": "Francis Ford Coppola"},
    {"id": 3, "title": "Pulp Fiction", "director": "Quentin Tarantino"}
]

class Movie(BaseModel):
    id: int = None
    title: str
    director: str

@app.get("/")
def get_desc():
    return {
        "description": "This is the database service that allows users to interact with the movie database. You can add new movies using the /write endpoint and retrieve movie data using the /read endpoint."
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/read")
def get_movies():
    return movie_db

@app.post("/write", status_code=201)
def post_movie(movie: Movie):

    if not all([movie.title, movie.director]):
        raise HTTPException(status_code=400, detail="You must provide all fields!")

    max_id = max(movie_db, key=lambda x: x['id'])

    new_movie = movie.model_dump()
    new_movie['id'] = max_id['id'] + 1
    movie_db.append(new_movie)

    return new_movie
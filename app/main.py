from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

# Simple in-memory store for example purposes
users_db = [
    User(id=1, name="Alice"),
    User(id=2, name="Bob"),
]

@app.get("/")
def read_root():
    return {"message": "Welcome to BlackJackCVBot"}

@app.get("/users", response_model=list[User])
def read_users():
    return users_db

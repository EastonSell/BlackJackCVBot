from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to BlackJackCVBot"}

@app.get("/users")
def read_users():
    return ["Alice", "Bob"]

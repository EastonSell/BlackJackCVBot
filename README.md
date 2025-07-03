# BlackJackCVBot

This project is a simple FastAPI service for demonstrating multi-agent collaboration workflows. It exposes a `/` root endpoint and a `/users` endpoint returning a list of example users.

## Running the server

Install dependencies and run the app with uvicorn:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running tests

Execute the unit tests with pytest:

```bash
pytest
```

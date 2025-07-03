# BlackJackCVBot

This project is a simple FastAPI service for demonstrating multi-agent collaboration workflows. It exposes:

* `/` — health check
* `/users` — list of example users
* `/count` — manage a running Hi-Lo count. The API now understands
  common card names so inputs like `"Ace of Spades"` or `"10H"`
  will be parsed correctly.
* `/decks` — configure number of decks for true count
* `/true_count` — retrieve the current true count

## Running the server

Install dependencies and run the app with uvicorn:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set `NUM_DECKS` to configure the number of decks used for true count
calculations at startup:

```bash
NUM_DECKS=6 uvicorn app.main:app --reload
```

## Running tests

Execute the unit tests with pytest:

```bash
pytest
```

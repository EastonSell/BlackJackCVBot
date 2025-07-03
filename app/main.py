from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .blackjack import CardCounter, basic_strategy

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class User(BaseModel):
    id: int
    name: str


class BoundingBox(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int


class TableLayout(BaseModel):
    dealer: BoundingBox | None = None
    players: list[BoundingBox] = []

# Simple in-memory store for example purposes
users_db = [
    User(id=1, name="Alice"),
    User(id=2, name="Bob"),
]

card_counter = CardCounter()
table_layout = TableLayout()

@app.get("/")
def read_root():
    return {"message": "Welcome to BlackJackCVBot"}

@app.get("/users", response_model=list[User])
def read_users():
    return users_db


@app.get("/draw", response_class=HTMLResponse)
def draw_page(request: Request):
    with open("app/static/draw.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/layout", response_model=TableLayout)
def set_layout(layout: TableLayout):
    global table_layout
    table_layout = layout
    return table_layout


@app.get("/layout", response_model=TableLayout)
def get_layout():
    return table_layout


@app.post("/reset_count")
def reset_count():
    card_counter.reset()
    return {"count": card_counter.get_count()}


class CardInput(BaseModel):
    card: str


@app.post("/count")
def add_card(input: CardInput):
    card_counter.add_card(input.card)
    return {"count": card_counter.get_count()}


@app.get("/count")
def get_count():
    return {"count": card_counter.get_count()}


class SuggestInput(BaseModel):
    player_total: int
    dealer_card: str


@app.post("/suggest")
def suggest_action(input: SuggestInput):
    action = basic_strategy(input.player_total, input.dealer_card)
    return {"action": action}

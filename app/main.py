"""Main FastAPI application exposing card counting endpoints."""

from pathlib import Path
import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass
from fastapi.encoders import jsonable_encoder

from .blackjack import CardCounter, basic_strategy
from .vision import recognize_card, recognize_card_bytes

# Resolve path to static files relative to this file so the app works when
# executed from any working directory.
STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class User(BaseModel):
    id: int
    name: str


@dataclass(frozen=True)
class BoundingBox:
    """Immutable rectangle used for layout coordinates."""

    x1: int
    y1: int
    x2: int
    y2: int


class TableLayout(BaseModel):
    dealer: BoundingBox | None = None
    # Use tuple for immutability
    players: tuple[BoundingBox, ...] = Field(default_factory=tuple)

# Simple in-memory store for example purposes
users_db = [
    User(id=1, name="Alice"),
    User(id=2, name="Bob"),
]

num_decks = int(os.getenv("NUM_DECKS", "1"))
card_counter = CardCounter(decks=num_decks)
table_layout = TableLayout()

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Welcome to BlackJackCVBot"}

@app.get("/users", response_model=list[User])
def read_users():
    """Return example list of users."""
    return users_db


@app.get("/draw", response_class=HTMLResponse)
def draw_page(request: Request):
    """Serve the drawing UI used to configure table layout."""
    with open(STATIC_DIR / "draw.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/layout", response_model=TableLayout)
def set_layout(layout: TableLayout):
    """Persist the provided table layout in memory."""
    global table_layout
    table_layout = layout
    return jsonable_encoder(table_layout)


@app.get("/layout", response_model=TableLayout)
def get_layout():
    """Return the currently configured table layout."""
    return jsonable_encoder(table_layout)


@app.post("/reset_count")
def reset_count():
    """Reset the running Hi-Lo card count."""
    card_counter.reset()
    return {"count": card_counter.get_count()}


class CardInput(BaseModel):
    card: str


@app.post("/count")
def add_card(input: CardInput):
    """Add a card to the counter and return the updated count."""
    card_counter.add_card(input.card)
    return {"count": card_counter.get_count()}


@app.get("/count")
def get_count():
    """Return the current card count."""
    return {"count": card_counter.get_count()}


class SuggestInput(BaseModel):
    player_total: int
    dealer_card: str


class DeckConfig(BaseModel):
    decks: int


@app.post("/suggest")
def suggest_action(input: SuggestInput):
    """Return basic-strategy advice based on totals."""
    action = basic_strategy(input.player_total, input.dealer_card)
    return {"action": action}


@app.post("/decks")
def set_decks(config: DeckConfig):
    """Configure the number of decks used for true count calculations."""
    card_counter.set_decks(config.decks)
    return {"decks": card_counter.num_decks}


@app.get("/true_count")
def get_true_count():
    """Return the current Hi-Lo true count."""
    return {"true_count": card_counter.get_true_count()}


@app.post("/recognize_card")
async def recognize_card_endpoint(file: UploadFile):
    """Detect and normalize a card value from an uploaded image."""
    data = await file.read()
    card = recognize_card_bytes(data)
    return {"card": card}

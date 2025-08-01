"""Blackjack utilities used by the API."""

from __future__ import annotations

import re

CARD_SYNONYMS = {
    "A": {"A", "ACE"},
    "K": {"K", "KING"},
    "Q": {"Q", "QUEEN"},
    "J": {"J", "JACK"},
    "10": {"10", "T", "TEN"},
    "9": {"9", "NINE"},
    "8": {"8", "EIGHT"},
    "7": {"7", "SEVEN"},
    "6": {"6", "SIX"},
    "5": {"5", "FIVE"},
    "4": {"4", "FOUR"},
    "3": {"3", "THREE"},
    "2": {"2", "TWO"},
}

SUIT_WORDS = {
    "H", "HEART", "HEARTS",
    "S", "SPADE", "SPADES",
    "D", "DIAMOND", "DIAMONDS",
    "C", "CLUB", "CLUBS",
}


def normalize_card(text: str) -> str | None:
    """Return canonical card value from various textual forms."""
    cleaned = re.sub(r"[^A-Za-z0-9]", " ", text).upper().split()
    tokens = [t for t in cleaned if t not in SUIT_WORDS and t not in {"OF", "THE"}]
    if not tokens:
        return None
    token = tokens[0]
    for value, names in CARD_SYNONYMS.items():
        if token in names:
            return value
        if len(token) > 1 and token[-1] in "HSDC" and token[:-1] in names:
            return value
    return None


class CardCounter:
    """Simple Hi-Lo card counter with true count support.

    The counter is stateful and not thread-safe, so it should be instantiated
    per-session or protected appropriately when used in a web context.
    """

    def __init__(self, decks: int = 1) -> None:
        self.running_count = 0
        self.cards_dealt = 0
        self.num_decks = decks

    def reset(self) -> None:
        self.running_count = 0
        self.cards_dealt = 0

    def set_decks(self, decks: int) -> None:
        """Configure number of decks used for true count calculations."""
        self.num_decks = max(1, decks)
        self.cards_dealt = 0

    def add_card(self, card: str) -> None:
        """Update running count with a single card.

        The input string can include suits or full card names, e.g. "10H" or
        "Ace of Spades". Only the rank is used for counting.
        """
        norm = normalize_card(card)
        value = norm if norm is not None else card.upper()
        if value in ["2", "3", "4", "5", "6"]:
            self.running_count += 1
        elif value in ["10", "J", "Q", "K", "A"]:
            self.running_count -= 1
        # 7,8,9 are zero
        self.cards_dealt += 1

    def get_count(self) -> int:
        return self.running_count

    def get_true_count(self) -> float:
        """Return the Hi-Lo true count as a floating point number."""
        decks_remaining = ((self.num_decks * 52) - self.cards_dealt) / 52
        if decks_remaining <= 0:
            decks_remaining = 1
        return self.running_count / decks_remaining


def basic_strategy(player_total: int, dealer_card: str) -> str:
    """Return a very simplified blackjack decision.

    Parameters
    ----------
    player_total: int
        Current total of the player's hand.
    dealer_card: str
        Visible dealer card.
    """
    dealer_norm = normalize_card(dealer_card)
    dealer = dealer_norm if dealer_norm is not None else dealer_card.upper()
    if player_total >= 17:
        return "stand"
    if player_total >= 13 and dealer in ["2", "3", "4", "5", "6"]:
        return "stand"
    if player_total == 12 and dealer in ["4", "5", "6"]:
        return "stand"
    if player_total == 11:
        return "double"
    if player_total == 10 and dealer not in ["10", "A"]:
        return "double"
    if player_total == 9 and dealer in ["3", "4", "5", "6"]:
        return "double"
    if player_total <= 8:
        return "hit"
    return "hit"

from typing import List

class CardCounter:
    """Simple Hi-Lo card counter."""

    def __init__(self) -> None:
        self.running_count = 0

    def reset(self) -> None:
        self.running_count = 0

    def add_card(self, card: str) -> None:
        """Update running count with a single card."""
        value = card.upper()
        if value in ["2", "3", "4", "5", "6"]:
            self.running_count += 1
        elif value in ["10", "J", "Q", "K", "A"]:
            self.running_count -= 1
        # 7,8,9 are zero

    def get_count(self) -> int:
        return self.running_count


def basic_strategy(player_total: int, dealer_card: str) -> str:
    """Return a very simplified blackjack decision."""
    dealer = dealer_card.upper()
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

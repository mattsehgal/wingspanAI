import random

from src.game.bird_card import BirdCard
from src.game.bonus_card import BonusCard
from src.parsing.parse_csv import parse_csv

from typing import List, Union


class Deck:
    def __init__(self):
        self.deck = []
        self.discard = []

    def draw(self, n: int) -> List[Union[BirdCard, BonusCard]]:
        return [self.deck.pop(0) for _ in range(n)]

    def discard(self, cards: List[Union[BirdCard, BonusCard]]):
        self.discard.extend(cards)


class BirdDeck(Deck):
    def __init__(self):
        self.deck = self._init_deck()
        self.tray = {bird_card.id: bird_card for bird_card in self.deck[:3]}
        self.deck = self.deck[3:]

    @staticmethod
    def _init_deck() -> List[BirdCard]:
        # df = pd.read_csv('/kaggle/input/wingspan-base-game-birds-cleaned/BaseGameBirds.csv')
        df = parse_csv()
        deck = [BirdCard(row) for index, row in df.iterrows()]
        random.shuffle(deck)
        return deck

    def _draw_from_deck(self) -> BirdCard:
        """Draws a card from the deck."""
        if self.deck:
            drawn_card = self.deck.pop(0)
            return drawn_card
        else:
            return None  # Return None if the deck is empty

    def _draw_from_tray(self, bird_id: int) -> BirdCard:
        """Draws a card from the tray based on position (0, 1, or 2)."""
        if bird_id in self.tray:
            drawn_card = self.tray.pop(bird_id)
            return drawn_card
        else:
            return None  # Return None for invalid position

    def draw(self, bird_id: int = -1) -> BirdCard:
        if bird_id == -1:
            return self._draw_from_deck()
        else:
            return self._draw_from_tray(bird_id)

    def refill_tray(self):
        """Refills the tray if any spot is empty."""
        empty_spots = 3 - len(self.tray)
        for _ in range(empty_spots):
            new_card = self.draw_from_deck()
            if new_card:
                self.tray.append(new_card)
            else:
                break  # Stop refilling if the deck is empty


class BonusDeck(Deck):
    def __init__(self):
        self.deck: List[BirdCard] = self._init_deck()
        self.discard: List[BonusCard] = []


if __name__ == '__main__':
    deck = BirdDeck()
    print(deck)

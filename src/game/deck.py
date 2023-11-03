import random
import pandas as pd
from typing import List
from bird_card import BirdCard


class Deck:

    def __init__(self):
        self.deck = self._init_deck()
        self.tray = self.deck[:3]
        self.deck = self.deck[3:]

    def _init_deck(self) -> List[BirdCard]:
        df = pd.read_csv('/kaggle/input/wingspan-base-game-birds-cleaned/BaseGameBirds.csv')
        df['color'] = df['color'].fillna('None')
        df['power_text'] = df['power_text'].fillna('')
        deck = [BirdCard(row) for index, row in df.iterrows()]
        random.shuffle(deck)
        return deck

    def draw_from_deck(self) -> BirdCard:
        """Draws a card from the deck."""
        if self.deck:
            drawn_card = self.deck.pop(0)
            return drawn_card
        else:
            return None  # Return None if the deck is empty

    def draw_from_tray(self, position: int) -> BirdCard:
        """Draws a card from the tray based on position (0, 1, or 2)."""
        if 0 <= position < len(self.tray):
            drawn_card = self.tray.pop(position)
            return drawn_card
        else:
            return None  # Return None for invalid position

    def refill_tray(self):
        """Refills the tray if any spot is empty."""
        empty_spots = 3 - len(self.tray)
        for _ in range(empty_spots):
            new_card = self.draw_from_deck()
            if new_card:
                self.tray.append(new_card)
            else:
                break  # Stop refilling if the deck is empty

    def __str__(self) -> str:
        string = "Deck:\n"
        for card in self.deck:
            string += card.__string__() + "\n"
        return string

    def trayToString(self) -> str:
        string = "Tray:\n"
        for card in self.tray:
            string += card.__string__() + "\n"
        return string

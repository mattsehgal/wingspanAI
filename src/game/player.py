from bird_card import BirdCard
from bonus_card import BonusCard
from board import Board
from deck import BirdDeck

from typing import Dict, List, Union


class Player:
    def __init__(self, player_id: int, name: str):
        self.id = player_id
        self.name = name

        self.bird_cards: List[BirdCard] = []
        self.bonus_cards: List[BonusCard] = []

        self.board = Board(self.id)
        self.food_tokens = {'slug': 0,
                            'wheat': 0,
                            'berry': 0,
                            'fish': 0,
                            'rat': 0}

        self.score = 0

    def play_bird(self, bird_id: int, habitat: str) -> bool:
        bird = self.bird_cards.pop(bird_id)
        # TODO try catch error handle for game rules
        return self.board.play_bird(bird, habitat)

    def gain_food(self, food_choice: Dict[str, int]) -> bool:
        for food, n in food_choice.items():
            if n != 0:
                self.food_tokens[food] += n

    def lay_eggs(self, bird_id_n: Dict[int, int]) -> bool:
        for bird_id, n in bird_id_n.items():
            self.board.lay_eggs(bird_id, n)

    def add_bird_cards(self, bird_cards: List[BirdCard]) -> bool:
        self.bird_cards.extend(bird_cards)

    def discard_bird_cards(self, bird_card_ids: List[int]):
        for card_id in bird_card_ids:
            self.bird_cards.remove(card_id)

    def add_bonus_cards(self, bonus_cards: List[BonusCard]) -> bool:
        self.bonus_cards.extend(bonus_cards)

    def discard_bonus_cards(self, bonus_card_ids: List[int]) -> bool:
        for card_id in bonus_card_ids:
            self.bonus_cards.remove(card_id)


class AIPlayer:
    def __init__(self):
        pass
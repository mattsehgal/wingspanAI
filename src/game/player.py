from board import Board

from typing import Dict, List, Union


class Player:
    def __init__(self, name):
        # deck!
        self.name = name

        self.bird_cards = []
        self.bonus_cards = []

        self.board = Board()
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

    def gain_food(self, food_choice: Dict[str, int]):
        for food, n in food_choice.items():
            if n != 0:
                self.food_tokens[food] += n

    def lay_eggs(self, bird_ids: Dict[int, int]):
        for _id, n in bird_ids.items():
            self.board.lay_egg(_id, n)

    def draw_bird_cards(self, card_choice: Dict[Union[str, int], int]):
        for card, n in card_choice.items():



    def draw_bonus_cards(self):
        pass


class AIPlayer:
    def __init__(self):
        pass
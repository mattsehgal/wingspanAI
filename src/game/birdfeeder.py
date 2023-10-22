import random

from player import Player
from game import Game

from typing import List


class FoodDie:
    def __init__(self):
        self.current_face = None

        self.faces = ['slug', 'wheat', 'slug|wheat', 'berry', 'fish', 'rat']

    def roll(self) -> str:
        face = random.choice(self.faces)
        self.current_face = face
        return face


class Birdfeeder:
    def __init__(self):
        self.dice_in = self._init_dice()
        self.dice_out = []

        self._reroll_dice(self.dice_in)

    @staticmethod
    def _init_dice() -> List[FoodDie]:
        return [FoodDie() for _ in range(5)]

    @staticmethod
    def _reroll_dice(dice: List[FoodDie]):
        for die in dice:
            die.roll()

    def gain(self, tokens):
        # gain based on face, choose from double face first when applicable
        # move from dice_in to dice_out
        pass

    def reroll(self):
        self.dice_in.extend(self.dice_out)
        self.dice_out.clear()
        self._reroll_dice(self.dice_in)

    def roll_not_in(self):
        self._reroll_dice(self.dice_out)

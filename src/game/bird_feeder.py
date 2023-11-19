import random

from typing import Dict


class FoodDie:
    def __init__(self):
        self.current_face = None

        self.faces = ['slug', 'wheat', 'slug|wheat', 'berry', 'fish', 'rat']

    def roll(self) -> str:
        face = random.choice(self.faces)
        self.current_face = face
        return face

    def __eq__(self) -> str:
        return self.current_face


class BirdFeeder:
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

    def _gain_food_from_die(self, ):
        pass

    def _token_in_feeder(self, token: str) -> bool:
        pass

    def gain_food(self, tokens: Dict[str, int]) -> bool:
        # TODO handle reroll
        for token, n in tokens.items():
            for _ in range(n):
                if token in self.dice_in:
                    die = self.dice_in.remove(token)
                    self.dice_out.append(die)
                else:
                    return False

    def reroll(self):
        self.dice_in.extend(self.dice_out)
        self.dice_out.clear()
        self._reroll_dice(self.dice_in)

    def roll_not_in(self):
        self._reroll_dice(self.dice_out)


if __name__ == '__main__':
    bf = BirdFeeder()
    print(bf)
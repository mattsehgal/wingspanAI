from player import Player
from actions import *

from typing import List


class Space:
    def __init__(self, actions):
        self.actions = actions

        self.bird = None

    def execute(self):
        pass


class FullRowSpace(Space):
    def execute(self):
        pass


class Habitat:
    def __init__(self, space_action_n: List[int]):
        self.spaces = self._init_spaces()
        self.curr_open_space = self.spaces[0]

    def _init_spaces(self) -> List[Space]:
        spaces = []

        for idx in range(5):
            actions = self._init_space_actions(idx)
            space = Space(actions)
            spaces.append(space)

        actions = self._init_space_actions(5)
        space = FullRowSpace(actions)
        spaces.append(space)

        return spaces

    def execute(self):
        pass

    def play_bird(self):
        pass


class Board:
    def __init__(self, player):
        self.player = player

        self.forest = Habitat(GainFoodAction, [1, 1, 2, 2, 3, 3])
        self.grassland = Habitat(LayEggsAction, [2, 2, 3, 3, 4, 4])
        self.wetland = Habitat(DrawCardsAction, [1, 1, 2, 2, 3, 3])

        self.habitats = {'forest': self.forest, 'grassland': self.grassland, 'wetland': self.wetland}

    def play_bird(self, bird: BirdCard, habitat: str):
        self.habitats[habitat]


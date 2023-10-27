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
    def __init__(self, action: Action, space_action_n: List[int]):
        self.action = action

        self.space_action_n = space_action_n

        self.spaces = self._init_spaces()

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

    def _init_space_actions(self, space_idx) -> List[Action]:
        n = self.space_action_n[space_idx]
        actions = [self.action(n)]

        # If odd space, add exchange action
        if space_idx % 2 != 0:
            actions.append(ExchangeAction(1))

        return actions


class Board:
    def __init__(self, player):
        self.player = player

        self.forest = Habitat(GainFoodAction, [1, 1, 2, 2, 3, 3])
        self.grassland = Habitat(LayEggsAction, [2, 2, 3, 3, 4, 4])
        self.wetland = Habitat(DrawCardsAction, [1, 1, 2, 2, 3, 3])


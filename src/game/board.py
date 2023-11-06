from actions import *
from bird_card import BirdCard

from typing import List


class Space:
    def __init__(self, actions: ActionSequence):
        self.actions = actions

        self.bird: BirdCard = None

    def execute(self):
        pass


class FullRowSpace(Space):
    def execute(self):
        pass


class Habitat:
    def __init__(self, space_action_n: List[int]):
        self.spaces = self._init_spaces()
        self.birds: Dict[int, BirdCard] = {}
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

    def _update_curr_open_space(self):
        if self.curr_open_space.bird:
            curr_idx = self.spaces.index(self.curr_open_space)
            self.curr_open_space = self.spaces[curr_idx+1]

    def execute(self):
        curr_idx = self.spaces.index(self.curr_open_space)
        for space in self.spaces[:curr_idx]:
            space.execute()

    def play_bird(self, bird: BirdCard):
        if not isinstance(self.curr_open_space, FullRowSpace):
            self.curr_open_space.bird = bird
            self._update_curr_open_space()
            self.birds[bird.id] = bird


class Board:
    def __init__(self, player_id: int):
        self.player_id = player_id

        self.forest = Habitat(GainFoodAction, [1, 1, 2, 2, 3, 3])
        self.grassland = Habitat(LayEggsAction, [2, 2, 3, 3, 4, 4])
        self.wetland = Habitat(DrawCardsAction, [1, 1, 2, 2, 3, 3])

        self.habitats = {'forest': self.forest, 'grassland': self.grassland, 'wetland': self.wetland}
        self.played_birds: Dict[int, BirdCard] = {}

    def play_bird(self, bird: BirdCard, habitat: str):
        self.habitats[habitat].play_bird(bird)
        bird.played_habitat = habitat
        self.played_birds[bird.id] = bird

    def lay_eggs(self, bird_id: int, n: int):
        self.played_birds[bird_id].eggs += n



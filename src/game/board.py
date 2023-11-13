from actions import *
from bird_card import BirdCard

from typing import List


class Space:
    def __init__(self, actions: ActionSequence):
        self.actions = actions
        self.bird: BirdCard = None

    def execute(self, game_state):
        if self.bird:
            self.bird.execute(game_state)
        else:
            self.actions.execute(game_state)


class FullRowSpace(Space):
    def __init__(self, actions: ActionSequence):
        super().__init__(actions)

    def execute(self, game_state):
        self.actions.execute(game_state)


class Habitat:
    def __init__(self, base_action: Action, space_action_n: List[int]):
        self.base_action = base_action
        self.spaces = self._init_spaces(space_action_n)
        self.birds: Dict[int, BirdCard] = {}
        self.curr_open_space = self.spaces[0]

    def _init_spaces(self, action_n: List[int]) -> List[Space]:
        spaces = []

        for i, n in enumerate(action_n):
            args = {'n': n}
            actions = [self.base_action(args)]
            # If odd (exchange spaces)
            if i % 2 != 0:
                exch_args = {}
                actions.append(ExchangeAction(exch_args))
            # If last space (no bird)
            if i+1 == len(action_n):
                space = FullRowSpace(actions)
            else:
                space = Space(ActionSequence(actions))
            spaces.append(space)

        return spaces

    def _update_curr_open_space(self):
        if self.curr_open_space.bird:
            curr_idx = self.spaces.index(self.curr_open_space)
            self.curr_open_space = self.spaces[curr_idx+1]

    def execute(self, game_state):
        curr_idx = self.spaces.index(self.curr_open_space)
        for space in self.spaces[:curr_idx]:
            space.execute(game_state)

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



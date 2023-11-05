from actions import *
from bird_card import BirdCard
from state import BoardState, HabitatState

from typing import List, Optional


class Space:
    def __init__(self, actions: ActionSequence):
        self.actions = actions
        self.bird: BirdCard = None

    def play_bird(self, bird: BirdCard):
        self.bird = bird
        self.actions = bird.power

    def execute(self, state: State):
        self.actions.execute(state)


class FullRowSpace(Space):
    def __init__(self, actions: ActionSequence):
        super(actions)

    def execute(self, state: State):
        self.actions.execute(state)


class Habitat:
    def __init__(self, base_action: Action, space_action_n: List[int]):
        self.name = {GainFoodAction: 'forest', LayEggsAction: 'grassland', DrawCardsAction: 'wetland'}[self.base_action]
        self.base_action = base_action
        self.base_item = {GainFoodAction: 'food', LayEggsAction: 'egg', DrawCardsAction: 'card'}[self.base_action]
        self.space_action_n = space_action_n
        self.spaces = self._init_spaces()
        self.curr_open_idx = 0
        self.curr_open_space = self.spaces[0]
        self.state = self._to_state()

    def _init_space_actions(self, idx: int) -> ActionSequence:
        n = self.space_action_n[idx]

        if n % 2 == 0:
            return ActionSequence([self.base_action({})])
        else:
            return ActionSequence([
                self.base_action,
                ExchangeAction({'recv_item': self.base_item})
            ])

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

    def _to_state(self) -> HabitatState:
        bird_states = [space.bird.state for space in self.spaces[:self.curr_open_idx]]
        return HabitatState(self)

    def execute(self):
        pass

    def play_bird(self, bird: BirdCard):
        self.curr_open_space.play_bird(bird)
        self.curr_open_idx += 1
        self.curr_open_space = self.spaces[self.curr_open_idx]


class Board:
    def __init__(self, player_id: int):
        self.player_id = player_id

        self.forest = Habitat(GainFoodAction, [1, 1, 2, 2, 3, 3])
        self.grassland = Habitat(LayEggsAction, [2, 2, 3, 3, 4, 4])
        self.wetland = Habitat(DrawCardsAction, [1, 1, 2, 2, 3, 3])

        self.habitats = {'forest': self.forest, 'grassland': self.grassland, 'wetland': self.wetland}

    def play_bird(self, bird: BirdCard, habitat: str):
        self.habitats[habitat].play_bird()


from game_controller import GameController
from game_state import GameState

from typing import List


class GameLoop:
    def __init__(self, player_names: List[str]):
        self.game_controller = self._init_game_controller(player_names)

    def _init_game_controller(self, player_names: List[str]) -> GameState:
        state = GameState(player_names)
        return GameController(state)


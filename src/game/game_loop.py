from game_controller import GameController
from game_state import GameState

from typing import List


class GameLoop:
    def __init__(self, player_names: List[str]):
        self.game_controller = self._init_game_controller(player_names)

    @staticmethod
    def _init_game_controller(player_names: List[str]) -> GameState:
        state = GameState(player_names)
        return GameController(state)

    def play(self):
        pass


if __name__ == '__main__':
    g = GameLoop(['p1', 'p2'])
    g.play()
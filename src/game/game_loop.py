from game_controller import GameController
from game_state import GameState

from typing import List


class GameLoop:
    def __init__(self, player_names: List[str]):
        self.game_controller = self._init_game_controller(player_names)
        # Game variables
        self.player_turns = 8
        self.player_turn_number = 1
        self.rounds = 4
        self.round_number = 1

    @staticmethod
    def _init_game_controller(player_names: List[str]) -> GameController:
        state = GameState(player_names)
        return GameController(state)

    def play(self):
        while self.round_number < self.rounds:
            self.round_number += 1

            while self.player_turn_number < self.player_turns:
                self.player_turn_number += 1

                for _ in self.game_controller.game_state.players:
                    self.game_controller.next_turn()

            self.player_turns -= 1



if __name__ == '__main__':
    g = GameLoop(['p1', 'p2'])
    g.play()
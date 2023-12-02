from src.game.game_controller import GameController
from src.game.game_state import GameState
from src.game.player_prompter import Prompter

from typing import List


class GameLoop:
    def __init__(self):
        self.game_controller = self._init_game_controller(self._init_player_names())
        # Game variables
        self.player_turns = 8
        self.player_turn_number = 1
        self.rounds = 4
        self.round_number = 1

    @staticmethod
    def _init_game_controller(player_names: List[str]) -> GameController:
        state = GameState(player_names)
        return GameController(state)

    @staticmethod
    def _init_player_names() -> List[str]:
        names = Prompter().get_players()
        return names

    def play(self):
        while self.round_number < self.rounds:
            self.round_number += 1

            while self.player_turn_number < self.player_turns:
                self.player_turn_number += 1

                for _ in self.game_controller.game_state.players:
                    self.game_controller.next_turn()

            self.game_controller.calculate_round_goal()
            self.player_turns -= 1


if __name__ == '__main__':
    g = GameLoop(['p1', 'p2'])
    g.play()

from actions import Action
from game_state import GameState


class GameController:
    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def execute_action(self, action: Action):
        action.execute(self.game_state)


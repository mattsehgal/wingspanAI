from actions import Action
from game_state import GameState
from player_prompter import Prompter

from typing import Dict, List


class GameController:
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.prompter = Prompter()

        self.history: List[GameState] = [game_state]

    def calculate_round_goals(self):
        round_goals = self.game_state.round_goals

    def execute_action(self, action: Action):
        if action.prompt:
            choice = self.prompt_user(action.args)
            action.execute(self.game_state, choice)
        else:
            action.execute(self.game_state)

    def next_turn(self):
        current_player = self.game_state.current_player
        choice = self.prompt_user(args={'id': str(current_player.id),
                                        'prompt': 'turn'}
                                  )
        actions = current_player.turn(choice)
        for action in actions:
            self.execute_action(action)

        # Update

    def prompt_user(self, args: Dict[str, str]) -> Dict[str, str]:
        prompt = self.prompter.prompt(args)
        # something
        choice = {}
        return choice


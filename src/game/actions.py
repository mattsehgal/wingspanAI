from state import *

from typing import AnyStr, Dict, List


# Base Player Actions
class Action:
    def __init__(self, args: Dict[str, str] = {}):
        self.args = args

    def execute(self, state: State) -> bool:
        return False


class PlayBirdAction(Action):
    def __init__(self):
        self.type = 'play_bird'

    def execute(self, state: State) -> bool:
        # player = state.current_player
        # choice = state.get_player_input(self.type)
        # bird_id = choice['bird_id']
        # player.play_bird(bird_id)
        pass


class GainFoodAction(Action):
    def __init__(self):
        self.type = 'gain_food'

    def execute(self, state):
        player = state.current_player
        choice = state.get_player_input(self.type, args=self.args)
        player.board.gain_food(choice)


class LayEggsAction(Action):
    def __init__(self):
        self.type = 'lay_eggs'

    def execute(self, state):
        player = state.current_player
        choice = state.get_player_input(self.type, args=self.args)
        player.board.lay_eggs(choice)


class DrawCardsAction(Action):
    def __init__(self):
        self.type = 'draw_cards'

    def execute(self, state):
        player = state.current_player
        choice = state.get_player_input(self.type, args=self.args)
        player.draw_bird_cards(choice)


# Other Actions
class CacheFoodAction(Action):
    def __init__(self):
        self.type = 'cache_food'

    def execute(self, state):
        player = state.current_player
        choice = state.get_player_input(self.type, args=self.args)
        player.board.current_space.bird.cache(self.args)


class ComplexAction(Action):
    def execute(self, state):
        pass


class DiscardAction(Action):
    def execute(self, state):
        player = state.current_player
        args = state.get_player_input(type='discard')
        player.board.discard(args)


class DrawBonusAction(Action):
    def __init__(self, draw_n, discard_n):
        self.draw_n = draw_n
        self.discard_n = discard_n

    def execute(self, state):
        player = state.current_player
        state.bonus_deck.draw(self.draw_n)
        player.discard(item='bonus', n=self.discard_n)


class ExchangeAction(Action):
    def execute(self, state):
        player = state.current_player
        args = state.get_player_input(type='exchange')
        state.exchange(args)


class FlockingAction(Action):
    def execute(self, state):
        player = state.current_player
        args = state.get_player_input(type='flocking')
        player.board.current_space.bird.tuck(args)  # or something


class GiveToPlayerAction(Action):
    def execute(self, state):
        pass


class HuntingAction(Action):
    def execute(self, state):
        pass


class RepeatPowerAction(Action):
    def execute(self, state):
        pass


class ActionSequence:
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def execute(self, state):
        for action in self.actions:
            action.execute(state)


# class ActionFactory:
#     def __init__(self):
#         pass
#
#     def create(self, action: str, args: Dict[str, AnyStr]) -> Action:
#         pass

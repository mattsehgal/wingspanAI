from src.utils.user_input import get_player_input
from state import *

from typing import Dict, List


# Base Player Actions
class Action:
    def __init__(self, action_type: str, args: Dict[str, str] = {}):
        self.type = action_type
        self.args = args

    def execute(self, state: State) -> State:
        return state


class PlayBirdAction(Action):
    def __init__(self, args):
        super('play_bird', args)

    def execute(self, state: PlayerState) -> PlayerState:
        player_id = state.player_id
        board_state = state.board_state
        choice = get_player_input(player_id, self.type, args=self.args)
        bird_id = choice['bird_id']
        habitat = choice['habitat']
        food_tokens = choice['food_tokens']
        egg_bird_ids = choice['egg_bird_ids']


class GainFoodAction(Action):
    def __init__(self, args):
        super('gain_food', args)

    def execute(self, state: GameState) -> State:
        player_id = state.current_player_id
        choice = get_player_input(player_id, self.type, args=self.args)
        location = choice['location']
        if location == 'bird_feeder':
            food_dice = choice['food']
            state.gain_from_birdfeeder(food_dice)
        elif location == 'supply':
            food_tokens = choice['food']
            state.gain_from_supply(food_tokens)
        return state


class LayEggsAction(Action):
    def __init__(self, args):
        super('lay_eggs', args)

    def execute(self, state: BoardState):
        player_id = state.player_id
        choice = get_player_input(player_id, self.type, args=self.args)
        bird_ids = choice['bird_ids']
        egg_n = choice['egg_n']
        state.lay_eggs(bird_ids, egg_n)



class DrawCardsAction(Action):
    def __init__(self):
        self.type = 'draw_cards'

    def execute(self, state: GameState):
        player_id = state.current_player_id
        choice = state.get_player_input(player_id, self.type, args=self.args)
        pass


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

    def execute(self, game_state):
        player_state = game_state.current_player_state
        game_state
        # player.discard(item='bonus', n=self.discard_n)


class ExchangeAction(Action):
    def __init__(self, args):
        super('exchange', args)
        self.recv_action = {
            'food': GainFoodAction,
            'egg': LayEggsAction,
            'card': DrawCardsAction
        }[args['recv_item']]

    def execute(self, state: GameState) -> GameState:
        discard = DiscardAction(self.args)
        receive = self.recv_action(self.args)
        new_state = discard.execute(state)
        return receive.execute(new_state)


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

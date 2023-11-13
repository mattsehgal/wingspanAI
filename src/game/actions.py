from typing import AnyStr, Dict, List, Union


# Base Player Actions
class Action:
    def __init__(self, args: Dict[str, AnyStr] = {}):
        self.args = args

    def execute(self, game_state) -> bool:
        return False


class PlayBirdAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'play_bird'
        try:
            # TODO verify loc1 arg
            self.habitat = self.args['location1']
        except KeyError:
            self.habitat = None

    def execute(self, choice: Dict[str, Union[int, str]], game_state) -> bool:
        habitat = self.habitat if self.habitat else choice['habitat']
        game_state.play_bird(choice['bird_id'], habitat)


class GainFoodAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'gain_food'

    def execute(self, choice: Dict[str, Union[int, str]], game_state):
        game_state.gain_food(choice['food_tokens'], self.args['location'])


class LayEggsAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'lay_eggs'

    def execute(self, game_state):
        player = game_state.current_player
        choice = game_state.get_player_input(self.name, args=self.args)
        player.board.lay_eggs(choice)


class DrawCardsAction(Action):
    def __init__(self, args):
        self.name = 'draw_cards'
        super().__init__(args)

    def execute(self, game_state):
        player = game_state.current_player
        choice = game_state.get_player_input(self.name, args=self.args)
        player.draw_bird_cards(choice)


# Other Actions
class CacheFoodAction(Action):
    def __init__(self):
        self.name = 'cache_food'

    def execute(self, game_state):
        player = game_state.current_player
        choice = game_state.get_player_input(self.name, args=self.args)
        player.board.current_space.bird.cache(self.args)


class ComplexAction(Action):
    def execute(self, game_state):
        pass


class DiscardAction(Action):
    def execute(self, game_state):
        player = game_state.current_player
        args = game_state.get_player_input(type='discard')
        player.board.discard(args)


class DrawBonusAction(Action):
    def __init__(self, draw_n, discard_n):
        self.draw_n = draw_n
        self.discard_n = discard_n

    def execute(self, game_state):
        player = game_state.current_player
        game_state.bonus_deck.draw(self.draw_n)
        player.discard(item='bonus', n=self.discard_n)


class ExchangeAction(Action):
    def execute(self, game_state):
        player = game_state.current_player
        args = game_state.get_player_input(type='exchange')
        game_state.exchange(args)


class FlockingAction(Action):
    def execute(self, game_state):
        player = game_state.current_player
        args = game_state.get_player_input(type='flocking')
        player.board.current_space.bird.tuck(args)  # or something


class GiveToPlayerAction(Action):
    def execute(self, game_state):
        pass


class HuntingAction(Action):
    def execute(self, game_state):
        pass


class RepeatPowerAction(Action):
    def execute(self, game_state):
        pass


class ActionSequence:
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def execute(self, game_state):
        for action in self.actions:
            action.execute(game_state)

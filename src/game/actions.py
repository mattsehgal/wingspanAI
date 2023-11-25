from typing import Dict, List, Union


# Base Player Actions
class Action:
    def __init__(self, args: Dict[str, str] = {}):
        self.args = args
        self.prompt = False

    def execute(self, game_state: "GameState") -> bool:
        return True


class PlayBirdAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'PLAY_BIRD'
        self.habitat = self.args['LOCATION']

    def execute(self, choice, game_state: "GameState") -> bool:
        habitat = self.habitat if self.habitat else choice['habitat']
        game_state.play_bird(choice['bird_id'], habitat)


class GainFoodAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'GAIN_FOOD'
        self.n = self.args['N']
        self.item = self.args['ITEM']
        self.location = self.args['LOCATION']

    def execute(self, game_state: "GameState", choice: Dict[str, str]) -> bool:
        food_tokens = choice['food_tokens']
        game_state.gain_food(food_tokens, self.location)


class LayEggsAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'LAY_EGGS'
        self.n = self.args['N']
        self.location = self.args['LOCATION']

    def execute(self, choice, game_state: "GameState") -> bool:
        game_state.lay_eggs(choice)


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
    def __init__(self, args):
        super().__init__(args)
        self.name = 'cache_food'

    def execute(self, game_state):
        player = game_state.current_player
        choice = game_state.get_player_input(self.name, args=self.args)


class ComplexAction(Action):
    def execute(self, game_state):
        pass


class DiscardAction(Action):
    def execute(self, game_state):
        player = game_state.current_player
        args = game_state.get_player_input(type='discard')


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


class ActionFactory:
    _MAPPER = {
        'CACHE': CacheFoodAction,
        'GAIN': GainFoodAction,
    }

    @classmethod
    def create(cls, action: str, args: Dict[str, str]) -> Action:
        return cls._MAPPER[action](args)


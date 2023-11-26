from typing import Dict, List


# Base Player Actions
class Action:
    def __init__(self, args: Dict[str, str] = {}):
        self.args = args

    def execute(self, game_state: "GameState") -> bool:
        return True


class PlayBirdAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'PLAY_BIRD'
        self.habitat = self.args['LOCATION']

    def execute(self, choice, game_state: "GameState") -> bool:
        habitat = self.habitat if self.habitat else choice['HABITAT']
        game_state.play_bird(choice['BIRD_ID'], habitat)


class GainFoodAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'GAIN_FOOD'
        self.n = self.args['N']
        self.item = self.args['ITEM']
        self.location = self.args['LOCATION']

    def execute(self, game_state: "GameState", choice: Dict[str, str]) -> bool:
        food_tokens = choice['FOOD_TOKENS']
        game_state.gain_food(food_tokens, self.location)


class LayEggsAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'LAY_EGGS'
        self.n = self.args['N']
        self.location = self.args['LOCATION']

    def execute(self, game_state: "GameState", choice: Dict[str, str]) -> bool:
        game_state.lay_eggs(choice)


class DrawCardsAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'DRAW_CARDS'
        self.n = self.args['N']
        self.location = self.args['LOCATION']

    def execute(self, game_state, choice):
        pass


# Other Actions
class CacheFoodAction(Action):
    def __init__(self, args):
        super().__init__(args)
        self.name = 'CACHE_FOOD'

    def execute(self, game_state, choice):
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


class EntailmentAction(Action):
    def __init__(self, args, entailed_action: Action):
        super().__init__(args)
        self.name = 'ENTAILMENT'
        self.entailment = args['ENTAILMENT']

        self.entailed_action = entailed_action

    def execute(self, game_state: "GameState") -> bool:
        entailment = True
        if entailment:
            self.entailed_action.execute(game_state)


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


class ActionSequence(Action):
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def execute(self, game_state):
        for action in self.actions:
            action.execute(game_state)


class ActionFactory:
    _MAPPER = {
        'CACHE': CacheFoodAction,
        'GAIN': GainFoodAction,
        'ENTAILMENT': EntailmentAction,
    }

    @classmethod
    def create(cls, action: str, args: Dict[str, str], entailed: str = None) -> Action:
        if entailed:
            args['ENTAILMENT'] = action
            entailed_action = cls._MAPPER[entailed]
            return cls._MAPPER['ENTAILMENT'](args, entailed_action=entailed_action)
        else:
            return cls._MAPPER[action](args)


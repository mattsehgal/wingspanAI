from actions import *
from bird_card import BirdCard
from game import Game


class BirdPower:
    def __init__(self, bird, **kwargs):
        self.bird = bird
        self.action = Action(kwargs)

    def execute(self, game):
        self.action.execute(game)


class DrawBonusPower(BirdPower):
    def __init__(self, bird, **kwargs):
        super(bird)
        self.actions = self._parse_kwargs_to_actions(**kwargs)
#{'action1': 'draw', 'n1': '2', 'item1': 'new bonus cards', 'location1': None, 'entailment1': 'and', 'action2': 'keep', 'n2': '1', 'item2': None, 'location2': None, 'condition1': None}
    def _parse_kwargs_to_actions(self, **kwargs) -> ActionSequence:
        n1 = kwargs.get('n1', None)
        n2 = kwargs.get('n2', None)
        action1 = DrawBonusAction(n1, n2)
        return ActionSequence([action1])

    def execute(self, game):
        self.actions.execute()


class CacheFoodPower(BirdPower):
    def __init__(self, bird, from_supply: bool):
        super(bird)
        self.from_supply = from_supply

    def execute(self, game):



class GainFoodPower(BirdPower):
    def __init__(self):
        pass


class LayEggsPower(BirdPower):
    def __init__(self):
        pass


class DrawCardsPower(BirdPower):
    def __init__(self):
        pass


class FlockingPower(BirdPower):
    def __init__(self):
        pass


class HuntingPower(BirdPower):
    def __init__(self):
        pass


class MigratingPower(BirdPower):
    def __init__(self):
        pass


class PlayAnotherPower(BirdPower):
    def __init__(self):
        pass


class BirdPowerFactory:
    def __init__(self):
        pass

    def _build_draw_bonus(self, **kwargs) -> DrawBonusPower:
        power = DrawBonusPower()

    def _build_draw_cards(self, **kwargs) -> DrawCardsPower:
        pass

    def create(self, **kwargs) -> BirdPower:
        power = None

        action1 = kwargs.get('action1', None)

        if action1 == 'draw':
            item1 = kwargs.get('item1', None)

            if 'bonus' in item1:
                return self._build_draw_bonus(**kwargs)
            else:
                return self.

# parse_csv:parse_bird_powers() -> ... -> BirdPower -> ActionFactory:create(action, args) -> Action

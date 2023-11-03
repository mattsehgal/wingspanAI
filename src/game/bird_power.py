from actions import *
from bird_card import BirdCard
from game import Game


class BirdPower:
    def __init__(self, bird: BirdCard, actions: ActionSequence):
        self.bird = bird
        self.actions = actions

    def execute(self, game):
        self.actions.execute(game)


class GainFoodPower(BirdPower):
    def execute(self, game):
        self.actions.execute(game)


class LayEggsPower(BirdPower):
    def __init__(self):
        pass


class DrawCardsPower(BirdPower):
    def __init__(self, bird, **kwargs):
        super(bird)
        self.actions = self._parse_kwargs_to_actions(**kwargs)

    def _parse_kwargs_to_actions(self, **kwargs) -> ActionSequence:
        n1 = kwargs.get('n1', None)
        location1 = kwargs.get('location1', None)
        entailment1 = kwargs.get('entailment1', None)

        if entailment1:
            pass

        return ActionSequence([])

    def execute(self, game):
        pass


class DrawBonusPower(BirdPower):
    def __init__(self, bird, actions):
        super(bird, actions)

    def execute(self, game):
        self.actions.execute()


class CacheFoodPower(BirdPower):
    def __init__(self, bird, actions):
        super(bird, actions)

    def execute(self, game):
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

    def _build_cache_food(self, **kwargs) -> CacheFoodPower:
        pass

    def _build_draw_bonus(self, **kwargs) -> DrawBonusPower:
        n1 = kwargs.get('n1', None)
        n2 = kwargs.get('n2', None)
        actions = ActionSequence([DrawBonusAction(draw_n=n1, discard_n=n2)])

        return DrawBonusPower(actions)

    def _build_draw_cards(self, **kwargs) -> DrawCardsPower:
        n1 = kwargs.get('n1', None)
        location1 = kwargs.get('location1', None)


    def create(self, **kwargs) -> BirdPower:
        action1 = kwargs.get('action1', None)
        # Actions: cache|discard|draw|gain|keep|lay|look at|move|play|repeat|roll|trade|tuck
        match action1:
            case 'cache':
                return self._build_cache_food(**kwargs)

            case 'draw':
                item1 = kwargs.get('item1', None)
                if 'bonus' in item1:
                    return self._build_draw_bonus(**kwargs)
                else:
                    return self._build_draw_cards(**kwargs)

            case 'play':
                return self._build_play_addtional_bird(**kwargs)




# parse_csv:parse_bird_powers() -> ... -> BirdPower -> ActionFactory:create(action, args) -> Action

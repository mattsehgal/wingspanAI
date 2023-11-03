from actions import *


class BirdPower:
    def __init__(self, bird_id: int, actions: ActionSequence):
        self.bird = bird_id
        self.actions = actions

    def execute(self):
        self.actions.execute()


class GainFoodPower(BirdPower):
    def execute(self):
        self.actions.execute()


class LayEggsPower(BirdPower):
    def __init__(self):
        pass


class DrawCardsPower(BirdPower):
    def execute(self):
        self.actions.execute()


class DrawBonusPower(BirdPower):
    def execute(self):
        self.actions.execute()


class CacheFoodPower(BirdPower):
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
    def __init__(self, bird_id: int):
        self.bird_id = bird_id

    def _build_none_power(self) -> BirdPower:
        return BirdPower(self.bird_id, ActionSequence([]))

    def _build_cache_food(self, **kwargs) -> CacheFoodPower:
        pass

    def _build_draw_bonus(self, **kwargs) -> DrawBonusPower:
        n1 = kwargs.get('n1', None)
        n2 = kwargs.get('n2', None)
        actions = ActionSequence([DrawBonusAction(draw_n=n1, discard_n=n2)])

        return DrawBonusPower(self.bird_id, actions)

    def _build_draw_cards(self, **kwargs) -> DrawCardsPower:
        n1 = kwargs.get('n1', None)
        location1 = kwargs.get('location1', None)

    def create(self, **kwargs) -> BirdPower:
        if self.bird_id == 226:
            print('here')
        if not kwargs:
            return self._build_none_power()

        action1 = kwargs.get('action1', None)
        # Actions: cache|discard|draw|gain|keep|lay|look at|move|play|repeat|roll|trade|tuck
        if action1 == 'cache':
            return self._build_cache_food(**kwargs)

        elif action1 == 'draw':
            item1 = kwargs.get('item1', None)
            if 'bonus' in item1:
                return self._build_draw_bonus(**kwargs)
            else:
                return self._build_draw_cards(**kwargs)

        else:
            return None

        # elif action1 == 'play':
        #     return self._build_play_addtional_bird(**kwargs)




# parse_csv:parse_bird_powers() -> ... -> BirdPower -> ActionFactory:create(action, args) -> Action

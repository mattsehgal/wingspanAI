from actions import *


class BirdPower:
    def __init__(self, bird_id: int, actions: ActionSequence):
        self.bird_id = bird_id
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
    def __init__(self, bird_id, **kwargs):
        super(bird_id)
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

    def _build_gain_food(self, **kwargs) -> GainFoodPower:
        item1 = kwargs.get('n1', None)
        n1 = kwargs.get('n1', None)
        location1 = kwargs.get('location1', None)
        entailment1 = kwargs.get('entailment1', None)
        if entailment1:
            # TODO vars2
            pass
        else:
            actions = ActionSequence([GainFoodAction()])
        return GainFoodPower(actions)

    def _build_flocking(self, **kwargs) -> FlockingPower:
        actions = ActionSequence([])
        return FlockingPower(actions)

    def create(self, **kwargs) -> BirdPower:
        action1 = kwargs.get('action1', None)
        # Actions: cache|discard|draw|gain|keep|lay|look at|move|play|repeat|roll|trade|tuck
        # CACHE
        if action1 == 'cache':
            return self._build_cache_food(**kwargs)
        # DISCARD
        elif action1 == 'discard':
            return self._build_discard_item(**kwargs)
        # DRAW CARD
        elif action1 == 'draw':
            item1 = kwargs.get('item1', None)
            if 'bonus' in item1:
                return self._build_draw_bonus(**kwargs)
            else:
                return self._build_draw_cards(**kwargs)
        # FLOCKING
        elif action1 == 'tuck':
            return self._build_flocking(**kwargs)
        # GAIN FOOD
        elif action1 == 'gain':
            return self._build_gain_food(**kwargs)
        # HUNTING
        elif action1 == 'look at' or action1 == 'roll':
            return self._build_hunting(**kwargs)
        # KEEP
        elif action1 == 'keep':
            print('idk')
        # LAY EGGS
        elif action1 == 'lay':
            return self._build_lay_eggs(**kwargs)
        # MIGRATE
        elif action1 == 'move':
            return self._build_migrate(**kwargs)
        # PLAY ADDITIONAL BIRD
        elif action1 == 'play':
            return self._build_play_addtional_bird(**kwargs)
        # REPEAT
        elif action1 == 'repeat':
            return self._build_repeat(**kwargs)
        # TRADE
        elif action1 == 'trade':
            pass
        # DEFAULT
        else:
            return BirdPower(ActionSequence([]))

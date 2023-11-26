from src.game.actions import *


class BirdPower:
    def __init__(self, bird_id: int, actions: ActionSequence):
        self.bird_id = bird_id
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

    def _to_action_args(self, **kwargs) -> List[Dict[str, str]]:
        action_args = []
        arg_list = []
        for kwarg in kwargs:
            if 'ACTION' in kwarg:
                if arg_list:
                    action_args.append(
                        {k[:-1] if k[-1].isdigit() else k: v
                         for k, v in kwargs.items()
                         if k in arg_list}
                    )
                    arg_list.clear()
                continue
            arg_list.append(kwarg)
        if arg_list:
            action_args.append(
                {k[:-1] if k[-1].isdigit() else k: v
                 for k, v in kwargs.items()
                 if k in arg_list}
            )

        return action_args

    def _build_cache_food(self, **kwargs) -> CacheFoodPower:
        pass

    def _build_draw_bonus(self, **kwargs) -> DrawBonusPower:
        n1 = kwargs.get('N1', None)
        n2 = kwargs.get('N2', None)
        actions = ActionSequence([DrawBonusAction(draw_n=n1, discard_n=n2)])

        return DrawBonusPower(self.bird_id, actions)

    def _build_draw_cards(self, **kwargs) -> DrawCardsPower:
        n1 = kwargs.get('N1', None)
        location1 = kwargs.get('LOCATION1', None)

    def _build_gain_food(self, **kwargs) -> GainFoodPower:
        action1 = kwargs.get('ACTION1', None)
        item1 = kwargs.get('ITEM1', None)
        n1 = kwargs.get('N1', None)
        location1 = kwargs.get('LOCATION1', None)
        entailment1 = kwargs.get('ENTAILMENT1', None)

        args = self._to_action_args(**kwargs)
        action_list = [ActionFactory.create(action1, args[0])]

        if entailment1:
            action2 = kwargs.get('ACTION2', None)
            action_list.append(ActionFactory.create(entailment1, args[1], entailed=action2))

        action_seq = ActionSequence(action_list)
        return GainFoodPower(self.bird_id, action_seq)

    def _build_flocking(self, **kwargs) -> FlockingPower:
        actions = ActionSequence([])
        return FlockingPower(actions)

    def create(self, **kwargs) -> BirdPower:
        action1 = kwargs.get('ACTION1', None)
        # Actions: cache|discard|draw|gain|keep|lay|look at|move|play|repeat|roll|trade|tuck
        # CACHE
        if action1 == 'CACHE':
            return self._build_cache_food(**kwargs)
        # DISCARD
        elif action1 == 'DISCARD':
            return self._build_discard_item(**kwargs)
        # DRAW CARD
        elif action1 == 'DRAW':
            item1 = kwargs.get('ITEM1', None)
            if 'BONUS' in item1:
                return self._build_draw_bonus(**kwargs)
            else:
                return self._build_draw_cards(**kwargs)
        # FLOCKING
        elif action1 == 'TUCK':
            return self._build_flocking(**kwargs)
        # GAIN FOOD
        elif action1 == 'GAIN':
            return self._build_gain_food(**kwargs)
        # HUNTING
        elif action1 == 'LOOK' or action1 == 'ROLL':
            return self._build_hunting(**kwargs)
        # KEEP
        elif action1 == 'KEEP':
            print('idk')
        # LAY EGGS
        elif action1 == 'LAY':
            return self._build_lay_eggs(**kwargs)
        # MIGRATE
        elif action1 == 'MOVE':
            return self._build_migrate(**kwargs)
        # PLAY ADDITIONAL BIRD
        elif action1 == 'PLAY':
            return self._build_play_addtional_bird(**kwargs)
        # REPEAT
        elif action1 == 'REPEAT':
            return self._build_repeat(**kwargs)
        # TRADE
        elif action1 == 'TRADE':
            pass
        # DEFAULT
        else:
            return BirdPower(ActionSequence([]))


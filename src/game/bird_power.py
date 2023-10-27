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
        self.action = DrawBonusAction(kwargs)

    def execute(self, game):
        self.action.execute()


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

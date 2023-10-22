from game import Game
from player import Player


class BirdPower:
    def execute(self, game, player):
        pass


class DrawBonusPower(BirdPower):
    def __init__(self, draw, keep):
        self.draw_num = draw
        self.keep_num = keep

    def execute(self, game, player):
        pass


class CacheFoodPower(BirdPower):
    def __init__(self):
        pass


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

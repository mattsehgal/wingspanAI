from bird_card import BirdCard
from game import Game


class BirdPower:
    def __init__(self, bird):
        self.bird = bird

    def execute(self, game):
        pass


class DrawBonusPower(BirdPower):
    def __init__(self, bird, draw, keep):
        super(bird)
        self.draw_num = draw
        self.keep_num = keep

    def execute(self, game):
        player = self.game.current_player

        for _ in range(self.draw_num):
            # Holy balls this gets complicated
            pass


class CacheFoodPower(BirdPower):
    def __init__(self, bird, from_supply: bool):
        super(bird)
        self.from_supply = from_supply

    def execute(self, game):
        player = self.game.current_player

        # This might be different in practice
        if self.from_supply:
            self.bird.cache += 1
        # else game.birdfeeder.gain_cache()



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

import pandas as pd
from typing import List
from bird_power import BirdPower


class BirdCard:
    def __init__(self, birdCard):
        self.name = self._init_name(birdCard)
        self.habitat = self._init_habitat(birdCard)
        self.food_cost = self._init_food_cost(birdCard)
        self.points = self._init_points(birdCard)
        self.wingspan = self._init_wingspan(birdCard)
        self.color = self._init_color(birdCard)
        self.power = self._init_power(birdCard)
        self.egg_capacity = self._init_egg_capacity(birdCard)
        self.nest_type = self._init_nest_type(birdCard)

    def _init_name(self, birdCard) -> str:
        return birdCard['common_name']

    def _init_habitat(self, birdCard) -> List[bool]:
        return {'forest': birdCard['forest'], 'grassland': birdCard['grassland'], 'wetland': birdCard['wetland']}

    def _init_food_cost(self, birdCard) -> str:
        if birdCard['food_slash']:
            food_cost = ("slug/" * birdCard['invertebrate'] +
                         "wheat/" * birdCard['seed'] +
                         "berry/" * birdCard['fruit'] +
                         "rat/" * birdCard['rodent'] +
                         "fish/" * birdCard['fish']
                         )
        else:
            food_cost = ("slug+" * birdCard['invertebrate'] +
                         "wheat+" * birdCard['seed'] +
                         "berry+" * birdCard['fruit'] +
                         "rat+" * birdCard['rodent'] +
                         "fish+" * birdCard['fish'] +
                         "wild+" * birdCard['wild_(food)']
                         )
        return food_cost[:-1]

    def _init_points(self, birdCard) -> int:
        return birdCard['victory_points']

    def _init_power(self, birdCard):
        return BirdPower(birdCard['power_text'], self.color)

    def _init_wingspan(self, birdCard) -> int:
        return birdCard['wingspan']

    def _init_color(self, birdCard) -> str:
        return birdCard['color']

    def _init_egg_capacity(self, birdCard) -> int:
        return birdCard['egg_capacity']

    def _init_nest_type(self, birdCard) -> str:
        return birdCard['nest_type']

    def __repr__(self) -> str:
        return self.name + "\n" + self.food_cost + "\n" + str(self.points) + "\n" + self.power + "\n"

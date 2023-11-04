from bird_power import BirdPower, BirdPowerFactory

from typing import Dict, Optional, Union


class BirdCard:
    def __init__(self, bird_card: Dict[str, Optional[Union[int, str]]]):
        self.id = bird_card['id']
        self.name = bird_card['common_name']
        self.habitat = {
            'forest': bird_card['forest'],
            'grassland': bird_card['grassland'],
            'wetland': bird_card['wetland']
        }
        self.food_cost = self._init_food_cost(bird_card)
        self.points = bird_card['victory_points']
        self.wingspan = bird_card['wingspan']
        self.color = bird_card['color']
        self.power = self._init_power(bird_card)
        self.eggs = 0
        self.egg_capacity = bird_card['egg_capacity']
        self.nest_type = bird_card['nest_type']
        self.state = self._to_state()

        # testing only
        self.power_text = bird_card['power_text']

    def _init_food_cost(self, bird_card) -> str:
        if bird_card['food_slash']:
            food_cost = ("slug/" * bird_card['invertebrate'] +
                         "wheat/" * bird_card['seed'] +
                         "berry/" * bird_card['fruit'] +
                         "rat/" * bird_card['rodent'] +
                         "fish/" * bird_card['fish']
                         )
        else:
            food_cost = ("slug+" * bird_card['invertebrate'] +
                         "wheat+" * bird_card['seed'] +
                         "berry+" * bird_card['fruit'] +
                         "rat+" * bird_card['rodent'] +
                         "fish+" * bird_card['fish'] +
                         "wild+" * bird_card['wild_(food)']
                         )
        return food_cost[:-1]

    def _init_power(self, bird_card) -> BirdPower:
        args = bird_card['power_args']
        if args is None:
            args = {}
        return BirdPowerFactory(bird_card['id']).create(**args)

    def _to_state(self) -> Dict[str, int]:
        return {
            'id': self.id,
            'eggs': self.eggs,
        }

from src.parser.enums.base import AutoName
from enum import auto

from typing import Optional


class Entailment(AutoName):
    MAY = auto()


class Item(AutoName):
    IT = auto()
    OR = auto()
    PREVIOUS = auto()

    @classmethod
    def is_food(cls, item: str) -> bool:
        return '[' in item


class Location(AutoName):
    # FOOD
    BIRDFEEDER = auto()
    SUPPLY = auto()
    # HABITAT
    FOREST = auto()
    GRASSLAND = auto()
    WETLAND = auto()
    # CARD
    CARD = auto()
    THIS = auto()

    @classmethod
    def get_habitat(cls, location: str) -> Optional["Location"]:
        for habitat in [cls.FOREST, cls.GRASSLAND, cls.WETLAND]:
            if habitat.value in location:
                return habitat.value
        return None

    @classmethod
    def THIS_CARD(cls) -> str:
        return ' '.join([cls.THIS.value, cls.CARD.value])

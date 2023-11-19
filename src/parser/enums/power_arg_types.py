from src.parser.enums.base import AutoName
from enum import auto

from typing import Optional


class Entailment(AutoName):
    MAY = auto()


class Item(AutoName):
    IT = auto()
    PREVIOUS = '^'


class Location(AutoName):
    # FOOD
    BIRDFEEDER = auto()
    SUPPLY = auto()
    # HABITAT
    FOREST = auto()
    GRASSLAND = auto()
    WETLAND = auto()
    # CARD
    THIS = auto()

    @classmethod
    def get_habitat(cls, string: str) -> Optional["Location"]:
        for habitat in [cls.FOREST, cls.GRASSLAND, cls.WETLAND]:
            if habitat.value in string:
                return habitat.value
        return None

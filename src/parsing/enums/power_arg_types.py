from src.parsing.enums.base import AutoName
from enum import auto

from typing import Optional


class Entailment(AutoName):
    IYD = 'IF YOU DO'
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
    BIRD = auto()
    CARD = auto()
    DECK = auto()
    HAND = auto()
    THIS = auto()
    TRAY = auto()

    @classmethod
    def _this_x(cls, X: "Location") -> str:
        return ' '.join([cls.THIS.value, X.value])

    @classmethod
    def get_habitat(cls, location: str) -> Optional["Location"]:
        for habitat in [cls.FOREST, cls.GRASSLAND, cls.WETLAND]:
            if habitat.value in location:
                return habitat.value
        return None

    @classmethod
    def ANY_BIRD(cls) -> str:
        return ' '.join([N.ANY.value, cls.BIRD.value])

    @classmethod
    def THIS_BIRD(cls) -> str:
        return cls._this_x(cls.BIRD)

    @classmethod
    def THIS_CARD(cls) -> str:
        return cls._this_x(cls.CARD)


class N(AutoName):
    A = auto()
    ALL = auto()
    ANY = auto()

from enum import Enum, auto


class Entailment(Enum):
    MAY = auto()


class Item(Enum):
    IT = auto()
    PREVIOUS = '^'


class Location(Enum):
    BIRDFEEDER = auto()
    SUPPLY = auto()
    THIS = auto()
    
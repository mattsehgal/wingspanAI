from src.parser.enums.power_arg_types import *

from typing import List


# BIRD POWER ARG PARSING
def parse_entailment(entailment: str) -> str:
    if Entailment.MAY.value in entailment:
        entailment = reduce_to_substring(entailment, Entailment.MAY.value)

    return entailment


def parse_item(item: str) -> List[str]:
    if Item.OR.value in item:
        item = [strip_brackets(it) for it in item.split(' '+Item.OR.value+' ')]
        return item
    elif Item.is_food(item):
        return strip_brackets(item)
    elif Item.IT.value in item:
        item = Item.PREVIOUS.value
    else:
        item = strip_brackets(item)

    return [item]


def parse_location(location: str) -> str:
    # HABITAT/NEST LOCATIONS
    habitat = Location.get_habitat(location)
    if habitat:
        location = habitat
    # GAIN FOOD LOCATIONS
    elif Location.BIRDFEEDER.value in location:
        location = reduce_to_substring(location, Location.BIRDFEEDER.value)
    elif Location.SUPPLY.value in location:
        location = reduce_to_substring(location, Location.SUPPLY.value)
    # CACHE FOOD/LAY EGGS LOCATIONS
    elif Location.BIRD.value in location:
        if Location.ANY_BIRD() in location:
            location = reduce_to_substring(location, Location.ANY_BIRD())
        elif Location.THIS_BIRD() in location:
            location = reduce_to_substring(location, Location.THIS_BIRD())
    elif Location.THIS_CARD() in location:
        location = reduce_to_substring(location, Location.THIS_CARD())
    # DRAW/DISCARD CARDS LOCATIONS
    elif Location.DECK.value in location:
        location = reduce_to_substring(location, Location.DECK.value)
    elif Location.HAND.value in location:
        location = reduce_to_substring(location, Location.HAND.value)
    elif Location.TRAY.value in location:
        location = reduce_to_substring(location, Location.TRAY.value)
    else:
        # TODO handle
        print('Location parse error')

    return location


def parse_n(n: str) -> str:
    if N.ALL.value in n:
        n = N.ANY.value
    elif N.ANY.value in n:
        n = N.ANY.value
    elif N.A.value in n:
        n = str(1)

    return n


# STRING OPS
def reduce_to_substring(string: str, substring: str):
    return substring if substring in string else string


def strip_brackets(string: str) -> str:
    return string.replace('[', '').replace(']', '')


def strip_parens(string: str) -> str:
    return string.replace('(', '').replace(')', '')


def strip_to_brackets(string: str) -> str:
    string = ''.join(string.split('[')[1].split(']')[0])
    return string

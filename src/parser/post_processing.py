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
    elif Location.THIS_CARD() in location:
        location = reduce_to_substring(location, Location.THIS_CARD())
    # DRAW/DISCARD CARDS LOCATIONS

    return location


def parse_n(n: str) -> str:
    # TODO handle getting /d out of any d/ etc, handle words = 1, handle "all"
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

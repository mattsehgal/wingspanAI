from src.game.enums.args.bird_power_args import *

# from typing import Any, Dict, List, Optional, Union


# BIRD POWER ARG PARSING
def parse_entailment(entailment: str) -> str:
    if Entailment.MAY.name in entailment:
        entailment = reduce_to_substring(entailment, Entailment.MAY.name)

    return entailment


def parse_item(item: str) -> str:
    if Item.IT.name in item:
        # ref backward on 'it', add resolve_backwards_refs method
        item = Item.PREVIOUS.name
    else:
        item = strip_brackets(item)

    return item


# TODO fix name/value issue
def parse_location(location: str) -> str:
    # GAIN FOOD LOCATIONS
    if Location.BIRDFEEDER.name in location:
        location = reduce_to_substring(location, Location.BIRDFEEDER.name)
    elif Location.SUPPLY.name in location:
        location = reduce_to_substring(location, Location.SUPPLY.name)
    # CACHE FOOD/LAY EGGS LOCATIONS

    # DRAW/DISCARD CARDS LOCATIONS

    return location


# STRING OPS
def reduce_to_substring(string: str, substring: str):
    return substring if substring in string else string


def remove_parens(string: str) -> str:
    return string.replace('(', '').replace(')', '')


def strip_brackets(string: str) -> str:
    return string.removeprefix('[').removesuffix(']')

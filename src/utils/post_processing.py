# from typing import Any, Dict, List, Optional, Union


# BIRD POWER ARG PARSING
def parse_entailment(entailment: str) -> str:
    if 'may' in entailment:
        reduce_to_substring(entailment, 'may')

    return entailment


def parse_item(item: str) -> str:
    if item:
        item = strip_brackets(item)

        # ref backward on 'it', add resolve_backwards_refs method

    return item


def parse_location(location: str) -> str:
    # GAIN FOOD LOCATIONS
    if 'birdfeeder' in location:
        reduce_to_substring(location, 'birdfeeder')
    elif 'supply' in location:
        reduce_to_substring(location, 'supply')
    # CACHE FOOD/LAY EGGS LOCATIONS

    # DRAW/DISCARD CARDS LOCATIONS

    return location


# STRING OPS
def reduce_to_substring(string: str, substring: str):
    return substring if substring in string else string


def strip_brackets(string: str) -> str:
    return string.removeprefix('[').removesuffix(']')

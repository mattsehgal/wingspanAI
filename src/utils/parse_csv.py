from dotenv import load_dotenv
import os
import pandas as pd
import re

from typing import AnyStr, Dict, List, Optional

load_dotenv()
bird_csv_path = os.environ['BIRD_CSV']
bird_df = pd.read_csv(bird_csv_path)


def get_unique_power_categories(df: pd.DataFrame) -> List[str]:
    uniques = df['power_category'].unique()
    return uniques.tolist()


def parse_first_word_dict(df: pd.DataFrame) -> Dict[str, List[str]]:
    power_list = df['power_text'].tolist()
    res_dict = dict()

    for text in power_list:
        if not isinstance(text, str):
            continue

        text = text.lower()
        first_word = text.split(' ')[0]
        if first_word in res_dict:
            res_dict[first_word].append(text)
        else:
            res_dict[first_word] = [text]

    return res_dict


def get_component_regex(components: List[str]) -> List[str]:
    component_regex = {
        'action': r'(?P<action>play|gain|lay|draw|discard|tuck)',
        'assertion': r'\.$',
        'condition': r'(?P<condition>you may)',
        'end_group': r')',
        'entailment': r'(?P<entailment> ?to ?)',
        'group': r'(',
        'if': r'',
        'item': r'(?P<item>(face-up )?\[.*?\]|new bonus cards?)',
        'literal_or': r'or',
        'location': r'(?: ?(from|on|that are in) (?P<location>.+?))',
        'n': r'(?P<n>(?:\d+|a|all|any \d+|the \d+|\s))',
        'on': r'on',
        'optional': r'?',
        'or': r'|',
        'players': r'(?P<players>\w+) players?'
    }

    increment = ['action', 'condition', 'item', 'location', 'n']

    component_count = {}
    patterns = []

    for component in components:
        pattern = component_regex[component]
        if component in increment:
            component_count[component] = component_count.get(component, 0) + 1
            pattern = pattern.replace('<'+component+'>',
                                      '<'+component+str(component_count[component])+'>')
        patterns.append(pattern)

    return patterns


def get_power_regex(power: str) -> str:
    power_components = {
        # DONE
        'all': ['players', 'action', 'n', 'item', 'location',
                'group', 'condition', 'action', 'n', 'item', 'location', 'end_group', 'optional',
                'assertion'],
        # DONE
        'discard': ['action', 'n', 'item', 'location', 'optional',  # Discard n item (from/on/that are in location)?
                    'entailment',                                   # to
                    'action', 'n', 'item', 'location', 'optional',  # action n item (from/on/that are in location)?
                    'assertion'],

        'draw': ['action', 'n', 'item', 'location', 'optional',  # Draw n card (from location)?
                 'group', 'condition', 'end_group', 'optional',  # (condition)?
                 'assertion'],

        'each': [],

        'gain': ['action', 'n', 'item',                                   # Gain n food1
                 'group', 'literal_or', 'item', 'end_group', 'optional',  # (or food2)?
                 'location', 'optional',                                  # from?
                 'assertion'],
        'if': [],
        'lay': [],
        'look': [],
        'play': [],
        'player(s)': [],
        'repeat': [],
        'roll': [],
        'trade': [],
        'tuck': [],
        'when': []

    }

    components = power_components[power]
    component_regex = get_component_regex(components)

    power_regex = ''
    optional_space_components = ['n']
    rstrip_components = ['assertion', 'end_group', 'group', 'location', 'optional', 'or']
    for component, regex in zip(components, component_regex):
        if component in optional_space_components:
            power_regex = power_regex.rstrip()
            power_regex += '\s?'+regex+'\s?'
        elif component in rstrip_components:
            power_regex = power_regex.rstrip()
            power_regex += regex+' ' if component not in ['optional', 'or'] else regex
        else:
            power_regex += regex+' ' if component not in ['group'] else regex

    return power_regex.rstrip()


def regex_group_dict(text: str, regex: str) -> Optional[Dict[str, AnyStr]]:
    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.match(text)

    match_dict = match.groupdict() if match else None

    if match_dict and 'entailment' in match_dict:
        match_dict['entailment'] = True

    return match_dict


def parse_bird_powers(df: pd.DataFrame) -> List[str]:
    first_word_map = parse_first_word_dict(df)


if __name__ == '__main__':
    fw = parse_first_word_dict(bird_df)
    power = 'all'
    regex = get_power_regex(power)
    print(regex)
    for text in fw[power]:
        print(text)
        print(regex_group_dict(text, regex))
        print()

    print('')

"""NOTES

all/each/... need to be folded into player component
draw needs to be solved fully for short text and brant
gain needs literals? or at least literal "or"

"""
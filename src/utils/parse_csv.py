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
        'action': r'(?P<action>play|gain|lay|draw|cache|discard|keep|look at|trade|tuck)',
        'assertion': r'\.$',
        'condition': r'(?P<condition>at .+?)',
        'else': r'if not,',
        'end_group': r')',
        'entailment': r'(?P<entailment>\s?(and|to|if you do,( also)?|you may)\s?)',
        'group': r'(',
        'if_ws': r'if (?P<if_ws>(\<|\>)\d+cm,)',
        'item': r'(?P<item>(face-up )?(?:\[.+?\]|it|new bonus cards?))\.?',
        'literal_or': r'or',
        'location': r'(?:\s?(behind|from|in|on|that are in|under) (?P<location>.+?))',
        'n': r'(?P<n>(?:\d+|a|all|any \d+|for any other|the \d+|\s))',
        'on': r'on',
        'optional': r'?',
        'or': r'|',
        'players': r'(?P<players>\w+) players?'
    }

    increment = ['action', 'condition', 'entailment', 'if_ws', 'item', 'location', 'n']

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
        # players action n item location (-> action n item location)?
        'all': ['players', 'action', 'n', 'item', 'location',
                'group', 'entailment', 'action', 'n', 'item', 'location',
                'end_group', 'optional', 'assertion'],
        # DONE
        # action n item location? -> action n item location?
        'discard': ['action', 'n', 'item', 'location', 'optional',
                    'entailment',
                    'action', 'n', 'item', 'location', 'optional',
                    'assertion'],
        # DONE
        # action n item location? (-> action n (item location condition)?)?
        'draw': ['action', 'n', 'item', 'location', 'optional',
                 'group', 'entailment', 'action', 'n',
                 'group', 'item', 'location', 'condition',
                 'end_group', 'optional', 'end_group', 'optional',
                 'assertion'],

        'each': [],
        # DONE
        # action n item (or item)? location (-> action n item location)?
        'gain': ['action', 'n', 'item',
                 'group', 'literal_or', 'item', 'end_group', 'optional',
                 'location',
                 'group', 'entailment', 'action', 'n', 'item', 'location',
                 'end_group', 'optional', 'assertion'],
        # TODO
        #
        'if': [],
        # DONE
        # action n item location
        'lay': ['action', 'n', 'item', 'location', 'assertion'],
        # DONE
        # look_deck if_ws action item location else action item
        'look': ['action', 'n', 'item', 'location',
                 'if_ws', 'action', 'item', 'location',
                 'else', 'action', 'item', 'assertion'],
        # TODO
        #
        'play': [],
        # TODO
        #
        'player(s)': [],
        # TODO
        #
        'repeat': [],
        # TODO
        #
        'roll': [],
        # DONE
        # action n item n item location
        'trade': ['action', 'n', 'item', 'n', 'item', 'location', 'assertion'],
        # DONE
        # action n item location -> action n item location?
        'tuck': ['action', 'n', 'item', 'location', 'entailment',
                 'action', 'n', 'item', 'location', 'optional', 'assertion'],
        # TODO
        #
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
            power_regex += regex+' ' if component not in ['group', 'optional', 'or'] else regex
        else:
            power_regex += regex+' '

    return power_regex.rstrip()


def regex_group_dict(text: str, regex: str) -> Optional[Dict[str, AnyStr]]:
    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.match(text)

    match_dict = match.groupdict() if match else None

    return match_dict


def parse_bird_powers(df: pd.DataFrame) -> List[str]:
    first_word_map = parse_first_word_dict(df)


if __name__ == '__main__':
    fw = parse_first_word_dict(bird_df)
    powers = ['all', 'discard', 'draw', 'gain', 'lay', 'look', 'trade', 'tuck']
    for power in powers:
        regex = get_power_regex(power)
        print(regex)
        for text in fw[power]:
            print(text)
            print(regex_group_dict(text, regex))
            print()

        print('')

"""NOTES

all/each/... need to be folded into players component
"""
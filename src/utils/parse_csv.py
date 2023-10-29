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
        'action': r'(?P<action>play|gain|lay|draw|cache|discard|keep|tuck)',
        'assertion': r'\.$',
        'condition': r'(?P<condition>at .+?)',
        'end_group': r')',
        'entailment': r'(?P<entailment>\s?(and|to|if you do,|you may)\s?)',
        'group': r'(',
        'if': r'',
        'item': r'(?P<item>(face-up )?(?:\[.+?\]|it|new bonus cards?))\.?',
        'literal_or': r'or',
        'location': r'(?:\s?(from|in|on|that are in) (?P<location>.+?))',
        'n': r'(?P<n>(?:\d+|a|all|any \d+|the \d+|\s))',
        'on': r'on',
        'optional': r'?',
        'or': r'|',
        'players': r'(?P<players>\w+) players?'
    }

    increment = ['action', 'condition', 'entailment', 'item', 'location', 'n']

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
        'all': ['players', 'action', 'n', 'item', 'location',    # Players action n item from/on location
                'group',                                         # (
                'condition', 'action', 'n', 'item', 'location',  # (condition action n item from/on location)?
                'end_group', 'optional',                         # )?
                'assertion'],
        # DONE
        'discard': ['action', 'n', 'item', 'location', 'optional',  # Discard n item (from/on location)?
                    'entailment',                                   # in order to
                    'action', 'n', 'item', 'location', 'optional',  # action n item (from/on location)?
                    'assertion'],
        # DONE (could maybe be prettier)
        'draw': ['action', 'n', 'item', 'location', 'optional',
                 'group',
                 'entailment', 'action', 'n',
                 'group',
                 'item', 'location', 'condition',
                 'end_group', 'optional',
                 'end_group', 'optional',
                 'assertion'],

        'each': [],
        # DONE TODO verify
        'gain': ['action', 'n', 'item',
                 'group', 'literal_or', 'item', 'end_group', 'optional',
                 'location',
                 'group', 'entailment', 'action', 'n', 'item', 'location', 'end_group', 'optional',
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
    power = 'gain'
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
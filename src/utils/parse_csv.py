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
        'action': r'(?P<action>\w+)',
        'assertion': r'\.?$',
        'condition': r'(?P<condition>.+)',
        'end_group': r')',
        'from': r'from',
        'group': r'(',
        'if': r'',
        'item': r'(?P<item>()?\[.*?\]|new bonus cards?)',
        'location': r'(?P<location>.+?)',
        'n': r'(?P<n>\d+|a|\s|the \d+)',
        'on': r'on',
        'opt_from_loc': r'( from (?P<location>.+?))?',
        'optional': r'?',
        'or': r'|',
        'to': r'to',
    }

    increment = ['action', 'condition', 'item', 'location', 'n', 'opt_from_loc']

    component_count = {}
    patterns = []

    for component in components:
        pattern = component_regex[component]
        if component in increment:
            if component == 'opt_from_loc':
                component = 'location'
            component_count[component] = component_count.get(component, 0) + 1
            pattern = pattern.replace('<'+component+'>',
                                      '<'+component+str(component_count[component])+'>')
        patterns.append(pattern)

    return patterns


def get_power_regex(power: str) -> str:
    prefix_phrases = {
        'all': r'^All players',
        'discard': r'^Discard',
        'draw': r'^Draw'
    }
    power_components = {
        'all': ['action', 'n', 'item', 'group', 'from', 'location', 'or', 'on', 'condition', 'end_group', 'assertion'],
        'discard': ['n', 'item', 'opt_from_loc', 'to', 'action', 'n', 'item', 'opt_from_loc', 'assertion'],
        'draw': ['n', 'item', 'opt_from_loc', 'group', 'condition', 'end_group', 'optional', 'assertion'],
        'each': [],
        'gain': [],
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
    components.insert(0, None)
    component_regex.insert(0, prefix_phrases[power])

    power_regex = ''
    rstrip_components = ['assertion', 'end_group', 'opt_from_loc', 'optional', 'or']

    for component, regex in zip(components, component_regex):
        if component == 'group':
            power_regex += regex
        elif component in rstrip_components:
            power_regex = power_regex.rstrip()
            power_regex += regex+' ' if component not in ['or'] else regex
        else:
            power_regex += regex+' '

    return power_regex.rstrip()


def regex_group_dict(text: str, regex: str) -> Optional[Dict[str, AnyStr]]:
    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.match(text)

    return match.groupdict() if match else None


def parse_bird_powers(df: pd.DataFrame) -> List[str]:
    first_word_map = parse_first_word_dict(df)


if __name__ == '__main__':
    fw = parse_first_word_dict(bird_df)
    power = 'draw'
    regex = get_power_regex(power)
    print(regex)
    for text in fw[power]:
        print(text)
        print(regex_group_dict(text, regex))

    print('')

from dotenv import load_dotenv
import os
import pandas as pd
import re

from src.game.enums.bird_power_types import ComponentType as ct
from src.game.enums.bird_power_types import *
from src.utils.post_processing import *

from typing import AnyStr, Dict, List, Optional

load_dotenv()
bird_csv_path = os.environ['BIRD_CSV']
bird_df = pd.read_csv(bird_csv_path)

INCREMENT_COMPONENTS = ct.list_from_names(['ACTION', 'CONDITION', 'ENTAILMENT', 'IF',
                                           'IF_WS', 'ITEM', 'LOCATION', 'N', 'WHEN_COND'])


def get_unique_power_categories(df: pd.DataFrame) -> List[str]:
    uniques = df['power_category'].unique()
    return uniques.tolist()


def parse_first_word_dict(df: pd.DataFrame) -> Dict[str, List[str]]:
    power_list = df['power_text'].tolist()
    res_dict = dict()

    for text in power_list:
        if not isinstance(text, str):
            if 'none' in res_dict:
                res_dict['none'].append('')
            else:
                res_dict['none'] = ['']
            continue

        text = text.upper()
        first_word = strip_parens(text.split(' ')[0].upper())
        if first_word in res_dict:
            res_dict[first_word].append(text)
        else:
            res_dict[first_word] = [text]

    return res_dict


def get_component_regex(components: List[str]) -> List[str]:
    # component_regex = {
    #     'action': r'(?P<action>play|gains?|lays?|draw|cache|discard|keep|look at|move|repeat|roll|trade|tuck)',
    #     'assertion': r'\.$',
    #     'condition': r'(?P<condition>are .+?,?|at .+?|if they .+?|pay .+?|starting .+?|with (the )?.+?:?)',
    #     'else': r'if not,',
    #     'end_group': r')',
    #     'entailment': r'(?P<entailment>\s?(also|and|to|if you do,( also)?|you may)\s?)',
    #     'group': r'(',
    #     'if': r'(?P<if>if)',
    #     'if_ws': r'if (?P<if_ws>(\<|\>)\d+cm,)',
    #     'item': r'(?P<item>(face-up )?(?:\[.+?\]|bird|dice|it|new bonus cards?))\.?',
    #     'location': r'(\s?(?P<location>(?:not\s)?(?:behind|from|(that are )?in|on|(is )?to|under)\s?.+?)\.?)',
    #     'n': r'(?P<n>(?:\d+|a( \w+)?|all|any( \d+)?|for any other|this|the \d+|\s))',
    #     'on': r'on',
    #     'optional': r'?',
    #     'or': r'|',
    #     'power': r'(?P<power>brown|pink|predator|white|\[.+?\])( power)?',
    #     'players': r'(?P<players>player\(s\)|\w+)( player\'?s?)?',
    #     'when': r'(?P<when>when)',
    #     'when_cond': r'(?P<when_cond>takes the \"(.+?)\" action|plays a \[.+?\] bird|predator succeeds),?',
    # }
    #
    # increment = ['action', 'condition', 'entailment', 'if', 'if_ws', 'item', 'location', 'n', 'when_cond']

    component_count = {}
    patterns = []

    for component in components:
        regex = ComponentMapper.get_regex(component).value
        if component in INCREMENT_COMPONENTS:
            component_count[component] = component_count.get(component, 0) + 1
            regex = regex.replace('<'+component.value+'>',
                                  '<'+component.value+str(component_count[component])+'>')
        patterns.append(regex)

    return patterns


def get_power_regex(power: str) -> str:
    # power_components = {
    #     # DONE
    #     # players action n item location (-> action n item location)?
    #     'all': ['players', 'action', 'n', 'item', 'location',
    #             'group', 'entailment', 'action', 'n', 'item', 'location',
    #             'end_group', 'optional', 'assertion'],
    #     # DONE
    #     # action n item location? -> action n item location?
    #     'discard': ['action', 'n', 'item', 'location', 'optional',
    #                 'entailment',
    #                 'action', 'n', 'item', 'location', 'optional',
    #                 'assertion'],
    #     # DONE
    #     # action n item location? (-> action n (item location condition)?)?
    #     'draw': ['action', 'n', 'item', 'location', 'optional',
    #              'group', 'entailment', 'action', 'n',
    #              'group', 'item', 'location', 'condition',
    #              'end_group', 'optional', 'end_group', 'optional',
    #              'assertion'],
    #     # DONE
    #     # players action n item location condition
    #     'each': ['players', 'action', 'n', 'item', 'location', 'condition', 'assertion'],
    #     # DONE
    #     # action n item (or item)? location (-> action n item location)?
    #     'gain': ['action', 'n', 'item', 'location',
    #              'group', 'entailment', 'action', 'n', 'item', 'location',
    #              'end_group', 'optional', 'assertion'],
    #     # DONE
    #     # if n item location action n location
    #     'if': ['if', 'n', 'item', 'location', 'action', 'item', 'location', 'assertion'],
    #     # DONE
    #     # action n item location
    #     'lay': ['action', 'n', 'item', 'location', 'assertion'],
    #     # DONE
    #     # action n item location if_ws action item location else action item
    #     'look': ['action', 'n', 'item', 'location',
    #              'if_ws', 'action', 'item', 'location',
    #              'else', 'action', 'item', 'assertion'],
    #     # DONE
    #     # action n item location condition
    #     'play': ['action', 'n', 'item', 'location', 'condition', 'assertion'],
    #     # DONE
    #     # players condition action n item location?
    #     'player(s)': ['players', 'condition', 'action', 'n', 'item', 'location', 'optional', 'assertion'],
    #     # DONE
    #     # action n power location
    #     'repeat': ['action', 'n', 'power', 'location', 'assertion'],
    #     # DONE
    #     # action n item location if n condition action n item -> action item location
    #     'roll': ['action', 'n', 'item', 'location',
    #              'if', 'n', 'condition', 'action', 'n', 'item',
    #              'entailment', 'action', 'item', 'location', 'assertion'],
    #     # DONE
    #     # action n item n item location
    #     'trade': ['action', 'n', 'item', 'n', 'item', 'location', 'assertion'],
    #     # DONE
    #     # action n item location -> action n item location?
    #     'tuck': ['action', 'n', 'item', 'location', 'entailment',
    #              'action', 'n', 'item', 'location', 'optional', 'assertion'],
    #     # DONE, TODO make less insane??
    #     # when players when_cond ((n item action n item location)|(action, n, item, location)|
    #     #                         (condition -> action n item location -> action item location))
    #     'when': ['when', 'players', 'when_cond',
    #              'group',
    #              'group', 'n', 'item', 'action', 'n', 'item', 'location', 'end_group', 'or',
    #              'group', 'action', 'n', 'item', 'location', 'end_group', 'or',
    #              'group', 'condition', 'entailment', 'action', 'n', 'item', 'location',
    #              'entailment', 'action', 'item', 'location', 'end_group',
    #              'end_group',
    #              'assertion'],
    #
    # }
    power_type = PowerType[power]
    components = PowerMapper.get_components(power_type)
    component_regex = get_component_regex(components)

    power_regex = ''
    optional_space_components = [ct.N]
    rstrip_components = [ct.ASSERTION, ct.END_GROUP, ct.GROUP, ct.LOCATION, ct.OPTIONAL, ct.OR]
    for component, regex in zip(components, component_regex):
        if component in optional_space_components:
            power_regex = power_regex.rstrip()
            power_regex += '\s?'+regex+'\s?'
        elif component in rstrip_components:
            power_regex = power_regex.rstrip()
            power_regex += regex+' ' if component not in [ct.OPTIONAL, ct.OR] else regex
        else:
            power_regex += regex+' '

    return power_regex.rstrip()


def regex_group_dict(text: str, regex: str) -> Optional[Dict[str, AnyStr]]:
    pattern = re.compile(regex, re.IGNORECASE)
    match = pattern.match(text)

    match_dict = match.groupdict() if match else None

    return match_dict


def parse_bird_powers() -> List[Dict[str, str]]:
    fw_map = parse_first_word_dict(bird_df)
    args_list = [regex_group_dict(text, get_power_regex(power))
                 if power != 'none' else {}
                 for power in fw_map.keys()
                 for text in fw_map[power]]
    return args_list


def post_process(arg_dicts: List[Dict[str, str]]):
    for args in arg_dicts:
        if not args:
            continue

        remove_keys = []

        for k, v in args.items():
            if not v or v == ' ':
                remove_keys.append(k)
            elif ct.ACTION.value in k:
                continue
            elif ct.CONDITION.value in k:
                pass
            elif ct.ENTAILMENT.value in k:
                args[k] = parse_entailment(v)
            elif ct.IF_WS.value in k:
                pass
            elif ct.IF.value in k:
                pass
            elif ct.ITEM.value in k:
                args[k] = parse_item(v)
            elif ct.LOCATION.value in k:
                args[k] = parse_location(v)
            elif ct.N == k:
                args[k] = parse_n(v)
            elif ct.WHEN_COND.value in k:
                pass
            else:
                continue

        # Link args labelled PREVIOUS to previously indexed arg
        for prev in {k: v for k, v in args.items() if v == 'PREVIOUS'}:
            # String of decremented index of the arg with value PREVIOUS
            idx = str(int(''.join(re.findall(r'\d+', prev))) - 1)
            arg = ''.join(re.findall(r'\D+', prev))
            args[prev] = arg+idx

        for k in remove_keys:
            args.pop(k)

    return arg_dicts


def parse_csv() -> pd.DataFrame:
    bird_power_args = parse_bird_powers()
    post_process(bird_power_args)
    bird_df['power_args'] = bird_power_args
    bird_df['color'] = bird_df['color'].fillna('None')
    bird_df['power_text'] = bird_df['power_text'].fillna('')
    return bird_df


if __name__ == '__main__':
    birds = parse_csv()
    re_list = parse_bird_powers()
    print(re_list)
    # fw = parse_first_word_dict(bird_df)
    # powers = [key.lower() for key in fw.keys()]
    # for power in powers:
    #     regex = get_power_regex(power)
    #     print(regex)
    #     for text in fw[power]:
    #         print(text)
    #         print(regex_group_dict(text, regex))

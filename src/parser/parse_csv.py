from dotenv import load_dotenv
import os
import pandas as pd
import re

from src.parser.enums.power_component_types import *
from src.parser.post_processing import *

from typing import AnyStr, Dict, List, Optional

load_dotenv()
bird_csv_path = os.environ['BIRD_CSV']
bird_df = pd.read_csv(bird_csv_path)

INCREMENT_COMPONENTS = ComponentType.list_from_names(
    ['ACTION', 'CONDITION', 'ENTAILMENT', 'IF',
     'IF_WS', 'ITEM', 'LOCATION', 'N', 'WHEN_COND']
)


def get_unique_power_categories(df: pd.DataFrame) -> List[str]:
    uniques = df['power_category'].unique()
    return uniques.tolist()


def parse_first_word_dict(df: pd.DataFrame) -> Dict[str, List[str]]:
    power_list = df['power_text'].tolist()
    res_dict = dict()

    for text in power_list:
        if not isinstance(text, str) or not text:
            NONE = 'NONE'
            if NONE in res_dict:
                res_dict[NONE].append(NONE)
            else:
                res_dict[NONE] = [NONE]
            continue

        text = text.upper()
        first_word = strip_parens(text.split(' ')[0].upper())
        if first_word in res_dict:
            res_dict[first_word].append(text)
        else:
            res_dict[first_word] = [text]

    return res_dict


def get_component_regex(components: List[str]) -> List[str]:
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
    power_type = PowerType[power]
    components = PowerMapper.get_components(power_type)
    component_regex = get_component_regex(components)

    power_regex = ''
    optional_space_components = [ComponentType.N]
    rstrip_components = [ComponentType.ASSERTION, ComponentType.END_GROUP, ComponentType.GROUP, ComponentType.LOCATION, ComponentType.OPTIONAL, ComponentType.OR]
    for component, regex in zip(components, component_regex):
        if component in optional_space_components:
            power_regex = power_regex.rstrip()
            power_regex += '\s?'+regex+'\s?'
        elif component in rstrip_components:
            power_regex = power_regex.rstrip()
            power_regex += regex+' ' if component not in [ComponentType.OPTIONAL, ComponentType.OR] else regex
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
                 if power != 'NONE' else {}
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
            elif ComponentType.ACTION.value in k:
                continue
            elif ComponentType.CONDITION.value in k:
                pass
            elif ComponentType.ENTAILMENT.value in k:
                args[k] = parse_entailment(v)
            elif ComponentType.IF_WS.value in k:
                pass
            elif ComponentType.IF.value in k:
                pass
            elif ComponentType.ITEM.value in k:
                args[k] = parse_item(v)
            elif ComponentType.LOCATION.value in k:
                args[k] = parse_location(v)
            elif ComponentType.N == k:
                args[k] = parse_n(v)
            elif ComponentType.WHEN_COND.value in k:
                pass
            else:
                continue

        # Link args labelled PREVIOUS to previously indexed arg
        for prev in {k: v for k, v in args.items() if (v and v[0] == Item.PREVIOUS.value)}:
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

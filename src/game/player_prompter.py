from enum import Enum

from typing import Any, Dict, List


class Prompt(Enum):
    PLAYER_NAME = 'Enter player name:'
    GAIN = 'Gain $N $ITEM from $LOCATION'
    LAY = 'Lay $N $ITEM on $LOCATION'
    DRAW = 'Draw $N $ITEM from $LOCATION'


class Prompter:
    def __init__(self):
        self._prompts = {
            'PLAYER_NAME': Prompt.PLAYER_NAME,
            'GAIN_FOOD': Prompt.GAIN,
            'LAY_EGGS': Prompt.LAY,
            'DRAW_CARDS': Prompt.DRAW,
        }

    @staticmethod
    def _fill_args(prompt: Prompt, args: Dict[str, str]) -> str:
        prompt_str: str = prompt.value
        split_prompt = prompt_str.split(' ')
        filled_prompt = []
        for splt in split_prompt:
            if splt.startswith('$'):
                splt = splt.removeprefix('$')
                filled_prompt.append(args[splt])
            else:
                filled_prompt.append(splt)
        return ' '.join(filled_prompt)

    def _from_user(self, prompt: str) -> Any:
        choice = input(prompt)
        return choice

    def get_players(self, n: int) -> List[str]:
        players = []

        for _ in range(n):
            prompt = self._prompts['PLAYER_NAME'].value
            player_name = self._from_user(prompt)
            players.append(player_name)

        return players

    def prompt(self, args: Dict[str, str]) -> Any:
        prompt_type = args['TYPE']
        prompt = self._prompts[prompt_type]
        text = self._fill_args(prompt, args)

        return self._from_user(text)


if __name__ == '__main__':
    p = Prompter()
    p.prompt({'TYPE': 'GAIN_FOOD', 'N': '1', 'ITEM': 'WILD', 'LOCATION': 'SUPPLY'})


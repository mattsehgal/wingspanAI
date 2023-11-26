from enum import Enum

from typing import Any, Dict, List


class Prompt(Enum):
    STARTUP = 'Welcome to WingspanAI\'s simulator.\nPress [ENTER] to begin.'
    PLAYER_NAME = 'Enter player name:\t'
    PLAYER_NUM = 'Enter number of players:\t'
    GAIN = 'Gain $N $ITEM from $LOCATION'
    LAY = 'Lay $N $ITEM on $LOCATION'
    DRAW = 'Draw $N $ITEM from $LOCATION'


class Prompter:
    def __init__(self):
        self._prompts = {
            'STARTUP': Prompt.STARTUP,
            'PLAYER_NAME': Prompt.PLAYER_NAME,
            'PLAYER_NUM': Prompt.PLAYER_NUM,
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

    def get_players(self) -> List[str]:
        _ = self.prompt({'TYPE': 'STARTUP'})
        players = []
        n = int(self.prompt({'TYPE': 'PLAYER_NUM'}))

        for _ in range(n):
            name = self.prompt({'TYPE': 'PLAYER_NAME'})
            players.append(name)

        return players

    def prompt(self, args: Dict[str, str]) -> Any:
        prompt_type = args['TYPE']
        prompt = self._prompts[prompt_type]
        if any(['$' in v for k, v in args.items()]):
            text = self._fill_args(prompt, args)
        else:
            text = prompt.value

        return self._from_user(text)


if __name__ == '__main__':
    p = Prompter()
    p.prompt({'TYPE': 'GAIN_FOOD', 'N': '1', 'ITEM': 'WILD', 'LOCATION': 'SUPPLY'})


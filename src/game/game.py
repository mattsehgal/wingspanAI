import random

from bird_card import BirdCard
from bonus_card import BonusCard
from player import Player
from state import *

from typing import Dict, List


class Game:
    def __init__(self, player_names):
        self.players = self._init_players(player_names)
        self._set_player_order()
        self.current_player = self.players[0]

        self.bird_deck = self._init_bird_deck()
        self.bonus_deck = self._init_bonus_deck()

        self.round_number = 1
        self.rounds = 4

        self.state = self._get_state()
        self.previous_states = []

    @staticmethod
    def _init_players(names) -> List[Player]:
        players = [Player(name) for name in names]
        return players

    def _set_player_order(self) -> None:
        random.shuffle(self.players)

    def _init_bird_deck(self) -> List[BirdCard]:
        pass

    def _init_bonus_deck(self) -> List[BonusCard]:
        pass

    def _get_state(self) -> GameState:
        return GameState(self)

    def _is_game_over(self):
        return self.round_number > self.rounds

    def get_player_input(self, prompt: str, args: Dict[str, str] = {}) -> str:
        if prompt == 'gain_food':
            pass
            # input(f"{}")
        elif prompt == 'lay_eggs':
            pass
        elif prompt == 'draw_cards':
            pass
        elif prompt == 'exchange':
            pass

        # choose
            # food to gain
            # bird to lay egg on
                # bird to remove egg from (pass negatives to the above?)
            # where to draw
            # card to keep
                # card to discard/tuck
            # item to exchange

    def next_turn(self):
        pass

    def play(self):
        while not self.is_game_over():
            self.next_turn()

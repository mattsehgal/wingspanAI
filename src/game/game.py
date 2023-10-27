import random

#from bird_card import BirdCard
from bonus_card import BonusCard
from player import Player

from typing import List


class Game:
    def __init__(self, player_names):
        self.players = self._init_players(player_names)
        self._set_player_order()
        self.current_player = self.players[0]

        self.bird_deck = self._init_bird_deck()
        self.bonus_deck = self._init_bonus_deck()

        self.round_number = 1
        self.rounds = 4

    @staticmethod
    def _init_players(names) -> List[Player]:
        players = [Player(name) for name in names]
        return players

    def _set_player_order(self) -> Player:
        random.shuffle(self.players)

    def _init_bird_deck(self) -> List[BirdCard]:
        pass

    def _init_bonus_deck(self) -> List[BonusCard]:
        pass

    def _is_game_over(self):
        return self.round_number > self.rounds

    def next_turn(self):
        pass

    def play(self):
        while not self.is_game_over():
            self.next_turn()

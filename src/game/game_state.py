import random

from bird_feeder import BirdFeeder
from board import Board
from deck import BirdDeck, BonusDeck
from player import Player
from round_goals import RoundGoalsBoard

from typing import Dict, List


class GameState:
    def __init__(self, player_names: List[str]):
        # Players
        self.players: List[Player] = [Player(_id, name) for _id, name in enumerate(player_names)]
        self.player_boards: Dict[int, Board] = {player.id: player.board for player in self.players}
        random.shuffle(self.players)  # Set player order
        self.current_player = self.players[0]
        # Game components
        self.bird_deck = BirdDeck()
        self.bonus_deck = BonusDeck()
        self.bird_feeder = BirdFeeder()
        self.round_goals = RoundGoalsBoard()
        # Game variables
        self.round_number = 1
        self.rounds = 4

    def play_bird(self, bird_id: int, habitat: str) -> bool:
        player = self.current_player
        return player.play_bird(bird_id, habitat)

    def gain_food(self, food_tokens: Dict[str, int], location: str) -> bool:
        player = self.current_player
        if location == 'bird_feeder':
            self.bird_feeder.gain_food(food_tokens)
        return player.gain_food(food_tokens)

    def lay_eggs(self, bird_id_n: Dict[int, int]):
        player = self.current_player
        return player.lay_eggs(bird_id_n)

    def draw_cards(self, card_choices: Dict[str, int]) -> bool:
        player = self.current_player
        drawn_cards = []
        for location, n_or_id in card_choices.items():
            if location == 'tray':
                bird_card = self.bird_deck.draw(n_or_id)
            else:
                bird_card = self.bird_deck.draw()
            drawn_cards.append(bird_card)
        return player.add_bird_cards(drawn_cards)

    def draw_bonus_cards(self, n: int) -> bool:
        player = self.current_player
        drawn_cards = self.bonus_deck.draw(n)
        player.add_bonus_cards(drawn_cards)


if __name__ == '__main__':
    s = GameState(['p1'])
    print(s)
import random

from src.game.bird_feeder import BirdFeeder
from src.game.board import Board
from src.game.deck import BirdDeck, BonusDeck
from src.game.player import Player
from src.game.round_goals import RoundGoalsBoard, RoundGoal

from typing import Dict, List, Optional


class GameState:
    def __init__(self, player_names: List[str]):
        # Players
        self.players: Dict[int, Player] = {_id: Player(_id, name) for _id, name in enumerate(player_names)}
        self.player_boards: Dict[int, Board] = {player.id: player.board for _, player in self.players.items()}
        random.shuffle(self.players)  # Set player order
        self.current_player = self.players[0]
        # Game components
        self.bird_deck = BirdDeck()
        self.bonus_deck = BonusDeck()
        self.bird_feeder = BirdFeeder()
        self.round_goals = RoundGoalsBoard()

    def _get_player(self, player_id: Optional[int]) -> Player:
        if player_id:
            return self.player[player_id]
        else:
            return self.current_player

    def play_bird(self, bird_id: int, habitat: str, player_id: int = None) -> bool:
        player = self._get_player(player_id)
        return player.play_bird(bird_id, habitat)

    def gain_food(self, food_tokens: Dict[str, int], location: str, player_id: int = None) -> bool:
        player = self._get_player(player_id)
        if location == 'BIRDFEEDER':
            self.bird_feeder.gain_food(food_tokens)
        return player.gain_food(food_tokens)

    def lay_eggs(self, bird_id_n: Dict[int, int], player_id: int = None) -> bool:
        player = self._get_player(player_id)
        return player.lay_eggs(bird_id_n)

    def draw_cards(self, card_choices: Dict[str, int], player_id: int = None) -> bool:
        player = self._get_player(player_id)
        drawn_cards = []
        for location, n_or_id in card_choices.items():
            if location == 'TRAY':
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
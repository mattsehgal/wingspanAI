from bird_card import BirdCard
from bonus_card import BonusCard
from bird_feeder import BirdFeeder
from board import Board
from game import Game
from player import Player

from typing import Dict, List


class State:
    def __init__(self):
        pass


class BirdFeederState(State):
    def __init__(self, bird_feeder: BirdFeeder):
        self.in_dice: List[str] = [die.current_face for die in bird_feeder.dice_in]
        self.out_dice: List[str] = [die.current_face for die in bird_feeder.dice_out]


class BoardState(State):
    def __init__(self, board: Board):
        # Could become PlayerState
        self.player: Player = board.player
        self.player_id: int = self.player.id
        self.bird_cards: Dict[int, BirdCard] = {bird_card.id: bird_card for bird_card in self.player.bird_cards}
        self.bonus_cards: Dict[int, BonusCard] = {bonus_card.id: bonus_card for bonus_card in self.player.bonus_cards}
        self.food_tokens: Dict[str, int] = self.player.food_tokens
        # Board Spaces


class GameState(State):
    def __init__(self, game: Game):
        self.bird_feeder_state: BirdFeederState = BirdFeederState(game.bird_feeder)
        self.board_states: List[BoardState] = [BoardState(player.board) for player in game.players]
        self.tray_state: List[int] = [bird.id for bird in game.bird_deck.tray]




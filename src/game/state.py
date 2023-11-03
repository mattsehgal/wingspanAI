from typing import Dict, List


class State:
    def __init__(self):
        pass


class BirdFeederState(State):
    def __init__(self, bird_feeder):
        self.in_dice: List[str] = [die.current_face for die in bird_feeder.dice_in]
        self.out_dice: List[str] = [die.current_face for die in bird_feeder.dice_out]


class BoardState(State):
    def __init__(self, board):
        # Could become PlayerState
        self.player = board.player
        self.player_id = self.player.id
        self.bird_cards = {bird_card.id: bird_card for bird_card in self.player.bird_cards}
        self.bonus_cards = {bonus_card.id: bonus_card for bonus_card in self.player.bonus_cards}
        self.food_tokens = self.player.food_tokens
        # Board Spaces


class DeckState(State):
    def __init__(self, deck):
        self.tray = deck.tray


class GameState(State):
    def __init__(self, game):
        self.bird_feeder_state: BirdFeederState = BirdFeederState(game.bird_feeder)
        self.board_states: List[BoardState] = [BoardState(player.board) for player in game.players]
        self.tray_state: DeckState = DeckState(game.bird_deck)




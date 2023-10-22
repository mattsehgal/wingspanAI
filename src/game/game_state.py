

class GameState:
    def __init__(self, game):
        self.players = game.players
        self.current_player = game.current_player

        self.current_board = self.current_player.board

        self.tray = game.tray
        self.bird_deck = game.bird_deck
        self.bonus_deck = game.bonus_deck

    def to_vector(self):
        pass

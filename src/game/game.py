

class Game:
    def __init__(self, players):
        self.players = players
        # self.current_player =
        self.bird_deck = self.init_bird_deck()
        self.bonus_deck = self.init_bonus_deck()
        self.round_number = 1
        self.rounds = 4

    def init_bird_deck(self):
        pass

    def init_bonus_deck(self):
        pass

    def next_turn(self):
        pass

    def is_game_over(self):
        return self.round_number > self.rounds

    def play(self):
        while not self.is_game_over():
            self.next_turn()
